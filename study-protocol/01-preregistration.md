# Pre-Registration — Repair Continuum N-of-1 Pilot

**Status:** DRAFT for registration · **Version:** 0.1 · **Date:** _____
**Investigator / Subject:** Elliot Roth (single subject, self-experiment)
**Registry target:** [OSF Registries](https://osf.io/registries) (frozen, timestamped) — OSF is the appropriate home for a self-funded N-of-1. ClinicalTrials.gov is for interventional trials under an IRB/IND; do not register there without one.

> **Register BEFORE the first active block.** The entire value of pre-registration is that the analysis and endpoints are locked before any data is seen. Freeze this document, get a timestamp/DOI, then start.

> **Scope of this document:** study *design* only — hypotheses, endpoints, randomization, blinding, analysis. It deliberately does **not** specify how the compound is prepared or administered. Route, dose, sterility certification, and clinical supervision are to be set with a licensed physician and a sterile-compounding pharmacy and recorded in a separate clinical annex, not here.

---

## 1. Background & rationale (≤250 words, lock it)

State, concisely and falsifiably:
- The gap: pulsatile bolus PK vs continuous-state repair biology (your thesis).
- Why N-of-1 is the right *first* instrument (hypothesis-generating, not confirmatory).
- What prior evidence exists for the compound(s) and what does **not** (be explicit that human efficacy evidence is thin — this pilot is about *feasibility + signal*, not proof).

Write the rationale so a skeptic agrees it's an honest question, not a foregone conclusion.

## 2. Objectives & hypotheses

Separate them by tier and commit to a **direction** for each. Undirected hypotheses invite post-hoc storytelling.

| Tier | Objective | Pre-specified hypothesis (directional) |
|------|-----------|----------------------------------------|
| **Primary** | _One_ endpoint only (see §5) | e.g. "Active blocks reduce post-stressor CK AUC vs placebo blocks." |
| Secondary | 3–5 endpoints | Each stated with direction. |
| Exploratory | Everything else | Explicitly hypothesis-generating; no confirmatory claims. |
| Feasibility | Delivery accuracy, adherence, blinding integrity, AE rate | Pass/fail thresholds set in §8. |

**One primary endpoint.** This is the single most important discipline in the whole document.

## 3. Design

**Recommended: randomized, self-blinded N-of-1 with alternating active/placebo blocks (a randomized block SCED).** Not a simple ABAB reversal — peptide effects plausibly have carryover, and reversal designs assume the effect washes out between phases.

- **Blocks:** k paired blocks (target **k ≥ 6 pairs**, i.e. 12 blocks; see §9 for why). Each block = [treatment period + washout].
- **Block length:** set treatment period ≥ expected time-to-effect; washout ≥ 5× the longest relevant half-life (biological, not just plasma). Justify both numbers from PK/PD, and if unknown, say so and pad conservatively.
- **Allocation:** within each pair, order of active vs placebo is randomized (see §4).
- **IV-first characterization phase (pre-study):** the initial IV test is a **separate, non-confirmatory tolerability/PK characterization step**, analyzed descriptively only. Its purpose: (a) confirm tolerability under supervision, (b) estimate PK to *set the block/washout lengths above*. It is not part of the randomized comparison and contributes no efficacy inference.

**Placebo:** vehicle-only, visually/handling-identical, prepared by someone other than the subject so blinding holds (see §4).

## 4. Randomization & blinding

- **Randomization:** generate the allocation sequence with a seeded RNG; record the seed and script in the repo (`analysis/allocation.py`). Do not hand-pick.
- **Allocation concealment:** a **third party** (not the subject) prepares coded units A/B and holds the keyfile. The subject never sees which is active.
- **Self-blinding:** subject records all outcomes without knowing allocation. The keyfile stays sealed (committed encrypted, or held by the third party) until the analysis is locked.
- **Unblinding:** only after the analysis script is finalized and the dataset frozen. Record the unblinding timestamp.
- **Blinding integrity check:** at each block, subject guesses allocation; compare guess accuracy to chance at the end (a real endpoint, §5 feasibility).

## 5. Outcomes (operationalized)

For every outcome specify: instrument, units, timing, and pre-registered direction. Draw from the site's four streams.

**Primary (choose ONE):**
- Candidate: **post-stressor CK AUC₀₋₇₂ₕ**, standardized eccentric protocol (5×10 max-effort), measured active-block vs placebo-block. Hard-to-fake functional readout.

**Secondary (3–5):** e.g. HRV (RMSSD) block-mean; hsCRP; IL-6; sleep efficiency; subjective recovery (1–10).

**Exploratory:** the full panel — BDNF, NfL, TGF-β1, VEGF, P1NP, CTX, hyaluronic acid, CANTAB, etc.

**Feasibility / safety:** delivery accuracy (from bench test), adherence %, blinding-guess accuracy, adverse-event log (graded, e.g. CTCAE).

Pre-register the **direction** of each biomarker (up/down) now — see the analysis plan.

## 6. Measurement schedule

Tabulate timepoints × measures (Week 0, 4, 8, 12, 16 for panels; daily for wearables/journal; stressor test at baseline + end). Lock the schedule; deviations are logged (§10).

## 7. Analysis plan

Full detail in `02-biomarker-analysis-plan.md`. Summary commitments locked here:
- Primary inference by **randomization test** (exact, distribution-free) on the primary endpoint.
- Secondary endpoints: FDR-controlled (Benjamini–Hochberg, q = 0.05) — reported as *secondary*, never elevated to headline.
- Exploratory: estimation + intervals only, labeled exploratory. No p-value shopping.

## 8. Decision & stopping rules

- **Success (feasibility):** pre-state thresholds — e.g. delivery accuracy within ±X%, adherence ≥ 90%, blinding maintained, no ≥Grade 3 AE.
- **Efficacy signal:** primary randomization-test p and effect estimate reported as-is; pre-state what magnitude would justify a Cohort-2 protocol (and note Cohort 2 requires IRB — out of scope here).
- **Safety stopping (mandatory, non-negotiable):** any Grade ≥3 AE, any infusion-site infection, any systemic reaction, or any lab crossing a pre-set safety boundary → **stop immediately**, unblind if clinically needed, seek care. List the specific lab boundaries with your physician.

## 9. Feasibility / "power" for N-of-1

A randomization test's smallest achievable p-value is bounded by the number of possible allocations. With k randomized pairs, p_min = 1 / 2^k for a paired sign-style test.
- k = 5 → p_min = 0.031
- **k = 6 → p_min = 0.016**
- k = 7 → p_min = 0.008

So **≥6 pairs** to be able to clear p < 0.05 at all, more for margin. Decide k **before** starting; document the calculation.

## 10. Protocol deviations & amendments

- Any deviation logged with date, reason, effect on analysis.
- Amendments after registration are permitted but must be timestamped as amendments (never silent edits); the original stays frozen.

## 11. Ethics & oversight

- Self-experimentation on a single consenting adult (yourself) does not require IRB in the US — **but Cohort 2 (any other human) does**, and the administration route requires physician supervision and pharmacy-certified sterility regardless. Record the physician of record and the compounding pharmacy here.
- Data sharing: CC-BY-4.0 open dataset on completion, as promised, with PII removed.

## 12. Registration record

- OSF project URL: _____
- Frozen timestamp / DOI: _____
- Git commit SHA of this document at registration: _____
