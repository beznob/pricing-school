"""Shared chart style + import path for the FRES prep notebooks.

Palette: validated reference categorical order (fixed slots, never cycled),
recessive grid/axes, thin marks. Also puts ../engine on
sys.path so notebooks can reuse the case-study engine directly.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib as mpl

_FTS = (Path(__file__).parent / ".." / "engine").resolve()
if str(_FTS) not in sys.path:
    sys.path.insert(0, str(_FTS))

# Categorical slots — fixed order (identity), never cycled past 8.
SERIES = ["#2a78d6", "#1baf7a", "#eda100", "#008300",
          "#4a3aa7", "#e34948", "#e87ba4", "#eb6834"]

C = {
    "blue": "#2a78d6", "aqua": "#1baf7a", "yellow": "#eda100",
    "green": "#008300", "violet": "#4a3aa7", "red": "#e34948",
    "magenta": "#e87ba4", "orange": "#eb6834",
    # chrome & ink
    "ink": "#0b0b0b", "ink2": "#52514e", "muted": "#898781",
    "grid": "#e1e0d9", "axis": "#c3c2b7", "surface": "#fcfcfb",
    # status (reserved; never used as a series)
    "good": "#0ca30c", "warning": "#fab219",
    "serious": "#ec835a", "critical": "#d03b3b",
    # sequential blue ramp (light -> dark)
    "seq": ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"],
}


def apply_style() -> None:
    mpl.rcParams.update({
        "figure.facecolor": C["surface"], "axes.facecolor": C["surface"],
        "figure.figsize": (9.0, 4.4), "figure.dpi": 110,
        "font.family": "sans-serif", "font.size": 10,
        "text.color": C["ink"], "axes.labelcolor": C["ink2"],
        "axes.edgecolor": C["axis"], "axes.linewidth": 0.8,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.color": C["grid"], "grid.linewidth": 0.6,
        "axes.axisbelow": True,
        "xtick.color": C["muted"], "ytick.color": C["muted"],
        "xtick.labelsize": 9, "ytick.labelsize": 9,
        "axes.titlesize": 11, "axes.titleweight": "bold",
        "axes.titlecolor": C["ink"], "axes.titlelocation": "left",
        "legend.frameon": False, "legend.fontsize": 9,
        "lines.linewidth": 2.0, "lines.markersize": 6,
    })


def annotate_bars(ax, bars, fmt="{:,.0f}", dy=0.5, color=None) -> None:
    """Selective direct labels on bar ends (text wears ink, not series color)."""
    for b in bars:
        ax.annotate(fmt.format(b.get_height()),
                    (b.get_x() + b.get_width() / 2, b.get_height()),
                    textcoords="offset points", xytext=(0, dy + 2),
                    ha="center", va="bottom", fontsize=8.5,
                    color=color or C["ink2"])
