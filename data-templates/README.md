# Data-entry templates

Blank CSVs matching the schema in `study-protocol/03-data-infrastructure.md`. Fill
these as you collect; they drop straight into the analysis pipeline.

| File | Feeds | Columns |
|------|-------|---------|
| `primary_endpoint.csv` | `analysis/analyze.py` (primary) | `pair,arm,value` — `arm` ∈ {active,placebo}; one+ rows per (pair,arm) |
| `biomarkers.csv` | exploratory panel | `timepoint,week,marker,value,units,loinc,notes` |
| `wearables_daily.csv` | continuous streams | `date,hrv_rmssd_ms,sleep_efficiency_pct,deep_min,rem_min,total_sleep_min,resting_hr_bpm,steps,source` |
| `journal_daily.csv` | subjective | `date,energy_1_10,…,site_reaction_0_3,notes` |
| `ae_log.csv` | safety | `date,event,ctcae_grade,related_to_intervention,action_taken,resolved,notes` |
| `effects_TEMPLATE.csv` | `analysis/forest_plot.py` | `label,point,ci_low,ci_high,direction` (direction: up/down) |

## Rules (from the data-infrastructure plan)
- **Raw is append-only.** Never edit a recorded value in place; correct via a new dated row + a note.
- **Dates in ISO 8601** (`YYYY-MM-DD`), times in UTC with local offset recorded.
- **Blank = missing**, not zero. The pipeline reports % missing per stream.
- Keep these out of the public repo until de-identified — `.gitignore` already excludes `data/`.
  Work in `data/` locally; commit only de-identified derived outputs on release.
- `pair`/`arm` in `primary_endpoint.csv` are opaque labels; the active/placebo mapping stays sealed
  in `keys/allocation.csv` until analysis lock.

## Flow
```
data-templates/primary_endpoint.csv  ->  fill ->  data/primary_endpoint.csv
make analyze                         # runs the pre-registered primary test
# effect estimates -> effects.csv -> python analysis/forest_plot.py --data effects.csv ...
```
