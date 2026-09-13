# Pod Output Bench Test — Delivery Accuracy Characterization

**Version:** 0.1 · **Date:** _____
**Purpose:** measure what an OmniPod *actually* dispenses at the intended ultra-low flow rate, on the bench, so the protocol isn't built on an unverified delivery assumption. This is the single highest-leverage test to run **first** — if the pump can't meter accurately at your target rate, the whole "continuous steady-state" thesis needs rethinking before anything else.

> **This is a bench/engineering test only.** It uses a **benign surrogate fluid** (distilled water, or a viscosity-matched inert surrogate) dispensed **into a container on a balance** — **never into a body, and never using the actual compound.** Nothing here involves administration. Do not substitute the study drug into this procedure.

---

## 1. What we're characterizing

At the site's stated 0.012 mL/hr, you're ~an order of magnitude below insulin basal norms, and the pod delivers in discrete pulses (nominal ~0.05 U ≈ 0.5 µL increments). So the real questions are:

1. **Running accuracy** — does mean delivered volume over time match commanded?
2. **Pulsatility** — what's the actual inter-pulse interval and per-pulse volume? "Continuous" may in fact be widely-spaced micro-boluses, which undermines the steady-state rationale.
3. **Start-up delay** — how long until steady delivery after activation.
4. **Minimum reliable increment** — the smallest volume the pod delivers repeatably.
5. **Stability over pod life** (7-day cycle) — does the rate drift.

## 2. Standard to follow

Use the infusion-pump accuracy methodology from **IEC 60601-2-24** (the recognized standard for infusion device delivery accuracy), specifically the **gravimetric method** and **trumpet-curve** analysis. This is exactly the method manufacturers and metrology labs use; adopting it makes your numbers credible and comparable.

## 3. Equipment

| Item | Spec / note |
|------|-------------|
| Analytical balance | Readability **0.01 mg (0.1 mg minimum)**; capacity ≥ 50 g. At 0.5 µL pulses you're weighing ~0.5 mg events — you need the resolution. |
| Collection vessel | Small tared beaker/vial on the pan. |
| **Evaporation trap** | Layer of light mineral oil over the water surface, **or** a sealed/humidified enclosure. At these volumes evaporation dominates the signal if uncontrolled — this is the #1 error source. |
| Evaporation blank | Identical vessel, no delivery, weighed in parallel to subtract background evaporation. |
| Balance data logger | Serial/USB capture to CSV at fixed interval (e.g. every 10–30 s). Manual reads won't resolve pulses. |
| Thermal control | Run at **~32 °C (skin temp)** for the representative case, plus room-temp reference. A thermostatic enclosure or water-bath jacket around the pod. |
| Surrogate fluid | Distilled/deionized water (known density). If the final formulation's viscosity ≠ water, also run a **viscosity-matched inert surrogate** (e.g. glycerol/water blend tuned to the target cP) — **not the drug**. |
| Vibration isolation | Balance on a stable bench away from HVAC/airflow; draft shield closed. |

## 4. Method

1. **Density reference:** measure or look up surrogate density ρ at test temperature. Volume = mass / ρ. Record ρ.
2. **Setup:** pod primed per normal, delivery line into the tared vessel; oil layer applied; enclosure at target temp; balance zeroed; logger started.
3. **Blank run:** log the evaporation blank in parallel for the full duration; its slope = background to subtract.
4. **Program** the pod to the target rate via your control app (AAPS). Record the commanded rate.
5. **Capture** continuously for:
   - **Start-up run:** first 2–6 h at high logging cadence (resolve start-up delay + first pulses).
   - **24 h running-accuracy run** at target rate.
   - **Full pod-life run (up to 7 days)** for drift, at least once.
6. **Replicates:** **n ≥ 3 pods** minimum (pod-to-pod variance is real); more is better. Record lot numbers.
7. Convert logged mass → volume (density-corrected), subtract blank.

## 5. Analysis / metrics

- **Overall percentage error:** (delivered − commanded) / commanded × 100, per run.
- **Trumpet curve (per IEC 60601-2-24):** compute max and min percentage flow deviation over sliding observation windows (e.g. 2, 5, 11, 19, 31 min); plot deviation vs window length. Short windows expose pulsatility; long windows show mean accuracy. This is the key deliverable.
- **Start-up delay:** time from command to first delivered pulse and to steady rate.
- **Pulse structure:** inter-pulse interval distribution and per-pulse volume (from the step pattern in the mass trace).
- **Minimum reliable increment:** smallest commanded amount reproducibly delivered (step-down series).
- **Drift:** rate vs pod-age over the 7-day run.
- Report mean ± SD across pods for each, with the trumpet plot.

## 6. Acceptance criteria (set BEFORE running)

Pre-specify pass/fail so this feeds the feasibility tier of the pre-registration, e.g.:
- Mean running accuracy within **±___%** of commanded over 24 h.
- Trumpet deviation at the clinically relevant window ≤ **___%**.
- Inter-pulse interval ≤ **___ min** (define what "continuous enough" means for your PK argument — tie this number to the plasma half-life: if inter-pulse interval ≪ half-life, pulsatility is smoothed out in plasma; if comparable, it isn't).
- Rate drift over pod life ≤ **___%**.

If it fails: the honest options are a different delivery device, a higher concentration/higher flow operating point, or revising the "continuous" claim — decide that on the bench, not mid-protocol.

## 7. Error sources to control (checklist)

- [ ] Evaporation (oil layer + parallel blank) — dominant at these volumes
- [ ] Air draft / vibration (draft shield, stable bench)
- [ ] Temperature drift (thermostatic enclosure, logged temp)
- [ ] Density assumption (measure ρ at temp)
- [ ] Balance drift (periodic re-zero / calibration mass check)
- [ ] Surrogate viscosity ≠ final fluid (run viscosity-matched surrogate)
- [ ] Bubbles in line (visual check; discard runs with visible air)

## 8. Output

A short bench-test report: setup photos, trumpet curves, accuracy table, pulse analysis, pass/fail vs §6, committed under `study-protocol/bench-test-results/`. Reference its accuracy numbers from the pre-registration feasibility section.
