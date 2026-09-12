"""
End-to-end runner for the **travel-money / prepaid-card** case study, aligned to
the *Senior Manager, Pricing, Distribution & Revenue* role.

Pipeline
--------
1.  Simulate the multi-channel travel-money panel + a prepaid-card portfolio.
2.  Estimate **channel FX-margin elasticity** causally (OLS vs IV) -> reuse the
    existing elasticity engine.
3.  **Distribution economics**: channel P&L, competitive positioning, margin
    support.
4.  **FCA Consumer Duty fair value**: scorecard, vulnerable-customer harm, and a
    written assessment.
5.  **AOP**: revenue build-up, scenario analysis, competitor sensitivity.
6.  Write figures to ``images/`` (``role_*.png``) and ``RESULTS.md``.

Run:  ``python run_role_case_study.py``
"""

from __future__ import annotations

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from aop_scenario import (competitive_index, competitor_sensitivity,
                          project_scenario, revenue_bridge, revenue_lines,
                          run_scenarios)
from distribution_economics import (channel_pnl, channel_positioning,
                                    margin_support_breakeven)
from elasticity_models import segmented_elasticity
from fair_value import (fair_value_metrics, fair_value_scorecard,
                        generate_fair_value_assessment, vulnerable_harm)
from travel_money_simulator import (DEFAULT_CHANNELS, TravelMoneyConfig,
                                    generate_card_portfolio, generate_channel_panel)

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "images")
os.makedirs(IMG, exist_ok=True)
plt.rcParams.update({"figure.dpi": 110, "font.size": 10, "axes.grid": True,
                     "grid.alpha": 0.25})
BLUE, RED, GREEN, ORANGE, PURPLE, GREY = \
    "#2c6fbb", "#c0392b", "#27ae60", "#e67e22", "#8e44ad", "#7f8c8d"


def banner(t): print("\n" + "=" * 76 + f"\n{t}\n" + "=" * 76)


# --------------------------------------------------------------------------- #
def elasticity_block(panel):
    banner("1 | CHANNEL FX-MARGIN ELASTICITY  (naive OLS vs causal IV/2SLS)")
    tbl = segmented_elasticity(panel)
    with pd.option_context("display.float_format", lambda v: f"{v:7.3f}"):
        print(tbl[["segment", "true_elasticity", "ols_elasticity",
                   "iv_elasticity", "first_stage_F"]].to_string(index=False))
    iv = dict(zip(tbl["segment"], tbl["iv_elasticity"]))

    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    x = np.arange(len(tbl)); w = .27
    ax.bar(x - w, tbl.true_elasticity, w, label="true", color=GREEN)
    ax.bar(x, tbl.ols_elasticity, w, label="OLS (biased)", color=RED)
    ax.bar(x + w, tbl.iv_elasticity, w, label="IV (causal)", color=BLUE)
    ax.axhline(-1, ls=":", c="gray"); ax.set_xticks(x); ax.set_xticklabels(tbl.segment)
    ax.set_ylabel("FX-margin elasticity"); ax.legend()
    ax.set_title("Channel elasticity: OLS understates price sensitivity, IV recovers it")
    fig.tight_layout(); fig.savefig(os.path.join(IMG, "role_fig1_channel_elasticity.png")); plt.close(fig)
    return tbl, iv


def distribution_block(panel, iv):
    banner("2 | DISTRIBUTION & CHANNEL ECONOMICS")
    pnl = channel_pnl(panel)
    with pd.option_context("display.float_format", lambda v: f"{v:,.2f}"):
        print(pnl[["gross_revenue", "commission_paid", "cost", "contribution",
                   "contribution_margin_pct", "contrib_share_pct"]].to_string())
    pos = channel_positioning(panel, elasticities=iv)
    print("\nRecommended competitive positioning (using causal elasticity):")
    print(pos[["channel", "elasticity_used", "commission_rate",
               "recommended_move", "uplift_vs_hold_pct"]].round(4).to_string(index=False))

    # Figure: P&L waterfall (stacked) + positioning uplift.
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    ax = axes[0]
    chs = pnl.index.tolist()
    contrib = pnl["contribution"].values / 1e6
    comm = pnl["commission_paid"].values / 1e6
    cost = pnl["cost"].values / 1e6
    ax.bar(chs, contrib, label="contribution", color=GREEN)
    ax.bar(chs, comm, bottom=contrib, label="commission (payaway)", color=ORANGE)
    ax.bar(chs, cost, bottom=contrib + comm, label="cost to serve", color=GREY)
    ax.set_ylabel("£m over 2 years"); ax.set_title("(a) Channel P&L: where gross revenue goes")
    ax.legend(fontsize=8)
    for i, ch in enumerate(chs):
        ax.text(i, (contrib + comm + cost)[i] + 1,
                f"{pnl['contribution_margin_pct'].values[i]:.0%}", ha="center", fontsize=8)

    ax = axes[1]
    order = ["digital", "retail", "agency", "post_office", "wholesale"]
    pos_i = pos.set_index("channel").loc[order]
    colors = [GREEN if "compete" in m or "undercut" in m else RED if "harvest" in m or "firm" in m else GREY
              for m in pos_i["recommended_move"]]
    ax.barh(order, pos_i["uplift_vs_hold_pct"] * 100, color=colors)
    for i, ch in enumerate(order):
        ax.text(pos_i["uplift_vs_hold_pct"].values[i] * 100 + 0.2, i,
                pos_i["recommended_move"].values[i], va="center", fontsize=8)
    ax.set_xlabel("FX-contribution uplift vs hold (%)")
    ax.set_title("(b) Recommended margin positioning by channel")
    fig.tight_layout(); fig.savefig(os.path.join(IMG, "role_fig2_distribution.png")); plt.close(fig)

    print("\nMargin-support break-even (10% FX-margin cut):")
    for ch, spec in DEFAULT_CHANNELS.items():
        r = margin_support_breakeven(iv.get(ch, spec.elasticity))
        print(f"  {ch:12s} eps={iv.get(ch, spec.elasticity):+.2f}  "
              f"implied +{r['implied_volume_uplift']:.1%} vs break-even "
              f"+{r['breakeven_volume_uplift']:.1%} -> "
              f"{'ACCRETIVE' if r['accretive'] else 'dilutive'}")
    return pnl, pos


def fair_value_block(portfolio):
    banner("3 | FCA CONSUMER DUTY — FAIR VALUE ASSESSMENT")
    sc = fair_value_scorecard(portfolio)
    with pd.option_context("display.float_format", lambda v: f"{v:,.3f}"):
        print(sc[["cards", "cost_pct_of_load", "avg_value_score",
                  "price_to_value", "pct_red", "status"]].to_string())
    vh = vulnerable_harm(portfolio)
    print(f"\nDifferential outcomes: vulnerable pay {vh['cost_gap_pp']:+.1f}pp more "
          f"({vh['vulnerable_cost_pct']:.1%} vs {vh['standard_cost_pct']:.1%}) for "
          f"lower value ({vh['vulnerable_value']:.2f} vs {vh['standard_value']:.2f}); "
          f"{vh['vulnerable_pct_red']:.0%} flagged Red vs {vh['standard_pct_red']:.0%}.")

    dfm = fair_value_metrics(portfolio)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    ax = axes[0]
    s = dfm.sample(min(4000, len(dfm)), random_state=1)
    for vul, col, lab in [(False, BLUE, "standard"), (True, RED, "vulnerable")]:
        d = s[s.vulnerable == vul]
        ax.scatter(d.value_score, d.cost_ratio * 100, s=8, alpha=.4, color=col, label=lab)
    ax.set_xlabel("benefit (value) score"); ax.set_ylabel("total price (% of load)")
    ax.set_title("(a) Price vs value — top-left = poor value (review)")
    ax.legend()

    ax = axes[1]
    piv = dfm.assign(group=np.where(dfm.vulnerable, "vulnerable", "standard")) \
             .groupby(["channel", "group"])["cost_ratio"].mean().mul(100).unstack()
    piv = piv.loc[["digital", "retail", "agency", "post_office", "wholesale"]]
    piv.plot(kind="bar", ax=ax, color={"standard": BLUE, "vulnerable": RED})
    ax.set_ylabel("total price (% of load)"); ax.set_xlabel("")
    ax.set_title("(b) Vulnerable customers pay more, esp. in high-fee channels")
    ax.tick_params(axis="x", rotation=0); ax.legend(title="")
    fig.tight_layout(); fig.savefig(os.path.join(IMG, "role_fig3_fair_value.png")); plt.close(fig)

    # The assessment is a stage-4 deliverable, so it is written where it is read.
    out = generate_fair_value_assessment(
        portfolio,
        os.path.join(os.path.dirname(HERE), "04_satisfy_the_regulator", "02_fair_value_assessment.md"))
    print(f"Wrote {os.path.basename(out)}")
    return sc, vh


def aop_block(panel, iv):
    banner("4 | ANNUAL OPERATING PLAN — SCENARIOS & COMPETITOR INTELLIGENCE")
    lines = revenue_lines(panel)
    print(f"Annualised gross revenue: £{lines.loc['TOTAL', 'gross_revenue']:,.0f} "
          f"(FX £{lines.loc['TOTAL', 'fx_revenue']:,.0f} + "
          f"fees £{lines.loc['TOTAL', 'fee_revenue']:,.0f})")
    sc = run_scenarios(panel, elasticities=iv)
    print("\nScenario analysis (vs base):")
    with pd.option_context("display.float_format", lambda v: f"{v:,.3f}"):
        print(sc[["scenario", "gross_revenue", "contribution",
                  "vs_base_contribution_pct"]].to_string(index=False))
    print("\nCompetitor sensitivity:")
    cs = competitor_sensitivity(panel, elasticities=iv)
    print(cs.round(4).to_string(index=False))

    # Figure: (a) revenue lines by channel, (b) scenario tornado, (c) bridge, (d) competitor.
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))

    ax = axes[0, 0]
    rl = lines.drop("TOTAL")[["fx_revenue", "fee_revenue"]] / 1e6
    rl.plot(kind="bar", stacked=True, ax=ax, color=[BLUE, ORANGE])
    ax.set_ylabel("£m / year"); ax.set_title("(a) AOP revenue build-up by channel")
    ax.tick_params(axis="x", rotation=20); ax.legend(["FX margin", "card/in-life fees"], fontsize=8)

    ax = axes[0, 1]
    s2 = sc[sc.scenario != "Base plan"].copy().sort_values("vs_base_contribution_pct")
    cols = [GREEN if v > 0 else RED for v in s2.vs_base_contribution_pct]
    ax.barh(s2.scenario, s2.vs_base_contribution_pct * 100, color=cols)
    ax.axvline(0, color="k", lw=.8); ax.set_xlabel("contribution vs base (%)")
    ax.set_title("(b) Scenario impact on contribution"); ax.tick_params(labelsize=8)

    ax = axes[1, 0]
    br = revenue_bridge(panel, {"volume_mult": 1.12, "margin_mult": 0.97, "competitor_mult": 0.92},
                        elasticities=iv)
    vals = br["contribution"].values / 1e6
    ax.plot(range(len(br)), vals, "o-", color=PURPLE)
    ax.set_xticks(range(len(br))); ax.set_xticklabels(br.step, rotation=20, fontsize=8)
    ax.set_ylabel("contribution (£m)")
    ax.set_title("(c) Revenue bridge: base → blended scenario")

    ax = axes[1, 1]
    ax.plot([float(m.strip("%")) for m in cs.competitor_move],
            cs.our_contribution_pct * 100, "o-", color=RED)
    ax.axhline(0, color="k", lw=.8); ax.axvline(0, color="k", lw=.8)
    ax.set_xlabel("competitor margin move (%)"); ax.set_ylabel("our contribution (%)")
    ax.set_title("(d) Competitor sensitivity (cross-elasticity)")
    fig.suptitle("Travel money AOP & competitor intelligence", y=1.0, fontsize=13)
    fig.tight_layout(); fig.savefig(os.path.join(IMG, "role_fig4_aop.png")); plt.close(fig)
    return lines, sc, cs


# --------------------------------------------------------------------------- #
def write_results(tbl, pnl, pos, sc_fv, vh, lines, sc_aop, cs, ci):
    L = ["# Role Case Study Results — Travel Money & Prepaid Card Pricing",
         "",
         "_Auto-generated by `run_role_case_study.py` (synthetic, fixed seed). "
         "Aligned to the Senior Manager, Pricing, Distribution & Revenue remit._",
         "",
         "## 1. Channel FX-margin elasticity (causal)",
         "",
         "| Channel | True ε | OLS ε | IV ε | First-stage F |",
         "|---|---:|---:|---:|---:|"]
    for _, r in tbl.iterrows():
        L.append(f"| {r['segment']} | {r['true_elasticity']:+.2f} | {r['ols_elasticity']:+.2f} "
                 f"| {r['iv_elasticity']:+.2f} | {r['first_stage_F']:,.0f} |")
    L += ["", "Digital is the most price-sensitive channel (price-transparent); wholesale the "
          "least. OLS understates sensitivity everywhere — pricing on it would "
          "systematically over-charge.", "",
          "## 2. Distribution economics", "",
          "| Channel | Gross rev | Commission | Cost | Contribution | Contrib margin | Rec. move |",
          "|---|---:|---:|---:|---:|---:|---|"]
    posi = pos.set_index("channel")
    for ch, r in pnl.iterrows():
        mv = posi.loc[ch, "recommended_move"] if ch in posi.index else "-"
        L.append(f"| {ch} | £{r['gross_revenue']/1e6:.1f}m | £{r['commission_paid']/1e6:.1f}m "
                 f"| £{r['cost']/1e6:.1f}m | £{r['contribution']/1e6:.1f}m "
                 f"| {r['contribution_margin_pct']:.0%} | {mv} |")
    L += ["", "The same FX margin earns very different *net* contribution by channel: "
          "the Post Office network pays ~45% of FX revenue away in Postmaster "
          "commission, retail carries the highest cost-to-serve, while digital drops "
          "almost all revenue to contribution. Elastic channels should compete on "
          "margin; inelastic channels (wholesale, Post Office) should harvest.", "",
          "## 3. FCA Consumer Duty — fair value", "",
          f"- Vulnerable customers pay **{vh['cost_gap_pp']:+.1f}pp** more "
          f"({vh['vulnerable_cost_pct']:.1%} of load vs {vh['standard_cost_pct']:.1%}) "
          f"for **lower** benefit, and **{vh['vulnerable_pct_red']:.0%}** are flagged Red "
          f"vs {vh['standard_pct_red']:.0%} of standard customers.",
          "- Driven by ATM and **inactivity fees eroding unspent balances** in the "
          "high-fee channels (agency, Post Office, retail).",
          "- See `../04_satisfy_the_regulator/02_fair_value_assessment.md` for the full assessment and "
          "remediation actions.", "",
          "## 4. Annual Operating Plan", "",
          f"Annualised gross revenue **£{lines.loc['TOTAL','gross_revenue']/1e6:.0f}m** "
          f"(FX £{lines.loc['TOTAL','fx_revenue']/1e6:.0f}m + fees "
          f"£{lines.loc['TOTAL','fee_revenue']/1e6:.0f}m). Scenario impact on contribution:",
          "", "| Scenario | Contribution vs base |", "|---|---:|"]
    for _, r in sc_aop[sc_aop.scenario != "Base plan"].iterrows():
        L.append(f"| {r['scenario']} | {r['vs_base_contribution_pct']:+.1%} |")
    L += ["", "Note a **uniform** +10% FX-margin rise *reduces* contribution (blended "
          "demand is elastic), whereas the channel-specific positioning in §2 *raises* "
          "it — uniform pricing moves destroy value; targeted ones create it.", "",
          "## Figures", "",
          "![Channel elasticity](images/role_fig1_channel_elasticity.png)",
          "![Distribution economics](images/role_fig2_distribution.png)",
          "![Fair value](images/role_fig3_fair_value.png)",
          "![AOP & competitor](images/role_fig4_aop.png)", ""]
    with open(os.path.join(HERE, "RESULTS.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))
    print(f"\nWrote RESULTS.md + 4 figures to images/.")


def main():
    banner("TRAVEL MONEY & PREPAID CARD PRICING — SENIOR MANAGER, PRICING, DISTRIBUTION & REVENUE")
    cfg = TravelMoneyConfig()
    panel = generate_channel_panel(cfg)
    portfolio = generate_card_portfolio(20000, cfg)
    print(f"Panel: {len(panel):,} channel-days | Portfolio: {len(portfolio):,} cards")

    tbl, iv = elasticity_block(panel)
    pnl, pos = distribution_block(panel, iv)
    sc_fv, vh = fair_value_block(portfolio)
    lines, sc_aop, cs = aop_block(panel, iv)
    ci = competitive_index(panel)
    write_results(tbl, pnl, pos, sc_fv, vh, lines, sc_aop, cs, ci)
    banner("DONE")


if __name__ == "__main__":
    main()
