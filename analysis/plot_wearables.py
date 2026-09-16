"""Wearable time-series plotter for the N-of-1 pilot.

Small-multiples (one panel per metric, shared date axis) — never a dual-axis chart.
Optional block shading marks ACTIVE periods (tint + light hatch, so it reads without
color); placebo periods are left unshaded. Optional rolling-mean trend overlay.

Statistics/plotting only — no device or dosing logic. Block labels are opaque
(active/placebo mapping stays sealed until analysis lock; see allocation.py).

Inputs
------
wearables CSV: a `date` column (ISO YYYY-MM-DD) + one column per metric.
blocks CSV (optional): `start,end,arm` rows; rows with arm=="active" are shaded.

Usage
-----
    python plot_wearables.py --data ../data/wearables_daily.csv \
        --metrics hrv_rmssd_ms resting_hr_bpm sleep_efficiency_pct \
        --blocks ../data/blocks.csv --roll 7 --out ../derived/wearables
"""
from __future__ import annotations

import argparse
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

INK = "#1A1A1A"
MUTED = "#8A8A8A"
GRID = "#E4E4E4"
LINE = "#3B6FE0"      # the metric line (single hue)
TREND = "#B0392B"     # rolling-mean overlay
ACTIVE_FILL = "#3B6FE0"  # active-band tint (drawn at low alpha) + hatch


def load_blocks(path: str | None) -> pd.DataFrame | None:
    if not path:
        return None
    b = pd.read_csv(path, parse_dates=["start", "end"])
    return b


def plot_wearables(
    df: pd.DataFrame,
    metrics: list[str],
    out: str,
    blocks: pd.DataFrame | None = None,
    roll: int = 0,
):
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    missing = [m for m in metrics if m not in df.columns]
    if missing:
        raise ValueError(f"metrics not in data: {missing}")

    n = len(metrics)
    fig, axes = plt.subplots(n, 1, figsize=(9, 2.1 * n + 0.6), dpi=160, sharex=True)
    if n == 1:
        axes = [axes]

    shaded_label_used = False
    for ax, metric in zip(axes, metrics):
        # active-period shading (tint + hatch: not color-alone)
        if blocks is not None:
            for _, blk in blocks.iterrows():
                if str(blk.get("arm", "")).lower() == "active":
                    ax.axvspan(
                        blk["start"], blk["end"],
                        facecolor=ACTIVE_FILL, alpha=0.08, hatch="////",
                        edgecolor=ACTIVE_FILL, linewidth=0, zorder=0,
                        label=None if shaded_label_used else "active period",
                    )
                    shaded_label_used = True

        s = df[["date", metric]].dropna()
        ax.plot(s["date"], s[metric], color=LINE, lw=1.6, marker="o", markersize=3,
                zorder=3)
        if roll and roll > 1:
            tr = s.set_index("date")[metric].rolling(roll, min_periods=max(2, roll // 2)).mean()
            ax.plot(tr.index, tr.values, color=TREND, lw=2, zorder=4,
                    label=f"{roll}-day mean")

        ax.set_title(metric, fontsize=10.5, color=INK, loc="left", pad=4, weight="bold")
        ax.grid(axis="y", color=GRID, lw=0.8, zorder=0)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        for sp in ("left", "bottom"):
            ax.spines[sp].set_color(MUTED)
        ax.tick_params(colors=MUTED, labelsize=8.5, length=0)

    axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    fig.autofmt_xdate(rotation=0, ha="center")

    # single combined legend (active band + trend), only if something to show
    handles, labels = [], []
    for ax in axes:
        h, l = ax.get_legend_handles_labels()
        for hi, li in zip(h, l):
            if li not in labels:
                handles.append(hi); labels.append(li)
    if handles:
        fig.legend(handles, labels, loc="upper right", frameon=False,
                   fontsize=8.5, bbox_to_anchor=(0.99, 1.0))

    fig.suptitle("Wearable time series", x=0.02, ha="left", fontsize=12,
                 color=INK, weight="bold")
    fig.subplots_adjust(left=0.10, right=0.97, top=0.90, bottom=0.10, hspace=0.35)

    png, svg = f"{out}.png", f"{out}.svg"
    fig.savefig(png)
    fig.savefig(svg)
    plt.close(fig)
    return png, svg


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data", required=True)
    ap.add_argument("--metrics", nargs="+", required=True)
    ap.add_argument("--blocks", default=None, help="optional CSV: start,end,arm")
    ap.add_argument("--roll", type=int, default=0, help="rolling-mean window (days); 0 = off")
    ap.add_argument("--out", default="../derived/wearables")
    args = ap.parse_args()

    df = pd.read_csv(args.data)
    blocks = load_blocks(args.blocks)
    png, svg = plot_wearables(df, args.metrics, args.out, blocks=blocks, roll=args.roll)
    print(f"[plot_wearables] wrote {png} and {svg}  ({len(args.metrics)} metrics)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
