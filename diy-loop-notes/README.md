# AndroidAPS + Omnipod DASH — DIY Loop Setup Notes

Personal, **unofficial** reference notes for setting up [AndroidAPS](https://github.com/nightscout/AndroidAPS)
(AAPS) with an **Omnipod DASH** pod for DIY type-1 diabetes closed-loop ("looping").

These notes summarize the setup path and the safety-critical settings in one place. They are a
convenience index, **not** a source of truth. The official documentation is the source of truth and
is version-specific — always follow it for your build:

- **AndroidAPS docs:** https://androidaps.readthedocs.io/
- **OpenAPS docs (reference implementation / algorithm background):** https://openaps.readthedocs.io/

---

## ⚠️ Read this first — safety & medical disclaimer

- **This is not medical advice.** It is a personal summary of publicly documented DIY looping setup.
- **DIY looping is not an approved medical device.** You take on all responsibility for it.
- **All dosing numbers are personal.** Basal rates, insulin-to-carb ratios (IC), insulin sensitivity
  factors (ISF), DIA, and every safety cap must come from — or be reviewed with — **your own
  clinician** (endocrinologist / diabetes care team). Numbers safe for one person are dangerous for
  another.
- **Keep a manual backup** (insulin pens + fast carbs) available at all times.
- **Do not skip the AAPS Objectives.** They are the built-in safety-staging mechanism.
- **Tell your care team.** The DIY community norm is transparency with your clinician, not hiding it.

If anything in these notes conflicts with the official docs or your clinician, **they win.**

---

## What this covers (and what it doesn't)

**Covers:** AndroidAPS with **Omnipod DASH** (direct BLE, no radio bridge needed).

**Does not cover:** Omnipod 5. Omnipod 5 is a proprietary hybrid closed-loop system; its command
protocol has not been publicly reverse-engineered and **no DIY system (AAPS/OpenAPS/Loop) drives it.**
If DIY looping is the goal, use a pod with a supported driver:

| Pump | DIY support | How |
|------|-------------|-----|
| Omnipod **DASH** | ✅ | Direct BLE, no extra hardware |
| Omnipod **Eros** | ✅ | Needs RileyLink / OrangeLink (433 MHz) |
| Omnipod **5** | ❌ | Not reverse-engineered; not supported |

---

## Contents

1. [Build & pair (AAPS + DASH)](01-build-and-pair.md)
2. [CGM bridge setup](02-cgm-bridge.md)
3. [Objectives unlock sequence](03-objectives.md)
4. [Safety caps — Max IOB, Max bolus, DIA, Max basal](04-safety-caps.md)

## The whole chain, in order

```
Build AAPS from source  →  get CGM data flowing  →  set safety caps
       →  pair DASH pod  →  work through Objectives  →  open loop
       →  constrained closed loop  →  full closed loop + SMB
```

Do not shortcut it. Each stage validates the one before it.
