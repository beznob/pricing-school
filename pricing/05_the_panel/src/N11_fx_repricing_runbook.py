# %% [markdown]
# # N11 · Sterling Drops 5% Overnight — the repricing runbook
#
# **Panel question** — the opening scenario, any interviewer: *"Sterling
# weakens 5% overnight. Walk me through what you do to spreads across channels
# this morning."*
#
# Not a statistics notebook — an **ops-arithmetic** one. The senior reflexes,
# in order: (1) hedge book first, (2) reprice off the new wholesale preserving
# **margin in bps** — never chase the market, (3) sequence by channel latency
# and honour locked orders, (4) check the comparison-site position before
# over/under-shooting, (5) watch cash availability (N3's problem arriving at
# speed), (6) Consumer Duty comms.

# %%
# %matplotlib inline
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from _style import C, apply_style
apply_style()

SHOCK = 0.05                                # GBP down 5% vs EUR/USD overnight

# --- Step 0, before anything: what does the hedge book say? ------------------
inventory = pd.DataFrame({
    "currency": ["EUR", "USD", "other"],
    "position_gbp_m": [6.5, 4.2, 2.3],      # cash we hold (bought at old rates)
    "hedge_cover": [0.70, 0.70, 0.40],      # forward-covered share
})
inventory["unhedged_m"] = inventory.position_gbp_m * (1 - inventory.hedge_cover)
# GBP weaker => our foreign-cash inventory is worth MORE in GBP; the exposure
# that hurts is the mirror: GBP we owe / restock cost. Net restock exposure:
inventory["restock_cost_uplift_m"] = inventory.unhedged_m * SHOCK
print(inventory.round(2).to_string(index=False))
exposure = inventory.restock_cost_uplift_m.sum()
print(f"\nUnhedged restock-cost exposure: £{exposure:.2f}m — the number to "
      "know BEFORE touching any retail rate. The point of the hedge book is "
      "that this morning is not a panic.")

# %% [markdown]
# ## 1. Reprice in margin bps off the NEW wholesale — don't chase the market
#
# The retail rate is `wholesale × (1 − margin)`. The controllable is the
# margin. Rebase to the new wholesale, hold the target bps; resist matching a
# competitor's knee-jerk overshoot.

# %%
old_wholesale = 1.1800                       # GBP/EUR
new_wholesale = old_wholesale * (1 - SHOCK)
TARGET_BPS = 430

rates = pd.DataFrame({
    "approach": ["stale (yesterday's rate)", "margin-in-bps rebase",
                 "chase competitor overshoot"],
    "customer_rate": [old_wholesale * (1 - TARGET_BPS / 1e4),
                      new_wholesale * (1 - TARGET_BPS / 1e4),
                      new_wholesale * (1 - 560 / 1e4)],
})
rates["effective_margin_bps"] = (1 - rates.customer_rate / new_wholesale) * 1e4
print(rates.round(4).to_string(index=False))
stale_bps = rates.effective_margin_bps.iloc[0]
print(f"\nYesterday's rate is now {stale_bps:.0f}bps of effective margin — "
      "NEGATIVE: every stale-rate sale hands out euros below this morning's "
      "replacement cost. Latency is not cosmetic.")

# %% [markdown]
# ## 2. Sequence by channel latency — and price the lag

# %%
channels = pd.DataFrame({
    "channel": ["app / web", "click-&-collect (new orders)", "ATM / kiosk",
                "branch POS", "partner (JL/W)"],
    "reprice_lag_hrs": [0.25, 0.25, 2, 6, 12],
    "daily_volume_m": [1.8, 0.9, 0.4, 2.6, 0.7],
})
# cost of the lag = volume sold at the stale rate x the ~5% mispricing
channels["stale_cost_k"] = (channels.daily_volume_m * 1e3
                            * (channels.reprice_lag_hrs / 12).clip(upper=1)
                            * SHOCK)              # £k over a 12h trading day
print(channels.round(2).to_string(index=False))
print(f"\nTotal cost of repricing lag this morning: "
      f"£{channels.stale_cost_k.sum():,.0f}k — dominated by branch POS and the "
      "partner estate. The fix is an out-of-cycle rate push runbook agreed "
      "with the network IN ADVANCE, not heroics on the day.")

# LOCKED click-&-collect orders: honour them. Price the promise, don't break it.
locked_book = 1.6      # £m ordered at old rates, not yet collected
lock_cost = locked_book * SHOCK * (1 - 0.70)     # unhedged share of the book
print(f"\nLocked C&C orders: £{locked_book}m at old rates -> honouring costs "
      f"~£{lock_cost*1e3:.0f}k after hedge cover. That is a Consumer Duty "
      "promise AND cheap marketing; breaking it is neither.")

# %% [markdown]
# ## 3. Comparison-site position — check before over/undershooting
#
# A 5% move scrambles every provider's rate for a few hours. Position is
# relative: if competitors lag, our rebased rate temporarily looks worse than
# their stale ones — do NOT panic-cut margin against rates that will vanish
# by noon.

# %%
comp = pd.DataFrame({
    "provider": ["us (rebased)", "supermarket (stale)", "bank (stale)",
                 "online specialist (rebased)", "airport (rebased)"],
    "eur_rate": [new_wholesale * (1 - 430 / 1e4), old_wholesale * (1 - 380 / 1e4),
                 old_wholesale * (1 - 450 / 1e4), new_wholesale * (1 - 180 / 1e4),
                 new_wholesale * (1 - 1050 / 1e4)],
    "stale": [False, True, True, False, False],
})
comp["rank_now"] = comp.eur_rate.rank(ascending=False).astype(int)
comp["true_margin_vs_new_wholesale_bps"] = ((1 - comp.eur_rate / new_wholesale)
                                            * 1e4).round(0)
print(comp.round(4).to_string(index=False))
print("\nThe stale supermarket rate 'beats' us this morning at NEGATIVE true "
      "margin — it will be gone by noon. Track rank against REBASED rates "
      "only; schedule a rank re-check at T+4h instead of reacting at T+0.")

# %% [markdown]
# ## 4. Demand spike & cash availability — N3 arriving at speed
#
# A big overnight move spikes walk-up demand ('get euros before it gets
# worse'). Yesterday's replenishment plan is now wrong.

# %%
spike, days = 1.6, 3
eur_daily = 2.2                    # £m/day normal EUR demand across the estate
extra = eur_daily * (spike - 1) * days
cover_days = inventory.loc[0, "position_gbp_m"] / (eur_daily * spike)
print(f"Demand spike x{spike} for ~{days} days -> +£{extra:.1f}m EUR demand.")
print(f"EUR inventory cover at spiked demand: {cover_days:.1f} days.")
print("Actions: pull forward the cash-centre run, rebalance from low-demand "
      "branches, and prioritise stockout-risk branches (the censoring in N3 "
      "means yesterday's 'sales' UNDERSTATE what Friday will ask for).")

# %% [markdown]
# ## 5. The runbook, on one page
#
# | T+ | Action | Owner |
# |---|---|---|
# | 0h | Read hedge book: unhedged exposure by currency (§0) | Treasury |
# | 0h | Rebase app/web/C&C rates: new wholesale, target bps held (§1) | Pricing |
# | 0h | Freeze auto-matching rules vs stale competitor rates (§3) | Pricing |
# | +1h | Confirm locked C&C book honoured; comms ready ("clear, fair, not misleading") | Ops + Compliance |
# | +2h | ATM/kiosk rate push | Ops |
# | +4h | Comparison-site rank re-check vs REBASED competitors (§3) | Pricing |
# | +6h | Branch POS out-of-cycle rate push (pre-agreed runbook) (§2) | Network |
# | +6h | Replenishment re-run with spike factor; branch cash rebalance (§4) | Cash ops |
# | +24h | Review: lag cost, rank, stockouts; update the runbook | All |
#
# ## The 60-second answer
#
# > "First call is the hedge book, not the rate card — with seventy percent
# > forward cover our unhedged restock exposure is about half a million on
# > this move, which means this morning is a process, not a panic. Then I
# > reprice off the *new* wholesale, holding target margin in basis points —
# > the margin is the controllable, and I will not chase competitors whose
# > screens are still showing yesterday's rates at what is now negative true
# > margin. Sequencing is by channel latency: app and web in minutes, and
# > every locked click-and-collect order gets honoured — that's a Consumer
# > Duty promise and cheap marketing. The expensive tail is branch POS, which
# > is why the out-of-cycle rate push is a pre-agreed runbook with the
# > network, not day-of heroics.
# >
# > Then the two second-order effects: comparison-site rank gets re-checked at
# > T-plus-four-hours against rebased rates only, and cash — a five percent
# > overnight move spikes walk-up demand, so the replenishment plan re-runs
# > this morning with a spike factor, prioritising the branches the stockout
# > model already flags. And customer comms stay 'clear, fair and not
# > misleading' — no 'rates improved!' spin on a sterling fall."
#
# ### What I'd say if pushed deeper
#
# 1. **"Why not widen spreads while volatility is high?"** — Intraday
#    volatility does justify a modest, symmetric widening — it's an inventory-
#    risk premium, the same economics as the surge controller's load-based
#    fee. But it must be a documented volatility rule with a cap, not a
#    discretionary grab on a day customers are anxious — that's the fairness
#    line.
# 2. **"What if the move happens over a weekend?"** — Worse case: branches
#    shut with Friday's rates loaded, gap risk on Monday's open. The runbook
#    needs a weekend variant: wider Friday-close margins into known event risk
#    (elections, central-bank decisions), and app/web repricing stays live.
# 3. **Honest limitation.** Every number here leans on the hedge ratios and
#    the locked-book size being *known this morning* — which is a statement
#    about data plumbing, not markets. If treasury's cover report arrives at
#    noon, the runbook fails at step zero; I'd test that feed's latency before
#    I trusted the playbook.
