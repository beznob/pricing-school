"""Build `data/meridian.db` — the whole Meridian FX business in one SQLite file.

Run `../02_prove_the_change/lab_01_data_foundation.ipynb` first (it writes the CSVs), then:

    python create_database.py

The CSVs are what the notebooks read. This database is for the *other* half of
the job — the half where somebody asks you a question in a meeting and the
answer is one query away, or where you want to practise the SQL a pricing
manager is actually expected to write.

    sqlite3 data/meridian.db "SELECT channel, SUM(contribution_gbp) FROM
                              fct_transactions GROUP BY channel"

Nothing is lost by using it: same rows, same columns, plus indexes and a
`truth` table holding the answer key.

WHY THE TABLES ARE SHAPED THIS WAY
----------------------------------
This is a **star schema**, the layout every commercial data warehouse uses,
and knowing how to read one is most of what "being technical enough" means in
a pricing role.

  * A **fact** table (`fct_*`) is one row per *event*, and the things it
    measures are additive: quotes, orders, turnover, contribution. You SUM
    facts.
  * A **dimension** table (`dim_*`) is one row per *thing* — a site, a
    product, a customer — and holds the attributes you slice by: channel,
    region, segment, age band. You GROUP BY dimensions.

Every analysis is then the same sentence: sum a fact, grouped by a dimension,
filtered by a date. "Contribution by channel last August" is
`SUM(contribution_gbp)` from a fact, `GROUP BY channel` from a dimension,
`WHERE date` from the calendar.

THE GRAIN IS THE THING TO GET RIGHT
-----------------------------------
"Grain" means what one row *is*. Get it wrong and you will double-count and
not notice, which is the most common way a pricing paper gets embarrassed in
front of a committee.

    fct_quotes         one shopping occasion    (someone asked our rate)
    fct_transactions   one completed order      (they bought)
    fct_daily          one day x site x product (the management-reporting grain)
    fct_region_week    one region x week        (the geo-experiment grain)
    fct_price_board    one day x zone x product (the grain price is SET at)

`fct_quotes` includes people who walked away; `fct_transactions` does not.
Conversion lives in the gap between them, and any elasticity estimated only
on transactions is estimating the wrong thing — it cannot see the customers
the price drove off, which is the entire effect you were trying to measure.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DB_PATH = DATA_DIR / "meridian.db"

# Every table lab 2.1 writes, with the grain and why a pricing manager
# would open it. Keep this list in step with the `tables` dict in lab 2.1.
TABLES: dict[str, str] = {
    # -- dimensions: what you group by -------------------------------------
    "dim_regions":           "one region — the unit a geo experiment randomises",
    "dim_sites":             "one selling location; price_zone says which rate board applies",
    "dim_products":          "one product, with the per-order costs that drive unit economics",
    "dim_segments":          "one customer segment (price sensitivities are NOT here — you estimate those)",
    "dim_customers":         "one customer: region, segment, age band, tenure, loyalty",
    "dim_cost_stack":        "one cost line, and whether it is variable or fixed",
    # -- facts: what you sum ------------------------------------------------
    "fct_calendar":          "one day: seasonality, school holidays, and the wholesale funding cost",
    "fct_marketing":         "one month x region: spend — a demand shifter and a confounder",
    "fct_fx_rates":          "one day x product: the wholesale mid-market rate",
    "fct_competitor_prices": "one day x competitor x zone x product: their published margin",
    "fct_price_board":       "one day x zone x product: THE GRAIN PRICE IS SET AT",
    "fct_quotes":            "one shopping occasion — the finest grain, and it includes the people who left",
    "fct_transactions":      "one completed order, with the full revenue and cost breakdown",
    "fct_daily":             "one day x site x product — where most commercial reporting lives",
    "fct_region_week":       "one region x week, all channels — immune to channel switching",
    "fct_stock":             "one branch-day x cash product: the limit that censors August demand",
    "fct_promotions":        "one promotion or trial: who, what, when, how deep",
    "fct_experiment":        "one experiment: design, dates, arms, allocation",
    "fct_customer_year":     "one customer: margin paid above the market, and the retention it cost",
}

# Columns worth indexing: the ones you filter and join on constantly. Any
# entry naming a column the table does not have is skipped with a warning
# rather than killing the build.
INDEX_COLUMNS: dict[str, list[str]] = {
    "fct_quotes":            ["date", "site_id", "customer_id", "product_id", "region_id"],
    "fct_transactions":      ["date", "site_id", "customer_id", "product_id", "region_id"],
    "fct_daily":             ["date", "site_id", "product_id", "channel"],
    "fct_price_board":       ["date", "zone", "product_id"],
    "fct_region_week":       ["region_id", "week"],
    "fct_stock":             ["date", "site_id", "product_id"],
    "fct_competitor_prices": ["date", "zone", "product_id"],
    "fct_calendar":          ["date"],
    "fct_marketing":         ["month", "region_id"],
    "dim_customers":         ["customer_id", "segment", "region_id"],
    "dim_sites":             ["site_id", "channel", "region_id", "price_zone"],
    "dim_products":          ["product_id"],
    "fct_customer_year":     ["customer_id"],
}


def _flatten(prefix: str, node, out: list[dict]) -> None:
    """Walk nested truth.json into (key, value) rows so it can live in a table."""
    if isinstance(node, dict):
        for key, value in node.items():
            _flatten(f"{prefix}.{key}" if prefix else key, value, out)
    else:
        out.append({"parameter": prefix, "value": str(node),
                    "is_number": isinstance(node, (int, float)) and not isinstance(node, bool)})


def load_truth(conn: sqlite3.Connection, data_dir: Path) -> int:
    """Put the answer key in a `truth` table.

    `truth.json` is nested — `semi_elasticity_pct_per_pp.by_segment.bargain_hunter`
    and so on — so it is flattened to one row per dotted parameter name. That
    makes it searchable, which is the point:

        SELECT * FROM truth WHERE parameter LIKE '%elasticity%';

    Look at it *after* you have estimated something, never before. The whole
    design of this course is that you commit to a number first; checking the
    key first turns a lesson into a lookup.
    """
    path = data_dir / "truth.json"
    if not path.exists():
        print(f"  ! no truth.json at {path} — skipping the answer key")
        return 0
    rows: list[dict] = []
    _flatten("", json.loads(path.read_text()), rows)
    pd.DataFrame(rows).to_sql("truth", conn, if_exists="replace", index=False)
    return len(rows)


def build(data_dir: Path = DATA_DIR, db_path: Path = DB_PATH) -> Path:
    """Load every CSV into SQLite, index it, and attach the answer key."""
    if not data_dir.exists() or not (data_dir / "fct_quotes.csv").exists():
        raise SystemExit(
            f"No data found in {data_dir}.\n"
            "Run ../02_prove_the_change/lab_01_data_foundation.ipynb top to bottom first — it builds every table.\n"
            "The CSVs are deliberately not committed to git, so the notebook is the "
            "source of truth and anyone can rebuild the world from scratch."
        )

    db_path.parent.mkdir(parents=True, exist_ok=True)
    db_path.unlink(missing_ok=True)          # a clean rebuild every time
    conn = sqlite3.connect(str(db_path))

    print(f"Building {db_path.name} from {data_dir}\n")
    loaded, missing = 0, []
    for table, grain in TABLES.items():
        csv_path = data_dir / f"{table}.csv"
        if not csv_path.exists():
            missing.append(table)
            continue
        frame = pd.read_csv(csv_path, low_memory=False)
        # SQLite has no date type. Storing ISO 8601 text means date comparison
        # and ordering still work in SQL, and db_helper parses it back to real
        # timestamps on the way out.
        for column in frame.columns:
            # `dtype == object` was the old test for "is this text?" and stopped
            # being true in pandas 3, where strings have their own dtype. Test
            # for what it is not: `fct_calendar.month` is a real integer while
            # `fct_marketing.month` is a date, so the name cannot decide it.
            is_text = not (pd.api.types.is_numeric_dtype(frame[column])
                           or pd.api.types.is_datetime64_any_dtype(frame[column]))
            if column in {"date", "week", "month", "start_date", "end_date"} and is_text:
                parsed = pd.to_datetime(frame[column], errors="coerce")
                if parsed.notna().all():
                    frame[column] = parsed.dt.strftime("%Y-%m-%d")
        frame.to_sql(table, conn, if_exists="replace", index=False)
        loaded += 1
        print(f"  {table:24s} {len(frame):>8,} rows   {grain}")

    if missing:
        print(f"\n  ! not found (re-run lab 2.1?): {', '.join(missing)}")

    # Indexes: the difference between a query that answers in a meeting and
    # one that answers after it. Only build the ones whose column exists.
    print()
    built, skipped = 0, 0
    for table, columns in INDEX_COLUMNS.items():
        if table in missing:
            continue
        present = {row[1] for row in conn.execute(f"PRAGMA table_info({table})")}
        for column in columns:
            if column not in present:
                skipped += 1
                continue
            conn.execute(f'CREATE INDEX "idx_{table}_{column}" ON "{table}" ("{column}")')
            built += 1
    print(f"  {built} indexes built" + (f", {skipped} skipped (column not in table)" if skipped else ""))

    n_truth = load_truth(conn, data_dir)
    if n_truth:
        print(f"  truth                    {n_truth:>8,} parameters  the answer key — look AFTER you estimate")

    conn.commit()
    conn.close()

    size_mb = db_path.stat().st_size / 1e6
    print(f"\nDone: {loaded} tables, {size_mb:.1f} MB at {db_path}\n")
    print("Try it:")
    print("  python -c \"from db_helper import MeridianDB; print(MeridianDB().pnl())\"")
    print(f"  sqlite3 {db_path} \"SELECT channel, ROUND(SUM(contribution_gbp)) "
          "FROM fct_transactions GROUP BY channel\"")
    return db_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--data-dir", type=Path, default=DATA_DIR,
                        help="folder holding the CSVs written by lab 2.1")
    parser.add_argument("--db", type=Path, default=DB_PATH, help="database file to write")
    args = parser.parse_args()
    build(args.data_dir, args.db)


if __name__ == "__main__":
    sys.exit(main())
