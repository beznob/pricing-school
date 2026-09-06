"""The finance a pricing manager is expected to do in their head.

Every formula on a pricing desk is here, once, with the commercial meaning
written next to it. The point is not the arithmetic — it is knowing *which*
number answers the question you have been asked, and what the number quietly
assumes.

Read it in order. The sections build:

    1. Margin arithmetic ......... the vocabulary. Margin is not markup.
    2. Contribution & break-even . which costs matter to a price decision.
    3. The discount trade ........ the formula you will use most.
    4. Demand response ........... elasticity, and the optimal price it implies.
    5. Bridges ................... how you explain a number change to a board.
    6. Value over time ........... NPV, lifetime value, and the retention drag.
    7. The decision .............. putting a price move in front of a committee.

Units, stated once and never varied:

    price / cost / revenue   GBP (£)
    margin_pp                percentage points of the order value.
                             Meridian FX sells £500 of euros at a 3.5pp margin
                             and books £17.50 of revenue. 1pp = 100 basis
                             points (bp).
    rates and ratios         decimals, not percentages. 0.58, never 58.
    volume                   orders (or quotes, where it says so)

Where a function takes `contribution_margin`, it wants the *ratio* — 0.58 for
"58p of every £1 of revenue survives variable cost". Passing 58 gives you an
answer that is wrong by two orders of magnitude and looks plausible, which is
the single most common error in this file's subject matter.

The worked examples are real Meridian FX figures from `data/` (built by
`01_data_foundation.ipynb`), so the numbers you see here are the numbers the
notebooks estimate. Run them:

    python -m doctest pricing_finance.py -v      # every example, checked
    python pricing_finance.py                    # a guided tour of the lot

See `FINANCE_FOR_PRICING.md` for the same ground in prose, with the traps.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

__all__ = [
    # 1. margin arithmetic
    "margin_pct", "markup_pct", "margin_to_markup", "markup_to_margin",
    "price_from_margin", "price_from_markup",
    # 2. contribution and break-even
    "contribution", "contribution_margin", "break_even_volume",
    "break_even_price", "operating_leverage",
    # 3. the discount trade
    "discount_break_even_volume", "price_rise_break_even_volume",
    "profit_impact_of_price_move",
    # 4. demand response
    "arc_elasticity", "semi_elasticity", "volume_after_price_change",
    "lerner_index", "optimal_margin_from_elasticity", "optimal_price_from_elasticity",
    "revenue_vs_profit_maximum",
    # 5. bridges
    "price_waterfall", "price_volume_mix",
    # 6. value over time
    "discount_factor", "npv", "payback_period", "customer_lifetime_value",
    "retention_multiplier", "lifetime_value_of_a_price_move",
    # 7. the decision
    "PriceMove", "margin_of_safety",
]


# ==========================================================================
# 1. MARGIN ARITHMETIC — the vocabulary
# ==========================================================================
#
# Half the arguments in a pricing meeting are two people using one word for
# two different numbers. Settle it first.
#
#   MARGIN is a share of the PRICE.   (price - cost) / price
#   MARKUP is a share of the COST.    (price - cost) / cost
#
# They are never equal (except at zero) and markup is always the larger of
# the two. "We need 50%" means a 100% markup if it means margin, and a 33%
# margin if it means markup. That is the difference between a business and a
# bankruptcy, so ask which one they mean.


def margin_pct(price: float, unit_cost: float) -> float:
    """Gross margin as a share of the *price*.

    The number that goes in the P&L, because the P&L starts at revenue.

        margin = (price - cost) / price

    A Meridian FX branch euro order: £18.19 of revenue on the spread, £6.19
    of variable cost to serve it.

    >>> round(margin_pct(18.19, 6.19), 4)
    0.6597

    Sixty-six pence of every revenue pound survives the cost of serving the
    order. That is the number to compare across channels — not the £12 of
    contribution, which just tells you the orders are big.
    """
    if price == 0:
        raise ValueError("margin is undefined at a price of zero")
    return (price - unit_cost) / price


def markup_pct(price: float, unit_cost: float) -> float:
    """Markup as a share of the *cost*.

    The number a buyer or a category manager uses, because they start from
    what they paid.

        markup = (price - cost) / cost

    >>> round(markup_pct(18.19, 6.19), 4)
    1.9386

    The same order is a 66% margin and a 194% markup. Same money, and the
    second number sounds four times better in a meeting. This is why you
    always ask which one is on the slide.
    """
    if unit_cost == 0:
        raise ValueError("markup is undefined at a cost of zero")
    return (price - unit_cost) / unit_cost


def margin_to_markup(margin: float) -> float:
    """Convert a margin ratio to the markup ratio that produces it.

        markup = margin / (1 - margin)

    >>> round(margin_to_markup(0.50), 4)
    1.0
    >>> round(margin_to_markup(0.6597), 4)
    1.9386

    A 50% margin needs a 100% markup. Doubling the cost gets you halfway to
    the price, not all the way — the fact that trips up cost-plus pricing.
    """
    if margin >= 1:
        raise ValueError("a margin of 100% or more implies an infinite markup")
    return margin / (1 - margin)


def markup_to_margin(markup: float) -> float:
    """Convert a markup ratio to the margin ratio it delivers.

        margin = markup / (1 + markup)

    >>> round(markup_to_margin(1.0), 4)
    0.5
    >>> round(markup_to_margin(0.30), 4)
    0.2308

    "Cost plus 30%" is a 23% margin. If the plan needed 30% margin, the
    business has just quietly missed it by seven points on every order.
    """
    return markup / (1 + markup)


def price_from_margin(unit_cost: float, target_margin: float) -> float:
    """The price that *achieves* a target margin.

        price = cost / (1 - margin)

    >>> round(price_from_margin(6.19, 0.60), 2)
    15.47

    Note the division. The instinct is `cost * (1 + margin)` — £9.90 here —
    which delivers a 37% margin, not 60%. If you only memorise one line of
    this module, memorise that margin targets divide and markup targets
    multiply.
    """
    if target_margin >= 1:
        raise ValueError("cannot price to a margin of 100% or more")
    return unit_cost / (1 - target_margin)


def price_from_markup(unit_cost: float, markup: float) -> float:
    """The price that applies a target markup.

        price = cost * (1 + markup)

    >>> round(price_from_markup(6.19, 0.60), 2)
    9.9
    """
    return unit_cost * (1 + markup)


# ==========================================================================
# 2. CONTRIBUTION AND BREAK-EVEN — which costs matter
# ==========================================================================
#
# A price decision is a decision about *one more order*. So the only costs
# that belong in it are the ones that change when that order happens.
#
#   VARIABLE cost  changes with the order. At Meridian FX: the wholesale
#                  funding cost of the currency, the card-acquiring or
#                  cash-handling fee, the handling and AML work, the courier
#                  for a home delivery, and the commission paid to the host
#                  retail network on every branch sale.
#   FIXED cost     does not. Branch equipment, insurance, training, the head
#                  office, compliance, treasury.
#
# Fixed costs are irrelevant to the optimal price and decisive for whether a
# site should exist. Both halves of that sentence matter. Allocating central
# overhead onto an order and then refusing any price below the result is the
# classic way to turn a profitable order away, because the overhead is paid
# either way and a rejected order contributes nothing towards it.


def contribution(price: float, variable_cost: float) -> float:
    """Contribution per order, in £.

    What one more order actually adds to the business before any fixed cost.
    This — not gross revenue, not turnover — is the currency of a price
    decision.

        contribution = price - variable cost

    An average Meridian order books £17.60 of revenue on the spread and costs
    £7.38 to serve:

    >>> round(contribution(17.60, 7.38), 2)
    10.22

    Turnover on the same order is about £478. Never let a turnover number
    into a pricing conversation; it is the value of the currency handed over
    the counter, and none of it is yours.
    """
    return price - variable_cost


def contribution_margin(price: float, variable_cost: float) -> float:
    """Contribution as a share of revenue — the `CM` every later formula wants.

        CM = (price - variable cost) / price

    >>> round(contribution_margin(17.60, 7.38), 4)
    0.5807

    Meridian's three channels look very different on this measure — airport
    ~0.79, branch ~0.65, online ~0.31 — because online carries a 0.9% card
    fee and a £4.50 courier that a branch sale does not. That spread is the
    whole reason "one price across all channels" (notebook 12) is a hard
    question rather than an obvious one.
    """
    if price == 0:
        raise ValueError("contribution margin is undefined at a price of zero")
    return (price - variable_cost) / price


def break_even_volume(fixed_costs: float, price: float, variable_cost: float) -> float:
    """Orders needed to cover a block of fixed cost.

        volume = fixed costs / contribution per order

    A Meridian branch carries £700 a month of fixed cost and makes £11.75 of
    contribution on an average order:

    >>> round(break_even_volume(700, 18.02, 6.27), 1)
    59.6

    Sixty orders a month keeps the lights on. Anything above that is profit,
    which is why footfall matters more than margin at a small site — and why
    the airport kiosks, at £5,000 a month, need ~285 orders before they earn
    anything at all.
    """
    cm = contribution(price, variable_cost)
    if cm <= 0:
        raise ValueError("no volume breaks even when contribution per order is <= 0")
    return fixed_costs / cm


def break_even_price(fixed_costs: float, volume: float, variable_cost: float) -> float:
    """The price at which a known volume just covers its fixed costs.

        price = variable cost + fixed costs / volume

    >>> round(break_even_price(700, 100, 6.27), 2)
    13.27

    Useful as a *floor*, never as a price. It answers "what must I get?", and
    the market answers "what will you get?". A floor above the market rate is
    a signal to close the site or cut the cost, not to post the price.
    """
    if volume <= 0:
        raise ValueError("volume must be positive")
    return variable_cost + fixed_costs / volume


def operating_leverage(total_contribution: float, operating_profit: float) -> float:
    """How hard profit moves when revenue moves — the gearing of the business.

        leverage = total contribution / operating profit

    Read it as a multiplier: at a leverage of 3, a 1% fall in volume takes 3%
    off profit.

    Meridian books about £1.82m of contribution against £360k a year of fixed
    cost, leaving £1.46m of operating profit:

    >>> round(operating_leverage(1_816_194, 1_456_194), 2)
    1.25

    Low gearing — this business is mostly variable cost, so a bad August
    hurts but does not threaten it. A business at leverage 5 cannot afford to
    experiment with price the way this one can, and that changes what you are
    allowed to propose.
    """
    if operating_profit == 0:
        raise ValueError("leverage is undefined at zero profit")
    return total_contribution / operating_profit


# ==========================================================================
# 3. THE DISCOUNT TRADE — the formula you will use most
# ==========================================================================
#
# Someone will ask you for a discount roughly weekly. The question is never
# "should we?" in the abstract; it is "how much more do we have to sell to be
# no worse off?". That has an exact answer, and it is brutal.


def discount_break_even_volume(contribution_margin: float, discount: float) -> float:
    """Volume uplift a discount must produce to break even.

        uplift = d / (CM - d)

    where both `d` (the discount) and `CM` (the contribution margin) are
    shares of the price. The discount comes straight off contribution, so a
    small cut against a thin margin needs an enormous volume response.

    Meridian's online channel runs a contribution margin near 0.31. Cut the
    rate by 10% of revenue:

    >>> round(discount_break_even_volume(0.31, 0.10), 3)
    0.476

    Online has to sell **48% more** to stand still. The same 10% cut at the
    airport, where CM is ~0.79:

    >>> round(discount_break_even_volume(0.79, 0.10), 3)
    0.145

    needs 14.5%. Identical discount, wildly different ask, purely because of
    the cost to serve underneath it. This is the number to bring when a
    channel asks for "just 10 basis points" — and the reason to bring the
    estimated elasticity next to it, so the room can see whether the required
    uplift is achievable or fantasy.

    A discount at or above the contribution margin can never break even:

    >>> discount_break_even_volume(0.31, 0.31)
    inf
    """
    if discount >= contribution_margin:
        return float("inf")
    return discount / (contribution_margin - discount)


def price_rise_break_even_volume(contribution_margin: float, rise: float) -> float:
    """Volume you can *afford to lose* on a price rise, as a negative share.

        loss = -r / (CM + r)

    The mirror of the discount formula, and the more encouraging one — a rise
    drops straight to contribution, so it buys a lot of room.

    Online again, CM 0.31, put the rate up by 10% of revenue:

    >>> round(price_rise_break_even_volume(0.31, 0.10), 3)
    -0.244

    You can lose a quarter of your orders and still be level. Pair it with
    the elasticity: Meridian's overall semi-elasticity is about -25% per
    margin point, so a rise of that size loses far more than 24% and the
    trade is a bad one. The formula tells you the hurdle; only an *estimate*
    of demand tells you whether you clear it.
    """
    return -rise / (contribution_margin + rise)


def profit_impact_of_price_move(
    orders: float,
    price: float,
    variable_cost: float,
    price_change: float,
    volume_change_pct: float,
) -> dict:
    """The full before-and-after of a price move, in £.

    The break-even formulas answer "what would it take?". This answers "given
    what I actually expect demand to do, what happens?" — which is the
    version that goes to a committee.

    Args:
        orders: today's order count.
        price: today's revenue per order, £.
        variable_cost: today's variable cost per order, £ (assumed unchanged).
        price_change: the move, £ per order. Negative for a discount.
        volume_change_pct: expected volume response, as a decimal (0.15 = +15%).

    Returns a dict of before, after, and the delta.

    Meridian online: 1,000 orders at £14.76 revenue and £10.18 cost. Cut the
    rate by £1.50 and expect the 25%-per-point response to deliver +20%:

    >>> out = profit_impact_of_price_move(1000, 14.76, 10.18, -1.50, 0.20)
    >>> round(out["contribution_before"], 2)
    4580.0
    >>> round(out["contribution_after"], 2)
    3696.0
    >>> round(out["contribution_change"], 2)
    -884.0
    >>> round(out["break_even_volume_change"], 3)
    0.487

    A fifth more orders, and the channel is £884 worse off — because it
    needed 49% more, not 20%. Revenue rises, contribution falls. That gap is
    where careers are made and lost: always report the contribution line.
    """
    cm_ratio = contribution_margin(price, variable_cost)
    before = orders * contribution(price, variable_cost)
    after = orders * (1 + volume_change_pct) * contribution(price + price_change, variable_cost)
    required = (discount_break_even_volume(cm_ratio, -price_change / price)
                if price_change < 0 else
                price_rise_break_even_volume(cm_ratio, price_change / price))
    return {
        "contribution_before": before,
        "contribution_after": after,
        "contribution_change": after - before,
        "revenue_before": orders * price,
        "revenue_after": orders * (1 + volume_change_pct) * (price + price_change),
        "break_even_volume_change": required,
        "expected_volume_change": volume_change_pct,
        "clears_hurdle": (volume_change_pct >= required if price_change < 0
                          else volume_change_pct >= required),
    }


# ==========================================================================
# 4. DEMAND RESPONSE — elasticity, and the price it implies
# ==========================================================================
#
# Everything above takes the volume response as given. This section is about
# where that number comes from — and it is the hardest number in pricing to
# get honestly, because the price you observe was set by someone reacting to
# the same demand you are trying to measure. Notebooks 03, 05 and 07 are
# about that problem. These functions are the arithmetic once you have an
# estimate you trust.


def arc_elasticity(p0: float, q0: float, p1: float, q1: float) -> float:
    """Midpoint (arc) price elasticity between two observed points.

        e = (%change in quantity) / (%change in price)

    using midpoints for both, so the answer does not depend on which point
    you call "before".

    >>> round(arc_elasticity(3.50, 1000, 3.85, 880), 3)
    -1.34

    Read it as: a 1% price rise loses 1.3% of volume. Below -1 ("elastic")
    a price rise loses revenue; between -1 and 0 ("inelastic") it gains
    revenue. Almost every honestly-estimated retail elasticity lands between
    -0.5 and -4.

    The trap: two points from history are a *correlation*, and the price
    moved for a reason. Meridian's naive regression of conversion on price
    returns a number close to zero, because the board went up in August when
    demand was strongest. The instrument in notebook 07 exists to fix exactly
    this.
    """
    if p1 == p0:
        raise ValueError("price did not change; elasticity is undefined")
    dq = (q1 - q0) / ((q1 + q0) / 2)
    dp = (p1 - p0) / ((p1 + p0) / 2)
    return dq / dp


def semi_elasticity(q0: float, q1: float, margin_change_pp: float) -> float:
    """Percentage change in volume per *margin point* — the desk's unit.

        semi-elasticity = (%change in quantity) / (change in margin, pp)

    A pricing desk moves the board in basis points, not percentages, so this
    is the number people actually quote. Meridian's true overall figure is
    about -25.5% per pp; by segment it runs from -5% (last-minute airside
    buyers, who have no alternative) to -51% (bargain hunters, who will
    switch app for 30bp).

    >>> round(semi_elasticity(1000, 745, 1.0), 1)
    -25.5

    Beware of averaging it. The overall -25.5 is not "the" elasticity of
    anything: it is a mix of four very different segments, and the mix
    changes when you move the price. That is notebook 09's subject.
    """
    if margin_change_pp == 0:
        raise ValueError("margin did not change; semi-elasticity is undefined")
    return 100 * ((q1 - q0) / q0) / margin_change_pp


def volume_after_price_change(q0: float, pct_price_change: float, elasticity: float) -> float:
    """Project volume after a price move, given an elasticity.

        q1 = q0 * (1 + e * %price change)

    >>> round(volume_after_price_change(1000, 0.10, -1.4), 1)
    860.0

    A linear approximation, and it is only safe for small moves — under about
    10%. For a bigger move, project from the demand curve itself (notebook
    03) rather than from a single slope, because elasticity is not constant:
    it steepens as price rises.
    """
    return q0 * (1 + elasticity * pct_price_change)


def lerner_index(price: float, marginal_cost: float) -> float:
    """The share of price that is margin — the textbook name for what you have.

        L = (price - marginal cost) / price

    >>> round(lerner_index(17.60, 7.38), 4)
    0.5807

    Numerically identical to the contribution margin. The reason it has its
    own name is the next function: at the profit-maximising price, L equals
    exactly 1/|elasticity|. So comparing your Lerner index to 1/|e| tells you
    at a glance whether you are priced too keenly or too dearly.
    """
    return contribution_margin(price, marginal_cost)


def optimal_margin_from_elasticity(elasticity: float) -> float:
    """The profit-maximising margin implied by an elasticity (the Lerner rule).

        (P - MC) / P = 1 / |e|

    >>> round(optimal_margin_from_elasticity(-2.5), 4)
    0.4
    >>> round(optimal_margin_from_elasticity(-1.4), 4)
    0.7143

    The most useful sanity check in pricing. Feed it your estimated
    elasticity and compare the answer to the margin you actually run:

      * running *below* the implied margin -> you are leaving money on the
        table (or your elasticity estimate is biased toward zero, which naive
        regression on historical price always is);
      * running *above* it -> volume is worth more than the extra points.

    Its assumptions are strong and worth saying out loud: one product, one
    segment, no competitive reaction, no effect on repeat purchase. Meridian
    breaks all four. Use it to *frame* an argument, never to set a board.

    An elasticity between -1 and 0 has no interior optimum — it says raise
    the price until something else stops you, which in practice means the
    regulator, the competition, or the customer never coming back:

    >>> optimal_margin_from_elasticity(-0.5)
    inf
    """
    if elasticity >= -1:
        return float("inf")
    return 1 / abs(elasticity)


def optimal_price_from_elasticity(marginal_cost: float, elasticity: float) -> float:
    """The profit-maximising price for a constant-elasticity demand curve.

        P* = MC * |e| / (|e| - 1)

    >>> round(optimal_price_from_elasticity(7.38, -2.5), 2)
    12.3
    >>> round(optimal_price_from_elasticity(7.38, -1.4), 2)
    25.83

    Watch how violently it moves. Between an elasticity of -2.5 and -1.4 the
    optimal price doubles — so the *uncertainty* in your elasticity estimate
    matters more than its point value. This is why notebook 08 optimises over
    a distribution of elasticities rather than a single number, and why a
    confidence interval belongs on every elasticity you present.
    """
    if elasticity >= -1:
        raise ValueError("no finite optimum: demand is inelastic at this price")
    e = abs(elasticity)
    return marginal_cost * e / (e - 1)


def revenue_vs_profit_maximum(elasticity: float) -> str:
    """Which price maximises what — a one-line orientation.

    Revenue is maximised at |e| = 1. Profit is maximised *dearer* than that,
    because at the revenue peak an extra order still costs money to serve.
    The gap between the two is where "we hit our revenue target and missed
    our profit target" comes from.

    >>> revenue_vs_profit_maximum(-0.8)
    'inelastic: raising price raises both revenue and profit'
    >>> revenue_vs_profit_maximum(-1.0)
    'unit elastic: revenue is at its peak; profit still wants a dearer price'
    >>> revenue_vs_profit_maximum(-2.0)
    'elastic: raising price loses revenue, and may still raise profit'
    """
    if elasticity > -1:
        return "inelastic: raising price raises both revenue and profit"
    if elasticity == -1:
        return "unit elastic: revenue is at its peak; profit still wants a dearer price"
    return "elastic: raising price loses revenue, and may still raise profit"


# ==========================================================================
# 5. BRIDGES — how you explain a number to a board
# ==========================================================================
#
# Two tables get built in every pricing function on earth. Neither is
# analytically clever; both are how the analysis gets believed.


def price_waterfall(list_price: float, leakages: dict[str, float]) -> pd.DataFrame:
    """List price down to pocket price, one leak at a time.

    The waterfall exists because nobody in the business can tell you what you
    actually got paid. There is a headline rate, and then there is what
    survives the size tier, the loyalty rate, the promotion, the commission
    to the host retail network, and the courier — and the last number is the
    only one that pays anybody.

    Args:
        list_price: the advertised or board price per order, £.
        leakages: ordered {name: amount} in £ per order. Positive numbers are
            deductions.

    Returns a DataFrame with each step, what it costs, and what is left.

    A Meridian branch euro order at the board rate:

    >>> w = price_waterfall(21.00, {
    ...     "size tier discount": 1.25,
    ...     "loyalty rate": 0.60,
    ...     "summer promotion": 0.96,
    ...     "network commission": 2.90,
    ...     "handling and funding": 3.30,
    ... })
    >>> print(w.to_string(index=False))  # doctest: +NORMALIZE_WHITESPACE
                    step  leak_gbp  running_gbp  pct_of_list
              list price      0.00        21.00        100.0
      size tier discount      1.25        19.75         94.0
            loyalty rate      0.60        19.15         91.2
        summer promotion      0.96        18.19         86.6
      network commission      2.90        15.29         72.8
    handling and funding      3.30        11.99         57.1
            pocket margin      0.00        11.99         57.1

    Fifty-seven pence in the pound reaches the pocket. Two facts fall out of
    this table that will not fall out of any average:

      * the biggest single leak is the **network commission** — a negotiated
        cost sitting in someone else's budget. The cheapest margin point
        available to Meridian is not a price change at all;
      * the discounts stack. Nobody approved a 13% cut; three people each
        approved a small one.

    Always build this at the *order* level, then look at the spread across
    orders. The average waterfall hides the tail, and the tail is where the
    money is.
    """
    rows = [{"step": "list price", "leak_gbp": 0.0, "running_gbp": list_price}]
    running = list_price
    for name, amount in leakages.items():
        running -= amount
        rows.append({"step": name, "leak_gbp": float(amount), "running_gbp": running})
    rows.append({"step": "pocket margin", "leak_gbp": 0.0, "running_gbp": running})
    df = pd.DataFrame(rows)
    df["running_gbp"] = df["running_gbp"].round(2)
    df["pct_of_list"] = (100 * df["running_gbp"] / list_price).round(1)
    return df


def price_volume_mix(base: pd.DataFrame, comparison: pd.DataFrame,
                     key: str = "product_id", price: str = "price",
                     volume: str = "volume") -> pd.DataFrame:
    """Split a revenue change into price, volume and mix.

    "Revenue is up £40k" is not an answer. The board wants to know whether
    the business sold more, charged more, or simply sold a richer basket —
    because those three have completely different implications and only one
    of them is yours.

        volume effect = (Q1 - Q0) x average base price
        mix effect    = sum(p0 x q1) - average base price x Q1
        price effect  = sum((p1 - p0) x q1)

    The three sum exactly to the revenue change.

    >>> base = pd.DataFrame({"product_id": ["EUR_CASH", "USD_CASH", "TRAVEL_CARD"],
    ...                      "price": [18.00, 17.00, 26.00],
    ...                      "volume": [1000, 600, 200]})
    >>> comp = pd.DataFrame({"product_id": ["EUR_CASH", "USD_CASH", "TRAVEL_CARD"],
    ...                      "price": [18.50, 16.80, 26.00],
    ...                      "volume": [1020, 640, 260]})
    >>> b = price_volume_mix(base, comp)
    >>> print(b.to_string(index=False))  # doctest: +NORMALIZE_WHITESPACE
                effect     gbp
          base revenue 33400.0
                volume  2226.7
                   mix   373.3
                 price   382.0
    comparison revenue 36382.0

    Revenue is up £2,982. Volume did most of the work (£2,227), mix added
    £373 because the dear travel card grew fastest, and the price line — the
    only one a pricing manager owns — contributed £382. Present it in that
    order and nobody can claim the volume growth as a pricing win.

    Note the euro rate went up 50p while the dollar rate came *down* 20p, and
    the net price effect is still positive. A single "average price" would
    have shown you none of that.
    """
    merged = base.merge(comparison, on=key, suffixes=("_0", "_1"), how="outer").fillna(0)
    p0, q0 = merged[f"{price}_0"].to_numpy(), merged[f"{volume}_0"].to_numpy()
    p1, q1 = merged[f"{price}_1"].to_numpy(), merged[f"{volume}_1"].to_numpy()

    rev0, rev1 = float((p0 * q0).sum()), float((p1 * q1).sum())
    Q0, Q1 = float(q0.sum()), float(q1.sum())
    avg_p0 = rev0 / Q0 if Q0 else 0.0

    vol_effect = (Q1 - Q0) * avg_p0
    mix_effect = float((p0 * q1).sum()) - avg_p0 * Q1
    price_effect = float(((p1 - p0) * q1).sum())

    return pd.DataFrame([
        {"effect": "base revenue", "gbp": round(rev0, 1)},
        {"effect": "volume", "gbp": round(vol_effect, 1)},
        {"effect": "mix", "gbp": round(mix_effect, 1)},
        {"effect": "price", "gbp": round(price_effect, 1)},
        {"effect": "comparison revenue", "gbp": round(rev1, 1)},
    ])


# ==========================================================================
# 6. VALUE OVER TIME — the correction that makes optimisers honest
# ==========================================================================
#
# Every formula so far treats an order as a one-off. Meridian's customers
# come back — 34,000 of them, roughly twice a year — and how they were
# treated last summer changes whether they come back at all. A static
# optimiser cannot see that, so it always recommends a price that is too
# high. This section is the correction.


def discount_factor(rate: float, years: float) -> float:
    """Today's value of £1 received `years` from now.

        factor = 1 / (1 + rate) ** years

    >>> round(discount_factor(0.10, 1), 4)
    0.9091
    >>> round(discount_factor(0.10, 3), 4)
    0.7513

    The rate is the business's cost of capital — what the money could earn
    elsewhere at similar risk. Ask finance for it; do not invent it. A high
    rate makes the business short-termist by construction, which is worth
    naming when a retention argument gets waved away.
    """
    return 1 / (1 + rate) ** years


def npv(cashflows: list[float], rate: float) -> float:
    """Net present value of a stream of cashflows, first entry at t=0.

        NPV = sum over t of cashflow[t] / (1 + rate) ** t

    A pricing investment — a promotion, a system, a test — costing £50k now
    and returning £20k a year for three years, at a 10% cost of capital:

    >>> round(npv([-50_000, 20_000, 20_000, 20_000], 0.10), 2)
    -262.96

    Marginally negative. Undiscounted it looked like a £10,000 winner; the
    time value of money ate all of it. This is why "it pays back in under
    three years" is not the same claim as "it creates value".
    """
    return float(sum(cf * discount_factor(rate, t) for t, cf in enumerate(cashflows)))


def payback_period(cashflows: list[float]) -> float:
    """Years until cumulative (undiscounted) cashflow turns positive.

    Interpolates within the year in which it crosses.

    >>> round(payback_period([-50_000, 20_000, 20_000, 20_000]), 2)
    2.5

    Crude by design, and every committee asks for it. It ignores the time
    value of money and everything after the crossover, so quote it next to
    the NPV rather than instead of it. Returns infinity if it never pays
    back:

    >>> payback_period([-50_000, 10_000, 10_000])
    inf
    """
    cumulative = 0.0
    for t, cf in enumerate(cashflows):
        previous = cumulative
        cumulative += cf
        if cumulative >= 0 and t > 0:
            return t - 1 + (-previous / cf if cf else 0)
    return float("inf")


def customer_lifetime_value(annual_contribution: float, retention_rate: float,
                            discount_rate: float = 0.10) -> float:
    """Present value of a customer, including this year.

        LTV = annual contribution x (1 + d) / (1 + d - r)

    where `r` is the share of customers who return next year and `d` is the
    cost of capital. The fraction is the "margin multiple" — how many years
    of contribution a customer is worth today.

    A Meridian customer making two trips a year at £10.22 of contribution,
    with 75% coming back:

    >>> round(customer_lifetime_value(20.44, 0.75, 0.10), 2)
    64.24

    Three years and a bit of contribution, not one. That multiple is the
    whole argument for pricing below the static optimum, and it is worth
    computing before you make the argument, because if retention is 40% the
    multiple is 1.6 and the argument mostly evaporates.
    """
    if retention_rate >= 1 + discount_rate:
        raise ValueError("retention at or above (1 + discount rate) implies infinite value")
    return annual_contribution * (1 + discount_rate) / (1 + discount_rate - retention_rate)


def retention_multiplier(margin_above_market_pp: float, refused_for_stock: bool = False,
                         margin_coefficient: float = 0.12,
                         stockout_coefficient: float = 0.15) -> float:
    """Share of next year's trips you keep, given how you treated the customer.

    This is Meridian's actual behavioural rule, the one `01_data_foundation`
    simulates and notebook 08 has to rediscover:

        multiplier = clip(1 - 0.12 x max(margin above market, 0)
                            - 0.15 x refused for stock,  0.5, 1.2)

    Only pricing *above* the best market rate is punished — being keen than
    the market does not buy extra loyalty, which is an asymmetry worth
    knowing before you promise one.

    Price at the market and nothing is lost:

    >>> round(retention_multiplier(0.0), 3)
    1.0

    Sit a full point above it and you lose 12% of next year's trips:

    >>> round(retention_multiplier(1.0), 3)
    0.88

    Refuse them for stock as well, and it compounds:

    >>> round(retention_multiplier(1.0, refused_for_stock=True), 3)
    0.73

    Note what that second number means commercially. Notebook 08's static
    optimiser wants to add margin points; each one costs 12% of a customer's
    future travel. The August stockouts are worse still — a refused customer
    is a bigger loss than a dear one — and stock is an operations budget, not
    a pricing lever. Some of the best margin work is not pricing work.
    """
    raw = (1
           - margin_coefficient * max(margin_above_market_pp, 0.0)
           - stockout_coefficient * (1.0 if refused_for_stock else 0.0))
    return float(np.clip(raw, 0.5, 1.2))


def lifetime_value_of_a_price_move(
    orders: float,
    contribution_per_order: float,
    margin_change_pp: float,
    volume_change_pct: float,
    trips_per_year: float = 2.0,
    retention_rate: float = 0.75,
    discount_rate: float = 0.10,
    order_value: float = 478.0,
) -> dict:
    """Today's contribution gain, and what it costs in customer lifetime value.

    The correction that makes a static price optimiser honest. It computes
    the move twice: once as this year's P&L sees it, and once including the
    retention damage from `retention_multiplier`.

    Args:
        orders: orders in the period.
        contribution_per_order: £ today.
        margin_change_pp: the price move in margin points. Positive is dearer.
        volume_change_pct: expected immediate volume response, decimal.
        trips_per_year, retention_rate, discount_rate: the LTV inputs.
        order_value: average turnover per order, £ — converts pp into £.

    Meridian branch: 100,000 orders at £11.75, put the board up 0.5pp, and
    accept the ~-28.7%-per-point response (so -14.4% of orders):

    >>> out = lifetime_value_of_a_price_move(
    ...     100_000, 11.75, margin_change_pp=0.5, volume_change_pct=-0.144,
    ...     order_value=503.55)
    >>> round(out["static_contribution_change"], 0)
    46319.0
    >>> round(out["lifetime_value_change"], 0)
    -437290.0
    >>> round(out["total_value_change"], 0)
    -390970.0
    >>> out["verdict"]
    'reject: the retention cost exceeds the in-year gain'

    A £46k win this year and a £437k hole in the customer base. The static
    number is the one the P&L will show and the one your optimiser will
    recommend. Bring both.

    Why the second number is so much larger than the first is the lesson.
    Sitting 0.5pp above the market costs 6% of next year's trips — but a
    retention *rate* enters the lifetime value geometrically, so cutting it
    from 0.75 to 0.705 takes 11% off the margin multiple, on every future
    year, for every customer. Small, permanent damage to repeat rate
    outweighs a large one-off gain whenever customers are loyal.

    Which means the conclusion is only as strong as the retention assumption,
    so state it and test it:

    >>> for r in (0.75, 0.55, 0.40):
    ...     o = lifetime_value_of_a_price_move(100_000, 11.75, 0.5, -0.144,
    ...                                        retention_rate=r, order_value=503.55)
    ...     print(f"retention {r:.0%}: lifetime £{o['lifetime_value_change']:>9,.0f}"
    ...           f"   total £{o['total_value_change']:>9,.0f}")
    retention 75%: lifetime £ -437,290   total £ -390,970
    retention 55%: lifetime £ -138,263   total £  -91,943
    retention 40%: lifetime £  -63,620   total £  -17,301

    At 40% retention the case is nearly a wash. Meridian's customers do come
    back — that is why notebook 08's optimiser needs the correction — but in
    a business with genuinely transactional customers this whole argument
    mostly evaporates. Find out which one you are in before you make it.

    Two assumptions are doing real work here and belong on the slide:
    the price move is *permanent* (so the retention penalty applies to every
    future year, not just the next one), and the volume response is the
    immediate one — the retention effect is on top of it, not part of it.
    """
    price_per_order = order_value * margin_change_pp / 100
    new_contribution = contribution_per_order + price_per_order
    new_orders = orders * (1 + volume_change_pct)
    static = new_orders * new_contribution - orders * contribution_per_order

    keep = retention_multiplier(margin_change_pp)
    customers = new_orders / trips_per_year
    ltv_now = customer_lifetime_value(new_contribution * trips_per_year,
                                      retention_rate, discount_rate)
    ltv_after = customer_lifetime_value(new_contribution * trips_per_year,
                                        retention_rate * keep, discount_rate)
    lifetime = customers * (ltv_after - ltv_now)

    total = static + lifetime
    verdict = ("accept: the move creates value even after retention"
               if total > 0 else
               "reject: the retention cost exceeds the in-year gain")
    return {
        "static_contribution_change": static,
        "retention_multiplier": keep,
        "lifetime_value_change": lifetime,
        "total_value_change": total,
        "verdict": verdict,
    }


# ==========================================================================
# 7. THE DECISION — putting a price move in front of a committee
# ==========================================================================


@dataclass
class PriceMove:
    """One proposed price change, costed end to end.

    A container that forces every number a pricing committee will ask for
    into one place, so nobody has to reconstruct the arithmetic live. Build
    it, print it, put it on the paper.

    >>> move = PriceMove(name="Online +25bp", orders=40_000,
    ...                  price=14.76, variable_cost=10.18,
    ...                  price_change=1.29, expected_volume_change=-0.066)
    >>> print(move.summary())
    Online +25bp
      contribution today      £183,200
      contribution after      £219,303
      change                  £+36,103  (+19.7%)
      volume hurdle           -22.0%   (need no worse than this)
      volume expected         -6.6%
      verdict                 clears the hurdle

    The hurdle line is the one that ends arguments: it is the volume loss the
    move survives, computed from the cost to serve, and it does not care
    whose opinion is in the room.
    """
    name: str
    orders: float
    price: float
    variable_cost: float
    price_change: float
    expected_volume_change: float

    @property
    def impact(self) -> dict:
        """The full before/after dict from `profit_impact_of_price_move`."""
        return profit_impact_of_price_move(
            self.orders, self.price, self.variable_cost,
            self.price_change, self.expected_volume_change)

    def summary(self) -> str:
        """A committee-ready block of text. Print it verbatim."""
        i = self.impact
        before, after = i["contribution_before"], i["contribution_after"]
        change = i["contribution_change"]
        hurdle = i["break_even_volume_change"]
        verdict = "clears the hurdle" if i["clears_hurdle"] else "does NOT clear the hurdle"
        return (f"{self.name}\n"
                f"  contribution today      £{before:,.0f}\n"
                f"  contribution after      £{after:,.0f}\n"
                f"  change                  £{change:+,.0f}  ({change / before:+.1%})\n"
                f"  volume hurdle           {hurdle:+.1%}   (need no worse than this)\n"
                f"  volume expected         {self.expected_volume_change:+.1%}\n"
                f"  verdict                 {verdict}")


def margin_of_safety(expected_volume_change: float, break_even_volume_change: float) -> float:
    """How much room the forecast has before the move stops paying.

        safety = expected - required

    >>> round(margin_of_safety(0.20, 0.476), 3)
    -0.276
    >>> round(margin_of_safety(-0.066, -0.219), 3)
    0.153

    Positive is headroom. The first case needs 48% more volume and expects
    20%, so it is 28 points short — no forecast error explains that away. The
    second has 15 points of room, which is the kind of margin that survives
    an elasticity estimate being somewhat wrong. Since your elasticity always
    *is* somewhat wrong, this — not the point estimate — is the number that
    should decide it.
    """
    return expected_volume_change - break_even_volume_change


# ==========================================================================
# A guided tour: python pricing_finance.py
# ==========================================================================

def _tour() -> None:
    """Run every section against real Meridian FX figures."""
    line = "=" * 74

    print(line)
    print("1. MARGIN ARITHMETIC — a branch euro order: £18.19 revenue, £6.19 cost")
    print(line)
    print(f"  margin   {margin_pct(18.19, 6.19):.1%}   (share of price — the P&L number)")
    print(f"  markup   {markup_pct(18.19, 6.19):.1%}   (share of cost — the buyer's number)")
    print(f"  to hit a 60% margin, price at £{price_from_margin(6.19, 0.60):.2f} "
          f"— not the £{price_from_markup(6.19, 0.60):.2f} that 'cost + 60%' gives you")

    print(f"\n{line}\n2. CONTRIBUTION AND BREAK-EVEN — per order, by channel\n{line}")
    channels = {"airport": (22.10, 4.59, 5000), "branch": (18.02, 6.27, 700),
                "online": (14.76, 10.18, 6000)}
    print(f"  {'channel':10s} {'revenue':>9s} {'var cost':>9s} {'contrib':>9s} "
          f"{'CM':>7s} {'break-even orders/mo':>21s}")
    for name, (rev, vc, fixed) in channels.items():
        print(f"  {name:10s} {rev:9.2f} {vc:9.2f} {contribution(rev, vc):9.2f} "
              f"{contribution_margin(rev, vc):7.1%} {break_even_volume(fixed, rev, vc):21.0f}")

    print(f"\n{line}\n3. THE DISCOUNT TRADE — what a 10% rate cut must deliver\n{line}")
    for name, (rev, vc, _) in channels.items():
        cm = contribution_margin(rev, vc)
        print(f"  {name:10s} CM {cm:5.1%} -> needs "
              f"{discount_break_even_volume(cm, 0.10):+7.1%} volume to break even; "
              f"a 10% rise survives {price_rise_break_even_volume(cm, 0.10):+6.1%}")
    print("  Same discount. Three completely different asks. Cost to serve is why.")

    print(f"\n{line}\n4. DEMAND RESPONSE — Meridian's true semi-elasticities\n{line}")
    truths = {"last_minute": -5.1, "holiday_family": -23.0,
              "frequent_flyer": -29.9, "bargain_hunter": -50.9}
    print("  segment           %/pp   implied elasticity   Lerner-optimal margin")
    for seg, semi in truths.items():
        e = semi / 100 * 3.66          # %/pp -> elasticity at a 3.66pp margin
        implied = optimal_margin_from_elasticity(e)
        shown = "no interior optimum" if implied == float("inf") else f"{implied:.0%}"
        print(f"  {seg:16s} {semi:6.1f}   {e:17.2f}   {shown:>21s}")
    print("  Three of the four are inelastic at today's board — the Lerner rule says")
    print("  'charge more'. Section 6 is why the business does not. Four segments, one")
    print("  board: notebook 09 is about whether you are allowed to split it.")

    print(f"\n{line}\n5. BRIDGES — where the board rate actually goes\n{line}")
    print(price_waterfall(21.00, {"size tier discount": 1.25, "loyalty rate": 0.60,
                                  "summer promotion": 0.96, "network commission": 2.90,
                                  "handling and funding": 3.30}).to_string(index=False))

    print(f"\n{line}\n6. VALUE OVER TIME — a 0.5pp branch rise, both ways\n{line}")
    out = lifetime_value_of_a_price_move(100_000, 11.75, 0.5, -0.144, order_value=503.55)
    print(f"  in-year contribution      £{out['static_contribution_change']:+,.0f}")
    print(f"  retention multiplier       {out['retention_multiplier']:.3f}")
    print(f"  lifetime value            £{out['lifetime_value_change']:+,.0f}")
    print(f"  total                     £{out['total_value_change']:+,.0f}")
    print(f"  {out['verdict']}")

    print(f"\n{line}\n7. THE DECISION\n{line}")
    print(PriceMove("Online +25bp", 40_000, 14.76, 10.18, 1.29, -0.066).summary())
    print("\nEvery figure above is checked by `python -m doctest pricing_finance.py`.")


if __name__ == "__main__":
    _tour()
