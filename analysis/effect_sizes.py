"""Effect-size estimators for the paired-block N-of-1, with pair-bootstrap CIs.

All operate on within-pair structure so they respect the design (see the SAP).
Nothing here is confirmatory on its own — report alongside the randomization test.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class Estimate:
    name: str
    point: float
    ci_low: float
    ci_high: float
    level: float

    def __str__(self) -> str:
        return f"{self.name}: {self.point:.4g}  [{self.ci_low:.4g}, {self.ci_high:.4g}] ({self.level:.0%} CI)"


def paired_smd(diffs: np.ndarray) -> float:
    """Standardized mean difference from within-pair diffs (mean/SD of diffs)."""
    diffs = np.asarray(diffs, float)
    sd = diffs.std(ddof=1)
    return float(diffs.mean() / sd) if sd > 0 else np.nan


def log_response_ratio(active: np.ndarray, placebo: np.ndarray) -> float:
    """Mean within-pair log ratio; exp()-1 ~ fractional change. Positive values only."""
    active = np.asarray(active, float)
    placebo = np.asarray(placebo, float)
    if np.any(active <= 0) or np.any(placebo <= 0):
        return np.nan
    return float(np.mean(np.log(active) - np.log(placebo)))


def tau_nonoverlap(active: np.ndarray, placebo: np.ndarray) -> float:
    """Simple nonoverlap index (Cliff's delta) of active vs placebo values in [-1, 1]."""
    active = np.asarray(active, float)
    placebo = np.asarray(placebo, float)
    gt = sum(a > p for a in active for p in placebo)
    lt = sum(a < p for a in active for p in placebo)
    n = active.size * placebo.size
    return float((gt - lt) / n) if n else np.nan


def pair_bootstrap_ci(
    stat_fn,
    *arrays: np.ndarray,
    n_boot: int = 10000,
    level: float = 0.95,
    seed: int = 0,
) -> tuple[float, float]:
    """Percentile bootstrap resampling PAIRS (columns aligned across arrays)."""
    arrays = [np.asarray(a, float) for a in arrays]
    k = arrays[0].size
    rng = np.random.default_rng(seed)
    boots = np.empty(n_boot)
    for b in range(n_boot):
        idx = rng.integers(0, k, size=k)
        boots[b] = stat_fn(*[a[idx] for a in arrays])
    alpha = (1 - level) / 2
    lo, hi = np.nanpercentile(boots, [100 * alpha, 100 * (1 - alpha)])
    return float(lo), float(hi)


def all_effects(
    df: pd.DataFrame,
    value: str = "value",
    pair: str = "pair",
    arm: str = "arm",
    active: str = "active",
    placebo: str = "placebo",
    level: float = 0.95,
    seed: int = 0,
) -> list[Estimate]:
    wide = df.pivot_table(index=pair, columns=arm, values=value, aggfunc="mean").dropna()
    a = wide[active].to_numpy()
    p = wide[placebo].to_numpy()
    d = a - p

    out: list[Estimate] = []

    lo, hi = pair_bootstrap_ci(lambda x: np.mean(x), d, n_boot=10000, level=level, seed=seed)
    out.append(Estimate("mean_diff (active-placebo)", float(d.mean()), lo, hi, level))

    lo, hi = pair_bootstrap_ci(lambda x: paired_smd(x), d, n_boot=10000, level=level, seed=seed)
    out.append(Estimate("paired_SMD", paired_smd(d), lo, hi, level))

    if np.all(a > 0) and np.all(p > 0):
        lo, hi = pair_bootstrap_ci(log_response_ratio, a, p, n_boot=10000, level=level, seed=seed)
        out.append(Estimate("log_response_ratio", log_response_ratio(a, p), lo, hi, level))

    lo, hi = pair_bootstrap_ci(tau_nonoverlap, a, p, n_boot=10000, level=level, seed=seed)
    out.append(Estimate("nonoverlap (Cliff delta)", tau_nonoverlap(a, p), lo, hi, level))

    return out


if __name__ == "__main__":
    rng = np.random.default_rng(0)
    a = rng.normal(10, 2, 6) + 2
    p = rng.normal(10, 2, 6)
    df = pd.DataFrame(
        {"pair": list(range(6)) * 2,
         "arm": ["active"] * 6 + ["placebo"] * 6,
         "value": np.concatenate([a, p])}
    )
    for e in all_effects(df):
        print(e)
