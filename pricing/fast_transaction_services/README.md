# Pricing, Distribution & Revenue — Travel Money, Prepaid Cards & Fast Transactions

A self-contained, **runnable** case study on **price-elasticity estimation,
distribution economics, FCA Consumer Duty fair value, dynamic pricing and AOP
scenario modelling.** It comes in two layers that share one engine:

> 📚 **Conceptual companion:** the
> [**pricing school**](../pricing_school/00_START_HERE.md) explains every principle
> behind this code — foundations in files 01–15, and the senior reference (strategy,
> channel economics, Consumer Duty, behavioural pricing, AOP, KPIs, governance) in
> files 18–21. Where this case study *shows* a technique, the school gives the theory,
> formula and senior-level judgement.

### 🅰 Role-aligned layer — Travel money & prepaid FX cards (start here for the role)

Built for the **Senior Manager, Pricing, Distribution & Revenue** remit
(multi-channel travel money + prepaid cards, Post Office / TMC / digital / agency,
under FCA Consumer Duty).

- 📘 **[`travel_money_pricing_case_study.md`](travel_money_pricing_case_study.md)** — the domain write-up.
- 🎯 **[`JD_alignment.md`](JD_alignment.md)** — every JD bullet mapped to a file/figure, + 5 interview stories.
- 📊 **[`ROLE_RESULTS.md`](ROLE_RESULTS.md)** & **[`FAIR_VALUE_ASSESSMENT.md`](FAIR_VALUE_ASSESSMENT.md)** — auto-generated.
- ▶️ Run: `python run_role_case_study.py`

| File | Role pillar |
|---|---|
| `travel_money_simulator.py` | 5 channels, FX margin, card lifecycle, competitor margins, fair-value portfolio |
| `distribution_economics.py` | Channel P&L, margin waterfall, competitive positioning, margin support |
| `fair_value.py` | FCA Consumer Duty (PRIN 2A.4) fair value assessment + vulnerable-customer harm |
| `aop_scenario.py` | AOP revenue build-up, scenario analysis, competitor price index & sensitivity |

### 🅱 Methods layer — Real-time payments ("FastPay")

The general elasticity + dynamic-pricing engine, demonstrated on a payments
platform. The role layer reuses this engine.

It demonstrates, with code and figures, the two ideas a senior pricing data
scientist is expected to nail:

1. **Elasticity must be estimated *causally*.** Naive log-log OLS is badly biased
   when the firm sets price in response to demand (surge). An instrumental-variable
   approach recovers the true demand curve.
2. **Dynamic pricing beats a flat fee** when cost-to-serve rises with load — and
   you can either hand-build a guarded surge rule or *learn* the policy online with
   contextual bandits.

## Read this first

📘 **[`dynamic_pricing_and_elasticity_case_study.md`](dynamic_pricing_and_elasticity_case_study.md)** —
the full written explanation (theory → identification → optimisation →
production), with an interview Q&A and references. Start here.

📊 **[`RESULTS.md`](RESULTS.md)** — auto-generated numerical results + figures.

## Run it

```bash
pip install -r requirements.txt
python run_case_study.py          # ~5 seconds; writes images/ and RESULTS.md
```

Each module also runs on its own as a quick self-test:

```bash
python fast_txn_simulator.py      # generate + summarise the synthetic panel
python elasticity_models.py       # OLS vs IV elasticity, per segment
python dynamic_pricing.py         # static vs surge vs bandits on one segment
```

## Files

| File | Role |
|---|---|
| `fast_txn_simulator.py` | Synthetic real-time-payments panel with **known** ground-truth elasticity, surge-style (endogenous) fee setting, and a cost-shock **instrument**. |
| `elasticity_models.py` | Elasticity estimators: two-point (point/arc), **naive OLS** (biased), **IV/2SLS** (causal, with first-stage F), and per-segment comparison vs truth. |
| `dynamic_pricing.py` | Lerner optimal fee, a calibrated live `TxnPricingEnv` (cost rises with load), a guarded **surge controller**, and **Thompson-sampling / ε-greedy** contextual bandits + a simulation harness. |
| `run_case_study.py` | End-to-end pipeline → console report, four figures in `images/`, and `RESULTS.md`. |
| `dynamic_pricing_and_elasticity_case_study.md` | The full explainer (the main deliverable). |

## Headline results (reproducible, fixed seed)

* Consumer elasticity: **OLS −1.15** vs **IV −1.88** vs **true −1.90**; the
  *pooled* OLS estimate is **+0.40** (wrong sign — pure endogeneity).
* Pricing on the biased OLS elasticity over-charges (4.0% vs optimal 1.2%) and
  **loses ~45% of profit**.
* Load-aware **dynamic pricing lifts profit ~19%** over a flat fee; contextual
  bandits learn that policy online, reaching ~91–95% of an omniscient oracle.

## Dependencies

`numpy`, `pandas`, `matplotlib` are all that's required to run the case study
(`scikit-learn`, `scipy`, `statsmodels` are listed for optional extensions). The
code deliberately avoids heavyweight econometrics packages so it runs anywhere.
