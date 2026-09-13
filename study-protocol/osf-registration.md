# OSF Preregistration — Repair Continuum N-of-1 Pilot

Filled from `01-preregistration.md`, using the OSF **Preregistration** template section
structure. Copy each section into the matching field on osf.io when you register, or
attach this file to a registration. Fields marked **`⟨FILL⟩`** need your decision and/or
your physician's input **before** you freeze — do not register with placeholders.

> Register on [OSF Registries](https://osf.io/registries) **before the first active block.**
> Freeze it, capture the timestamp/DOI + the git commit SHA of this file.

---

## Study Information

**Title**
Continuous vs pulsed low-rate subcutaneous delivery in a single subject: a randomized, self-blinded N-of-1 pilot (Repair Continuum).

**Description**
A single-subject (N-of-1) pilot testing whether low-rate pulsed/continuous delivery of a shelf-stable investigational compound alters tissue-repair and recovery biomarkers relative to matched placebo periods, and whether a reproducible open-source measurement platform can generate a credible single-subject signal. This is a **feasibility- and signal-generating** study, not a confirmatory efficacy trial. Human-efficacy evidence for the compound(s) is limited; the pilot does not claim to establish efficacy.

**Hypotheses** (directional, locked)
- **Primary (H1):** Active periods reduce post-stressor CK AUC₀₋₇₂ₕ relative to placebo periods (one-sided, active < placebo).
- **Secondary (H2–H6):** ⟨FILL — 3–5 from HRV RMSSD ↑, hsCRP ↓, IL-6 ↓, sleep efficiency ↑, subjective recovery ↑; state each direction⟩
- **Exploratory:** Full biomarker panel; hypothesis-generating only, directions pre-listed in the SAP table.

---

## Design Plan

**Study type**
Experimental — single-subject (N-of-1), randomized, self-blinded, placebo-controlled.

**Blinding**
Subject is blinded (self-blinded). A third party generates and holds the allocation and prepares handling-identical active/placebo units; the keyfile stays sealed until analysis lock. Blinding integrity is measured (per-block guess vs chance; Bang's index).

**Is there any additional blinding?**
Outcome capture (labs, wearables, journal) recorded without knowledge of allocation. Lab assays run by an external lab blind to allocation.

**Study design**
Randomized paired-block single-case experimental design (SCED). k paired blocks; within each pair, the order of one active and one placebo period is randomized. Each period = treatment window + washout. A separate, pre-study **IV characterization phase** (tolerability + PK, physician-supervised) is descriptive only and contributes no confirmatory inference; it exists to set block/washout lengths.
- k = **`⟨FILL⟩`** pairs (must be ≥ 6; see Sample Size).
- Treatment window length = **`⟨FILL⟩`** (≥ expected time-to-effect).
- Washout length = **`⟨FILL⟩`** (≥ 5× longest relevant half-life).

**Randomization**
Seeded RNG (`analysis/allocation.py`); seed and script committed; within-pair order randomized independently per pair. SHA-256 of the allocation recorded at seal.

---

## Sampling Plan

**Existing data**
Registration prior to creation of data.

**Explanation of existing data**
N/A — no outcome data collected before registration. (Any pilot/characterization values are non-confirmatory and will be labeled.)

**Data collection procedures**
Single subject (the investigator). Four streams: (1) biomarker panels at Weeks 0/4/8/12/16; (2) standardized eccentric stressor + CK time-course at baseline and end; (3) continuous wearable telemetry (HRV, sleep, RHR, activity), daily; (4) daily subjective journal. Capture and schema per `03-data-infrastructure.md`.

**Sample size**
N = 1 subject; **k = `⟨FILL⟩` paired blocks** (the unit of inference). Total periods = 2k.

**Sample size rationale**
The randomization test's smallest achievable one-sided p is 1/2^k, so k ≥ 6 is required to reach p < 0.05 at all (k=6 → 0.0156; k=8 → 0.0039). Choose k for margin and to cover expected dropout of blocks; justify the final k here: **`⟨FILL⟩`**.

**Stopping rule**
Fixed k; no interim efficacy peeking (would inflate error). **Mandatory safety stopping** independent of the analysis: any Grade ≥3 adverse event (CTCAE), any infusion-site infection, any systemic reaction, or any safety lab crossing a pre-set boundary → stop immediately, unblind if clinically indicated, seek care. Safety boundaries: **`⟨FILL — with physician⟩`**.

---

## Variables

**Manipulated variables**
A single within-pair factor with two levels: **active** vs **placebo** period. These are opaque labels for analysis. The compound identity, route, dose, concentration, sterility/endotoxin certification, and administration procedure are specified in a separate clinical annex agreed with a licensed physician and a sterile-compounding pharmacy — **out of scope for this registration**, which fixes design and analysis only.

**Measured variables**
- Primary: post-stressor CK AUC₀₋₇₂ₕ (U/L·h) from a standardized 5×10 max-effort eccentric protocol.
- Secondary: **`⟨FILL⟩`** (with units + LOINC where applicable).
- Exploratory panel: BDNF, NfL, hsCRP, IL-6, TGF-β1, VEGF, P1NP, CTX, hyaluronic acid, CK; CANTAB cognitive domains; wearable HRV (RMSSD), sleep architecture, RHR, activity; daily 1–10 subjective ratings.
- Feasibility/safety: delivery accuracy (bench test), adherence %, blinding-guess accuracy, graded AE log.

**Indices**
Within-pair difference d = active − placebo per pair (primary). Block-mean summaries for wearable streams feed the same test. Effect indices: paired SMD, log response ratio, Cliff's-delta nonoverlap (see SAP).

---

## Analysis Plan

**Statistical models**
Primary: exact **sign-flip randomization test** on within-pair differences of the primary endpoint (`analysis/randomization_test.py`) — validity from the randomization, no normality/independence assumption. Secondary endpoints: same test per endpoint. Wearable series: block-mean summaries into the randomization test, with a GLS+AR(1) sensitivity model on the daily series (detrended, day-of-week covariate).

**Transformations**
Strictly positive biomarkers analyzed on the log scale (log response ratio). Wearable series detrended with a pre-specified LOESS/spline span before residual analysis.

**Inference criteria**
Primary: one-sided α = 0.05 in the pre-registered direction. Secondary family: Benjamini–Hochberg FDR, q = 0.05. Exploratory: estimation + CIs only, no confirmatory p-values.

**Data exclusion**
No outcome exclusions except protocol deviations logged in `logs/deviations.md`; sensitivity analysis with/without deviated blocks pre-specified.

**Missing data**
Report % missing per stream. Available-case for descriptives; multiple imputation sensitivity if a stream exceeds 10% missing. The randomization test uses complete pairs; incomplete pairs handled by a pre-stated rule: **`⟨FILL — e.g. drop incomplete pair⟩`**.

**Exploratory analysis**
The full panel and any post-hoc looks are reported as exploratory and clearly labeled; no exploratory result is presented as confirmatory.

---

## Other

- **Reproducibility:** pre-unblinding dry run on simulated data (`analysis/dry_run.py`) committed with its output before unblinding, proving the pipeline predates the results.
- **Reporting:** CENT 2015 (CONSORT extension for N-of-1) checklist.
- **Ethics/oversight:** self-experimentation on one consenting adult; **any additional human subjects (Cohort 2) require IRB review and are not covered by this registration.** Physician of record: **`⟨FILL⟩`**; compounding pharmacy: **`⟨FILL⟩`**.
- **Data sharing:** de-identified data, code, frozen pre-reg + SAP, deviation log released CC-BY-4.0 on completion.
- **Repository commit SHA at registration:** **`⟨FILL⟩`**
