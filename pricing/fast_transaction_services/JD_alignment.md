# JD Alignment — Senior Manager, Pricing, Distribution & Revenue

How this case study maps, point by point, to the role's accountabilities and
required skills. Every claim is backed by runnable code, a figure, or a generated
document in this folder — so it doubles as an interview portfolio.

> **Domain match.** The role is travel money + prepaid FX cards sold across
> retail, TMC, digital, agency and the **Post Office / Postmaster** network, under
> **FCA Consumer Duty**. The case study is built on exactly that: FX **margin** is
> the price lever, channels carry different commission/cost economics, and a
> prepaid-card portfolio drives the fair-value work.

---

## 1. Business accountabilities → evidence

| JD accountability | Demonstrated by | Talking point |
|---|---|---|
| **Own enterprise-wide pricing strategy across retail, TMC, digital channels** | `travel_money_simulator.py` (5 channels), `distribution_economics.py::channel_positioning` | Channel-specific FX-margin strategy: compete where elastic (digital), harvest where inelastic (TMC, Post Office). |
| **Lead pricing tests, commercial trials & elasticity modelling** | `elasticity_models.py` (OLS vs IV/2SLS), `dynamic_pricing.py` (bandits/experiments) | I estimate elasticity *causally* — naive tests mislead because price is set in response to demand; I use instruments / experiments to get the true number. |
| **Margin modelling, margin support frameworks, revenue distribution across channels** | `distribution_economics.py::channel_pnl`, `margin_waterfall`, `margin_support_breakeven` | Per-channel margin waterfall (gross → Postmaster commission → cost → contribution) and a break-even test for when "margin support" is self-funding. |
| **Own channel distribution strategy & pricing architecture** | `distribution_economics.py`, `role_fig2_distribution.png` | The same FX margin yields very different *net* contribution by channel; pricing architecture must price the *net*, not the headline margin. |
| **Competitor monitoring & market intelligence** | `aop_scenario.py::competitive_index`, `competitor_sensitivity` | A live price index vs market + cross-elasticity sensitivity quantifying the revenue hit from a competitor price war. |
| **Product & channel pricing modelling and scenario analysis** | `aop_scenario.py::run_scenarios`, `revenue_bridge` | Elasticity-aware scenario engine + a revenue bridge that attributes change to volume / margin / competitor / mix. |
| **Manage AOP modelling for pricing revenue lines** | `aop_scenario.py::revenue_lines`, `run_scenarios`, `role_fig4_aop.png` | Annualised build-up by revenue line (new sales, reloads, in-life) and channel, flexed under a standard scenario set. |
| **Pricing strategy support for Postmasters / Post Office network** | Post Office channel in `travel_money_simulator.py` (45% commission) + waterfall | Quantifies the Postmaster payaway and its effect on the optimal Post Office margin. |
| **Ensure FCA Consumer Duty fair value compliance** | `fair_value.py`, `FAIR_VALUE_ASSESSMENT.md`, `role_fig3_fair_value.png` | A full price-vs-value assessment with vulnerable-customer differential-outcome testing and remediation actions. |
| **Provide pricing expertise & modelling to product/commercial/finance** | All modules + `ROLE_RESULTS.md`, `travel_money_pricing_case_study.md` | Translates models into clear commercial recommendations and documented evidence. |
| **Own P&L for TMC (new sales, reloads, in-life)** | `aop_scenario.py::revenue_lines` (line-level), `channel_pnl` | Revenue decomposed into the exact lines named in the JD. |

---

## 2. Principal-task skills → evidence

**Pricing & Revenue Management**
- *Pricing strategy, yield management, revenue optimisation* → dynamic/yield pricing in `dynamic_pricing.py` (surge by load), profit optimisation via the Lerner rule.
- *Building pricing models, elasticity analyses, margin scenarios* → `elasticity_models.py`, `distribution_economics.py`, `aop_scenario.py`.
- *Designing & evaluating pricing tests* → causal identification (`iv_2sls_elasticity`), online experimentation (contextual bandits), and the warning that uncontrolled tests are confounded.

**Distribution & Channel Economics**
- *Distribution economics across retail/digital/agency* → `channel_pnl`, `channel_positioning`.
- *Model & optimise multi-channel economics* → channel-specific optimal positioning given commission + cost-to-serve + elasticity.
- *Postmaster / franchise economics* → Post Office channel commission modelling.

**Regulatory & Compliance**
- *FCA Consumer Duty fair value for prepaid* → `fair_value.py` (PRIN 2A.4 framing), `FAIR_VALUE_ASSESSMENT.md`.
- *Regulatory pricing justifications & fair value documentation* → `generate_fair_value_assessment()` produces the documented assessment.
- *Competition law / pricing governance* → guardrails (caps/floors/rate-limits) in `dynamic_pricing.py`; the case study calls out collusion/parallel-pricing and fairness risks.

**Analytical & Technical**
- *Python, data modelling, scenario analysis, data viz* → all modules are Python (numpy/pandas/matplotlib); 8 figures generated.
- *SQL / R / Excel / BI (Power BI/Tableau)* → the panel/portfolio outputs are tidy tables ready for SQL warehousing and BI; see the "Productionising" note in the case study.
- *Translate complex models into clear commercial recommendations* → `ROLE_RESULTS.md`, `RESULTS.md`, and the recommendation columns (`recommended_move`, fair-value `status`).

---

## 3. Five interview stories this repo lets you tell

1. **"Our elasticity was wrong and it was costing us margin."** OLS said demand
   was inelastic (or even positively sloped) because we surge the FX margin in
   peak season; an IV/2SLS using a wholesale-cost instrument showed customers are
   far more price-sensitive (digital ε ≈ −2.2). Pricing on the biased number
   over-charges and loses ~45% of profit. *(`elasticity_models.py`)*

2. **"The headline FX margin lies about channel profitability."** The Post Office
   earns the highest gross revenue but pays ~45% away in Postmaster commission;
   digital drops 96% of revenue to contribution. I price the *net* and position
   each channel by its own elasticity. *(`distribution_economics.py`)*

3. **"Uniform price moves destroy value; targeted ones create it."** A blanket
   +10% FX margin *reduces* contribution (blended demand is elastic), but
   harvesting only the inelastic channels and competing in the elastic ones lifts
   it. *(`aop_scenario.py` vs `channel_positioning`)*

4. **"We found — and fixed — a Consumer Duty fair-value problem."** Vulnerable
   customers paid ~1.7pp more for lower benefit, driven by inactivity fees eroding
   unspent balances; I documented it and recommended fee caps and balance returns.
   *(`fair_value.py`, `FAIR_VALUE_ASSESSMENT.md`)*

5. **"I can defend the AOP under scrutiny."** Elasticity-aware scenarios and a
   revenue bridge that attributes every pound of change to volume, margin,
   competitor and mix — including the downside of a competitor price war.
   *(`aop_scenario.py`)*

---

## 4. Honest gaps / how I'd extend on the job

- **Real data & identification.** Swap the simulator for transaction data; secure
  identification with live **geo/switchback pricing experiments** plus the
  cost-shock instrument as a cross-check.
- **Heterogeneous elasticity at scale.** Move from per-channel IV to **double ML /
  causal forests** for customer-level elasticity (corridor, ticket size, tenure).
- **Two-sided / Post Office incentives.** Model Postmaster commission as a
  *strategic* lever (does a higher payaway buy enough footfall/volume to pay for
  itself?).
- **BI & governance.** Wire the outputs into Power BI/Tableau dashboards and a
  quarterly fair-value governance cycle with automated drift monitoring (PSI on
  margin, mix, competitor index).

---

## 5. Going deeper — the theory behind every claim

The [**pricing school**](../pricing_school/00_START_HERE.md) is the conceptual
companion to this evidence: foundations (files 01–15) plus the senior reference
(files 18–21) covering strategy & WTP, causal elasticity and the methods
catalogue, revenue management, channel economics, packaging, promotions,
P&L/unit economics, AOP & bridges, FCA Consumer Duty & competition law,
behavioural pricing, B2B/contract, subscription/platform, competitor
war-gaming, operations & governance, KPIs, a formula cheat-sheet
([glossary](../pricing_school/10_glossary.md)), and the travel-money domain
deep-dive. The [question bank](../pricing_school/14_interview_qa_bank.md) §F
expands the five stories above into rehearsed STAR answers.
