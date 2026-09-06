# Dynamic Pricing & Elasticity Modelling for a Fast Transaction Service

A complete, end-to-end explanation — theory, causal identification, optimisation,
and a runnable case study — built around **"FastPay"**, a real-time
money-movement / instant-payments platform. The lever is the **instant-transfer
fee** (a percentage of the transaction); the outcomes are **paid instant
volume** and **profit**.

This document is the narrative; the maths is made concrete by four small,
dependency-light Python modules in this folder that you can run in ~5 seconds:

| File | What it does |
|---|---|
| `fast_txn_simulator.py` | Generates a realistic payments panel with a **known** ground-truth elasticity, surge-style (endogenous) fee setting, and a cost-shock instrument. |
| `elasticity_models.py` | Estimates elasticity: two-point, **naive OLS (biased)**, **IV/2SLS (causal)**, and per-segment. |
| `dynamic_pricing.py` | Turns elasticity into price (Lerner optimum), plus a **rule-based surge** controller and **contextual bandits** (Thompson sampling, ε-greedy). |
| `run_case_study.py` | Runs the whole pipeline, prints results, and writes the figures + `RESULTS.md`. |

> **TL;DR of the results** (reproducible, fixed seed):
> * Naive OLS estimates a consumer elasticity of **−1.15** (and a *pooled* elasticity of **+0.40** — wrong sign!); IV/2SLS recovers **−1.88** against a true **−1.90**.
> * Setting the fee from the biased OLS elasticity **over-charges** (4.0% vs the optimal 1.2%) and **throws away ~45% of profit**.
> * Load-aware **dynamic pricing lifts profit ~19%** over a flat fee, and contextual bandits learn that policy online.

---

## 1. Why "fast transaction services" is a dynamic-pricing problem

A fast transaction service (instant payments, card processing, FX, ride-hailing
dispatch, quick-commerce checkout) has four properties that make pricing both
high-stakes and hard:

1. **High velocity & low margin.** Millions of transactions, cents of margin
   each. A 1% pricing error is enormous in aggregate, so getting elasticity
   right matters.
2. **Real-time, fluctuating load.** Demand has strong time-of-day / day-of-week
   structure plus shocks (paydays, sales events, outages at competitors). Near
   capacity, the *marginal cost to serve* rises (latency SLAs, fraud exposure,
   liquidity/float, infra). That is the economic reason to price dynamically.
3. **A free/slow alternative.** Customers can usually wait for the free rail
   (next-day ACH) — so the *instant* product is genuinely price-elastic, and the
   elasticity differs sharply by segment.
4. **A two-sided / networked market.** Fees affect both senders and receivers,
   merchants and consumers, and competitors react. Pricing is strategic, not
   just a single-firm optimisation.

The job splits into two questions:

* **Elasticity modelling** — *how does volume respond to the fee?* (a causal
  question about a demand curve).
* **Dynamic pricing** — *given that response, what fee should I charge right now,
  for this segment, at this load?* (an optimisation + control question).

You cannot do the second well without doing the first honestly. The rest of this
document does both.

---

## 2. Price elasticity of demand — the foundations

### 2.1 Definition

Price elasticity of demand is the **percentage change in quantity demanded per
one-percent change in price**:

$$\varepsilon \;=\; \frac{\partial Q / Q}{\partial P / P} \;=\; \frac{\partial \log Q}{\partial \log P}.$$

Because demand curves slope down, $\varepsilon < 0$. Vocabulary:

| Regime | $\lvert\varepsilon\rvert$ | Meaning | Pricing implication |
|---|---|---|---|
| **Elastic** | $> 1$ | volume reacts more than price | cutting price can grow revenue; don't over-charge |
| **Unit elastic** | $= 1$ | revenue flat in price | revenue-neutral |
| **Inelastic** | $< 1$ | volume reacts less than price | raising price grows revenue (pricing power) |

In our case study the **consumer** segment is elastic (−1.9: they'll wait for the
free rail), while **enterprise payouts** are inelastic (−0.85: time-critical, low
substitutability → pricing power).

### 2.2 Point vs arc elasticity (the two-point formulas)

For a discrete A/B price change from $(P_0,Q_0)$ to $(P_1,Q_1)$:

* **Point elasticity** (anchored at the base point): $\dfrac{(Q_1-Q_0)/Q_0}{(P_1-P_0)/P_0}$
* **Arc / midpoint elasticity** (symmetric to direction): $\dfrac{(Q_1-Q_0)/\bar{Q}}{(P_1-P_0)/\bar{P}}$ with $\bar{X}=(X_0+X_1)/2$.

Use **arc** when comparing a price increase vs decrease (it gives the same number
both ways); use **point** for marginal/local reasoning. Both are in
`elasticity_models.py` (`point_elasticity`, `arc_elasticity`).

### 2.3 The constant-elasticity (log-log) demand model

The workhorse model assumes elasticity is constant over the relevant range:

$$Q = A\,P^{\varepsilon}\quad\Longleftrightarrow\quad \log Q = \log A + \varepsilon \log P.$$

Take logs and it's **linear**, so $\varepsilon$ is just the slope of a regression
of $\log Q$ on $\log P$. That is why "log-log regression" is the default
elasticity tool. (Alternatives: **linear demand** $Q=a-bP$ where elasticity
varies along the curve; **logit/multinomial-logit** demand when you model the
*share* choosing instant vs the free rail — the right choice when there is a
discrete substitution.)

### 2.4 Own vs cross vs other elasticities

* **Own-price elasticity** — response of a product's own demand to its own price
  (our focus).
* **Cross-price elasticity** — response to a *competitor's* fee (or to the price
  of the free rail). Positive for substitutes. Critical in payments because the
  free/slow rail is the substitute that caps your fee.
* **Income / size elasticity** — response to transaction size or merchant scale.

---

## 3. The hard part: estimating elasticity *causally*

> **The core message.** You almost never get to see a clean demand curve in
> observational data, because **price is not set randomly** — it is set by a
> firm reacting to the very demand it is trying to measure. Naive regression then
> estimates a tangled mix of demand *and* supply behaviour, not the causal demand
> slope.

### 3.1 The endogeneity / simultaneity problem

In FastPay the fee is set partly by a **surge policy**: when latent demand $u$ is
high (payday, a competitor outage), the firm raises the fee. But high $u$ *also*
lifts volume directly. So in the data, **high-fee hours are also high-volume
hours**, and a regression of $\log Q$ on $\log P$ sees a slope that is biased
*upward* (toward zero, or even positive).

Formally, the structural system the simulator implements is:

$$
\begin{aligned}
\log Q_t &= \beta_0 + \varepsilon \,\log P_t + \delta\, u_t + \text{season}_t + \eta_t \qquad(\text{demand})\\
\log P_t &= \gamma_0 + \gamma_u\, u_t + \gamma_z\, z_t + \nu_t \qquad\qquad(\text{firm's fee policy})
\end{aligned}
$$

Because $\gamma_u>0$ and $u_t$ appears in the demand error, $\operatorname{Cov}(\log P_t, \text{error}) \neq 0$ → **OLS is inconsistent**. The bias is
$\operatorname{plim}(\hat\varepsilon_{OLS}) - \varepsilon \propto +\gamma_u\delta > 0$.

This is exactly what the code shows:

```
Pooled OLS elasticity : +0.395   <-- biased, even wrong-signed
Pooled IV  elasticity : -1.331
```

`fig1_endogeneity_scatter.png` is the picture: colour each point by the
(normally unobserved) demand shock and you can *see* that the OLS line through
the cloud is flatter than the true demand curve.

> **Sign intuition for interviews.** If your estimated elasticity is near zero or
> positive, you almost certainly have a *supply/endogeneity* problem, not an
> inelastic product. "Prices went up and so did sales" measures your own pricing
> reflex, not customer behaviour.

### 3.2 Fix #1 — Instrumental variables (IV / 2SLS)

Find a variable $z$ that **moves the fee but is independent of the demand shock**.
A *cost-side shock* is the classic instrument: per-transaction
processing/interchange cost shifts the fee the firm charges (cost pass-through)
but does not change a customer's willingness to pay except *through* the fee.

A valid instrument needs:

1. **Relevance** — $z$ genuinely moves $P$ (testable: first-stage $F\gg 10$).
2. **Exclusion** — $z$ affects $Q$ *only* through $P$ (an assumption, argued from
   domain knowledge, not testable directly).

**Two-stage least squares (2SLS):**
* *Stage 1*: regress $\log P$ on $z$ (+ controls) → fitted $\widehat{\log P}$.
* *Stage 2*: regress $\log Q$ on $\widehat{\log P}$ (+ controls). The slope is the
  causal elasticity.

In `elasticity_models.py` this is `iv_2sls_elasticity` (with proper 2SLS standard
errors via the projection form, and a `first_stage_strength` relevance check).
The result is decisive:

| Segment | True ε | OLS ε | IV ε | First-stage F |
|---|---:|---:|---:|---:|
| consumer | −1.90 | −1.15 | **−1.88** | 2,192 |
| smb | −1.35 | −0.72 | **−1.34** | 3,314 |
| enterprise | −0.85 | −0.44 | **−0.86** | 6,884 |

OLS understates sensitivity by ~40–50%; IV lands within ~0.02 of the truth, with
a very strong first stage. See `fig2_elasticity_estimates.png`.

Other instruments used in practice: **lagged prices**, **taxes/levies**,
**competitor cost shocks**, **input/FX cost**, **Hausman instruments** (prices of
the same product in other markets that share cost but not local demand).

### 3.3 Fix #2 — Randomised experiments (the gold standard)

If you can randomise the fee, price *is* exogenous and OLS is unbiased by
construction. For fast transaction services the practical designs are:

* **Customer-level A/B holdouts** — randomise small fee deltas across users.
  Clean, but the network/market-level equilibrium effects are missed.
* **Geo / switchback experiments** — randomise the price *over time* within a
  market (alternating on/off in short windows). Standard at ride-hailing and
  delivery platforms because pricing affects the shared marketplace, so you must
  randomise the *market-time*, not the user.
* **Price experiments as instruments.** Even a *partial*, encouragement-style
  experiment gives you an exogenous shifter you can use as an instrument.

Experiments are the cleanest source of the variation IV is trying to mimic; in
production you typically run *both* — experiment where you can, IV/observational
where you can't.

### 3.4 Fix #3 — Panel / fixed-effects & difference-in-differences

With repeated observations per segment/market you can absorb stable confounders:

* **Fixed effects** for segment, hour-of-day, day-of-week soak up predictable
  demand structure (we include a `season` control throughout).
* **Difference-in-differences** around a fee change in some markets but not
  others identifies the effect off the *change*, under a parallel-trends
  assumption.

Fixed effects handle *observed/structural* confounders; they do **not** fix the
*simultaneity* with the unobserved shock $u$ — that still needs IV or
randomisation. (A frequent interview trap: "just add controls." Controls remove
confounding you can measure; they cannot remove the endogeneity from an
unobserved demand shock the price reacts to.)

### 3.5 Fix #4 — Double/Debiased ML & causal forests (heterogeneous elasticity)

Elasticity is not one number — it varies by customer, ticket size, time, and
tenure. To estimate a **conditional** elasticity $\varepsilon(x)$ (a CATE on a
continuous treatment) without hand-specifying every interaction:

* **Double / Debiased ML (DML)** (Chernozhukov et al., 2018): use flexible ML to
  predict the outcome and the treatment from covariates, *partial both out*
  (orthogonalisation), then estimate the price effect on the residuals. The
  Neyman-orthogonal moment makes the estimate robust to small ML errors in the
  nuisance models. Pair it with an instrument when price is endogenous.
* **Causal forests / Generalized Random Forests** (Athey & Wager): honest trees
  on the residualised data give $\varepsilon(x)$ with valid confidence intervals,
  and naturally surface *who* is most price-sensitive — exactly what you need for
  segment- and personalised pricing.

DML works well precisely because price is *continuous* (it's the canonical
continuous-treatment use case). Our per-segment IV in §3.2 is a simple, fully
transparent stand-in for "estimate a heterogeneous elasticity"; DML is how you'd
scale that to hundreds of features in production.

### 3.6 A practical estimation checklist

1. Plot $\log Q$ vs $\log P$ and colour by candidate confounders. If the slope
   looks "too flat," suspect endogeneity.
2. State your identification strategy *before* modelling: experiment? instrument?
   panel variation? What makes price move *for reasons unrelated to demand*?
3. Validate the instrument: first-stage $F$, and argue exclusion from domain
   knowledge.
4. Estimate heterogeneity (by segment first, then DML/causal forest).
5. Sanity-check signs and magnitudes against a holdout *experiment*.
6. Quantify the **decision** sensitivity (next section), not just the parameter.

---

## 4. From elasticity to price — the optimisation

### 4.1 The profit-maximising fee (Lerner rule)

Per transaction, revenue is $p = f \cdot \text{ticket}$ (fee × ticket size) and
marginal cost-to-serve is $c$. With constant-elasticity demand $Q(p)=Kp^{\varepsilon}$, profit $\pi=(p-c)Q(p)$ is maximised where marginal revenue
equals marginal cost, giving the **Lerner condition**:

$$\boxed{\;\frac{p^\* - c}{p^\*} = -\frac{1}{\varepsilon}\;}\qquad\Longrightarrow\qquad p^\* = \frac{c}{1 + 1/\varepsilon}.$$

The optimal **markup is the inverse of elasticity**: the more elastic demand, the
thinner the margin you can hold. Two consequences pricing analysts must internalise:

* **It only has an interior solution when demand is elastic** ($\varepsilon<-1$).
  For *inelastic* segments (enterprise, $\varepsilon=-0.85$) the formula says
  "raise price without bound" — in reality the binding constraint is **competition
  and the free-rail substitute**, *not* the first-order condition. That is a
  corner solution, handled explicitly in `lerner_optimal_fee` (`corner_solution=True`).
* **In low-margin payments, naive marginal-cost markup under-prices.** The real
  fee also has to recover fraud, support, capital, compliance and fixed cost, and
  reflect *value* delivered (speed). We model this with a **fully-loaded
  contribution cost** rather than the raw processing cost (`TxnPricingEnv.calibrated`).

### 4.2 Why a biased elasticity is *expensive*, not just *wrong*

The headline practical result. The OLS elasticity for the consumer segment
(−1.15) makes demand look much more inelastic than it is, so the markup rule says
"charge more." Following it pushes the fee to the **4.0% cap** when the true
profit-maximising fee is **1.2%**:

```
Optimal fee from TRUE elasticity :  1.20%  → profit/period $14,211
Optimal fee from IV   elasticity :  1.21%  → profit/period $14,209   (≈ truth)
Optimal fee from OLS  elasticity :  4.00%  → profit/period  $7,838   (45% profit LOST)
```

`fig3_profit_curve.png` shows it geometrically: the biased estimate walks you off
the top of the profit hill. **The causal question is not academic — it changes the
decision and ~halves the profit.** Always report the *decision* sensitivity to the
elasticity estimate, not just a confidence interval on $\varepsilon$.

### 4.3 Constrained & multi-objective pricing

Real fee optimisation is constrained:

* **Floors/caps** (regulatory, contractual, brand), **competitive ceilings** (the
  free rail and rival fees), **fairness caps** (see §6).
* **Multi-objective**: profit *and* market share / network growth. In two-sided
  markets you may price one side near cost to grow the other (interchange-style
  cross-subsidy). Express as $\max \;\pi + \lambda\cdot(\text{growth})$ or as a
  constrained optimisation.

---

## 5. Dynamic pricing — pricing in real time

### 5.1 What makes it *dynamic*, and why it pays

A subtle but crucial point: **with constant elasticity and constant marginal
cost, the profit-maximising price does not depend on the demand level.** Surging
just because demand is high would be leaving the static optimum for no reason.
Dynamic pricing is justified when one of these holds:

1. **Marginal cost rises with load** (congestion, capacity, SLA, fraud, float).
   Then the optimal fee genuinely rises at peak — and pricing also *sheds* demand
   to protect the system. *This is the mechanism we model* (`congestion_kappa`):
   `fig4_dynamic_pricing.png` panel (d) shows the optimal fee climbing with load.
2. **Elasticity varies with state** (peak users are less willing to wait → less
   elastic), so the optimal markup changes.
3. **Inventory/perishability or commitments** (finite capacity in a window).

For FastPay, (1) is the cleanest economic justification and ties pricing to
**load management**, which is what a payments platform actually needs.

### 5.2 Strategy ladder

**(a) Rule-based surge with guardrails** (`SurgeController`).
A transparent controller: `fee = base_fee × surge_multiplier(load)`, where the
multiplier rises with load. Production guardrails are *part of the algorithm*:

* a **fee floor and cap** (never below cost-plus-floor, never above the
  competitive/fairness ceiling);
* a **surge cap** (the multiplier itself is capped);
* a **per-step rate limit** (the fee can't move more than X% between periods).

The rate limit is what prevents **oscillation and "price-war" whipsaw** — a real
failure mode when algorithms react to each other. In the simulation this simple,
auditable rule reaches **95.7% of the oracle** and lifts profit **~19%** over the
flat fee.

**(b) Optimisation-based / model-predictive.** Re-estimate the demand curve and
cost-to-serve each interval and solve the constrained optimum directly (§4). More
optimal than a fixed rule, but only as good as the live demand model, and harder
to audit.

**(c) Learning controllers — contextual bandits.** When you *don't* know the
cost/demand structure, **learn it online**:

* **Thompson sampling** (`ThompsonBanditController`): keep a Bayesian posterior on
  expected profit for each (load-context, fee-arm); sample from each posterior and
  play the best draw. Exploration falls out of the posterior uncertainty
  automatically. Used in this family by Walmart Labs and ride-hailing platforms.
* **ε-greedy** (`EpsilonGreedyController`): exploit the best-known fee, explore at
  random with probability ε. Simple, surprisingly strong.

Both learn a *load-aware* policy from rewards alone and reach **~91–95% of the
oracle** here — without ever being told the cost structure. Panels (a)/(b) of
`fig4_dynamic_pricing.png` show their cumulative profit and *regret* converging.

**(d) Reinforcement learning.** When today's price changes *tomorrow's* demand
(retention, reference-price effects, learning customers), the problem is
sequential and a full RL/contextual-MDP formulation is warranted. Bandits are the
right tool when periods are (approximately) independent; RL when they're not.

### 5.3 The exploration–exploitation trade-off

Every adaptive pricer must spend some traffic *learning* (exploration) to earn
more later (exploitation). Bandit **regret** (the gap to the oracle) is the
principled way to budget that: panel (b) shows the static policy's regret growing
linearly (it never learns) while the learners' regret flattens. In production you
cap exploration with the same guardrails (§6) so customers never see an absurd
price during learning.

---

## 6. Production realities: guardrails, fairness, feedback, monitoring

Dynamic pricing fails in characteristic ways. Design against them up front:

* **Feedback loops & oscillation.** Algorithms reacting to each other (or to their
  own past prices via reference effects) can spiral. → rate limits, hysteresis,
  damping, and *price change budgets*.
* **Fairness & trust.** Congestion surges fall hardest on price-sensitive users;
  in essential services this is an equity and reputational risk. → surge caps,
  protected floors, transparency about *why* the price moved, and excluding
  protected attributes. There is active research on *envy-free* and
  *utility-fair* dynamic pricing.
* **Cannibalisation.** A lower instant fee can pull volume from a more profitable
  adjacent product (or from your own future periods). → optimise *portfolio*
  contribution, not a single SKU.
* **Endogeneity creep.** Once a model sets prices, your logs are no longer
  experimental — tomorrow's elasticity estimate inherits today's policy. → keep a
  **randomised holdout / exploration stream** permanently on, to retain a clean
  source of identification.
* **Drift & monitoring.** Elasticity moves with the economy and competition.
  Monitor input drift (PSI/KS on fee, ticket, mix), the **first-stage strength**
  of your instrument, realised-vs-predicted volume, and *decision* drift (are
  recommended fees creeping toward the cap?). Alert and fall back to a safe static
  fee on anomaly.
* **Latency & robustness.** At transaction speed the pricer is in the critical
  path: it needs millisecond inference, graceful degradation to a cached/static
  fee, and circuit breakers.

---

## 7. The case study, end to end

`run_case_study.py` stitches the whole argument together and is fully
reproducible:

1. **Simulate** 8,640 hourly observations × 3 segments of FastPay history, with a
   known elasticity, surge-style endogenous fees, and a cost-shock instrument.
2. **Estimate** elasticity by OLS (biased) and IV/2SLS (causal) per segment, and
   score against ground truth → `fig1`, `fig2`.
3. **Optimise** the fee, and quantify the profit lost by pricing on the biased
   elasticity → `fig3`.
4. **Price dynamically**: compare a flat fee, a guarded surge rule, and two
   contextual bandits against a load-aware oracle → `fig4`, `RESULTS.md`.

Run it:

```bash
pip install numpy pandas matplotlib scikit-learn scipy statsmodels
python run_case_study.py        # ~5s; writes images/ and RESULTS.md
```

Each module also has a `__main__` self-test you can run on its own.

---

## 8. Interview-ready Q&A

**Q. Your elasticity came out positive. What happened?**
Almost certainly endogeneity: price is set in response to demand (surge / demand
forecasting), so OLS conflates the demand curve with the pricing policy. Fix with
an experiment or a cost-side instrument; the sign should flip negative. (Here:
OLS +0.40 → IV −1.33.)

**Q. What makes a good instrument for price?**
Relevant (moves price; first-stage F ≫ 10) and excludable (affects demand only
through price). Cost/interchange shocks, input/FX costs, taxes, lagged prices,
Hausman (other-market) prices. Exclusion is an *argument from domain knowledge*,
not a test.

**Q. Adding controls vs IV — when is each enough?**
Controls/fixed effects remove confounding you can *measure*. They do **not**
remove simultaneity with an *unobserved* shock the price reacts to — that needs
IV or randomisation.

**Q. When is dynamic pricing actually optimal (vs a fixed price)?**
When marginal cost rises with load (congestion/capacity), when elasticity varies
with the demand state, or with perishable/finite inventory. With constant
elasticity *and* constant marginal cost, the static optimum is also the dynamic
optimum.

**Q. Bandit vs RL for pricing?**
Bandits when periods are ~independent (today's price doesn't move tomorrow's
demand). RL when there are dynamics — retention, reference-price effects, learning
customers — i.e. a sequential decision problem.

**Q. Thompson sampling vs ε-greedy?**
Both balance explore/exploit. TS explores in proportion to posterior uncertainty
(usually lower regret, no ε to tune); ε-greedy is simpler and robust. Cap
exploration with guardrails either way.

**Q. How do you keep elasticity estimable once a model is pricing?**
Maintain a permanent randomised exploration/holdout stream so you always have a
clean, experimental source of price variation — otherwise the policy contaminates
all future identification.

**Q. The model says raise the fee to the cap. Do you?**
Check first: is the segment genuinely inelastic, or is the elasticity biased
toward zero (endogeneity)? A corner solution at the cap is a red flag to validate
with an experiment before shipping.

---

## 9. References & further reading

Causal identification & elasticity
* Chernozhukov et al. (2018), *Double/Debiased Machine Learning for Treatment and Structural Parameters* — [arXiv:1608.00060](https://arxiv.org/abs/1608.00060)
* Athey & Wager, *Generalized Random Forests / Causal Forests* — [GRF for marketplaces, arXiv:2203.10975](https://arxiv.org/pdf/2203.10975)
* *Dealing with Endogeneity: A Nontechnical Guide for Marketing Researchers* — [Springer](https://link.springer.com/rwe/10.1007/978-3-319-05542-8_8-1)
* *Estimating Models of Supply and Demand: Instruments and Covariance Restrictions* — [PDF](https://alexandermackay.org/files/Estimating%20Models%20of%20Supply%20and%20Demand.pdf)
* Price elasticity via IV (applied) — [Electricity demand, arXiv:2306.12863](https://arxiv.org/pdf/2306.12863)
* *Heterogeneous Treatment Effect using Double Machine Learning* — [Towards Data Science](https://towardsdatascience.com/heterogeneous-treatment-effect-using-double-machine-learning-65ab41f9a5dc/)

Dynamic pricing, bandits & RL
* *Thompson Sampling for Dynamic Pricing* — [arXiv:1802.03050](https://arxiv.org/pdf/1802.03050)
* *On Dynamic Pricing with Covariates* (contextual) — [arXiv:2112.13254](https://arxiv.org/pdf/2112.13254)
* *Survey of dynamic pricing based on Multi-Armed Bandit algorithms* — [ResearchGate](https://www.researchgate.net/publication/378435403_Survey_of_dynamic_pricing_based_on_Multi-Armed_Bandit_algorithms)
* *Dynamic Pricing with Multi-Armed Bandits: Learning by Doing* — [Medium / TDS](https://medium.com/data-science/dynamic-pricing-with-multi-armed-bandit-learning-by-doing-3e4550ed02ac)
* `awesome-dynamic-pricing` reading list — [GitHub](https://github.com/DallasBuyer/awesome-dynamic-pricing)

Fairness, guardrails & pitfalls
* *Utility Fairness in Contextual Dynamic Pricing with Demand Learning* — [arXiv:2311.16528](https://arxiv.org/pdf/2311.16528)
* *Robust Dynamic Pricing and Admission Control with Fairness Guarantees* — [arXiv:2603.17764](https://arxiv.org/pdf/2603.17764)
* *Algorithmic Pricing — guardrails framework* — [Umbrex](https://umbrex.com/resources/frameworks/pricing-frameworks/algorithmic-pricing/)

Classics
* Talluri & van Ryzin, *The Theory and Practice of Revenue Management*.
* Pearl, *Causality*; Cunningham, *Causal Inference: The Mixtape*.
