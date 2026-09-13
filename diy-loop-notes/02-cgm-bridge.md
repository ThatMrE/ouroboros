# 2. CGM Bridge Setup

> Not medical advice. Follow the official docs for your build:
> https://androidaps.readthedocs.io/ — summary only.

AAPS never talks to the sensor directly. A collector app reads the transmitter and **hands** BG to AAPS.

## Two delivery channels

- **Local broadcast** — a collector on the same phone (xDrip+, Juggluco, or a patched Dexcom app)
  pushes readings to AAPS over Android intents. **Preferred:** no internet, minimal lag, robust.
- **Nightscout (NSClient) bridge** — AAPS pulls BG from your Nightscout site. Works, but adds latency
  and a hard internet dependency in the dosing loop. **Fallback only, never the sole source.**

## Pick the collector by sensor

| Sensor | Best collector | Notes |
|--------|----------------|-------|
| Dexcom G6/G7 | patched Dexcom app ("BYODA") or xDrip+ | native app smoothest; xDrip+ = more control |
| Libre 2 | xDrip+ or Juggluco | BLE direct to phone |
| Libre 3 | Juggluco (most reliable) or xDrip+ | |
| Older Dexcom / MDT | xDrip+ | |

## Path A — xDrip+ → AAPS (the workhorse)

1. Install **xDrip+** (its GitHub releases; not Play Store). Get it collecting BG and showing **live
   values** before touching AAPS.
2. **xDrip+ → Settings → Inter-app settings:**
   - **Broadcast Service API / Local Broadcast** → **ON**
   - **Identify Receiver** → `info.nightscout.androidaps`
     (if you built a custom applicationId, use **that exact string** — the #1 reason data doesn't arrive)
   - **Compatible Broadcast** → ON
3. **AAPS → Config Builder → BG Source → xDrip+.** Enable.
4. Confirm BG dots appear on the AAPS graph within ~5 min, matching xDrip+.

## Path B — Dexcom native app (BYODA) → AAPS

1. Build/install the patched Dexcom G6/G7 app (same self-sign idea as AAPS).
2. **AAPS → Config Builder → BG Source → Dexcom G6/G7 (native).**
3. Grant the Dexcom app permission to send values when prompted. Start the sensor in the Dexcom app;
   confirm readings flow into AAPS.
   - Smoothest UX + best warm-up handling; downside is rebuilding when Dexcom updates.

## Path C — Juggluco (esp. Libre 3) → AAPS

1. Install **Juggluco**, start the Libre sensor in it, confirm live values.
2. Juggluco → enable **xDrip+ broadcast** (it emulates the same local broadcast).
3. **AAPS → BG Source → xDrip+** (yes, xDrip+ — Juggluco impersonates it).

## Path D — Nightscout bridge (fallback only)

1. **AAPS → Config Builder → BG Source → NSClient BG.**
2. Configure the **NSClient / NSClientV3** plugin with your Nightscout URL + API secret/token.
3. Your collector uploads to Nightscout; AAPS reads it down.
   - Only if you can't run a local collector. Never the sole source for closed loop.

## The things that actually break it

- **Wrong package name in "Identify Receiver."** Custom applicationId must match exactly, or broadcasts
  vanish silently.
- **Battery optimization.** Android kills the collector/AAPS in the background and BG stops. Set **both**
  apps to "Don't optimize / Unrestricted," lock them in recents. Some OEMs (Xiaomi, Huawei, Samsung)
  need autostart/protected-app toggles too. **Most common cause of a loop going quiet overnight.**
- **Two collectors fighting** over one transmitter — pick one owner.
- **AAPS won't loop on stale/absent data** by design. That's correct behavior — fix the collector.
- **Verify agreement** with a fingerstick during warm-up and after any sensor change before trusting SMBs.

**Get the collector rock-solid on its own for a day before letting AAPS act on it.** A flaky bridge is
worse than no loop.
