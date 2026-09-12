# 1.2 · Percentages, Basis Points, and Where the FX Price Hides

## 1. Three ways to say "how much" — don't mix them up

**Percent (%)** — parts per hundred. 5% of £200 = £10.

**Percentage point (pp)** — the *difference between two percentages*.
If your margin goes from 4% to 5%, it rose **1 percentage point** — but as a
relative change it rose 25% (because 5 is a quarter bigger than 4). Saying
"margin up 25%" and "margin up 1 point" describe the same event. People get
badly confused here; pricing managers say "points" when comparing rates.

**Basis point (bp)** — one hundredth of a percentage point.
> **100 bps = 1%. So 1 bp = 0.01%.**

Why bother? Because in currency, banking and insurance, the numbers that
matter are tiny. "We moved the margin from 4.30% to 4.35%" is clumsy;
"we moved it 5 bps" is precise and quick. Get fluent in this — it's the
native language of the trade.

| Plain English | In bps |
|---|---|
| half a percent | 50 bps |
| 4.3% | 430 bps |
| 0.05% | 5 bps |

## 2. Exchange rates in 60 seconds

An **exchange rate** is a price: how many euros one pound buys.

- The **interbank rate** (also "mid-market" or "wholesale") is the rate big
  banks trade at with each other — the fair, no-profit rate. Say **1.18**
  euros per pound today.
- The rate a shop offers *you* is worse — say **1.13**. The gap is where the
  shop earns its money.

That gap is called the **spread** (or the **FX margin**):

> **Spread = (interbank − retail) ÷ interbank = (1.18 − 1.13) ÷ 1.18 ≈ 4.2% = 420 bps**

## 3. The "0% commission" trick — the most important idea in this file

Shops advertise **"0% commission!"**. True — no fee line appears on your
receipt. But the profit didn't disappear; it moved **inside the exchange
rate**. You paid 420 bps without ever seeing a charge.

This is called an **implicit margin** — implicit meaning *hidden in the
rate rather than shown as a fee*. Compare two ways of charging for £500 of euros:

| | You see | You actually pay |
|---|---|---|
| Fee model (e.g. Wise) | rate 1.18 + "fee £3" | £3 (0.6%) — visible |
| Spread model (high street) | rate 1.13, "0% commission" | ~£21 (4.2%) — invisible |

Neither is dishonest by itself — but a pricing manager must always compare
**total cost to the customer**, not the headline. (UK regulators care about
exactly this; see [File 4.1](../04_satisfy_the_regulator/01_segments_and_fairness.md).)

## 4. Buy rate, sell rate, and buyback

The shop quotes **two** rates:

- **Sell rate** — the rate when the shop *sells you* euros (you're going on
  holiday). Worse than interbank *in one direction*.
- **Buy rate** — the rate when the shop *buys back* your leftover euros
  (you've come home). Worse than interbank *in the other direction*.

The shop earns on both trips. **Buyback** (selling your leftovers back) is
typically 150–250 bps worse again than the sell rate. A customer who buys
€1,000 and returns €200 pays the spread twice on that €200.

## 5. Tiered rates — a discount for size

Many shops give a better rate for bigger orders: for example a rate
improvement at £400, £500 and £1,000. This is a **tier** (or volume
discount). Two reasons to do it:

1. Big orders are cheaper *per pound* to serve (one till visit either way).
2. Big-order customers shop around more, so they need a sharper price.

Remember tiers — they come back in [File 1.4](04_price_volume_mix_and_leakage.md) as a place where money leaks
(what if the till gives the £1,000 rate to a £300 order by mistake?).

## 6. Check yourself

**Q1.** The interbank rate is 1.20; a kiosk offers 1.08. What's the spread
in % and in bps?

**Q2.** Margin moved from 430 bps to 460 bps. Describe the change in
(a) basis points, (b) percentage points, (c) relative percent.

**Q3.** A "0% commission" shop offers 1.13 (interbank 1.18). A rival charges
the interbank rate 1.18 plus a 1.5% fee. Where is £600 cheaper to exchange?

---

### Answers

**A1.** (1.20 − 1.08) ÷ 1.20 = 0.10 = **10% = 1,000 bps**. (Airport-level
pricing — remember this scale.)

**A2.** (a) +30 bps. (b) +0.3 percentage points. (c) 30/430 ≈ **+7% relative**.
All three describe the same move.

**A3.** Shop A: 4.2% of £600 ≈ **£25.40**. Shop B: 1.5% of £600 = **£9**.
Shop B is much cheaper — despite Shop A's "0% commission" sign. Headlines
are not prices.

---

## Where this idea goes — the ladder

1. **This file:** basis points, the spread, the implicit margin — and the
   reflex of comparing **total cost**, never the headline.
2. **[File 1.4](04_price_volume_mix_and_leakage.md)** does business in these units: the price waterfall's ledges
   are measured in bps, and a leakage audit is a hunt for the bps that went
   missing between the rate board and the till.
3. **[File 4.1](../04_satisfy_the_regulator/01_segments_and_fairness.md)** is the same total-cost comparison with a regulator watching.
   *Fair value* under the Consumer Duty asks exactly the question you asked
   of the two shops in §3 — what did the customer really pay, and was it
   reasonable — but asked separately for every customer group.
4. **[The distributions appendix](../appendix/distributions_for_pricing.md) §4** names the danger underneath the spread: daily rate moves
   have fatter tails than a bell curve, which is why the **hedge** (see the
   glossary, [The glossary](../appendix/glossary.md)) exists — the spread you earn must survive the day the
   market jumps.
5. **The real numbers:** the [master prompt](../../interview/FRES_MASTER_PREP_PROMPT.md)'s Part 1 has the market's
   directional levels (high-street ~4.6–5.2%, online ~2–3% better, airport
   ~10% worse, fintechs under 1%):
   [`../../interview/FRES_MASTER_PREP_PROMPT.md`](../../interview/FRES_MASTER_PREP_PROMPT.md).
