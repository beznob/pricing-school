# Engine

All the runnable Python in one place. The labs in stages 1 to 4 import from here
through a small `toolkit.py` shim in each folder, and the panel notebooks import it
directly via `_style.py`. Nothing is reimplemented anywhere else.

```bash
pip install -r requirements.txt
python run_role_case_study.py     # about five seconds
```

That writes [RESULTS.md](RESULTS.md), four figures into `images/`, and the fair value
assessment into
[../04_satisfy_the_regulator/02_fair_value_assessment.md](../04_satisfy_the_regulator/02_fair_value_assessment.md).

## The pricing models

| Module | What it does |
|---|---|
| `travel_money_simulator.py` | The synthetic business: five channels, FX margin, card lifecycle, competitor margins, a fair value portfolio, with known ground truth and a cost-shock instrument |
| `elasticity_models.py` | Elasticity estimators. Two point, naive OLS which is biased, and IV/2SLS which is causal, with the first stage F statistic and a per-segment comparison against truth |
| `distribution_economics.py` | Channel P&L, the margin waterfall, competitive positioning, and the margin support break-even |
| `dynamic_pricing.py` | The Lerner optimal fee, a live pricing environment where cost rises with load, a guarded surge controller, and Thompson sampling and epsilon-greedy bandits |
| `fair_value.py` | FCA Consumer Duty fair value scoring under PRIN 2A.4, vulnerable customer harm, and the generated assessment document |
| `aop_scenario.py` | The AOP revenue build-up by line and channel, scenario analysis, the revenue bridge, and a competitor price index with cross-elasticity sensitivity |
| `run_role_case_study.py` | The end to end pipeline: console report, four figures, and `RESULTS.md` |

Each module also runs on its own as a quick self test, for example
`python elasticity_models.py`.

## The commercial toolkit

| Module | What it does |
|---|---|
| `pricing_toolkit.py` | Plumbing for the labs. Finds `../data/`, loads tables with the right dtypes, and sets one chart style. No pricing logic lives here on purpose |
| `pricing_finance.py` | Roughly thirty pricing formulas as runnable, doctested functions. Each docstring says what the number means commercially, not just how it is computed |
| `db_helper.py` | The business as SQL. Plumbing plus eight worked commercial views, one question each, with the SQL written out to be read |
| `create_database.py` | Builds `../data/meridian.db`, 19 tables, indexed, from the CSV files |
| `pricing_charts.py` | The eight charts a pricing manager presents, written to `../03_defend_the_plan/charts/`, each with the headline to say, how to read it aloud, the questions you will get, and the caveat to volunteer |

## Headline results

From [RESULTS.md](RESULTS.md), regenerated on a fixed seed. Three things worth being
able to say from memory.

Naive OLS understates price sensitivity in every channel, because the desk raises the
margin when demand is already strong. Digital is truly at about -2.2 and OLS reports
-1.1. Pricing on the biased number systematically over-charges.

The headline FX margin says almost nothing about channel profitability. The Post
Office earns the highest gross revenue and pays around 45% of it away in Postmaster
commission, while digital drops almost all of its revenue to contribution. Price the
net, not the headline.

Uniform price moves destroy value and targeted ones create it. A blanket 10% rise in
FX margin reduces contribution, because blended demand is elastic, while harvesting
the inelastic channels and competing in the elastic ones lifts it.

## The written case study

[CASE_STUDY.md](CASE_STUDY.md) is the domain write-up: the business and its price
levers, channel elasticity estimated causally, distribution economics, Consumer Duty
fair value, and AOP scenario modelling with competitor intelligence.

## A note on the name

These modules were first written for a real-time payments case study called FastPay,
which is why some internals still speak of transactions and fees rather than currency
and margin. The payments layer itself is parked in
[../_archive/fastpay_payments/](../_archive/fastpay_payments/). Nothing in the track
depends on it.
