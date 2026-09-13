"""Exact randomization (sign-flip) test for the paired-block N-of-1 primary endpoint.

Design: k paired blocks, each with one ``active`` and one ``placebo`` period whose
ORDER was randomized (see ``allocation.py``). The null hypothesis is that the arm
label is exchangeable within each pair; under it, the sign of each within-pair
difference d_i = active_i - placebo_i flips with probability 1/2. The reference
distribution is therefore the 2^k sign combinations — enumerated exactly when
feasible, Monte-Carlo sampled otherwise. This is assumption-light: validity comes
from the randomization, not from normality or independence.

See ``02-biomarker-analysis-plan.md`` for how this is used (primary endpoint).
"""
from __future__ import annotations

import itertools
from dataclasses import dataclass, asdict

import numpy as np
import pandas as pd

MAX_EXACT_K = 22  # 2^22 ~ 4.2M rows; beyond this, Monte-Carlo


def within_pair_diffs(
    df: pd.DataFrame,
    value: str = "value",
    pair: str = "pair",
    arm: str = "arm",
    active: str = "active",
    placebo: str = "placebo",
) -> np.ndarray:
    """Collapse tidy (pair, arm, value) rows to one active-minus-placebo diff per pair."""
    wide = df.pivot_table(index=pair, columns=arm, values=value, aggfunc="mean")
    missing = [c for c in (active, placebo) if c not in wide.columns]
    if missing:
        raise ValueError(f"missing arm(s) in data: {missing}")
    diffs = (wide[active] - wide[placebo]).dropna().to_numpy()
    if diffs.size == 0:
        raise ValueError("no complete pairs found")
    return diffs


@dataclass
class RandomizationResult:
    t_obs: float
    p_value: float
    k: int
    alternative: str
    exact: bool
    n_reference: int
    p_min: float

    def __str__(self) -> str:
        kind = "exact" if self.exact else "Monte-Carlo"
        return (
            f"Randomization test ({kind}, {self.alternative}): "
            f"T={self.t_obs:.4g}, p={self.p_value:.4g} "
            f"(k={self.k}, p_min={self.p_min:.4g}, N_ref={self.n_reference})"
        )


def randomization_test(
    diffs: np.ndarray,
    alternative: str = "greater",
    n_mc: int | None = None,
    seed: int = 0,
) -> RandomizationResult:
    """Sign-flip randomization test on within-pair differences.

    alternative: 'greater' (active > placebo), 'less', or 'two-sided'.
    Pre-register the direction; use one-sided to match it.
    """
    diffs = np.asarray(diffs, dtype=float)
    k = diffs.size
    t_obs = float(diffs.mean())

    if n_mc is None and k <= MAX_EXACT_K:
        signs = np.array(list(itertools.product((1, -1), repeat=k)), dtype=float)
        stats = (signs * diffs).mean(axis=1)
        exact = True
        n_ref = stats.size
    else:
        rng = np.random.default_rng(seed)
        n_mc = int(n_mc or 20000)
        signs = rng.choice((1.0, -1.0), size=(n_mc, k))
        stats = (signs * diffs).mean(axis=1)
        stats = np.concatenate([stats, [t_obs]])  # always include the observed
        exact = False
        n_ref = stats.size

    if alternative == "greater":
        p = float(np.mean(stats >= t_obs))
    elif alternative == "less":
        p = float(np.mean(stats <= t_obs))
    elif alternative == "two-sided":
        p = float(np.mean(np.abs(stats) >= abs(t_obs)))
    else:
        raise ValueError("alternative must be 'greater', 'less', or 'two-sided'")

    return RandomizationResult(
        t_obs=t_obs,
        p_value=p,
        k=k,
        alternative=alternative,
        exact=exact,
        n_reference=n_ref,
        p_min=1.0 / (2 ** k),
    )


if __name__ == "__main__":
    # tiny self-check
    d = np.array([2.1, 1.4, 3.0, 0.9, 2.6, 1.8])
    print(randomization_test(d, alternative="greater"))
