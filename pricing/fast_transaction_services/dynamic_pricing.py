"""
Dynamic-pricing engine for the fast-transaction-service case study.

This module turns an *estimated demand curve* into pricing decisions, and then
shows how to price **dynamically** as load and demand change in real time.

Three layers, from textbook to production:

1.  **Static profit optimisation** (``lerner_optimal_fee`` / ``profit_curve``).
    The closed-form monopoly markup from the elasticity, plus a grid search.
    Pricing on the *causal* (IV) elasticity finds the true optimum; pricing on a
    *biased* (OLS) elasticity does not.

2.  **Rule-based surge** (``SurgeController``). A real-time controller that lifts
    the fee when system load is high -- justified here because marginal
    cost-to-serve rises with utilisation -- with explicit guardrails: a fee
    floor/cap, a surge cap, and a per-step rate limit so prices never whipsaw.

3.  **Learning controllers** (``ThompsonBanditController``,
    ``EpsilonGreedyController``). Contextual bandits that *learn* the best fee
    per load state online, trading exploration for exploitation. We score them
    by cumulative profit and regret against a load-aware oracle.

The "environment" (``TxnPricingEnv``) holds the *true* structural parameters;
the controllers never see them -- they only see the rewards they earn, exactly
like a live pricing system.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import numpy as np
import pandas as pd


# ===========================================================================
#  1. STATIC PROFIT OPTIMISATION
# ===========================================================================
def lerner_optimal_fee(
    elasticity: float,
    unit_cost: float,
    avg_ticket: float,
    fee_bounds: tuple[float, float] = (0.001, 0.05),
) -> dict:
    """Profit-maximising % fee from the elasticity (Lerner / monopoly markup).

    Revenue per txn is ``p = fee * avg_ticket``; marginal cost is ``unit_cost``.
    For constant-elasticity demand the first-order condition is the Lerner rule
    ``(p - c) / p = -1 / elasticity`` => ``p* = c / (1 + 1/elasticity)``.

    Only valid when demand is **elastic** (``elasticity < -1``). If demand is
    inelastic (``-1 <= elasticity < 0``) the unconstrained optimum is unbounded,
    so the optimum is the cap -- a *corner solution* where guardrails/competition
    set the price, not the FOC. We flag that case.
    """
    lo, hi = fee_bounds
    if elasticity < -1.0:
        optimal_p = unit_cost / (1.0 + 1.0 / elasticity)      # revenue/txn
        fee = optimal_p / avg_ticket
        return {
            "optimal_fee": float(np.clip(fee, lo, hi)),
            "markup": -1.0 / elasticity,
            "corner_solution": False,
        }
    # Inelastic: FOC says "raise price"; the cap binds.
    return {
        "optimal_fee": float(hi),
        "markup": float("inf"),
        "corner_solution": True,
    }


def constant_elasticity_demand(
    fee: np.ndarray | float,
    elasticity: float,
    q_ref: float,
    fee_ref: float,
) -> np.ndarray | float:
    """Constant-elasticity demand calibrated to a reference point (fee_ref, q_ref)."""
    return q_ref * (np.asarray(fee, dtype=float) / fee_ref) ** elasticity


def profit_curve(
    elasticity: float,
    q_ref: float,
    fee_ref: float,
    unit_cost: float,
    avg_ticket: float,
    fee_grid: np.ndarray,
) -> pd.DataFrame:
    """Expected volume / revenue / profit across a grid of candidate fees."""
    volume = constant_elasticity_demand(fee_grid, elasticity, q_ref, fee_ref)
    revenue = fee_grid * avg_ticket * volume
    cost = unit_cost * volume
    profit = revenue - cost
    return pd.DataFrame(
        {"fee": fee_grid, "volume": volume, "revenue": revenue,
         "cost": cost, "profit": profit}
    )


def optimal_fee_grid(curve: pd.DataFrame) -> dict:
    """Pick the profit-maximising row from a ``profit_curve`` table."""
    i = int(curve["profit"].to_numpy().argmax())
    row = curve.iloc[i]
    return {"optimal_fee": float(row["fee"]), "optimal_profit": float(row["profit"])}


# ===========================================================================
#  2. THE LIVE ENVIRONMENT (holds the TRUE parameters)
# ===========================================================================
@dataclass
class TxnPricingEnv:
    """A single segment's live pricing environment.

    Demand is constant-elasticity around a reference point, scaled by a
    time-varying **demand state** ``m`` (>1 at peak). Crucially, the marginal
    cost to serve *rises with the demand state* (congestion / capacity pressure),
    which is what makes surge pricing genuinely profit-maximising rather than
    mere opportunism.
    """

    elasticity: float
    q_ref: float                 # reference volume at fee_ref, m=1
    fee_ref: float               # reference fee
    base_cost: float             # marginal cost to serve at m=1
    avg_ticket: float            # $ per transaction (fee is a % of this)
    congestion_kappa: float = 0.9  # how fast unit cost rises with load
    demand_noise: float = 0.05   # lognormal noise on realised volume
    fee_bounds: tuple[float, float] = (0.002, 0.04)

    @classmethod
    def calibrated(
        cls,
        elasticity: float,
        fee_ref: float,
        q_ref: float,
        avg_ticket: float,
        congestion_kappa: float = 0.9,
        **kwargs,
    ) -> "TxnPricingEnv":
        """Build an env whose Lerner optimum at average load (m=1) equals ``fee_ref``.

        We back-solve the *fully-loaded contribution cost* from the Lerner rule:
        ``base_cost = fee_ref * avg_ticket * (1 + 1/elasticity)``. This cost is
        deliberately larger than the raw processing cost -- in payments the
        contribution cost also carries fraud, support, capital and compliance, so
        the profit-maximising fee lands at a realistic level instead of near zero.
        Requires elastic demand (``elasticity < -1``).
        """
        if elasticity >= -1.0:
            raise ValueError("calibrated() needs elastic demand (elasticity < -1).")
        base_cost = fee_ref * avg_ticket * (1.0 + 1.0 / elasticity)
        return cls(
            elasticity=elasticity, q_ref=q_ref, fee_ref=fee_ref,
            base_cost=base_cost, avg_ticket=avg_ticket,
            congestion_kappa=congestion_kappa, **kwargs,
        )

    def unit_cost(self, m: float) -> float:
        """Marginal cost to serve at demand state ``m`` (rises above m=1)."""
        return self.base_cost * (1.0 + self.congestion_kappa * max(m - 1.0, 0.0))

    def expected_volume(self, fee: float, m: float) -> float:
        return m * constant_elasticity_demand(fee, self.elasticity, self.q_ref, self.fee_ref)

    def expected_profit(self, fee: float, m: float) -> float:
        vol = self.expected_volume(fee, m)
        margin = fee * self.avg_ticket - self.unit_cost(m)
        return margin * vol

    def realized_profit(self, fee: float, m: float, rng: np.random.Generator) -> dict:
        """Sample a noisy realised outcome for a chosen fee at demand state m."""
        exp_vol = self.expected_volume(fee, m)
        vol = exp_vol * rng.lognormal(mean=0.0, sigma=self.demand_noise)
        margin = fee * self.avg_ticket - self.unit_cost(m)
        return {"profit": margin * vol, "volume": vol, "fee": fee}

    def best_fee(self, m: float, fee_grid: np.ndarray) -> dict:
        """Oracle: the load-aware profit-maximising fee at demand state m."""
        profits = np.array([self.expected_profit(f, m) for f in fee_grid])
        i = int(profits.argmax())
        return {"fee": float(fee_grid[i]), "profit": float(profits[i])}


# ===========================================================================
#  3. CONTROLLERS
# ===========================================================================
class BaseController:
    name = "base"

    def act(self, context: int, m_hint: float) -> float:        # noqa: ARG002
        raise NotImplementedError

    def update(self, context: int, fee: float, reward: float) -> None:
        pass


class StaticController(BaseController):
    """Charges one fixed fee forever (the baseline)."""

    def __init__(self, fee: float, name: str = "static"):
        self.fee = float(fee)
        self.name = name

    def act(self, context: int, m_hint: float) -> float:
        return self.fee


@dataclass
class SurgeController(BaseController):
    """Rule-based surge with guardrails.

    Lifts the fee above ``base_fee`` when observed load is high and trims it when
    load is slack, then enforces production guardrails:
      * absolute fee floor / cap,
      * a surge cap (multiplier never exceeds ``surge_cap``),
      * a per-step rate limit so the fee cannot jump more than ``max_step`` (in
        relative terms) between consecutive periods -- this is what prevents
        oscillation and "price-war" whipsaw.
    """

    base_fee: float
    fee_bounds: tuple[float, float] = (0.002, 0.04)
    surge_cap: float = 2.5
    discount_floor: float = 0.85
    surge_strength: float = 1.6
    load_threshold: float = 0.5
    max_step: float = 0.15
    name: str = "surge_rule"
    _last_fee: float = field(default=None, init=False)

    def act(self, context: int, m_hint: float) -> float:
        load = context / max(self._n_contexts - 1, 1) if hasattr(self, "_n_contexts") else m_hint
        # Map load (0..1) to a surge multiplier around 1.0.
        mult = 1.0 + self.surge_strength * (load - self.load_threshold)
        mult = float(np.clip(mult, self.discount_floor, self.surge_cap))
        target = self.base_fee * mult
        lo, hi = self.fee_bounds
        target = float(np.clip(target, lo, hi))
        # Rate-limit relative to last fee.
        if self._last_fee is not None:
            max_up = self._last_fee * (1 + self.max_step)
            max_dn = self._last_fee * (1 - self.max_step)
            target = float(np.clip(target, max_dn, max_up))
        self._last_fee = target
        return target

    def bind_contexts(self, n_contexts: int) -> "SurgeController":
        self._n_contexts = n_contexts
        return self


@dataclass
class ThompsonBanditController(BaseController):
    """Contextual Gaussian Thompson sampling over a discrete fee grid.

    Maintains a Normal posterior on mean reward for every (load-context, fee-arm)
    pair, samples from each posterior, and plays the arm with the highest sample.
    Naturally balances exploration and exploitation and converges to the best fee
    per load state. (Walmart Labs and ride-hailing platforms use this family of
    methods for live pricing.)
    """

    fee_grid: np.ndarray
    n_contexts: int
    prior_mean: float = 0.0
    prior_var: float = 1e6           # diffuse prior
    obs_var: float = 1.0             # reward observation noise (scaled rewards)
    name: str = "thompson_bandit"

    def __post_init__(self):
        k = len(self.fee_grid)
        self._mu = np.full((self.n_contexts, k), self.prior_mean)
        self._var = np.full((self.n_contexts, k), self.prior_var)
        self._rng = np.random.default_rng(0)

    def act(self, context: int, m_hint: float) -> float:
        samples = self._rng.normal(self._mu[context], np.sqrt(self._var[context]))
        self._last_arm = int(samples.argmax())
        return float(self.fee_grid[self._last_arm])

    def update(self, context: int, fee: float, reward: float) -> None:
        arm = int(np.argmin(np.abs(self.fee_grid - fee)))
        # Bayesian update of a Normal mean with known observation variance.
        prior_var = self._var[context, arm]
        prior_mu = self._mu[context, arm]
        post_var = 1.0 / (1.0 / prior_var + 1.0 / self.obs_var)
        post_mu = post_var * (prior_mu / prior_var + reward / self.obs_var)
        self._mu[context, arm] = post_mu
        self._var[context, arm] = post_var


@dataclass
class EpsilonGreedyController(BaseController):
    """Contextual epsilon-greedy over the fee grid (simple online baseline)."""

    fee_grid: np.ndarray
    n_contexts: int
    epsilon: float = 0.1
    name: str = "epsilon_greedy"

    def __post_init__(self):
        k = len(self.fee_grid)
        self._sum = np.zeros((self.n_contexts, k))
        self._count = np.zeros((self.n_contexts, k))
        self._rng = np.random.default_rng(0)

    def act(self, context: int, m_hint: float) -> float:
        k = len(self.fee_grid)
        if self._rng.random() < self.epsilon or self._count[context].sum() == 0:
            self._last_arm = int(self._rng.integers(k))
        else:
            means = np.divide(
                self._sum[context], self._count[context],
                out=np.full(k, -np.inf), where=self._count[context] > 0,
            )
            self._last_arm = int(means.argmax())
        return float(self.fee_grid[self._last_arm])

    def update(self, context: int, fee: float, reward: float) -> None:
        arm = int(np.argmin(np.abs(self.fee_grid - fee)))
        self._sum[context, arm] += reward
        self._count[context, arm] += 1


# ===========================================================================
#  4. SIMULATION HARNESS
# ===========================================================================
def _demand_state_path(T: int, n_contexts: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """Generate a time-of-day-style demand-state path and its load context bucket."""
    rng = np.random.default_rng(seed)
    hour = np.arange(T) % 24
    tod = 0.6 + 1.4 * np.exp(-0.5 * ((hour - 19) / 3.0) ** 2) \
        + 0.8 * np.exp(-0.5 * ((hour - 10) / 2.5) ** 2)
    noise = rng.lognormal(0.0, 0.15, size=T)
    m = tod * noise                                   # demand state (>0)
    # Bucket the *load* (rank of m) into contexts 0..n_contexts-1.
    ranks = pd.Series(m).rank(pct=True).to_numpy()
    context = np.clip((ranks * n_contexts).astype(int), 0, n_contexts - 1)
    return m, context


def run_simulation(
    env: TxnPricingEnv,
    controllers: dict[str, BaseController],
    fee_grid: np.ndarray,
    T: int = 4000,
    n_contexts: int = 5,
    reward_scale: float | None = None,
    seed: int = 7,
) -> dict:
    """Run all controllers against the same demand path and score them.

    Returns per-controller cumulative profit and cumulative regret vs a
    load-aware oracle, plus the realised fee path.
    """
    m_path, ctx_path = _demand_state_path(T, n_contexts, seed)
    rng = np.random.default_rng(seed + 1)

    # Oracle (knows true params) for regret accounting.
    oracle_profit = np.array(
        [env.best_fee(m_path[t], fee_grid)["profit"] for t in range(T)]
    )
    if reward_scale is None:
        reward_scale = float(np.median(np.abs(oracle_profit)) + 1e-9)

    results: dict[str, dict] = {}
    for cname, ctrl in controllers.items():
        if hasattr(ctrl, "bind_contexts"):
            ctrl.bind_contexts(n_contexts)
        profits = np.zeros(T)
        fees = np.zeros(T)
        for t in range(T):
            ctx = int(ctx_path[t])
            m = float(m_path[t])
            m_hint = ctx / max(n_contexts - 1, 1)          # observed load proxy
            fee = ctrl.act(ctx, m_hint)
            out = env.realized_profit(fee, m, rng)
            profits[t] = out["profit"]
            fees[t] = fee
            ctrl.update(ctx, fee, out["profit"] / reward_scale)
        results[cname] = {
            "cum_profit": np.cumsum(profits),
            "fees": fees,
            "total_profit": float(profits.sum()),
            "regret": np.cumsum(oracle_profit - profits),
        }

    results["_oracle"] = {
        "cum_profit": np.cumsum(oracle_profit),
        "total_profit": float(oracle_profit.sum()),
    }
    results["_meta"] = {"m_path": m_path, "ctx_path": ctx_path, "T": T}
    return results


if __name__ == "__main__":
    # Quick self-test on the consumer segment, calibrated so the current 1.2%
    # fee is myopically optimal at average load.
    env = TxnPricingEnv.calibrated(
        elasticity=-1.9, fee_ref=0.012, q_ref=15000, avg_ticket=150.0,
    )
    fee_grid = np.round(np.arange(0.006, 0.0301, 0.002), 4)   # 0.012 is on the grid

    lo = lerner_optimal_fee(env.elasticity, env.base_cost, env.avg_ticket)
    print(f"Calibrated contribution cost: ${env.base_cost:.3f}/txn")
    print("Lerner optimal fee (m=1):", round(lo["optimal_fee"], 4),
          "| markup:", round(lo["markup"], 3))

    controllers = {
        "static_base": StaticController(0.012),
        "surge_rule": SurgeController(base_fee=0.012),
        "epsilon_greedy": EpsilonGreedyController(fee_grid, n_contexts=5),
        "thompson_bandit": ThompsonBanditController(fee_grid, n_contexts=5),
    }
    res = run_simulation(env, controllers, fee_grid, T=4000)
    print(f"\n{'controller':18s} {'total_profit':>14s} {'% of oracle':>12s}")
    oracle = res["_oracle"]["total_profit"]
    for k in ["static_base", "surge_rule", "epsilon_greedy", "thompson_bandit"]:
        tp = res[k]["total_profit"]
        print(f"{k:18s} {tp:14,.0f} {100*tp/oracle:11.1f}%")
    print(f"{'_oracle':18s} {oracle:14,.0f} {100.0:11.1f}%")
