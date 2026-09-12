# 14 · The Question Bank — the best Q&As from the whole repo, in one place

*(Distilled from the case study's interview Q&A, the panel notebooks' 60-second
answers, and the behavioural story bank — now at
`workspace/notes/interview_story_bank.md`.
Each answer here is the **short version** — the pointer takes you to the
full treatment. Drill these out loud.)*

## How to use this file

Cover the answer. Say yours out loud. Compare. The goal is not memorising
words — it's that the *shape* of each answer (diagnose → method → judgement
→ caveat) becomes your reflex.

---

## A. Technical — elasticity and causality

**A1. "Your elasticity estimate came out positive. What happened?"**
> Almost certainly endogeneity: we raise prices when demand is strong, so
> high prices sit next to high volumes in the data. "Prices went up and so
> did sales" measures our own pricing reflex, not customer behaviour. Fix
> with an experiment, or an instrument like the wholesale cost.
> *(School 03 §6 · notebook N9 shows our own algorithm creating this bias)*

**A2. "Why not just add more control variables instead?"**
> Controls remove confounding you can *measure*. They can't fix price
> reacting to demand shocks you *can't* measure — that needs randomisation
> or an instrument. "Just add controls" is the classic trap answer.
> *(Case study §3.4)*

**A3. "What makes a good instrument for price?"**
> Two properties: it genuinely moves the price (testable — strong first
> stage), and it affects demand *only through* the price (an argument from
> domain knowledge, never testable). Wholesale cost shocks are the classic
> FX instrument.
> *(Case study §3.2)*

**A4. "The model says raise the price to the cap. Do you?"**
> A corner solution is a warning, not an answer. Either the segment is
> genuinely inelastic — in which case competition and fairness are the real
> constraints — or the elasticity is biased toward zero. Validate with an
> experiment before shipping.
> *(School 03 §5 · case study §8)*

**A5. "How do you estimate elasticity for 11,500 branches × 60 currencies?"**
> Hierarchically. Most cells are too thin to stand alone, so each cell
> borrows strength from its cluster — shrinkage in proportion to its own
> noise. It's credibility theory in modern clothes, and it also kills the
> multiple-testing problem, because noise gets shrunk before anyone builds
> a narrative on it.
> *(Notebook N2)*

## B. Technical — testing and measurement

**B1. "Sales rose 8% after the price change. Did it work?"**
> Against what? If controls rose 5%, my effect is 3 points and the rest is
> market. I'd never present a before/after without a control group — the
> market moves for everyone.
> *(School 06 §2 · notebook N5's holdout)*

**B2. "The CI crosses zero — so no effect, right?"**
> No — a blurry photo of a cat isn't evidence there's no cat. At this test's
> power, a true +2% would 'fail' most of the time. I'd report the range, the
> probability the effect is positive, the expected value, and the bounded
> downside — then decide, rather than verdict-ise.
> *(School 05 §4–5 · notebook N4 — drill this one hardest)*

**B3. "Design a price test across the branch network."**
> Cluster-randomise at travel-to-work-area level, not branch — customers
> cross-shop, and branch-level tests overstate lift by counting stolen
> volume as created. Buffer the borders, compute the minimum detectable
> effect before starting, and use each branch's own baseline to sharpen it.
> *(School 06 §3–5 · notebook N1)*

**B4. "How do you keep measuring once the model sets the prices?"**
> Keep a small permanent randomised stream — a few percent of traffic at
> random in-corridor prices. Otherwise the model's own logs stop containing
> clean variation, and next year's elasticity is calibrated on this year's
> habits. It costs under a percent of profit; it's the cheapest insurance
> the system buys.
> *(Notebook N9)*

## C. Technical — models in production

**C1. "GLM or machine learning for the rate card?"**
> Both, in their lanes: the GLM is the auditable rate card regulators and
> committees can read; ML finds what the GLM misses, and the findings get
> folded back in. The sophistication should live in validation, not the
> headline.
> *(School 12 §4 · notebook N10's simplicity premium)*

**C2. "How do you validate a pricing model?"**
> Out-of-time above all: train on the past, test on the most recent months —
> pricing data drifts, and shuffled-split results flatter. Then lift/AUC
> over accuracy (base rates mislead), and a check that performance doesn't
> collapse on any one segment.
> *(School 12 §6)*

**C3. "How do you know the model's gone stale?"**
> Drift monitoring on the inputs (PSI with the usual 0.1/0.25 traffic
> lights), rolling predicted-vs-actual on the outputs, and *decision* drift
> — recommended prices creeping toward the cap. Pre-agreed retraining
> triggers and a static fallback price.
> *(School 12 §8)*

**C4. "Permutation importance or SHAP?"**
> Permutation for a quick global sanity scan; SHAP when a human needs
> convincing — it gives direction and per-customer explanations, which is
> what a committee or a complaint response actually needs.
> *(School 12 §7)*

**C5. "What's capping and why does pricing care?"**
> Two kinds: cap the *inputs* so an outlier can't bend the model, and cap
> the *outputs* — price floors/ceilings and a max step per change, so no
> customer gets a jump the business can't defend. The second is also a
> regulatory matter (price-walking).
> *(School 12 §5)*

## D. Commercial judgement

**D1. "You have 8 weeks to show value. What do you do?"**
> A leakage audit before any model: build the pocket-price waterfall, size
> each giveaway, fix the biggest governance-shaped ones, and prove it with a
> holdout. A 1% improvement in realised price is worth ~11% of operating
> profit — and clean prices make every later analysis more trustworthy.
> *(School 04 · notebook N5)*

**D2. "A competitor undercuts us at 50 branches. Response?"**
> Diagnose first — promotional or structural? Hold through a promo. If
> structural: non-price levers everywhere (stock, service, buyback), price
> defence only where branch elasticity clears break-even, and measure with
> matched twins. Never blanket-match — that hands them our pricing pen.
> *(School 08 · notebook N8)*

**D3. "Should the card be priced against cash?"**
> As a portfolio, never as SKUs. A card price cut's gross uplift is roughly
> half cannibalised cash; and its real job may be defensive — retaining
> customers who'd otherwise leave for the fintechs — which only shows
> against the *declining* counterfactual, not today's baseline.
> *(Notebook N7)*

**D4. "Walk-up rates are worse than online and the network is complaining."**
> Part of the differential is justified by cost and elasticity. The check
> that matters is the mix: if the walk-up premium concentrates on
> vulnerable, less-digital customers, that's the pocket of poor value the
> FCA says averages disguise. Narrow or mitigate there; and fix the network
> issue by crediting collections to branches — socialised before anything
> changes publicly.
> *(School 07 §3 · notebook N6)*

**D5. "Sterling drops 5% overnight — this morning?"**
> Hedge book first — that's what makes it a process, not a panic. Reprice
> off the *new* wholesale holding margin in bps; never chase competitors'
> stale screens. Sequence by channel latency, honour every locked order,
> re-check the comparison-site rank at T+4, and re-run the cash plan for the
> demand spike.
> *(Notebook N11)*

**D6. "We stock out of euros every Friday. Charge more on Fridays?"**
> Ops first: Friday 'sales' are censored — the till never records the
> customer we turned away — and forecasts trained on them spiral the stock
> down. Fix the forecast (free), then logistics; price only a residual hard
> cap, modestly, because the Friday walk-up is a captive customer and
> surge-pricing them is a fair-value risk.
> *(School 09 · notebook N3)*

## E. Behavioural — the three stories to have ready

From the repo's behavioural banks, the three that matter most for a senior
pricing seat (prepare each in STAR shape — Situation, Task, Action, Result):

1. **"I was wrong and adapted."** Own a real failure and the specific change
   you made. Candidates who own failures beat candidates who blame the
   market — this is the strongest single signal panels report.
2. **Cross-functional scar tissue.** A pricing/model change you got
   *implemented* through a resistant function (sales, network, IT) — with
   the pre-wiring, the concession you made, and what shipped.
3. **The bridge-builder.** Aligning stakeholders with conflicting KPIs
   around one solution (the repo's own version: Head of Pricing wanted
   profitability, Head of DS wanted out-of-time reliability, model-risk
   wanted compliance — the shipped solution let each call it a win).

**Red-flag phrases to never say:** "it wasn't significant so it didn't
work" · a single elasticity quoted as gospel · "we'd start by building a
model" (before data/leakage) · taking credit for a market tailwind · only
"I", never "we".

## F. The five case-study stories (rehearse cold, in STAR shape)

Each maps to a file/figure in
[`../engine/README.md`](../engine/README.md):

1. **"Our elasticity was wrong and it was costing us margin."** OLS said
   inelastic (even positive) because we surge margin in peak season; IV with a
   wholesale-cost instrument showed digital ε ≈ −2.2. Pricing on the biased
   number loses ~45% of profit.
2. **"The headline FX margin lies about channel profitability."** Post Office:
   biggest gross revenue, ~45% paid away in commission; digital drops ~96% of
   revenue to contribution. Price the net; position each channel by its own
   elasticity.
3. **"Uniform moves destroy value; targeted ones create it."** A blanket +10%
   margin *reduces* contribution; harvesting only the inelastic channels lifts it.
4. **"We found — and fixed — a Consumer Duty fair-value problem."** Vulnerable
   customers paid ~1.7pp more for lower benefit, driven by inactivity fees;
   documented it, recommended fee caps and balance returns.
5. **"I can defend the AOP under scrutiny."** Elasticity-aware scenarios + a
   bridge attributing every pound to volume/price/mix/competitor — including a
   price-war downside.

## G. One-line answers to the classic questions

| If they ask… | Say… |
|---|---|
| "How do you find the right price?" | Value sets the ceiling, cost the floor, competitors the reference; estimate elasticity *causally*; optimal margin ≈ 1/\|ε\|. |
| "Is our demand elastic?" | "Depends on the segment/channel — and you must *measure* it causally, because raw data understates how price-sensitive customers are." |
| "Should we raise prices 10%?" | "Where? Harvest the inelastic segments, compete in the elastic ones, size it in £ of profit — a blanket move is usually the wrong tool." |
| "A competitor cut prices — match?" | "First quantify the £ we'd actually lose, then respond selectively in the contested segment — matching everywhere bleeds margin." |
| "Most important number in pricing?" | "The causal elasticity — it sets the optimal markup, the discount break-even and the competitor response, and it's the one most often wrong." |

**Technical gotchas they may probe:** Lerner `(P−c)/P = 1/|ε|` valid for
|ε|>1 · discount break-even `d/(CM−d)` · why OLS is biased toward inelastic ·
DiD needs parallel pre-trends · the Bertrand trap · NRR > 100%. (All in the
glossary's formula cheat-sheet, [The glossary](../appendix/glossary.md).)

**Questions to ask them (signals seniority):** How is pricing governed — CoE,
embedded, or hub-and-spoke? · How do you estimate demand response today —
experiments or judgement? · How mature is the fair-value process for the
prepaid book? · Where's the biggest known leakage — commission, discounting, or
mix? · How do Pricing, Finance (AOP) and Compliance relate?

**Logistics:** bring the case-study repo as the portfolio and offer to walk one
figure; lead with the commercial outcome, support with method; name the
limitations (synthetic data, identification caveats) — honesty about gaps reads
as senior.

---

**Full versions:** every panel notebook ends with a 60-second spoken
answer and three pushed-deeper follow-ups —
[`README.md`](README.md) maps them to questions.
The case-study Q&A is in
[`../_archive/fastpay_payments/dynamic_pricing_and_elasticity_case_study.md`](../_archive/fastpay_payments/dynamic_pricing_and_elasticity_case_study.md) §8.
