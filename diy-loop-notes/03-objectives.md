# 3. Objectives Unlock Sequence

> Not medical advice. Exact durations/action-counts are version-specific — see the official
> **"Objectives"** page: https://androidaps.readthedocs.io/ — summary only.

The Objectives are AAPS's built-in **staged unlock**. Each turns on more autonomy; you can't jump ahead.
Found in **Config Builder → Objectives**.

## The nine objectives

| # | Unlocks | What you actually do |
|---|---------|----------------------|
| 1 | Visualization & monitoring | Get BG flowing, pump connected, profile active; a minimum wait applies. |
| 2 | *(the exam)* | Answer multiple-choice questions on how AAPS works; wrong answers link to docs. The real knowledge gate. |
| 3 | **Open loop** | Run open loop for a period. AAPS only *recommends*; you accept/reject. |
| 4 | Verifying recommendations | Perform a number of suggested actions over a minimum window. |
| 5 | **Closed loop, Max IOB = 0** | Loop runs unattended but can **only reduce basal** (low-glucose-suspend). Safest closed loop. |
| 6 | Raising Max IOB > 0 | Tune basals/ratios, then allow the loop to add insulin via temp basals. |
| 7 | **Autosens** | Enable auto-sensitivity. |
| 8 | **SMB (Super Micro Bolus)** | Enable aggressive micro-bolus dosing — the most insulin authority. |
| 9 | Automation / advanced | Automation rules, advanced features. |

(Numbering + exact waits drift between releases. Trust the docs for your build.)

## How the gating works

- **Sequential and time-gated.** Each objective needs the previous one done, plus a **minimum duration**
  and/or **minimum number of actions**. The timers are deliberate.
- **The exam (Obj 2)** is the one to get right — covers DIA, IOB, when the loop won't dose, safety
  behavior. Hints link to docs.
- **No legitimate skip.** Editing the DB / pre-filled codes to skip ahead defeats the safety staging.
  Jumping to SMB on day one is exactly how bad settings become a real hypo.

## The path worth walking

1. **Obj 1–2** — get data solid, pass the exam.
2. **Obj 3 open loop, several days.** Do its recommendations match what you'd do manually? If consistently
   wrong, your **profile is wrong — fix basal/IC/ISF now**, before any closed loop.
3. **Obj 5 (Max IOB = 0), a good while.** Let it prove it suspends correctly on lows.
4. **Obj 6** — raise Max IOB slowly, keep watching.
5. **Obj 7 autosens, then Obj 8 SMB** only once the loop has been boring for a week or two.

**Rule that keeps it safe:** advance only when the current objective has been unremarkable. A surprising
low or a recommendation you disagree with means **stay put and fix settings**, not press on.
