# 2.4 · Forecasting and Stockouts — when your own data lies to you

## 1. Forecasting in plain words

A **forecast** is a structured best guess about future demand, built from
history. For a currency branch the workhorse is embarrassingly simple:

> "Next Friday will look like recent Fridays, adjusted for the season."

- **Seasonality** — repeating patterns: Fridays beat Tuesdays, July beats
  January, school holidays spike everything. Most retail forecasting is
  90% getting seasonality right.
- **Trend** — the slow drift up or down underneath the pattern.
- **Noise** — the leftover wobble nobody can predict. ([File 2.1](01_averages_and_uncertainty.md)'s spread.)

Why a *pricing* manager cares: forecasts decide how much **stock** (here,
physical cash in each currency) sits in each branch. And stock, it turns
out, quietly corrupts the very data your pricing analysis runs on.

## 2. The stockout — and the customer your till never met

A **stockout**: the branch runs out of euros at 2pm on a busy Friday.
Customers keep arriving until closing; they're turned away.

Now look at what the data recorded. Say true demand was **£33k** but the
branch only had **£26k** in the drawer:

> The till shows **sales = £26k**. Nowhere does it show the £7k that walked
> out the door. **Your data never records the customer you turned away.**

The technical word is that the sales figure is **censored** — cut off at the
stock level. Sales and demand are different things, and they differ exactly
on the days that matter most (your busiest ones).

## 3. The death spiral — the most beautiful trap in this track

Watch what happens when a *forecast* is trained on *censored sales*:

1. Friday demand is £33k, stock is £30k → till records £30k.
2. The forecast learns "Fridays ≈ £30k" → next order: £30k *(a bit less,
   with averaging)*.
3. Stock arrives lower → till records even less → forecast learns less →
   orders less…

Round and round: **under-forecast → under-stock → more censoring → deeper
under-forecast.** In the repo's simulation, Friday stock walks from £33k
down to £21k over thirty weeks *while true demand never changed*. Every step
looked reasonable. The system starved itself — and the P&L never showed the
lost sales as a line item, because *money you never took has no line*.

## 4. Getting out of the spiral

The core move is to stop treating stockout-day sales as demand:

- **Flag the stockout days** (the till knows when the drawer hit zero — or
  infer it: sales exactly equal to stock is a giveaway).
- On those days, read the number as "**demand was at least this much**",
  not "demand was this much".
- Refit the forecast with that reading. Statisticians have standard tools
  for "at least" data (censored models); the *idea* is just: a day you sold
  out is a floor, not a measurement.
- Where a weekday has been starved so long that almost every day is a
  sellout, the data can't tell you the truth at all — deliberately
  **over-stock a probe week** and *measure*.

In the repo's simulation, the naive forecast understated Friday demand by
**40%**; the censored-aware refit got within a few percent of the truth from
the *same corrupted history* — and the same ordering rule, fed the honest
forecast, stopped spiralling.

## 5. Where pricing fits (last, on purpose)

"We sell out every Friday — should we charge more on Fridays?" The senior
answer, in order:

1. **It's an ops problem first.** Fix the forecast (free), then the cash
   logistics. Most "pricing problems" at stockout branches are supply
   problems wearing a disguise.
2. **Price only the residual.** If a hard physical limit remains (the cash
   van can only carry so much), a *modest* Friday premium that nudges some
   customers to Thursday can be worth a few percent.
3. **Mind the fairness line** ([File 4.1](../04_satisfy_the_regulator/01_segments_and_fairness.md)): the Friday walk-up customer is
   captive. Surge-pricing captive customers in a regulated business is
   exactly where fair value bites. Modest, documented, and with a cheaper
   alternative signposted — or not at all.

## 6. Check yourself

**Q1.** A branch's Saturday sales are remarkably *consistent*: £18.0k,
£18.0k, £17.9k, £18.0k… A junior says "great, low noise, easy to forecast."
What do you suspect?

**Q2.** True Friday demand £30k; stock £24k. What does the till record, and
what's the honest sentence about that number?

**Q3.** Your fix raises Friday stock and sales jump 20%. Marketing claims
their campaign did it. How do you settle it? (One word from [File 2.2](02_tests_and_experiments.md).)

---

### Answers

**A1.** Suspiciously flat at a round-ish number = probably **selling out
every Saturday** — you're looking at the stock level, not demand. Check the
stockout flags; consider a probe week with extra stock.

**A2.** Till records **£24k**. Honest sentence: "Friday demand was **at
least** £24k — the drawer emptied, so the true number is higher."

**A3.** **Holdout** — raise stock at most branches, keep a random set on the
old plan, compare ([File 2.2](02_tests_and_experiments.md)). If the campaign did it, the holdout branches
jump too; if the stock fix did it, they don't.

---

## Where this idea goes — the ladder

1. **This file:** sales ≠ demand, censoring, the death spiral, and
   ops-before-pricing.
2. **[File 2.1](01_averages_and_uncertainty.md)'s suspicion, sharpened:** a sales figure is a summary that
   hides what didn't happen. The suspiciously flat Saturdays in Q1 are the
   same reflex as "averaged over whom?" — always ask what the number
   *couldn't* record.
3. **[The distributions appendix](../appendix/distributions_for_pricing.md) gives demand a shape:** arrivals are Poisson or negative
   binomial, order sizes log-normal. A stockout *clips the top off* those
   shapes — which is why "demand was at least £24k" needs censored-aware
   fitting rather than ordinary averaging.
4. **[File 2.2](02_tests_and_experiments.md) settles the credit:** when your stock fix and marketing's
   campaign land in the same month, only a **holdout** says whose win it
   was. And the probe week (§4) is a tiny experiment wearing this file's
   clothes.
5. **[File 4.1](../04_satisfy_the_regulator/01_segments_and_fairness.md) guards the pricing rung:** if a hard limit remains and you
   price the scarcity, remember the Friday walk-up is a **captive
   customer** — modest, documented, signposted, or not at all.
6. **In code:**
   [`../05_the_panel/N3_censored_demand_stockouts.ipynb`](../05_the_panel/N3_censored_demand_stockouts.ipynb)
   runs the whole spiral live — the chart of stock walking away from demand
   is the single most persuasive image in the repo — then arrests it with
   the censored-aware refit.
