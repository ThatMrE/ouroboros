"""Seeded allocation for the randomized, self-blinded N-of-1 (paired-block SCED).

For each of k paired blocks, randomizes the ORDER of the two arms
(``active`` / ``placebo``) within the pair. The subject stays blind; a third
party generates and holds the output. The seed is recorded so the sequence is
reproducible and auditable, and a SHA-256 fingerprint lets you prove at
unblinding that the sealed file was not altered.

This module contains NO administration logic. "active"/"placebo" are opaque
labels for the analysis; how a period is actually run is out of scope here and
belongs with a physician + compounding pharmacy.

Usage
-----
    python allocation.py --pairs 6 --seed 20260912 --out ../keys/allocation.csv
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone

import numpy as np

ARMS = ("active", "placebo")


def generate_allocation(n_pairs: int, seed: int) -> list[dict]:
    """Return one row per pair with a randomized within-pair arm order."""
    if n_pairs < 1:
        raise ValueError("n_pairs must be >= 1")
    rng = np.random.default_rng(seed)
    rows = []
    for pair in range(1, n_pairs + 1):
        first_active = bool(rng.integers(0, 2))
        rows.append(
            {
                "pair": pair,
                "period_1_arm": "active" if first_active else "placebo",
                "period_2_arm": "placebo" if first_active else "active",
                "active_period": 1 if first_active else 2,
            }
        )
    return rows


def allocation_fingerprint(rows: list[dict]) -> str:
    """Stable SHA-256 over the allocation, for sealed-file integrity checks."""
    payload = json.dumps(rows, sort_keys=True).encode()
    return hashlib.sha256(payload).hexdigest()


def write_allocation(rows: list[dict], path: str, seed: int) -> str:
    fp = allocation_fingerprint(rows)
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["# N-of-1 allocation keyfile — SEALED until analysis lock"])
        w.writerow([f"# generated_utc={datetime.now(timezone.utc).isoformat()}"])
        w.writerow([f"# seed={seed}"])
        w.writerow([f"# sha256={fp}"])
        w.writerow(["pair", "period_1_arm", "period_2_arm", "active_period"])
        for r in rows:
            w.writerow([r["pair"], r["period_1_arm"], r["period_2_arm"], r["active_period"]])
    return fp


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pairs", type=int, required=True, help="number of paired blocks k")
    ap.add_argument("--seed", type=int, required=True, help="RNG seed (record it!)")
    ap.add_argument("--out", default="allocation.csv", help="output keyfile path")
    args = ap.parse_args()

    rows = generate_allocation(args.pairs, args.seed)
    fp = write_allocation(rows, args.out, args.seed)
    p_min = 1 / (2 ** args.pairs)
    print(f"Wrote {args.pairs} pairs to {args.out}")
    print(f"seed={args.seed}  sha256={fp}")
    print(f"Smallest achievable one-sided randomization p-value: p_min = 1/2^{args.pairs} = {p_min:.4g}")
    if p_min > 0.05:
        print("WARNING: with this k you CANNOT reach p<0.05. Increase --pairs (>=6).")


if __name__ == "__main__":
    main()
