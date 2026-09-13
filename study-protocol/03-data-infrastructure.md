# Data Infrastructure Plan — N-of-1

**Version:** 0.1 · **Date:** _____
Goal: every number is captured once, timestamped, versioned, and regenerable — so the final open dataset is trustworthy and the analysis is reproducible by a stranger.

---

## 1. Principles

1. **Raw is sacred.** Raw captures are append-only and never edited in place. All cleaning happens in code, from raw → derived.
2. **Separate capture from allocation.** The blinding keyfile lives apart from outcome data and stays sealed until analysis lock (see §5).
3. **Everything timestamped, in UTC**, with local offset recorded.
4. **Reproducible from `raw/` with one command.**

## 2. Capture tooling

**Recommended: [REDCap](https://projectredcap.org/) if you can access an instance** (many institutions/ResearchHub collaborators can host; it's the clinical-data-capture gold standard, supports N-of-1, audit trails, data dictionary, validation, e-consent). It gives you validation and an audit log for free.

**Lightweight fallback (fully self-hosted, no institution):**
- Structured entry via a form (a self-hosted [Formbricks]/[LimeSurvey], or even a validated spreadsheet template) → export to CSV.
- Wearables via official export/APIs (Oura API, Garmin Connect / Health API, Whoop API). Pull raw JSON, store verbatim.
- Lab results: PDF + transcribed CSV, double-entered (enter twice, diff to catch typos).

Either way, the **repo holds the schema, dictionary, and code**; the **data** lives in a private store (§6).

## 3. Repository layout

```
ouroboros/                     (or a dedicated study repo)
  study-protocol/              # frozen pre-reg, SAP, this doc, bench-test
  data-dictionary/
    biomarkers.yaml            # every field: name, units, LOINC, range, direction
    wearables.yaml
    functional.yaml
    journal.yaml
  raw/                         # append-only; NEVER hand-edited (see §6 re: PII)
    biomarkers/labs_YYYYMMDD.csv
    wearables/oura_YYYYMMDD.json
    ...
  derived/                     # generated only by code
  analysis/
    allocation.py              # seeded randomization (seed recorded)
    pipeline.py                # raw -> derived
    primary_randomization_test.py
    figures.py
    env.lock / requirements.txt / renv.lock
  keys/                        # SEALED — see §5 (encrypted or gitignored+external)
  logs/
    deviations.md
    ae_log.csv                 # adverse events, CTCAE-graded
```

## 4. Schema / data dictionary (per field)

Each field defined once in `data-dictionary/*.yaml`:
```yaml
- field: crp_hs
  label: High-sensitivity CRP
  units: mg/L
  loinc: "30522-7"
  valid_range: [0, 20]
  hypothesized_direction: down       # from the SAP directional table
  instrument: "Lab X assay Y"
  capture: lab
```
Use **LOINC** codes for labs and standard units — makes the open dataset interoperable and forces consistency.

## 5. Blinding & allocation integrity

- `analysis/allocation.py` generates the sequence from a **recorded seed**; output written to `keys/allocation.enc` (age/gpg-encrypted) held by the **third-party preparer**, not the subject.
- Outcome capture systems must **not** contain the allocation.
- Unblinding = decrypt keyfile *after* dataset freeze + analysis lock; record the timestamp in `logs/deviations.md`.

## 6. Storage, PII & backup

- **PII** (name, DOB, raw wearable accounts, photos of sites) stays out of the public repo. Keep raw PII in an encrypted private store (encrypted drive / private bucket with versioning). Public repo gets **de-identified derived data** only.
- **3-2-1 backup:** 3 copies, 2 media, 1 offsite. Wearable data especially — pull and back up regularly; vendor exports expire.
- **Immutability:** enable object-versioning on the raw store, or commit raw to a private git-LFS repo, so nothing is silently overwritten.

## 7. Data validation

- On ingest, `pipeline.py` checks each field against `valid_range`, flags out-of-range and missing, writes a validation report to `derived/validation_report.md`.
- Lab CSVs double-entered and diffed.
- Wearable gaps quantified (the SAP needs % missingness per stream).

## 8. Reproducible environment

- Pin everything: `requirements.txt` + a lockfile (`pip-tools`/`uv`/`conda-lock`) or `renv.lock` for R.
- One entry point: `make all` (or `analysis/run_all.sh`) regenerates `derived/` + all figures from `raw/`.
- Tag the repo at registration, at dataset freeze, and at publication.

## 9. Release (on completion)

- Publish de-identified `raw`/`derived`, dictionary, code, frozen pre-reg + SAP, deviation log → OSF + repo, **CC-BY-4.0**.
- Include the pre-unblinding simulated-data dry-run notebook (proves the pipeline predates the results).
