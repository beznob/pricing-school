# Pricing

Everything for the **Senior Manager, Pricing, Distribution & Revenue** role at
**First Rate Exchange Services**, the Post Office travel money joint venture.

The folder is arranged as the job, not as a syllabus. A pricing manager does four
things over and over: works out what to charge, proves a change was worth making,
defends the number when it goes into a plan, and shows the regulator the customer
got fair value. Each of those is a numbered folder, and the panel folder is where
the four get spent.

Files are named by stage and position, so **file 2.3** is the third prose file in
`02_prove_the_change/` and **lab 1.2** is the second runnable lesson in
`01_set_the_rate/`. Every cross reference in the track uses those names, and every
heading matches its filename, so you always know where you are.

The [skills map](00_the_role/skills_map.md) lists every accountability in the job
description and the exact steps below that teach it, prove it and rehearse it.

---

## How each step works

Read the prose file first. It is written in plain English, uses small round numbers,
and ends with two or three practice questions with answers at the bottom. Try them
before you look. Then open the lab beside it, and before you run each cell, say what
number you expect. The Meridian FX world the labs run on was generated from
written-down rules, so `data/truth.json` holds the real elasticities and the real
effects, and you can mark yourself. Finally, where a panel notebook rehearses the
same idea, read its sixty second answer aloud. Read, predict, check, say. That loop
is the method, more than any single technique.

---

## The path, step by step

The prose is grouped by job stage. The labs share one dataset and build on each
other, so they run in dependency order, which is not quite the stage order. The
sequence below is the honest one: follow it and nothing is asked of you before it
has been taught. The three places it loops back to an earlier stage are marked.

| Step | Do this | Done when you can |
|---|---|---|
| 1 | Read [file 0.1](00_the_role/the_job_and_the_evidence.md), the job mapped to evidence | Say what the role is accountable for in one breath |
| 2 | Read [file 0.2](00_the_role/the_market.md), the travel money market, then [file 0.4](00_the_role/the_card_and_the_migration.md), the card and the migration | Name the revenue lines, say what TMC means in this job, and describe what a processor migration changes for pricing |
| 3 | Read [file 1.1](01_set_the_rate/01_price_cost_and_profit.md) | Explain why a 2% price cut can eat half the profit per sale |
| 4 | Read [file 1.2](01_set_the_rate/02_percentages_and_basis_points.md) | Say where the profit hides in "0% commission" |
| 5 | Run [lab 2.1](02_prove_the_change/lab_01_data_foundation.ipynb), top to bottom | The data folder is built and you can say what grain the price is set at |
| 6 | Run [lab 1.1](01_set_the_rate/lab_01_price_cost_and_profit.ipynb) | Compute the discount break-even and read a price waterfall |
| 7 | Read [file 1.3](01_set_the_rate/03_elasticity.md) | State the minus one dividing line and the markup rule |
| 8 | Run [lab 1.2](01_set_the_rate/lab_02_demand_and_elasticity.ipynb) | Estimate an elasticity and check it against the answer key |
| 9 | Read [file 1.4](01_set_the_rate/04_price_volume_mix_and_leakage.md) | Split a profit move into price, volume and mix, and name three leaks |
| 10 | Read [file 1.5](01_set_the_rate/05_competition.md) | Tell a promotional move from a structural one and say why never to blanket match |
| 11 | Read [file 2.1](02_prove_the_change/01_averages_and_uncertainty.md) | Explain why a range crossing zero is not "no effect", and frame it as expected value |
| 12 | Run [lab 2.2](02_prove_the_change/lab_02_statistical_foundations.ipynb) | Size a test from the noise in the data |
| 13 | Read [file 2.2](02_prove_the_change/02_tests_and_experiments.md) | Design a control group and name the neighbour problem |
| 14 | Run [lab 2.3](02_prove_the_change/lab_03_regression_for_pricing.ipynb) | Say why the grain you aggregate to changes the answer |
| 15 | Run [lab 2.4](02_prove_the_change/lab_04_experiments_and_ab_testing.ipynb) | Analyse the real A/B test in the data without peeking |
| 16 | Read [file 2.3](02_prove_the_change/03_causal_inference_primer.md) | Explain why the desk's own pricing rule is the confounder, and what an instrument is |
| 17 | Run [lab 2.5](02_prove_the_change/lab_05_causal_inference.ipynb) | Recover a true effect with difference in differences and with an instrument |
| 18 | Run [lab 2.6](02_prove_the_change/lab_06_causality_segments_competition.ipynb) | Do the residual on residual trick by hand |
| 19 | Read [file 2.4](02_prove_the_change/04_forecasting_and_stockouts.md) | Describe the stockout death spiral and how to get out of it |
| 20 | **Loop back.** Run [lab 1.3](01_set_the_rate/lab_03_price_optimisation.ipynb) | Find a profit maximising price and say why a static optimiser is too aggressive |
| 21 | Read [file 1.6](01_set_the_rate/06_strategy_and_offer_design.md) | Walk the strategy ladder and name three fences |
| 22 | Read [file 1.7](01_set_the_rate/07_channels_promotions_revenue_management.md) | Price the pocket, not the list, and state the discount break-even from memory |
| 23 | Run [lab 1.5](01_set_the_rate/lab_05_dynamic_pricing_ladder.ipynb) | Explain the shadow price on a sales target |
| 24 | Read [file 4.1](04_satisfy_the_regulator/01_segments_and_fairness.md) | Describe the fairness check that passes while the harm is real |
| 25 | Run [lab 4.1](04_satisfy_the_regulator/lab_01_segmentation_and_fairness.ipynb) | Run a fairness audit and cost a policy cap |
| 26 | Read [file 4.2](04_satisfy_the_regulator/02_fair_value_assessment.md), then regenerate it with `python engine/fair_value.py` | Explain a price against value assessment to a compliance colleague |
| 27 | **Loop back.** Run [lab 1.4](01_set_the_rate/lab_04_competition_and_dynamics.ipynb) | Test whether a competitor leads or follows, and recover censored demand |
| 28 | Read [file 3.1](03_defend_the_plan/01_finance_for_pricing.md), then run `python engine/pricing_finance.py` | Tell turnover from revenue from contribution without hesitating |
| 29 | Read [file 3.2](03_defend_the_plan/02_kpis_and_stakeholders.md) | Build a revenue bridge and say who in the business owns each line |
| 30 | **Loop back.** Run [lab 3.1](03_defend_the_plan/lab_01_operating_model.ipynb) | Take a set of price moves into an AOP and monitor them with PSI |
| 31 | Read [file 3.3](03_defend_the_plan/03_operating_model_and_governance.md) | Describe the operating cadence and the governance around a price change |
| 32 | Run `python engine/run_role_case_study.py`, then read [RESULTS.md](engine/RESULTS.md) and [CASE_STUDY.md](engine/CASE_STUDY.md) | Recite the three headline results in the engine README |
| 33 | Read [file 3.4](03_defend_the_plan/04_stakeholder_storytelling.md) with the charts from `python engine/pricing_charts.py` open | Give the headline, the reading, the caveat and the answer to the obvious question for each chart |
| 34 | The live proposal: [one pager](05_the_panel/omnichannel_one_pager.md), [reasoning](05_the_panel/omnichannel_reasoning_and_concepts.md), then run [the omnichannel lab](05_the_panel/lab_omnichannel_case_study.ipynb) | Defend the rollout rule and say what you would ask for on day one |
| 35 | The [panel notebooks](05_the_panel/README.md) in tier order: N4, N5, N1, N3, N6, then N2, N7, N9, then N8, N10, N11 | Say each sixty second answer, timed, and volunteer its limitation |
| 36 | The [question bank](05_the_panel/interview_qa_bank.md) and the self test below, out loud | Score eight or more on the self test |

The [appendix](appendix/) is not a step. Dip into it when a file sends you there:
the glossary, the shapes of randomness, the full data science workflow, the database
and its SQL drills.

---

## The stages, for navigation

| Stage | What the job asks | Folder |
|---|---|---|
| 0 | Who FRES is and what the role is accountable for | [00_the_role](00_the_role/) |
| 1 | Decide what to charge | [01_set_the_rate](01_set_the_rate/) |
| 2 | Show the change worked | [02_prove_the_change](02_prove_the_change/) |
| 3 | Survive contact with finance | [03_defend_the_plan](03_defend_the_plan/) |
| 4 | Prove fair value | [04_satisfy_the_regulator](04_satisfy_the_regulator/) |
| 5 | Answer the interview | [05_the_panel](05_the_panel/) |

Supporting the track: [engine](engine/) holds every line of shared Python, the
simulator, the estimators, channel P&L, fair value scoring, AOP scenarios and the
commercial toolkit. [data](data/) is the Meridian FX world, generated by lab 2.1 and
not committed. [_archive](_archive/) is superseded work that nothing depends on.

---

## Getting it running

```bash
pip install -r engine/requirements.txt
jupyter lab                       # step 5 builds the data everything else reads
cd engine && python run_role_case_study.py    # the case study needs no data build
```

---

## Am I ready? The self test

Say each of these out loud, unprepared. Score yourself honestly.

| # | Can I explain | Taught in |
|---|---|---|
| 1 | why a 2% price cut can eat half the profit per sale | file 1.1 |
| 2 | where the profit hides in "0% commission" | file 1.2 |
| 3 | elasticity, the minus one dividing line, and the markup rule | file 1.3 |
| 4 | price, volume and mix, and the leakage waterfall | file 1.4 |
| 5 | promotional versus structural competition, and why never to blanket match | file 1.5 |
| 6 | why a confidence interval crossing zero does not mean the change failed | file 2.1 |
| 7 | control groups, difference in differences, and the neighbour problem | file 2.2 |
| 8 | why the desk's own pricing rule makes naive elasticity wrong | file 2.3 |
| 9 | censored sales and the stockout death spiral | file 2.4 |
| 10 | the AOP build, the revenue bridge, and what finance will push back on | file 3.2 |
| 11 | the fairness check that passes while the harm is real | file 4.1 |
| 12 | which distribution fits order sizes, counts and tails | the distributions appendix |

Eight or more confident and you can go straight to steps 34 to 36. Fewer than eight
and the plan below patches the gaps.

---

## The four week plan

About an hour a day. Read, do the practice questions, say one answer out loud. The
job is a commercial role that happens to need real statistics, so never spend a whole
week on one side. The steps already alternate; follow them in order.

**Week 1, the money.** Steps 1 to 10. At the weekend run the case study (step 32
early) and simply read the output. You should recognise most of the words by then.

**Week 2, the evidence.** Steps 11 to 19. Finish with panel notebooks N4 and N5 and
read their sixty second answers aloud. N4 is the single highest leverage answer in
the whole folder.

**Week 3, the judgement.** Steps 20 to 33. Add panel notebooks N6 and N8, and draft
your own three career stories in STAR shape.

**Week 4, integration.** Steps 34 to 36, then a full timed mock against the self
test and the [skills map](00_the_role/skills_map.md).

**If you have 48 hours.** Re-run the self test and patch only the failures. Run N4
and drill its answer until it is automatic. Read the question bank end to end, out
loud. Re-read the honesty rule below. Then sleep, because fluency beats coverage.

---

## Three habits that outlast the plan

Every average invites the question "averaged over whom?". Every result invites
"compared to what control?". Every recommendation invites "what is the downside, and
can we reverse it?". Ask those three relentlessly and you will out-perform people
with better maths, because the maths is rarely the binding constraint.

## The honesty rule

Every number in this folder comes from a simulator or a generated dataset. The
figures demonstrate that a method works, not what FRES actually earns. Say so in the
room. Claiming a modelled result as a real one is the fastest way to lose a panel,
and volunteering the limitation is what makes the rest of the answer credible.
