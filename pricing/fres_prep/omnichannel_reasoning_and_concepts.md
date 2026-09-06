# How the One-Pager Was Built — Reasoning, Maths, and Concepts to Learn

This companion explains the thinking behind [omnichannel_one_pager.md](omnichannel_one_pager.md): the chain of reasoning a pricing manager runs through, the small amount of maths that carries the whole argument, and the concepts to learn (with pointers into the pricing school files) so you can reproduce this reasoning on any similar question.

---

## Part 1 — Decoding the question

Executive questions like this are never really "yes or no." Read it again and notice it contains **four separate questions**:

1. **Judgement:** would you recommend it? (They want a position, not a survey.)
2. **Risk awareness:** do you understand what differential pricing is *for*, i.e. what you'd be giving up?
3. **Delivery skill:** how would you sequence it? (Can you turn strategy into a plan with decision points?)
4. **Analytical maturity:** what data would you ask for *and why*? (Do you know what drives the answer, or do you just want "all the data"?)

The trap in the question is the false binary. A candidate who says a flat "yes — simplicity and trust!" ignores the economics. A candidate who says a flat "no — margin destruction!" ignores strategy, brand and regulation. The professional answer is almost always **conditional and sequenced**: commit to a direction, stage the journey by risk, and put measurement gates between the stages. That is what the one-pager does.

A second, subtler trap: "no data pack" is not an obstacle, it's part of the test. They want to see whether you can reason **structurally** first (what *must* be true for this to be a good idea?) and then name the data that would confirm or kill each condition. Structure first, data second.

---

## Part 2 — The reasoning chain, step by step

### Step 1: Ask *why* the price differences exist in the first place

Never recommend removing a structure before you know why it's there (Chesterton's fence). Differential prices in FX cash exist for two economically distinct reasons:

**Reason A — costs differ by channel.**
Serving a customer in a branch involves staff time, physical cash inventory, secure logistics (banknotes must be bought, transported, insured, and idle stock earns nothing). Serving a customer online involves platform costs and delivery. Buying £5,000 in one transaction costs far less *per pound* to serve than fifty £100 transactions — which is exactly why volume tiers exist.

**Reason B — customers differ by channel in how price-sensitive they are.**
An online customer has a comparison site open in another tab; their demand is highly **elastic**. A branch customer walked in while doing their shopping; they are buying convenience and trust, and their demand is relatively **inelastic**. Charging a higher margin where demand is inelastic and a lower one where it is elastic is textbook **third-degree price discrimination** — and it is profit-maximising. (See `pricing_school/03_elasticity.md` and `07_segments_and_fairness.md`.)

This gives you the first honest sentence of the analysis: *the current structure is not an accident — it is (roughly) the profit-maximising arrangement.* Therefore:

### Step 2: The key static result — a single price can only lose money *in the static model*

Write profit with channel-specific prices:

    Profit = Σᵢ  qᵢ(pᵢ) × (pᵢ − cᵢ)

where i runs over channels/segments, qᵢ(pᵢ) is demand in segment i, and cᵢ its unit cost-to-serve. Choosing each pᵢ freely and choosing one common p are the same optimisation problem except the single-price version has an added constraint (p₁ = p₂ = … = p). **Adding a constraint can never increase the maximum.** So in a static world, moving to one price weakly reduces profit — full stop.

This is the mathematically honest core of the answer, and it forces the right follow-up question: **if the static model says "never," the case for doing it must come from things outside the static model.** That's not a loophole; it's where the real strategic content lives:

1. **The demand curves themselves may shift.** "One honest rate everywhere" is a marketable trust proposition. If it shifts q(p) outward (more customers, at the same price), the static comparison no longer applies. This is a *brand* effect, and it is uncertain — which is exactly why the one-pager insists on a pilot.
2. **Costs fall.** Running one price is operationally cheaper: simpler systems, simpler training, fewer pricing errors, no channel-conflict management, simpler governance.
3. **Regulatory risk falls.** Under the FCA's **Consumer Duty**, firms must show products deliver fair value, and unexplained price differences for identical products (same banknotes!) are increasingly hard to defend — especially geographic variation, which pattern-matches to the "loyalty penalty" pricing practices the FCA has attacked in insurance. Removing that risk has real, if hard-to-quantify, value.
4. **Competitive positioning.** A single transparent rate is a differentiator against competitors who obfuscate (e.g. "0% commission" with a wide spread). See `pricing_school/08_competition_basics.md`.

So the recommendation structure writes itself: **static economics says cost, strategic/dynamic effects say benefit, and the honest answer is "yes if the dynamic effects are big enough — so let's measure them before completing the move."**

### Step 3: Quantify the trade with one back-of-envelope formula

The Executive doesn't need calculus; they need the break-even condition. Suppose in some part of the book we cut the margin rate from m to m·(1−x) (e.g. x = 10% margin give-up). Old profit per unit ∝ m; to hold profit flat we need volume to grow by factor g where

    (1 + g) × m(1 − x) = m   ⟹   g = x / (1 − x) ≈ x   for small x.

But careful — that's the give-up as a fraction *of margin*. If instead you think in terms of price: cutting the *customer price* of FX by Δp basis points costs you Δp of margin directly, and the required volume uplift is

    required volume growth ≈ Δp / (margin in bp − Δp)

Example: margin is 300bp on a currency online vs 500bp in branch. Harmonising at 400bp gives branch customers 100bp back. Required branch volume growth to break even ≈ 100/(500−100) = **25%**. That is a big ask — and now the elasticity question ("do branch customers respond that much?") stops being academic and becomes the single number the entire decision hangs on. This is why "evidence of price responsiveness by channel" is the most important line in the data ask.

The same arithmetic run in the other direction (raising the online rate toward the middle) uses the online elasticity, which is *high*, so volume losses there can be severe. That asymmetry — inelastic branch customers get a gift they didn't need, elastic online customers get a price rise they will punish — is the precise mechanism behind "gives away branch margin *and* makes us uncompetitive online, most likely both at once" in the one-pager. (Maths background helps here: this is just evaluating one function, revenue response, at two points with very different local slopes.)

### Step 4: Mix effects — where the single price "lands" matters

The single rate must sit somewhere in the interval [cheapest current rate, dearest current rate]. The P&L impact is a **mix-weighted** sum: for each cell (channel × currency × tier × location), impact ≈ volume share × margin change × (1 + volume response). This is why the very first ask is the **margin heatmap by cell** — you cannot even locate the least-damaging landing point without it. (See `04_price_volume_mix_and_leakage.md` for price/volume/mix decomposition.)

It also yields the sequencing principle: **remove differences in increasing order of margin-at-risk.** Geographic variation typically earns the least and offends fairness the most → do it first. Channel differential earns a lot and is elasticity-justified → pilot it. Volume tiers are cost-justified *and* chosen by the customer (anyone can buy more to get the better rate — it's self-selection, not discrimination) → defend or do last.

### Step 5: Convert uncertainty into a pilot, not an opinion

The decision hinges on two numbers nobody in the room knows: branch-customer elasticity and the size of the trust/brand uplift. When a decision hinges on an unknown behavioural response, the professional move is **test-and-learn**: harmonise a few currencies or regions, hold others as controls, and read the volume response (difference-in-differences against the control group; see `06_tests_and_experiments.md` and `05B_causal_inference_primer.md`). This converts "recommend yes/no" into "recommend a cheap way to find out" — which is nearly always the right executive recommendation under uncertainty.

Sequencing also has an **options logic**: each stage is reversible-ish and buys information before the next, bigger commitment. Stage the spend of irreversibility. Full harmonisation announced with fanfare is very hard to walk back ("we're bringing back higher branch rates" is a terrible press release), so it must go last, after the pilot has de-risked it.

### Step 6: The data ask — one line of data per line of reasoning

Notice every item in the one-pager's data list maps to exactly one step above. That mapping *is* the answer to "why":

| Data asked for | Which step of the reasoning it feeds |
|---|---|
| Margin by channel × currency × tier × location | Step 4: locate the landing point, rank differences by margin-at-risk |
| Historic price-response evidence | Step 3: the elasticity that decides break-even |
| Cost-to-serve by channel | Step 1/2: the floor for the single rate; same price ≠ same profit |
| Competitor rates by channel | Step 2 (competition corridor): the rate must stay inside what the market bears |
| Customer overlap between channels | Step 3: distinguishes market growth from the same customer switching channel (cannibalisation) |
| Cost of running differential pricing | Step 2, benefit #2: the savings that offset margin dilution |
| Fair value assessment | Step 2, benefit #3: the regulatory case |

If you can produce that mapping on demand, you'll never pad a data request again — and interviewers can tell.

---

## Part 3 — Concepts to learn (the curriculum behind this answer)

In rough order of importance for reproducing this reasoning:

1. **Price elasticity of demand** — the % volume change per % price change; the single number the whole decision turns on. Know why elasticity differs by channel/segment (search costs, switching costs, salience of comparison). → `pricing_school/03_elasticity.md`
2. **Price discrimination (1st/2nd/3rd degree)** — the economics of why firms charge different prices for the same thing. Channel pricing = 3rd degree (segment-based); volume tiers = 2nd degree (self-selection via menu). The classic result: optimal margin is higher where elasticity is lower (the inverse-elasticity / Lerner rule: (p−c)/p = 1/|ε|). This is what makes "remove all differentials" a provably costly constraint in the static model. → `07_segments_and_fairness.md`
3. **Constrained optimisation intuition** — adding constraints never raises a maximum. You don't need Lagrange multipliers in the room; you need the one-sentence version and the discipline it imposes: *the benefits must therefore come from outside the static model.*
4. **Break-even / margin-volume arithmetic** — required volume uplift = margin give-up ÷ remaining margin. Do these in your head, in basis points, since FX margins are quoted in bp. → `01_price_cost_profit.md`, `02_percentages_and_basis_points.md`
5. **Price/volume/mix decomposition** — how a portfolio P&L change splits into price, volume and mix effects; why the mix-weighted heatmap is the first data ask. → `04_price_volume_mix_and_leakage.md`
6. **Cost-to-serve** — same price with different costs still means different profit by channel; cash logistics, inventory holding, staff time vs delivery. Know why "one price" and "one margin" are different statements.
7. **Competition and price corridors** — the feasible band for the single rate is set by competitors channel by channel: comparison sites bound the online rate, local bureaux bound branch rates. → `08_competition_basics.md`
8. **Test-and-learn / causal inference** — pilots with control groups, difference-in-differences, why a before/after comparison is not evidence (FX volumes move with seasons, travel demand and the interbank rate). → `06_tests_and_experiments.md`, `05B_causal_inference_primer.md`
9. **Consumer Duty and fair value (FCA)** — the regulatory frame: firms must evidence fair value; unexplained differential pricing for identical products is under scrutiny; the insurance "loyalty penalty" ban (GIPP, 2022) is the precedent everyone in UK pricing knows. This turns "fairness" from a soft word into a hard risk line.
10. **Behavioural pricing / salience** — headline rate vs total cost, "0% commission" framing, why transparency can be a *competitive weapon* rather than just a cost. → `19_channels_promotions_competition.md`
11. **Sequencing under uncertainty (real-options thinking)** — stage decisions so cheap, reversible steps buy the information needed for expensive, irreversible ones; put explicit decision gates between stages.
12. **Cannibalisation vs market growth** — when online volume rises after harmonisation, is it new customers or your own branch customers walking out and clicking? Only customer-level overlap data can tell you, and the profit consequences are opposite.
13. **Executive writing** — one page means: recommendation in the first paragraph, one piece of arithmetic the reader can retell, numbered plan with gates, data ask where every line has a "why." Notice the one-pager never uses the words "elasticity," "third-degree price discrimination," or "difference-in-differences" — the concepts are all there, in plain English. That translation skill is the job. → `13_commercial_kpis_and_stakeholders.md`

### A reusable template for "should we simplify pricing?" questions

1. Why does the current structure exist? (cost-based vs elasticity-based differences)
2. Static cost of the constraint (it's never zero — say so honestly).
3. Dynamic benefits that could outweigh it (demand shift, cost savings, regulatory risk, competitive positioning).
4. Break-even arithmetic linking 2 and 3.
5. Sequence by margin-at-risk, cheapest/most-defensible-to-remove first.
6. Pilot the uncertain middle; gate the irreversible end.
7. Data ask = one line per step above.

That template answers this question — and also "should we scrap promotions?", "should we end student discounts?", "should we align UK and EU prices?", and most of their cousins.
