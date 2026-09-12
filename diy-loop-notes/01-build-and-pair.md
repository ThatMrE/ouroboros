# 1. Build & Pair — AndroidAPS + Omnipod DASH

> Not medical advice. Follow the official docs for your build version:
> https://androidaps.readthedocs.io/ — this is a summary only.

## Naming, so it's clear

- **OpenAPS** = the reference implementation + algorithm docs. Runs on a separate "rig," not your phone.
- **AndroidAPS (AAPS)** = the Android app that implements the same `oref0/oref1` algorithms. **This is
  what you want for phone-based looping.** Its docs live at androidaps.readthedocs.io.

Omnipod DASH talks **Bluetooth LE directly** to the phone — **no RileyLink/OrangeLink** (that's Eros only).

## 0. Prerequisites

- Android phone, Android 9+. A **dedicated/spare phone** is the community norm so reboots/updates don't
  interrupt looping.
- **Omnipod DASH pods.** A PDM is not required — AAPS becomes the controller.
- A **CGM AAPS can read** (see [CGM bridge](02-cgm-bridge.md)).
- A computer with **Android Studio** for the build.
- Your **basal / IC / ISF** numbers from your clinician. Do not invent these.
- **Backup insulin (pens) + fast carbs**, always.

## 1. Build it yourself (there is no Play Store build)

Self-signing is deliberate — it prevents silent updates from pushing code into a medical loop.

```bash
git clone https://github.com/nightscout/AndroidAPS.git
cd AndroidAPS
git checkout master   # latest stable; avoid 'dev' unless you know why
```

In **Android Studio**:

1. Open the project, let Gradle sync.
2. **Build → Generate Signed Bundle/APK → APK → Create new keystore.**
   Save the `.jks` file and passwords somewhere you will **not** lose them — you need the *same* key for
   every future update, or you have to uninstall (losing settings/history).
3. Build the `full` variant, `release`. Install the APK on the phone.

Follow the official **"Building APK"** section for current Gradle/JDK versions — those drift.

## 2. First run — AAPS ships locked

You **cannot** enable closed loop until you complete the **Objectives** (see [03](03-objectives.md)).
Don't look for a bypass; that staging is the point.

## 3. Configure BEFORE pairing a pod

In **Config Builder**, set up in this order:

1. **CGM source (BG Source)** → verify live values on the graph. ([details](02-cgm-bridge.md))
2. **Profile** → DIA, IC, ISF, basal, targets from your clinician. Activate it.
3. **Insulin plugin** → the model matching your insulin (e.g. Rapid-Acting / Ultra-Rapid).
4. **APS** → the algorithm (openaps SMB is standard once unlocked).
5. **Pump** → **Omnipod DASH**.
6. **Loop** stays **off** until Objectives allow it.

## 4. Pair the DASH pod

With the DASH plugin selected, open its tab:

1. **Turn on Bluetooth.** No radio stick needed.
2. Fill the pod (min ~85 U) with the fill syringe; listen for the priming beeps.
3. **Pod management → Activate Pod.**
4. AAPS scans for the pod's BLE advertisement and bonds. If it doesn't appear: pod must be fresh
   (never activated), keep it within a few cm during pairing, toggle Bluetooth off/on if the scan hangs.
5. Follow prompts: prime → attach to body → insert cannula. AAPS reports cannula status.
6. Do a **small manual test bolus** (or verify basal delivery) before trusting it.

Replace the pod every ~72 h (up to ~80 h + grace) via **Pod management → Deactivate Pod**.

## 5. Turn on looping — gradually

Only after Objectives unlock each stage:

- **Open loop** (recommends only, you confirm) until numbers track your reality.
- **Closed loop**, then enable **SMB** last.
- Set **Max IOB / Max bolus / Max basal** conservatively first ([safety caps](04-safety-caps.md)).

## Where people actually get hurt

- **Wrong profile numbers** → the loop faithfully over/under-doses. Get them from your clinician.
- **Building `dev`/old forks** with known dosing bugs → run a tagged stable release.
- **No manual backup** → always carry pens and fast carbs.
- **Losing your keystore** → keep a backup; recovery means a reinstall.
- **Not telling your care team.**
