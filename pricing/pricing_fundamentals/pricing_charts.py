"""Eight charts a pricing manager presents — and the words to say over each one.

    python pricing_charts.py            # build every chart into charts/ and
                                        # print the narration for each

Or one at a time, in a notebook:

    from pricing_charts import CHARTS, build
    fig, chart = build("waterfall")
    print(chart.script())

Why this file exists
--------------------
A chart is not the deliverable. **The sentence is the deliverable.** The chart
is the evidence you put behind it so nobody has to take your word for it.

Most pricing analysis dies in the room, not in the spreadsheet, and it dies
the same way every time: the analyst puts up a correct chart and then narrates
the axes. "So here we have contribution on the y-axis, and along the bottom
we've got channel..." Everyone can read. What they cannot do is tell which of
the twelve things on the slide is the one that should change their mind.

So every chart here carries four things, and you should never build one
without all four:

    headline   the sentence you say first, before anyone looks at the chart.
               It is a claim, not a description. "Online is a third of our
               contribution margin" — not "contribution by channel".
    read       how to walk someone through it: which mark to point at, in
               what order, and what each one means.
    ask        the two or three questions this chart provokes, with the
               answer you should already have. The chart is not finished
               until you can answer these without opening another file.
    caveat     what the chart cannot tell you. Say it yourself, early. The
               fastest way to lose a room is to have the caveat found for
               you; the fastest way to win one is to have named it first.

`chart.script()` prints all four for the chart you are about to show. Read it
out loud before the meeting. That is the actual exercise.

A note on the language
----------------------
The wording in these scripts is deliberately plain, and it is deliberately
*committed*. Compare:

    weak    "The data seems to suggest that online might potentially be
             somewhat less profitable, although of course there are a number
             of factors involved."
    strong  "Online earns 32p of contribution on every revenue pound. The
             branch earns 82p. The gap is the courier and the card fee, not
             the price."

The second is shorter, it names the number, and it says what causes the gap.
Hedging does not make you sound careful; naming your uncertainty does — which
is what the `caveat` line is for. Say the number, then say what would change
your mind. `STAKEHOLDER_STORYTELLING.md` takes this apart phrase by phrase.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from db_helper import MeridianDB
from toolkit import C, INK, SUB, MUT, tidy
from toolkit import style as _course_style


def style() -> None:
    """The course style, plus the one rcParam it is missing.

    `axes.axisbelow` puts the gridlines *behind* the bars. Without it a
    gridline is drawn through every filled mark, which reads as a bar chopped
    into segments — the single most common way a correct chart is misread.
    """
    _course_style()
    plt.rcParams["axes.axisbelow"] = True

OUT = Path(__file__).parent / "charts"

#: Fixed colour per channel, everywhere, forever. If "online" is blue on one
#: slide and orange on the next, your audience spends the meeting re-reading
#: the legend instead of listening to you. Consistency across a deck is worth
#: more than the prettiest single chart in it.
CHANNEL_C = {"branch": C[0], "airport": C[1], "online": C[5]}


# ==========================================================================
# Helpers — the small things that separate a working chart from a good one
# ==========================================================================

def _money(x: float, pence: bool = False) -> str:
    """£ with the separators a commercial audience expects."""
    if abs(x) >= 1_000_000:
        return f"£{x / 1_000_000:,.2f}m"
    if abs(x) >= 1_000 and not pence:
        return f"£{x:,.0f}"
    return f"£{x:,.2f}"


def _label_bars(ax, bars, fmt: Callable[[float], str], *, inside: bool = False,
                colour: str | None = None) -> None:
    """Print the value on each bar.

    Direct labelling beats a y-axis. If the number matters, say it on the
    mark; if it does not matter, it should not be on the chart at all. Every
    gridline you make someone trace with their eye is a second they are not
    listening to you.
    """
    for bar in bars:
        h = bar.get_height()
        if inside:
            ax.text(bar.get_x() + bar.get_width() / 2, h / 2, fmt(h),
                    ha="center", va="center", fontsize=9,
                    color=colour or "white", fontweight="bold")
        else:
            off = 0.01 * max(abs(h), 1e-9) if h >= 0 else -0.01 * abs(h)
            ax.text(bar.get_x() + bar.get_width() / 2, h + off, fmt(h),
                    ha="center", va="bottom" if h >= 0 else "top",
                    fontsize=9, color=colour or SUB)


def _headline(fig, ax, headline: str, subtitle: str = "") -> None:
    """Put the CLAIM where a title normally goes.

    "Contribution by channel" tells the room what the axes are, which they can
    see. "Online is 43% of orders and 21% of contribution" tells them what to
    do about it. A chart title is the cheapest sentence on the slide — never
    spend it on a restatement of the axis labels.
    """
    ax.set_title(headline, loc="left", fontsize=12.5, color=INK,
                 fontweight="bold", pad=24 if subtitle else 10)
    if subtitle:
        ax.text(0, 1.015, subtitle, transform=ax.transAxes, fontsize=9.5,
                color=MUT, va="bottom")


def _note(ax, text: str, xy, xytext, colour: str = SUB, arrow: bool = True) -> None:
    """Write the point on the chart, next to the mark that makes it."""
    ax.annotate(text, xy=xy, xytext=xytext, fontsize=9, color=colour,
                arrowprops=dict(arrowstyle="->", color=colour, lw=1.1,
                                shrinkA=2, shrinkB=4) if arrow else None)


# ==========================================================================
# The chart record — chart plus script
# ==========================================================================

@dataclass
class Chart:
    """One chart, and everything you need to say while it is on screen."""

    key: str
    question: str          # the meeting question this chart answers
    headline: str          # the claim you say FIRST
    read: str              # how to walk them through the marks
    ask: list[tuple[str, str]]   # (what they will ask, what you answer)
    caveat: str            # what it cannot tell you — say it yourself
    build: Callable[[MeridianDB], plt.Figure] = field(repr=False, default=None)

    def script(self) -> str:
        """The narration, formatted for reading out loud."""
        w = 78
        out = [f"{'=' * w}", f"  {self.key.upper()}  —  {self.question}", "=" * w, ""]
        out += ["SAY FIRST", f"  {self.headline}", ""]
        out += ["THEN WALK THEM THROUGH IT"]
        out += [f"  {line}" for line in self.read.strip().splitlines()]
        out += ["", "THEY WILL ASK"]
        for q, a in self.ask:
            out += [f"  Q: {q}", f"  A: {a}", ""]
        out += ["SAY THE CAVEAT YOURSELF, EARLY", f"  {self.caveat}", ""]
        return "\n".join(out)


# ==========================================================================
# 1. Where the volume is, and where the money is
# ==========================================================================

def _fig_contribution(db: MeridianDB) -> plt.Figure:
    p = db.pnl("channel").set_index("channel").loc[["branch", "airport", "online"]]
    share = pd.DataFrame({
        "orders": p["orders"] / p["orders"].sum(),
        "turnover": p["turnover_gbp"] / p["turnover_gbp"].sum(),
        "revenue": p["gross_revenue_gbp"] / p["gross_revenue_gbp"].sum(),
        "contribution": p["contribution_gbp"] / p["contribution_gbp"].sum(),
    })

    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.6),
                                  gridspec_kw={"width_ratios": [1.55, 1]})

    # Left: the same three channels measured four ways. The story is the
    # DIVERGENCE between the first bar and the last one.
    x = np.arange(len(share.columns))
    bottom = np.zeros(len(share.columns))
    for ch in share.index:
        vals = share.loc[ch].values
        ax.bar(x, vals, 0.62, bottom=bottom, color=CHANNEL_C[ch],
               edgecolor="white", linewidth=1.2, label=ch)
        for xi, (v, b) in enumerate(zip(vals, bottom)):
            if v > 0.05:
                ax.text(xi, b + v / 2, f"{ch}\n{v:.0%}", ha="center", va="center",
                        fontsize=9.5, color="white", fontweight="bold")
        bottom += vals
    ax.set_xticks(x)
    ax.set_xticklabels(["orders\n(volume)", "turnover\n(not ours)",
                        "gross revenue\n(our top line)", "contribution\n(what is left)"])
    # A strip of whitespace above the bars, so the annotation has somewhere to
    # live that is not on top of a label. Never write over your own data.
    ax.set_ylim(0, 1.16); ax.set_yticks([]); ax.grid(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_visible(False)
    _headline(fig, ax,
              "Online sells 43% of the orders and earns 17% of the contribution",
              "share of each measure, 2024–25, all channels = 100%")
    ax.text(1.5, 1.10, "the distance between these two is the whole pricing question",
            ha="center", fontsize=9.5, color=INK)
    for xi in (0, 3):
        ax.annotate("", xy=(xi, 1.005), xytext=(xi, 1.075),
                    arrowprops=dict(arrowstyle="->", color=INK, lw=1.1))

    # Right: the same fact as a rate, which is the form people remember.
    cm = p["contribution_margin"]
    bars = ax2.barh(range(len(cm)), cm.values,
                    color=[CHANNEL_C[c] for c in cm.index], height=0.6)
    ax2.set_yticks(range(len(cm)))
    ax2.set_yticklabels(cm.index)
    ax2.set_xlim(0, 1.0); ax2.set_xticks([])
    ax2.grid(False)
    ax2.spines["bottom"].set_visible(False)
    for i, (bar, v) in enumerate(zip(bars, cm.values)):
        ax2.text(v + 0.02, i, f"{v:.0%}", va="center", fontsize=11,
                 color=INK, fontweight="bold")
    _headline(fig, ax2, "Contribution per revenue pound",
              "how much of what we charge survives the cost of serving")
    fig.tight_layout()
    return fig


CH_CONTRIBUTION = Chart(
    key="contribution",
    question="Which channel actually makes us money?",
    headline=(
        "Online sells 43% of our orders and earns 17% of our contribution. "
        "It keeps 32p of every revenue pound; the branch keeps 82p."),
    read="""
Point at the first bar and the last bar, in that order, and say nothing else
about the middle two until someone asks.

  * bar 1 — orders. This is the shape of the business people carry in their
    heads. Online is the biggest thing we do.
  * bar 4 — contribution. This is the shape of the business that pays for the
    business. Online is the smallest.
  * the right-hand panel is the same fact as a rate, and the rate is what
    people remember a week later: 32p against 82p.

Say the middle bars only to kill the objection before it arrives: turnover is
the currency the customer hands over, which is not our money at any point.
£61m of turnover and £2.3m of revenue are both true and they are not the same
sentence.
""",
    ask=[
        ("So should we shut the online channel?",
         "No. Online earned £254k of contribution across the two years, which "
         "is real money we would lose. The chart says its costs to serve are "
         "structural, so the lever is the courier contract and the card fee, "
         "not the rate board."),
        ("Why is airport so much better?",
         "A 6.34pp spread against 3.61pp on the high street, on a customer who "
         "is past security and cannot shop around. It is the smallest order in "
         "the business and the most profitable one."),
        ("Is online growing faster than the rest?",
         "No, and I want to correct that before it becomes an assumption. "
         "Online orders grew 7.7% in 2025; the branch network grew 9.9%. Our "
         "channel mix is close to stable, which means this gap is a standing "
         "structural fact rather than a trend running away from us."),
    ],
    caveat=(
        "This is contribution, not profit. It is before every fixed cost — the "
        "£14k a month the Heathrow kiosk pays in rent is not in here, and it is "
        "the largest fixed cost we have. Contribution is the right measure for "
        "a price decision and the wrong one for a close-the-channel decision."),
    build=_fig_contribution,
)


# ==========================================================================
# 2. The pocket price waterfall
# ==========================================================================

def _fig_waterfall(db: MeridianDB) -> plt.Figure:
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.0), sharey=True)

    for ax, ch in zip(axes, ["branch", "online"]):
        full = db.price_waterfall(ch)
        board = float(full.iloc[0]["running_gbp"])
        pocket = float(full.iloc[-1]["running_gbp"])
        # Keep the board rate; drop the subtotal rows and any step too small
        # to draw. A bar under 10p on this scale is thinner than its own
        # outline — labelling a mark nobody can see is worse than omitting it,
        # so the narration carries those instead.
        steps = full.iloc[1:-1]
        steps = steps[~steps["step"].str.startswith("=")]
        steps = steps[steps["leak_gbp"].abs() >= 0.10].reset_index(drop=True)

        labels = (["board\nrate"]
                  + [s.replace("less ", "").replace(" ", "\n") for s in steps["step"]]
                  + ["pocket\nmargin"])

        ax.bar(0, board, 0.62, color=C[0], edgecolor="white", zorder=3)
        ax.text(0, board + 0.4, _money(board, True), ha="center", fontsize=9.5,
                color=INK, fontweight="bold")

        running = board
        for i, row in steps.iterrows():
            leak = float(row["leak_gbp"])
            top, bot = running, running - leak
            lo, hi = min(top, bot), max(top, bot)
            # A revenue step (negative leak) is green and points UP.
            ax.bar(i + 1, hi - lo, 0.62, bottom=lo,
                   color=C[1] if leak < 0 else C[5], edgecolor="white", zorder=3)
            ax.text(i + 1, hi + 0.4, f"{'+' if leak < 0 else '−'}{abs(leak):.2f}",
                    ha="center", fontsize=9, color=C[1] if leak < 0 else C[5],
                    fontweight="bold")
            running = bot
            ax.plot([i + 0.69, i + 1.31], [running, running], color=MUT, lw=0.9, zorder=2)

        n = len(steps) + 1
        ax.bar(n, pocket, 0.62, color=C[3], edgecolor="white", zorder=3)
        ax.text(n, pocket + 0.4, _money(pocket, True), ha="center", fontsize=9.5,
                color=INK, fontweight="bold")

        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, fontsize=8.5)
        ax.set_ylim(0, 27)
        ax.set_axisbelow(True)          # gridlines behind the bars, not through them
        tidy(ax)
        _headline(fig, ax, f"{ch} — {pocket / board:.0%} of the board rate reaches the pocket",
                  f"average order, {_money(board, True)} of board rate")

    axes[0].set_ylabel("£ per order")
    _note(axes[1], "the card fee is\nrevenue, not a leak",
          xy=(1.0, 15.3), xytext=(0.45, 20.6), colour=C[1])
    _note(axes[1], "payment fee and courier are\nbigger than the entire\nbranch spread",
          xy=(2.9, 11.5), xytext=(2.45, 22.6), colour=C[5])
    fig.tight_layout()
    return fig


CH_WATERFALL = Chart(
    key="waterfall",
    question="Where does the price we advertise actually go?",
    headline=(
        "We advertise the same kind of rate in both channels and keep 86p in "
        "the pound on the high street against 36p online. Nothing in that gap "
        "is a price decision."),
    read="""
Read each waterfall left to right, out loud, as a sentence. Do not describe
the bars — perform the arithmetic.

  "We start at £18.54 of board rate on a typical branch order. The card fee
   adds 86p. Funding costs us £1.16, the payment fee £1.02, handling £1.33.
   We keep £15.89."

Then the same for online, and let the difference land on its own:

  "Same starting point, near enough — £13.27. The fee adds £1.67 because
   online sells most of the travel cards. Then the payment fee takes £4.58 and
   the courier takes £2.98. We keep £4.73."

Two marks are worth pointing at:

  * the green bar going UP. An ancillary fee is revenue. Hide it and you lose
    track of a lever that is far less elastic than the headline rate.
  * the two red bars on the right of the online chart. Together they are
    larger than the entire spread on a branch order. That is the sentence.
""",
    ask=[
        ("Can we just charge online customers more?",
         "We could, and demand there is the most price-sensitive we have "
         "measured — the March experiment lost 16% of conversions for 0.4pp. "
         "Closing a £11 gap on the rate board is not available."),
        ("What would actually close it?",
         "The courier contract and the card acquiring rate. £2.98 and £4.58 of "
         "cost per order, both negotiated rather than engineered, both sitting "
         "in someone else's budget. That is where the £11 is."),
        ("Why is the branch waterfall so flat?",
         "Because its costs barely scale with the order. Handling is £1.33 "
         "whether the order is £200 or £2,000, so a bigger basket is nearly "
         "pure contribution."),
    ],
    caveat=(
        "This is the average order, and the average waterfall hides the tail. "
        "The small online orders lose money outright once the £2.98 courier is "
        "on them — I would want a minimum-order or a delivery charge on the "
        "bottom decile before I touched anything else."),
    build=_fig_waterfall,
)


# ==========================================================================
# 3. The discount hurdle
# ==========================================================================

def _fig_hurdle(db: MeridianDB) -> plt.Figure:
    cuts = np.arange(0.02, 0.26, 0.0025)
    econ = db.discount_hurdles(0.10).set_index("channel")
    cm = econ["contribution_margin"]
    ymax = 140

    fig, ax = plt.subplots(figsize=(10.0, 5.2))
    for ch in ["branch", "airport", "online"]:
        m = float(cm[ch])
        need = 100 * np.where(cuts < m, cuts / (m - cuts), np.inf)
        ax.plot(100 * cuts, need, color=CHANNEL_C[ch], lw=2.4)

        # Direct-label each curve at the last point still inside the axes.
        # A label parked at the curve's true endpoint would be off the chart —
        # the online hurdle goes to infinity as the cut approaches its margin.
        inside = np.where(need <= ymax - 6)[0]
        i = int(inside[-1])
        ax.text(100 * cuts[i] + 0.45, need[i], f"{ch}  (CM {m:.0%})",
                color=CHANNEL_C[ch], fontsize=10.5, va="center", fontweight="bold")

    # The 10% column, marked, because that is the discount people propose.
    ax.axvline(10, color=MUT, lw=1, ls=(0, (4, 3)), zorder=1)
    dots = sorted(((float(econ.loc[c, "volume_uplift_needed"]), c)
                   for c in ["branch", "airport", "online"]))
    for rank, (v, ch) in enumerate(dots):
        y = 100 * v
        ax.plot([10], [y], "o", color=CHANNEL_C[ch], ms=7, zorder=5)
        # The branch and airport dots are a point apart; stagger the labels
        # rather than let them collide.
        dy = (-9, 9, 0)[rank] if rank < 2 else 0
        ax.annotate(f"+{y:.0f}%", xy=(10, y), xytext=(9.3, y + dy),
                    ha="right", va="center", fontsize=10.5,
                    color=CHANNEL_C[ch], fontweight="bold",
                    arrowprops=dict(arrowstyle="-", color=CHANNEL_C[ch], lw=0.9)
                    if dy else None)

    # What the business has actually been shown to deliver from a rate move.
    ax.axhspan(0, 20, color=C[1], alpha=0.08, zorder=0)
    ax.text(24.6, 17.5, "the largest response we have ever measured",
            fontsize=9.5, color=C[1], ha="right")

    ax.set_xlim(2, 25); ax.set_ylim(0, ymax)
    ax.set_xlabel("rate cut, % of the spread we charge")
    ax.set_ylabel("extra orders needed just to stand still, %")
    ax.set_axisbelow(True)
    tidy(ax)
    _headline(fig, ax,
              "A 10% rate cut online has to find 46% more orders to break even",
              "volume uplift required to hold contribution flat  ·  d / (CM − d)")
    fig.tight_layout()
    return fig


CH_HURDLE = Chart(
    key="hurdle",
    question="Can we do 10% off?",
    headline=(
        "A 10% rate cut needs 14% more orders on the high street and 46% more "
        "online, just to stand still. The best uplift we have ever measured "
        "from a rate move is about 16%."),
    read="""
This chart has one job: to turn "can we discount?" into an arithmetic question
that answers itself. Walk it in three moves.

  1. Point at the dashed line — that is the 10% someone just proposed.
  2. Read the three dots off it: +13% airport, +14% branch, +46% online.
  3. Point at the shaded band: that is the size of response we have actually
     observed. The branch dot is on the edge of it. The online dot is nowhere
     near it.

Then say the rule the curves encode, because it is the thing worth
remembering after the chart is gone: **the thinner the margin, the steeper the
hurdle.** Online has a third of the branch's contribution margin, so the same
headline discount asks it for more than three times the volume.
""",
    ask=[
        ("Where does the curve come from?",
         "d divided by (CM − d). A 10% cut on a 32% margin leaves 22% to earn "
         "the lost money back with, so you need 10/22 — 46% — more orders. It "
         "is arithmetic, not a forecast."),
        ("What if we discount only 5%?",
         "Then online needs +18% and the branch +6%. The branch becomes "
         "arguable at 5%; online does not become arguable until about 3%."),
        ("Isn't a price rise just this in reverse?",
         "No, and this is worth being precise about. A 10% rise can afford to "
         "lose 24% of online volume before it costs us anything. The trade is "
         "never symmetric — rises always buy more room than cuts cost."),
    ],
    caveat=(
        "The hurdle is not a decision, it is the bar the decision has to clear. "
        "It assumes contribution margin holds as volume moves, which stops "
        "being true if the extra orders are smaller ones, and it counts nothing "
        "beyond this year — a defensive cut that keeps a customer may be worth "
        "more than the hurdle says."),
    build=_fig_hurdle,
)


# ==========================================================================
# 4. The demand curve you see vs the one you measured
# ==========================================================================

def _fig_elasticity(db: MeridianDB) -> plt.Figure:
    obs = db.query("""
        SELECT ROUND(quoted_margin_pp - comp_best_margin_pp, 1) AS above,
               COUNT(*) AS n, AVG(converted) AS conv
        FROM fct_quotes GROUP BY above HAVING n > 2000 ORDER BY above
    """)
    arms = db.query("""
        SELECT arm, COUNT(*) n, AVG(quoted_margin_pp) mpp, AVG(converted) conv
        FROM fct_quotes WHERE arm IS NOT NULL GROUP BY arm
    """).set_index("arm")

    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(12.0, 4.9),
                                  gridspec_kw={"width_ratios": [1.5, 1]})

    # Left — what you get by looking at the data as it fell out.
    ax.scatter(obs["above"], 100 * obs["conv"], s=obs["n"] / 90,
               color=C[0], alpha=0.55, edgecolor="white", linewidth=0.8, zorder=3)
    b = np.polyfit(obs["above"], np.log(obs["conv"]), 1, w=np.sqrt(obs["n"]))
    xs = np.linspace(obs["above"].min(), obs["above"].max(), 50)
    ax.plot(xs, 100 * np.exp(np.polyval(b, xs)), color=C[0], lw=2.2, zorder=4)
    ax.text(0.9, 63, f"what the history says\n{100 * b[0]:.0f}% of demand per pp",
            color=C[0], fontsize=10, fontweight="bold")

    # The same slope drawn from the experiment's own starting point, so the
    # two lines are visually comparable rather than just two numbers.
    dpp = float(arms.loc["test", "mpp"] - arms.loc["control", "mpp"])
    semi = (float(arms.loc["test", "conv"]) / float(arms.loc["control", "conv"]) - 1) / dpp
    x0, y0 = 0.0, 100 * float(obs.set_index("above").loc[0.0, "conv"])
    ax.plot(xs, y0 * np.exp(semi * (xs - x0)), color=C[5], lw=2.2, ls=(0, (5, 2)))
    ax.text(-0.75, 40, f"what the experiment says\n{100 * semi:.0f}% of demand per pp",
            color=C[5], fontsize=10, fontweight="bold")

    ax.set_xlabel("our rate minus the best rate in the market, pp")
    ax.set_ylabel("quotes that converted, %")
    ax.set_ylim(30, 75)
    tidy(ax)
    _headline(fig, ax, "The history understates our price sensitivity threefold",
              "bubble size = quotes  ·  220,945 quotes, 2024–25")

    # Right — the experiment on its own, with the interval, because a
    # difference without an interval is an anecdote.
    conv = 100 * arms["conv"]
    err = 100 * 1.96 * np.sqrt(arms["conv"] * (1 - arms["conv"]) / arms["n"])
    bars = ax2.bar(["control\n2.35pp", "test\n2.76pp"], conv.values,
                   yerr=err.values, capsize=6, width=0.55,
                   color=[C[0], C[5]], edgecolor="white",
                   error_kw=dict(ecolor=SUB, lw=1.3))
    _label_bars(ax2, bars, lambda v: f"{v:.1f}%", inside=True)
    ax2.set_ylim(0, 78)
    ax2.set_ylabel("conversion, %")
    tidy(ax2)
    _headline(fig, ax2, "+0.40pp cost us 9.6pp of conversion",
              "randomised, 4,624 online quotes, Mar–Apr 2025")
    ax2.annotate("", xy=(1, conv.iloc[1] + 6), xytext=(0, conv.iloc[0] + 6),
                 arrowprops=dict(arrowstyle="->", color=INK, lw=1.4))
    ax2.text(0.5, conv.iloc[0] + 8, "−16% of demand", ha="center",
             fontsize=10, color=INK, fontweight="bold")
    fig.tight_layout()
    return fig


CH_ELASTICITY = Chart(
    key="elasticity",
    question="How much volume do we lose if we put the rate up?",
    headline=(
        "Our own trading history says we lose 12% of demand per point of rate. "
        "The randomised test says 39%. The history is wrong, and the direction "
        "of the error is the expensive one — it makes every price rise look safe."),
    read="""
Show the left panel first and let them believe it for about ten seconds. It is
a clean, well-populated, entirely honest chart, and it is the one most pricing
decks stop at.

Then put the dashed line on it and explain why the two disagree:

  "We never set our rate at random. We charge more when demand is strong — in
   August, at the airport, to the customers who are not shopping around. So
   the high-rate points on this chart are also the high-demand points, and the
   two effects cancel out. The chart is not measuring what price does to
   demand. It is measuring where we chose to put our prices."

Then the right panel, which is the answer:

  "In March we flipped a coin on 4,624 online quotes and put 0.4pp on half of
   them. Conversion fell from 60.0% to 50.5%. Nothing else differed, because
   nothing else could — that is what the coin flip buys us. The error bars do
   not overlap."
""",
    ask=[
        ("Which number should we plan on?",
         "Thirty, and stress-test at forty. The point estimate is 39% but the "
         "95% interval runs from 27% to 51%, so quoting 39% to two figures "
         "would be false precision. And this is online cash only — the same "
         "test has never been run at the kiosk, where last-minute buyers past "
         "security are the least sensitive customers we have. Never carry one "
         "channel's elasticity into another."),
        ("The experiment is only 4,624 quotes. Is that enough?",
         "Enough to act on, not enough to be precise with. The 95% interval on "
         "the conversion drop runs 6.7pp to 12.4pp — wide, but comfortably "
         "clear of zero, so the direction and the rough size are settled. "
         "Telling 30% apart from 39% would need roughly ten times the sample, "
         "which is why I am giving you a range rather than a number."),
        ("Then why do we produce the left-hand chart at all?",
         "For the segment and seasonal patterns inside it, which are real. Just "
         "never for a slope. The rule is: describe with history, decide with "
         "experiments."),
    ],
    caveat=(
        "The experiment ran on online cash for eight weeks in spring, so it "
        "carries the seasonality of exactly those weeks. It also measures the "
        "first-order response only — a customer we lose today may also not come "
        "back next year, and that is a separate and larger number."),
    build=_fig_elasticity,
)


# ==========================================================================
# 5. Retention — the cost of a price rise that does not show up this year
# ==========================================================================

def _fig_retention(db: MeridianDB) -> plt.Figure:
    # Split each bucket's retention loss into the part price explains and the
    # part it does not. Customers who were never refused for stock isolate the
    # price effect; the rest of the bar is what running out of cash costs us.
    r = db.query("""
        SELECT price_bucket,
               COUNT(*)                                              AS customers,
               ROUND(AVG(margin_above_market), 3)                    AS above,
               ROUND(AVG(retention_multiplier), 4)                   AS retention,
               ROUND(AVG(CASE WHEN refused = 0 THEN retention_multiplier END), 4)
                                                                     AS retention_no_refusal
        FROM (SELECT *, NTILE(5) OVER (ORDER BY margin_above_market) AS price_bucket
              FROM fct_customer_year)
        GROUP BY price_bucket ORDER BY price_bucket
    """)
    price_pct = 100 * (r["retention_no_refusal"] - 1)
    stock_pct = 100 * (r["retention"] - r["retention_no_refusal"])

    fig, ax = plt.subplots(figsize=(10.5, 5.2))
    x = np.arange(len(r))
    b1 = ax.bar(x, price_pct, width=0.6, color=C[5], zorder=3,
                label="what the price cost us")
    ax.bar(x, stock_pct, width=0.6, bottom=price_pct, color=C[2], zorder=3,
           label="what running out of cash cost us")

    for xi, (pv, sv) in enumerate(zip(price_pct, stock_pct)):
        if pv < -0.4:
            ax.text(xi, pv / 2, f"{pv:.1f}", ha="center", va="center",
                    fontsize=9.5, color="white", fontweight="bold")
        ax.text(xi, pv + sv - 0.28, f"{pv + sv:.1f}%", ha="center", va="top",
                fontsize=10.5, color=INK, fontweight="bold")

    # The claim, drawn: 12% of next year's trips per point above the market.
    ref = -12 * np.clip(r["above"], 0, None)
    ax.plot(x, ref, color=INK, lw=1.6, ls=(0, (5, 2)), zorder=4)
    ax.text(4.34, float(ref.iloc[-1]) + 0.1, "12% per point\nabove the market",
            fontsize=9.5, color=INK, va="center")

    ax.set_xticks(x)
    ax.set_xticklabels([f"{v:+.2f}pp\n({n:,} customers)"
                        for v, n in zip(r["above"], r["customers"])], fontsize=9)
    ax.set_xlim(-0.6, 5.35)
    ax.set_ylim(-9, 1)
    ax.axhline(0, color=MUT, lw=1, zorder=2)
    ax.set_ylabel("next year's orders vs a customer priced at market, %")
    ax.set_xlabel("average rate paid above the best rate in the market")
    ax.legend(loc="lower left", fontsize=9.5)
    tidy(ax)
    _headline(fig, ax,
              "Price costs 12% of next year's trips per point. "
              "Running out of cash costs another 1.4%, flat.",
              "32,259 customer-years in fifths  ·  the dashed line is the price effect alone")
    fig.tight_layout()
    return fig


CH_RETENTION = Chart(
    key="retention",
    question="What does a price rise cost us next year?",
    headline=(
        "Every point of rate we charge above the market costs us 12% of that "
        "customer's trips next year. It never lands in the month we took the "
        "price, so no monthly report we produce will ever show it."),
    read="""
This is the chart that changes what a price rise is worth, so give it time.

  * left to right, our customers sorted into fifths by how far above the
    market we priced them. The left-hand two fifths we priced at or *below*
    the market.
  * the height of each bar is how much less they came back the following
    year, against a customer priced at market.
  * **the bar is split by cause.** Red is what the price cost us. Amber is
    what running out of cash cost us — customers we turned away in August
    because the branch had nothing left to sell.

Then point at the dashed line, because it is the claim and the proof at once:

  "That line is 12% of next year's trips per point above the market, drawn
   from the coefficient rather than fitted to these bars. It lands on the
   bottom of the red block in every bucket. That is the price effect, and it
   is clean."

And read the amber blocks across, because their message is the opposite:

  "The amber is about 1.4% in every bucket — it does not care what we charged.
   Being unable to serve someone costs us roughly a point and a half of next
   year regardless of price. We have never costed that, and August is when we
   do it."

Then convert it into money, because the chart is in percentages and the
decision is in pounds:

  "A frequent flyer is worth £56 of contribution a year. Take half a point
   more and we earn a few pounds now and lose 6% of every year after it. On a
   four-year relationship that trade is roughly a wash — and a straight loss
   on anyone who would have stayed longer."
""",
    ask=[
        ("Is this cause, or is it just that certain customers pay more?",
         "Partly the second, and I would not present it as causal on its own. "
         "What makes me take it seriously is that the red blocks land on the "
         "12%-per-point line in all five buckets, including the two where we "
         "priced below the market and the effect should be — and is — zero. A "
         "pure selection artefact would not respect that boundary."),
        ("So do we never raise prices?",
         "We raise them where the lifetime arithmetic still works. Last-minute "
         "airport buyers barely respond and barely repeat: raise there. "
         "Frequent flyers respond and repeat: that is where a rise costs more "
         "than it earns."),
        ("How would we prove it properly?",
         "Hold the rate flat for a random half of a region for two quarters and "
         "measure repeat rates the year after. It is a long experiment, which "
         "is exactly why nobody has run it and why this effect stays invisible."),
    ],
    caveat=(
        "The split is clean but the whole thing is observational. Nobody was "
        "randomly assigned to a price bucket, and the customers we charged most "
        "above the market are disproportionately last-minute airport buyers, "
        "who behave differently for reasons that have nothing to do with price. "
        "The top bucket also spans +0.28pp to +1.6pp, so its average hides most "
        "of its range. I am showing you a pattern consistent with the lifetime "
        "story, not proof of it."),
    build=_fig_retention,
)


# ==========================================================================
# 6. The segment map — where the price is, and where the demand is
# ==========================================================================

#: One colour per segment, held across all three panels. In a small-multiple
#: the reader learns the colour once in the first panel and then reads the
#: other two without looking back at a legend — which is the entire reason to
#: draw small multiples instead of one crowded scatter.
SEGMENT_C = {"last_minute": C[1], "holiday_family": C[0],
             "frequent_flyer": C[4], "bargain_hunter": C[5]}
SEGMENT_ORDER = ["last_minute", "holiday_family", "frequent_flyer", "bargain_hunter"]


def _fig_segments(db: MeridianDB) -> plt.Figure:
    m = db.margin_by_segment()

    fig, axes = plt.subplots(1, 3, figsize=(13.0, 4.8), sharex=True)
    for ax, ch in zip(axes, ["online", "branch", "airport"]):
        s = (m[m["channel"] == ch].set_index("segment")
             .loc[SEGMENT_ORDER[::-1]])          # best at the top
        y = np.arange(len(s))
        ax.barh(y, 100 * s["conversion"], height=0.62,
                color=[SEGMENT_C[i] for i in s.index], zorder=3)
        for yi, (seg, row) in zip(y, s.iterrows()):
            conv = 100 * row["conversion"]
            ax.text(conv + 1.8, yi, f"{conv:.0f}%", va="center",
                    fontsize=10, color=INK, fontweight="bold")
            # A name printed inside a short bar spills out of it and collides
            # with the value. Park it outside instead, in ink rather than white.
            if conv > 28:
                ax.text(1.8, yi, seg.replace("_", " "), va="center", fontsize=9.5,
                        color="white", fontweight="bold", zorder=4)
            else:
                ax.text(conv + 12, yi, seg.replace("_", " "), va="center",
                        fontsize=9.5, color=SUB, zorder=4)
        ax.set_yticks([]); ax.set_xlim(0, 100)
        ax.set_ylim(-0.6, len(s) - 0.4)
        ax.grid(False)
        for sp in ("left", "bottom"):
            ax.spines[sp].set_visible(False)
        rate = float(s["avg_quoted_margin_pp"].mean())
        _headline(fig, ax, f"{ch}  —  we quote {rate:.2f}pp",
                  f"£{s['contribution_gbp'].sum() / 1000:,.0f}k of contribution")

    fig.suptitle("Push the rate from 2.7pp to 6.3pp and last-minute buyers "
                 "do not blink — bargain hunters halve, twice",
                 x=0.008, ha="left", fontsize=13.5, color=INK, fontweight="bold")
    # One annotation, in the gap between the bottom two rows — the only
    # genuinely empty space on the panel. Two arrows on a chart this legible
    # would be fighting the bars for attention.
    axes[2].text(41, 0.5, "the same 6.34pp, and four\nout of five walk away",
                 va="center", fontsize=9.5, color=C[5], linespacing=1.35)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    return fig


CH_SEGMENTS = Chart(
    key="segments",
    question="Are we charging the right customers the right rate?",
    headline=(
        "Between online and the airport our rate goes up by 3.7 points. "
        "Last-minute conversion moves by one point; bargain hunters fall from "
        "49% to 18%. We are quoting one price to four different businesses."),
    read="""
Three panels, cheapest rate on the left, dearest on the right. Read across
each colour, not down each panel — the story is in how differently the four
rows respond to the same 3.7 points of rate.

  * **last minute** (green) — 80%, 79%, 80%. Flat. Someone past security whose
    flight leaves in an hour is not comparing rates, and we could have
    guessed that; what we could not have guessed is how completely flat it is.
  * **bargain hunter** (red) — 49%, 34%, 18%. It halves, and then it nearly
    halves again. Same product, same company, same week.
  * **holiday family** and **frequent flyer** sit in between and slope the way
    you would expect a demand curve to slope.

The line to land: **the rate board knows where the customer is standing and
nothing about who they are.** We are charging our least price-sensitive
customers and our most price-sensitive customers the same number, and the
only reason it works at all is that they tend to stand in different places.
""",
    ask=[
        ("Can we actually price by segment?",
         "Partly, and carefully. Time of day, product and channel are legitimate "
         "proxies we already use. Charging an identifiable individual more "
         "because a model says they will pay is where Consumer Duty stops us — "
         "notebook 09 sets the boundary."),
        ("What's the size of the prize?",
         "Bargain hunters at the airport are 3,972 quotes converting at 18% — "
         "£16k of contribution against last-minute's £254k in the same kiosk. "
         "Almost all of that gap is conversion, not basket size. Even a "
         "discounted sale to most of the 82% we currently lose is additive."),
        ("Why not just cut the airport rate for everyone?",
         "Because the top-right bubble is £254k and it is not asking for a "
         "discount. A blanket cut hands margin to the customers least likely to "
         "walk. Any move here has to be conditional or it is just a giveaway."),
    ],
    caveat=(
        "Conversion is not elasticity, and this chart is not a demand curve. "
        "The three panels differ in far more than rate — a browser at home and "
        "a kiosk past security are different purchases, and the segment mix "
        "differs across them too. Read it as a map of where we are, not as a "
        "prediction of what a rate move would do. For that, only the "
        "experiment counts."),
    build=_fig_segments,
)


# ==========================================================================
# 7. The revenue bridge
# ==========================================================================

def _fig_bridge(db: MeridianDB) -> plt.Figure:
    from pricing_finance import price_volume_mix

    b = db.revenue_bridge(2024, 2025)
    cols = ["product_id", "price", "volume"]
    pvm = (price_volume_mix(b[b["year"] == 2024][cols], b[b["year"] == 2025][cols])
           .set_index("effect")["gbp"])
    base, comp = float(pvm["base revenue"]), float(pvm["comparison revenue"])

    steps = [("volume", float(pvm["volume"]), "8.4% more orders"),
             ("mix", float(pvm["mix"]), "nil — the product\nsplit did not move"),
             ("price", float(pvm["price"]), "0.9% of rate\ngiven back")]

    fig, ax = plt.subplots(figsize=(10.2, 5.4))
    lo_axis = 1_050_000
    ax.bar(0, base - lo_axis, 0.62, bottom=lo_axis, color=C[0], zorder=3)
    ax.text(0, base + 4_000, _money(base), ha="center", fontsize=11,
            color=INK, fontweight="bold")

    running = base
    ax.plot([0.31, 0.69], [running, running], color=MUT, lw=1, zorder=2)
    for i, (label, val, note) in enumerate(steps, start=1):
        lo, hi = min(running, running + val), max(running, running + val)
        # A bar under £2k is invisible on a £1.1m axis. Draw a tick so the step
        # still reads as a step, and let the label carry the number — never
        # inflate a bar to make a nil effect look like something.
        height = max(hi - lo, 1_200)
        ax.bar(i, height, 0.62, bottom=lo, zorder=3,
               color=C[1] if val > 0 else C[5])
        ax.text(i, hi + 4_000, f"{'+' if val > 0 else '−'}{_money(abs(val))}",
                ha="center", fontsize=11, color=C[1] if val > 0 else C[5],
                fontweight="bold")
        ax.text(i, hi + 15_000, note, ha="center", fontsize=9, color=SUB,
                va="bottom", linespacing=1.4)
        running += val
        ax.plot([i + 0.31, i + 0.69], [running, running], color=MUT, lw=1, zorder=2)

    ax.bar(4, comp - lo_axis, 0.62, bottom=lo_axis, color=C[3], zorder=3)
    ax.text(4, comp + 4_000, _money(comp), ha="center", fontsize=11,
            color=INK, fontweight="bold")

    ax.set_xticks(range(5))
    ax.set_xticklabels(["2024\nrevenue", "volume", "mix", "price", "2025\nrevenue"])
    ax.set_ylim(lo_axis, 1_290_000)
    ax.set_yticks([])
    ax.grid(False)
    ax.spines["left"].set_visible(False)
    _headline(fig, ax,
              "Revenue grew 7.4% and pricing was not the reason — rate went backwards",
              "gross revenue bridge, 2024 → 2025, split by product")
    fig.tight_layout()
    return fig


CH_BRIDGE = Chart(
    key="bridge",
    question="Revenue is up 7.4% — how did pricing do?",
    headline=(
        "All of the growth is volume, and then some. We sold 8.4% more orders "
        "and gave 0.9% of rate back doing it. Pricing did not deliver this year; "
        "it cost us £10k."),
    read="""
The bridge exists to stop one specific thing happening: a good year being
attributed to pricing, or a bad one being blamed on it, with nobody able to
check. Walk it as three separate causes.

  "£1.108m in 2024. Volume added £93k — we served 8.4% more orders. Mix took
   £185, which is nothing; the product split barely moved. Price took £10k
   back: average revenue per order fell 0.9%. £1.190m in 2025."

Say the last sentence plainly and do not soften it:

  "So the honest read is that the business grew and pricing was slightly
   dilutive. If we want pricing to show up in this bridge next year, the
   airport rate is where it would come from."

Bringing this table before you are asked is the difference between a pricing
function that gets funded and one that gets audited.
""",
    ask=[
        ("Is a 0.9% rate decline bad?",
         "Not necessarily — it is the price of the volume. £93k of volume for "
         "£10k of rate is a trade I would make again. What matters is that we "
         "chose it rather than discovering it."),
        ("Why is the mix effect so small?",
         "Because nothing moved. I re-ran the bridge split by channel rather "
         "than product and the mix effect is minus £9 — the channel shares are "
         "flat to a rounding error. That is worth saying out loud, because "
         "'mix' is the line people reach for when they want the answer to be "
         "someone else's fault."),
        ("Can we bridge contribution instead of revenue?",
         "Yes, and we should. Contribution grew 6.7% against revenue's 7.4%, so "
         "the growth we took was slightly poorer-quality than the base. On a "
         "revenue bridge that gap is invisible. It is the more honest chart and "
         "I will bring it next month."),
    ],
    caveat=(
        "'Price' here is average revenue per order, so it moves whenever the "
        "mix inside a product moves. Bigger baskets at the same rate would show "
        "up as a price rise. Splitting to product × channel × size tightens it. "
        "No bridge is completely clean; there are only bridges whose residual "
        "you have named."),
    build=_fig_bridge,
)


# ==========================================================================
# 8. Stockouts — when sales stop measuring demand
# ==========================================================================

def _fig_stockouts(db: MeridianDB) -> plt.Figure:
    s = db.query("""
        SELECT strftime('%Y-%m', date) AS ym,
               ROUND(100.0 * AVG(stockout_flag), 2) AS stockout_rate,
               ROUND(AVG(value_sold_gbp), 0)        AS sold,
               ROUND(AVG(stock_limit_gbp), 0)       AS limit_gbp
        FROM fct_stock GROUP BY ym ORDER BY ym
    """)
    s["month"] = pd.to_datetime(s["ym"] + "-01")

    fig, ax = plt.subplots(figsize=(11.0, 4.9))
    ax.fill_between(s["month"], 0, s["stockout_rate"], color=C[5], alpha=0.16)
    ax.plot(s["month"], s["stockout_rate"], color=C[5], lw=2.4)
    ax.set_ylabel("branch-days that hit the cash limit, %", color=C[5])
    ax.tick_params(axis="y", colors=C[5])
    ax.set_ylim(0, 26)

    ax2 = ax.twinx()
    ax2.plot(s["month"], s["sold"], color=C[0], lw=2.2, ls=(0, (5, 2)))
    ax2.set_ylabel("average cash sold per branch-day, £", color=C[0])
    ax2.tick_params(axis="y", colors=C[0])
    ax2.set_ylim(3_000, 7_000)
    ax2.grid(False)

    for ym, lbl in [("2024-08", None), ("2025-08", "21% of August branch-days\nsold out")]:
        row = s[s["ym"] == ym].iloc[0]
        ax.plot([row["month"]], [row["stockout_rate"]], "o", color=C[5], ms=8, zorder=5)
        if lbl:
            _note(ax, lbl, xy=(row["month"], row["stockout_rate"]),
                  xytext=(pd.Timestamp("2025-01-15"), 22), colour=C[5])

    tidy(ax)
    _headline(fig, ax,
              "In August we do not know what demand was — we ran out of cash",
              "monthly stockout rate against cash sold, branch network, 2024–25")
    fig.tight_layout()
    return fig


CH_STOCKOUTS = Chart(
    key="stockouts",
    question="Why can't we just read demand off the sales?",
    headline=(
        "One August branch-day in five hit the cash limit. On those days sales "
        "measured our stock, not our customers — and August is when we set the "
        "peak rate."),
    read="""
Two lines, and the point is where they stop agreeing.

  * the red area is the share of branch-days that hit the cash limit. It sits
    under 5% from October through May and reaches 21% in August 2025.
  * the blue dashed line is cash sold per branch-day. It climbs through every
    summer and then stops climbing in August — in 2024 it actually falls, from
    £5,120 a day in July to £5,013 in August, while the stockout rate goes the
    other way.

That is the whole chart. Sales did not stop rising because demand stopped
rising. They stopped rising because the branch had nothing left to sell.

Say what it costs us:

  "Every model we fit on August sales is fitted on a censored number. It reads
   the flat top as saturated demand and tells us the peak rate is already
   optimal. It cannot see the customers who were turned away, because they
   never became a row in the sales table."
""",
    ask=[
        ("How much demand did we actually lose?",
         "We can bound it, not measure it. Quotes carry a lost-to-stockout "
         "flag: about 10% of customer-years contain at least one refusal. The "
         "honest answer is that August demand is understated and we do not know "
         "by how much — which is itself the finding."),
        ("Does this change the peak rate?",
         "It changes what we can claim about it. Right now August is the month "
         "we are least entitled to have an opinion on, and it is the month "
         "carrying the highest rate. I would fix the measurement before I "
         "touched the rate."),
        ("What would fix it?",
         "Use quotes, not transactions — the customer who was refused is still "
         "a row there. And raise the August cash limit at the four worst "
         "branches for one summer, which buys us an uncensored month to "
         "estimate from."),
    ],
    caveat=(
        "The stockout flag is a branch-day flag, so a branch that ran out at "
        "4pm counts the same as one that never opened with enough. It "
        "overstates how much of the day was lost and understates nothing — so "
        "treat it as an upper bound on days and a lower bound on the problem."),
    build=_fig_stockouts,
)


# ==========================================================================
# The deck
# ==========================================================================

CHARTS: dict[str, Chart] = {c.key: c for c in [
    CH_CONTRIBUTION, CH_WATERFALL, CH_HURDLE, CH_ELASTICITY,
    CH_RETENTION, CH_SEGMENTS, CH_BRIDGE, CH_STOCKOUTS,
]}


def build(key: str, db: MeridianDB | None = None) -> tuple[plt.Figure, Chart]:
    """Build one chart. Returns the figure and its script."""
    if key not in CHARTS:
        raise ValueError(f"no chart {key!r}. Have: {', '.join(CHARTS)}")
    chart = CHARTS[key]
    own = db is None
    db = db or MeridianDB()
    try:
        style()
        return chart.build(db), chart
    finally:
        if own:
            db.close()


def build_all(out: Path = OUT, quiet: bool = False) -> list[Path]:
    """Build every chart into `out/`, and print the script for each."""
    out.mkdir(exist_ok=True)
    paths = []
    with MeridianDB() as db:
        style()
        for key, chart in CHARTS.items():
            fig = chart.build(db)
            path = out / f"{key}.png"
            fig.savefig(path, dpi=140, bbox_inches="tight",
                        facecolor=fig.get_facecolor())
            plt.close(fig)
            paths.append(path)
            if not quiet:
                print(chart.script())
                print(f"  -> {path.relative_to(path.parent.parent)}\n")
    return paths


if __name__ == "__main__":
    paths = build_all()
    print("=" * 78)
    print(f"  {len(paths)} charts written to {OUT}")
    print("=" * 78)
    print("""
  Now do the exercise, because building the chart is the easy half.

    1. Pick one chart. Read its `headline` out loud. Time yourself: it should
       take under eight seconds and contain at least one number.
    2. Cover the script and narrate the chart from the marks alone.
    3. Uncover the `ask` block. Answer each question out loud before reading
       the answer. If you cannot, you do not know the chart yet.
    4. Say the caveat last, and notice that saying it makes you sound more
       confident rather than less. That is the whole trick.

  STAKEHOLDER_STORYTELLING.md takes the language apart phrase by phrase.
""")
