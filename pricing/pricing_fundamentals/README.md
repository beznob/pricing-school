# Pricing Fundamentals — a runnable course, zero to hero

A hands-on companion to [`../pricing_school/`](../pricing_school/00_START_HERE.md).

The school explains pricing in prose. **This course makes you do it** — on a
simulated but realistic business, with an answer key, so you can find out
whether your estimate was right instead of just plausible.

Every notebook is mostly *text*: the concepts, the vocabulary, the
commercial reasoning and the traps. The code is there to prove each claim on
data you can poke at, not to be the lesson.

## How to run it

```bash
pip install numpy pandas matplotlib scipy statsmodels scikit-learn jupyter
jupyter lab            # from inside this folder
```

Then **run `01_data_foundation.ipynb` first, top to bottom** (about a
minute). It builds nineteen CSV tables plus `data/truth.json` in `data/`.
Every other notebook loads them. The CSVs are not committed to git — this
repository ignores `*.csv` — so the notebook is the source of truth and
anyone can rebuild the world from scratch.

Notebooks 02 onwards can be read in order or dipped into; each states its
prerequisites at the top and ends with practice questions and worked
answers.

## The commercial toolkit

Five files sit beside the notebooks and are worth an hour on their own — they
are the finance, the data plumbing and the presentation craft a pricing
manager is expected to have at their fingertips, rather than a lesson to work
through.

```bash
python pricing_finance.py            # every pricing formula, on real figures
python -m doctest pricing_finance.py # and every number in it, checked
python create_database.py            # CSVs -> data/meridian.db (19 tables, indexed)
python db_helper.py                  # eight worked commercial queries, printed
python pricing_charts.py             # eight board charts + the words to say
```

| File | What it gives you |
|---|---|
| **[`FINANCE_FOR_PRICING.md`](FINANCE_FOR_PRICING.md)** | **Start here if the finance is the unfamiliar part.** Turnover vs revenue vs contribution, margin vs markup, which costs belong in a price decision, the discount break-even, the Lerner rule, the price waterfall and the PVM bridge, lifetime value and NPV — each with Meridian's own numbers and the way it is normally got wrong |
| **[`pricing_finance.py`](pricing_finance.py)** | The same thirty-odd formulas as runnable, doctested functions. Every docstring says what the number *means* commercially, not just how it is computed |
| **[`db_helper.py`](db_helper.py)** | The business as SQL. Plumbing (`query`, `schema`, `truth`) plus eight worked views — `pnl()`, `unit_economics()`, `discount_hurdles()`, `price_waterfall()`, `revenue_bridge()`, `margin_by_segment()`, `stockout_cost()`, `retention_by_price()` — one commercial question each, with the SQL written out to be read |
| **[`pricing_charts.py`](pricing_charts.py)** | The eight charts a pricing manager actually presents, built from the live database — and for each one the **headline** to say first, how to **read** it out loud, the questions you will be **asked** with your answers, and the **caveat** to volunteer before someone finds it |
| **[`STAKEHOLDER_STORYTELLING.md`](STAKEHOLDER_STORYTELLING.md)** | **The English of explaining a pricing chart.** Writing a headline that is a claim rather than a caption, the verbs and collocations commercial audiences expect, the word pairs that quietly cost you credibility (turnover/revenue/contribution, percent/percentage point, margin/markup, elasticity/semi-elasticity), calibrated confidence instead of hedging, sentence frames for the six questions you always get, and how to say no. With drills |

See [`DATABASE_USAGE.md`](DATABASE_USAGE.md) for the schema, how to read a
star schema, and the queries worth having.

**If stakeholder communication is the part you want to work on**, run
`python pricing_charts.py`, then read
[`STAKEHOLDER_STORYTELLING.md`](STAKEHOLDER_STORYTELLING.md) with the eight
PNGs in `charts/` open beside it. The charts are the evidence; the guide is
the language.

## The course

| # | Notebook | Track | What you learn |
|---|---|---|---|
| 01 | `01_data_foundation.ipynb` | Data | Builds the world. Grain, facts vs dimensions, quotes vs sales, channel choice, censoring, selection — and the answer key |
| 02 | `02_price_cost_and_profit.ipynb` | Commercial | Margin vs markup, cost taxonomy, contribution, break-even, discount break-even `d/(CM−d)`, the price waterfall, the price–volume–mix bridge |
| 03 | `03_demand_and_elasticity.ipynb` | Commercial + technical | Willingness to pay, the demand curve, elasticity and semi-elasticity, the Lerner rule, revenue vs profit maxima, cross-price effects, segment heterogeneity, WTP research methods |
| 04 | `04_statistical_foundations.ipynb` | Statistical | Distributions for pricing, how averages lie, sampling error, confidence intervals, the bootstrap, power and MDE, regression to the mean |
| 05 | `05_regression_for_pricing.ipynb` | Statistical | OLS and logistic regression as pricing tools, omitted-variable bias, why the *grain* you aggregate to changes the answer, fixed effects, validation, calibration |
| 06 | `06_experiments_and_ab_testing.ipynb` | Statistical + commercial | Randomisation, hypothesis tests, the real A/B test in the data, metric choice, variance reduction, peeking, guardrails |
| 07 | `07_causal_inference.ipynb` | Technical | Confounding and DAGs, difference-in-differences across 12 regions, instrumental variables (and a flawed one), double machine learning, bad controls |
| 08 | `08_price_optimisation.ipynb` | Commercial + technical | Profit curves, constrained optimisation and shadow prices, uncertainty, promotions and incrementality, and the lifetime-value correction that makes every static optimiser too aggressive |
| 09 | `09_segmentation_and_fairness.ipynb` | Commercial | Price discrimination, fences, Simpson's paradox, a fairness audit that finds a real age gap, Consumer Duty, the cost of a policy cap |
| 10 | `10_competition_and_dynamics.ipynb` | Commercial + technical | Competitive response and lead-lag tests, price wars, dynamic pricing, bandits, recovering stockout-censored demand |
| 11 | `11_operating_model.ipynb` | Commercial | KPIs and the P&L, the revenue bridge, governance and committees, PSI and control charts, the capstone case |
| 12 | `12_omnichannel_case_study.ipynb` | **The whole course, applied** | A live proposal — one price across all channels for FX cash — taken from "is it worth doing?" to a funded, pre-registered geo test: sizing the prize, the cost-to-serve floor, the cannibalisation-proof metric, power on the real region panel, randomisation inference, why the business's own 2024 trial could never have worked, and the rollout decision rule |

**Notebook 12 is the one to read if you only read one.** It works the
omnichannel single-price proposal in
[`../fres_prep/omnichannel_one_pager.md`](../fres_prep/omnichannel_one_pager.md)
all the way through, and it is where the commercial judgement lives: what to
measure, what not to promise, how to sequence the work, and how to write the
paper that gets it approved.

## The business you will be pricing

**Meridian FX** sells foreign currency to UK travellers.

- **Four high-street branches**, one **airport kiosk** (Heathrow T3) and one
  **online** channel — six locations across 12 regions, two calendar years of
  trading, 14,000 customers who come back.
- **Three products**: euro cash, dollar cash, and a multi-currency prepaid
  card that carries a £4.95 fee.
- The rate board is set **per site and product per day**, which is the grain
  every price decision has to be made at.

`db.overview()` prints the live row counts; `01_data_foundation.ipynb`
regenerates the world, so treat any figure in a document as a description of
one build rather than a constant.

Five structural features let it teach the whole subject rather than one
corner of it:

| Feature | Why it matters |
|---|---|
| **12 regions, two branches each** | Regions are the unit a geo experiment randomises — enough of them to run and analyse a real one (notebook 12) |
| **Customers choose their channel, and the choice depends on the price gap** | Move the online-versus-branch gap and customers switch. That is **cannibalisation**, measurable rather than assumed |
| **Customers come back — or don't** | Overcharging above the market costs about 12% of a customer's trips next year, so price affects lifetime value, not just today's order |
| **A commission to the host retail network on every branch sale** | The largest branch variable cost is negotiated, not engineered — and it belongs to another department |
| **Stock limits that censor demand every August** | Sales become a floor on demand, not a measurement of it |

Everything is generated from written-down rules, so `data/truth.json` holds
the real elasticities, the real channel-switching coefficient, the real
experiment, promotion and trial effects, the real stockout losses, the
retention parameters and the profit-maximising margins. **Estimate first,
then check.** That loop — and not any single technique — is what the course
is teaching.

The data also contains, on purpose:

- a **randomised online A/B test** (+40bp, eight weeks) with known potential
  outcomes;
- a **non-randomised promotion** across four regions, for difference-in-differences;
- a **badly designed 2024 regional trial** (two regions, six weeks,
  hand-picked) that notebook 12 dissects;
- an **imperfect instrument** — funding-cost shocks that cluster in peak
  season, because that is what really happens;
- **marketing campaigns** that confound regional analysis;
- **complaints**, as a guardrail metric and a worked example of a collider.

See `data/DATA_DICTIONARY.md` (written by notebook 01) for every table and
column.

## Where this sits

- [`../pricing_school/`](../pricing_school/00_START_HERE.md) — the prose
  school: plain-English foundations, senior reference, glossary, interview
  bank. Read alongside; the two use the same travel-money world.
- [`../fast_transaction_services/`](../fast_transaction_services/README.md) —
  the production-shaped case study with reports and pipelines.
- [`../fres_prep/`](../fres_prep/README.md) — interview notebooks, one hard
  question each, including the omnichannel one-pager notebook 12 works from.
