"""Shared plumbing for the Pricing Fundamentals course.

Deliberately tiny. It does three boring things so the notebooks can spend
their code cells on pricing instead of housekeeping:

1. finds the `data/` folder (built by notebook 01) no matter where the
   notebook was started from,
2. loads the tables with the right dtypes (dates parsed, ids as strings),
3. sets one consistent, colour-blind-safe chart style.

Nothing in here contains pricing logic. If a number matters to a lesson, it
is computed in the notebook where you can see it.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------
# 1. Where is the data?
# --------------------------------------------------------------------------


def data_dir() -> Path:
    """Return the course `data/` folder, searching upwards from the cwd."""
    here = Path.cwd().resolve()
    for folder in [here, *here.parents]:
        candidate = folder / "data"
        if (candidate / "fct_quotes.csv").exists():
            return candidate
        if folder.name == "pricing_fundamentals":
            return folder / "data"
    return here / "data"


DATE_COLS = {"date", "week", "month", "opened_date", "start_date", "end_date", "first_seen"}
ID_COLS = {"site_id", "product_id", "customer_id", "quote_id", "promo_id"}


def load(name: str) -> pd.DataFrame:
    """Load one table by name, e.g. load('fct_quotes')."""
    path = data_dir() / f"{name}.csv"
    if not path.exists():
        raise FileNotFoundError(
            f"Could not find {path}.\n"
            "Run 01_data_foundation.ipynb top to bottom first — it builds every table "
            "this course uses (the CSVs are not committed to git on purpose)."
        )
    df = pd.read_csv(path, low_memory=False)
    for col in df.columns:
        if col in DATE_COLS:
            df[col] = pd.to_datetime(df[col])
        elif col in ID_COLS:
            df[col] = df[col].astype("string")
    if "arm" in df.columns:            # empty outside the experiment window
        df["arm"] = df["arm"].fillna("").astype(str)
    return df


def load_all(*names: str) -> tuple[pd.DataFrame, ...]:
    """Load several tables at once: quotes, daily = load_all('fct_quotes', 'fct_daily')."""
    return tuple(load(n) for n in names)


def truth() -> dict:
    """The answer key written by notebook 01 — the parameters that generated the world."""
    path = data_dir() / "truth.json"
    if not path.exists():
        raise FileNotFoundError(f"Could not find {path}. Run 01_data_foundation.ipynb first.")
    return json.loads(path.read_text())


def zone_week_panel(quotes: pd.DataFrame, min_quotes: int = 10) -> pd.DataFrame:
    """Aggregate quotes to pricing zone x week x product.

    This is the grain the *price is actually set at*: one rate board per zone
    (a region for branches, the site for airports, one nationally for online).
    Analysing at a finer grain adds measurement error to the price — the daily
    average margin at one small site reflects which customers happened to walk
    in — and measurement error in a regressor drags its coefficient toward
    zero. Aggregating to the decision grain removes that.
    """
    df = quotes.copy()
    df["zone"] = np.where(df["channel"] == "branch", df["region_id"], df["site_id"])
    df["week"] = df["date"].dt.to_period("W").dt.start_time
    panel = (df.groupby(["zone", "channel", "week", "product_id"])
             .agg(quotes=("quote_id", "count"), orders=("converted", "sum"),
                  margin=("our_margin_pp", "mean"), quoted_margin=("quoted_margin_pp", "mean"),
                  comp=("comp_best_margin_pp", "mean"), season=("season_z", "mean"),
                  funding=("funding_cost_bp", "mean"), promo=("promo_flag", "max"),
                  trial=("trial_flag", "max"), order_value=("order_value_gbp", "mean"))
             .reset_index())
    panel = panel[(panel["quotes"] >= min_quotes) & (panel["orders"] > 0)].copy()
    panel["conversion"] = panel["orders"] / panel["quotes"]
    panel["log_conversion"] = np.log(panel["conversion"])
    return panel


def tables() -> pd.DataFrame:
    """List the tables available, with row counts and size on disk."""
    rows = []
    for path in sorted(data_dir().glob("*.csv")):
        with path.open() as fh:
            n = sum(1 for _ in fh) - 1
        rows.append({"table": path.stem, "rows": n, "MB": round(path.stat().st_size / 1e6, 2)})
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------
# 2. One chart style for the whole course
# --------------------------------------------------------------------------

# Colour-blind-safe, fixed order. Use C[0] for "us", C[5] for warnings.
C = ["#2a78d6", "#1baf7a", "#eda100", "#008300", "#4a3aa7", "#e34948"]
INK, SUB, MUT, GRID, AXIS = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"


def style() -> None:
    """Apply the course chart style. Call once near the top of a notebook."""
    import matplotlib.pyplot as plt

    plt.rcParams.update({
        "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb",
        "axes.edgecolor": AXIS, "axes.labelcolor": SUB, "axes.titlecolor": INK,
        "xtick.color": MUT, "ytick.color": MUT,
        "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.prop_cycle": plt.cycler(color=C),
        "lines.linewidth": 2, "font.size": 10.5, "axes.titlesize": 12,
        "figure.figsize": (8, 4.0), "figure.dpi": 100, "legend.frameon": False,
        "savefig.bbox": "tight",
    })


def tidy(ax) -> None:
    """Drop the vertical gridlines — they rarely help."""
    ax.grid(axis="x", visible=False)


# --------------------------------------------------------------------------
# 3. Formatting helpers (for tables you show to a commercial audience)
# --------------------------------------------------------------------------


def money(x: float, dp: int = 0) -> str:
    """£1,234 — the format every commercial slide uses."""
    return f"£{x:,.{dp}f}"


def pct(x: float, dp: int = 1) -> str:
    """0.0734 -> '7.3%'."""
    return f"{100 * x:.{dp}f}%"


def pp(x: float, dp: int = 2) -> str:
    """Percentage points / margin points — the unit a pricing desk speaks in."""
    return f"{x:+.{dp}f}pp"
