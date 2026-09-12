"""Pre-unblinding dry run (SAP §9).

Runs the WHOLE primary pipeline on simulated data:
  1) a null world (true_effect = 0)  -> the test should NOT cry wolf, and a
     calibration check confirms the false-positive rate ~ nominal alpha;
  2) an effect world (true_effect > 0) -> the test SHOULD detect it, and the
     effect estimators should bracket the truth.

Commit this and its output BEFORE unblinding, to prove the pipeline predates the
real results and was not tuned to them.

    python dry_run.py
"""
from __future__ import annotations

import numpy as np

from simulate import simulate
from randomization_test import within_pair_diffs, randomization_test
from effect_sizes import all_effects

ALPHA = 0.05
N_PAIRS = 8          # p_min = 1/2^8 = 0.0039, comfortable margin under 0.05
TRUE_EFFECT = 10.0   # outcome units injected into ACTIVE periods


def one_world(true_effect: float, seed: int):
    df = simulate(n_pairs=N_PAIRS, true_effect=true_effect, seed=seed)
    diffs = within_pair_diffs(df)
    res = randomization_test(diffs, alternative="greater")
    effects = all_effects(df)
    return res, effects


def calibration(true_effect: float, n_worlds: int = 400, base_seed: int = 1000):
    """Fraction of simulated worlds with p < ALPHA (should ~alpha under null,
    high under a real effect = empirical power)."""
    hits = 0
    for s in range(n_worlds):
        df = simulate(n_pairs=N_PAIRS, true_effect=true_effect, seed=base_seed + s)
        diffs = within_pair_diffs(df)
        if randomization_test(diffs, alternative="greater").p_value < ALPHA:
            hits += 1
    return hits / n_worlds


def main() -> None:
    print("=" * 70)
    print(f"DRY RUN  (k={N_PAIRS} pairs, alpha={ALPHA}, injected effect={TRUE_EFFECT})")
    print("=" * 70)

    print("\n[1] NULL WORLD (true_effect = 0)")
    res0, eff0 = one_world(0.0, seed=42)
    print("   ", res0)
    for e in eff0:
        print("    ", e)

    print("\n[2] EFFECT WORLD (true_effect > 0)")
    res1, eff1 = one_world(TRUE_EFFECT, seed=42)
    print("   ", res1)
    for e in eff1:
        print("    ", e)

    print("\n[3] CALIBRATION over many simulated worlds")
    fpr = calibration(0.0, n_worlds=400)
    power = calibration(TRUE_EFFECT, n_worlds=400)
    print(f"    False-positive rate under null : {fpr:.3f}   (target <= ~{ALPHA})")
    print(f"    Empirical power at effect={TRUE_EFFECT} : {power:.3f}   (want high)")

    print("\nCHECKS")
    ok_null = res0.p_value > ALPHA
    ok_eff = res1.p_value < ALPHA
    ok_fpr = fpr <= ALPHA + 0.03  # sampling slack
    ok_pow = power >= 0.80
    for label, ok in [
        ("null world not significant", ok_null),
        ("effect world significant", ok_eff),
        ("false-positive rate ~ nominal", ok_fpr),
        ("power >= 0.80", ok_pow),
    ]:
        print(f"    [{'PASS' if ok else 'FAIL'}] {label}")

    if all([ok_null, ok_eff, ok_fpr, ok_pow]):
        print("\nDRY RUN PASSED — pipeline recovers known effects and is calibrated.")
    else:
        raise SystemExit("DRY RUN FAILED — investigate before trusting the pipeline.")


if __name__ == "__main__":
    main()
