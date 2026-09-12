# 02 · Prove the change

Showing that a price change did what you say it did. This is the technical spine of
the role and the part a Head of Data will push hardest on.

Steps are numbered as in the [track](../README.md). Lab 2.1 was already run at step
5, because it builds the world every other lab reads. If you have not run it, do
that first: it takes about a minute and writes every table into `../data/`.

## The steps

| Step | Do this | What it teaches | Done when you can |
|---|---|---|---|
| 11 | Read [2.1 Averages and uncertainty](01_averages_and_uncertainty.md) | Mean against median, spread, confidence intervals, expected value | Explain why a range crossing zero is not "no effect", and frame the decision as expected value |
| 12 | Run [lab 2.2](lab_02_statistical_foundations.ipynb) | Distributions, how averages lie, sampling error, the bootstrap, power and minimum detectable effect, regression to the mean | Size a test from the noise in the data |
| 13 | Read [2.2 Tests and experiments](02_tests_and_experiments.md) | Control groups, randomisation, power, spillover | Design a control group and name the neighbour problem |
| 14 | Run [lab 2.3](lab_03_regression_for_pricing.ipynb) | OLS and logistic regression as pricing tools, omitted variable bias, why the grain you aggregate to changes the answer, fixed effects | Say why the grain changes the answer |
| 15 | Run [lab 2.4](lab_04_experiments_and_ab_testing.ipynb) | Randomisation, the real A/B test hidden in the data, metric choice, variance reduction, peeking, guardrails | Analyse the A/B test without peeking |
| 16 | Read [2.3 Causal inference primer](03_causal_inference_primer.md) | Confounders, endogeneity, instruments, controls, colliders, and the methods catalogue at the back | Explain why the desk's own pricing rule is the confounder, and what an instrument is |
| 17 | Run [lab 2.5](lab_05_causal_inference.ipynb) | DAGs, difference in differences across 12 regions, instrumental variables including a deliberately flawed one, double machine learning, bad controls | Recover a true effect two ways and say which assumption each leans on |
| 18 | Run [lab 2.6](lab_06_causality_segments_competition.ipynb) | The residual on residual trick that scales into DML, segment level answers, the randomised branch test that settles it | Do residual on residual by hand |
| 19 | Read [2.4 Forecasting and stockouts](04_forecasting_and_stockouts.md) | Forecasting, censored demand, the stockout death spiral | Describe the spiral and how to get out of it |

Then loop back to [stage 1](../01_set_the_rate/) for step 20, lab 1.3.

## Why this stage exists

The dataset contains, on purpose, a randomised online A/B test with known potential
outcomes, a non-randomised promotion across four regions for difference in
differences, a badly designed 2024 regional trial that could never have worked, an
imperfect instrument, marketing campaigns that confound regional analysis, and
complaints as a worked example of a collider.

The answer key in `../data/truth.json` holds the real elasticities, the real
switching coefficient and the real effects. Estimate first, then check. That loop is
the lesson, more than any single technique.

## Where the ideas go

The identification you learn here is what makes the numbers in stage 3 defensible,
and the exploration problem it creates under regulation is handled in stage 4 and in
panel notebook N9. Panel notebooks N1, N3, N4 and N10 are the interview-grade
versions of this stage, and N4 is the single most valuable answer in the folder.
