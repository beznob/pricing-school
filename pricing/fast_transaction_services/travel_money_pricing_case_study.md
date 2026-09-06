# Travel Money & Prepaid Card Pricing — A Distribution & Revenue Case Study

A domain-specific companion to
[`dynamic_pricing_and_elasticity_case_study.md`](dynamic_pricing_and_elasticity_case_study.md)
(the general methods), built for the **Senior Manager, Pricing, Distribution &
Revenue** remit: multi-channel travel money + prepaid FX cards, sold through
retail, TMC, digital, agency and the **Post Office / Postmaster** network, under
**FCA Consumer Duty**.

Run it all in ~5 seconds:

```bash
pip install numpy pandas matplotlib
python run_role_case_study.py     # writes ROLE_RESULTS.md, FAIR_VALUE_ASSESSMENT.md, role_*.png
```

| Module | Role pillar |
|---|---|
| `travel_money_simulator.py` | The business: 5 channels, FX margin, card lifecycle, competitor margins |
| `elasticity_models.py` *(reused)* | Causal **elasticity modelling** of FX margin |
| `distribution_economics.py` | **Distribution & channel economics**, margin support |
| `fair_value.py` | **FCA Consumer Duty** fair value assessment |
| `aop_scenario.py` | **AOP** scenario modelling + competitor intelligence |

---

## 1. The business and the price levers

The "price" in travel money is not one number. Revenue comes from a **bundle**:

* **FX margin (the spread)** — the markup over the wholesale/interbank rate. This
  is the primary, most visible lever, and where elasticity bites hardest.
* **Card fees** — issuance, ATM withdrawal, and **inactivity** fees.
* **In-life FX** — margin earned when customers spend abroad.
* **Breakage** — unspent balances on dormant cards.

The P&L splits into the lines the JD names — **new card sales, reloads, in-life
revenue** — and is earned across channels with very different economics.

## 2. Channel elasticity, estimated causally

Each channel has a different **FX-margin elasticity**, and we must estimate it
*causally* because the firm pushes margin up in peak holiday season when demand is
already high (endogeneity). Reusing the IV/2SLS engine with a wholesale-cost
instrument (`role_fig1_channel_elasticity.png`):

| Channel | True ε | OLS ε | IV ε |
|---|---:|---:|---:|
| digital | −2.20 | −1.10 | **−2.21** |
| retail | −1.30 | −0.36 | **−1.39** |
| agency | −1.20 | −0.47 | **−1.29** |
| post_office | −1.00 | −0.17 | **−1.10** |
| tmc | −0.70 | −0.04 | **−0.68** |

**Digital is the most price-sensitive** (customers compare rates in seconds);
**TMC is the least** (contracted B2B2C). Naive OLS makes every channel look far
more inelastic than it is — pricing on it would systematically over-charge and
quietly bleed volume. *(Mechanism and IV validity: see the methods doc, §3.)*

## 3. Distribution economics — price the *net*, not the headline

The same FX margin earns wildly different **net contribution** by channel, because
of commission (Postmaster/agency payaway) and cost-to-serve
(`role_fig2_distribution.png`, panel a):

| Channel | Gross rev (2y) | Commission | Cost to serve | Contribution | Contrib margin |
|---|---:|---:|---:|---:|---:|
| digital | £82.4m | £0 | £3.4m | £79.0m | **96%** |
| post_office | £109.1m | **£35.4m** | £4.8m | £68.9m | 63% |
| retail | £73.7m | £0 | **£13.0m** | £60.8m | 82% |
| tmc | £56.0m | £3.3m | £1.9m | £50.8m | 91% |
| agency | £31.5m | £6.7m | £2.4m | £22.4m | 71% |

The Post Office is the **biggest gross-revenue channel but only the second-biggest
contributor** — ~45% of its FX revenue is paid away as Postmaster commission. The
**margin waterfall** (`margin_waterfall`) makes this explicit per £ loaded.

**Positioning follows elasticity** (`channel_positioning`, panel b): compete hard
on margin in elastic **digital** (≈ +20% FX-contribution uplift), **harvest** the
inelastic **TMC / Post Office**, hold roughly steady where high cost-to-serve
(retail) makes chasing volume expensive.

**Margin support** (`margin_support_breakeven`) answers "is a giveaway
self-funding?": a 10% FX-margin cut needs +11.1% volume to break even; elastic
channels deliver more than that (accretive), inelastic TMC does not (dilutive). A
clean, defensible rule for when to fund a competitive response.

## 4. FCA Consumer Duty — fair value (PRIN 2A.4)

Consumer Duty requires the **total price** over the lifecycle to be reasonable
relative to the **benefits**, with explicit attention to **vulnerable customers**.
`fair_value.py` operationalises this and writes a documented assessment
(`FAIR_VALUE_ASSESSMENT.md`, `role_fig3_fair_value.png`):

* **Total price** = FX cost + issuance + ATM + **inactivity fees that erode
  unspent balances** (the classic prepaid harm).
* **Benefit (value) score** proxies speed, acceptance, security, convenience.
* **Differential outcomes**: vulnerable customers pay **+1.7pp more**
  (7.0% vs 5.3% of load) for **lower** benefit, and **44%** are flagged Red on
  price-to-value vs **9%** of standard customers — concentrated in the high-fee
  agency / Post Office / retail channels.
* **Remediation**: cap inactivity fees at the remaining balance, auto-refund small
  dormant balances, disclose total cost pre-purchase, and signpost the cheaper
  digital option to price-sensitive / vulnerable customers.

This is the "regulatory pricing justification and fair value documentation" the
role must produce — generated, not hand-waved.

## 5. AOP scenario modelling & competitor intelligence

`aop_scenario.py` builds the annual plan (~**£176m** gross: £115m FX + £61m fees)
and flexes it under a standard scenario set (`role_fig4_aop.png`):

| Scenario | Contribution vs base |
|---|---:|
| Upside (travel boom, +12% vol) | +12.0% |
| Cut FX margin −10% (uniform) | +8.6% |
| Shift 10% volume to digital | −1.5% |
| Raise FX margin +10% (uniform) | −6.7% |
| Competitor price war −15% | −7.8% |
| Downside (recession, −12% vol) | −12.0% |

Two senior insights fall straight out:

1. **Uniform margin moves are the wrong tool.** A blanket +10% FX margin *reduces*
   contribution because blended demand is elastic — yet §3 showed that *targeted*
   harvesting of the inelastic channels *raises* it. Channel-specific beats
   one-size-fits-all.
2. **Competitor moves are quantifiable.** The cross-elasticity sensitivity turns
   "the market is getting aggressive" into a number: a 15% competitor undercut
   costs ~7.8% of contribution — which is what a margin-support budget should be
   sized against.

A **revenue bridge** attributes any plan-vs-actual gap to volume, FX margin,
competitor and channel-mix effects, so the AOP can be defended line by line.

## 6. Productionising (how this becomes BAU)

* **Data & BI**: the tidy panel/portfolio tables drop straight into SQL +
  Power BI / Tableau; the scorecards become governance dashboards.
* **Identification**: keep a permanent **randomised price-exploration / geo
  switchback** stream so elasticity stays estimable once models set prices.
* **Governance**: quarterly fair-value re-assessment; drift monitoring (PSI on FX
  margin, channel mix, competitor index); guardrails (caps/floors/rate-limits) on
  any automated margin move to stay clear of fairness and competition-law risk.
* **Scale**: replace per-channel IV with **double ML / causal forests** for
  customer-level elasticity (corridor, ticket, tenure).

---

**See also:** [`JD_alignment.md`](JD_alignment.md) maps each JD bullet to the exact
file/figure that evidences it, plus five interview stories;
[`ROLE_RESULTS.md`](ROLE_RESULTS.md) has the auto-generated numbers and figures.
