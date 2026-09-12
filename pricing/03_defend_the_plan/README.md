# 03 · Defend the plan

A pricing number is not finished when it is right. It is finished when it has
survived finance, gone into the annual operating plan, and been explained to a room
that will not read your appendix. This stage is that half of the job.

Steps are numbered as in the [track](../README.md). This stage comes after stage 4
in the sequence, because its lab builds on the fairness lab.

## The steps

| Step | Do this | What it teaches | Done when you can |
|---|---|---|---|
| 28 | Read [3.1 Finance for pricing](01_finance_for_pricing.md), then run `python ../engine/pricing_finance.py` | Turnover against revenue against contribution, margin against markup, which costs belong in a price decision, the discount break-even, the Lerner rule, the waterfall, lifetime value and NPV | Tell turnover from revenue from contribution without hesitating |
| 29 | Read [3.2 KPIs and stakeholders](02_kpis_and_stakeholders.md) | The KPI dictionary with real benchmarks, the stakeholder map, how decisions pass committee, the first 90 days | Build a revenue bridge and say who owns each line |
| 30 | Run [lab 3.1](lab_01_operating_model.ipynb) | KPIs and the P&L, the revenue bridge, governance and committees, drift monitoring with PSI and control charts, a capstone case | Take a set of price moves into an AOP and monitor them |
| 31 | Read [3.3 Operating model and governance](03_operating_model_and_governance.md) | The operating cadence, P&L and unit economics, the AOP build, regulation, systems and controls. Senior reference | Describe the cadence and the governance around a price change |
| 32 | Run `python ../engine/run_role_case_study.py`, then read [RESULTS.md](../engine/RESULTS.md) and [CASE_STUDY.md](../engine/CASE_STUDY.md) | The whole business end to end: channel elasticity, distribution economics, fair value, the AOP under scenarios | Recite the three headline results in the [engine README](../engine/README.md) |
| 33 | Read [3.4 Stakeholder storytelling](04_stakeholder_storytelling.md) with the eight charts open | A headline that is a claim rather than a caption, the word pairs that cost credibility, calibrated confidence, sentence frames for the six questions you always get, how to say no | Give the headline, the reading, the caveat and the answer to the obvious question for each chart |

Then [stage 5](../05_the_panel/).

## The charts

[charts/](charts/) holds the eight charts a pricing manager actually presents, built
from the live database. Regenerate them with `python ../engine/pricing_charts.py`.
The script prints, for each chart, the headline to say first, how to read it out
loud, the questions you will be asked with your answers, and the caveat to volunteer
before someone else finds it. The charts are the evidence and file 3.4 is the
language.

## The commercial toolkit

Three scripts in [engine](../engine/) belong to this stage. `pricing_finance.py` is
every pricing formula as a runnable, doctested function, and
`python -m doctest pricing_finance.py` checks every number in it. `db_helper.py` is
the business as SQL: `pnl()`, `unit_economics()`, `discount_hurdles()`,
`price_waterfall()`, `revenue_bridge()`, `margin_by_segment()`, `stockout_cost()`
and `retention_by_price()`, one commercial question each, with the SQL written out
to be read. `pricing_charts.py` is described above. The schema is documented in
[database usage](../appendix/database_usage.md) and the SQL drills are in
[SQL learning questions](../appendix/sql_learning_questions.md).

## Where the ideas go

Panel notebook N5 is the interview-grade pocket price waterfall and N11 is the
repricing runbook a CFO would want to see. The regulatory half of governance is in
[stage 4](../04_satisfy_the_regulator/) and in §4 of file 3.3.
