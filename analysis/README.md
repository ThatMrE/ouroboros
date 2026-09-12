# Analysis code — N-of-1 primary pipeline

Statistics only. No device control, no dosing, no administration logic. Operates
on tidy data (`pair, arm, value`) and on simulated data for the dry run.

## Files
| File | Purpose |
|------|---------|
| `allocation.py` | Seeded, auditable within-pair randomization of `active`/`placebo`. Writes a sealed keyfile with seed + SHA-256. |
| `randomization_test.py` | Exact sign-flip randomization test on within-pair differences (the pre-registered primary analysis). Monte-Carlo fallback for large k. |
| `effect_sizes.py` | Paired SMD, log response ratio, nonoverlap (Cliff's delta), with pair-bootstrap CIs. |
| `simulate.py` | Simulate paired-block data with a KNOWN injected effect (AR(1) noise + per-pair level). |
| `dry_run.py` | Runs the whole pipeline on simulated null and effect worlds; checks calibration + power. Commit its output BEFORE unblinding. |

## Quickstart
```bash
pip install -r requirements.txt

# 1. Generate the allocation (a THIRD PARTY does this and holds the file)
python allocation.py --pairs 8 --seed <SEED> --out ../keys/allocation.csv

# 2. Prove the pipeline works on simulated data (pre-unblinding)
python dry_run.py
```

## Discipline
- Run `dry_run.py` and commit its output **before** touching real data — it proves
  the pipeline predates and wasn't tuned to the results (SAP §9).
- Pre-register the direction (`alternative="greater"`/`"less"`) to match the hypothesis.
- Need k >= 6 pairs for the randomization test to reach p<0.05 at all; k=8 gives margin.
- `active`/`placebo` are opaque labels here; administration is out of scope for this code.
