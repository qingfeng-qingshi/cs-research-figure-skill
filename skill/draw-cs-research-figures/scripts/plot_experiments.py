#!/usr/bin/env python3
import argparse
import math
import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

INK = "#203040"
MUTED = "#5F7182"
GRID = "#DCE4EA"
FOCAL = "#2F6F9F"
SERIES_COLORS = ["#3978A8", "#E07A3F", "#4A9A53", "#C74448", "#8064A2", "#4AA6A8"]
MARKERS = ["o", "s", "D", "X", "^", "P"]
BASELINES = ["#78A89C", "#D8A24A", "#8E7DB5", "#C87864", "#7095B5", "#A0A8B0"]
ABLATIONS = ["#D98D62", "#67A6A3", "#9A82BA", "#D0A44C", "#7898B4"]

def wrap(value, width=22):
    return chr(10).join(textwrap.wrap(str(value), width=width, break_long_words=False)) or str(value)

def title_two_lines(value, limit=52):
    value = " ".join(str(value).split())
    if len(value) <= limit:
        return value
    words = value.split()
    candidates = []
    for i in range(1, len(words)):
        left, right = " ".join(words[:i]), " ".join(words[i:])
        candidates.append((max(len(left), len(right)), abs(len(left)-len(right)), left, right))
    _, _, left, right = min(candidates)
    return left + chr(10) + right

def load(path):
    df = pd.read_csv(path)
    if "value" not in df.columns:
        raise ValueError("missing column: value")
    df["value"] = pd.to_numeric(df["value"])
    return df

def is_focal(name):
    name = str(name).lower()
    return any(key in name for key in ("proposed", "ours", "full model", "our method"))

def style_axis(ax):
    ax.set_facecolor("#FFFFFF")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#93A5B4")
    ax.spines["bottom"].set_color("#93A5B4")
    ax.tick_params(colors=MUTED, labelsize=9, length=0, pad=6, labelrotation=0)
    ax.grid(color=GRID, linewidth=0.75, alpha=0.9)
    ax.set_axisbelow(True)

def comparison(df, ax):
    required = {"variant", "metric"}
    if not required.issubset(df.columns):
        raise ValueError("comparison needs variant, metric, value")
    metrics = list(dict.fromkeys(df["metric"]))
    variants = list(dict.fromkeys(df["variant"]))
    if len(metrics) == 1:
        metric = metrics[0]
        part = df[df.metric == metric].sort_values("value")
        colors, index = [], 0
        for name in part["variant"]:
            if is_focal(name):
                colors.append(FOCAL)
            else:
                colors.append(BASELINES[index % len(BASELINES)])
                index += 1
        bars = ax.barh([wrap(x, 24) for x in part["variant"]], part["value"], color=colors, height=0.62, edgecolor="#FFFFFF", linewidth=0.8)
        xmax = float(part["value"].max())
        ax.set_xlim(0, xmax * 1.14)
        ax.bar_label(bars, labels=[f"{v:.2f}" for v in part["value"]], padding=6, fontsize=9.5, color=INK)
        ax.set_xlabel(metric, color=INK, fontsize=10.5, labelpad=9)
        ax.grid(axis="x")
        ax.grid(axis="y", visible=False)
    else:
        x = np.arange(len(variants))
        width = 0.76 / len(metrics)
        for i, metric in enumerate(metrics):
            vals = df[df.metric == metric].set_index("variant").reindex(variants)["value"]
            ax.bar(x + (i-(len(metrics)-1)/2)*width, vals, width, label=metric, color=BASELINES[i % len(BASELINES)], edgecolor="#FFFFFF", linewidth=0.6)
        ax.set_xticks(x, [wrap(v, 16) for v in variants], rotation=0, ha="center")
        ax.legend(frameon=False, ncol=min(3, len(metrics)), fontsize=8.5, loc="upper left")
        ax.grid(axis="y")
        ax.grid(axis="x", visible=False)

def discrete_ablation(df, ax):
    required = {"variant", "metric"}
    if not required.issubset(df.columns):
        raise ValueError("discrete ablation needs variant, metric, value")
    metrics = list(dict.fromkeys(df["metric"]))
    if len(metrics) != 1:
        raise ValueError("discrete ablation expects one metric per figure")
    metric = metrics[0]
    part = df[df.metric == metric]
    variants, values = list(part["variant"]), list(part["value"])
    full = values[0]
    colors = [FOCAL] + [ABLATIONS[i % len(ABLATIONS)] for i in range(len(values)-1)]
    bars = ax.barh([wrap(v, 27) for v in variants], values, color=colors, height=0.60, edgecolor="#FFFFFF", linewidth=0.8)
    ax.invert_yaxis()
    ax.set_xlim(0, max(values)*1.20)
    labels = [f"{values[0]:.2f}"] + [f"{v:.2f}  ({v-full:+.2f})" for v in values[1:]]
    ax.bar_label(bars, labels=labels, padding=6, fontsize=9.5, color=INK)
    ax.set_xlabel(metric, color=INK, fontsize=10.5, labelpad=9)
    ax.grid(axis="x")
    ax.grid(axis="y", visible=False)

def curve_ablation(df, title):
    required = {"x", "series", "value"}
    if not required.issubset(df.columns):
        raise ValueError("curve ablation needs x, series, value; optional panel, metric, x_label, panel_title")
    df = df.copy()
    df["x"] = pd.to_numeric(df["x"])
    panels = list(dict.fromkeys(df["panel"])) if "panel" in df.columns else ["Ablation"]
    cols = min(2, len(panels))
    rows = math.ceil(len(panels)/cols)
    fig, axes = plt.subplots(rows, cols, figsize=(5.2*cols, 3.8*rows), squeeze=False, constrained_layout=True, sharey=True)
    all_values = df["value"].dropna()
    low, high = float(all_values.min()), float(all_values.max())
    pad = max((high-low)*0.12, 0.01)
    for index, panel in enumerate(panels):
        ax = axes[index//cols][index%cols]
        style_axis(ax)
        part = df[df["panel"] == panel] if "panel" in df.columns else df
        series_values = list(dict.fromkeys(part["series"]))
        for i, series in enumerate(series_values):
            line = part[part["series"] == series].sort_values("x")
            ax.plot(line["x"], line["value"], color=SERIES_COLORS[i % len(SERIES_COLORS)], marker=MARKERS[i % len(MARKERS)], markersize=5.2, linewidth=1.8, label=str(series))
        metric = str(part["metric"].iloc[0]) if "metric" in part.columns else "Performance"
        xlabel = str(part["x_label"].iloc[0]) if "x_label" in part.columns else "Ordered setting"
        panel_title = str(part["panel_title"].iloc[0]) if "panel_title" in part.columns else str(panel)
        ax.set_title(wrap(panel_title, 34), fontsize=11, fontweight="semibold", color=INK, pad=9)
        ax.set_xlabel(xlabel, fontsize=9.5, color=INK)
        ax.set_ylabel(metric, fontsize=9.5, color=INK)
        ax.set_ylim(low-pad, high+pad)
        ax.grid(True)
        ax.legend(frameon=False, fontsize=8.2, ncol=min(3, len(series_values)), loc="best", handlelength=2.0, columnspacing=1.0)
    for index in range(len(panels), rows*cols):
        axes[index//cols][index%cols].set_visible(False)
    fig.suptitle(title_two_lines(title), x=0.5, ha="center", fontsize=15, fontweight="semibold", color=INK)
    fig.patch.set_facecolor("#FFFFFF")
    return fig

def save(fig, out_prefix):
    prefix = Path(out_prefix)
    prefix.parent.mkdir(parents=True, exist_ok=True)
    for ext in ("svg", "pdf", "png"):
        fig.savefig(prefix.with_suffix("." + ext), dpi=260, bbox_inches="tight", facecolor="#FFFFFF")
    print("Wrote", ", ".join(str(prefix.with_suffix("." + ext)) for ext in ("svg", "pdf", "png")))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--kind", choices=["comparison", "ablation"], required=True)
    parser.add_argument("--ablation-mode", choices=["auto", "curve", "discrete"], default="auto")
    parser.add_argument("--title")
    parser.add_argument("--out-prefix", required=True)
    args = parser.parse_args()
    df = load(args.input)
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,"text.color":INK,"axes.labelcolor":INK,"axes.titlecolor":INK,"svg.fonttype":"none","pdf.fonttype":42})
    mode = args.ablation_mode
    if args.kind == "ablation" and mode == "auto":
        mode = "curve" if {"x", "series"}.issubset(df.columns) else "discrete"
    default_title = "Comparison with Baselines" if args.kind == "comparison" else "Ablation Study"
    title = args.title or default_title
    if args.kind == "ablation" and mode == "curve":
        fig = curve_ablation(df, title)
    else:
        rows = max(4, len(df["variant"].unique()))
        fig, ax = plt.subplots(figsize=(8.2, max(3.8, 0.68*rows+1.5)), constrained_layout=True)
        style_axis(ax)
        comparison(df, ax) if args.kind == "comparison" else discrete_ablation(df, ax)
        fig.suptitle(title_two_lines(title), x=0.5, ha="center", fontsize=15, fontweight="semibold", color=INK)
        fig.patch.set_facecolor("#FFFFFF")
    save(fig, args.out_prefix)

if __name__ == "__main__":
    main()
