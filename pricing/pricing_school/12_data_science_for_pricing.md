# 12 · Data Science for Pricing — the technical workflow, end to end

*(This file distils the repo's data-science interview material — the Hastings
workflow notebooks and the former interview notes, now consolidated here and in
`workspace/notes/` — into one workflow. It's the "technical track" of this school: everything a
pricing manager must **understand and challenge**, even if analysts run it.)*

## The workflow at a glance

```
1 Data & EDA → 2 Conversion model → 3 Elasticity → 4 Optimise price
                                                        ↓
        7 Monitor in production ← 6 Validate honestly ← 5 Guardrails
```

Each step below: what it is, the one thing that goes wrong, and the question
you ask to catch it.

## 0. The bridge in — every step is a foundation idea, promoted

Nothing in this workflow is new. Each step is a Part 1 idea wearing
production clothes — keep this table open as you read, and if a step feels
abstract, drop down to its foundation file:

| Step here | The simple idea it grows from |
|---|---|
| 1 · EDA | File 05's "averaged over whom?" + File 11's shapes: look before you model |
| 2 · Conversion model | File 03's elasticity, measured per quote — the log-price coefficient **is** the elasticity |
| 3 · Expected profit | File 01's contribution × File 05's expected value |
| 4 · GLMs | File 11's shapes plugged into a regression |
| 5 · Guardrails | File 07's fairness line + File 03 §5's "a model asking for the cap is a warning" |
| 6 · Validation | File 06's "compared to what?", pointed at models — out-of-time is the control group *in time* |
| 7 · Explaining (SHAP) | File 13's stakeholders: a price nobody can explain is a price no committee will pass |
| 8 · Monitoring | File 09's lesson that a system corrupts its own data — so keep a clean stream flowing |

## 1. Data and EDA (exploratory data analysis)

Before any model: look at the data. Histograms of every column (File 11's
shapes), missing values, weird spikes, and **granularity** — what does one
row mean? One *quote*? One *day per branch*? Mixing granularities is the
most common silent error in pricing data.

Practitioners spend more time cleaning and joining data than modelling —
one real case consolidated 250+ files before any analysis. **Saying this out
loud signals experience.**

> **Your question:** "What does one row represent, and what share of rows
> had to be cleaned or dropped?"

## 2. The conversion model — the engine of modern pricing

The workhorse: a model that predicts, for each quote,

> **P(customer buys | the price we quoted, and who they are)**

Usually a **logistic regression** (a model whose output is a probability
between 0 and 1) or a boosted-tree model. The features that matter most, in
practice (from real pricing shops):

- **Relative price to market** — your quote ÷ market average. Customers
  respond to *position*, not absolute price. On a comparison site, your
  **rank** matters even more than your rate.
- **Behavioural signals** — lead time (booking early = choosier), channel,
  time of day, number of quote edits.
- **Customer & product basics** — order size, destination/currency, tenure.

**The elasticity connection (neat and worth remembering):** if you include
**log(relative price)** as a feature, its coefficient reads directly as the
price sensitivity — "a 1% price rise changes conversion by about X%". The
conversion model *contains* File 03's elasticity.

> **Your question:** "Is price in the model as *relative to market*, and
> where does the market price come from?"

## 3. From model to money: expected profit

For any candidate price:

> **Expected profit per quote = (price − cost) × P(buy at that price)**

Sweep the price up and down, compute expected profit at each level, pick the
top — that's price optimisation in one sentence. (Grand versions add
constraints; the skeleton is this.)

**The catch you already know:** if the historical prices in the training
data were set *in response to* demand (File 03 §6, endogeneity), the model's
"price effect" is poisoned, and the optimiser confidently walks you off a
cliff — in the repo's case study, pricing on the poisoned number costs
**45% of profit**. Fixes: experiments (File 06) or instruments (glossary: IV).

> **Your question:** "Where did the price *variation* in the training data
> come from — did we set those prices because demand was high?"

## 4. GLMs — the industry's shared language

A **GLM** (generalised linear model) is a regression that lets you pick the
right output shape (File 11) for the job. The table to recognise:

| You're predicting | Family | Example |
|---|---|---|
| Yes/no (buy? claim?) | Binomial (logistic) | conversion model |
| A count | Poisson / neg-binomial | claims, arrivals per day |
| A positive skewed amount | Gamma | claim cost, cost-to-serve |
| A continuous symmetric thing | Normal | rate-move noise |

Why GLMs persist when fancier models exist: they're **explainable line by
line** — which regulators, auditors and committees require. Modern shops run
both: GLM for the auditable rate card, machine learning to find what the GLM
misses, then fold the findings back in.

## 5. Guardrails and capping

Two different "caps" — do not confuse them:

- **Feature capping** — cap *inputs* before modelling (e.g. "number of past
  claims" capped at 5) so one weird record can't bend the model.
- **Price/premium capping** — cap *outputs*: floors and ceilings on the
  price itself, and a **max step per change** so prices can't jump on a
  customer. This is also a regulatory matter (the UK banned "price walking"
  — quietly ratcheting loyal customers' renewals).

Plus the guardrails from the notebooks: bounded corridors for any automated
pricing, no protected characteristics as features, and a kill-switch to a
safe static price.

> **Your question:** "What stops this model from quoting something absurd —
> and how fast can we turn it off?"

## 6. Validation — the honest exam

- **Train/test split:** never grade a model on data it studied.
  **Overfitting** = memorising the training data's noise; looks brilliant,
  fails live.
- **Cross-validation:** repeat the split several ways, average — steadier
  verdict.
- **Out-of-time (OOT) validation — the one pricing cares most about:**
  train on Jan–Sep, test on Oct–Dec. Pricing data drifts with seasons,
  competitors and the economy; a model must prove itself on the *future*,
  not on shuffled past. If someone shows random-split results only, ask for
  OOT.
- **Metrics you'll hear:** **AUC** (how well the model separates buyers
  from non-buyers: 0.5 = coin flip, 1.0 = perfect; ~0.7–0.8 is typical and
  useful), **Gini** (same idea, rescaled: Gini = 2×AUC−1), **lift** (how much
  better than guessing in the top slice).

> **Your question:** "What's the out-of-time performance, and how much worse
> is it than the random-split number?" (It's always somewhat worse; a *big*
> gap means drift or leakage.)

## 7. Explaining the model — SHAP vs permutation

Committees and regulators ask "why did it quote that?" Two standard tools:

- **Permutation importance** — shuffle one feature; see how much accuracy
  drops. Simple, global, but blind to *direction* and unreliable when
  features are correlated.
- **SHAP** — assigns each feature a fair share of each individual
  prediction (game-theory maths under the hood). Gives **direction** (this
  feature pushed the price *up*), **per-customer explanations** (crucial for
  a complaint or a regulator), and handles correlated features better.

Plain rule: permutation for a quick sanity scan; **SHAP when a human needs
to be convinced**.

## 8. Monitoring — models rot

The world drifts; a model trained on last year slowly stops describing this
year. Production pricing needs:

- **Data drift alarms** — is today's input mix still like the training mix?
  The standard score is **PSI** (population stability index): roughly, "how
  different is the current distribution from the reference one?" Rules of
  thumb: PSI < 0.1 fine · 0.1–0.25 watch · > 0.25 investigate/retrain.
- **Performance tracking** — predicted vs actual, on a rolling window, with
  a **traffic-light dashboard** (green/amber/red) so non-technical owners
  can see health at a glance.
- **Decision drift** — are recommended prices creeping toward the cap?
  (A model asking for the cap is a warning, not an answer — File 03 §5.)
- **Retraining triggers and a fallback** — pre-agreed thresholds, and a safe
  static price to fall back to. And remember the subtle one from the
  notebooks: once the model sets prices, its own logs stop containing clean
  price variation — keep a small **randomised exploration stream** on
  permanently, or next year's model learns from this year's habits.

> **Your question:** "Show me the PSI trend and the date of the last
> retrain — and what's the fallback if it breaks at 9am Saturday?"

## 8B. Conversion vs retention models — the feature difference

*(Absorbed from the interview notes.)* Both predict a customer's decision, but
the context dictates the features:

- **Conversion (new business):** the prospect is actively shopping — the model
  is about the *offer*. Features: price competitiveness (`quote_price`,
  `market_average_price`, `relative_price_to_market`, `rank_on_aggregator`,
  `log_relative_price`, `discount_applied`), prospect profile (age, product
  details, claims history, credit tier), acquisition channel. There is no
  behavioural history with you, because there is none.
- **Retention (renewal):** the customer has history — the model is about the
  *experience and the price shock*. Features: tenure and loyalty
  (`years_as_customer`, `past_renewals`), in-life experience (claims and their
  outcome, mid-term adjustments, contact-centre calls, payment history),
  **price shock** (`renewal_premium`, `previous_premium`, increase in % and £,
  `premium_change_vs_inflation`), and policy setup (`auto_renewal_enabled`,
  payment method). Change-from-last-year features usually drive the decision.

One line: **conversion is winning a stranger with a competitive offer;
retention is keeping a known customer through their reaction to a new price.**

## 9. Check yourself

**Q1.** A colleague reports 94% accuracy on a random train/test split.
What two follow-ups do you ask before believing it matters?

**Q2.** The conversion model's log-relative-price coefficient is −1.8.
Translate for the pricing committee in one sentence.

**Q3.** PSI on order-size jumped to 0.31 after a competitor's app died and
their customers flooded in. Is the model wrong? What do you do?

---

### Answers

**A1.** (1) "What's the **out-of-time** performance?" (2) "What's the
**base rate**?" — if 93% of quotes don't convert anyway, 94% accuracy might
be a coin that always says 'no'. Ask for AUC/lift instead of accuracy.

**A2.** "Customers in this segment are price-elastic: a 1% price increase
loses about 1.8% of conversions — so a price *rise* here shrinks revenue."
(File 03's dividing line, spoken through the model.)

**A3.** The model isn't *wrong* — the **world changed** (new customer mix).
PSI did its job. Short-term: watch performance, widen guardrails' human
review; medium-term: retrain including the new mix; and record the event —
it's exactly the regime change File 03 warned makes elasticity a moving target.

---

**When you're ready for more:** the workflow lives as real notebooks in
[`../../hastings/`](../../hastings/) (EDA → baseline → feature importance →
fine-tune → uncertainty), the production concerns in
[`../fres_prep/N9_safe_exploration_consumer_duty.ipynb`](../fres_prep/N9_safe_exploration_consumer_duty.ipynb),
and full model code in
[`../fast_transaction_services/`](../fast_transaction_services/README.md).
