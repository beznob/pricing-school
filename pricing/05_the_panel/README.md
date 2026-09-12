# 05 · The panel

Eleven notebooks, one hard interview question each, plus the live proposal that runs
through the whole interview. This is where the four stages get spent.

Every notebook follows one contract: simulate a known ground truth, show the naive
method failing, apply the fix, prove it recovers the truth, then end with
`## The 60-second answer`, which is the words you say out loud rather than a summary,
and `### What I'd say if pushed deeper`, which is three follow-ups of which the third
is always an honest limitation. Volunteering that limitation is what signals
seniority.

## The live proposal

The omnichannel question, one rate for FX cash across every channel, is the thread
the panel keeps pulling on. Three files cover it at three depths.

| File | What it is |
|---|---|
| [omnichannel_one_pager.md](omnichannel_one_pager.md) | The executive recommendation. Progressive rollout gated by region level tests, Monte Carlo for test sizing, historical elasticities treated as biased priors, and the public promise held back until last because the marketing claim is the irreversible step. Ends with the data you would ask for on day one |
| [omnichannel_reasoning_and_concepts.md](omnichannel_reasoning_and_concepts.md) | How the one pager was built. The reasoning chain step by step, and the concepts behind each move |
| [lab_omnichannel_case_study.ipynb](lab_omnichannel_case_study.ipynb) | The same proposal worked all the way through on data: sizing the prize, the cost to serve floor, the cannibalisation-proof metric, power on the real region panel, randomisation inference, why the business's own 2024 trial could never have worked, and the rollout decision rule |

**If you only work one thing in this folder, work that notebook.** It is where the
commercial judgement lives: what to measure, what not to promise, how to sequence,
and how to write the paper that gets approved.

## Tier 1, highest differentiator per hour

| Notebook | Panel question | Asked by | Headline result |
|---|---|---|---|
| [N4_uncertainty_to_decision](N4_uncertainty_to_decision.ipynb) | "+2% margin, the confidence interval crosses zero. Did it work?" | CRO/CCO | A true +2% fails significance 65% of the time at this design. Probability of being accretive is 93%, expected value £1.1m a year, and extending the test has negative value of information, so roll out with monitoring |
| [N5_pocket_price_waterfall](N5_pocket_price_waterfall.ipynb) | "You have 8 weeks to show quick wins" | CRO/CCO | Headline 500bps becomes pocket 435bps. £1.6m a year of recoverable leakage, and +1% realised price is +11.1% operating profit, computed rather than quoted. Holdout difference in differences says 0.73% against a naive over-claim of 3.56% |
| [N1_geo_experiment_design](N1_geo_experiment_design.ipynb) | "Design a margin test across the estate" | Head of Data | Cross-shopping roughly doubles the measured lift. Travel-to-work-area clustering with a buffer sweep fixes it. The MDE table shows 5bps is invisible to a 50 branch pilot, CUPED cuts MDE by 55%, and synthetic control recovers the truth |
| [N3_censored_demand_stockouts](N3_censored_demand_stockouts.ipynb) | "Euros stock out every Friday. Is that pricing or ops?" | Head of Data and Product | The naive forecast understates Friday demand by 40% and spirals stock from 33k to 21k. Censored maximum likelihood recovers the truth within about 4%, and the same policy with a fixed forecast arrests the spiral |
| [N6_channel_differential_fair_value](N6_channel_differential_fair_value.ipynb) | "Click and collect undercuts walk-up" and "evidence airport fair value" | CRO/CCO | The within-channel fairness check passes while the mix hides a 1.33 percentage point vulnerable customer premium. Also covers favourable-subset benchmarking and the airport as a distinct target market |

## Tier 2

| Notebook | Panel question | Headline result |
|---|---|---|
| [N2_hierarchical_elasticity](N2_hierarchical_elasticity.ipynb) | "Elasticity at 11,500 by 60 granularity?" | Partial pooling cuts RMSE by 66% against per-cell estimates, and shrinkage kills 25 phantom insights a naive dashboard would flag |
| [N7_card_vs_cash_cannibalisation](N7_card_vs_cash_cannibalisation.ipynb) | "Card against cash. Cannibalisation or halo?" | A +41% gross uplift is 45% cannibalised and roughly flat at portfolio level. A blanket cut loses even as a defence, while a targeted retention cut wins |
| [N9_safe_exploration_consumer_duty](N9_safe_exploration_consumer_duty.ipynb) | "Bandits under FCA regulation?" | The fee corridor costs 1.6% in steady state and out-learns the unconstrained bandit. Endogeneity creep is shown three ways, and a 5% exploration stream restores identification for under 1% tax |

## Tier 3

| Notebook | Panel question | Headline result |
|---|---|---|
| [N8_competitor_response_game](N8_competitor_response_game.ipynb) | "A competitor opens next to 50 branches" | Promotional means hold, structural means targeted defence. Matched-control difference in differences says -8.6% against a naive -4.5%, where the truth is -8% |
| [N10_heterogeneous_elasticity_dml](N10_heterogeneous_elasticity_dml.ipynb) | "Customer level elasticity, and when not to bother" | Pooled OLS says -8.0 where the truth is -1.6. Cross-fitted double ML recovers the real curve, and a three segment split gets about the same answer, which is the simplicity premium |
| [N11_fx_repricing_runbook](N11_fx_repricing_runbook.ipynb) | "Sterling drops 5% overnight" | Hedge book first at £0.23m exposure, then rebase margin in bps because a stale rate costs 74bps, channel latency costs £106k, honour the locked click and collect book, and follow the T+0 to T+24h runbook |

## The question bank

[interview_qa_bank.md](interview_qa_bank.md) collects the best questions from the
whole folder with short model answers. Drill them out loud rather than reading them.

## Build and rebuild

The notebooks are generated from percent-format Python in [src/](src/). `_build.py`
converts and executes them, so figures and printed results are embedded:

```bash
python _build.py src/N4_uncertainty_to_decision.py     # one notebook
for f in src/N*.py; do python _build.py "$f"; done     # all, about two minutes
```

`_style.py` holds the shared chart palette and puts [../engine](../engine/) on the
import path, so the notebooks import the case study engine directly and never
reimplement it.

## How to rehearse

Read the panel question at the top and say your answer aloud, cold. Then run the
notebook and watch the naive method fail and the fix recover the truth. Then read the
sixty second answer aloud, timed, until it is yours. Finish with the deeper
follow-ups.

Every figure in these notebooks is simulated and directional. They demonstrate
method, not FRES's actual economics. Say that in the room.
