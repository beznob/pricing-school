"""
Synthetic data generator for a *fast transaction service* (real-time payments).

Business framing
----------------
"FastPay" is a real-time money-movement platform. Customers can settle a payment
on the slow/free rail (e.g. next-day ACH) or pay a **fee** to move money
*instantly*. The lever we control is the instant-transfer ``fee_rate`` (the
"price"); the outcome we care about is paid instant **volume** (the "demand")
and the resulting **profit**.

Why this dataset is interesting for causal pricing
--------------------------------------------------
We bake in three things that make naive elasticity estimation wrong, and that a
good pricing analyst has to handle:

1.  **A known ground-truth elasticity** (per segment) so we can score estimators.
2.  **Endogeneity via surge-style fee setting.** The firm raises the fee when
    latent demand ``u`` is high (a "surge" policy). ``u`` is *unobserved* and
    also lifts demand directly, so price and demand are determined jointly.
    => Ordinary least squares of log(volume) on log(fee) is biased *upward*
       (it looks like customers barely respond, or even respond positively).
3.  **A cost-side instrument.** Per-transaction processing/interchange cost
    ``z`` shifts the fee the firm charges (cost pass-through) but does not touch
    customer demand except through the fee. That makes ``z`` a valid instrument
    to recover the true elasticity.

The structural equations (per observation t, per segment s)
-----------------------------------------------------------
    cost_t      = c0_s + z_t                                 # marginal cost to serve
    log(fee_t)  = g0_s + g_u * u_t + g_z * z_t + e_fee       # firm's (confounded) policy
    log(Q_t)    = b0_s + eps_s*log(fee_t) + d_s*u_t
                       + season_t + e_dem                    # true demand curve

``eps_s`` (< 0) is the structural own-price elasticity we want to recover.
Because cov(log fee, u) > 0 and u also raises Q, OLS is biased toward zero.
``z`` is independent of ``u`` so 2SLS using ``z`` is consistent.

The module is intentionally dependency-light (numpy + pandas only) so it runs
anywhere without the rest of the repo.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict

import numpy as np
import pandas as pd


# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #
@dataclass
class SegmentSpec:
    """Per-segment structural parameters."""

    name: str
    elasticity: float          # eps_s  (structural own-price elasticity, < 0)
    base_log_demand: float     # b0_s   (scale of the segment)
    base_cost: float           # c0_s   ($ marginal cost to serve one instant txn)
    surge_sensitivity: float   # g_u    (how aggressively the firm surges on demand)
    cost_passthrough: float    # g_z    (how much processing cost is passed into fee)
    demand_shock_loading: float  # d_s  (how much latent demand u lifts volume)
    base_log_fee: float        # g0_s   (typical log fee level)


DEFAULT_SEGMENTS: Dict[str, SegmentSpec] = {
    # Consumers are the most price sensitive (they will happily wait for the free rail).
    "consumer": SegmentSpec(
        name="consumer",
        elasticity=-1.9,
        base_log_demand=9.9,   # ~20k instant txns/hour at the reference fee
        base_cost=0.18,
        surge_sensitivity=0.65,
        cost_passthrough=0.55,
        demand_shock_loading=0.9,
        base_log_fee=np.log(0.012),   # ~1.2% fee
    ),
    # SMBs need money to move but shop around -> moderately elastic.
    "smb": SegmentSpec(
        name="smb",
        elasticity=-1.35,
        base_log_demand=8.0,   # ~3k instant txns/hour at the reference fee
        base_cost=0.22,
        surge_sensitivity=0.55,
        cost_passthrough=0.6,
        demand_shock_loading=0.8,
        base_log_fee=np.log(0.010),   # ~1.0% fee
    ),
    # Enterprise/marketplace payouts are time-critical -> least elastic (pricing power).
    "enterprise": SegmentSpec(
        name="enterprise",
        elasticity=-0.85,
        base_log_demand=6.0,   # ~400 instant payouts/hour at the reference fee
        base_cost=0.30,
        surge_sensitivity=0.45,
        cost_passthrough=0.7,
        demand_shock_loading=0.7,
        base_log_fee=np.log(0.008),   # ~0.8% fee
    ),
}


@dataclass
class SimConfig:
    """Top-level simulation configuration."""

    n_days: int = 120                 # ~4 months of history
    obs_per_day: int = 24             # hourly observations
    seed: int = 42
    sigma_u: float = 0.45             # std of latent demand shock (the confounder)
    sigma_z: float = 0.55             # std of cost/instrument shock
    sigma_fee: float = 0.08           # idiosyncratic noise in the fee policy
    sigma_demand: float = 0.10        # idiosyncratic demand noise
    u_persistence: float = 0.5        # AR(1) persistence of the demand shock
    segments: Dict[str, SegmentSpec] = field(
        default_factory=lambda: {k: v for k, v in DEFAULT_SEGMENTS.items()}
    )


# --------------------------------------------------------------------------- #
# Time-of-day / seasonality helpers
# --------------------------------------------------------------------------- #
def _time_of_day_factor(hour: np.ndarray) -> np.ndarray:
    """Two demand peaks (morning payroll/commerce + evening), like a real network."""
    morning = np.exp(-0.5 * ((hour - 10) / 2.5) ** 2)
    evening = np.exp(-0.5 * ((hour - 19) / 2.8) ** 2)
    return 0.25 + 0.9 * morning + 1.0 * evening


def _day_of_week_factor(dow: np.ndarray) -> np.ndarray:
    """Weekdays busier than weekends for B2B-heavy payment flows."""
    weekday = np.where(dow < 5, 1.0, 0.6)
    return weekday


# --------------------------------------------------------------------------- #
# Core generator
# --------------------------------------------------------------------------- #
def generate_fast_txn_data(config: SimConfig | None = None) -> pd.DataFrame:
    """Generate the panel of (segment x hour) observations.

    Returns a tidy DataFrame with the columns a pricing team would actually have,
    plus the *latent* ground-truth columns (prefixed ``true_``/``latent_``) that
    a real team would NOT observe -- we keep them so we can score estimators.
    """
    config = config or SimConfig()
    rng = np.random.default_rng(config.seed)

    n_periods = config.n_days * config.obs_per_day
    period = np.arange(n_periods)
    hour = period % config.obs_per_day
    day = period // config.obs_per_day
    dow = day % 7

    # Latent demand shock u_t: AR(1) so "surges" cluster in time, plus a
    # deterministic time-of-day / day-of-week component that we *do* observe.
    eps_u = rng.normal(0.0, config.sigma_u, size=n_periods)
    u = np.zeros(n_periods)
    for t in range(1, n_periods):
        u[t] = config.u_persistence * u[t - 1] + eps_u[t]

    tod = _time_of_day_factor(hour)
    dowf = _day_of_week_factor(dow)
    # Observed seasonal index in log space (firms have this from forecasting).
    season = np.log(tod) + np.log(dowf)

    # System load proxy (0-1): how close the platform is to its capacity this hour.
    # Driven by observed season + latent surge -> used later by the surge controller.
    raw_load = 0.55 * (season - season.mean()) / (season.std() + 1e-9) + 0.8 * u
    load = 1.0 / (1.0 + np.exp(-raw_load))  # squash to (0, 1)

    frames = []
    for spec in config.segments.values():
        # Cost / instrument shock z_t (independent of u): processing & interchange.
        z = rng.normal(0.0, config.sigma_z, size=n_periods)
        cost = np.clip(spec.base_cost * np.exp(0.25 * z), 0.02, None)  # $ per txn

        # ---- Firm's (confounded) fee policy -------------------------------- #
        # Raises fee when latent demand u is high (surge) AND passes cost through.
        log_fee = (
            spec.base_log_fee
            + spec.surge_sensitivity * u
            + spec.cost_passthrough * z
            + 0.15 * (season - season.mean())
            + rng.normal(0.0, config.sigma_fee, size=n_periods)
        )
        fee_rate = np.clip(np.exp(log_fee), 0.001, 0.05)  # 0.1%..5% guardrail
        log_fee = np.log(fee_rate)

        # ---- True structural demand --------------------------------------- #
        # Price term is centered at the segment's reference fee so that
        # ``base_log_demand`` is the interpretable log-volume at that fee. The
        # slope w.r.t. log_fee is still exactly ``elasticity`` (centering only
        # shifts the intercept), so estimators are unaffected.
        log_q = (
            spec.base_log_demand
            + spec.elasticity * (log_fee - spec.base_log_fee)
            + spec.demand_shock_loading * u
            + season
            + rng.normal(0.0, config.sigma_demand, size=n_periods)
        )
        volume = np.exp(log_q)  # number of paid instant transactions this hour

        # Average ticket size (just for revenue framing; fee is a % of this).
        avg_ticket = np.clip(rng.lognormal(mean=5.0, sigma=0.4, size=n_periods), 20, 5000)

        revenue = fee_rate * avg_ticket * volume
        variable_cost = cost * volume
        profit = revenue - variable_cost

        frames.append(
            pd.DataFrame(
                {
                    "period": period,
                    "day": day,
                    "hour": hour,
                    "dow": dow,
                    "segment": spec.name,
                    # Observed by the team:
                    "fee_rate": fee_rate,
                    "log_fee": log_fee,
                    "volume": volume,
                    "log_volume": log_q,
                    "avg_ticket": avg_ticket,
                    "unit_cost": cost,
                    "cost_shock_z": z,          # instrument (observed: cost data)
                    "season": season,
                    "load": load,
                    "revenue": revenue,
                    "variable_cost": variable_cost,
                    "profit": profit,
                    # Latent / ground-truth (NOT observable in reality):
                    "latent_demand_u": u,
                    "true_elasticity": spec.elasticity,
                }
            )
        )

    df = pd.concat(frames, ignore_index=True)
    return df


def segment_truth(config: SimConfig | None = None) -> pd.DataFrame:
    """Return the ground-truth elasticity / cost table for scoring."""
    config = config or SimConfig()
    rows = [
        {
            "segment": s.name,
            "true_elasticity": s.elasticity,
            "base_cost": s.base_cost,
            "base_fee": float(np.exp(s.base_log_fee)),
        }
        for s in config.segments.values()
    ]
    return pd.DataFrame(rows)


if __name__ == "__main__":
    cfg = SimConfig()
    data = generate_fast_txn_data(cfg)
    print(f"Generated {len(data):,} rows across {data['segment'].nunique()} segments.")
    print(data.groupby("segment")[["fee_rate", "volume", "profit", "load"]].mean())
    print("\nGround truth:")
    print(segment_truth(cfg).to_string(index=False))
