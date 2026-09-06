# The Meridian FX database

`data/meridian.db` is the whole business in one SQLite file: 19 tables,
157 MB, indexed. It is not committed to git — build it yourself.

```bash
jupyter lab 01_data_foundation.ipynb    # run top to bottom — writes the CSVs
python create_database.py               # CSVs -> meridian.db, ~30 seconds
python db_helper.py                     # every worked view, printed
```

The CSVs are what the notebooks read. The database is for the *other* half of
the job: someone asks a question in a meeting and the answer is one query
away, or you want to practise the SQL a pricing role actually expects.

---

## Reading a star schema

This is the layout every commercial data warehouse uses, and being able to
read one is most of what "technical enough" means in a pricing job.

- A **fact** (`fct_*`) is one row per **event**, and what it measures is
  additive: quotes, orders, turnover, contribution. **You SUM facts.**
- A **dimension** (`dim_*`) is one row per **thing** — a site, a product, a
  customer — holding the attributes you slice by: channel, region, segment,
  age band. **You GROUP BY dimensions.**

Every analysis is then the same sentence: *sum a fact, grouped by a dimension,
filtered by a date.*

```sql
SELECT s.channel, ROUND(SUM(t.contribution_gbp)) AS contribution
FROM fct_transactions t
JOIN dim_sites s ON t.site_id = s.site_id
WHERE t.date BETWEEN '2025-08-01' AND '2025-08-31'
GROUP BY s.channel;
```

### Grain is the thing to get right

"Grain" means what one row **is**. Get it wrong and you double-count without
noticing, which is the most common way a pricing paper gets embarrassed in
front of a committee.

| Table | Rows | One row is |
|---|---|---|
| `fct_quotes` | 220,945 | one shopping occasion — **includes the people who walked away** |
| `fct_transactions` | 124,678 | one completed order, with the full revenue and cost breakdown |
| `fct_customer_year` | 32,259 | one customer-year: margin paid above market, and the retention it cost |
| `dim_customers` | 14,000 | one customer |
| `fct_price_board` | 13,158 | one day × site × product — **the grain price is SET at** |
| `fct_daily` | 13,052 | one day × site × product — where commercial reporting lives |
| `fct_stock` | 7,299 | one branch-day × cash product — the limit that censors August |
| `fct_competitor_prices` | 6,579 | one day × competitor × market × product |
| `fct_fx_rates` | 2,193 | one day × product: the wholesale mid-market rate |
| `fct_region_week` | 1,896 | one region × week, all channels — the geo-experiment panel |
| `fct_calendar` | 731 | one day: seasonality, school holidays, funding cost |
| `truth` | 104 | the answer key, flattened from `truth.json` |
| `fct_marketing` | 41 | one month × region: spend (a confounder for regional analysis) |
| `dim_regions` | 12 | one region — the unit a geo experiment randomises |
| `dim_sites` | 6 | one selling location; `channel` and `is_airport` decide which board applies |
| `dim_cost_stack` | 6 | one cost line, and whether it is variable or fixed |
| `dim_segments` | 4 | one segment (**price sensitivities are NOT here — you estimate those**) |
| `dim_products` | 3 | one product, with the per-order costs driving unit economics |
| `fct_promotions` / `fct_experiment` | 1 / 1 | design metadata |

Do not take these counts on trust — `01_data_foundation.ipynb` regenerates the
world, and a regenerated world has different row counts. `db.overview()`
prints the live figures, and it is the habit worth having: check the grain
against the database, not against a document.

**`fct_quotes` includes the customers who left; `fct_transactions` does not.**
Conversion lives in the gap. Any elasticity estimated only on transactions is
estimating the wrong thing — it cannot see the customers the price drove off,
which is the entire effect you were trying to measure.

---

## The Python helper

```python
from db_helper import MeridianDB

with MeridianDB() as db:
    df = db.query("SELECT * FROM fct_daily WHERE date >= '2025-06-01'")
```

### Plumbing

| Method | Does |
|---|---|
| `query(sql, params)` | SQL in, DataFrame out, **dates parsed to real timestamps** |
| `tables()` / `overview()` | what exists, and how big |
| `schema(table)` / `sample(table)` | columns and types; a few rows to see the grain |
| `truth(like)` | search the answer key: `db.truth('elasticity')` |
| `daily()` / `quotes()` / `transactions()` | facts joined to their dimensions |

`query` parses dates because SQLite has no date type. Left alone that is a
silent bug: `df["date"].dt.month` explodes, and worse, `df["date"] > "2025-2"`
compares *strings* and quietly returns nonsense.

### Worked views — one question each

| Method | Question it answers |
|---|---|
| `pnl()` | turnover → revenue → variable cost → contribution, by any slice |
| `unit_economics()` | what one order earns, cost line by cost line |
| `discount_hurdles()` | how much extra volume a discount must produce |
| `price_waterfall()` | board rate down to pocket margin, on real orders |
| `revenue_bridge()` | year-on-year revenue split into volume, mix and price |
| `margin_by_segment()` | conversion and margin by segment, measured **on quotes** |
| `stockout_cost()` | the months when sales stopped measuring demand |
| `retention_by_price()` | do customers charged above market come back less? |

**Read the SQL in these methods** — it is the point, not an implementation
detail. Each docstring says what the answer means and how it is normally
misread.

`revenue_bridge` pairs with `pricing_finance.price_volume_mix`:

```python
from pricing_finance import price_volume_mix

bridge = db.revenue_bridge(2023, 2024)
print(price_volume_mix(bridge[bridge.year == 2023][["product_id", "price", "volume"]],
                       bridge[bridge.year == 2024][["product_id", "price", "volume"]]))
```

### Nothing here is causal

Every method is **description**: what happened, sliced sensibly. Turning
description into a causal claim — "the price cut caused the volume" — is what
notebooks 06 and 07 are for. Skipping that step is the single most expensive
mistake in the discipline, and the data is built to punish it: `db.margin_by_segment()`
shows bargain hunters converting worst on the keenest rates, which reads as a
*positive* price elasticity if you take it at face value.

---

## Queries worth having

**Are we above or below the market, and where?**

```sql
SELECT s.site_name, b.product_id,
       ROUND(AVG(b.our_margin_pp), 3)                            AS ours,
       ROUND(AVG(b.comp_best_margin_pp), 3)                      AS best_competitor,
       ROUND(AVG(b.our_margin_pp - b.comp_best_margin_pp), 3)    AS gap_pp
FROM fct_price_board b
JOIN dim_sites s ON b.site_id = s.site_id
WHERE b.date >= '2025-06-01'
GROUP BY s.site_name, b.product_id
ORDER BY gap_pp DESC;
```

Positive gap = dearer than the market. Notebook 08 costs that gap in retention.

**Conversion against price, at the grain price is set at**

```sql
SELECT ROUND(q.our_margin_pp, 1)                      AS margin_pp,
       COUNT(*)                                       AS quotes,
       ROUND(1.0 * SUM(q.converted) / COUNT(*), 4)    AS conversion
FROM fct_quotes q
JOIN dim_sites s ON q.site_id = s.site_id
WHERE s.channel = 'branch' AND s.is_airport = 0
GROUP BY ROUND(q.our_margin_pp, 1)
HAVING quotes > 500
ORDER BY margin_pp;
```

The slope comes out at about **−7.7% per margin point**. The true figure for
the branch network — `db.truth('by_site')` — is between **−26% and −28%**.
**That is the lesson, not a bug** — the board went up in August when demand was
strongest, so the price rises are sitting on top of the demand peaks and
cancelling themselves out. A naive read understates the real price response by
a factor of three and a half, and would have you believe a rate rise is nearly
free.

**The experiment, which is the one clean comparison in the data**

```sql
SELECT arm, COUNT(*) AS quotes,
       ROUND(1.0 * SUM(converted) / COUNT(*), 4)     AS conversion,
       ROUND(AVG(quoted_margin_pp), 3)               AS margin_pp
FROM fct_quotes
WHERE arm IS NOT NULL
GROUP BY arm;
```

Randomised, so the difference *is* the effect: +0.41pp of margin costs 9.6
points of conversion — 60.0% down to 50.5% — which is roughly **−39% per pp**
on 4,624 quotes.

It is noisy. The true online figure is **−28.7%**, and the 95% interval on this
estimate runs from −27% to −51%: the truth is inside it, near the bottom. But
compare that with the observational query above, whose −7.7% is not in the
interval and never could be. **One clean comparison on four thousand quotes
beats two hundred thousand dirty ones** — and the honest way to report it is
"−39%, and I would plan on 30", not "−39%".

**Where the stock ran out**

```sql
SELECT strftime('%Y-%m', date)                          AS year_month,
       SUM(stockout_flag)                               AS stockout_days,
       ROUND(100.0 * SUM(stockout_flag) / COUNT(*), 2)  AS rate_pct
FROM fct_stock
GROUP BY year_month
ORDER BY rate_pct DESC
LIMIT 6;
```

August 2025 peaks near 9%. On those days sales are a **floor** on demand, not
a measurement of it.

---

## Practical notes

- **Rebuilding is safe and cheap.** `create_database.py` drops and recreates
  the file every run, so nothing you do to the database is precious. If you
  want to keep a derived table, write it somewhere else.
- **Filter in SQL, not in pandas.** `db.quotes()` caps at 50,000 rows on
  purpose. Pulling a fifth of a million rows into memory to then group them is
  a habit worth not forming; the indexes exist so you do not have to.
- **29 indexes** cover `date`, `site_id`, `product_id`, `customer_id` and
  `region_id` on the tables where they matter. `create_database.py` prints how
  many it built and how many it skipped because the column is not on that
  table — a skip is information, not an error.
- **The `truth` table is flattened and searchable**
  (`SELECT * FROM truth WHERE parameter LIKE '%elasticity%'`). Look at it
  *after* you have committed to an estimate. Checking first feels efficient
  and teaches you nothing.

## See also

- **[`FINANCE_FOR_PRICING.md`](FINANCE_FOR_PRICING.md)** — the financial
  concepts behind every one of these queries
- **[`pricing_finance.py`](pricing_finance.py)** — those concepts as runnable,
  doctested code
- `data/DATA_DICTIONARY.md` — every table and column, written by notebook 01
- `data/truth.json` — the answer key in its original nested form
