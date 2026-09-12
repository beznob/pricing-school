# 1.4 · Why Did Profit Move? — price, volume, mix, and the leaks

Two skills in this file, and they're the ones finance directors test first:
**explaining** a profit change, and **finding** the money quietly leaking out.

## 1. The most famous number in pricing

Set up a simple business (per £100 of revenue):

| Line | £ |
|---|---|
| Revenue | 100 |
| Variable costs | 60 |
| Fixed costs | 31 |
| **Operating profit** | **9** |

Now improve *one thing at a time* by 1% and watch profit:

| Move | New profit | Profit change |
|---|---|---|
| **Price +1%** (volume unchanged) | 101 − 60 − 31 = 10 | **+11%** |
| Variable cost −1% | 100 − 59.4 − 31 = 9.6 | +6.7% |
| Volume +1% (price flat) | 101 − 60.6 − 31 = 9.4 | +4.4% |
| Fixed cost −1% | 100 − 60 − 30.7 = 9.3 | +3.4% |

**Price is the biggest lever — nearly triple the volume lever.** Why? A price
increase drops *straight through* to profit (no extra cost comes with it),
while extra volume drags its variable costs along.

This ~11% figure is from a famous Harvard Business Review study (Marn &
Rosiello, 1992) of average companies. The exact number depends on the cost
shape, but the ranking — **price > variable cost > volume > fixed cost** —
is nearly universal. Memorise the ranking, not the number.

## 2. Price–volume–mix: explaining "profits are down, why?"

When profit moves, break the move into three causes:

- **Price effect** — we charged different prices.
- **Volume effect** — we sold more or fewer units.
- **Mix effect** — the *blend* of what we sold changed (more cheap stuff,
  less expensive stuff), even if each price and total volume held.

### Worked example

Last year: 100 online sales (margin £20 each) + 100 branch sales (margin £40
each) = **£6,000**.
This year: 140 online + 60 branch, same margins each, same total 200 sales
= 140×20 + 60×40 = **£5,200**.

Prices identical. Total volume identical. Profit down £800. The entire drop
is **mix**: customers shifted toward the lower-margin channel. If you don't
name the mix effect, someone will wrongly blame prices or the sales team.

**Mix is the sneakiest of the three** — it moves on its own (customers
drifting online, holiday destinations shifting) and it's invisible unless
you look for it. [File 4.1](../04_satisfy_the_regulator/01_segments_and_fairness.md) shows mix creating a *fairness* problem too.

## 3. Pocket price and leakage — where the price you set isn't the price you get

The **list price** is what's on the rate board. The **pocket price** is what
actually ends up in your pocket after every little giveaway along the way.
The chain from one to the other is called the **price waterfall** — picture
the price stepping down a series of small ledges:

```
List price (rate board)            500 bps of margin
  − volume-tier discounts           −28   (intentional — that's fine)
  − promo codes                      −6
  − staff & partner special rates    −3
  − rate promised at order,
    market moved before pickup       −6
  − branch staff "just this once"
    discounts                       −14
  = POCKET margin                  ~443 bps ... call it 435 after hedging
```

Each ledge looks tiny. Together they can be worth more than any clever
optimisation project — and **nobody owns them**, because each lives in a
different system (the till, the marketing tool, the website).

**Leakage** = the ledges that aren't supposed to be there (a discount
applied to the wrong order size; unmanaged staff discounts; promo codes
stacking). The classic first assignment for a new pricing manager is a
**leakage audit**: build the waterfall, size each ledge, fix the biggest
easy ones. It beats building models because:

1. The money is real and immediate.
2. Fixing it is governance (rules, till checks), not maths.
3. Clean prices make every *future* analysis more trustworthy.

## 4. One warning: don't claim the market's win as your own

You fix a leak; profit rises 3%. But the market also grew that quarter. How
much of the 3% is *yours*? The honest answer needs a comparison group ([File 2.2](../02_prove_the_change/02_tests_and_experiments.md)). For now, one sentence to remember:

> "We estimate £X of improvement, of which £Y is cleanly attributable to the
> fix; the rest is market." — **Always under-claim.** Finance people trust
> under-claimers with bigger budgets.

## 5. Check yourself

**Q1.** Revenue 100, variable cost 70, fixed cost 25 (profit 5). What does a
1% price rise do to profit, in %?

**Q2.** Last year: 50 premium sales (margin £100) + 50 basic (margin £20).
This year: 30 premium + 70 basic, same margins. Same total sales. What
happened to profit, and what do you call the cause?

**Q3.** Your list margin is 500 bps but the average collected margin is
460 bps. 25 bps of the gap is intentional volume tiers. How big is the
leakage, and what's the first thing you'd ask for?

---

### Answers

**A1.** New profit = 101 − 70 − 25 = 6. Change = 1/5 = **+20%**. (Thin-profit
businesses have *huge* price leverage — even more than the famous 11%.)

**A2.** 50×100+50×20 = £6,000 → 30×100+70×20 = £4,400. Down £1,600 with no
price or volume change: a pure **mix effect** (shift toward the low-margin
product).

**A3.** 500 − 25 intentional = 475 expected; collected 460 → **15 bps of
leakage**. First ask: the transaction-level data from the till and website,
so you can build the waterfall and see *which* ledge the 15 bps hides in.

---

## Where this idea goes — the ladder

1. **This file:** the price > cost > volume > fixed ranking, the
   price–volume–mix decomposition, and the waterfall from list price down to
   pocket price.
2. **[File 2.2](../02_prove_the_change/02_tests_and_experiments.md)** turns §4's warning ("don't claim the market's win") into a
   method: a control group and difference-in-differences separate your fix
   from the market's tailwind. This is why every leakage fix should ship
   with a holdout attached.
3. **[File 4.1](../04_satisfy_the_regulator/01_segments_and_fairness.md)** shows the mix effect doing something more dangerous than
   moving profit: the same customer drift that shifted your channel mix can
   quietly shift *who pays what* — the fairness trap that passes every
   within-channel check.
4. **[File 3.2](../03_defend_the_plan/02_kpis_and_stakeholders.md)** formalises the decomposition for the boardroom: the **revenue
   bridge** (volume + price + mix + competitor effects, against plan) is PVM
   with an AOP attached — and the leakage audit is the classic
   first-90-days move (§5 there).
5. **In code:**
   [`../05_the_panel/N5_pocket_price_waterfall.ipynb`](../05_the_panel/N5_pocket_price_waterfall.ipynb)
   builds this exact waterfall, sizes five leaks, computes the 11% lever on
   a simulated business, and designs the honest before/after test.
