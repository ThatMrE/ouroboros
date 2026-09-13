"""Forest plot for the N-of-1 biomarker effect panel.

Renders one row per marker: point estimate + confidence interval, with a vertical
reference line at the null. Secondary (non-color) encoding: a FILLED marker means
the CI excludes the null (notable), an OPEN marker means it includes null — so the
signal survives grayscale / color-vision deficiency. Single restrained hue; direct
value labels; recessive axes. Static report figure (PNG + SVG).

Statistics/plotting only — no device or dosing logic.

Input CSV columns:  label,point,ci_low,ci_high[,direction]
    direction (optional): "up"/"down" — the pre-registered hypothesized direction,
    drawn as a small caret next to the label for at-a-glance concordance.

Usage
-----
    python forest_plot.py --data ../derived/effects.csv --out ../derived/forest \
        --null 0 --xlabel "Effect (active - placebo)" --title "Exploratory panel"
    # ratio-scale (e.g. log response ratio exp'd): --null 1 --logx
"""
from __future__ import annotations

import argparse
import csv
import sys

import matplotlib

matplotlib.use("Agg")  # headless
import matplotlib.pyplot as plt

# --- restrained palette (single hue + ink/gray tokens; no rainbow) ---
INK = "#1A1A1A"
MUTED = "#8A8A8A"
GRID = "#E4E4E4"
ACCENT = "#3B6FE0"     # single series hue
NULLLINE = "#B0392B"   # reference line, distinct from the series hue


def read_estimates(path: str) -> list[dict]:
    with open(path, newline="") as fh:
        rows = list(csv.DictReader(fh))
    out = []
    for r in rows:
        out.append(
            {
                "label": r["label"],
                "point": float(r["point"]),
                "ci_low": float(r["ci_low"]),
                "ci_high": float(r["ci_high"]),
                "direction": (r.get("direction") or "").strip().lower(),
            }
        )
    if not out:
        raise ValueError("no rows in estimates CSV")
    return out


def forest_plot(
    estimates: list[dict],
    out: str,
    null: float = 0.0,
    xlabel: str = "Effect (active − placebo)",
    title: str = "Biomarker effect panel",
    logx: bool = False,
    sort: bool = True,
):
    est = list(estimates)
    if sort:
        est = sorted(est, key=lambda e: e["point"])

    labels = [e["label"] for e in est]
    y = list(range(len(est)))

    fig_h = max(2.4, 0.5 * len(est) + 1.4)
    fig, ax = plt.subplots(figsize=(8.2, fig_h), dpi=160)

    # null reference line
    ax.axvline(null, color=NULLLINE, lw=1.4, zorder=1)

    for yi, e in zip(y, est):
        excludes_null = (e["ci_low"] > null) or (e["ci_high"] < null)
        # CI whisker
        ax.plot([e["ci_low"], e["ci_high"]], [yi, yi], color=ACCENT, lw=2, zorder=2,
                solid_capstyle="round")
        # point: filled if CI excludes null, open otherwise (secondary, non-color, encoding)
        ax.plot(
            [e["point"]], [yi],
            marker="o", markersize=8,
            markerfacecolor=ACCENT if excludes_null else "white",
            markeredgecolor=ACCENT, markeredgewidth=1.8, zorder=3,
        )
        # direct value label — aligned right-hand column (never overlaps the plot)
        ax.annotate(
            f"{e['point']:.3g}  [{e['ci_low']:.3g}, {e['ci_high']:.3g}]",
            xy=(1.03, yi), xycoords=("axes fraction", "data"),
            va="center", ha="left", fontsize=8.5, color=MUTED,
            annotation_clip=False,
        )

    ax.set_yticks(y)
    # hypothesis-direction caret prepended to the label when provided
    ylabels = []
    for e in est:
        caret = {"up": "▲ ", "down": "▼ "}.get(e["direction"], "")
        ylabels.append(caret + e["label"])
    ax.set_yticklabels(ylabels, fontsize=9.5, color=INK)

    ax.set_xlabel(xlabel, fontsize=9.5, color=INK)
    if logx:
        ax.set_xscale("log")
    ax.set_title(title, fontsize=11.5, color=INK, loc="left", pad=10, weight="bold")

    # recessive axes/grid
    ax.grid(axis="x", color=GRID, lw=0.8, zorder=0)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(MUTED)
    ax.tick_params(colors=MUTED, length=0)
    ax.margins(y=0.08)

    # give the value labels room (right-hand value column)
    fig.subplots_adjust(left=0.28, right=0.72, top=0.90, bottom=0.16)

    png, svg = f"{out}.png", f"{out}.svg"
    fig.savefig(png)
    fig.savefig(svg)
    plt.close(fig)
    return png, svg


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data", required=True, help="CSV: label,point,ci_low,ci_high[,direction]")
    ap.add_argument("--out", default="../derived/forest", help="output path stem (.png/.svg added)")
    ap.add_argument("--null", type=float, default=0.0, help="reference line (0 for diffs, 1 for ratios)")
    ap.add_argument("--xlabel", default="Effect (active − placebo)")
    ap.add_argument("--title", default="Biomarker effect panel")
    ap.add_argument("--logx", action="store_true")
    ap.add_argument("--no-sort", dest="sort", action="store_false")
    args = ap.parse_args()

    est = read_estimates(args.data)
    png, svg = forest_plot(est, args.out, null=args.null, xlabel=args.xlabel,
                           title=args.title, logx=args.logx, sort=args.sort)
    print(f"[forest_plot] wrote {png} and {svg}  ({len(est)} markers)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
