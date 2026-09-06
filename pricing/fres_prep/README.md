# FRES Prep Notebooks — the interview programme, executed

The notebook programme specified in
[`../../interview/FRES_MASTER_PREP_PROMPT.md`](../../interview/FRES_MASTER_PREP_PROMPT.md)
(Part 5), built on the case-study engine in
[`../fast_transaction_services/`](../fast_transaction_services/).

Every notebook obeys one contract: **simulate known ground truth → show the
naive method failing → apply the fix → prove recovery → end with
`## The 60-second answer`** (the verbatim spoken script) and
`### What I'd say if pushed deeper` (three follow-ups, always including one
honest limitation).

## Tier 1 — highest differentiator per hour

| Notebook | Panel question | Asked by | Headline result |
|---|---|---|---|
| [N4_uncertainty_to_decision](N4_uncertainty_to_decision.ipynb) | "+2% margin, CI crosses zero — did it work?" | CRO/CCO | A true +2% "fails" significance 65% of the time at this design; P(accretive)=93%, EV £1.1m/yr, extending the test has *negative* value of information → roll out with monitoring |
| [N5_pocket_price_waterfall](N5_pocket_price_waterfall.ipynb) | "8 weeks to show quick wins" | CRO/CCO | Headline 500bps → pocket 435bps; £1.6m/yr recoverable leakage; +1% realised price = **+11.1%** operating profit (computed, not quoted); holdout DiD 0.73% vs naive over-claim 3.56% |
| [N1_geo_experiment_design](N1_geo_experiment_design.ipynb) | "Design a margin test across the estate" | Head of Data | Cross-shopping ~doubles measured lift vs truth; TTWA clustering + buffer sweep fixes it; MDE table (5bps invisible to a 50-branch pilot); CUPED −55% MDE; synthetic control recovers −6.0% to −5.96% |
| [N3_censored_demand_stockouts](N3_censored_demand_stockouts.ipynb) | "Euros stock out every Friday — pricing or ops?" | Head of Data + Product | Naive forecast understates Friday demand 40% and spirals stock 33k→21k; censored MLE recovers truth within ~4%; same policy + fixed forecast arrests the spiral |
| [N6_channel_differential_fair_value](N6_channel_differential_fair_value.ipynb) | "Click-&-collect undercuts walk-up" / "Evidence airport fair value" | CRO/CCO | Within-channel fairness check passes while the **mix** hides +1.33pp vulnerable-customer premium; favourable-subset benchmarking vs full market; airport as distinct target market with MAG cost stack |

## Tier 2

| Notebook | Panel question | Headline result |
|---|---|---|
| [N2_hierarchical_elasticity](N2_hierarchical_elasticity.ipynb) | "Elasticity at 11,500 × 60 granularity?" | EB partial pooling cuts RMSE 66% vs per-cell; shrinkage kills 25 phantom "insights" a naive dashboard flags |
| [N7_card_vs_cash_cannibalisation](N7_card_vs_cash_cannibalisation.ipynb) | "Card vs cash — cannibalisation or halo?" | +41% gross uplift is 45% cannibalised and ~flat at portfolio level; blanket cut loses even as defence; **targeted** retention cut wins |
| [N9_safe_exploration_consumer_duty](N9_safe_exploration_consumer_duty.ipynb) | "Bandits under FCA regulation?" | Fee corridor costs 1.6% steady-state and *out-learns* the unconstrained bandit; endogeneity creep shown 3 ways (bias −0.11 vs −1.90; rank-deficient frozen policy; ε=5% stream restores identification for <1% tax); OPE scores a policy from logs |

## Tier 3

| Notebook | Panel question | Headline result |
|---|---|---|
| [N8_competitor_response_game](N8_competitor_response_game.ipynb) | "Competitor opens next to 50 branches" | Promo → hold; structural → **targeted** defence (uses the engine's `margin_support_breakeven` per branch); matched-control DiD −8.6% vs naive −4.5% (truth −8%) |
| [N10_heterogeneous_elasticity_dml](N10_heterogeneous_elasticity_dml.ipynb) | "Customer-level elasticity — and when not to bother" | Pooled OLS −8.0 vs truth −1.6; interaction OLS bends; cross-fitted DML recovers ε(x); a 3-segment split gets ~the same answer (the simplicity premium) |
| [N11_fx_repricing_runbook](N11_fx_repricing_runbook.ipynb) | "Sterling drops 5% overnight" | Hedge book first (£0.23m exposure); margin-in-bps rebase (stale rate = −74bps margin); channel-latency costs £106k; honour the locked C&C book; T+0→T+24h runbook table |

## Build / rebuild

Sources are percent-format `.py` files in [`src/`](src/); `_build.py` converts
and **executes** them (figures and printed results are embedded):

```bash
python _build.py src/N4_uncertainty_to_decision.py     # one notebook
for f in src/N*.py; do python _build.py "$f"; done     # all (~2 min)
```

`_style.py` holds the shared chart palette and puts
`../fast_transaction_services` on `sys.path` — notebooks import the case-study
engine directly (`elasticity_models`, `dynamic_pricing`,
`distribution_economics`, `fair_value`, `travel_money_simulator`) and never
re-implement it.

## How to rehearse with these

1. Read the panel question at the top. Say your answer aloud, cold.
2. Run the notebook; watch the naive method fail and the fix recover truth.
3. Read `## The 60-second answer` aloud, timed. Repeat until it's yours.
4. Read `### What I'd say if pushed deeper` — the third item is always an
   honest limitation. Volunteering these is what signals seniority to the
   Head of Data.

All quantitative figures in these notebooks are **simulated and directional**
— they demonstrate method, not FRES's actual economics (see the Honesty Rule,
Part 6 of the master prompt).
