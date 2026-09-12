# The Shapes of Randomness — which distribution for what

*(This file distils the repo's insurance-maths deep dive (now parked in
[`../_archive/insurance_project/probability_distributions_pricing.md`](../_archive/insurance_project/probability_distributions_pricing.md))
into the six shapes a pricing person actually uses. Skip the formulas on a first read; learn the **shapes and the
"use it when" rules**.)*

## 0. The bridge in — you already know why this file matters

The foundation files kept telling you that numbers lie in particular ways. This file gives
those ways names. If you remember the foundation on the left, the deep
version is one step away:

| You learned (foundations) | This file makes it precise |
|---|---|
| The mean lies about money — one whale drags it ([File 2.1](../02_prove_the_change/01_averages_and_uncertainty.md) §1) | Money is **log-normal** (shape ②); mean ≫ median is your tail detector |
| The wobble decides how much data you need ([File 2.1](../02_prove_the_change/01_averages_and_uncertainty.md) §3) | Every shape carries its own wobble — and clumpy counts (④) wobble far more than Poisson admits |
| Counting customers arriving ([File 2.4](../02_prove_the_change/04_forecasting_and_stockouts.md) §1) | Counts are **Poisson** (③) — or negative binomial (④) once real life clusters them |
| A sell-out day is a floor, not a measurement ([File 2.4](../02_prove_the_change/04_forecasting_and_stockouts.md) §2) | Censoring = the top of a distribution cut off; fit shapes that respect the cut |
| Profit is squeezed between two big numbers ([File 1.1](../01_set_the_rate/01_price_cost_and_profit.md) §4) | The squeeze breaks in the **tail** (⑥) — which is why you price the tail, not the average |

Nothing here replaces the plain-words versions; it upgrades them from
suspicions into checks you can run on data.

## 1. What a distribution is, in one paragraph

Random things still have *shapes*. Roll a die a thousand times and the
outcomes spread evenly; measure a thousand people's heights and they pile up
in the middle. A **distribution** is the name for that shape. Choosing the
right shape for your data matters because the shape decides how often
**extreme** things happen — and in pricing, the extremes (the £12,000 order,
the catastrophic claim, the wild Friday) are where the money and the risk live.

## 2. The six shapes, plain words first

### ① Normal (the bell curve) — "many small ± nudges"
Symmetric hill around the average. Shows up when a result is the **sum** of
many small independent pushes (measurement noise, daily rate wiggles).
- **Use it when:** modelling noise/errors; things that can go up or down
  symmetrically.
- **Don't use it for:** money amounts. Money can't go below zero and always
  has a long right tail — the normal gives both, wrongly.

### ② Log-normal — "many small × multiplications"
Take a normal, then exponentiate: you get a pile squeezed against zero with
a **long right tail**. Shows up when a result is the **product** of many
factors (income × habit × trip length ⇒ order size).
- **Use it when:** order values, transaction sizes, incomes, claim amounts,
  house prices. **This is the default shape of money.** Every simulator in
  this repo draws order sizes and branch sizes from it.
- **Tell-tale:** mean well above median ([File 2.1](../02_prove_the_change/01_averages_and_uncertainty.md)'s whale effect).

### ③ Poisson — "counting rare arrivals"
The counting distribution: how many customers walk in today, how many
claims this month? One number describes it: the average rate λ ("lambda").
Its signature: **mean = variance**.
- **Use it when:** counting independent events over time.
- **Worked feel:** λ = 2.5 claims/year ⇒ P(no claims) ≈ 8%, P(one) ≈ 21%,
  P(two) ≈ 26%.

### ④ Negative binomial — "counting, but clumpy"
Real counts are usually *messier* than Poisson: some customers/branches are
consistently claim-prone, so events **cluster** and the variance exceeds the
mean (called **overdispersion**). The negative binomial is "Poisson with
personality differences mixed in".
- **Use it when:** your counts show variance > mean. (Check! It's one line
  of code, and it's the difference between the right and wrong model.)

### ⑤ Gamma — "positive, skewed, moderately tailed"
The workhorse for **cost amounts**: strictly positive, right-skewed,
flexible. Repair bills, medical costs, claim severities.
- **Use it when:** positive amounts with a moderate tail. It's the default
  *severity* family in insurance GLMs ([The workflow appendix](data_science_workflow.md)).

### ⑥ Pareto — "the monster tail"
The 80/20 distribution: most outcomes small, a few *enormous* — and the
enormous ones dominate the total. Catastrophes, cyber losses, reinsurance.
- **Use it when:** the tail is the whole point. Warning: for heavy versions
  the average is barely meaningful — one more observation can move it a lot.
- **Pricing lesson:** if losses are Pareto-ish, "average cost" is a
  dangerous number; you price the tail (and cap it — see [The workflow appendix](data_science_workflow.md) on capping).

## 3. The one formula worth memorising: frequency × severity

Insurance (and any claims-like cost) splits total cost into **how often**
(frequency — a counting shape, ③/④) and **how big when it happens**
(severity — a money shape, ⑤/②/⑥). Total cost = the sum of a random number
of random amounts, and its average is beautifully simple:

> **Expected total = (expected count) × (expected size)**
> E[S] = E[N] × E[X]

**Worked example:** a travel-card portfolio expects **0.8 disputes** per
1,000 cards per month (frequency), and a dispute costs **£150** on average
(severity). Expected dispute cost = 0.8 × £150 = **£120 per 1,000 cards per
month**. Price that into the card fee, plus a cushion for the spread.

The cushion is why the *shapes* matter, not just the averages: the variance
of the total depends on both the count's wobble and the size's wobble — a
clumpy frequency (④) or heavy severity (⑥) needs a much bigger cushion for
the same average.

## 4. Mapping the shapes onto travel money

| Thing in the business | Shape | Why |
|---|---|---|
| Order sizes (£ per customer) | Log-normal | many small, a few huge — money |
| Customers per branch per day | Poisson / neg-binomial | counting arrivals; clumpy on event days |
| Branch sizes across the estate | Log-normal | few giant branches, many small |
| Daily FX rate moves | Normal-ish, **but fatter-tailed** | sums of nudges — until a shock day |
| Card disputes / fraud events | Frequency × severity | count × cost |
| A customer converts or not | Bernoulli (a coin with probability p) | the atom of conversion modelling ([The workflow appendix](data_science_workflow.md)) |

The FX-rate caveat matters: real market moves have **fatter tails than
normal** — the "once-in-a-decade" 5% overnight drop happens far more often
than a bell curve predicts. That is precisely why hedging exists (see
**hedge** in the glossary, [The glossary](glossary.md); the runbook notebook N11 opens with the
hedge book).

## 5. How to choose a shape, honestly

1. **Plot the data first.** A histogram tells you 80% of the answer:
   symmetric → normal-ish; squeezed-left long-right → log-normal/gamma;
   counts → Poisson family.
2. **Check mean vs variance** for counts (variance ≫ mean ⇒ negative
   binomial), **mean vs median** for money (mean ≫ median ⇒ heavy tail).
3. **Fit two or three candidates and compare** — standard tools score each
   fit (the score you'll hear named is **AIC**: lower = better fit, with a
   penalty for complexity). Don't agonise; do compare.
4. **Care most about the tail.** Two shapes can match in the middle and
   disagree 10× in the tail — and the tail is what you're pricing. A
   goodness-of-fit test that weights the tail (Anderson–Darling) beats one
   that doesn't (Kolmogorov–Smirnov) for pricing work.
5. **Then stress it:** "if the tail is twice as heavy as my fit says, do I
   still make money?" If no — cap the exposure, don't sharpen the estimate.

## 6. Check yourself

**Q1.** Branch daily order counts: mean 40, variance 260. Poisson or
negative binomial, and why?

**Q2.** Order values: median £400, mean £650. What shape, and which of
mean/median do you use to describe "a typical order"?

**Q3.** Card-loss events: 1.2 per 1,000 cards/month, average cost £90.
Expected cost per 1,000 cards per month? And name one reason the *cushion*
above that number should be bigger than a normal-shaped world suggests.

---

### Answers

**A1.** Variance (260) ≫ mean (40) — **overdispersed**, so **negative
binomial**. A Poisson would say variance ≈ 40 and badly understate busy-day
risk.

**A2.** Mean ≫ median ⇒ right-skewed money ⇒ **log-normal-ish**. Typical
order = the **median** (£400); the mean is dragged by whales.

**A3.** 1.2 × £90 = **£108**. The cushion must respect the shapes: if
frequency clusters (fraud waves → negative binomial) or severity is
heavy-tailed (one £5,000 event), the total wobbles far more than a
bell-curve world — same average, much worse bad months.

---

**When you're ready for more:** the single deep-dive file is
[`../_archive/insurance_project/probability_distributions_pricing.md`](../_archive/insurance_project/probability_distributions_pricing.md)
(all formulas, goodness-of-fit, extreme-value theory, Tweedie/Beta/Weibull,
tail-risk measures, credibility). Every simulator in
[the panel notebooks](../05_the_panel/README.md) uses these shapes — now you'll
recognise them.
