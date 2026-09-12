"""
Distribution & channel economics for the travel-money / prepaid-card business.

This is the "Distribution & Revenue" half of the role: the same FX margin earns
very different *net* contribution depending on the channel's **commission**
(Postmaster / agency payaway) and **cost-to-serve**. Owning the pricing
architecture means optimising margin *per channel*, and knowing when "margin
support" (a deliberate giveaway to defend volume) actually pays for itself.

Functions
---------
* ``channel_pnl``              -> per-channel revenue / commission / cost / contribution.
* ``margin_waterfall``         -> decompose £1 of FX margin into payaway, cost, kept.
* ``channel_optimal_margin``   -> profit-max FX margin per channel (net of commission).
* ``margin_support_breakeven`` -> volume uplift required to fund a margin giveaway,
                                  and whether the channel's elasticity delivers it.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from travel_money_simulator import DEFAULT_CHANNELS


# --------------------------------------------------------------------------- #
def channel_pnl(panel: pd.DataFrame) -> pd.DataFrame:
    """Aggregate the channel x day panel into a per-channel P&L."""
    agg = panel.groupby("channel").agg(
        orders=("volume", "sum"),
        load_value=("load_value", "sum"),
        fx_revenue=("fx_revenue", "sum"),
        fee_revenue=("fee_revenue", "sum"),
        gross_revenue=("gross_revenue", "sum"),
        commission_paid=("commission_paid", "sum"),
        cost=("cost", "sum"),
        contribution=("contribution", "sum"),
        avg_margin=("fx_margin", "mean"),
    )
    agg["contribution_margin_pct"] = agg["contribution"] / agg["gross_revenue"]
    agg["take_rate_on_load"] = agg["gross_revenue"] / agg["load_value"]   # revenue / £ loaded
    agg["net_take_on_load"] = agg["contribution"] / agg["load_value"]     # kept / £ loaded
    agg["rev_share_pct"] = agg["gross_revenue"] / agg["gross_revenue"].sum()
    agg["contrib_share_pct"] = agg["contribution"] / agg["contribution"].sum()
    return agg.sort_values("contribution", ascending=False)


def margin_waterfall(panel: pd.DataFrame, channel: str) -> pd.DataFrame:
    """Decompose gross revenue per £ loaded into payaway / cost / kept (one channel)."""
    sub = panel[panel["channel"] == channel]
    load = sub["load_value"].sum()
    rows = [
        ("Gross revenue", sub["gross_revenue"].sum() / load),
        ("- Channel commission", -sub["commission_paid"].sum() / load),
        ("- Cost to serve", -sub["cost"].sum() / load),
        ("= Net contribution", sub["contribution"].sum() / load),
    ]
    return pd.DataFrame(rows, columns=["component", "per_£_loaded"])


# --------------------------------------------------------------------------- #
# Competitive positioning: evaluate discrete, realistic strategic moves rather
# than an unconstrained FOC. With cost-to-serve tiny relative to order value, the
# textbook marginal-cost markup collapses to the floor; the *real* decision a
# pricing manager makes is "where do we sit vs the market?", trading margin for
# volume (and the fee income that rides on volume). The causal elasticity drives
# the volume response, so the best position reflects how elastic the channel is.
# --------------------------------------------------------------------------- #
POSITION_MOVES = {
    "-15% (compete hard)": 0.85,
    "-5% (undercut)": 0.95,
    "hold": 1.00,
    "+5% (firm up)": 1.05,
    "+15% (harvest)": 1.15,
}


def _contribution_at_move(sub: pd.DataFrame, spec, eps: float, move: float) -> float:
    """FX-line contribution if the FX margin is multiplied by ``move``.

    We judge the **spread** decision on FX economics only (FX revenue net of
    channel commission and cost-to-serve). Card/in-life fee income is a separate
    monetisation lever -- folding it in here would turn every spread call into a
    volume grab. Volume responds with the (causal) elasticity.
    """
    vol_mult = move ** eps                                  # (m_new/m_cur)^elasticity
    fx_rev = sub["fx_revenue"].sum() * move * vol_mult      # margin x load, both move
    commission = spec.commission_rate * fx_rev
    cost = sub["cost"].sum() * vol_mult
    return fx_rev - commission - cost


def channel_positioning(panel: pd.DataFrame, elasticities: dict | None = None) -> pd.DataFrame:
    """Best competitive margin position per channel, given the causal elasticity.

    Returns, for each channel, the contribution under each strategic move and the
    recommended move (the contribution-maximising one). Elastic channels (digital)
    should compete on margin; inelastic channels (wholesale, Post Office) should harvest.
    """
    rows = []
    for ch, spec in DEFAULT_CHANNELS.items():
        sub = panel[panel["channel"] == ch]
        eps = (elasticities or {}).get(ch, spec.elasticity)
        contribs = {lbl: _contribution_at_move(sub, spec, eps, mv)
                    for lbl, mv in POSITION_MOVES.items()}
        hold = contribs["hold"]                              # FX-line baseline
        best_label = max(contribs, key=contribs.get)
        rows.append({
            "channel": ch,
            "elasticity_used": round(eps, 2),
            "commission_rate": spec.commission_rate,
            "fx_contribution_hold": hold,
            "recommended_move": best_label,
            "best_fx_contribution": contribs[best_label],
            "uplift_vs_hold_pct": contribs[best_label] / hold - 1,
            **{lbl: contribs[lbl] for lbl in POSITION_MOVES},
        })
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- #
def margin_support_breakeven(elasticity: float, margin_cut_pct: float = 0.10) -> dict:
    """Is a margin giveaway self-funding?

    Cutting the FX margin by ``margin_cut_pct`` reduces contribution per order but
    lifts volume. Returns the **break-even volume uplift** needed to hold total
    contribution and the **elasticity-implied uplift** actually delivered. If
    implied > break-even, the giveaway is accretive (a green light for "margin
    support" to defend a channel).
    """
    m1_over_m0 = 1 - margin_cut_pct
    # Approx: contribution per order scales with margin (fees/cost aside), so the
    # break-even volume multiplier is ~ 1 / (1 - cut). Elasticity delivers
    # (m1/m0)**elasticity.
    breakeven_mult = 1.0 / m1_over_m0
    implied_mult = m1_over_m0 ** elasticity
    return {
        "margin_cut_pct": margin_cut_pct,
        "breakeven_volume_uplift": breakeven_mult - 1,
        "implied_volume_uplift": implied_mult - 1,
        "accretive": implied_mult > breakeven_mult,
        "net_contribution_change_pct": implied_mult * m1_over_m0 - 1,
    }


if __name__ == "__main__":
    from travel_money_simulator import TravelMoneyConfig, generate_channel_panel

    panel = generate_channel_panel(TravelMoneyConfig())

    print("Per-channel P&L (2 years):")
    pnl = channel_pnl(panel)
    cols = ["gross_revenue", "commission_paid", "cost", "contribution",
            "contribution_margin_pct", "net_take_on_load", "contrib_share_pct"]
    with pd.option_context("display.float_format", lambda v: f"{v:,.3f}"):
        print(pnl[cols].to_string())

    print("\nPost Office margin waterfall (per £ loaded):")
    print(margin_waterfall(panel, "post_office").to_string(index=False))

    print("\nCompetitive positioning (recommended move by channel):")
    pos = channel_positioning(panel)
    print(pos[["channel", "elasticity_used", "commission_rate",
               "recommended_move", "uplift_vs_hold_pct"]].round(4).to_string(index=False))

    print("\nMargin-support break-even (10% margin cut):")
    for ch, spec in DEFAULT_CHANNELS.items():
        r = margin_support_breakeven(spec.elasticity)
        print(f"  {ch:12s} eps={spec.elasticity:+.1f}  "
              f"break-even +{r['breakeven_volume_uplift']:.1%}  "
              f"implied +{r['implied_volume_uplift']:.1%}  "
              f"-> {'ACCRETIVE' if r['accretive'] else 'dilutive'}")
