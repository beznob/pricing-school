"""
FCA Consumer Duty -- Price & Value (fair value) assessment for prepaid cards.

The Consumer Duty (PRIN 2A.4) requires firms to show that the **total price** a
customer pays is *reasonable relative to the overall benefits*. For a prepaid
travel card the total price is not just the FX margin -- it is the whole
lifecycle cost: FX spread + issuance + ATM withdrawals + **inactivity fees** that
erode unspent balances (**breakage**). Firms must also check for **differential
outcomes**, especially for **vulnerable customers**, and keep **documentation**
evidencing the assessment.

This module operationalises that:

* ``fair_value_metrics``        -> per-card total price, price-as-%-of-load, a
  benefit (value) score, and a price-to-value ratio with a RAG flag.
* ``fair_value_scorecard``      -> the assessment by segment (channel x vulnerability).
* ``vulnerable_harm``           -> differential-outcomes test (vulnerable vs not).
* ``generate_fair_value_assessment`` -> a written fair-value assessment (the
  regulatory documentation the role must produce).

Reference: FCA PRIN 2A.4 and FG22/5; FCA review of fair value frameworks (2023).
"""

from __future__ import annotations

import os

import numpy as np
import pandas as pd


GREEN, AMBER, RED = "Green", "Amber", "Red (review)"


# --------------------------------------------------------------------------- #
def fair_value_metrics(portfolio: pd.DataFrame) -> pd.DataFrame:
    """Add Consumer Duty price/value fields to the card portfolio.

    * ``cost_ratio``      -- total lifetime price as a % of value loaded.
    * ``price_to_value``  -- price (cost_ratio) per unit of benefit (value_score);
      higher = worse value.
    * ``inactivity_drag`` -- inactivity fees as a % of the unspent balance (a
      direct measure of balance erosion -- the classic prepaid harm).
    * ``fv_flag``         -- RAG status from the price-to-value distribution.
    """
    df = portfolio.copy()
    df["price_to_value"] = df["cost_ratio"] / df["value_score"].clip(lower=0.05)
    df["inactivity_drag"] = df["inactivity_fees"] / df["breakage"].clip(lower=1.0)

    # RAG thresholds from the portfolio's own distribution (benchmark-relative).
    p50, p85 = df["price_to_value"].quantile([0.50, 0.85])
    df["fv_flag"] = np.select(
        [df["price_to_value"] <= p50, df["price_to_value"] <= p85],
        [GREEN, AMBER], default=RED,
    )
    return df


def fair_value_scorecard(portfolio: pd.DataFrame) -> pd.DataFrame:
    """Fair value assessment by segment (channel x vulnerability)."""
    df = fair_value_metrics(portfolio)
    df["group"] = np.where(df["vulnerable"], "vulnerable", "standard")
    g = df.groupby(["channel", "group"]).agg(
        cards=("card_id", "count"),
        avg_load=("load_value", "mean"),
        cost_pct_of_load=("cost_ratio", "mean"),
        avg_value_score=("value_score", "mean"),
        price_to_value=("price_to_value", "mean"),
        breakage_pct=("breakage", lambda s: (s / df.loc[s.index, "load_value"]).mean()),
        inactivity_drag=("inactivity_drag", "mean"),
        pct_red=("fv_flag", lambda s: (s == RED).mean()),
    )
    # Segment-level RAG: red if poor value *and* a material red tail.
    bench = df["price_to_value"].median()
    g["status"] = np.select(
        [(g["price_to_value"] > 1.4 * bench) | (g["pct_red"] > 0.30),
         (g["price_to_value"] > 1.1 * bench) | (g["pct_red"] > 0.15)],
        [RED, AMBER], default=GREEN,
    )
    return g.sort_values("price_to_value", ascending=False)


def vulnerable_harm(portfolio: pd.DataFrame) -> dict:
    """Differential-outcomes test: do vulnerable customers get worse value?"""
    df = fair_value_metrics(portfolio)
    vul = df[df["vulnerable"]]
    std = df[~df["vulnerable"]]
    return {
        "vulnerable_cost_pct": vul["cost_ratio"].mean(),
        "standard_cost_pct": std["cost_ratio"].mean(),
        "cost_gap_pp": (vul["cost_ratio"].mean() - std["cost_ratio"].mean()) * 100,
        "vulnerable_value": vul["value_score"].mean(),
        "standard_value": std["value_score"].mean(),
        "vulnerable_inactivity_drag": vul["inactivity_drag"].mean(),
        "standard_inactivity_drag": std["inactivity_drag"].mean(),
        "vulnerable_pct_red": (vul["fv_flag"] == RED).mean(),
        "standard_pct_red": (std["fv_flag"] == RED).mean(),
    }


def identify_remediation(portfolio: pd.DataFrame, top_n: int = 3) -> pd.DataFrame:
    """The worst segments to prioritise for fair-value remediation."""
    sc = fair_value_scorecard(portfolio).reset_index()
    red = sc[sc["status"] == RED].copy()
    red["priority_score"] = red["price_to_value"] * red["cards"]
    return red.sort_values("priority_score", ascending=False).head(top_n)


# --------------------------------------------------------------------------- #
def generate_fair_value_assessment(portfolio: pd.DataFrame, out_path: str) -> str:
    """Write a Consumer Duty fair-value assessment document to ``out_path``."""
    df = fair_value_metrics(portfolio)
    sc = fair_value_scorecard(portfolio)
    vh = vulnerable_harm(portfolio)
    rem = identify_remediation(portfolio)

    n = len(df)
    overall_cost = df["cost_ratio"].mean()
    pct_red = (df["fv_flag"] == RED).mean()
    breakage_total = df["breakage"].sum()
    inactivity_total = df["inactivity_fees"].sum()

    L = []
    L.append("# 4.2 · Fair Value Assessment — Prepaid Travel Card (FCA Consumer Duty, PRIN 2A.4)")
    L.append("")
    L.append("_Auto-generated by `fair_value.py`. Illustrative, synthetic portfolio._")
    L.append("")
    L.append("## 1. Scope & method")
    L.append("")
    L.append(f"Assessment of **{n:,}** in-life prepaid cards. We compare the **total "
             "price** a customer pays over the product lifecycle (FX margin + "
             "issuance + ATM + inactivity fees) against the **benefits** (speed, "
             "acceptance, security, FX certainty, convenience), and test for "
             "**differential outcomes** for vulnerable customers, per FG22/5.")
    L.append("")
    L.append("## 2. Headline result")
    L.append("")
    L.append(f"- Average total price paid: **{overall_cost:.1%} of value loaded**.")
    L.append(f"- Cards flagged **Red** on price-to-value: **{pct_red:.1%}**.")
    L.append(f"- Unspent balances (breakage): **£{breakage_total:,.0f}**; inactivity "
             f"fees charged on dormant balances: **£{inactivity_total:,.0f}** "
             "— a priority area: charges that erode unspent balances are a known "
             "prepaid fair-value harm.")
    L.append("")
    L.append("## 3. Differential outcomes — vulnerable customers")
    L.append("")
    L.append("| Metric | Vulnerable | Standard | Gap |")
    L.append("|---|---:|---:|---:|")
    L.append(f"| Total price (% of load) | {vh['vulnerable_cost_pct']:.1%} | "
             f"{vh['standard_cost_pct']:.1%} | {vh['cost_gap_pp']:+.1f}pp |")
    L.append(f"| Benefit (value) score | {vh['vulnerable_value']:.2f} | "
             f"{vh['standard_value']:.2f} | "
             f"{vh['vulnerable_value']-vh['standard_value']:+.2f} |")
    L.append(f"| Inactivity drag (fees / unspent) | {vh['vulnerable_inactivity_drag']:.1%} | "
             f"{vh['standard_inactivity_drag']:.1%} | "
             f"{(vh['vulnerable_inactivity_drag']-vh['standard_inactivity_drag'])*100:+.1f}pp |")
    L.append(f"| Cards flagged Red | {vh['vulnerable_pct_red']:.1%} | "
             f"{vh['standard_pct_red']:.1%} | "
             f"{(vh['vulnerable_pct_red']-vh['standard_pct_red'])*100:+.1f}pp |")
    L.append("")
    verdict = ("**Material differential outcome identified**" if vh["cost_gap_pp"] > 0.5
               else "No material differential outcome")
    L.append(f"Verdict: {verdict}. Vulnerable customers pay "
             f"{vh['cost_gap_pp']:+.1f}pp more for {'lower' if vh['vulnerable_value']<vh['standard_value'] else 'similar'} "
             "benefit, driven mainly by ATM and inactivity charges on lower, "
             "less-actively-spent balances.")
    L.append("")
    L.append("## 4. Segment scorecard (worst-value first)")
    L.append("")
    L.append("| Channel | Group | Cards | Price (% load) | Value | Price/Value | % Red | Status |")
    L.append("|---|---|---:|---:|---:|---:|---:|---|")
    for (ch, grp), r in sc.iterrows():
        L.append(f"| {ch} | {grp} | {int(r['cards']):,} | {r['cost_pct_of_load']:.1%} | "
                 f"{r['avg_value_score']:.2f} | {r['price_to_value']:.2f} | "
                 f"{r['pct_red']:.0%} | {r['status']} |")
    L.append("")
    L.append("## 5. Remediation priorities & actions")
    L.append("")
    if len(rem):
        for _, r in rem.iterrows():
            L.append(f"- **{r['channel']} / {r['group']}** "
                     f"({int(r['cards']):,} cards, price/value {r['price_to_value']:.2f}): "
                     "review FX margin and cap inactivity fees on dormant balances; "
                     "proactive balance-return / spend-down prompts.")
    else:
        L.append("- No segment breaches the Red threshold; continue monitoring.")
    L.append("")
    L.append("**Standard actions to evidence fair value:** cap inactivity fees at the "
             "remaining balance (no negative balances), auto-refund small dormant "
             "balances, clear pre-purchase disclosure of total cost, a cheaper "
             "digital option signposted to price-sensitive and vulnerable customers, "
             "and a quarterly re-assessment with these metrics.")
    L.append("")

    os.makedirs(os.path.dirname(out_path), exist_ok=True) if os.path.dirname(out_path) else None
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))
    return out_path


if __name__ == "__main__":
    from travel_money_simulator import TravelMoneyConfig, generate_card_portfolio

    port = generate_card_portfolio(20000, TravelMoneyConfig())

    print("Fair value scorecard (worst value first):")
    sc = fair_value_scorecard(port)
    with pd.option_context("display.float_format", lambda v: f"{v:,.3f}"):
        print(sc[["cards", "cost_pct_of_load", "avg_value_score",
                  "price_to_value", "inactivity_drag", "pct_red", "status"]].to_string())

    print("\nVulnerable-customer differential outcomes:")
    for k, v in vulnerable_harm(port).items():
        print(f"  {k:30s} {v:.4f}")

    # The assessment is a stage-4 deliverable, so it is written where it is read.
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = generate_fair_value_assessment(
        port, os.path.join(root, "04_satisfy_the_regulator", "02_fair_value_assessment.md"))
    print(f"\nWrote {out}")
