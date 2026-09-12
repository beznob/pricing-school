# 3.4 · Explaining pricing charts in English

A working guide to saying what a chart means, in a room where the people
listening decide things.

Everything here is built on the eight charts in `pricing_charts.py`, and every
number is Meridian's own. Build them first:

```bash
python create_database.py     # once
python pricing_charts.py      # eight charts into charts/, plus the narration
```

This document is about the **words**. `pricing_charts.py` holds the script for
each specific chart; this holds the patterns those scripts are built from, so
you can write your own.

---

## 1. The sentence is the deliverable

The most common failure in a pricing meeting is not a wrong number. It is a
correct chart that nobody acts on, because the analyst narrated the axes
instead of making a claim.

> **What people say:** "So this shows contribution by channel. On the y-axis
> we've got contribution, and along the bottom we've got our three channels,
> and as you can see there are some differences between them."
>
> **What to say:** "Online sells 43% of our orders and earns 17% of our
> contribution. It keeps 32p of every revenue pound; the branch keeps 82p."

The first version contains no information the audience could not read for
themselves. The second contains a claim, three numbers, and an implied
question — *why?* — which is the question you want them to ask, because you
have the answer.

**The rule: a chart title and an opening sentence are the two most expensive
lines in your deck. Never spend either on a description of the axes.**

### The four parts

Every chart you present needs four things prepared. Not written on the slide —
prepared, in your head or on a card.

| Part | What it is | How long |
|---|---|---|
| **Headline** | The claim. Said before anyone looks at the chart. | One sentence, under 8 seconds |
| **Read** | How to walk them through the marks, in order. | 20–40 seconds |
| **Ask** | The questions this will provoke, and your answers. | Prepared, not spoken |
| **Caveat** | What the chart cannot tell you. **You** say it, early. | One sentence |

`Chart.script()` in `pricing_charts.py` prints all four for any chart. Read one
out loud before your next meeting; that is the exercise.

---

## 2. Writing the headline

A headline is a **claim**, in the present tense, containing at least one
number, and short enough to say without breathing.

### The three shapes that work

**Shape 1 — the gap.** Two numbers that should match and don't.

> Online sells 43% of our orders and earns 17% of our contribution.

> A 10% rate cut needs 14% more orders on the high street and 46% online.

> Our trading history says we lose 12% of demand per point of rate. The
> randomised test says 39%.

**Shape 2 — the survival.** What is left after everything takes its cut.

> We keep 86p in the pound on the high street and 36p online.

> £18.54 of board rate becomes £4.73 of pocket margin.

**Shape 3 — the hidden cost.** A number that never appears in a report.

> Every point of rate above the market costs 12% of that customer's trips
> next year.

> One August branch-day in five hit the cash limit. On those days sales
> measured our stock, not our customers.

### Before and after

| Weak | Strong | Why |
|---|---|---|
| Contribution analysis by channel | Online is 43% of orders and 17% of contribution | Claim, not category |
| Online has lower margins | Online keeps 32p in the pound; the branch keeps 82p | Two numbers beat one adjective |
| Discounting can be risky | A 10% cut online needs 46% more orders to break even | Names the risk in units |
| There may be an elasticity issue | The history says −12% per point; the experiment says −39% | Says which number is wrong |
| Price increases affect retention | A point of rate costs 12% of next year's trips | Cause, effect, magnitude |
| August data quality concerns | In August we do not know what demand was — we ran out of cash | Says what is actually wrong |

Notice what the strong column never does: it never uses **may**, **might**,
**could potentially**, **it seems that**, or **there are concerns around**.

---

## 3. Narrating the chart out loud

Once the claim has landed, walk them through the evidence. Three rules.

### Rule 1 — point at marks, in an order, and say why each one

Bad: "As you can see, there's quite a lot going on here."

Good:

> "Point at the first bar and the last bar, in that order. Bar one is orders —
> that is the shape of the business people carry in their heads. Bar four is
> contribution — that is the shape of the business that pays for the business."

The phrase **in that order** is doing real work. An audience reads a chart in
whatever order their eye lands; you are choosing the order for them.

### Rule 2 — perform the arithmetic, don't describe the bars

A waterfall is a sentence with numbers in it. Say the sentence.

> "We start at £18.54 of board rate on a typical branch order. The card fee
> adds 86p. Funding costs us £1.16, the payment fee £1.02, handling £1.33.
> We keep £15.89."

Not: "There are several cost lines here, and you can see the biggest one is
handling."

### Rule 3 — let the comparison land on its own

Do not tell people what to feel about a number. Put the two numbers next to
each other and stop talking.

> "Same starting point, near enough — £13.27. Then the payment fee takes £4.58
> and the courier takes £2.98. We keep £4.73."
>
> *(pause)*

The pause is part of the sentence. If you fill it with "which is obviously
a big problem", you have taken the conclusion away from them, and people
defend conclusions they reached themselves.

### Verbs that do the work

English gives you a precise verb for almost every move a number makes. Using
the right one saves you a clause.

| Instead of | Use | When |
|---|---|---|
| goes up / goes down | rises, falls | a level over time |
| goes up by a lot | climbs, jumps, doubles | large or fast change |
| goes down by a lot | falls away, halves, collapses | large or fast change |
| stays the same | holds, is flat, does not move | no change — say it plainly |
| is different from | diverges from, breaks away from | two series separating |
| is the same as | tracks, moves with | two series together |
| makes money | earns, contributes, returns | profit language |
| costs money | costs us, takes, leaks | cost language |
| is caused by | is driven by, comes from | attribution |
| shows | says, tells us | *"the chart says"* is stronger than *"shows"* |

**Collocations worth memorising** (these pair naturally in business English;
other combinations sound wrong even when grammatical):

- margin — *thin, healthy, under pressure, erodes, holds up*
- price — *keen, competitive, premium, holds, moves, comes off*
- volume — *soft, robust, holds up, falls away*
- costs — *scale with, sit in (another budget), come off the top*
- demand — *responds, softens, holds, is price-sensitive*
- a discount — *we run one, it lands, it converts, it costs us*

> Meridian examples: "The branch waterfall is flat because its costs barely
> **scale with** the order." · "The courier contract **sits in** another
> department's budget." · "Last-minute demand **holds** even at 6.34pp."

---

## 4. The words pricing people confuse (and stakeholders notice)

These pairs are the ones that quietly destroy credibility. Get them right and
you sound like you have done the job before.

### turnover vs revenue vs contribution vs profit

| Word | At Meridian | Never say |
|---|---|---|
| **turnover** | £60.6m — the currency the customer hands over. Not ours at any point. | "we turned over £60m" as a boast |
| **gross revenue** | £2.3m — the spread we charged. Our top line. | "revenue" when you mean turnover |
| **contribution** | £1.51m — revenue minus every variable cost. The number for a price decision. | "profit" |
| **profit** | contribution minus fixed costs. Not in any chart here. | "contribution" when the room hears "profit" |

The trap: someone proposes "a 1% discount". **One percent of which one?** Off
turnover that is £606k and wipes out a quarter of the business. Off revenue it
is £23k. People genuinely mean different things. Make them say which.

> **The sentence:** "Before we go further — 1% of turnover or 1% of revenue?
> They are £606k apart."

### percent vs percentage point

This is the single most common numerical error in pricing meetings, and it is
always expensive.

- Our margin goes from **3.6pp to 4.0pp**. That is a rise of **0.4 percentage
  points**, or **11 percent**.
- Saying "we put the margin up 0.4%" when you mean 0.4pp understates the move
  by a factor of twenty-eight.

**Rule: rates change by percentage points; quantities change by percent.**
Meridian's margins are rates (pp). Meridian's volumes are quantities (%).

> ✅ "The experiment added 0.40pp to the rate and cost us 9.6 percentage points
> of conversion — a 16% fall in demand."

Notice that sentence uses both correctly and marks the difference explicitly.
That is worth doing every time.

### margin vs markup

- **Margin** is over the price. **Markup** is over the cost.
- A 60% margin is a 150% markup. They are never the same number.
- If someone says "a 50% margin" and you compute from cost, you will be 33%
  wrong on every price you set.

> **The sentence:** "Just to check we mean the same thing — is that 50% of the
> price, or 50% on top of the cost?"

### price vs rate vs spread

At Meridian the customer never sees a "price" — they see an exchange rate. Our
price is the **spread**: the gap between the wholesale rate and the rate we
quote, measured in percentage points. Say **rate** or **spread**, not "price",
in front of anyone commercial. It signals you know the product.

### elasticity vs semi-elasticity

- **Elasticity** is % change in quantity per **%** change in price.
- **Semi-elasticity** is % change in quantity per **percentage point** of
  margin. This is what Meridian uses, because our price is a rate.
- Meridian's number is **−39% per pp** (online, from the experiment). It is
  *not* "an elasticity of −39", which would be an absurd figure.

> **Say:** "Our semi-elasticity online is minus 39% per percentage point. So
> 0.4pp on the rate costs us about 16% of demand."

### correlation language vs causal language

Use the weaker verb when the evidence is observational. This is not hedging —
it is accuracy, and the room can tell the difference.

| Evidence | Verb to use |
|---|---|
| Randomised experiment | **caused, cost us, delivered** |
| Controlled regression | **is associated with, is consistent with** |
| Raw cross-tab | **moves with, tracks, appears alongside** |

> ✅ "The test **cost us** 9.6 points of conversion." (randomised)
> ✅ "Customers priced above the market **came back** less — I would not call
> that causal on its own." (observational)

---

## 5. Saying numbers out loud

Written numbers and spoken numbers are different registers. On a slide, be
precise; in the sentence, round.

| On the chart | In the sentence |
|---|---|
| £92,582 | "about ninety-three thousand" |
| 46.39% | "forty-six percent" or "about half again" |
| 0.4639 | never say a decimal out loud — convert it |
| £1,190,252.75 | "one point one nine million" |
| −6.85% | "just under seven percent" |
| 3.669pp | "three and two-thirds of a point" or "3.7" |

**Ratios beat percentages when the number is large.** "46% more orders" is
harder to hold than "half again as many orders". "82p in the pound" is easier
than "a contribution margin of 81.9%".

**Give a number a size, not just a value.** "£10,148" means nothing on its own.
"£10,148 — about a tenth of what volume gave us" means something.

**Never read a table aloud.** If a table is on screen, say the one row that
matters and let them read the rest.

---

## 6. Uncertainty: hedging vs calibration

Non-native speakers are often taught to soften claims to sound polite. In a
commercial meeting this backfires: softening reads as *not knowing*, and the
room stops listening. What you want instead is **calibration** — a firm claim
with its limits named.

### Hedging (avoid)

> "The data seems to suggest that online might potentially be somewhat less
> profitable, although of course there are a number of factors involved and it
> would probably be worth looking into it further."

Twenty-nine words, no number, no claim, no next step. The speaker sounds
unsure of something they actually know.

### Calibration (use)

> "Online earns 32p of contribution on every revenue pound. The branch earns
> 82p. The gap is the courier and the card fee, not the rate — and this is
> contribution, so no fixed costs are in it."

Firm claim, two numbers, the cause, and the limit. **The caveat makes it
sound stronger, not weaker,** because it shows you know where the edge is.

### Sentence frames for calibration

- "**The number I would plan on is** 39% per point. **The number I would not
  defend is** anything below 25%."
- "**This is solid for** online cash. **It is not measured for** the airport,
  and I would not carry it across."
- "**What would change my mind is** a second experiment at the kiosk."
- "**I am confident about the direction and not the size.** The interval runs
  from 7 to 12 points of conversion."
- "**We can bound this, not measure it.** August demand is understated and we
  do not know by how much — which is itself the finding."

That last frame is worth learning by heart. "We do not know, and here is
exactly what we do not know" is a finding, and it is far stronger than a
confident guess.

---

## 7. Handling the questions

Most questions in a pricing meeting are one of six types. Learn the shape of
each and you stop being surprised.

### Type 1 — "So should we just do X?" (the leap)

They have jumped from your chart to a decision. Do not say "no".

> **Frame:** *Agree with the observation, redirect to the mechanism.*
>
> Q: "So should we shut the online channel?"
> A: "The gap is real — but online still earns £254k of contribution we would
> lose. What the chart says is that the cost to serve is structural, so the
> lever is the courier contract, not the rate board."

### Type 2 — "Is that number right?" (the challenge)

Never defend. Give the provenance and the check.

> **Frame:** *Where it came from, how it was checked, what would break it.*
>
> Q: "The experiment is only 4,624 quotes. Is that enough?"
> A: "For this size of effect, yes. The 95% interval on the drop runs from 6.7
> to 12.4 points — wide, but comfortably clear of zero. If we needed to tell
> 30% from 39% we would need roughly ten times the sample."

### Type 3 — "What about Y?" (the missing factor)

If they are right, say so immediately and completely. It costs you nothing and
buys the rest of the meeting.

> **Frame:** *Yes, and here is how much it would move.*
>
> "You're right that mix isn't in this. I ran it — split by channel the mix
> effect is minus nine pounds. It genuinely didn't move."

If they are wrong, still start with what is right about the question.

### Type 4 — "Can you just..." (the scope grenade)

> **Frame:** *What it would take, and what it would displace.*
>
> "I can. It is about two days, because the segment cut needs the quote table
> rather than transactions. That would push the airport hurdle work to the
> following week — is that the right trade?"

### Type 5 — "I don't think that's what we're seeing" (the disagreement)

Do not repeat your point louder. Find the specific thing you disagree about.

> **Frame:** *Locate the disagreement, then propose the test.*
>
> "I think we agree on the numbers and disagree on which one to plan from. You
> are reading the trading history, which says 12% per point; I am reading the
> experiment, which says 39%. If that is the disagreement, the way to settle it
> is a second experiment at the kiosk, and I can have it designed this week."

That reply does three things: it takes the heat out, it names the actual
disagreement, and it ends with an action. Learn this one.

### Type 6 — silence

Silence usually means "I have not understood and will not say so". Rescue it
without embarrassing anyone.

> "Let me put that a different way. For every pound of revenue we take online,
> 68p goes straight back out in fees and courier. On the high street it is 18p."

---

## 8. Saying no, and pushing back

Pricing managers say no more often than almost any other commercial role. In
English, the strength of a refusal lives in the **structure**, not in stronger
words. Soften the framing; keep the content hard.

| Too soft (invites a rerun) | Right | Too hard (makes an enemy) |
|---|---|---|
| "I'm not sure that would really work" | "That needs 46% more orders. The most we've measured is 16%, so I can't make that add up." | "That's wrong." |
| "It might be a bit difficult" | "I can do it, but not by Thursday. What would you like me to drop?" | "There's no time." |
| "Maybe we could look at it" | "Not on this evidence. Give me a two-week test and I'll have an answer." | "We don't have the data." |

**The reliable structure:** *acknowledge the goal → name the constraint in
numbers → offer the path.*

> "I understand we want the volume. A 10% cut needs 46% more orders online and
> the largest response we have ever measured is 16%, so this specific move
> loses money. If the goal is online volume, the delivery charge is the lever
> I would pull — that is £2.98 an order and it is not a rate change."

Never say "impossible". Say what it would take.

---

## 9. Tables for stakeholders

A table is a chart that has given up on making a point — unless you make it
make one.

**Six rules:**

1. **Sort by the column that carries the argument**, not alphabetically and
   not by ID. If the point is contribution, sort by contribution.
2. **Put the punchline column last**, on the right, where the eye stops.
3. **One decision per table.** If you need two, make two tables.
4. **Round in the table too.** `0.4639` is not a number a human can hold;
   `+46%` is.
5. **Say the units in the header**, never in the cells: `contribution (£/order)`
   not `£15.89` repeated forty times.
6. **Say one row out loud** and let them read the rest. Never read a table.

Compare the same query, presented two ways:

```
channel   orders  revenue_gbp  contribution_gbp  contribution_margin
online     53632    803815.44         253820.92               0.3158
branch     48183    934809.10         765675.53               0.8191
airport    22863    559634.92         494326.70               0.8833
```

```
Channel   Orders   Revenue    Contribution   Kept per £
airport   22,863   £560k      £494k          88p
branch    48,183   £935k      £766k          82p
online    53,632   £804k      £254k          32p        ← the row
```

Same data. The second sorts by the argument, rounds to what a person can hold,
renames `contribution_margin` to the thing it actually means, and marks the
row you are going to talk about.

`toolkit.py` has formatting helpers for the £ and pp columns.

---

## 10. The written version

Charts get presented once and forwarded ten times. Whatever you say in the
room has to survive in writing without you.

**The one-pager, in order:**

1. **The claim**, as a sentence. Same headline you would say out loud.
2. **The number**, with its unit and its provenance in the same line.
3. **The chart**, with the headline as its title.
4. **What it means for the decision in front of us** — two sentences.
5. **What would change the answer** — one sentence.

Nothing else. No methodology section, no data caveats paragraph, no appendix
of things you tried. Those go below a horizontal rule, or in the model.

**Email subject lines** follow the same rule as headlines — claim, not topic:

| Weak | Strong |
|---|---|
| Channel profitability analysis | Online: 43% of orders, 17% of contribution |
| Q1 pricing experiment results | Rate test: +0.4pp cost us 16% of online demand |
| Discount request — online | 10% off online needs 46% more orders; recommend no |

That last one gives the recommendation in the subject line. If the reader only
sees the subject, they still have your answer.

---

## 11. Drills

Do these against the real charts. They take fifteen minutes and they work.

**Drill 1 — the eight-second headline.**
Build the charts. Cover the scripts. For each chart, write one sentence with a
number in it. Time yourself saying it. Over eight seconds means it has two
ideas in it; split it.

**Drill 2 — narrate blind.**
Open a chart, cover its `read` block, and narrate it out loud to an empty room
for thirty seconds. Then uncover and compare. The gap is what you did not
actually understand.

**Drill 3 — answer before reading.**
Open a chart's `ask` block, cover the answers, and answer each question out
loud. If you cannot, you do not know the chart yet — go back to the query.

**Drill 4 — the hostile read.**
Take any chart and argue against your own headline for one minute. Whatever
you come up with is what the room will come up with, so it belongs in your
`caveat` before they say it.

**Drill 5 — kill the hedges.**
Write a paragraph about a chart the way you naturally would. Then delete every
instance of: *seems, appears, might, may, could, potentially, somewhat, quite,
rather, a bit, arguably, it is possible that, there are concerns around*. Read
what is left. Restore only the words that were carrying real uncertainty —
usually one or two, not fifteen.

**Drill 6 — translate the decimal.**
Take any output from `db_helper` and say every number in it out loud as you
would in a meeting. `0.3158` becomes "about a third". `0.4639` becomes "half
again". `-0.0685` becomes "just under seven percent". This is the single
fastest way to stop sounding like you are reading a spreadsheet.

---

## 12. Where each chart fits

| Chart | The meeting it belongs in | The one sentence |
|---|---|---|
| `contribution` | Channel strategy, budget | Online is 43% of orders and 17% of contribution |
| `waterfall` | Cost-to-serve, margin recovery | 86p in the pound on the high street, 36p online |
| `hurdle` | Any discount request | 10% off online needs 46% more orders |
| `elasticity` | Rate reviews, planning | The history says 12% per point; the test says 39% |
| `retention` | Annual pricing, lifetime value | A point of rate costs 12% of next year's trips |
| `segments` | Segmentation, fairness review | One rate, four different businesses |
| `bridge` | Year-end, performance review | The growth was volume; rate went backwards |
| `stockouts` | Demand planning, data quality | In August we do not know what demand was |

---

## Further reading in this folder

- **`pricing_charts.py`** — the eight charts, and the full script for each.
- **`01_finance_for_pricing.md`** — the finance behind every number quoted here.
- **`pricing_finance.py`** — the formulas, runnable, with doctests.
- **`db_helper.py`** — the queries the charts are built from.
- **`../appendix/database_usage.md`** — the star schema and the SQL worth having.
