# 05 · Averages, Ranges, and Deciding Without Certainty

Pricing decisions are made on noisy, incomplete numbers. This file teaches
you to read them honestly — and to make good decisions anyway.

## 1. Mean vs median — and when the average lies

- **Mean** (the everyday "average") — add everything up, divide by the count.
- **Median** — line everyone up in order; take the middle one.

Five customers exchange: £200, £300, £400, £500, £8,000.

- Mean = 9,400 ÷ 5 = **£1,880**
- Median = **£400**

One big customer dragged the mean far above what a *typical* customer does.
Money data is almost always shaped like this (many small, a few huge), so:

> **For "what does a typical customer do?", use the median.
> For "how much money in total?", use the mean (×count).**

## 2. Averages hide groups — the single most useful suspicion you can develop

"Average margin is 4.4%" sounds fine. But maybe:

- Online customers (half your volume): 2.7%
- Branch customers (other half): 6.1%

The average was true and useless. Whenever someone shows you an average, ask
the same question: **"averaged over whom?"** — then ask to see it split by
group (channel, region, customer type). File 07 shows this question
uncovering a fairness problem the average completely hid.

## 3. Spread: how wobbly is the number?

Two branches both average £10,000/week:

- Branch A: 9,800 · 10,100 · 10,050 · 9,900 — calm.
- Branch B: 4,000 · 16,500 · 7,000 · 12,500 — wild.

The **standard deviation** measures that wobble — roughly, "how far from the
average is a typical week?" A ≈ £130; B ≈ £4,700. You don't need to compute
it by hand; you need to **ask for it**, because the wobble decides how much
data you need before you can trust a comparison (File 06).

## 4. "The range of likely values" — confidence intervals in plain words

You test a price change and measure **+2% profit**. Is it exactly 2%? Never
— you measured on a sample of noisy weeks. Statisticians attach a **range of
likely values** (the formal name is a *confidence interval*):

> "Our best estimate is **+2%**, and the plausible range is **−0.5% to +4.5%**."

Two honest readings of that range:

1. The effect is *probably* positive (most of the range is above zero).
2. We're not sure — it *could* be slightly negative.

### The classic mistake — burn this into memory

The range includes zero, so someone says: **"not statistically significant —
it didn't work."** That is wrong. The right sentence is:

> **"Our measurement is too blurry to be sure — which is a statement about
> the camera, not about the thing we photographed."**

A blurry photo of a cat is not evidence there's no cat. If the true effect
really were +2%, a small test would *often* produce a range touching zero.
The width of the range tells you about your **test's power** (its ability to
see effects — File 06), not about the world.

## 5. Making the decision anyway: expected value

You can decide well *without* certainty. The tool is **expected value (EV)**:
multiply each outcome by its probability, add them up.

A £1 raffle ticket: 1-in-100 chance of £50.
EV = (1/100 × £50) + (99/100 × £0) = **£0.50**. You paid £1 for 50p of
expected win — bad bet, even though you *might* win.

### Now the pricing version

Your test said +2%, range −0.5% to +4.5%. Analysis says there's a **90%
chance the effect is positive**, and on your business +2% ≈ £1m/year.

- Roll it out: if positive (90%) you gain ≈ £1m/yr; if negative (10%),
  monitoring catches it in ~8 weeks and you roll back, losing maybe £150k.
- EV ≈ 0.9 × (+1,000k) + 0.1 × (−150k) = **+£885k**. Roll out.

Notice what made this decision easy: not certainty, but a **positive EV**
plus a **bounded, reversible downside** (you can undo it, and you'll notice
quickly). That combination — *expected value, capped loss, reversibility* —
is how senior people decide under uncertainty. Present results that way and
you will sound ten years more experienced than "p < 0.05".

## 6. How to talk about uncertainty to busy people

- ✅ "Best estimate +2%; plausible range slightly-negative to strongly-positive."
- ✅ "About a 90% chance this makes money; if we're wrong we lose at most ~£150k."
- ✅ "The wide range means we need a longer test, not that the effect is zero."
- ❌ "The p-value was 0.11 so we failed to reject the null hypothesis." (True,
  useless, and the room stopped listening at "p-value".)

## 7. Check yourself

**Q1.** Incomes at a branch's customers: mostly £20k–£40k, plus two
millionaires. Which is higher, mean or median? Which describes the typical
customer?

**Q2.** A test result: +3%, plausible range −1% to +7%. Your boss says "it
didn't work then". Give the two-sentence correct reply.

**Q3.** A move has a 70% chance of +£500k and a 30% chance of −£400k, and it
can't be reversed. A second move has a 60% chance of +£300k and 40% chance
of −£50k, reversible in a month. EV of each? Which would you rather ship?

---

### Answers

**A1.** Mean is higher (the millionaires drag it up); **median** describes
the typical customer.

**A2.** "Best estimate is +3% — the test is too small to pin it down, which
tells us about the test, not the effect. Given most of the range is
positive, I'd either roll out with monitoring or extend the test, not bin it."

**A3.** EV₁ = 0.7×500 − 0.3×400 = **+£230k**. EV₂ = 0.6×300 − 0.4×50 =
**+£160k**. EV₁ is bigger, but it's irreversible with a big possible loss;
EV₂ is nearly as good with a small, undoable downside. Most experienced
operators ship **move 2** — EV is the start of the argument, not the end.
Reversibility is worth real money.

---

## Where this idea goes — the ladder

1. **This file:** mean vs median, the wobble, the range of likely values,
   and deciding by expected value with a bounded, reversible downside.
2. **File 06** turns "the range is wide" from an excuse into a design
   problem: the width is set by the test's **power**, so you compute the
   minimum detectable effect *before* testing instead of apologising after.
3. **File 11** makes §1's suspicion precise. "The mean lies about money"
   has a reason: money is **log-normal** (many small, a few huge), and
   mean ≫ median is your heavy-tail detector. The wobble gets a shape too —
   and the shape, not the average, decides how big a cushion you need.
4. **Files 12–13** apply the same honesty upward: models get graded
   **out-of-time** rather than on flattering shuffles (12 §6), and decisions
   get sold to committees in exactly this file's language — "90% chance
   positive, downside capped at £150k, reversible in 8 weeks" (13 §§3–4).
5. **In code:**
   [`../fres_prep/N4_uncertainty_to_decision.ipynb`](../fres_prep/N4_uncertainty_to_decision.ipynb)
   runs this entire file as a live calculation — including proving that a
   true +2% effect "fails" a small test 65% of the time, and pricing the
   option of extending the test vs rolling out now.
