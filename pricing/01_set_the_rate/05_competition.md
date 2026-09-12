# 1.5 · Competition — price wars and how not to start one

## 1. The price war in one table

Two currency shops face each other across a high street. Each can **hold**
its price or **cut**. Yearly profit for (You, Rival):

| | Rival holds | Rival cuts |
|---|---|---|
| **You hold** | (10, 10) | (6, 12) |
| **You cut** | (12, 6) | (7, 7) |

Read it slowly:

- If you both hold: comfortable (10, 10).
- If you cut and they don't: you win big (12) — *for a while*.
- But they see your cut and cut back. You both end at **(7, 7)** — everyone
  poorer, market shares roughly where they started.

This trap has a name — the **prisoner's dilemma**: each side's "smart"
individual move (cut) makes both sides worse off. Price wars are this table
playing out in slow motion. The pricing manager's job is to *not be the one
who flips the table to (7,7)* — and not to overreact when someone else
seems to.

## 2. The first question, always: temporary or permanent?

A competitor drops their rates. Before doing anything, diagnose:

- **Promotional** (temporary): a launch splash, a funded land-grab, a
  seasonal push. It ends when the budget does. Usual best answer: **hold**,
  keep your regulars happy, let their money burn.
- **Structural** (permanent): a genuinely lower-cost rival (a fintech app, a
  kiosk with no rent). It won't end. Ignoring it means slowly bleeding share.

How to tell: watch for 4–6 weeks; check whether their price is *below their
own cost to provide* (nobody sustains that); look at signals like hiring and
new sites. **Don't respond to noise.**

## 3. If you must respond: the ladder

Cheapest rung first.

1. **Non-price moves** — be *better*, not just cheaper: currency always in
   stock, faster service, buy back leftovers at a decent rate, easier
   click-and-collect. In a convenience business these defend share without
   giving up a penny of margin.
2. **Targeted price moves** — cut only where it pays: the specific branches
   under attack, and among those, only the ones where customers are
   price-sensitive enough that the volume you keep covers the margin you
   give ([File 1.1](01_price_cost_and_profit.md) and [file 1.3](03_elasticity.md): contribution and elasticity decide, branch by branch).
3. **Fenced discounts** — cuts hidden behind a condition: bigger-order
   tiers, online-order-only rates, buyback deals. A **fence** is any hoop
   that lets price-sensitive customers get the deal without repricing
   everyone. Bonus: fenced cuts are hard for a rival's pricing desk to read,
   which slows the war-escalation loop.
4. **Across-the-board match** — last resort, and usually wrong. See below.

## 4. The cautionary tale: "Meet or Beat"

In the 1990s Delta Air Lines promised to *meet or beat* competitor fares.
Sounds strong — it means **your competitors now set your prices**. Any rival
with lower costs (or higher desperation) could drag Delta's fares down at
will, and did. The industry-wide fare war that followed cost enormous sums.

The lesson, one line, worth quoting in any meeting where "let's just match
them" comes up:

> **Matching everyone hands your pricing pen to the competitor.**

## 5. Measure the punch you actually took

You can't run a controlled experiment on a competitor opening stores (you
don't control them). The honest measurement: for each affected branch, find
a **twin** — an unaffected branch of similar size and type — and compare
their paths (this is the control-group logic of [File 2.2](../02_prove_the_change/02_tests_and_experiments.md), built by matching
instead of randomising). Typical finding: the naive read *understates* the
hit, because the overall market was growing while the affected branches were
being bitten.

## 6. Comparison sites — the always-on price war

Rate-comparison websites show every provider's price, live, ranked. Two
consequences:

- Your **rank** matters as much as your rate (customers click the top few).
- Everyone can see everyone — so cuts get matched in hours, which makes the
  prisoner's dilemma tighter. One caution from the FX world: after a sudden
  market move, rivals' displayed rates may be **stale** (not yet updated).
  Never chase a rate that will vanish by lunchtime.

## 7. Check yourself

**Q1.** In the table of section 1, you're at (10, 10). Your board wants the
12. What do you tell them?

**Q2.** A venture-funded kiosk opens by your top 50 branches at rates below
its own cost. Promo or structural — and what's your first move?

**Q3.** You decide some price response is needed at 20 of the 50 branches.
Why those 20 and not all 50? (Two files from this track answer it.)

---

### Answers

**A1.** "The 12 lasts one round. They cut back and we live at (7,7)
permanently. The 3 we'd gain for a quarter costs us 3 a year forever —
we hold, and we make it easy for them to hold too."

**A2.** Below-own-cost pricing is unsustainable → likely **promotional**
(until proven otherwise). First move: **non-price defence** (stock,
service, buyback) plus watching their behaviour for 4–6 weeks — not a cut.

**A3.** Because the cut only pays where **contribution** given up is smaller
than the volume defended — which depends on each branch's **elasticity**
([File 1.3](03_elasticity.md)) and margin ([File 1.1](01_price_cost_and_profit.md)). At inelastic branches, cutting is pure
giveaway; the non-price bundle is cheaper.

---

## Where this idea goes — the ladder

1. **This file:** the payoff table, the promo-vs-structural diagnosis, and
   the response ladder from non-price moves to (almost never) matching.
2. **[File 1.1](01_price_cost_and_profit.md) and [file 1.3](03_elasticity.md) decide *where* to fight:** a defensive cut only pays at
   branches where the contribution given up ([File 1.1](01_price_cost_and_profit.md)) is smaller than the
   volume defended — which each branch's elasticity ([File 1.3](03_elasticity.md)) decides. The
   response ladder's rung 2 is those two files doing local arithmetic.
3. **[File 2.2](../02_prove_the_change/02_tests_and_experiments.md)'s logic, without the randomiser:** you can't A/B-test a
   competitor opening stores, so you build the control group by hand —
   **matched twins** (§5). The glossary's *synthetic control* is the formal
   tool: a weighted blend of unaffected branches standing in for the world
   that didn't get hit.
4. **[The workflow appendix](../appendix/data_science_workflow.md) §2** is the always-on version of the war: on comparison sites
   your *rank* becomes one of the strongest features in the conversion
   model. Competition stops being an event and becomes a variable.
5. **In code:**
   [`../05_the_panel/N8_competitor_response_game.ipynb`](../05_the_panel/N8_competitor_response_game.ipynb)
   prices this entire file: the payoff table with real numbers, promo vs
   structural verdicts, the branch-by-branch defend/don't-defend rule, and
   the matched-twin measurement.
