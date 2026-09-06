# 13 · The Commercial Side — KPIs, stakeholders, and getting decisions through

*(The "commercial track" of this school. Technique gets you into the room;
this file is what senior pricing people are actually judged on. Distilled
from the repo's interview notes, the practitioner deep-dive, and the master
prompt's tacit-skills sections — aimed squarely at the Senior Manager,
Pricing, Distribution & Revenue job description.)*

**The bridge in:** every tool in this file has a Part 1 ancestor. The
revenue bridge is File 04's price–volume–mix formalised; conversion and rank
KPIs carry File 03's elasticity through File 12's model; contribution and
pocket margin are Files 01 and 04; fair-value MI is File 07 made a standing
report; and the "reversible experiment with guardrails" framing that gets
decisions through committee is File 05's expected-value-plus-bounded-downside,
spoken aloud. If a KPI here feels abstract, walk it back to its file.

## 1. The KPI dictionary — with real-world feel for the numbers

**Volume & competitiveness**
- **Conversion rate** — quotes that become sales. The direct read on
  competitiveness. Real-world feel (from insurance comparison-site
  businesses): ~4–8% on a comparison site is healthy, under 2–3% is weak;
  direct channels run higher; **renewal/retention ~75%+**. Know the feel —
  quoting a plausible range instantly signals you've done the job.
- **Rank / price position** — where you sit on the comparison site. Often
  matters more than your absolute rate (customers click the top few).
- **Market share** — competitive context for everything else.

**Money**
- **GWP / revenue** — top line: volume × price. Growth here says nothing
  about profit — always pair it with margin.
- **Contribution & pocket margin** — Files 01 and 04. The pair that stops
  "record revenue!" from hiding a margin collapse.
- **Combined ratio** (insurance's favourite): claims paid + expenses, as a
  share of premium earned. **Below 100% = underwriting profit.** The FX
  cousin: cost-to-serve + commission + hedging as a share of spread revenue.
- **CLV (customer lifetime value)** — total profit over the whole
  relationship. The number that justifies losing a little today to keep a
  customer for years (File 07's retention logic; the card's defensive role).

**Plan-keeping (straight from the JD)**
- **AOP (annual operating plan)** — the year's promised numbers, by line
  (e.g. new card sales / reloads / in-life revenue). You will be asked "are
  we on plan, and if not, why?" — the answer is a **revenue bridge**: volume
  effect + price effect + mix effect + competitor effect (File 04, formalised).
- **Fair-value MI** — the standing fairness report (File 07): outcome
  distributions by customer group, vulnerable-customer checks, remediation
  status. Under Consumer Duty this is a KPI pack, not a one-off.

## 2. Stakeholders — pricing touches everyone's targets

Pricing is political because every function's bonus points a different way:

| Stakeholder | What they want | What they fear | Speak to them in |
|---|---|---|---|
| Sales / network / Postmasters | volume, footfall, easy tills | being undercut by your own website | conversion, footfall, branch credit for collections |
| Finance / CFO | margin, plan certainty | volume bought with margin | contribution, bridge vs AOP, bounded downside |
| Marketing | share, headlines ("0% commission!") | ugly rates on comparison sites | rank, acquisition cost, CLV |
| Ops / cash logistics | simplicity, stable plans | pricing spikes wrecking stock plans | stockouts, forecast accuracy (File 09) |
| Compliance / risk | documented fairness | surprises and complaints | fair-value MI, guardrails (Files 07, 12) |
| Data science | clean tests, model health | being asked to bless dirty reads | MDE, holdouts, OOT performance (Files 06, 12) |

Real example of the balancing act (from this repo's author's own notes):
the Head of Pricing wanted profitability and competitive edge; the Head of
Data Science wanted out-of-time reliability; model risk wanted compliance
evidence. The solution that shipped was the one framed so **each** could
call it a win — "the final solution was not just my solution; it was *our*
solution."

## 3. How pricing decisions actually get made (and die)

Most pricing recommendations die in committee. The ones that pass share
five habits:

1. **Pre-wire.** Walk every key stakeholder through it one-to-one *before*
   the meeting. Nobody important should be surprised in the room — surprised
   people defend themselves; briefed people help you.
2. **Bring one shared fact base** (the waterfall, the bridge) so the debate
   is about the *action*, not whose numbers are right.
3. **Frame it as a reversible experiment with guardrails**, not a bet:
   "80% rollout, 20% holdout, rollback trigger at −X%." Reversibility melts
   opposition — you're not asking anyone to be wrong forever (File 05 §5).
4. **Pre-empt the loss-aversion objection.** Executives fear volume loss
   more than they value margin gain. Answer "what if volume drops?" *before*
   it's asked: the elasticity evidence, the floor, the rollback.
5. **Lose small battles on purpose.** Concede the visible discount the sales
   director loves; bank the credibility for the structural fix (approval
   tiers) that actually moves the P&L (File 04).

And when the CEO wants a price move for non-analytical reasons: don't fight
it head-on. Quantify it, offer the *bounded, phased* version with an
off-ramp if the data turns, and keep both the relationship and the evidence.

## 4. Talking to each audience — one result, three tellings

The margin test from File 05 (+2%, range crossing zero, P(positive)=90%):

- **To the CFO:** "Best estimate +£1m a year; a 90% chance it's
  margin-accretive; worst case is capped at ~£150k by an 8-week rollback.
  I recommend rolling out with the holdout kept on."
- **To the network:** "Rates change Tuesday; here's the one-pager for the
  counter, collections still credit to your branch, and if the local rate
  looks wrong ring this number — nothing else changes for you."
- **To compliance:** "Fair-value assessment updated; the differential
  narrows for assisted orders; monitoring adds a vulnerable-outcomes cut;
  here's the documented rollback trigger."

Same fact. Three languages. That is most of the senior job.

## 5. The first 90 days in a pricing seat (the classic playbook)

- **Days 1–30 — listen and diagnose, change nothing.** Stakeholder tour
  (every row of the section-2 table). Data audit: can we even run a clean
  test (File 06)? **Leakage audit** (File 04). Fair-value review (File 07).
  Map the competitive position.
- **Days 31–60 — structure and early wins.** Fix one or two leaks *with a
  holdout to prove it*. Stand up a lightweight pricing forum (cadence,
  guardrails, decision rights) so pricing stops being everyone's second job.
  Draft the test roadmap.
- **Days 61–90 — elevate.** Present the diagnosis + roadmap: what I found,
  what I fixed, what next quarter delivers. Secure the measurement
  investment. Establish fair-value MI as standing output. Co-design one
  change *with* the network — credibility you'll spend all year.

The theme: **diagnose before you prescribe, and land something small and
provable before proposing anything big.**

## 6. Check yourself

**Q1.** Revenue is up 6% vs plan but contribution is flat. Using this file's
vocabulary, what are the two most likely stories, and what analysis names
the culprit?

**Q2.** Your price recommendation is analytically airtight and gets rejected
in committee. List three process mistakes (not maths mistakes) that likely
killed it.

**Q3.** The sales director demands a visible cut to a rate their team hates.
Your data says it's mildly value-destroying but small. What does the
"lose battles" principle say — and what do you ask for in exchange?

---

### Answers

**A1.** Either **mix** shifted to low-margin channels/products, or the
volume was **bought with margin** (discounting/leakage). The **revenue
bridge** (volume/price/mix/competitor decomposition) names which.

**A2.** Nobody was pre-wired (a key stakeholder felt ambushed); it was
framed as a permanent bet instead of a reversible, guard-railed experiment;
and the "what if volume drops" fear was left unanswered instead of
pre-empted with the floor and rollback.

**A3.** Concede it — visibly and graciously — and bank the credit for the
structural ask: the approval-tier / leakage-governance change that's worth
10× the giveaway. (And put a small holdout behind the cut anyway, so the
cost of the concession gets measured, not argued about.)

---

**When you're ready for more:** the master prompt's Part 4.5–4.6
([`../../interview/FRES_MASTER_PREP_PROMPT.md`](../../interview/FRES_MASTER_PREP_PROMPT.md))
carries the full tacit-skills layer; the AOP machinery is runnable in
[`../fast_transaction_services/aop_scenario.py`](../fast_transaction_services/aop_scenario.py).
