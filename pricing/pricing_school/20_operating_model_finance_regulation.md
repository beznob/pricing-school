# 20 · Running the Function — Operating Model, P&L, AOP, Regulation, Governance

*(Consolidated from the former `pricing_manager_handbook` chapters 00, 09, 10,
11, 17, 18 and 19. Foundations: KPIs & stakeholders in File 13, fairness in
File 07, monitoring in File 12 §8.)*

## 1. The role and the operating model

A senior pricing manager owns the **commercial logic of how the firm captures
value** — what we charge, to whom, through which channel, under what rules, and
how the revenue line is defended in the plan. The deliverable is never "a
model"; it is a **defensible commercial decision plus the evidence** that lets
the CRO, Finance and the regulator trust it.

**Five accountabilities:** pricing strategy · causal elasticity & testing ·
distribution/channel economics (net margin) · revenue & AOP ownership ·
conduct & compliance.

**The operating cadence** (pricing is a process on a rhythm, not a project):

| Cadence | Activity |
|---|---|
| Daily | Competitor rate monitoring, automated feeds, guardrail alerts, exception queue |
| Weekly | Price index vs market, win/loss & volume review, live-test readouts, discount approvals |
| Monthly | Margin & leakage review, channel P&L, promo post-mortems, forecast re-base |
| Quarterly | Fair-value re-assessment, elasticity refresh, strategy review, governance sign-off |
| Annual | AOP build, architecture review, segment & fence redesign |

**Where the function sits:** centralised CoE (scales expertise, slow), embedded
(fast, inconsistent), or **hub-and-spoke** — central team owns methodology,
guardrails, systems and the price book; embedded partners own local execution.
Usually the right answer.

**The senior-vs-analyst line (interview-critical):** the analyst estimates the
elasticity; the senior manager decides what to do given the elasticity *and*
the conduct/competitor/finance constraints, owns the P&L consequence, and gets
buy-in. "What is ε?" vs "should we move price, by how much, where, and how do
we defend it?"

## 2. P&L fluency and unit economics

```
Revenue
  − variable cost (cost-to-serve, processing, commission, fraud)
  = CONTRIBUTION            ← the pricing-controllable line
  − fixed cost
  = operating profit
```

Price moves flow almost entirely to contribution — the 1%-price ≈ 11%-profit
lever of File 04. Core formulas: CM ratio `(P−V)/P`; break-even volume
`fixed ÷ (P−V)`; discount break-even `d/(CM−d)` and rise tolerance `d/(CM+d)`
(File 19 §2). High operating leverage (fixed-heavy) makes profit very sensitive
to both volume and price.

**LTV and acquisition:**

```
LTV = ARPU × contribution margin ÷ churn      (steady state)
    = Σ_t margin_t / (1+r)^t                   (discounted, more correct)
```

**CAC** fully loaded; **LTV/CAC ≈ 3×** is the usual health rule of thumb, but
always pair it with **payback period** — a great ratio can still be
cash-starved. Price affects *all* of these: a rise lifts ARPU but can raise
churn — model the net LTV effect.

**The travel-money revenue lines** (own them line by line — each has its own
margin, growth and risk): new card sales (issuance + first-load FX), reloads
(the recurring engine), in-life/spend (FX + interchange + ATM), **breakage**
and **inactivity fees** (high margin, *the* classic Consumer Duty harm — §4).
Don't forget **float** (customer money held), funding and hedging cost,
chargebacks/fraud — they belong in the variable-cost stack, not a footnote.

**Habits:** express every move in **£ of contribution**, not %; carry a
tornado/sensitivity view (price > mix > volume > cost); always hold a
recession/price-war downside scenario ready.

## 3. AOP, forecasting and the revenue bridge

**Build bottom-up** by revenue line × channel × segment
(`revenue = Σ volume × price(metric) × mix`), reconcile top-down. Drive each
line with explicit volume / price / mix / elasticity assumptions — the senior
skill is **internal consistency**: never "+10% margin and flat volume" on an
elastic line.

**Scenarios, never a point estimate:** base / upside / downside (recession,
price war, FX volatility) / policy moves — each run *through the elasticity* so
volume responds endogenously. The repeatable headline: **uniform price moves
under-perform targeted ones** (File 19 §1), and the scenario engine is how you
prove it to Finance.

**The revenue bridge (PVM)** — decompose every plan-vs-actual gap:

```
ΔRevenue = volume effect + price effect + mix effect (+ FX + competitor)
  volume = ΔQ × P₀      price = ΔP × Q₁ (pick a convention, keep it)
  mix    = share shift between high- and low-margin lines
```

**If you can't bridge it, you don't understand it.**

**Forecasting craft:** decompose (trend + seasonality + events + price/promo +
competitor + macro) rather than forecasting the blob; a transparent model
Finance trusts often beats a black box; backtest **out-of-time** and report
**bias**, not just error (consistent over/under is worse than noise for a
plan); reconcile bottom-up with top-down; re-forecast on a rolling cadence.
The plan is also the **budget envelope**: the price-war downside sizes the
margin-support budget, and one elasticity is the single source of truth for
plan and optimiser alike.

## 4. Regulation — Consumer Duty and competition law

*(Working knowledge, not legal advice — engage Compliance early.)*

**FCA Consumer Duty (PRIN 12 / 2A)** — in force 31 Jul 2023 (open products),
31 Jul 2024 (closed). Firms must act to deliver **good outcomes**; the
cross-cutting rules: act in good faith, avoid foreseeable harm, enable
customers to pursue their objectives. Four outcomes: products & services,
**price & value (fair value — the pricing-critical one)**, consumer
understanding, consumer support.

A defensible **fair-value assessment** covers: **total price over the
lifecycle** (FX margin, issuance, ATM, inactivity/dormancy fees, breakage — not
the headline); the benefits delivered; comparison vs alternatives and across
customer groups; **differential outcomes for vulnerable customers** (FG21/1 —
health, life events, resilience, capability); remediation and governance
(cap inactivity fees at remaining balance, auto-refund small dormant balances,
disclose total cost, signpost cheaper options), **re-assessed at least annually
with board-level MI**. File 07 teaches the mix trap that makes group averages
lie.

**Competition law (Competition Act 1998; CMA):**
- **Chapter I — agreements**: price fixing/cartels (criminal); **information
  exchange** — even sharing future pricing intentions can be illegal (careful
  with benchmarking and trade bodies); **RPM** — dictating a partner's *minimum*
  resale price is generally unlawful (max/RRP is fine); **algorithmic/tacit
  collusion** — pricing algorithms must not learn to coordinate or signal.
- **Chapter II — abuse of dominance**: excessive or predatory pricing, margin
  squeeze, discriminatory/exclusivity terms.
- Also: **MFN/parity clauses** are restricted (the OTA cases); misleading
  "was/now" reference prices and drip pricing breach consumer-protection law.

**Payments/e-money specifics:** Electronic Money Regulations 2011 (issuance,
**safeguarding** of customer funds), PSRs 2017/PSD2, FX transparency
expectations.

## 5. Operations, systems and governance

**The price management lifecycle — own all of it, not just step 1:**

```
Set → Approve → Publish/Deploy → Execute → Monitor → Review → Re-set
```

**Systems:** rate/price engine (system of record; guardrails live here), CPQ
for negotiated deals, automated competitor feed → index, a decision/
optimisation layer *inside* guardrails with a kill-switch, BI/MI dashboards
(realisation, channel P&L, fair-value scorecard, drift).

**Controls:** pricing committee + authority matrix; caps/floors/max-step/
fairness constraints enforced in the engine; every change **versioned,
attributable, reversible** (audit trail); segregation between price-setters and
controllers; fair-value and competition-law governance on a cadence.

**Monitoring (MLOps for pricing — File 12 §8 is the foundation):** PSI on
inputs (margin, mix, competitor index; >0.25 = investigate), realised-vs-
predicted performance, guardrail-breach patterns, conduct signals (complaints,
fair-value RAG) — and the **permanent randomised exploration/holdout stream**,
because once the model sets prices it poisons its own training data. Keep a
documented runbook for drift alerts, breaches, complaint spikes and competitor
wars.

## 6. The KPI dictionary — senior extras

File 13 carries the core set. Additional metrics worth defining precisely:

| Metric | Definition | Why |
|---|---|---|
| **Price realisation** | pocket ÷ list | The leakage measure; low outliers = recoverable margin |
| **Realised FX margin** | actual spread captured vs interbank | The core travel-money price metric |
| **Take rate** | revenue ÷ value transacted | Monetisation intensity |
| **Attach rate** | % of sales with an add-on/fee | Packaging health |
| **Pass-through** | % of a cost/competitor move reflected in price | Pricing execution |
| **Breakage rate** | unspent balance % | Revenue *and* conduct metric |
| **Fair-value RAG / vulnerable differential** | outcome distribution by group | The standing conduct pack |

**The senior habit:** every KPI gets numerator, denominator, population, window,
and *which* price/margin (list vs pocket, gross vs contribution) pinned down in
a published metric dictionary — most pricing arguments are definition disputes.
The CRO scorecard is one page: realised margin & leakage, price index, volume &
mix, promo ROI, fair-value RAG, AOP variance bridge — each with trend and RAG.

## 7. Influence — the senior extras

File 13 §§2–4 carry the stakeholder map and committee playbook. Additions from
the senior reference:

- **Answer-first (pyramid principle):** make the recommendation, then show the
  evidence — never a build-up to a reveal.
- **Bring options** (base/aggressive/cautious) with a clear pick — give the
  executive a decision, not a fait accompli.
- **Lead with the £ prize and the £ risk**, not the methodology; name the
  trade-off honestly.
- **Chair a decision-led cadence** — each meeting resolves something; a status
  meeting is a failure mode.
- **30-60-90:** learn the P&L/data/competitors/conduct posture and find the
  obvious leakage (0–30); stand up the price index + realisation view, estimate
  elasticity causally on the biggest line, pick 1–2 quick wins (30–60); ship a
  measured quick win, propose the cadence + guardrails, kick off the fair-value
  assessment (60–90). Earn the right to the big bets. (Plain-English version:
  File 13 §5.)

## Checklist

- [ ] A written strategy, a named owner and a bridge for every revenue line.
- [ ] Elasticity measured causally, refreshed on a cadence, one source of truth.
- [ ] Every price move sized in £ contribution with a downside scenario.
- [ ] Fair-value assessment documented, vulnerable outcomes tested, re-assessed annually.
- [ ] No RPM, no pricing-intention exchange, collusion-safe algorithms.
- [ ] Lifecycle controls: versioned, attributable, reversible; exploration stream on.
- [ ] KPI dictionary published; scorecard ties to £ contribution and the AOP bridge.

## Red flags

- Cost-plus with no view of value; "our customers aren't price-sensitive" with no causal evidence.
- A plan that can't be decomposed into volume/price/mix/FX/competitor.
- Inactivity/breakage revenue with no fair-value justification.
- Prices set in spreadsheets with no audit trail; a live model with no kill-switch.
- Fair value assessed once at launch and never again.
- Presenting methodology before the recommendation; surprising Compliance late.
