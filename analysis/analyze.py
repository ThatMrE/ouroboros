"""Run the pre-registered primary analysis on REAL (unblinded) data.

Expects a tidy CSV at data/primary_endpoint.csv with columns:
    pair,arm,value      # arm in {active, placebo}; one or more rows per (pair,arm)

Only run this AFTER: dry run committed, dataset frozen, allocation keyfile
unsealed and merged in. Writes a report to derived/primary_result.txt.

    python analyze.py --data ../data/primary_endpoint.csv --alt greater
"""
from __future__ import annotations

import argparse
import os
import sys

import pandas as pd

from randomization_test import within_pair_diffs, randomization_test
from effect_sizes import all_effects


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data", default="../data/primary_endpoint.csv")
    ap.add_argument("--alt", default="greater", choices=["greater", "less", "two-sided"],
                    help="pre-registered direction")
    ap.add_argument("--out", default="../derived/primary_result.txt")
    args = ap.parse_args()

    if not os.path.exists(args.data):
        print(f"[analyze] No data file at {args.data}.")
        print("[analyze] This target runs the REAL analysis; it needs frozen, unblinded data.")
        print("[analyze] Expected columns: pair,arm,value (arm in {active,placebo}).")
        return 0  # not an error — just nothing to analyze yet

    df = pd.read_csv(args.data)
    diffs = within_pair_diffs(df)
    res = randomization_test(diffs, alternative=args.alt)
    effects = all_effects(df)

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    lines = ["PRIMARY ANALYSIS (pre-registered)", "=" * 40, str(res), "", "Effect sizes:"]
    lines += [f"  {e}" for e in effects]
    report = "\n".join(lines)
    with open(args.out, "w") as fh:
        fh.write(report + "\n")
    print(report)
    print(f"\n[analyze] wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
