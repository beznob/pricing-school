# The finance a pricing manager is expected to know

Every formula here is implemented, with a worked example, in
[`pricing_finance.py`](pricing_finance.py). Read this for the reasoning; run
that for the arithmetic:

```bash
python pricing_finance.py                 # a guided tour on real Meridian figures
python -m doctest pricing_finance.py -v   # every number in this file, checked
```

The numbers throughout are Meridian FX's own, from `data/` (built by
`01_data_foundation.ipynb`). Nothing here is illustrative-only.

---

## 0. The three numbers people confuse, settled first

| Number | What it is | Meridian, per average order |
|---|---|---|
| **Turnover** | The value of currency handed across the counter | **£478** |
| **Gross revenue** | The spread we charged on it | **£17.60** |
| **Contribution** | What is left after the cost of serving that order | **£10.22** |

Turnover is not ours. We hand over €560 and take £478; the business earns the
**spread**, and the £478 is a number that belongs on a compliance report, not
a P&L. Meridian turns over **£85m** a year and books **£3.1m** of revenue.

This matters the first time someone says "let's do 1% off". One percent of
turnover is £850k and destroys nearly half the contribution of the business.
One percent of revenue is £31k. **Both people in the room think they are being
clear.** Make them say which.

The general rule: a pricing decision is made in **contribution**, reported in
**revenue**, and constrained in **turnover**. Know which one you are holding.

---

## 1. Margin is not markup

> `margin_pct` · `markup_pct` · `margin_to_markup` · `price_from_margin`

**Margin** is a share of the price. **Markup** is a share of the cost.

```
margin = (price − cost) / price          markup = (price − cost) / cost
```

A branch euro order books £18.19 of revenue and costs £6.19 to serve. That is
a **66% margin** and a **194% markup** — the same money, and the second number
sounds four times better on a slide.

The expensive version of the confusion is in *setting* a price:

```
to hit a 60% margin:   price = cost / (1 − 0.60) = £15.47      ← divide
"cost plus 60%":       price = cost × 1.60       = £9.90       ← multiply
```

The second delivers a **37% margin**, not 60%. Margin targets divide; markup
targets multiply. If you memorise one line from this document, that is it.

---

## 2. Which costs belong in a price decision

> `contribution` · `contribution_margin` · `break_even_volume`

A price decision is a decision about **one more order**. So only costs that
change when that order happens belong in it.

| | Meridian | In a price decision? |
|---|---|---|
| **Variable** | funding the currency, card/cash handling fee, counting and AML, courier, **commission to the host retail network** | **Yes** |
| **Fixed** | branch equipment, insurance, training, head office, compliance, treasury (£30k/month) | **No** |

Fixed costs are **irrelevant to the optimal price and decisive for whether a
site should exist.** Both halves matter.

The classic error is allocating central overhead onto an order and then
refusing any price below the result. The overhead is paid either way; a
rejected order contributes nothing towards it. Allocation is an accounting
convention, not a cost — `dim_cost_stack` says so in as many words.

**Contribution margin by channel** is where the whole business becomes legible:

| Channel | Revenue/order | Variable cost | Contribution | **CM** | Break-even orders/month |
|---|---|---|---|---|---|
| airport | £22.10 | £4.59 | £17.51 | **79%** | 286 (on £5,000 fixed) |
| branch | £18.02 | £6.27 | £11.75 | **65%** | 60 (on £700 fixed) |
| online | £14.76 | £10.18 | £4.58 | **31%** | 1,310 (on £6,000 fixed) |

Online carries a 0.9% card fee and a £4.50 courier against the thinnest
spread. That is why "one price across all channels" (notebook 12) is a hard
question rather than an obvious one.

---

## 3. The discount trade — the formula you will use most

> `discount_break_even_volume` · `price_rise_break_even_volume`

Someone asks you for a discount roughly weekly. The question is never "should
we?" in the abstract; it is **"how much more do we have to sell to be no worse
off?"** That has an exact answer:

```
volume uplift needed  =   d / (CM − d)          for a discount of d
volume loss affordable = −r / (CM + r)          for a price rise of r
```

both as shares of revenue. A 10% rate cut:

| Channel | CM | **Must sell** | A 10% *rise* survives |
|---|---|---|---|
| airport | 79% | **+14.4%** | −11.2% |
| branch | 65% | **+18.1%** | −13.3% |
| online | 31% | **+47.6%** | −24.4% |

Same discount. Three completely different asks, purely because of the cost to
serve underneath. `db.discount_hurdles()` computes this straight from the data.

Two things follow, and they are the backbone of the job:

1. **The trade is not symmetric.** A rise always buys more room than a cut
   costs, because the money drops straight to contribution.
2. **A hurdle is not a decision.** It tells you what it would take. Only an
   *estimate of demand* tells you whether you clear it — which is why the next
   section exists, and why notebooks 03, 05, 06 and 07 are all about getting
   that estimate honestly.

---

## 4. Elasticity, and the price it implies

> `arc_elasticity` · `semi_elasticity` · `optimal_margin_from_elasticity`

**Elasticity** is the % change in volume per 1% change in price. Below −1 the
demand is *elastic* and a price rise loses revenue; between −1 and 0 it is
*inelastic* and a rise gains revenue.

**Semi-elasticity** — % volume per **margin point** — is the unit a desk
actually speaks in, because boards move in basis points. Meridian's true
figures:

| Segment | %/pp | Why |
|---|---|---|
| `last_minute` | **−5.1** | airside, day-before; no realistic alternative |
| `holiday_family` | **−23.0** | buying currency as a chore |
| `frequent_flyer` | **−29.9** | values speed, but shops |
| `bargain_hunter` | **−50.9** | will switch app for 30bp |

One board rate, four demand curves. The overall −25.5% is not "the" elasticity
of anything — it is a *mix*, and the mix changes when you move the price.

**The Lerner rule** turns an elasticity into an implied price:

```
at the profit-maximising price:   (P − MC) / P  =  1 / |elasticity|
```

The most useful sanity check in pricing: compare the implied margin to the one
you run. Below it, you are leaving money on the table; above it, volume is
worth more than the extra points.

Two warnings, both load-bearing:

- **Watch how violently it moves.** Between elasticity −2.5 and −1.4 the
  optimal price *doubles*. The **uncertainty** in your estimate matters more
  than its point value, which is why notebook 08 optimises over a distribution
  and why a confidence interval belongs on every elasticity you present.
- **Its assumptions are strong**: one product, one segment, no competitive
  reaction, no effect on repeat purchase. Meridian breaks all four. Use the
  rule to *frame* an argument, never to set a board.

### The reason a two-point elasticity is nearly always wrong

The price you observe **was set by someone reacting to the demand you are
trying to measure.** Meridian's board went *up* in August, when demand was
strongest, so the price rises sit on top of the demand peaks and partly cancel
themselves out. Regress branch conversion on the board rate and you get
**−7% per margin point**; the truth is **−28.7%**. Four times too small, in the
direction that makes a rate rise look nearly free.

Slice by segment instead and it gets worse — bargain hunters convert worst on
the *keenest* rates, because the pricing rule already discounts to them. Taken
at face value that is a *positive* price elasticity: raise prices, sell more.

Nothing about the arithmetic is at fault; the *correlation is not the effect*. Every technique in notebooks 06 and 07 —
randomisation, difference-in-differences, instrumental variables — exists to
solve that one problem.

---

## 5. The two tables you will build in every job

### The price waterfall

Board rate down to what actually reaches the pocket. Two real orders, from
`db.price_waterfall('branch')` and `db.price_waterfall('online')`:

```
                          branch            online
board rate                £18.54  100.0%    £13.27  100.0%
plus rate adjustments      £0.00  100.0%     £0.05  100.4%
plus ancillary fees        £0.86  104.6%     £1.67  112.9%
= gross revenue           £19.40  104.6%    £14.99  112.9%
less funding cost          £1.16   98.4%     £1.15  104.2%
less payment fee           £1.02   92.9%     £4.58   69.7%
less handling              £1.33   85.7%     £1.54   58.1%
less delivery              £0.00   85.7%     £2.98   35.6%
= pocket margin           £15.89   85.7%     £4.73   35.6%
```

Three readings, and none of them is available from an average:

- **The biggest leaks are not prices.** Online, the payment fee (£4.58) and the
  courier (£2.98) together take more than the entire spread on a branch order.
  Both are *negotiated, not engineered*, and both sit in another department's
  budget. The cheapest margin point available to Meridian is not a price
  change at all.
- **The ancillary fee is revenue.** The travel card's £4.95 fee is why both
  waterfalls have an upward step. Fees are a lever people forget they own, and
  they are usually far less elastic than the headline rate. A waterfall with an
  upward step is not a mistake, and hiding one is how a business loses track of
  its ancillary income.
- **Rate adjustments are nil here — check before you assume.** Meridian's
  promotions move the average board rate by 5p online and nothing at all
  elsewhere. In most businesses this line is the largest one on the chart,
  because discounts stack: nobody approves a 13% cut, but three people each
  approve a small one. Meridian is not that business, and the way you find out
  is by drawing the line and looking at it.

Build it at *order* level and then look at the spread. The average waterfall
hides the tail, and the tail is where the money is — the small online orders
lose money outright once the £2.98 courier is on them.

### The price–volume–mix bridge

"Revenue is up 7.4%" is not an answer to "how did pricing do?". Meridian
2024 → 2025, from `db.revenue_bridge()`:

| Effect | £ | Meaning |
|---|---|---|
| volume | **+92,582** | we served 8.4% more orders |
| mix | −185 | nothing: the product split did not move |
| price | **−10,148** | we charged 0.9% less per order |
| **total** | **+82,249** | 2024 £1.108m → 2025 £1.190m |

So the honest read is that the business grew and pricing was slightly
dilutive. That is not a bad year — £93k of volume for £10k of rate is a trade
worth making — but it is the opposite of what "revenue up 7.4%" implies, and
saying it before anyone else does is the difference between a pricing function
that gets funded and one that gets audited. Present it in this order and
nobody claims volume growth as a pricing win either.

Bridge contribution as well as revenue, whenever you can. Contribution grew
6.7% against revenue's 7.4%: the growth we took was slightly poorer quality
than the base, and on a revenue bridge that gap is invisible.

State the caveat when you show it: "price" here is average revenue per order,
so it moves when the mix *within* a product moves. There is no completely
clean bridge; there are only bridges whose residual you have named.

---

## 6. The correction that makes optimisers honest

> `customer_lifetime_value` · `retention_multiplier` · `lifetime_value_of_a_price_move`

Everything above treats an order as a one-off. Meridian's 14,000 customers
come back about twice a year, and **how they were treated last summer changes
whether they come back at all.** A static optimiser cannot see that, so it
always recommends a price that is too high.

Meridian's actual behavioural rule, the one notebook 01 simulates and notebook
08 has to rediscover:

```
retention multiplier = clip(1 − 0.12 × max(margin above market, 0)
                              − 0.15 × refused for stock,  0.5, 1.2)
```

Every point above the best market rate costs about **12% of next year's
trips**. Being *keener* than the market buys nothing back — an asymmetry worth
knowing before you promise one.

Run a 0.5pp branch rise both ways:

| | |
|---|---|
| in-year contribution | **+£46,319** |
| lifetime value | **−£437,290** |
| **total** | **−£390,970** |

The static number is the one the P&L will show and the one your optimiser will
recommend. **Bring both.**

Why the second is ten times the first is the actual lesson: a retention *rate*
enters lifetime value geometrically. Cutting it from 0.75 to 0.705 takes 11%
off the margin multiple, on every future year, for every customer. **Small
permanent damage to repeat rate outweighs a large one-off gain whenever
customers are loyal.**

Which means the conclusion is only as strong as the retention assumption, so
state it and test it:

| Retention | Lifetime value | Total |
|---|---|---|
| 75% | −£437,290 | −£390,970 |
| 55% | −£138,263 | −£91,943 |
| 40% | −£63,620 | −£17,301 |

At 40% the case is nearly a wash. Find out which business you are in **before**
you make the argument.

Two assumptions are doing real work and belong on the slide: the move is
**permanent** (so the penalty applies every future year), and the volume
response is the **immediate** one — retention is on top of it, not part of it.

**And note where this points.** The August stockouts cost 15% of retention — a
refused customer is a bigger loss than a dear one — and stock is an operations
budget, not a pricing lever. Some of the most valuable work a pricing manager
does is proving the problem is not pricing.

---

## 7. Money over time

> `discount_factor` · `npv` · `payback_period`

A pricing investment costing £50k now and returning £20k a year for three
years, at a 10% cost of capital:

- undiscounted: **+£10,000**, a clear winner
- **NPV: −£263**, marginally value-destroying
- payback: **2.5 years**

The time value of money ate all of it. *"It pays back in under three years"* is
not the same claim as *"it creates value"*, and committees ask for the first
while meaning the second. Quote payback next to NPV, never instead of it.

Ask finance for the discount rate; do not invent it. A high rate makes the
business short-termist by construction — worth naming out loud when a retention
argument gets waved away.

---

## 8. Putting it in front of a committee

> `PriceMove` · `margin_of_safety`

```
Online +25bp
  contribution today      £183,200
  contribution after      £219,303
  change                  £+36,103  (+19.7%)
  volume hurdle           -22.0%   (need no worse than this)
  volume expected         -6.6%
  verdict                 clears the hurdle
```

The **hurdle** line ends arguments: it is the volume loss the move survives,
computed from the cost to serve, and it does not care whose opinion is in the
room.

The **margin of safety** — expected minus required — is what should actually
decide it. A move needing +48% while expecting +20% is 28 points short and no
forecast error explains that away. A move with 15 points of room survives an
elasticity estimate being somewhat wrong. Since your elasticity always *is*
somewhat wrong, the safety margin beats the point estimate every time.

---

## The order to learn this in

| Want | Read | Run |
|---|---|---|
| The vocabulary | §0–2 above | `python pricing_finance.py` |
| What the business earns | §2 | `db.pnl()`, `db.unit_economics()` |
| To answer "can we discount?" | §3 | `db.discount_hurdles()` |
| To estimate demand honestly | §4 | notebooks 03, 05, 06, 07 |
| To explain a number to a board | §5 | `db.price_waterfall()`, `db.revenue_bridge()` |
| To price for the long run | §6 | notebook 08, `db.retention_by_price()` |
| The whole job at once | — | **notebook 12** |

Two habits are worth more than any formula on this page:

1. **Estimate before you look.** `data/truth.json` holds the real parameters.
   Write your number down first — the skill being built is judging whether
   your own estimate is trustworthy, and you cannot practise that with the
   answer on screen.
2. **Say which number you are holding.** Turnover, revenue, contribution,
   lifetime value. Most pricing arguments are two people being right about
   different quantities.
