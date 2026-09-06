"""Query Meridian FX from Python — and learn the questions worth asking.

    from db_helper import MeridianDB

    with MeridianDB() as db:
        print(db.pnl())                 # the P&L, top to bottom
        print(db.unit_economics())       # what one order earns, by channel
        print(db.discount_hurdles())     # what a rate cut must deliver

Build the database first with `python create_database.py` (which needs the
CSVs from `01_data_foundation.ipynb`).

There are two kinds of method here, and the split is deliberate.

**Plumbing** — `query`, `tables`, `schema`, `sample`, `truth`. Thin wrappers
so you can write your own SQL without boilerplate. Use these most.

**Worked views** — `pnl`, `unit_economics`, `discount_hurdles`,
`margin_by_segment`, `price_waterfall`, `revenue_bridge`, `stockout_cost`,
`retention_by_price`. Each is one question a pricing manager gets asked, with
the SQL written out and a docstring explaining what the answer means and how
it is normally misread. Read the SQL — it is the point, not an implementation
detail.

No method here estimates anything causal. Everything below is *description*:
what happened, sliced sensibly. Turning description into a causal claim —
"the price cut caused the volume" — is what notebooks 06 and 07 are for, and
skipping that step is the single most expensive mistake in the discipline.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

DEFAULT_DB = Path(__file__).parent / "data" / "meridian.db"

# SQLite has no date type, so dates come back as text. Left alone, that is a
# silent bug: `df["date"].dt.month` explodes, and worse, `df["date"] > "2025-2"`
# compares strings and quietly returns nonsense. Parse on the way out, always.
DATE_COLS = {"date", "week", "month", "start_date", "end_date"}


#: The three channels a pricing manager actually talks about. `dim_sites`
#: stores only `channel` (branch / online) and an `is_airport` flag, but the
#: Heathrow kiosk trades nothing like a high-street branch — different rate,
#: different cost to serve, different customer — so every commercial view
#: splits it out. Keep this in one place: if the definition of "channel"
#: drifts between two charts, the meeting stops being about pricing.
CHANNEL_SQL = "CASE WHEN s.is_airport = 1 THEN 'airport' ELSE s.channel END"

#: Columns you may slice a P&L by, and where each one lives. Anything on
#: `fct_transactions` is used directly; anything else is resolved against the
#: site dimension, which is joined in for you.
SLICEABLE = {
    "channel":    CHANNEL_SQL,
    "site_name":  "s.site_name",
    "site_id":    "s.site_id",
    "region":     "s.region",
    "market":     "s.market",
    "segment":    "t.segment",
    "product_id": "t.product_id",
    "promo_flag": "t.promo_flag",
    "arm":        "t.arm",
    "year":       "CAST(strftime('%Y', t.date) AS INTEGER)",
}


def _is_text(series: pd.Series) -> bool:
    """True for a column of strings, whatever pandas is calling that this year.

    `dtype == object` was the old test and stopped being true in pandas 3,
    where strings get their own dtype. Testing for what a column is *not*
    survives the next rename too. (`fct_calendar.month` is a genuine integer;
    `fct_marketing.month` is a date. Same name, different type, so the check
    has to be on the data.)
    """
    return not (pd.api.types.is_numeric_dtype(series)
                or pd.api.types.is_datetime64_any_dtype(series))


class MeridianDB:
    """A connection to `data/meridian.db`, plus the queries worth having.

    >>> db = MeridianDB()
    >>> len(db.tables()) >= 19
    True
    >>> db.close()
    """

    def __init__(self, db_path: str | Path | None = None):
        self.db_path = Path(db_path) if db_path else DEFAULT_DB
        if not self.db_path.exists():
            raise FileNotFoundError(
                f"No database at {self.db_path}.\n"
                "Build it with:  python create_database.py\n"
                "(which needs the CSVs from 01_data_foundation.ipynb — run that first)."
            )
        self.conn = sqlite3.connect(str(self.db_path))

    # ------------------------------------------------------------------
    # Plumbing
    # ------------------------------------------------------------------

    def query(self, sql: str, params: tuple = ()) -> pd.DataFrame:
        """Run SQL, get a DataFrame back, with dates parsed to real timestamps.

        >>> db = MeridianDB()
        >>> df = db.query("SELECT date, contribution_gbp FROM fct_daily LIMIT 5")
        >>> str(df["date"].dtype).startswith("datetime")
        True
        >>> db.close()

        That assertion is the whole reason this wrapper exists. `pd.read_sql`
        alone hands back the date as a *string*, and every subsequent month or
        season comparison silently does the wrong thing.
        """
        df = pd.read_sql(sql, self.conn, params=params)
        for column in df.columns:
            if column in DATE_COLS and _is_text(df[column]):
                parsed = pd.to_datetime(df[column], errors="coerce")
                if parsed.notna().any():
                    df[column] = parsed
        return df

    def tables(self) -> list[str]:
        """Every table in the database, dimensions first."""
        rows = self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()
        return [r[0] for r in rows]

    def schema(self, table: str) -> pd.DataFrame:
        """Columns and types for one table. Start here when you meet a table."""
        return self.query(f"PRAGMA table_info({self._safe(table)})")[["name", "type"]]

    def sample(self, table: str, n: int = 5) -> pd.DataFrame:
        """A few rows, to see what one row actually *is* — the grain."""
        return self.query(f"SELECT * FROM {self._safe(table)} LIMIT {int(n)}")

    def overview(self) -> pd.DataFrame:
        """Every table with its row count — the first thing to run on a new database."""
        rows = [{"table": t, "rows": self.conn.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]}
                for t in self.tables()]
        return pd.DataFrame(rows).sort_values("rows", ascending=False).reset_index(drop=True)

    def truth(self, like: str = "") -> pd.DataFrame:
        """The answer key. Search it: `db.truth('elasticity')`.

        Estimate first, then look. Checking the key before you have committed
        to a number feels efficient and teaches you nothing — the skill being
        built is judging whether your own estimate is trustworthy, and you
        cannot practise that with the answer on screen.
        """
        if like:
            return self.query("SELECT parameter, value FROM truth WHERE parameter LIKE ?",
                              (f"%{like}%",))
        return self.query("SELECT parameter, value FROM truth")

    def _safe(self, table: str) -> str:
        """Reject a table name that is not actually in the database."""
        if table not in self.tables():
            raise ValueError(f"No table named {table!r}. Try db.tables().")
        return f'"{table}"'

    # ------------------------------------------------------------------
    # Enriched fact tables — facts joined to the dimensions you slice by
    # ------------------------------------------------------------------

    def daily(self, limit: int | None = None) -> pd.DataFrame:
        """`fct_daily` joined to site, product and calendar attributes.

        One row per day x site x product — the grain management reporting
        lives at. `fct_daily` already carries the calendar fields, so this
        adds the site attributes you slice by (channel, region, market) and
        the product cost parameters you would otherwise have to look up.
        """
        return self.query(f"""
            SELECT d.*,
                   s.site_name, s.channel, s.region, s.market, s.is_airport,
                   s.fixed_cost_month_gbp,
                   p.product_name, p.category, p.handling_cost_gbp, p.card_fee_gbp
            FROM fct_daily d
            LEFT JOIN dim_sites    s ON d.site_id    = s.site_id
            LEFT JOIN dim_products p ON d.product_id = p.product_id
            ORDER BY d.date, d.site_id, d.product_id
            {self._limit(limit)}
        """)

    def quotes(self, limit: int | None = 50_000) -> pd.DataFrame:
        """`fct_quotes` joined to site, product and customer attributes.

        **The important table.** One row per shopping occasion, including the
        people who asked our rate and walked away. Conversion — and therefore
        every honest elasticity — lives here and nowhere else.

        220,945 rows, so it is limited by default. Pass `limit=None` for the
        lot, or filter in SQL with `db.query(...)`, which is what you should
        do for real work: pulling a fifth of a million rows into pandas to
        then group them is a habit worth not forming.
        """
        return self.query(f"""
            SELECT q.*,
                   s.site_name, s.channel, s.region, s.market, s.is_airport,
                   p.product_name, p.category,
                   c.age_band, c.tenure_years, c.digital_engaged, c.loyalty_member
            FROM fct_quotes q
            LEFT JOIN dim_sites     s ON q.site_id     = s.site_id
            LEFT JOIN dim_products  p ON q.product_id  = p.product_id
            LEFT JOIN dim_customers c ON q.customer_id = c.customer_id
            ORDER BY q.date, q.quote_id
            {self._limit(limit)}
        """)

    def transactions(self, limit: int | None = 50_000) -> pd.DataFrame:
        """`fct_transactions` joined to site, product and customer attributes.

        One row per completed order, with the full revenue and cost
        breakdown. Everything in the P&L comes from here.

        Remember what it cannot tell you: it holds only the customers who
        said yes. Average margin computed on this table is *realised* margin,
        which rises when you put prices up purely because the price-sensitive
        customers stopped appearing in it. That is selection, not success.
        """
        return self.query(f"""
            SELECT t.*,
                   s.site_name, s.channel, s.region, s.market, s.is_airport,
                   p.product_name, p.category,
                   c.age_band, c.tenure_years, c.digital_engaged, c.loyalty_member
            FROM fct_transactions t
            LEFT JOIN dim_sites     s ON t.site_id     = s.site_id
            LEFT JOIN dim_products  p ON t.product_id  = p.product_id
            LEFT JOIN dim_customers c ON t.customer_id = c.customer_id
            ORDER BY t.date, t.txn_id
            {self._limit(limit)}
        """)

    @staticmethod
    def _limit(limit: int | None) -> str:
        return "" if limit is None else f"LIMIT {int(limit)}"

    # ------------------------------------------------------------------
    # Worked views — one question each
    # ------------------------------------------------------------------

    def pnl(self, group_by: str = "channel") -> pd.DataFrame:
        """The P&L from turnover down to contribution, sliced how you like.

        Args:
            group_by: any key in `SLICEABLE` — 'channel', 'segment',
                'product_id', 'region', 'market', 'site_name', 'year'.

        The line order is the point, and it is the order every commercial
        P&L uses:

            turnover        the value of currency handed over. NOT ours.
            gross revenue   the spread we charged. This is our top line.
            variable cost   funding, payment fees, handling, delivery,
                            commission to the host retail network.
            contribution    what is left to pay for the branches and the
                            head office. THE number for a price decision.

        The gap between turnover and gross revenue is where careless pricing
        analysis dies. Meridian turns over ~£85m and books ~£3.1m of revenue:
        a "1% discount" means 1% of which one? Off turnover it is £850k and
        wipes out a quarter of the business; off revenue it is £31k. People
        do mean different things, so make them say.

        >>> MeridianDB().pnl("channel")["channel"].tolist()
        ['branch', 'airport', 'online']
        """
        column = self._slice(group_by)
        df = self.query(f"""
            SELECT {column} AS "{group_by}",
                   COUNT(*)                     AS orders,
                   SUM(t.order_value_gbp)       AS turnover_gbp,
                   SUM(t.gross_revenue_gbp)     AS gross_revenue_gbp,
                   SUM(t.variable_cost_gbp)     AS variable_cost_gbp,
                   SUM(t.contribution_gbp)      AS contribution_gbp
            FROM fct_transactions t
            JOIN dim_sites s ON t.site_id = s.site_id
            GROUP BY {column}
            ORDER BY contribution_gbp DESC
        """)
        df["contribution_margin"] = (df["contribution_gbp"] / df["gross_revenue_gbp"]).round(4)
        df["revenue_yield_pp"] = (100 * df["gross_revenue_gbp"] / df["turnover_gbp"]).round(3)
        return df

    def unit_economics(self, group_by: str = "channel") -> pd.DataFrame:
        """What ONE order earns, cost line by cost line.

        The P&L in totals tells you where the money is. This tells you where
        it *comes from*, which is what you can act on. Every column is a mean
        per order, in £.

        Read it across a row and the structure of the business appears:

          * **airport** — the *smallest* order in the business (£378 against
            £512 elsewhere) sold at nearly double the spread (6.34pp against
            3.61pp). A captive customer at the gate is not shopping around.
            £21.62 of contribution on an order costing £2.86 to serve.
          * **branch** — 3.61pp of spread on a £512 order, and only £2 an
            hour of costs to serve it, because the funding and payment costs
            scale with the order while handling does not. 82p of every
            revenue pound survives to contribution.
          * **online** — the same £509 order and almost the same spread as
            the branch, but a £4.58 card fee and a £2.98 courier turn £14.99
            of revenue into £4.73 of contribution. **32p in the pound against
            the branch's 82p.** This single fact is why "one price across all
            channels" (notebook 12) is a real question and not a tidy-up.

        >>> float(MeridianDB().unit_economics().set_index("channel")
        ...       .loc["online", "delivery_gbp"])
        2.98
        """
        column = self._slice(group_by)
        return self.query(f"""
            SELECT {column} AS "{group_by}",
                   COUNT(*)                            AS orders,
                   ROUND(AVG(t.order_value_gbp), 2)    AS avg_order_gbp,
                   ROUND(AVG(t.margin_pp), 3)          AS avg_margin_pp,
                   ROUND(AVG(t.gross_revenue_gbp), 2)  AS revenue_gbp,
                   ROUND(AVG(t.funding_cost_gbp), 2)   AS funding_gbp,
                   ROUND(AVG(t.payment_fee_gbp), 2)    AS payment_gbp,
                   ROUND(AVG(t.handling_cost_gbp), 2)  AS handling_gbp,
                   ROUND(AVG(t.delivery_cost_gbp), 2)  AS delivery_gbp,
                   ROUND(AVG(t.variable_cost_gbp), 2)  AS variable_cost_gbp,
                   ROUND(AVG(t.contribution_gbp), 2)   AS contribution_gbp
            FROM fct_transactions t
            JOIN dim_sites s ON t.site_id = s.site_id
            GROUP BY {column}
            ORDER BY contribution_gbp DESC
        """)

    def discount_hurdles(self, discount_pct: float = 0.10,
                         group_by: str = "channel") -> pd.DataFrame:
        """How much extra volume a discount must produce, by slice.

        Joins the unit economics to the formula `d / (CM - d)` from
        `pricing_finance.discount_break_even_volume`, so you can answer the
        weekly "can we do 10% off?" without leaving the database.

        The `volume_uplift_needed` column is the answer to bring. Beside it,
        `volume_loss_affordable` shows what the same-sized price *rise*
        survives — the trade is never symmetric, and a rise almost always
        buys more room than a cut costs.

        A hurdle is not a decision. Put it next to an estimated elasticity
        (notebook 03) and ask whether the required uplift is achievable. If
        the hurdle is 48% and your best estimate of the response is 20%, the
        answer is no and no amount of enthusiasm changes it.
        """
        econ = self.unit_economics(group_by)
        cm = econ["contribution_gbp"] / econ["revenue_gbp"]
        out = econ[[group_by, "orders", "revenue_gbp", "contribution_gbp"]].copy()
        out["contribution_margin"] = cm.round(4)
        out["discount_pct"] = discount_pct
        out["volume_uplift_needed"] = (discount_pct / (cm - discount_pct)).where(
            cm > discount_pct, float("inf")).round(4)
        out["volume_loss_affordable"] = (-discount_pct / (cm + discount_pct)).round(4)
        return out

    def margin_by_segment(self) -> pd.DataFrame:
        """Conversion and margin by customer segment — the fixed `segment_analysis`.

        One row per segment x channel, built from `fct_quotes` so that the
        customers who *did not* buy are still in the denominator. The previous
        version of this method aggregated an alias that was never joined and
        could not run at all; this one is the query it was reaching for.

        `quotes`, `orders` and `conversion` come from the quote table;
        contribution is joined on from the transaction table, matched
        `quote_id` to `txn_id` (a transaction keeps its quote's id).

        What to look for: `bargain_hunter` converts worst and is quoted the
        keenest rates — because the pricing rule already discounts to them,
        not because keen prices repel customers. Reading a raw cross-tab of
        price against conversion here gives you an elasticity with the wrong
        *sign*. That confound is notebook 07's opening example.
        """
        return self.query(f"""
            SELECT q.segment,
                   {CHANNEL_SQL}                                  AS channel,
                   COUNT(*)                                       AS quotes,
                   SUM(q.converted)                               AS orders,
                   ROUND(1.0 * SUM(q.converted) / COUNT(*), 4)    AS conversion,
                   ROUND(AVG(q.quoted_margin_pp), 3)              AS avg_quoted_margin_pp,
                   ROUND(AVG(q.comp_best_margin_pp), 3)           AS avg_competitor_margin_pp,
                   ROUND(AVG(q.quoted_margin_pp - q.comp_best_margin_pp), 3)
                                                                  AS avg_above_market_pp,
                   ROUND(AVG(q.order_value_gbp), 2)               AS avg_order_gbp,
                   ROUND(COALESCE(SUM(t.contribution_gbp), 0), 2) AS contribution_gbp
            FROM fct_quotes q
            JOIN dim_sites s ON q.site_id = s.site_id
            LEFT JOIN fct_transactions t ON q.quote_id = t.txn_id
            GROUP BY q.segment, {CHANNEL_SQL}
            ORDER BY q.segment, channel
        """)

    def price_waterfall(self, channel: str = "branch") -> pd.DataFrame:
        """Board rate down to pocket margin, averaged over real orders.

        The **board rate** is what we advertise. The **pocket margin** is what
        survives after every adjustment the customer received and every cost
        of serving them. This runs the waterfall on real transactions rather
        than a worked example, so the lines reconcile to the penny:

            board rate  +  rate adjustments  +  ancillary fees  = gross revenue
            gross revenue  -  every variable cost               = pocket margin

        `leak_gbp` is signed: **positive takes money away, negative adds it.**
        A waterfall with an upward step is not a mistake, and hiding one is
        how businesses lose track of ancillary revenue.

        Read the three channels side by side and the whole pricing question
        appears:

          * **branch** — £18.54 of board rate becomes £15.89 of pocket. 86p in
            the pound. The card fee *adds* 86p; the costs of serving take
            £3.51, and handling (£1.33) is the biggest of them.
          * **airport** — £23.94 of board rate on a smaller order, because the
            rate is nearly double. £21.62 of pocket, 90p in the pound.
          * **online** — £13.27 of board rate becomes **£4.73**. 36p in the
            pound. Nothing is wrong with the price: the £4.58 payment fee and
            the £2.98 courier are simply larger than the entire spread on a
            branch order. You cannot fix this on the rate board.

        The steps that matter here are the ones nobody calls "price":

          * **the ancillary fee is revenue** (+£1.67 online, where the travel
            card sells best). Fees are a pricing lever people forget they
            own, and they are usually far less elastic than the headline rate;
          * **rate adjustments are almost nothing** (5p online, nil elsewhere).
            Meridian's promotions are not where its margin goes — which is
            worth knowing before anyone proposes cutting them;
          * **delivery is the whole online story**. A courier contract is
            negotiated, not engineered. It sits in another department's
            budget, which is why it is usually the margin nobody has taken.

        Always build this at order level, then look at the spread across
        orders. The average waterfall hides the tail, and the tail is where
        the money is.

        `pricing_finance.price_waterfall` renders the same structure for a
        hypothetical order when you want the shape on a slide.

        >>> wf = MeridianDB().price_waterfall("online")
        >>> float(wf.iloc[-1]["running_gbp"])
        4.73
        """
        row = self.query(f"""
            SELECT AVG(q.our_margin_pp * t.order_value_gbp / 100.0)      AS board,
                   AVG((q.quoted_margin_pp - q.our_margin_pp)
                       * t.order_value_gbp / 100.0)                      AS rate_adj,
                   AVG((t.margin_pp - q.quoted_margin_pp)
                       * t.order_value_gbp / 100.0)                      AS realised_adj,
                   AVG(t.gross_revenue_gbp
                       - t.margin_pp * t.order_value_gbp / 100.0)        AS ancillary,
                   AVG(t.funding_cost_gbp)                               AS funding,
                   AVG(t.payment_fee_gbp)                                AS payment,
                   AVG(t.handling_cost_gbp)                              AS handling,
                   AVG(t.delivery_cost_gbp)                              AS delivery,
                   AVG(t.gross_revenue_gbp)                              AS gross,
                   AVG(t.contribution_gbp)                               AS pocket
            FROM fct_transactions t
            JOIN fct_quotes q ON t.txn_id  = q.quote_id
            JOIN dim_sites  s ON t.site_id = s.site_id
            WHERE {CHANNEL_SQL} = ?
        """, (channel,))
        if row.empty or pd.isna(row.iloc[0]["board"]):
            raise ValueError(f"no orders for channel {channel!r}. "
                             f"Try 'branch', 'airport' or 'online'.")
        row = row.iloc[0]

        board = float(row["board"])
        # Signed so that `running - leak` walks down the page. Revenue steps
        # therefore carry a MINUS sign, which is the whole point of the
        # `leak_gbp` convention: an upward step is a negative leak.
        steps = [("board rate", 0.0, board)]
        running = board
        for label, key in [("rate adjustments",   "rate_adj"),
                           ("realisation",        "realised_adj"),
                           ("ancillary fees",     "ancillary"),
                           ("= gross revenue",    None),
                           ("less funding cost",  "funding"),
                           ("less payment fee",   "payment"),
                           ("less handling",      "handling"),
                           ("less delivery",      "delivery"),
                           ("= pocket margin",    None)]:
            leak = 0.0 if key is None else float(row[key])
            if key in ("rate_adj", "realised_adj", "ancillary"):
                leak = -leak          # these ADD to revenue
            running -= leak
            steps.append((label, leak, running))

        out = pd.DataFrame(steps, columns=["step", "leak_gbp", "running_gbp"])
        out["leak_gbp"] = out["leak_gbp"].round(2) + 0.0    # kill -0.00
        out["running_gbp"] = out["running_gbp"].round(2)
        out["pct_of_board"] = (100 * out["running_gbp"] / board).round(1)
        return out

    def revenue_bridge(self, year_from: int = 2024, year_to: int = 2025) -> pd.DataFrame:
        """Split a year-on-year revenue change into volume, mix and price.

        "Revenue is up" is not an answer to "how did pricing do?". The bridge
        separates the three causes, and only one of them is yours:

            volume   we served more orders
            mix      the orders we served were richer (or poorer)
            price    we charged more per order

        Feed the result to `pricing_finance.price_volume_mix` for the
        arithmetic; this method assembles the price and volume by product
        that it needs:

            bridge = db.revenue_bridge(2024, 2025)
            price_volume_mix(bridge[bridge.year == 2024][["product_id", "price", "volume"]],
                             bridge[bridge.year == 2025][["product_id", "price", "volume"]])

        Meridian 2024 -> 2025 comes out as revenue **+£82,249, and more than
        all of it is volume**: +£92,582 of volume, -£10,148 of price and
        -£185 of mix. The headline is "revenue up 7.4%". The bridge says the
        business sold 8.4% more orders and gave 0.9% of rate back doing it.

        That is the sentence a pricing manager has to be able to say out loud
        before someone else says the opposite. A pricing manager who cannot
        produce this table on request will have someone else's volume growth
        attributed to them, which sounds like a good problem until the year
        volume falls.

        One caveat to state whenever you show it: `price` here is average
        revenue per order, so it moves when the *mix within a product* moves —
        bigger orders at the same rate look like a price rise. Splitting to
        product x channel x size tier tightens it. There is no bridge that is
        completely clean; there are only bridges whose residual you have named.

        >>> MeridianDB().revenue_bridge()["year"].unique().tolist()
        [2024, 2025]
        """
        return self.query("""
            SELECT year, product_id,
                   COUNT(*)                             AS volume,
                   ROUND(AVG(gross_revenue_gbp), 4)     AS price,
                   ROUND(SUM(gross_revenue_gbp), 2)     AS revenue_gbp
            FROM (SELECT CAST(strftime('%Y', date) AS INTEGER) AS year, *
                  FROM fct_transactions)
            WHERE year IN (?, ?)
            GROUP BY year, product_id
            ORDER BY year, product_id
        """, (year_from, year_to))

    def stockout_cost(self) -> pd.DataFrame:
        """What running out of euro notes in August costs, by month.

        A branch that runs out of currency stops selling it. Sales on those
        days are a *floor* on demand, not a measurement of it — the technical
        name is right-censoring, and it makes August's demand look smaller
        than it was, which makes August's elasticity look smaller than it is.

        The commercial point is blunter. Look at `stockout_days` against
        `avg_contribution_per_open_day`: the lost contribution on a refused
        day is real money, and the fix is a stock-ordering decision in an
        operations budget, not a price. Some of the most valuable work a
        pricing manager does is proving that the problem is not pricing.

        Notebook 10 recovers the uncensored demand curve properly.
        """
        return self.query("""
            SELECT strftime('%Y-%m', s.date)                       AS year_month,
                   COUNT(*)                                        AS branch_product_days,
                   SUM(s.stockout_flag)                            AS stockout_days,
                   ROUND(100.0 * SUM(s.stockout_flag) / COUNT(*), 2) AS stockout_rate_pct,
                   ROUND(AVG(s.value_sold_gbp), 2)                 AS avg_value_sold_gbp,
                   ROUND(AVG(s.stock_limit_gbp), 2)                AS avg_stock_limit_gbp
            FROM fct_stock s
            GROUP BY year_month
            ORDER BY stockout_rate_pct DESC
            LIMIT 12
        """)

    def retention_by_price(self, buckets: int = 5) -> pd.DataFrame:
        """Do customers charged above the market come back less? (Yes.)

        Buckets customers by the average margin they paid above the best
        market rate, and shows the retention multiplier that went with it.

        This is the empirical version of the argument in
        `pricing_finance.lifetime_value_of_a_price_move`: pricing above the
        market is not free even when the customer buys today. Every point
        above the market costs about 12% of next year's trips.

        Treat the pattern as suggestive, not proven. Customers were not
        randomly assigned to price buckets — the ones who paid most above the
        market are disproportionately last-minute airport buyers, who behave
        differently for reasons that have nothing to do with price. Notebook
        01 does the like-for-like comparison properly, by normalising each
        customer against their own travel rate. Getting from "these two
        columns move together" to "the price caused it" is the job.
        """
        # NTILE is a window function, so it has to be computed in a subquery
        # before you are allowed to GROUP BY the bucket it produces.
        return self.query(f"""
            SELECT price_bucket,
                   COUNT(*)                                  AS customers,
                   ROUND(MIN(margin_above_market), 3)        AS min_above_market_pp,
                   ROUND(AVG(margin_above_market), 3)        AS avg_above_market_pp,
                   ROUND(MAX(margin_above_market), 3)        AS max_above_market_pp,
                   ROUND(AVG(orders), 2)                     AS avg_orders,
                   ROUND(AVG(refused), 4)                    AS share_refused_for_stock,
                   ROUND(AVG(retention_multiplier), 4)       AS retention_multiplier
            FROM (SELECT *,
                         NTILE({int(buckets)}) OVER (ORDER BY margin_above_market) AS price_bucket
                  FROM fct_customer_year)
            GROUP BY price_bucket
            ORDER BY price_bucket
        """)

    def _slice(self, group_by: str) -> str:
        """Resolve a slice name to SQL, over `fct_transactions t` + `dim_sites s`.

        Only names in `SLICEABLE` are allowed. This is not paranoia about
        malicious input — it is a working assistant catching the typo before
        it becomes a chart. `db.pnl("chanel")` should fail loudly at the
        prompt, not quietly return one row.
        """
        if group_by not in SLICEABLE:
            raise ValueError(
                f"cannot slice by {group_by!r}. "
                f"Try one of: {', '.join(sorted(SLICEABLE))}")
        return SLICEABLE[group_by]

    def _safe_column(self, table: str, column: str) -> str:
        """Reject a column that is not on the table — a typo should not become SQL."""
        present = {row[1] for row in self.conn.execute(f"PRAGMA table_info({table})")}
        if column not in present:
            raise ValueError(f"{table} has no column {column!r}. "
                             f"Available: {', '.join(sorted(present))}")
        return f'"{column}"'

    # ------------------------------------------------------------------

    def close(self) -> None:
        self.conn.close()

    def __enter__(self) -> "MeridianDB":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()


def _tour() -> None:
    """python db_helper.py — every worked view, run against the real database."""
    pd.set_option("display.width", 150, "display.max_columns", 30)
    with MeridianDB() as db:
        for title, frame in [
            ("THE P&L BY CHANNEL — note turnover is not revenue", db.pnl()),
            ("UNIT ECONOMICS — what one order earns, cost line by cost line", db.unit_economics()),
            ("DISCOUNT HURDLES — what a 10% rate cut must deliver", db.discount_hurdles()),
            ("PRICE WATERFALL — a branch order, board rate to pocket", db.price_waterfall("branch")),
            ("MARGIN BY SEGMENT — conversion measured on quotes, not sales",
             db.margin_by_segment().head(8)),
            ("STOCKOUTS — the months when sales stopped measuring demand",
             db.stockout_cost().head(6)),
            ("RETENTION vs PRICE — pricing above the market is not free",
             db.retention_by_price()),
        ]:
            print(f"\n{'=' * 78}\n{title}\n{'=' * 78}")
            print(frame.to_string(index=False))


if __name__ == "__main__":
    _tour()
