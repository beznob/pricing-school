# Pricing School — Start Here

**Goal:** take you from zero to thinking like a pricing manager, in plain
English, one small step at a time.

**The rules of this school:**
- No term is used before it is explained.
- No formula appears without a worked example using small, round numbers.
- Every file ends with 2–3 practice questions. Answers are at the bottom —
  try first, then check.
- Examples use a travel-money business (selling euros to holidaymakers)
  because that is the world the rest of this repo prepares you for.

## What does a pricing manager actually do?

A pricing manager decides **what to charge**, **who to charge it to**, and
**how to prove the decision was right**. That splits into three skills:

1. **Arithmetic** — margins, percentages, break-even. (Files 01–02)
2. **Judgement** — how customers and competitors react. (Files 03–04, 07–09)
3. **Evidence** — testing changes and reading results honestly. (Files 05–06)

Most people think pricing is about clever maths. It is mostly about clear
thinking with simple maths — done carefully, and explained so a room full of
busy people can act on it.

## The path

Read in order. Each file takes roughly 30–45 minutes if you do the practice.

| File | What you learn | One-line takeaway |
|---|---|---|
| [01_price_cost_profit.md](01_price_cost_profit.md) | Price, cost, profit, margin, break-even | Profit is a small number squeezed between two big ones |
| [02_percentages_and_basis_points.md](02_percentages_and_basis_points.md) | %, percentage points, basis points, FX spreads | "0% commission" doesn't mean free |
| [03_elasticity.md](03_elasticity.md) | How demand reacts to price | Raise price 1% — how much volume do you lose? |
| [04_price_volume_mix_and_leakage.md](04_price_volume_mix_and_leakage.md) | Why profit moved; where price quietly leaks away | Fix the leaks before building anything clever |
| [05_averages_and_uncertainty.md](05_averages_and_uncertainty.md) | Averages, ranges, expected value | An unclear result is not the same as "no effect" |
| [05B_causal_inference_primer.md](05B_causal_inference_primer.md) | Confounders, endogeneity, instruments, control variables, colliders | Naive elasticity lies; here's why and how to fix it |
| [06_tests_and_experiments.md](06_tests_and_experiments.md) | How to test a price change properly | Before/after comparisons lie; control groups don't |
| [07_segments_and_fairness.md](07_segments_and_fairness.md) | Different prices for different people — and UK fairness rules | The average can look fine while one group gets a bad deal |
| [08_competition_basics.md](08_competition_basics.md) | Price wars and how not to start one | Never let a competitor set your prices for you |
| [09_forecasting_and_stockouts.md](09_forecasting_and_stockouts.md) | Predicting demand; what stockouts do to your data | The till never records the customer who walked away |
| [10_glossary.md](10_glossary.md) | Every term in one place | Look things up any time |

## Part 2 — the working toolkit (files 11–15)

After the foundations, these five files carry the **technical** and
**commercial** tracks of the actual job — distilled from everything useful
elsewhere in this repo (the insurance-maths files, the data-science
interview material, the practitioner notes), so you don't have to read the
originals unless you want the deep version.

| File | Track | What you learn |
|---|---|---|
| [11_distributions_for_pricing.md](11_distributions_for_pricing.md) | Technical | The six shapes of randomness and which one for what — order sizes, counts, tails, frequency × severity |
| [12_data_science_for_pricing.md](12_data_science_for_pricing.md) | Technical | The full workflow: EDA → conversion model → elasticity → optimise → validate (out-of-time!) → explain (SHAP) → monitor (PSI) |
| [13_commercial_kpis_and_stakeholders.md](13_commercial_kpis_and_stakeholders.md) | Commercial | The KPI dictionary with real-world benchmarks, the stakeholder map, how decisions pass committee, the first 90 days |
| [14_interview_qa_bank.md](14_interview_qa_bank.md) | Both | ~20 of the repo's best questions with short model answers — drill these out loud |
| [15_learning_path.md](15_learning_path.md) | Both | The four-week plan interleaving both tracks, the self-test, and the 48-hour compressed path |

**In a hurry?** Read [15_learning_path.md](15_learning_path.md) first — it
contains the self-test that tells you which files you can skip.

## Part 2b — the senior reference (files 18–21)

These four files absorbed everything unique from the former
`pricing_manager_handbook` (now deleted): denser, checklist-style reference
material for the Senior Manager altitude. Read them *after* the foundations —
each assumes Part 1's vocabulary.

| File | What it gives you |
|---|---|
| [18_pricing_strategy_and_offer_design.md](18_pricing_strategy_and_offer_design.md) | Strategy ladder, fences & discrimination, WTP research (EVE, Van Westendorp, conjoint), bundling & tiers, behavioural pricing, B2B/contract, subscription & platform pricing |
| [19_channels_promotions_competition.md](19_channels_promotions_competition.md) | Channel net economics, discount break-even `d/(CM−d)`, promo incrementality & governance, revenue management & dynamic-pricing guardrails, price indices, war-gaming |
| [20_operating_model_finance_regulation.md](20_operating_model_finance_regulation.md) | The operating cadence, P&L & LTV/CAC, AOP build & revenue bridge, Consumer Duty + competition law, pricing systems & controls, KPI dictionary, influence extras |
| [21_travel_money_domain.md](21_travel_money_domain.md) | The specific market: products, revenue lines, channel economics, fintech threat, regulatory frame, the senior agenda |

The senior *technical* material (2SLS mechanics, the DiD/RDD/synthetic-control/
DML methods catalogue, the causal cheat sheet) lives at the back of
[05B_causal_inference_primer.md](05B_causal_inference_primer.md) §§12–14, and
the formula cheat-sheet is in [10_glossary.md](10_glossary.md).

## Part 3 — the runnable lessons (notebooks 16–17)

Two Jupyter notebooks continue the school where the markdown stops — same
rules (plain English, small numbers, practice questions at the end), but
every claim is executed in front of you. Run them top to bottom; each takes
about 20 minutes.

| Notebook | What you learn |
|---|---|
| [16_causality_segments_competition.ipynb](16_causality_segments_competition.ipynb) | Why naive elasticity lies (the desk's own pricing rule is the confounder), fixing it by controlling for the competitor and the season, the residual-on-residual trick that scales into DML, segment-level answers, the competitor as confounder *and* lever, and the randomised branch test that settles it |
| [17_dynamic_pricing_ladder.ipynb](17_dynamic_pricing_ladder.ipynb) | Dynamic pricing as one idea plus five upgrades: re-solve when conditions change → learn the demand curve while selling (bandits) → limited stock (pace pricing) → competitor reactions (how algorithms start price wars) → profit optimisation with a sales target as a constraint, and the shadow price that settles the meeting |

## How the simple and the deep connect — the ladder rule

The school is built on one rule: **every deep idea in Part 2 and in the
repo's notebooks is one of Part 1's simple ideas plus exactly one new
complication.** Nothing you learn early gets thrown away — it gets promoted.
So when something advanced feels confusing, the fix is never "read it
again"; it is "find the rung below it."

The rungs are written out in two places:

- Every Part 1 file ends with **"Where this idea goes — the ladder"**: a
  rung-by-rung walk from its simple form up to the production version and
  the code, saying at each rung *what gets added and why the simpler
  version stops being enough*.
- Files 11 and 12 open with a **bridge-in table** mapping each of their
  sections back down to the foundation it grew from.

The master map, one line per idea:

| Simple form (Part 1) | Deep form (Part 2 / notebooks) | The connection in one line |
|---|---|---|
| Contribution & break-even (01) | Revenue bridge & AOP (13) | the same arithmetic, spoken to a CFO |
| Total cost vs headline (02) | Fair value under Consumer Duty (07 → 13) | the regulator requires the two-shop comparison you did in File 02 |
| Elasticity (03) | Conversion model & optimisation (12) | the log-price coefficient **is** the elasticity |
| Mix & leakage (04) | The fairness mix trap (07); the revenue bridge (13) | mix moves profit — and quietly moves *who pays* |
| "Averages lie" (05) | Distributions & tails (11) | "mean ≫ median" gets a name: log-normal |
| EV + reversibility (05) | Committee framing & guardrails (13, 12) | "bounded and reversible" is what passes committee |
| Control groups & MDE (06) | Geo tests & exploration streams (N1, 12 §8) | once models set prices, the experiment can never end |
| Segments (07) | Elasticity at scale (N2) | thousands of thin segments borrow strength from each other |
| Promo vs structural (08) | Matched twins & synthetic control (N8) | control-group logic for events you can't randomise |
| Censored sales (09) | Censored-aware forecasting (N3) | a sell-out is a floor, not a measurement |

## What comes after

When these ten files feel comfortable, you are ready for the advanced
material in this repo:

- **The runnable case study:** [`../fast_transaction_services/`](../fast_transaction_services/README.md)
  — real code doing everything you learned here, on a simulated travel-money
  business.
- **The interview notebooks:** [`../fres_prep/`](../fres_prep/README.md)
  — eleven notebooks, each answering one hard interview question.
- **The senior-level prep guide:** [`../../interview/FRES_MASTER_PREP_PROMPT.md`](../../interview/FRES_MASTER_PREP_PROMPT.md)
  — the full roadmap this school is the foundation for.

Each Part 1 file's closing ladder names the advanced material it climbs to;
Part 2 files end with pointers to the full deep versions in the repo.
