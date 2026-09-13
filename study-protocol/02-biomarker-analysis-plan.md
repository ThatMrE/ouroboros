# Biomarker & Outcome Analysis Plan (SAP) — N-of-1

**Version:** 0.1 · **Date:** _____ · Companion to `01-preregistration.md`
**Lock this before unblinding.** Every choice below is pre-specified; the analysis script is written and dry-run on *simulated* data before real data is unblinded.

---

## 0. Guiding principles

1. **One primary endpoint, one primary test.** Everything else is secondary/exploratory and labeled so in every output.
2. **N-of-1 time series violate independence.** Standard t-tests are invalid here (serial autocorrelation inflates false positives). Use methods that don't assume independence.
3. **Estimation over dichotomy.** Report effect sizes with intervals, not just p-values.
4. **Pre-specify direction** for every marker (below). A marker moving the "wrong" way is not a win.

---

## 1. Primary analysis — randomization test

The primary endpoint (post-stressor CK AUC₀₋₇₂ₕ, per pre-reg §5) is analyzed with a **randomization (permutation) test**, which is exact and makes **no distributional or independence assumptions** — it derives the null from the actual randomized allocation.

**Procedure**
1. Test statistic T = mean(active blocks) − mean(placebo blocks) on the primary endpoint.
2. Enumerate (or Monte-Carlo sample, ≥10,000) all allocation sequences consistent with the randomization scheme (§4 of pre-reg).
3. Recompute T under each; the p-value = proportion of |T*| ≥ |T_observed| (two-sided) — but since direction is pre-registered, use the **one-sided** tail in the hypothesized direction and state this.
4. Report T_observed, the permutation null distribution (plot it), and exact p.

**Why not ARIMA/GLS for the primary:** those are fine for modeling but require correct model specification; the randomization test is assumption-light and its validity comes from the design itself. Keep the primary bulletproof.

## 2. Effect-size estimation (all endpoints)

Report, per endpoint:
- **Standardized mean difference** between phases (active vs placebo), with a **carryover-robust** variant that uses only within-pair contrasts.
- **Log response ratio** for strictly positive biomarkers (interpretable as % change).
- **Tau-U** (nonoverlap index) as a nonparametric robustness check for each time series.
- **Bootstrap CIs** via block/pair resampling (respects the paired structure), not naive i.i.d. bootstrap.

## 3. Secondary endpoints — multiplicity control

- The 3–5 secondary endpoints (pre-reg §5) each get the same randomization test + effect estimate.
- Control the **false discovery rate** across the secondary family with **Benjamini–Hochberg, q = 0.05**.
- Report both raw and BH-adjusted p. Never promote a secondary "hit" to a primary claim.

## 4. Exploratory panel — estimation only

The full marker panel (BDNF, NfL, TGF-β1, VEGF, P1NP, CTX, hyaluronic acid, IL-6, hsCRP, CANTAB domains…):
- **Estimation + intervals only, explicitly labeled exploratory.** No confirmatory p-values.
- Present as a forest plot of standardized effects with CIs.
- Pre-register the **directional prior** for each (fill this table before starting):

| Marker | Hypothesized direction under active | Rationale (1 line) |
|--------|-------------------------------------|--------------------|
| VEGF | ↑ | pro-angiogenic MoA |
| TGF-β1 | ↑ | fibroblast activation |
| P1NP | ↑ | bone/collagen formation |
| CTX | ↓ or ns | resorption |
| hsCRP | ↓ | anti-inflammatory claim |
| IL-6 | ↓ | " |
| NfL | ns | safety (no neuro-axonal harm) |
| … | … | … |

Markers moving opposite to prior are reported honestly as counter-evidence.

## 5. Continuous wearable streams (HRV, sleep, RHR, activity)

Daily series over ~120 days need explicit time-series handling:
- **Detrend** slow drift (fitness, seasonality) with a pre-specified method (e.g. LOESS or a spline with pre-set span); analyze residuals.
- **Model autocorrelation:** fit per-stream to phase indicator with **GLS + AR(1)** (or ARIMA with auto-selected order on the *baseline* segment, then held fixed), OR feed block-mean summaries into the same randomization test (simpler, preferred for the confirmatory tier).
- **Day-of-week and weekend effects** as covariates.
- **Missing data:** pre-specify handling — report % missing per stream; use available-case for descriptive, and a sensitivity analysis with multiple imputation if missingness > 10%. Do **not** silently drop.

## 6. Blinding-integrity analysis

- Compare block-level allocation guesses to chance (binomial test). Report Bang's Blinding Index. If blinding failed, the primary result is downgraded to exploratory in the writeup — state this rule now.

## 7. Safety analysis

- AE table graded (CTCAE), by block and by active/placebo.
- Safety labs plotted against pre-set boundaries (pre-reg §8) with the boundary lines drawn.

## 8. Sensitivity analyses (pre-specified)

- Primary result with/without any deviated blocks.
- Carryover-only (within-pair) vs pooled estimator.
- Leave-one-block-out stability of the primary effect.
- Alternative detrending spans for wearables.

## 9. Reproducibility

- All analysis in versioned scripts (`analysis/`), run against a **pinned environment** (see data-infrastructure doc).
- **Pre-registration dry run:** execute the entire pipeline end-to-end on simulated data with a known injected effect, confirm it recovers it, and commit that notebook *before* unblinding. This proves the pipeline wasn't tuned to the real data.
- Random seeds recorded; outputs regenerable from raw data with one command.

## 10. Reporting

- CONSORT-extension for N-of-1 (the **CENT 2015** guideline) as the reporting checklist.
- Publish: frozen pre-reg, SAP, code, de-identified data, and the discrepancy log (any deviation from this plan).
