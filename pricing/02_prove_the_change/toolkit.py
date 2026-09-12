"""Shim so `from toolkit import ...` works from this folder.

The real module is `engine/pricing_toolkit.py`. Every runnable lesson in this
folder imports it through here, which keeps one copy of the plumbing while
letting the notebooks sit beside the prose they belong to.
"""
import sys
from pathlib import Path

_ENGINE = Path(__file__).resolve().parents[1] / "engine"
if str(_ENGINE) not in sys.path:
    sys.path.insert(0, str(_ENGINE))

from pricing_toolkit import *          # noqa: F401,F403
from pricing_toolkit import C, INK, SUB, MUT, GRID, AXIS   # noqa: F401
