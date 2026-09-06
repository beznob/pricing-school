"""
Synthetic data generator for a **travel money & prepaid FX card** business.

This reframes the case study onto the exact domain of the *Senior Manager,
Pricing, Distribution & Revenue* role: multi-channel travel money + prepaid
cards, where the primary price lever is the **FX margin** (the spread over the
wholesale/interbank rate) plus a set of card fees, sold through several channels
with very different economics (own digital, own retail, the **Post Office /
Postmaster** network, **TMC** B2B2C partners, and third-party **agencies**).

Two generators
--------------
* ``generate_channel_panel`` -> a channel x day panel used for **elasticity
  estimation**, **distribution economics** and **AOP scenario modelling**. It is
  deliberately *column-compatible with* ``elasticity_models.py`` (it emits
  ``log_volume``, ``log_fee`` = log FX margin, ``cost_shock_z`` instrument,
  ``season``, ``segment`` = channel, ``true_elasticity``) so we reuse the same
  causal IV/2SLS estimators without rewriting them.
* ``generate_card_portfolio`` -> a customer-level prepaid-card table used for the
  **FCA Consumer Duty fair-value** assessment (balances, lifecycle fees, usage,
  tenure, vulnerability flag).

As in the payments case study, the firm sets a *higher* FX margin in peak holiday
season when demand is high (endogeneity / surge), and a wholesale FX cost shock
serves as the instrument that recovers the true elasticity.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict

import numpy as np
import pandas as pd


# --------------------------------------------------------------------------- #
# Channel economics
# --------------------------------------------------------------------------- #
@dataclass
class ChannelSpec:
    name: str
    elasticity: float          # FX-margin elasticity of demand (< 0)
    base_margin: float         # typical FX margin (spread over wholesale), e.g. 0.035 = 3.5%
    base_daily_orders: float   # scale: orders/day at the reference margin
    commission_rate: float     # share of FX revenue paid away to the channel (Postmaster/agent)
    cost_to_serve: float       # £ variable cost per order borne by us
    issuance_share: float      # fraction of orders that are NEW cards (vs reloads)
    avg_order_value: float     # £ loaded per order
    margin_seasonality: float  # how hard the firm pushes margin up in peak season (endogeneity)


# Postmaster/agency channels carry high commission but low cost-to-serve to us;
# digital is price-transparent (most elastic) but cheap to serve; TMC is
# contracted/wholesale (least elastic, thin margin).
DEFAULT_CHANNELS: Dict[str, ChannelSpec] = {
    "digital": ChannelSpec("digital", -2.2, 0.022, 4200, 0.00, 1.20, 0.55, 720, 0.45),
    "retail": ChannelSpec("retail", -1.3, 0.036, 2600, 0.00, 7.50, 0.45, 780, 0.35),
    "post_office": ChannelSpec("post_office", -1.0, 0.039, 3400, 0.45, 2.10, 0.40, 820, 0.30),
    "tmc": ChannelSpec("tmc", -0.7, 0.018, 1500, 0.10, 1.80, 0.25, 1650, 0.20),
    "agency": ChannelSpec("agency", -1.2, 0.041, 1100, 0.30, 3.20, 0.50, 690, 0.30),
}


@dataclass
class TravelMoneyConfig:
    n_days: int = 730               # 2 years of daily data
    seed: int = 2026
    sigma_demand_shock: float = 0.30
    sigma_cost_shock: float = 0.55
    sigma_margin_noise: float = 0.06
    sigma_demand_noise: float = 0.08
    shock_persistence: float = 0.6
    channels: Dict[str, ChannelSpec] = field(
        default_factory=lambda: {k: v for k, v in DEFAULT_CHANNELS.items()}
    )


# --------------------------------------------------------------------------- #
# Seasonality (travel money is intensely seasonal)
# --------------------------------------------------------------------------- #
def _annual_season(day_of_year: np.ndarray) -> np.ndarray:
    """Summer holiday peak (Jul/Aug), a December spike, and an Easter bump."""
    doy = day_of_year
    summer = np.exp(-0.5 * ((doy - 210) / 35) ** 2)         # ~late July
    december = 0.6 * np.exp(-0.5 * ((doy - 350) / 14) ** 2)  # pre-Christmas travel
    easter = 0.4 * np.exp(-0.5 * ((doy - 100) / 18) ** 2)    # spring break
    return 0.55 + 1.0 * summer + december + easter


# --------------------------------------------------------------------------- #
# Channel x day panel
# --------------------------------------------------------------------------- #
def generate_channel_panel(config: TravelMoneyConfig | None = None) -> pd.DataFrame:
    config = config or TravelMoneyConfig()
    rng = np.random.default_rng(config.seed)

    day = np.arange(config.n_days)
    doy = day % 365
    season_idx = _annual_season(doy)                       # multiplicative demand index
    season = np.log(season_idx)                            # log-space control

    # Latent demand shock (AR(1)) shared across channels (macro travel appetite).
    eps = rng.normal(0, config.sigma_demand_shock, config.n_days)
    u = np.zeros(config.n_days)
    for t in range(1, config.n_days):
        u[t] = config.shock_persistence * u[t - 1] + eps[t]

    frames = []
    for spec in config.channels.values():
        # Wholesale FX cost / volatility shock -> the instrument.
        z = rng.normal(0, config.sigma_cost_shock, config.n_days)

        # Firm's margin policy: push margin up in peak season & when demand is hot
        # (endogeneity), and pass through wholesale cost (instrument relevance).
        log_margin = (
            np.log(spec.base_margin)
            + spec.margin_seasonality * (season - season.mean())
            + 0.5 * spec.margin_seasonality * u
            + 0.25 * z
            + rng.normal(0, config.sigma_margin_noise, config.n_days)
        )
        fx_margin = np.clip(np.exp(log_margin), 0.004, 0.075)
        log_margin = np.log(fx_margin)

        # Competitor market margin (what Travelex/Tesco/Wise-style rivals charge).
        competitor_margin = np.clip(
            spec.base_margin * np.exp(0.10 * rng.normal(0, 1, config.n_days) + 0.15 * u),
            0.004, 0.08,
        )

        # True demand: constant own-margin elasticity, plus a *cross*-price term
        # in the competitor's margin (cross-elasticity ~ +0.5, centred so it does
        # not contaminate the own-price slope). Both terms are centred at the base
        # margin so ``base_daily_orders`` stays the interpretable scale.
        cross_elasticity = 0.5
        log_orders = (
            np.log(spec.base_daily_orders)
            + spec.elasticity * (log_margin - np.log(spec.base_margin))
            + cross_elasticity * (np.log(competitor_margin) - np.log(spec.base_margin))
            + 0.8 * u
            + season
            + rng.normal(0, config.sigma_demand_noise, config.n_days)
        )
        orders = np.exp(log_orders)

        avg_order_value = np.clip(
            rng.lognormal(np.log(spec.avg_order_value), 0.18, config.n_days), 120, 6000
        )
        load_value = orders * avg_order_value

        # --- Revenue lines (these feed the AOP model) --------------------- #
        fx_revenue = fx_margin * load_value
        new_cards = orders * spec.issuance_share
        issuance_fee_rev = new_cards * 4.95                       # £4.95 card issue fee
        reload_value = load_value * (1 - spec.issuance_share)     # reload portion of load
        # In-life revenue: ATM withdrawals, FX on spend abroad, inactivity, breakage.
        atm_fee_rev = orders * 0.55 * 2.00                        # ~55% use ATM, £2 each
        inactivity_fee_rev = new_cards * 0.18 * 1.50             # dormant-card fees
        in_life_fx_rev = load_value * 0.012                       # FX on overseas spend
        fee_revenue = issuance_fee_rev + atm_fee_rev + inactivity_fee_rev + in_life_fx_rev

        gross_revenue = fx_revenue + fee_revenue
        commission_paid = spec.commission_rate * fx_revenue       # paid to channel
        cost = spec.cost_to_serve * orders
        contribution = gross_revenue - commission_paid - cost

        frames.append(pd.DataFrame({
            "day": day,
            "day_of_year": doy,
            "segment": spec.name,                # 'segment' so elasticity engine reuses it
            "channel": spec.name,
            # --- elasticity-engine-compatible columns ---
            "fee_rate": fx_margin,               # the "price" is the FX margin
            "fx_margin": fx_margin,
            "log_fee": log_margin,
            "volume": orders,
            "log_volume": log_orders,
            "cost_shock_z": z,                   # instrument
            "season": season,
            "true_elasticity": spec.elasticity,
            # --- travel-money economics ---
            "competitor_margin": competitor_margin,
            "avg_order_value": avg_order_value,
            "load_value": load_value,
            "new_cards": new_cards,
            "reload_value": reload_value,
            "commission_rate": spec.commission_rate,
            "cost_to_serve": spec.cost_to_serve,
            "fx_revenue": fx_revenue,
            "issuance_fee_rev": issuance_fee_rev,
            "atm_fee_rev": atm_fee_rev,
            "inactivity_fee_rev": inactivity_fee_rev,
            "in_life_fx_rev": in_life_fx_rev,
            "fee_revenue": fee_revenue,
            "gross_revenue": gross_revenue,
            "commission_paid": commission_paid,
            "cost": cost,
            "contribution": contribution,
        }))

    return pd.concat(frames, ignore_index=True)


# --------------------------------------------------------------------------- #
# Customer-level prepaid card portfolio (for the fair-value assessment)
# --------------------------------------------------------------------------- #
def generate_card_portfolio(
    n_cards: int = 20000, config: TravelMoneyConfig | None = None
) -> pd.DataFrame:
    """A portfolio of issued prepaid cards with lifecycle fees, for Consumer Duty."""
    config = config or TravelMoneyConfig()
    rng = np.random.default_rng(config.seed + 1)

    channel = rng.choice(list(config.channels.keys()), n_cards,
                         p=[0.42, 0.20, 0.22, 0.08, 0.08])
    specs = config.channels
    base_margin = np.array([specs[c].base_margin for c in channel])

    load_value = np.clip(rng.lognormal(np.log(650), 0.7, n_cards), 50, 12000)
    # Vulnerable customers: lower digital engagement, more likely high-fee channels.
    vulnerable = rng.random(n_cards) < 0.16

    # FX margin actually charged (some dispersion around channel base).
    fx_margin = np.clip(base_margin * rng.lognormal(0, 0.12, n_cards), 0.004, 0.08)
    fx_cost = fx_margin * load_value

    # Usage / spend-down. Vulnerable & older customers leave more unspent (breakage)
    # and incur more ATM / inactivity fees -> a fair-value red flag.
    spend_rate = np.clip(rng.beta(5, 2, n_cards) - 0.18 * vulnerable, 0.05, 1.0)
    spent = load_value * spend_rate
    breakage = load_value - spent                            # unspent balance

    n_atm = rng.poisson(2.0 + 1.5 * vulnerable, n_cards)
    atm_fees = n_atm * 2.00
    months_dormant = np.clip(rng.poisson(3 + 4 * vulnerable, n_cards), 0, 24)
    inactivity_fees = np.minimum(months_dormant * 1.50, breakage)  # capped at balance
    issuance_fee = np.where(rng.random(n_cards) < 0.6, 4.95, 0.0)

    total_fees = atm_fees + inactivity_fees + issuance_fee
    total_cost_to_customer = fx_cost + total_fees           # total price (Consumer Duty)
    cost_ratio = total_cost_to_customer / load_value        # price as % of value loaded

    # A simple 'benefit/value' score (speed, acceptance, security, convenience),
    # higher for digital/managed usage, lower when a card sits dormant.
    value_score = np.clip(
        0.60 + 0.25 * spend_rate - 0.20 * (months_dormant / 24)
        + 0.10 * (channel == "digital") - 0.08 * vulnerable
        + rng.normal(0, 0.05, n_cards),
        0.05, 1.0,
    )

    return pd.DataFrame({
        "card_id": np.arange(n_cards),
        "channel": channel,
        "vulnerable": vulnerable,
        "load_value": load_value,
        "fx_margin": fx_margin,
        "fx_cost": fx_cost,
        "spend_rate": spend_rate,
        "breakage": breakage,
        "n_atm": n_atm,
        "atm_fees": atm_fees,
        "months_dormant": months_dormant,
        "inactivity_fees": inactivity_fees,
        "issuance_fee": issuance_fee,
        "total_fees": total_fees,
        "total_cost_to_customer": total_cost_to_customer,
        "cost_ratio": cost_ratio,
        "value_score": value_score,
    })


def channel_truth(config: TravelMoneyConfig | None = None) -> pd.DataFrame:
    config = config or TravelMoneyConfig()
    return pd.DataFrame([
        {"channel": s.name, "true_elasticity": s.elasticity,
         "base_margin": s.base_margin, "commission_rate": s.commission_rate,
         "cost_to_serve": s.cost_to_serve}
        for s in config.channels.values()
    ])


if __name__ == "__main__":
    cfg = TravelMoneyConfig()
    panel = generate_channel_panel(cfg)
    print(f"Channel panel: {len(panel):,} channel-days "
          f"({panel['channel'].nunique()} channels x {panel['day'].nunique()} days)")
    summ = panel.groupby("channel").agg(
        fx_margin=("fx_margin", "mean"),
        orders_day=("volume", "mean"),
        gross_rev_day=("gross_revenue", "mean"),
        commission_day=("commission_paid", "mean"),
        contribution_day=("contribution", "mean"),
    )
    print(summ.round(3).to_string())

    port = generate_card_portfolio(20000, cfg)
    print(f"\nCard portfolio: {len(port):,} cards | "
          f"avg total cost to customer {port['cost_ratio'].mean():.1%} of load | "
          f"vulnerable share {port['vulnerable'].mean():.1%}")
