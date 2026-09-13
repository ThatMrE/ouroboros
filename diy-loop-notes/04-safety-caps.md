# 4. Safety Caps — Max IOB, Max Bolus, DIA, Max Basal

> **Not medical advice.** These are the hard ceilings on what the loop can do. Every value here is
> **personal** and must come from — or be reviewed with — **your clinician.** Follow the official docs
> for your build: https://androidaps.readthedocs.io/

## Two things to understand first

1. **These scale off your total daily dose (TDD), basal rates, and normal meal boluses.** Values safe for
   a 20 U/day adult are dangerous for a child on 8 U/day and useless for someone on 80. **Review with your
   endocrinologist.**
2. **AAPS enforces its own hardcoded maxima on top of your profile.** Your settings can only make it
   *more* conservative than the app's built-in limits, never less. Intentional.

## DIA — Duration of Insulin Action

- **AAPS enforces a 5-hour floor.** You cannot set DIA below 5 h, even if an old pump used 3–4 h. The
  oref algorithms model a long insulin tail.
- **Start at 5 h** for rapid analogs (NovoRapid/Novolog, Humalog, Apidra). Fiasp/Lyumjev are faster at
  the front but AAPS still wants ≥5 h — leave it at 5.
- DIA is **not** an early tuning knob. Set 5 h and tune basal/IC/ISF instead.

## Max bolus

- The largest single bolus AAPS will ever deliver or let you enter — a fat-finger guard.
- **Set it just above your largest routine meal bolus.** Biggest normal meal ~8 U → set ~10. **Not** 25
  "just in case" — the point is that a slip can't blow past your real needs.

## Max IOB — the one that matters most for closed loop

Ceiling on how much insulin-on-board the **loop** builds before it stops adding more.

- **Objective 5 forces Max IOB = 0.** At 0 the loop can only ever *reduce* basal (low-glucose-suspend).
  Safest possible closed loop; live here for a while.
- **SMB vs AMA count IOB differently.** In **SMB**, Max IOB **includes bolus IOB** (meal boluses) — so
  the number must be big enough that a normal meal doesn't slam the ceiling, but that also authorizes more
  total insulin. In older **AMA** it counts only basal-derived IOB above profile. Same number, very
  different meaning — know which mode you're in.
- **Starting logic once you leave 0 (Obj 6+):** raise slowly. A cautious starting point is around the
  size of a single typical meal bolus, then increase in small steps only after days of unremarkable
  looping. Use the docs' version-specific suggested value / worked example based on your TDD.

## Max basal (the temp-basal ceiling)

Set as multipliers under safety preferences:

- **Max basal as multiple of profile basal** — commonly start ~**3–4×**. Caps how hard one temp basal
  runs above scheduled rate.
- **Max daily basal multiplier** — commonly ~**3×** average daily basal.
- Start on the low end (3×). Raise later; no rush.

## The rule that ties it together

Set these **before** enabling closed loop, so the **worst case is tolerable**: if every ceiling were hit
at once, the total insulin should be an amount you'd be comfortable having on board — not a scary one. The
Objective ladder then lets the loop approach these caps gradually.

**If the loop is constantly pinned against Max IOB, your profile (basal/IC/ISF) is probably wrong — fix
the profile, don't just raise the ceiling.**

Write your proposed numbers down and run them past your endo or diabetes educator before flipping to
closed loop. This is exactly the layer where a data-entry error becomes a real hypo.
