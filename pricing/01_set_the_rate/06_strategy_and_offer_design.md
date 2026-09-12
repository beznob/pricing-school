# 1.6 · Pricing Strategy & Offer Design — the senior reference

*(Consolidated from the former `pricing_manager_handbook` chapters 01, 02, 07, 12,
13 and 14. Where the foundation files teach the foundations in plain English, this
file is the senior working reference: frameworks, formulas, checklists.)*

## 1. The three bases of price — and the value stick

| Basis | Logic | Problem |
|---|---|---|
| **Cost-plus** | price = cost × (1 + markup) | Ignores value and demand; procyclically wrong (cuts price exactly when costs and demand are low); leaves money on the table |
| **Competition-based** | price = benchmark ± position | Outsources your strategy to rivals; races to the bottom |
| **Value-based** | price = f(willingness to pay) | Hard to measure — but the only one that maximises captured value |

The mature answer: **cost is the floor, value is the ceiling, competition is
the reference point** — strategy chooses where in that band to sit, per segment.

The value stick: `Cost ── Price ── Customer's WTP`. **Price − Cost** is firm
margin; **WTP − Price** is consumer surplus. Strategy decides how to split the
value created (WTP − Cost). Consumer Duty is, in effect, a regulatory floor on
how much surplus you must leave the customer ([File 4.1](../04_satisfy_the_regulator/01_segments_and_fairness.md)).

## 2. The strategy ladder — six decisions, in order

1. **Objective** — profit max? penetration? skim? defend? LTV vs first-transaction
   margin? Make it explicit; everything cascades.
2. **Segmentation** — the distinct WTP groups, and the *observable* signal that
   separates them.
3. **Value proposition per segment** — what value do we deliver, and how does it differ?
4. **Price metric** — *what unit you charge for* (per transaction, per £ loaded,
   per month, % of value). Often matters more than the level: pick the metric
   that scales with the value received, is hard to game, and feels fair.
5. **Price architecture** — tiers, fences, add-ons, bundles, good-better-best.
6. **Price level & fences** — the numbers, and the rules that stop a high-WTP
   customer buying the cheap option.

**Penetration vs skimming (launch choice):** skim when differentiation is strong,
capacity constrained, high-WTP early adopters exist (risk: invites entry);
penetrate when scale/network effects matter and you want to deter entrants
(risk: anchors a low reference price you can't raise).

## 3. Fences and the degrees of price discrimination

A **fence** makes the high-WTP customer unwilling/unable to take the cheap price.
Good fences are hard to arbitrage, correlated with WTP, and perceived as fair.
Types: customer attributes, product version, channel, time (advance vs
last-minute), volume/commitment, geography, bundling, hassle.

- **1st degree** — each customer pays their exact WTP (approximated by
  personalised pricing; conduct-constrained).
- **2nd degree** — self-selected version/quantity (tiers, bundles, volume). The
  customer sorts themselves.
- **3rd degree** — by observable group (student, region, channel).

## 4. Measuring value and willingness to pay

**EVE / EVC (economic value to the customer)** — build value from the next-best
alternative up:

```
EVE = Reference price (next-best alternative)
    + positive differentiation value (£)  − negative differentiation value (£)
```

EVE sets the economic ceiling; capturing **50–70% of quantified differentiation
value** is a common, defensible target.

**The value map** — plot competitors on perceived price (x) vs perceived benefit
(y). The diagonal is the **Value Equivalence Line (VEL)**: above the line gains
share, below loses it. The single best one-slide artefact for a strategy conversation.

**WTP research toolkit** (triangulate ≥2, at least one behavioural):

| Method | What it does | Caveat |
|---|---|---|
| **Van Westendorp** | 4 questions (too cheap / bargain / getting expensive / too expensive) → acceptable price range, OPP, IPP | Stated attitudes, no competition or volume — a sanity range, not a demand curve |
| **Gabor-Granger** | Purchase intent at a series of prices → demand curve, revenue-max price | Still stated-preference, single-product |
| **Conjoint / discrete choice** | Choices between attribute bundles → part-worth utilities; WTP for an attribute = `−(β_attr / β_price)` | Gold standard for stated WTP; expensive to field |
| **Revealed preference** | Transactions + experiments ([File 1.3](03_elasticity.md) and [file 2.2](../02_prove_the_change/02_tests_and_experiments.md)) | The truth — use surveys for hypotheses, experiments to decide |

**WTP ↔ elasticity:** the distribution of WTP across customers *is* the demand
curve (demand at p = share of customers with WTP ≥ p); elasticity is its local
slope. Knowing the *shape*, not one number, is what lets you pick tiers and
fences well.

## 5. Packaging, bundling and versioning

Packaging is applied 2nd-degree discrimination — customers self-select into
paying their WTP.

- **Good-Better-Best**: Good anchors entry and blocks cheap entrants; **Better is
  the designed default**; Best captures the high-WTP tail and anchors high (even
  low take-up is valuable). 3–4 tiers; price ratios commonly ≈ 1 : 1.5–2 : 3+,
  tuned to the WTP distribution. Fence features must track WTP.
- **Versioning levers**: features, usage limits, speed/SLA, support, seats,
  delay, convenience/hassle, brand. Deliberately limiting the cheap version
  ("damaged goods") is a legitimate fence.
- **Bundling** works because it **reduces the dispersion of WTP across the
  bundle**. Most powerful when valuations are *negatively correlated* and
  marginal cost is low. **Mixed bundling** (bundle *and* components) is usually
  optimal. Worked intuition: A values {X:£8, Y:£2}, B values {X:£2, Y:£8} — no
  single per-item price captures both; a £10 bundle sells to both.
- **Add-ons** unbundle high-WTP extras (priority, insurance, rate-lock) — but
  total cost must stay clear (drip pricing is a conduct hazard).
- **Fighter brand** — a separate low-price line to meet a discounter without
  cannibalising the premium brand; fence it hard.
- **Freemium vs free trial**: trial when value is obvious immediately; freemium
  when value accrues with usage and the free user's marginal cost ≈ 0.

## 6. Behavioural pricing — perception, honestly used

Customers perceive price relative to **references, framing and context**. Use
these to reduce friction and communicate value — exploiting them breaches
Consumer Duty ([File 4.1](../04_satisfy_the_regulator/01_segments_and_fairness.md)).

- **Anchoring & reference prices** — the first number frames everything; price
  rises feel like *losses* vs the reference (loss aversion ≈ 2× gains).
- **Rule of 100** (Weber–Fechner): below ~£100 frame discounts as **% off**;
  above, as **£ off**.
- Classic effects: **charm/left-digit** (£9.99; round numbers signal premium),
  **decoy/asymmetric dominance** (a dominated option steers to the target),
  **centre-stage/compromise** (people pick the middle — design Better as the
  middle), **partitioned vs all-in pricing** (keep total cost visible early),
  **endowment & "free"**, **genuine** scarcity/urgency only.
- **Precision**: precise prices (£1,847) feel justified for considered purchases;
  round prices feel premium.
- **Fairness perception is a real constraint** — customers punish prices they
  perceive as gouging or opaque even at cost to themselves.
- **The conduct line**: never monetise inertia/forgetfulness (inactivity fees,
  silent auto-renew), fake reference prices, or drip-reveal fees.

## 7. B2B, contract and negotiated pricing

Relevant via wholesale partners and corporate/agency channels. Different physics: negotiated
not posted; few, large, heterogeneous deals; multi-stakeholder buying; TCO
thinking; switching costs create lock-in.

- **EVE is most usable in B2B** — quantify the customer's £ value and anchor the
  negotiation on it, shifting from "your price vs competitor's" to "your value
  vs your price".
- **Pocket-price band** — plot realised prices across deals; the *width* of the
  band is the opportunity. **Price realisation = pocket ÷ list**; track per rep,
  segment, size.
- **Deal desk & governance**: approval matrix by depth/role; discount ladders
  tied to **volume, term, prepayment, exclusivity** (every concession buys
  something — **give-get**); CPQ enforces the policy and captures the waterfall.
- **Contract structures**: volume tiers; **two-part tariff** (access fee +
  per-unit); rebates (retrospective, threshold — accrual headache,
  competition-law sensitivity); **index-linked/pass-through** for cost-volatile
  inputs (crucial for FX contracts); most-favoured-customer clauses (concede
  with caution).
- **Price increases**: justify with value/index, segment the rise by elasticity,
  give notice/grandfather deliberately, and **measure realisation** (announced ≠
  realised).

## 8. Subscription and platform pricing

**Recurring metrics:** MRR/ARR, ARPU/ARPA, gross churn, **NRR** (net revenue
retention incl. expansion — >100% = growth with zero new customers; the single
best health metric), quick ratio, LTV = ARPU × margin ÷ churn (see [File 3.3](../03_defend_the_plan/03_operating_model_and_governance.md) for
the discounted form).

**Levers:** the metric (usage/value metrics expand automatically; seat metrics
don't), tiers (§5 applies), **annual vs monthly** (annual prepay buys cash +
retention — discount it deliberately), expansion paths (design NRR > 100%),
grandfathering on repricing (fairness/churn vs realisation).

**In travel money:** a monthly-fee "premium FX" plan (better rate, fee waivers)
trades transactional margin for recurring revenue and stickiness — model the
*net* LTV effect including cannibalised spread.

**Two-sided platforms** (cardholders ↔ merchants; travellers ↔ Postmasters):
classic one-sided pricing breaks under cross-side network effects.
- **The split is the lever** — who you charge matters as much as how much.
- **Subsidise the more elastic / value-driving side**; charge the side that
  benefits more and is less price-sensitive.
- Bootstrap the harder-to-acquire side first (chicken-and-egg).
- Watch **multi-homing** (reduces pricing power) and platform regulation
  (interchange, parity clauses).

## Checklist

- [ ] Objective explicit; segments defined by an observable, fence-able signal.
- [ ] The **metric** scales with delivered value and is defensible.
- [ ] WTP triangulated from ≥2 methods, one behavioural; EVE stated vs the next-best alternative.
- [ ] Tiers map to WTP segments; **mixed bundling** where valuations are dispersed.
- [ ] Behavioural techniques survive a conduct review (total cost clear, nothing exploits bias).
- [ ] B2B: pocket-price band measured; concessions are give-get; FX contracts index-linked.
- [ ] Recurring: metric enables NRR > 100%; platform sides priced jointly.

## Red flags

- One price for all customers "for simplicity" — almost always value-destroying.
- A metric that doesn't scale with value (flat fee where value varies 100×).
- Treating survey WTP as ground truth without behavioural validation.
- Fences a customer can trivially arbitrage; tiers everyone ignores.
- Fake scarcity, fictitious "was" prices, drip-revealed fees, monetised inertia.
- A wide, unexplained pocket-price band; announced increases never measured.

## Check yourself

Try these before you look at the answers below.

1. A prepaid card delivers benefits a customer values at £30 a year. It costs £8 a
   year to serve, and the next best alternative costs the customer £20. Where do
   cost, value and competition sit on the value stick, and in what band is the
   price actually chosen?
2. You want two prices for the same euros: a keener rate for people who order
   online three days ahead, and the board rate for walk-ups. What is the fence,
   which degree of price discrimination is it, and what makes it a good fence?
3. Customer A values a rate lock at £8 and home delivery at £2. Customer B values
   them at £2 and £8. What do single per-item prices capture, and what does a £10
   bundle do?

**Answers.** (1) Cost £8 is the floor, willingness to pay £30 is the ceiling, and
the £20 alternative is the reference point. The price is chosen between £8 and £30
with £20 as the anchor. Capturing 50 to 70% of the £10 of extra value over the
alternative points at roughly £25 to £27. (2) The fence is time plus channel, an
advance online order. It is second degree discrimination because the customer
sorts themselves. It is a good fence because it cannot be arbitraged (you cannot
un-walk-in), it correlates with willingness to pay (planners compare more), and
it reads as fair. (3) At £8 each, each customer buys one item and you sell two
units for £16. At £2 each you sell four units for £8 and leave money on the
table. A £10 bundle sells to both for £20, because bundling shrinks the spread of
willingness to pay across the bundle. It works best when valuations are
negatively correlated and the marginal cost is low.
