# 4.1 · Different Prices for Different People — and the fairness line

## 1. Segments: customers are not one blob

A **segment** is a group of customers who behave similarly: how much they
buy, how price-sensitive they are ([File 1.3](../01_set_the_rate/03_elasticity.md)), which channel they use.
Examples in travel money:

- **Digital-first** — compares rates online in seconds. Very price-sensitive.
- **Branch walk-up** — values a person, cash in hand, today. Less sensitive.
- **Airport last-minute** — no alternatives left. Barely sensitive at all.

Because elasticity differs by segment, the *profit-maximising* price differs
by segment ([File 1.3](../01_set_the_rate/03_elasticity.md)'s markup rule). Charging everyone the same price
overcharges some and undercharges others.

## 2. Differential pricing: normal, useful… and watched

Charging different prices to different groups is called **differential
pricing** (or price discrimination — the technical term, not an insult).
Much of it is ordinary and accepted:

- Volume tiers (big orders get better rates) ✅
- Channel differences (online cheaper than in-person — it costs less to serve) ✅
- Student/senior discounts ✅

And some of it gets companies into trouble. In the UK the regulator (the
**FCA** — Financial Conduct Authority) watches financial products under a
rule called the **Consumer Duty**. The part that matters for pricing is
**fair value**:

> **The total price a customer pays must be reasonable compared to the
> benefit they get — and that must be true for every group of customers,
> especially vulnerable ones. Not just on average.**

Key vocabulary:
- **Vulnerable customer** — someone less able to protect their own
  interests: poor health, low financial confidence, low digital skills, a
  recent life shock. Not an insult — a category the rules require you to check.
- **Cross-subsidy** — one group's high prices funding another group's low
  ones. Allowed! But you must check who's doing the subsidising.

## 3. The trap: the check that passes while the harm is real

Here's the subtle bit — the single most useful fairness insight in this track. Suppose your price sheet is purely channel-based:

- Online: 2.7% · Branch: 5.2% · Airport: 10.5%

Within each channel, vulnerable and non-vulnerable customers pay **exactly
the same**. A fairness check *within channels* passes with flying colours.

But vulnerable customers are, on average, **less digital** — so more of them
buy at the branch and the airport:

| | Online (2.7%) | Branch (5.2%) | Average paid |
|---|---|---|---|
| Typical customers | 60% | 40% | **3.7%** |
| Vulnerable customers | 15% | 85% | **4.8%** |

Same price sheet. No one decided to charge vulnerable people more. Yet they
pay over a point more, *because of where they buy*. This is a **mix effect**
([File 1.4](../01_set_the_rate/04_price_volume_mix_and_leakage.md)) creating a fairness problem — and it is invisible in averages and
in within-channel checks. The regulator's own words: group averages "could
disguise… pockets of poor value."

**What a good pricing manager does about it** (not "make all prices equal"):
- Check the **distribution** of what each group actually pays, not the average.
- **Signpost** the cheaper option (help branch customers order online, or
  offer the online rate for assisted orders in-branch).
- **Cap** the gap between channels if the vulnerable-mix evidence demands it.
- Write it down — the Duty expects documented evidence, including what your
  data *can't* see.

## 4. One more watch-item: the captive customer

Fair value gets hardest where the customer **can't walk away**: the airport,
a Friday-evening stockout, a locked-in renewal. High prices to captive
customers may still be defensible (real costs, real convenience) — but
"defensible" means you can show the maths of costs and benefits, not just
"the market bears it". If the only justification is *they had no choice*,
you're on the wrong side of the line.

## 5. Check yourself

**Q1.** Your average customer pays 4.0%. Is that enough to say pricing is
fair? What two follow-up views do you ask for?

**Q2.** Online costs you £2 per order to serve; branch costs £8. Branch
price is 2.5 points higher. A colleague says "so the differential is fully
justified by cost". What's the missing check?

**Q3.** A rate promise: customers who order online can collect in-branch at
the online rate. Which fairness problem from this file does that help, and
why might branch staff dislike it?

---

### Answers

**A1.** No — averages hide groups. Ask for (1) the **split by segment and
channel**, and (2) the **distribution** of what vulnerable customers pay vs
everyone else.

**A2.** Cost explains *part* of the gap; the missing check is **who pays
it**: if the branch premium lands mostly on vulnerable, less-digital
customers, cost alone won't carry the fair-value argument — you need
mitigation (signposting, assisted online rate) or a smaller gap.

**A3.** It narrows the vulnerable-mix gap (branch-reliant customers can get
the cheap rate). Branch staff may fear it undercuts their till — the fix is
to *credit collections to the branch's numbers*, so the branch wins when
customers collect there.

---

## Where this idea goes — the ladder

This file is where three earlier ideas collide; then it feeds two later ones.

1. **Built from three rungs below:** segment elasticities ([File 1.3](../01_set_the_rate/03_elasticity.md) §4)
   explain *why* prices differ by group; the mix effect ([File 1.4](../01_set_the_rate/04_price_volume_mix_and_leakage.md) §2)
   explains how a fair-looking price sheet can land unfairly; and "averages
   hide groups" ([File 2.1](../02_prove_the_change/01_averages_and_uncertainty.md) §2) is the habit that catches it. The §3 trap is
   literally [File 1.4](../01_set_the_rate/04_price_volume_mix_and_leakage.md)'s mix effect caught doing something the regulator cares
   about.
2. **[The workflow appendix](../appendix/data_science_workflow.md) §5** wires the fairness line into the machinery: price caps and
   maximum step sizes, no protected characteristics as features, human
   review — guardrails are this file translated into model constraints.
3. **[File 3.2](../03_defend_the_plan/02_kpis_and_stakeholders.md)** makes it a standing duty rather than a one-off analysis:
   **fair-value MI** is a KPI pack the committee sees every cycle, and the
   branch-credit fix for signposting (Q3 above) reappears there as
   stakeholder management.
4. **In code:**
   [`../05_the_panel/N6_channel_differential_fair_value.ipynb`](../05_the_panel/N6_channel_differential_fair_value.ipynb)
   simulates exactly §3's trap — the within-channel check passing while the
   mix hides a +1.3-point premium on vulnerable customers — and
   [`../engine/fair_value.py`](../engine/fair_value.py)
   is the production version of the check.
