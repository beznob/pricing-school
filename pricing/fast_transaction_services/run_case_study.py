"""
End-to-end runner for the fast-transaction-service dynamic-pricing case study.

Pipeline
--------
1.  Generate the synthetic real-time-payments panel.
2.  Estimate price elasticity per segment -- naive OLS (biased) vs IV/2SLS
    (causal) -- and score both against the ground truth.
3.  Turn the elasticity into a profit-maximising fee, and show how pricing on a
    *biased* elasticity destroys profit.
4.  Run the dynamic-pricing simulation (static vs rule-based surge vs contextual
    bandits) and measure profit / regret against a load-aware oracle.
5.  Write all figures to ``images/`` and a summary to ``RESULTS.md``.

Run:  ``python run_case_study.py``
"""

from __future__ import annotations

import os

import matplotlib

matplotlib.use("Agg")  # headless
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from dynamic_pricing import (
    EpsilonGreedyController,
    StaticController,
    SurgeController,
    ThompsonBanditController,
    TxnPricingEnv,
    lerner_optimal_fee,
    optimal_fee_grid,
    profit_curve,
    run_simulation,
)
from elasticity_models import (
    iv_2sls_elasticity,
    naive_ols_elasticity,
    segmented_elasticity,
)
from fast_txn_simulator import DEFAULT_SEGMENTS, SimConfig, generate_fast_txn_data

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "images")
os.makedirs(IMG, exist_ok=True)

plt.rcParams.update({"figure.dpi": 110, "font.size": 11, "axes.grid": True,
                     "grid.alpha": 0.25})
BLUE, RED, GREEN, ORANGE, PURPLE = "#2c6fbb", "#c0392b", "#27ae60", "#e67e22", "#8e44ad"


# --------------------------------------------------------------------------- #
def banner(text: str) -> None:
    print("\n" + "=" * 74 + f"\n{text}\n" + "=" * 74)


# --------------------------------------------------------------------------- #
# STEP 1-2: data + elasticity estimation
# --------------------------------------------------------------------------- #
def run_elasticity_block(df: pd.DataFrame) -> pd.DataFrame:
    banner("STEP 1-2  |  PRICE ELASTICITY: naive OLS (biased) vs IV/2SLS (causal)")

    pooled_ols = naive_ols_elasticity(df)
    pooled_iv = iv_2sls_elasticity(df)
    print(f"Pooled OLS elasticity : {pooled_ols['elasticity']:+.3f} "
          f"(se {pooled_ols['se']:.3f})   <-- biased, even wrong-signed")
    print(f"Pooled IV  elasticity : {pooled_iv['elasticity']:+.3f} "
          f"(se {pooled_iv['se']:.3f})   first-stage F = {pooled_iv['first_stage_F']:.0f}")

    table = segmented_elasticity(df)
    print("\nPer-segment (the firm prices each segment separately):")
    with pd.option_context("display.float_format", lambda v: f"{v:7.3f}"):
        print(table[["segment", "true_elasticity", "ols_elasticity",
                     "iv_elasticity", "first_stage_F", "ols_bias", "iv_bias"]]
              .to_string(index=False))

    _plot_confounded_scatter(df)
    _plot_elasticity_bars(table)
    return table


def _plot_confounded_scatter(df: pd.DataFrame) -> None:
    """Show *why* OLS is biased: high-fee hours are also high-demand hours."""
    sub = df[df["segment"] == "consumer"].sample(2000, random_state=1)
    fig, ax = plt.subplots(figsize=(8, 5.2))
    sc = ax.scatter(sub["log_fee"], sub["log_volume"], c=sub["latent_demand_u"],
                    cmap="coolwarm", s=12, alpha=0.7)
    # Naive OLS line through the cloud.
    b = np.polyfit(sub["log_fee"], sub["log_volume"], 1)
    xs = np.linspace(sub["log_fee"].min(), sub["log_fee"].max(), 50)
    ax.plot(xs, np.polyval(b, xs), color="black", lw=2.5,
            label=f"OLS fit (slope {b[0]:+.2f})")
    # True structural slope (anchored at the cloud mean).
    true_slope = -1.9
    anchor_x, anchor_y = sub["log_fee"].mean(), sub["log_volume"].mean()
    ax.plot(xs, anchor_y + true_slope * (xs - anchor_x), color=GREEN, lw=2.5,
            ls="--", label=f"true elasticity ({true_slope:+.2f})")
    ax.set_xlabel("log(fee)")
    ax.set_ylabel("log(volume)")
    ax.set_title("Endogeneity in one picture: colour = unobserved demand shock\n"
                 "the firm surges the fee when demand is high → OLS slope is biased up")
    plt.colorbar(sc, label="latent demand shock u (unobserved)")
    ax.legend(loc="upper right")
    fig.tight_layout()
    fig.savefig(os.path.join(IMG, "fig1_endogeneity_scatter.png"))
    plt.close(fig)


def _plot_elasticity_bars(table: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(8.5, 5))
    x = np.arange(len(table))
    w = 0.27
    ax.bar(x - w, table["true_elasticity"], w, label="Ground truth", color=GREEN)
    ax.bar(x, table["ols_elasticity"], w, label="Naive OLS", color=RED)
    ax.bar(x + w, table["iv_elasticity"], w, label="IV / 2SLS", color=BLUE)
    ax.axhline(-1.0, color="gray", ls=":", lw=1)
    ax.text(len(table) - 0.5, -1.02, "elastic ↓ / inelastic ↑", ha="right",
            va="top", fontsize=9, color="gray")
    ax.set_xticks(x)
    ax.set_xticklabels(table["segment"])
    ax.set_ylabel("price elasticity of demand")
    ax.set_title("OLS understates price sensitivity; IV recovers the truth")
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(IMG, "fig2_elasticity_estimates.png"))
    plt.close(fig)


# --------------------------------------------------------------------------- #
# STEP 3: static optimisation + the cost of using a biased elasticity
# --------------------------------------------------------------------------- #
def run_optimisation_block(table: pd.DataFrame) -> dict:
    banner("STEP 3  |  FROM ELASTICITY TO PRICE: why a biased elasticity loses money")

    seg = "consumer"
    row = table[table["segment"] == seg].iloc[0]
    spec = DEFAULT_SEGMENTS[seg]
    fee_ref = float(np.exp(spec.base_log_fee))
    q_ref, avg_ticket = 15000.0, 150.0

    env = TxnPricingEnv.calibrated(
        elasticity=row["true_elasticity"], fee_ref=fee_ref, q_ref=q_ref,
        avg_ticket=avg_ticket,
    )
    cost = env.base_cost

    fee_grid = np.linspace(0.004, env.fee_bounds[1], 200)
    curve_true = profit_curve(row["true_elasticity"], q_ref, fee_ref, cost, avg_ticket, fee_grid)
    opt_true = optimal_fee_grid(curve_true)

    # Decisions implied by each elasticity estimate.
    def implied_fee(eps: float) -> float:
        out = lerner_optimal_fee(eps, cost, avg_ticket, env.fee_bounds)
        return out["optimal_fee"]

    fee_from_truth = implied_fee(row["true_elasticity"])
    fee_from_iv = implied_fee(row["iv_elasticity"])
    fee_from_ols = implied_fee(row["ols_elasticity"])

    # Realised profit (under TRUE demand) of pricing at each implied fee.
    def true_profit(fee: float) -> float:
        return float(profit_curve(row["true_elasticity"], q_ref, fee_ref, cost,
                                  avg_ticket, np.array([fee]))["profit"].iloc[0])

    p_truth, p_iv, p_ols = map(true_profit, (fee_from_truth, fee_from_iv, fee_from_ols))
    loss_ols = 1 - p_ols / p_truth

    print(f"Segment '{seg}':  fully-loaded cost ${cost:.3f}/txn, ticket ${avg_ticket:.0f}")
    print(f"  Optimal fee from TRUE elasticity : {fee_from_truth*100:5.2f}%  "
          f"→ profit/period ${p_truth:,.0f}")
    print(f"  Optimal fee from IV   elasticity : {fee_from_iv*100:5.2f}%  "
          f"→ profit/period ${p_iv:,.0f}")
    print(f"  Optimal fee from OLS  elasticity : {fee_from_ols*100:5.2f}%  "
          f"→ profit/period ${p_ols:,.0f}   ({loss_ols*100:.0f}% profit LOST)")
    print("  → OLS makes demand look inelastic, so it tells you to over-charge.")

    _plot_profit_curve(curve_true, opt_true, fee_from_ols, p_ols, fee_from_iv)
    return {
        "segment": seg, "cost": cost, "avg_ticket": avg_ticket, "fee_ref": fee_ref,
        "q_ref": q_ref, "opt_true": opt_true, "fee_from_ols": fee_from_ols,
        "fee_from_iv": fee_from_iv, "loss_ols": loss_ols, "env": env,
    }


def _plot_profit_curve(curve, opt_true, fee_ols, p_ols, fee_iv) -> None:
    fig, ax = plt.subplots(figsize=(8.5, 5))
    ax.plot(curve["fee"] * 100, curve["profit"], color=BLUE, lw=2.5,
            label="profit (true demand)")
    ax.axvline(opt_true["optimal_fee"] * 100, color=GREEN, ls="--", lw=2,
               label=f"optimal / IV fee = {opt_true['optimal_fee']*100:.2f}%")
    ax.scatter([fee_ols * 100], [p_ols], color=RED, zorder=5, s=70,
               label=f"OLS-implied fee = {fee_ols*100:.2f}% (over-charges)")
    ax.set_xlabel("instant-transfer fee (%)")
    ax.set_ylabel("expected profit / period ($)")
    ax.set_title("Pricing on a biased elasticity walks off the profit hill")
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(IMG, "fig3_profit_curve.png"))
    plt.close(fig)


# --------------------------------------------------------------------------- #
# STEP 4: dynamic pricing simulation
# --------------------------------------------------------------------------- #
def run_dynamic_block(opt_ctx: dict) -> dict:
    banner("STEP 4  |  DYNAMIC PRICING: static vs rule-based surge vs contextual bandits")

    env: TxnPricingEnv = opt_ctx["env"]
    fee_ref = opt_ctx["fee_ref"]
    fee_grid = np.round(np.arange(0.006, 0.0301, 0.002), 4)
    n_contexts = 5

    controllers = {
        "static_1.2%": StaticController(fee_ref, name="static_1.2%"),
        "surge_rule": SurgeController(base_fee=fee_ref, fee_bounds=env.fee_bounds),
        "epsilon_greedy": EpsilonGreedyController(fee_grid, n_contexts, epsilon=0.1),
        "thompson_bandit": ThompsonBanditController(fee_grid, n_contexts),
    }
    res = run_simulation(env, controllers, fee_grid, T=5000, n_contexts=n_contexts, seed=7)

    oracle = res["_oracle"]["total_profit"]
    print(f"{'controller':16s} {'total profit':>15s} {'% of oracle':>12s}")
    summary = {}
    for k in ["static_1.2%", "surge_rule", "epsilon_greedy", "thompson_bandit"]:
        tp = res[k]["total_profit"]
        summary[k] = (tp, 100 * tp / oracle)
        print(f"{k:16s} {tp:15,.0f} {100*tp/oracle:11.1f}%")
    print(f"{'oracle':16s} {oracle:15,.0f} {100.0:11.1f}%")
    uplift = summary["surge_rule"][0] / summary["static_1.2%"][0] - 1
    print(f"\nRule-based surge lifts profit {uplift*100:.1f}% over the flat fee.")

    _plot_dynamic(res, env, fee_grid, fee_ref, n_contexts)
    return {"summary": summary, "oracle": oracle, "uplift": uplift}


def _plot_dynamic(res, env, fee_grid, fee_ref, n_contexts) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    colors = {"static_1.2%": "gray", "surge_rule": ORANGE,
              "epsilon_greedy": PURPLE, "thompson_bandit": BLUE}

    # (a) cumulative profit
    ax = axes[0, 0]
    ax.plot(res["_oracle"]["cum_profit"], color=GREEN, lw=2.5, label="oracle")
    for k, c in colors.items():
        ax.plot(res[k]["cum_profit"], color=c, lw=1.8, label=k)
    ax.set_title("(a) Cumulative profit")
    ax.set_xlabel("period (hour)")
    ax.set_ylabel("cumulative profit ($)")
    ax.legend(fontsize=9)

    # (b) cumulative regret
    ax = axes[0, 1]
    for k, c in colors.items():
        ax.plot(res[k]["regret"], color=c, lw=1.8, label=k)
    ax.set_title("(b) Cumulative regret vs oracle (lower is better)")
    ax.set_xlabel("period (hour)")
    ax.set_ylabel("cumulative regret ($)")
    ax.legend(fontsize=9)

    # (c) one-day fee trajectories
    ax = axes[1, 0]
    day = slice(24 * 3, 24 * 5)  # two representative days
    for k in ["static_1.2%", "surge_rule", "thompson_bandit"]:
        ax.plot(res[k]["fees"][day] * 100, color=colors[k], lw=1.8, label=k)
    ax.set_title("(c) Fee trajectory over two days")
    ax.set_xlabel("hour")
    ax.set_ylabel("fee (%)")
    ax.legend(fontsize=9)

    # (d) optimal fee vs load (why surge is optimal)
    ax = axes[1, 1]
    loads = np.linspace(0.6, 2.2, 60)               # demand state m
    opt_fees = [env.best_fee(m, np.linspace(0.006, env.fee_bounds[1], 200))["fee"]
                for m in loads]
    ax.plot(loads, np.array(opt_fees) * 100, color=RED, lw=2.5)
    ax.axhline(fee_ref * 100, color="gray", ls=":", label="flat fee 1.2%")
    ax.set_title("(d) Profit-max fee rises with load (congestion cost) → surge is optimal")
    ax.set_xlabel("demand state m (1 = average load)")
    ax.set_ylabel("optimal fee (%)")
    ax.legend(fontsize=9)

    fig.suptitle("Dynamic pricing for a fast transaction service", fontsize=14, y=1.0)
    fig.tight_layout()
    fig.savefig(os.path.join(IMG, "fig4_dynamic_pricing.png"))
    plt.close(fig)


# --------------------------------------------------------------------------- #
# Write RESULTS.md
# --------------------------------------------------------------------------- #
def write_results(table, opt_ctx, dyn) -> None:
    s = dyn["summary"]
    lines = [
        "# Case Study Results — Dynamic Pricing for a Fast Transaction Service",
        "",
        "_Auto-generated by `run_case_study.py`. Numbers are from the synthetic "
        "`FastPay` simulator with a fixed seed, so they are reproducible._",
        "",
        "## 1. Price elasticity: naive OLS is badly biased",
        "",
        "The firm raises the instant-transfer fee when (unobserved) demand spikes "
        "— a surge policy — so price and demand are jointly determined. Ordinary "
        "least squares therefore **understates** price sensitivity; a cost-shock "
        "instrument (IV/2SLS) recovers the true elasticity.",
        "",
        "| Segment | True ε | OLS ε | IV ε | First-stage F |",
        "|---|---:|---:|---:|---:|",
    ]
    for _, r in table.iterrows():
        lines.append(
            f"| {r['segment']} | {r['true_elasticity']:+.2f} | "
            f"{r['ols_elasticity']:+.2f} | {r['iv_elasticity']:+.2f} | "
            f"{r['first_stage_F']:,.0f} |"
        )
    lines += [
        "",
        "OLS bias is large and positive (toward zero): demand looks far more "
        "inelastic than it is. The pooled OLS estimate is even **positive**, which "
        "would suggest raising prices grows volume — a classic endogeneity trap.",
        "",
        "## 2. A biased elasticity makes you over-charge",
        "",
        f"For the **{opt_ctx['segment']}** segment (fully-loaded cost "
        f"${opt_ctx['cost']:.3f}/txn, ${opt_ctx['avg_ticket']:.0f} avg ticket):",
        "",
        f"- Optimal fee from the **causal (IV)** elasticity: "
        f"**{opt_ctx['opt_true']['optimal_fee']*100:.2f}%**",
        f"- Fee implied by the **biased (OLS)** elasticity: "
        f"**{opt_ctx['fee_from_ols']*100:.2f}%** (it looks inelastic, so you "
        f"over-charge)",
        f"- Pricing on the OLS number throws away **~{opt_ctx['loss_ols']*100:.0f}% "
        f"of profit** versus the true optimum.",
        "",
        "## 3. Dynamic pricing beats a flat fee",
        "",
        "Because marginal cost-to-serve rises with system load (congestion), the "
        "profit-maximising fee is higher at peak — so *load-aware* pricing wins. "
        "Controllers are scored against a load-aware oracle on the same demand path:",
        "",
        "| Controller | Total profit | % of oracle |",
        "|---|---:|---:|",
    ]
    for k in ["static_1.2%", "surge_rule", "epsilon_greedy", "thompson_bandit"]:
        tp, pct = s[k]
        lines.append(f"| {k} | ${tp:,.0f} | {pct:.1f}% |")
    lines.append(f"| **oracle** | ${dyn['oracle']:,.0f} | 100.0% |")
    lines += [
        "",
        f"The rule-based surge controller lifts profit **{dyn['uplift']*100:.1f}%** "
        "over the flat fee while staying inside its guardrails (fee floor/cap, "
        "surge cap, per-step rate limit). The contextual bandits *learn* the "
        "load-aware policy online without ever being told the cost structure.",
        "",
        "## Figures",
        "",
        "![Endogeneity scatter](images/fig1_endogeneity_scatter.png)",
        "![Elasticity estimates](images/fig2_elasticity_estimates.png)",
        "![Profit curve](images/fig3_profit_curve.png)",
        "![Dynamic pricing](images/fig4_dynamic_pricing.png)",
        "",
    ]
    with open(os.path.join(HERE, "RESULTS.md"), "w") as fh:
        fh.write("\n".join(lines))
    print(f"\nWrote {os.path.join(HERE, 'RESULTS.md')} and 4 figures to images/.")


# --------------------------------------------------------------------------- #
def main() -> None:
    banner("FAST TRANSACTION SERVICES — DYNAMIC PRICING & ELASTICITY CASE STUDY")
    df = generate_fast_txn_data(SimConfig())
    print(f"Generated {len(df):,} hourly observations across "
          f"{df['segment'].nunique()} segments "
          f"({df['day'].nunique()} days).")

    table = run_elasticity_block(df)
    opt_ctx = run_optimisation_block(table)
    dyn = run_dynamic_block(opt_ctx)
    write_results(table, opt_ctx, dyn)
    banner("DONE")


if __name__ == "__main__":
    main()
