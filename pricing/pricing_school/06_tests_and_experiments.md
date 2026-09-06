# 06 · Testing a Price Change Properly

You changed a price. Sales moved. **Was it you, or was it the weather?**
This file is about answering that honestly.

## 1. Why before/after comparisons lie

You cut the margin in March; April sales are up 6%. Success? Maybe. But:

- Easter fell in April (seasonality),
- the pound wobbled (market),
- a competitor closed two branches (competition),
- and the weather was nice.

All four moved April sales *regardless of your price*. A **before/after
comparison** mixes your effect with everything else that happened. It is the
most common analysis in business and the least trustworthy.

## 2. The fix: a control group

Run the change in *some* branches (**treatment group**) and not in others
(**control group**) **over the same weeks**. Easter, the pound, the weather
— they hit both groups equally. Whatever *differs between the groups* is
your effect.

> **Effect ≈ (change in treated branches) − (change in control branches)**

That subtraction has a formal name — **difference-in-differences** ("DiD") —
because you take each group's before→after difference, then the difference
between those. Worked example:

|  | Before | After | Change |
|---|---|---|---|
| Treated branches | £100k/wk | £108k | +8% |
| Control branches | £100k/wk | £105k | +5% |

Naive read: "+8%!" Honest read: the *market* gave everyone +5%; your change
added **+3%**. (This is the "don't claim the market's win" rule from File 04,
now with a method behind it.)

## 3. Why you must randomise (not hand-pick)

If you *choose* your best branches for the test, the comparison is rigged —
your best branches would have outgrown the others anyway. Assigning by
**random draw** is what makes the two groups genuinely comparable: same mix
of big/small, city/rural, lucky/unlucky. Randomness isn't sloppiness; it's
the whole guarantee.

A held-back control group is often called a **holdout** — as in "we rolled
it out to 80% and held out 20% to keep measuring".

## 4. Can your test even see the effect? (power)

Small effects need big tests. If branches naturally wobble ±5% a week and
your price change causes +0.5%, a 20-branch test will *never* see it —
the signal drowns in the wobble.

The honest question to ask **before** testing:

> **"What is the smallest effect this test could reliably detect?"**

That number is called the **minimum detectable effect (MDE)**. If your MDE
is 2% and you expect a 0.5% effect, don't run the test — make it bigger,
longer, or accept you'll get a *range*, not a verdict (File 05). Asking for
the MDE up front is one of the fastest ways to sound senior — and it
prevents the doomed test whose "no significant result" gets misread as
"no effect".

Two cheap ways to shrink the MDE:

1. **Run longer / more branches** — more data, less wobble in the average.
2. **Use last month's data as a baseline** — compare each branch to *its own
   normal level* rather than raw sales. Calm branches stay calm, so the
   wobble shrinks. (The technical name is CUPED; the idea is just
   "measure the change from each branch's own baseline".)

## 5. The neighbour problem (spillover)

Branch A tests a better rate. Customers who *would have* gone to branch B
next door walk to A instead. Now:

- A's sales are up (partly stolen, not created),
- B — a *control* branch — is down (contaminated).

Your comparison **overstates** the true gain, because part of A's win came
out of B's pocket. The network as a whole gained less than the test claims.
This is called **spillover** or **interference** — the groups leaked into
each other.

**Fixes, in plain words:**
- Randomise by **area, not branch** (whole towns get the change or don't),
  so the walking-next-door happens *inside* one group and cancels out.
- Leave a **buffer**: ignore branches sitting on the border between a
  treated area and a control area.
- If the change is visible online to everyone (comparison sites), accept the
  control group is partly treated and report your result as a **minimum** —
  "at least +X%".

## 6. A test checklist you can reuse forever

1. What exactly changes, where, for how long?
2. Who is the **control group**, and was assignment **random**?
3. What's the **MDE** — can this test see the effect we expect?
4. Any way the groups can **leak** into each other? (neighbours, online)
5. What decision will we take if the result is positive / negative /
   unclear? (Decide *before* seeing the data — it keeps everyone honest.)
6. Report: best estimate, range, and what the market did to the control.

## 7. Check yourself

**Q1.** Sales rose 10% after a price cut. Controls rose 7%. What's your
effect, and what explains the 7%?

**Q2.** A colleague proposes testing a 0.3% expected effect on 10 branches
for 2 weeks. Branch weekly wobble is ±4%. What do you ask first, and what's
your instinct?

**Q3.** In a city-centre test, treated shops boomed and nearby control shops
dipped. Is your measured effect too high or too low — and why?

---

### Answers

**A1.** Your effect ≈ **+3 points**. The other 7 points are market/season —
they happened to the controls too.

**A2.** Ask for the **MDE**. Instinct: with ±4% wobble, 10 branches × 2 weeks
can't reliably see 0.3% — the test is doomed to a shrug. Bigger, longer, or
don't bother.

**A3.** **Too high.** Part of the treated boom was customers stolen from the
controls, and the dipping controls made the gap look even bigger. Randomise
by area and re-test.

---

## Where this idea goes — the ladder

1. **This file:** control groups, difference-in-differences, randomisation,
   MDE, and spillover.
2. **Look back before looking up — File 03 §6:** this file *is* the fix for
   endogeneity. An experiment creates price variation that owes nothing to
   demand, and that is what makes elasticity measurable at all. The deep
   reason pricing teams run tests is not to be scientific — it's that their
   historical data is poisoned by their own pricing habits.
3. **File 08 §5** handles the case you can't randomise (you don't control
   the competitor): approximate the control group by hand with **matched
   twins**. The glossary's *synthetic control* is the formal version of the
   same instinct.
4. **File 12 §8** makes the experiment permanent: once a model sets prices,
   its own logs stop containing clean variation — so production systems keep
   a small randomised **exploration stream** running forever. The test never
   really ends.
5. **In code:**
   [`../fres_prep/N1_geo_experiment_design.ipynb`](../fres_prep/N1_geo_experiment_design.ipynb)
   builds all of this — the neighbour problem roughly *doubling* a measured
   effect, area-level randomisation fixing it, MDE tables, and the baseline
   trick (CUPED) cutting the MDE in half.
