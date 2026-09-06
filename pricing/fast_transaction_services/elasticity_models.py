"""
Price-elasticity estimators for the fast-transaction-service case study.

The point of this module is to show *why naive elasticity estimates are
dangerous* and how causal identification fixes them.

Estimators provided
--------------------
* ``point_elasticity`` / ``arc_elasticity`` -- textbook two-point formulas.
* ``naive_ols_elasticity``  -- log-log OLS of volume on fee. **Biased** here,
  because the firm surges the fee with unobserved demand (endogeneity).
* ``iv_2sls_elasticity``    -- two-stage least squares using the per-transaction
  cost shock as an instrument for the fee. **Consistent** for the structural
  elasticity.
* ``segmented_elasticity``  -- run OLS + IV per customer segment and compare
  against the simulator's ground truth.

Everything is plain numpy/pandas; no heavyweight econometrics dependency.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np
import pandas as pd


# --------------------------------------------------------------------------- #
# Two-point ("school book") elasticities
# --------------------------------------------------------------------------- #
def point_elasticity(q0: float, q1: float, p0: float, p1: float) -> float:
    """Point elasticity using the base point (p0, q0): (dQ/Q) / (dP/P)."""
    return ((q1 - q0) / q0) / ((p1 - p0) / p0)


def arc_elasticity(q0: float, q1: float, p0: float, p1: float) -> float:
    """Midpoint (arc) elasticity -- symmetric to the direction of the change."""
    return ((q1 - q0) / ((q1 + q0) / 2)) / ((p1 - p0) / ((p1 + p0) / 2))


# --------------------------------------------------------------------------- #
# Linear-algebra helpers (OLS + 2SLS with standard errors)
# --------------------------------------------------------------------------- #
@dataclass
class RegResult:
    coef: np.ndarray
    se: np.ndarray
    names: list[str]
    n: int

    def get(self, name: str) -> tuple[float, float]:
        i = self.names.index(name)
        return float(self.coef[i]), float(self.se[i])


def _ols(y: np.ndarray, X: np.ndarray, names: Sequence[str]) -> RegResult:
    """OLS with homoskedastic standard errors."""
    XtX_inv = np.linalg.inv(X.T @ X)
    beta = XtX_inv @ X.T @ y
    resid = y - X @ beta
    dof = max(X.shape[0] - X.shape[1], 1)
    sigma2 = (resid @ resid) / dof
    cov = sigma2 * XtX_inv
    return RegResult(beta, np.sqrt(np.diag(cov)), list(names), X.shape[0])


def _tsls(
    y: np.ndarray, X: np.ndarray, Z: np.ndarray, names: Sequence[str]
) -> RegResult:
    """Two-stage least squares.

    ``X`` are the regressors (including exogenous controls + the endogenous fee
    term and a constant). ``Z`` are the instruments (the same exogenous controls
    + the excluded instrument(s), e.g. the cost shock). Returns point estimates
    and homoskedastic 2SLS standard errors via the projection form.
    """
    ZtZ_inv = np.linalg.inv(Z.T @ Z)
    Pz_X = Z @ (ZtZ_inv @ (Z.T @ X))            # project regressors onto instruments
    A_inv = np.linalg.inv(Pz_X.T @ X)
    beta = A_inv @ (Pz_X.T @ y)
    resid = y - X @ beta                          # residuals use *actual* X
    dof = max(X.shape[0] - X.shape[1], 1)
    sigma2 = (resid @ resid) / dof
    cov = sigma2 * np.linalg.inv(Pz_X.T @ Pz_X)
    return RegResult(beta, np.sqrt(np.diag(cov)), list(names), X.shape[0])


def _design(df: pd.DataFrame, cols: Sequence[str]) -> np.ndarray:
    """Stack a constant with the requested columns into a design matrix."""
    const = np.ones((len(df), 1))
    if cols:
        return np.hstack([const, df[list(cols)].to_numpy(dtype=float)])
    return const


# --------------------------------------------------------------------------- #
# Elasticity estimators
# --------------------------------------------------------------------------- #
def naive_ols_elasticity(
    df: pd.DataFrame, controls: Sequence[str] = ("season",)
) -> dict:
    """Log-log OLS: regress log(volume) on log(fee) [+ observed controls].

    This is what a team gets if they regress demand on price using observational
    data. It is biased here because ``log_fee`` is correlated with the
    *unobserved* demand shock that the firm surges on.
    """
    y = df["log_volume"].to_numpy(dtype=float)
    names = ["const", "log_fee", *controls]
    X = _design(df, ["log_fee", *controls])
    res = _ols(y, X, names)
    coef, se = res.get("log_fee")
    return {"method": "OLS (log-log)", "elasticity": coef, "se": se, "n": res.n}


def first_stage_strength(
    df: pd.DataFrame, instrument: str = "cost_shock_z", controls: Sequence[str] = ("season",)
) -> dict:
    """Relevance check: regress the endogenous log(fee) on the instrument(s).

    Reports the instrument coefficient and the first-stage F-statistic (a rule of
    thumb is F > 10 for a 'strong' instrument).
    """
    y = df["log_fee"].to_numpy(dtype=float)
    names = ["const", *controls, instrument]
    X = _design(df, [*controls, instrument])
    res = _ols(y, X, names)
    coef, se = res.get(instrument)
    f_stat = (coef / se) ** 2                      # single-instrument F = t^2
    return {"instrument_coef": coef, "instrument_se": se, "F_stat": f_stat, "n": res.n}


def iv_2sls_elasticity(
    df: pd.DataFrame,
    instrument: str = "cost_shock_z",
    controls: Sequence[str] = ("season",),
) -> dict:
    """2SLS elasticity using the cost shock as an instrument for log(fee)."""
    y = df["log_volume"].to_numpy(dtype=float)
    names = ["const", "log_fee", *controls]
    X = _design(df, ["log_fee", *controls])                 # endogenous + exog
    Z = _design(df, [*controls, instrument])                # exog + excluded IV
    res = _tsls(y, X, Z, names)
    coef, se = res.get("log_fee")
    fs = first_stage_strength(df, instrument, controls)
    return {
        "method": "IV / 2SLS",
        "elasticity": coef,
        "se": se,
        "n": res.n,
        "first_stage_F": fs["F_stat"],
    }


def segmented_elasticity(
    df: pd.DataFrame,
    instrument: str = "cost_shock_z",
    controls: Sequence[str] = ("season",),
) -> pd.DataFrame:
    """Estimate OLS and IV elasticities per segment and join the ground truth."""
    rows = []
    for seg, sub in df.groupby("segment"):
        ols = naive_ols_elasticity(sub, controls)
        iv = iv_2sls_elasticity(sub, instrument, controls)
        truth = float(sub["true_elasticity"].iloc[0])
        rows.append(
            {
                "segment": seg,
                "true_elasticity": truth,
                "ols_elasticity": ols["elasticity"],
                "ols_se": ols["se"],
                "iv_elasticity": iv["elasticity"],
                "iv_se": iv["se"],
                "first_stage_F": iv["first_stage_F"],
                "ols_bias": ols["elasticity"] - truth,
                "iv_bias": iv["elasticity"] - truth,
            }
        )
    return pd.DataFrame(rows).sort_values("true_elasticity").reset_index(drop=True)


if __name__ == "__main__":
    from fast_txn_simulator import SimConfig, generate_fast_txn_data

    data = generate_fast_txn_data(SimConfig())

    print("Pooled estimates (all segments):")
    print("  OLS:", naive_ols_elasticity(data))
    print("  IV :", iv_2sls_elasticity(data))

    print("\nPer-segment elasticity (truth vs OLS vs IV):")
    table = segmented_elasticity(data)
    with pd.option_context("display.float_format", lambda v: f"{v:7.3f}"):
        print(table.to_string(index=False))
