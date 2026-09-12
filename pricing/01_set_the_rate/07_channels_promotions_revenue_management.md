# 1.7 · Channels, Promotions, Competition & Revenue Management — the senior reference

*(Consolidated from the former `pricing_manager_handbook` chapters 05, 06, 08
and 15. Foundations: waterfall & leakage in [File 1.4](04_price_volume_mix_and_leakage.md), price wars in [File 1.5](05_competition.md),
elasticity in [File 1.3](03_elasticity.md).)*

## 1. Channel economics — price the pocket, not the list

The same headline price earns wildly different net margin by channel. The full
waterfall ([File 1.4](04_price_volume_mix_and_leakage.md)'s version, with the channel deductions spelled out):

```
List price
  − on-invoice discounts / promotions      → invoice price
  − off-invoice rebates, volume bonuses
  − channel commission / payaway (Postmaster, agency, affiliate)
  − cost-to-serve (processing, fraud, support, cash handling, settlement)
  − funding/float cost, chargebacks, breakage adjustments
  = POCKET margin / net contribution   ← the only number that matters
```

Model three drivers per channel: **revenue intensity** (take rate × volume),
**commission/payaway** (often the dominant deduction — Postmaster ≈ 45% of FX
revenue in the case study), **cost-to-serve** (physical dear, digital cheap).
`Contribution = gross revenue − commission − cost-to-serve`. **Rank channels by
contribution, not gross revenue** — the biggest gross earner can be a middling
contributor.

**Positioning follows elasticity** ([File 1.3](03_elasticity.md) + net economics):
- Elastic + low cost-to-serve (digital) → **compete hard**; volume rewards the cut.
- Inelastic (wholesale, contracted, walk-in) → **harvest** — hold or raise margin.
- High cost-to-serve (physical retail) → chasing volume is expensive; hold.

This is why **uniform moves destroy value and targeted ones create it** — a
blanket +10% margin can *reduce* contribution while channel-specific harvesting
raises it.

**Partner commission is a strategic lever, not a fixed cost** — model whether a
higher payaway buys enough footfall/volume/exclusivity to pay for itself.

**Omnichannel cautions:** price to each channel's *role* (acquisition, retention,
reach), keep unexplained gaps small (arbitrage, trust, Consumer Duty), manage
channel conflict with segmentation and channel-specific bundles — and never
dictate a partner's minimum resale price (RPM — see [File 3.3](../03_defend_the_plan/03_operating_model_and_governance.md)).

## 2. Margin support and the discount break-even (memorise)

Cut price by fraction `d` with contribution-margin ratio `CM = (P−V)/P`. The
volume uplift needed just to hold total contribution:

> **required uplift = d / (CM − d)**   (for a price *rise*, the volume you can
> afford to lose is `d / (CM + d)`)

The lower the margin, the deadlier the discount: at CM = 30%, a 10% cut needs
**+50%** volume; at CM = 60%, +20%. Compare against the **elasticity-implied**
uplift `(1−d)^ε − 1`: fund the cut only if implied > break-even (accretive);
otherwise it's a margin transfer to customers who'd have bought anyway.

## 3. Promotions and trade spend

**Incrementality is everything.** Decompose headline promo "uplift" into:
- **Incremental** — genuinely new sales (the only part that counts),
- **Cannibalisation** — pulled from your own full-price products,
- **Pull-forward / pantry-loading** — borrowed from the future (trough follows),
- **Subsidised baseline** — would-have-bought-anyway, now cheaper. Pure loss.

**Promo ROI = incremental contribution ÷ promo cost**, measured with a
holdout/control ([File 2.2](../02_prove_the_change/02_tests_and_experiments.md)), never pre/post.

**Trade promotions** (channel businesses): on-invoice vs off-invoice (rebates,
listing fees — harder to track → leakage risk); watch forward-buying/diverting;
measure sell-*through* (to end customers), not sell-*in* (to the partner).

**Discount governance** (the senior contribution — build the system, don't
approve one-offs): discount ladders tied to commitment, an approval matrix with
floors, discount-to-value linkage, **sunset rules** so reference prices don't
ratchet down ("never pay full price" trap), and standing leakage reporting.

**High-Low vs EDLP:** frequent promos exploit deal-seekers but train waiting and
add cost; every-day-low-price builds trust but forgoes discrimination. Choose by
segment and brand. Framing follows the Rule of 100 ([File 1.6](06_strategy_and_offer_design.md) §6); "was/now"
claims must be genuine.

## 4. Revenue management and dynamic pricing

**From elasticity to the optimal price.** Maximising `π = (P − c)·Q(P)` gives
MR = MC and the **Lerner rule** ([File 1.3](03_elasticity.md) §5):

```
(P − c)/P = 1/|ε|        P* = c·|ε|/(|ε|−1)   (valid only when |ε| > 1)
MR = P(1 − 1/|ε|)
```

Revenue is maxed at ε = −1; **profit** is maxed at a more inelastic point
(you also save variable cost on the units you don't sell).

**When the textbook FOC collapses:** with marginal cost tiny relative to price
(digital/FX), `P*` pushes to a corner/floor — the real lever becomes strategic
positioning vs the market, inside guardrails and fair value. Knowing when the
formula stops being the right tool is a senior distinction.

**Yield management** — right capacity, right customer, right price, right time:
demand forecasting by segment and lead time; capacity fences protecting
inventory for high-WTP late buyers; overbooking and **bid prices** (price the
marginal unit at its displacement cost); time-based price paths.

**Dynamic pricing drivers** (tie every move to a real driver, not noise):
cost-to-serve/load (surge), demand (peak season), competitor (index within
guardrails), personalisation (most conduct-sensitive — prefer
segment/eligibility over individual in regulated retail).

**Building the policy:** start with a hand-built, guarded, auditable rule
(caps/floors/rate-limits) — the right default in a regulated firm; a learned
policy (bandits/RL, see [file 2.3](../02_prove_the_change/03_causal_inference_primer.md)'s methods catalogue) can close most of
the gap to an oracle but must run *inside* the same guardrails with monitoring
and a kill-switch. Guardrails are non-negotiable: caps & floors, rate limits,
fairness constraints, no collusion-facilitating behaviour, drift monitoring,
kill-switch ([File 4.1](../04_satisfy_the_regulator/01_segments_and_fairness.md), [the workflow appendix](../appendix/data_science_workflow.md) and [file 3.3](../03_defend_the_plan/03_operating_model_and_governance.md)).

## 5. Competitor intelligence and war-gaming

**Price index:** define a like-for-like basket (same amount, corridor, channel);
collect from public sources/mystery shopping on a cadence (daily for FX);
index = your price ÷ market; compare **total cost**, not headline ([File 1.2](02_percentages_and_basis_points.md)'s
reflex). *Competition-law guardrail:* never exchange pricing intentions with
competitors; keep benchmarking clean ([File 3.3](../03_defend_the_plan/03_operating_model_and_governance.md) §4).

**Quantify the threat:** cross-price elasticity `ε_xy = %ΔQ_x / %ΔP_y`
(positive = substitutes) turns "the market is aggressive" into **£ of
contribution at risk** — which is what sizes the margin-support budget.

**Game theory lenses** ([File 1.5](05_competition.md) taught the prisoner's dilemma; the extras):
- **Bertrand trap** — near-identical products + low switching costs drive price
  to marginal cost. Digital FX is dangerously close → differentiate on brand,
  convenience, trust, bundling, or die on margin.
- **Repeated games** — "hold price" can be a stable equilibrium without any
  agreement; *engineering* that coordination (signalling, instant matching
  algorithms) crosses the legal line.
- **Commitment** — a credible price-match guarantee can *deter* undercutting by
  removing the rival's share gain.

**War-game before any material move:** who reacts → how fast/deep → your
response to their response → payoff matrix under {move/hold} × {follow/don't} →
**pre-commit a response rule** so you don't react emotionally mid-war.

**Avoiding/exiting wars:** don't start one against a structural cost advantage;
compete selectively in the contested segment (fighter offer, [File 1.6](06_strategy_and_offer_design.md) §5) rather
than across the board; de-escalate by giving rivals a face-saving exit.

## Checklist

- [ ] Waterfall built list → pocket per channel; channels ranked by **contribution**.
- [ ] Each channel positioned by its own causal elasticity + cost-to-serve.
- [ ] Every discount cleared `d/(CM−d)` vs the elasticity-implied uplift *before* approval.
- [ ] Promo ROI measured on **incrementality** with a holdout.
- [ ] Dynamic moves tied to a real driver, inside caps/floors/rate-limits with a kill-switch.
- [ ] A total-cost price index from legal sources; competitor threats sized in £.
- [ ] A war-game and pre-committed response rule before material moves.

## Red flags

- Ranking or funding channels on gross revenue while commission hides the truth.
- "We need to be competitive" discounts with no break-even test.
- Celebrating pre/post promo uplift with no control; reference-price erosion.
- Surge with no caps; a learned pricing policy with no guardrails.
- Matching every competitor move reflexively; any pricing-intention exchange.

## Check yourself

Try these before you look at the answers below.

1. Channel A earns £100m gross with 45% commission paid away and £5m of cost to
   serve. Channel B earns £60m gross with no commission and £3m of cost to serve.
   Rank them by contribution.
2. Contribution margin is 40% and marketing wants a 10% price cut. What volume
   uplift is needed just to stand still? If elasticity is minus 2, what uplift do
   you expect? Do you approve the cut?
3. A promotion week shows sales up 30% on the week before. Name the four parts a
   headline uplift has to be split into, say which one counts, and say how it
   must be measured.

**Answers.** (1) A: 100 minus 45 minus 5 is £50m. B: 60 minus 0 minus 3 is £57m.
B ranks higher despite the smaller gross, which is the whole point of pricing the
pocket rather than the list. (2) Required uplift is 0.10 divided by (0.40 minus
0.10), which is 33%. Expected uplift at elasticity minus 2 is 0.9 to the power
minus 2, minus 1, which is about 23%. Expected is below required, so the cut
loses contribution and should not be approved as a margin move. It might still be
approved as a deliberate acquisition spend, but call it that. (3) Incremental
sales, cannibalisation of your own full price products, pull forward from future
weeks, and the subsidised baseline of people who would have bought anyway. Only
the incremental part counts, and it is measured against a holdout or control,
never before and after.
