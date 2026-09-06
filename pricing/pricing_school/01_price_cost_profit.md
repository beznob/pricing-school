# 01 · Price, Cost, Profit — the four numbers everything else is built on

## 1. The basic chain

Imagine a small kiosk that sells euros to holidaymakers.

- **Price** — what the customer pays you.
- **Revenue** — price × how many you sell. All the money coming in.
- **Cost** — the money going out.
- **Profit** — what's left: **Profit = Revenue − Cost**.

That's it. Everything in pricing is about making that last number bigger
*without breaking something else* (customers leaving, regulators frowning,
competitors retaliating).

## 2. Two kinds of cost — this distinction matters everywhere

- **Variable cost** — a cost you pay *per sale*. Sell more, pay more.
  (The euros themselves, card fees, the plastic wallet you hand over.)
- **Fixed cost** — a cost you pay *no matter what*. Sell nothing, pay it
  anyway. (Rent, staff salaries, the till.)

**Why it matters:** when you sell one more unit, only the *variable* cost
goes up. So the profit from one extra sale is:

> **Contribution = Price − Variable cost** (per unit)

"Contribution" because each sale *contributes* that much toward covering the
fixed costs — and once those are covered, toward profit.

### Worked example

Your kiosk sells €1,000 bundles.

| Item | Amount |
|---|---|
| Price to customer | £900 |
| Variable cost (buying the euros + handling) | £860 |
| **Contribution per sale** | **£40** |
| Fixed costs (rent + staff) | £2,000 per week |

Each sale contributes £40. To cover £2,000 of fixed costs you need:

> **Break-even = Fixed costs ÷ Contribution per unit = 2,000 ÷ 40 = 50 sales/week**

Sale number 51 onward is profit. This is the **break-even point** — the most
useful single number when someone proposes anything ("hire another person",
"cut the price"): *how many extra sales does this need to pay for itself?*

## 3. Margin vs markup — two words people constantly mix up

Both describe the gap between price and cost. They divide by different things.

- **Margin** = (Price − Cost) ÷ **Price** → "what share of the price is profit?"
- **Markup** = (Price − Cost) ÷ **Cost** → "how much did I add on top of cost?"

Same kiosk: price £900, cost £860, gap £40.

- Margin = 40 ÷ 900 = **4.4%** — of every pound the customer pays, 4.4p is yours.
- Markup = 40 ÷ 860 = **4.7%** — you added 4.7% on top of what it cost you.

They're close here because the gap is small. On big gaps they differ a lot:
price £100, cost £50 → margin 50%, markup 100%. **In this industry people
almost always mean margin**, and they usually quote it as a share of the
price (or of the amount exchanged).

## 4. Why small margins make pricing a high-wire act

Notice the kiosk's shape: £900 comes in, £860 goes straight out, £40 is
yours before rent. The profit is a **small number squeezed between two big
ones**. That has a huge consequence:

> A tiny change in price causes a **big** change in profit.

Drop the price just 1% (£9) and your £40 contribution becomes £31 — a **22%
drop in contribution** from a 1% price move. This "small margin, big
sensitivity" effect is the reason pricing gets so much attention in
businesses like currency exchange, insurance, and groceries. File 04 turns
this into the most famous number in pricing.

## 5. Check yourself

**Q1.** A branch sells travel cards at £5 each. The card costs £2 to buy and
load. Fixed costs are £600/week. How many cards to break even?

**Q2.** Price £80, cost £60. What is the margin? What is the markup?

**Q3.** Your contribution per sale is £40 on a £900 price. A colleague says
"let's cut the price 2% — it's only 2%". How much of your contribution per
sale does that 2% eat?

---

### Answers

**A1.** Contribution = 5 − 2 = £3. Break-even = 600 ÷ 3 = **200 cards/week**.

**A2.** Gap = £20. Margin = 20/80 = **25%**. Markup = 20/60 = **33%**.

**A3.** 2% of £900 = £18. Contribution falls £40 → £22 — the "only 2%" price
cut ate **45% of your profit per sale**. (This is why pricing managers get
twitchy about casual discounts.)

---

## Where this idea goes — the ladder

Nothing in this file gets replaced later — it gets promoted. Rung by rung:

1. **This file:** contribution and break-even — the profit in *one more
   sale*, and how many extra sales pay for a decision.
2. **File 04** runs the same arithmetic at company scale. Because profit is
   a small number squeezed between two big ones (§4), a 1% price move swings
   profit ~11% — the most famous number in pricing is just this file's
   kiosk, multiplied.
3. **File 03** turns margin from a *result* you calculate into a *decision*
   you make: the right margin is set by how customers react (elasticity),
   not by cost-plus habit. Until you know the elasticity, this file cannot
   tell you whether £40 of contribution is the best you could be earning.
4. **File 13** is the same numbers spoken upward: the CFO's "are we on
   plan?" is answered with a **revenue bridge** — break-even thinking with a
   committee in the room.
5. **In code:**
   [`../fast_transaction_services/distribution_economics.py`](../fast_transaction_services/distribution_economics.py)
   computes the version with no shortcuts — margin per channel after
   commissions and cost-to-serve, which decides where a sale is worth making
   at all (case study §3).
