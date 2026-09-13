"""Simulate paired-block N-of-1 outcome data with a KNOWN injected effect.

Used only for the pre-unblinding dry run (SAP §9): prove the pipeline recovers an
effect it was given, before it ever sees real data. Includes AR(1) within-period
noise and a per-pair random level, so it isn't an unrealistically clean toy.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from allocation import generate_allocation


def simulate(
    n_pairs: int,
    true_effect: float,
    seed: int = 0,
    baseline: float = 100.0,
    pair_sd: float = 8.0,
    noise_sd: float = 6.0,
    ar1: float = 0.4,
    obs_per_period: int = 5,
    allocation_seed: int | None = None,
) -> pd.DataFrame:
    """Return tidy rows: pair, arm, period, obs, value.

    true_effect is added to ACTIVE periods (in outcome units). Set 0 for the null.
    """
    rng = np.random.default_rng(seed)
    alloc = generate_allocation(n_pairs, allocation_seed if allocation_seed is not None else seed)

    def ar1_noise(n: int) -> np.ndarray:
        e = rng.normal(0, noise_sd, n)
        x = np.empty(n)
        x[0] = e[0]
        for t in range(1, n):
            x[t] = ar1 * x[t - 1] + e[t]
        return x

    rows = []
    for row in alloc:
        pair = row["pair"]
        pair_level = rng.normal(0, pair_sd)
        for period in (1, 2):
            arm = row[f"period_{period}_arm"]
            eff = true_effect if arm == "active" else 0.0
            vals = baseline + pair_level + eff + ar1_noise(obs_per_period)
            for j, v in enumerate(vals):
                rows.append({"pair": pair, "arm": arm, "period": period, "obs": j, "value": float(v)})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = simulate(n_pairs=6, true_effect=10.0, seed=1)
    print(df.head())
    print("\nblock means:\n", df.groupby(["pair", "arm"])["value"].mean().unstack())
