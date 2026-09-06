"""
Annual Operating Plan (AOP) revenue modelling, scenario analysis & competitor
intelligence for the travel-money / prepaid-card business.

This is the planning half of the role: build the revenue lines (new card sales,
reloads, in-life), flex them under **scenarios** (market growth, FX-margin moves,
competitor pressure, channel mix), produce a **revenue bridge**, and track a
**competitive price index** with cross-elasticity sensitivity.

The scenario engine is elasticity-aware: an FX-margin change flows through to
volume via the (causally estimated) own-price elasticity, and a competitor move
flows through via the cross-price elasticity.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from travel_money_simulator import DEFAULT_CHANNELS

CROSS_ELASTICITY = 0.5  # volume sensitivity to the competitor's margin (matches simulator)

REVENUE_LINES = ["fx_revenue", "issuance_fee_rev", "atm_fee_rev",
                 "inactivity_fee_rev", "in_life_fx_rev"]


# --------------------------------------------------------------------------- #
# Base plan
# --------------------------------------------------------------------------- #
def _annualise(panel: pd.DataFrame) -> float:
    """Scale factor to turn the panel total into a 12-month run-rate."""
    return 365.0 / panel["day"].nunique()


def revenue_lines(panel: pd.DataFrame) -> pd.DataFrame:
    """Annualised revenue by line and channel (the AOP build-up)."""
    f = _annualise(panel)
    g = panel.groupby("channel")[REVENUE_LINES].sum() * f
    g["fee_revenue"] = g[["issuance_fee_rev", "atm_fee_rev",
                          "inactivity_fee_rev", "in_life_fx_rev"]].sum(axis=1)
    g["gross_revenue"] = g["fx_revenue"] + g["fee_revenue"]
    g.loc["TOTAL"] = g.sum()
    return g


def _channel_base(panel: pd.DataFrame) -> pd.DataFrame:
    """Per-channel base aggregates used by the scenario engine (annualised)."""
    f = _annualise(panel)
    base = panel.groupby("channel").agg(
        orders=("volume", "sum"),
        fx_revenue=("fx_revenue", "sum"),
        fee_revenue=("fee_revenue", "sum"),
        commission_paid=("commission_paid", "sum"),
        cost=("cost", "sum"),
    ) * f
    base["commission_rate"] = [DEFAULT_CHANNELS[c].commission_rate for c in base.index]
    base["elasticity"] = [DEFAULT_CHANNELS[c].elasticity for c in base.index]
    return base


# --------------------------------------------------------------------------- #
# Scenario engine
# --------------------------------------------------------------------------- #
def project_scenario(
    panel: pd.DataFrame,
    volume_mult: float = 1.0,
    margin_mult: float = 1.0,
    competitor_mult: float = 1.0,
    digital_shift: float = 0.0,
    elasticities: dict | None = None,
) -> dict:
    """Project annual revenue & contribution under a scenario.

    Parameters
    ----------
    volume_mult : exogenous market growth/decline applied to all volume.
    margin_mult : FX-margin move (flows to volume via own elasticity).
    competitor_mult : competitor-margin move (flows to volume via cross-elasticity).
    digital_shift : fraction of *other* channels' volume reallocated to digital.
    """
    base = _channel_base(panel).copy()
    eps = {**{c: s.elasticity for c, s in DEFAULT_CHANNELS.items()}, **(elasticities or {})}

    out = {"fx_revenue": 0.0, "fee_revenue": 0.0, "commission_paid": 0.0,
           "cost": 0.0, "contribution": 0.0, "orders": 0.0}

    # Optional channel-mix shift toward digital.
    shift_pool = 0.0
    if digital_shift:
        for ch in base.index:
            if ch != "digital":
                moved = base.loc[ch, "orders"] * digital_shift
                shift_pool += moved

    for ch in base.index:
        e = eps[ch]
        vol_mult = (volume_mult * margin_mult ** e * competitor_mult ** CROSS_ELASTICITY)
        orders = base.loc[ch, "orders"] * vol_mult
        # apply mix shift
        if digital_shift:
            if ch == "digital":
                orders += shift_pool * (volume_mult)      # digital gains the pool
            else:
                orders *= (1 - digital_shift)
        scale = orders / base.loc[ch, "orders"]           # net order scaling for this channel

        fx_rev = base.loc[ch, "fx_revenue"] * margin_mult * scale
        fee_rev = base.loc[ch, "fee_revenue"] * scale
        commission = base.loc[ch, "commission_rate"] * fx_rev
        cost = base.loc[ch, "cost"] * scale
        out["fx_revenue"] += fx_rev
        out["fee_revenue"] += fee_rev
        out["commission_paid"] += commission
        out["cost"] += cost
        out["orders"] += orders

    out["gross_revenue"] = out["fx_revenue"] + out["fee_revenue"]
    out["contribution"] = out["gross_revenue"] - out["commission_paid"] - out["cost"]
    return out


def run_scenarios(panel: pd.DataFrame, elasticities: dict | None = None) -> pd.DataFrame:
    """A standard AOP scenario set."""
    scenarios = {
        "Base plan": {},
        "Upside (travel boom)": {"volume_mult": 1.12},
        "Downside (recession)": {"volume_mult": 0.88},
        "Raise FX margin +10%": {"margin_mult": 1.10},
        "Cut FX margin -10%": {"margin_mult": 0.90},
        "Competitor price war -15%": {"competitor_mult": 0.85},
        "Shift 10% volume to digital": {"digital_shift": 0.10},
    }
    base = project_scenario(panel, elasticities=elasticities)
    rows = []
    for name, kw in scenarios.items():
        s = project_scenario(panel, elasticities=elasticities, **kw)
        rows.append({
            "scenario": name,
            "gross_revenue": s["gross_revenue"],
            "contribution": s["contribution"],
            "vs_base_revenue_pct": s["gross_revenue"] / base["gross_revenue"] - 1,
            "vs_base_contribution_pct": s["contribution"] / base["contribution"] - 1,
        })
    return pd.DataFrame(rows)


def revenue_bridge(panel: pd.DataFrame, target: dict, elasticities: dict | None = None) -> pd.DataFrame:
    """Decompose the contribution change Base -> target scenario into driver effects.

    Sequential attribution: add one driver at a time (volume, then margin, then
    competitor) so the steps sum exactly to the total change.
    """
    drivers = ["volume_mult", "margin_mult", "competitor_mult", "digital_shift"]
    labels = {"volume_mult": "Market volume", "margin_mult": "FX margin",
              "competitor_mult": "Competitor", "digital_shift": "Channel mix"}
    defaults = {"volume_mult": 1.0, "margin_mult": 1.0, "competitor_mult": 1.0, "digital_shift": 0.0}

    state = dict(defaults)
    prev = project_scenario(panel, elasticities=elasticities, **state)["contribution"]
    rows = [{"step": "Base", "contribution": prev, "delta": 0.0}]
    for d in drivers:
        if d in target and target[d] != defaults[d]:
            state[d] = target[d]
            cur = project_scenario(panel, elasticities=elasticities, **state)["contribution"]
            rows.append({"step": labels[d], "contribution": cur, "delta": cur - prev})
            prev = cur
    rows.append({"step": "Target", "contribution": prev, "delta": 0.0})
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- #
# Competitor intelligence
# --------------------------------------------------------------------------- #
def competitive_index(panel: pd.DataFrame) -> pd.DataFrame:
    """Our FX margin vs the market, by channel. Index > 100 = we are dearer."""
    g = panel.groupby("channel").agg(
        our_margin=("fx_margin", "mean"),
        competitor_margin=("competitor_margin", "mean"),
    )
    g["price_index"] = 100 * g["our_margin"] / g["competitor_margin"]
    g["position"] = np.where(g["price_index"] > 103, "above market",
                     np.where(g["price_index"] < 97, "below market", "at market"))
    return g.sort_values("price_index", ascending=False)


def competitor_sensitivity(panel: pd.DataFrame, moves=(-0.15, -0.10, -0.05, 0.05, 0.10),
                           elasticities: dict | None = None) -> pd.DataFrame:
    """Revenue/contribution impact if the *competitor* moves their margin."""
    base = project_scenario(panel, elasticities=elasticities)
    rows = []
    for mv in moves:
        s = project_scenario(panel, competitor_mult=1 + mv, elasticities=elasticities)
        rows.append({
            "competitor_move": f"{mv:+.0%}",
            "our_revenue_pct": s["gross_revenue"] / base["gross_revenue"] - 1,
            "our_contribution_pct": s["contribution"] / base["contribution"] - 1,
        })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    from travel_money_simulator import TravelMoneyConfig, generate_channel_panel

    panel = generate_channel_panel(TravelMoneyConfig())

    print("AOP revenue build-up (annualised, £):")
    with pd.option_context("display.float_format", lambda v: f"{v:,.0f}"):
        print(revenue_lines(panel)[["fx_revenue", "fee_revenue", "gross_revenue"]].to_string())

    print("\nScenario analysis (vs base plan):")
    sc = run_scenarios(panel)
    with pd.option_context("display.float_format", lambda v: f"{v:,.3f}"):
        print(sc.to_string(index=False))

    print("\nCompetitive price index (>100 = dearer than market):")
    print(competitive_index(panel).round(2).to_string())

    print("\nCompetitor sensitivity:")
    print(competitor_sensitivity(panel).round(4).to_string(index=False))
