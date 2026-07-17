#!/usr/bin/env python3
import argparse
import math
import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from conference_presets import PRESETS, apply_preset
from profile_results import profile_dataframe

INK, MUTED, GRID = "#203040", "#5F7182", "#DCE4EA"
FOCAL = "#2878B5"
COLORS = ["#2878B5", "#D95F59", "#4C956C", "#E5A84B", "#8064A2", "#45A6A6"]
MARKERS = ["o", "s", "D", "X", "^", "P"]


def wrap(value, width=22):
    return "\n".join(textwrap.wrap(str(value), width=width, break_long_words=False)) or str(value)


def title_two_lines(value, limit=52):
    value = " ".join(str(value).split())
    if len(value) <= limit:
        return value
    words = value.split()
    choices = [(max(len(" ".join(words[:i])), len(" ".join(words[i:]))), abs(len(" ".join(words[:i])) - len(" ".join(words[i:]))), i) for i in range(1, len(words))]
    i = min(choices)[2]
    return " ".join(words[:i]) + "\n" + " ".join(words[i:])


def load(path):
    df = pd.read_csv(path)
    if "value" not in df.columns:
        raise ValueError("missing column: value")
    df["value"] = pd.to_numeric(df["value"])
    return df


def is_focal(name):
    return any(k in str(name).lower() for k in ("proposed", "ours", "full model", "our method"))


def style_axis(ax):
    ax.set_facecolor("#FFFFFF")
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#93A5B4")
    ax.tick_params(colors=MUTED, length=0, pad=5, labelrotation=0)
    ax.grid(color=GRID, linewidth=0.7, alpha=0.9)
    ax.set_axisbelow(True)


def error_values(part):
    for name in ("error", "err", "std", "sd", "sem", "stderr"):
        if name in part.columns:
            return pd.to_numeric(part[name]).to_numpy()
    return None


def comparison_figure(df, title, figsize):
    if not {"variant", "metric"}.issubset(df.columns):
        raise ValueError("comparison needs variant, metric, value")
    metrics = list(dict.fromkeys(df["metric"]))
    variants = list(dict.fromkeys(df["variant"]))
    height = max(figsize[1], 1.5 + 0.52 * len(variants))
    fig, ax = plt.subplots(figsize=(figsize[0], height), constrained_layout=True)
    style_axis(ax)
    if len(metrics) == 1:
        part = df[df.metric == metrics[0]].sort_values("value")
        colors = [FOCAL if is_focal(v) else COLORS[(i + 1) % len(COLORS)] for i, v in enumerate(part["variant"])]
        bars = ax.barh([wrap(v, 25) for v in part["variant"]], part["value"], xerr=error_values(part),
                       color=colors, height=0.62, edgecolor="#FFFFFF", capsize=3)
        xmax = float((part["value"] + (pd.Series(error_values(part)) if error_values(part) is not None else 0)).max())
        ax.set_xlim(0, xmax * 1.14)
        ax.bar_label(bars, labels=[f"{v:.2f}" for v in part["value"]], padding=5, color=INK)
        ax.set_xlabel(str(metrics[0]))
        ax.grid(axis="x"); ax.grid(axis="y", visible=False)
    else:
        x = np.arange(len(variants)); width = 0.78 / len(metrics)
        for i, metric in enumerate(metrics):
            part = df[df.metric == metric].set_index("variant").reindex(variants)
            ax.bar(x + (i - (len(metrics)-1)/2) * width, part["value"], width,
                   yerr=error_values(part), label=metric, color=COLORS[i % len(COLORS)], capsize=2)
        ax.set_xticks(x, [wrap(v, 15) for v in variants])
        ax.legend(frameon=False, ncol=min(3, len(metrics)))
        ax.grid(axis="y"); ax.grid(axis="x", visible=False)
    fig.suptitle(title_two_lines(title), fontsize=14, fontweight="semibold", color=INK)
    return fig


def discrete_ablation_figure(df, title, figsize):
    if not {"variant", "metric"}.issubset(df.columns) or df["metric"].nunique() != 1:
        raise ValueError("discrete ablation needs variant, metric, value and one metric")
    values = df["value"].to_numpy(); labels = df["variant"].astype(str).tolist(); full = values[0]
    height = max(figsize[1], 1.5 + 0.52 * len(labels))
    fig, ax = plt.subplots(figsize=(figsize[0], height), constrained_layout=True)
    style_axis(ax)
    bars = ax.barh([wrap(v, 26) for v in labels], values,
                   color=[FOCAL] + [COLORS[(i + 1) % len(COLORS)] for i in range(len(values)-1)], height=0.6)
    ax.invert_yaxis(); ax.set_xlim(0, max(values) * 1.2)
    text = [f"{values[0]:.2f}"] + [f"{v:.2f} ({v-full:+.2f})" for v in values[1:]]
    ax.bar_label(bars, labels=text, padding=5, color=INK)
    ax.set_xlabel(str(df["metric"].iloc[0])); ax.grid(axis="x"); ax.grid(axis="y", visible=False)
    fig.suptitle(title_two_lines(title), fontsize=14, fontweight="semibold", color=INK)
    return fig


def curve_ablation_figure(df, title, figsize):
    if not {"x", "series", "value"}.issubset(df.columns):
        raise ValueError("curve ablation needs x, series, value")
    df = df.copy(); df["x"] = pd.to_numeric(df["x"])
    panels = list(dict.fromkeys(df["panel"])) if "panel" in df.columns else ["Ablation"]
    cols, rows = min(2, len(panels)), math.ceil(len(panels) / min(2, len(panels)))
    fig, axes = plt.subplots(rows, cols, figsize=(figsize[0], max(figsize[1], 2.8 * rows)), squeeze=False, constrained_layout=True, sharey=True)
    low, high = float(df.value.min()), float(df.value.max()); pad = max((high-low)*0.12, 0.01)
    for index, panel in enumerate(panels):
        ax = axes[index//cols][index%cols]; style_axis(ax)
        part = df[df.panel == panel] if "panel" in df.columns else df
        for i, series in enumerate(dict.fromkeys(part["series"])):
            line = part[part.series == series].sort_values("x")
            ax.plot(line.x, line.value, color=COLORS[i % len(COLORS)], marker=MARKERS[i % len(MARKERS)], linewidth=1.5, label=str(series))
        ax.set_title(wrap(part["panel_title"].iloc[0] if "panel_title" in part else panel, 28), fontweight="semibold")
        ax.set_xlabel(str(part["x_label"].iloc[0] if "x_label" in part else "Ordered setting"))
        ax.set_ylabel(str(part["metric"].iloc[0] if "metric" in part else "Performance")); ax.set_ylim(low-pad, high+pad)
        ax.legend(frameon=False, ncol=min(3, part.series.nunique()))
    for index in range(len(panels), rows*cols): axes[index//cols][index%cols].set_visible(False)
    fig.suptitle(title_two_lines(title), fontsize=14, fontweight="semibold", color=INK)
    return fig


def boxplot_figure(df, title, figsize):
    group = next((c for c in ("variant", "method", "model", "group") if c in df.columns), None)
    if not group: raise ValueError("boxplot needs variant/method/model/group")
    labels = list(dict.fromkeys(df[group].astype(str)))
    values = [df[df[group].astype(str) == label].value.dropna().to_numpy() for label in labels]
    fig, ax = plt.subplots(figsize=(figsize[0], max(figsize[1], 1.4 + 0.48*len(labels))), constrained_layout=True); style_axis(ax)
    bp = ax.boxplot(values, vert=False, patch_artist=True, labels=[wrap(v, 24) for v in labels], widths=0.52,
                    medianprops={"color": INK, "linewidth": 1.4}, flierprops={"marker": ""})
    for i, patch in enumerate(bp["boxes"]): patch.set(facecolor=FOCAL if is_focal(labels[i]) else COLORS[(i+1)%len(COLORS)], alpha=0.7)
    rng = np.random.default_rng(7)
    for i, vals in enumerate(values, 1):
        ax.scatter(vals, np.full(len(vals), i)+rng.normal(0, 0.045, len(vals)), s=18, color=INK, alpha=0.65, edgecolor="white", linewidth=0.3)
        ax.text(max(vals), i+0.23, f"n={len(vals)}", ha="right", fontsize=7, color=MUTED)
    ax.set_xlabel(str(df.metric.iloc[0]) if "metric" in df else "Performance"); ax.grid(axis="x"); ax.grid(axis="y", visible=False)
    fig.suptitle(title_two_lines(title), fontsize=14, fontweight="semibold", color=INK)
    return fig


def heatmap_figure(df, title, figsize):
    row, column = ("row", "column") if {"row", "column"}.issubset(df.columns) else (next((c for c in ("variant", "method", "model") if c in df), None), next((c for c in ("metric", "dataset") if c in df), None))
    if not row or not column: raise ValueError("heatmap needs row/column or variant/metric")
    table = df.pivot_table(index=row, columns=column, values="value", aggfunc="mean")
    fig, ax = plt.subplots(figsize=(max(figsize[0], 1.4+0.7*table.shape[1]), max(figsize[1], 1.5+0.45*table.shape[0])), constrained_layout=True)
    image = ax.imshow(table.to_numpy(), cmap="YlGnBu", aspect="auto")
    ax.set_xticks(range(table.shape[1]), [wrap(v, 14) for v in table.columns]); ax.set_yticks(range(table.shape[0]), [wrap(v, 20) for v in table.index]); ax.tick_params(labelrotation=0, length=0)
    midpoint = (np.nanmin(table.to_numpy()) + np.nanmax(table.to_numpy())) / 2
    for i in range(table.shape[0]):
        for j in range(table.shape[1]):
            v = table.iloc[i, j]
            if pd.notna(v): ax.text(j, i, f"{v:.2f}", ha="center", va="center", color="white" if v > midpoint else INK)
    for spine in ax.spines.values(): spine.set_visible(False)
    cbar = fig.colorbar(image, ax=ax, fraction=0.035, pad=0.025); cbar.outline.set_visible(False)
    fig.suptitle(title_two_lines(title), fontsize=14, fontweight="semibold", color=INK)
    return fig


def save(fig, out_prefix, dpi):
    prefix = Path(out_prefix); prefix.parent.mkdir(parents=True, exist_ok=True); fig.patch.set_facecolor("white")
    for ext in ("svg", "pdf", "png"): fig.savefig(prefix.with_suffix("."+ext), dpi=dpi, bbox_inches="tight", facecolor="white")
    print("Wrote", ", ".join(str(prefix.with_suffix("."+e)) for e in ("svg", "pdf", "png")))


def main():
    p = argparse.ArgumentParser(); p.add_argument("--input", required=True)
    p.add_argument("--kind", choices=["auto", "comparison", "ablation", "heatmap", "boxplot"], default="auto")
    p.add_argument("--ablation-mode", choices=["auto", "curve", "discrete"], default="auto")
    p.add_argument("--title"); p.add_argument("--out-prefix", required=True)
    p.add_argument("--preset", choices=list(PRESETS), default="cvpr"); p.add_argument("--layout", choices=["single", "double"], default="double")
    args = p.parse_args(); df = load(args.input); preset = apply_preset(args.preset, args.layout)
    global COLORS, FOCAL; COLORS = preset["colors"]; FOCAL = COLORS[0]
    kind, mode = args.kind, args.ablation_mode
    if kind == "auto":
        rec = profile_dataframe(df)["recommendation"]; print(f"Auto-selected {rec['kind']}: {rec['reason']}")
        kind = rec["kind"]
    if kind == "ablation": kind = "ablation-curve" if mode == "curve" or (mode == "auto" and {"x", "series"}.issubset(df.columns)) else "ablation-discrete"
    titles = {"comparison":"Comparison with Baselines", "ablation-discrete":"Ablation Study", "ablation-curve":"Ablation Study", "heatmap":"Performance Matrix", "boxplot":"Performance Across Repeated Runs"}
    title = args.title or titles[kind]; size = (preset["width"], preset["height"])
    makers = {"comparison": comparison_figure, "ablation-discrete": discrete_ablation_figure, "ablation-curve": curve_ablation_figure, "heatmap": heatmap_figure, "boxplot": boxplot_figure}
    save(makers[kind](df, title, size), args.out_prefix, preset["dpi"])


if __name__ == "__main__": main()
