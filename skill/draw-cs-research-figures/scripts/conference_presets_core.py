#!/usr/bin/env python3
"""Reusable publication presets for CS/AI experiment figures.

The dimensions are practical starting points, not substitutes for the current
author kit of a venue. SVG text remains editable and PDF uses TrueType fonts.
"""
from __future__ import annotations

import matplotlib.pyplot as plt


PALETTES = {
    "conference": ["#2878B5", "#D95F59", "#4C956C", "#E5A84B", "#8064A2", "#45A6A6"],
    "ieee": ["#2166AC", "#B2182B", "#4D9221", "#762A83", "#D6604D", "#4393C3"],
    "zh": ["#2F6F9F", "#C66B3D", "#4D8B67", "#B88A2A", "#7866A8", "#3F9296"],
}

PRESETS = {
    "cvpr": {"single": 3.25, "double": 6.75, "font": "Arial", "base": 8.0, "dpi": 300, "palette": "conference"},
    "neurips": {"single": 3.25, "double": 6.50, "font": "DejaVu Sans", "base": 8.0, "dpi": 300, "palette": "conference"},
    "icml": {"single": 3.25, "double": 6.75, "font": "DejaVu Sans", "base": 8.0, "dpi": 300, "palette": "conference"},
    "acl": {"single": 3.30, "double": 6.90, "font": "Times New Roman", "base": 8.0, "dpi": 300, "palette": "conference"},
    "ieee": {"single": 3.50, "double": 7.16, "font": "Times New Roman", "base": 8.0, "dpi": 600, "palette": "ieee"},
    "zh-thesis": {"single": 5.70, "double": 6.90, "font": "Microsoft YaHei", "base": 9.0, "dpi": 300, "palette": "zh"},
}


def get_preset(name: str, layout: str = "double", height_ratio: float = 0.58) -> dict:
    if name not in PRESETS:
        raise ValueError(f"unknown preset {name!r}; choose from {', '.join(PRESETS)}")
    if layout not in {"single", "double"}:
        raise ValueError("layout must be single or double")
    item = dict(PRESETS[name])
    width = float(item[layout])
    item.update(name=name, layout=layout, width=width, height=width * height_ratio)
    item["colors"] = list(PALETTES[item["palette"]])
    return item


def apply_preset(name: str, layout: str = "double") -> dict:
    p = get_preset(name, layout)
    font = p["font"]
    base = p["base"]
    plt.rcParams.update({
        "figure.figsize": (p["width"], p["height"]),
        "figure.dpi": 140,
        "savefig.dpi": p["dpi"],
        "font.family": "sans-serif",
        "font.sans-serif": [font, "Noto Sans CJK SC", "Microsoft YaHei", "Arial", "DejaVu Sans"],
        "font.size": base,
        "axes.labelsize": base + 0.5,
        "axes.titlesize": base + 1.5,
        "xtick.labelsize": base - 0.5,
        "ytick.labelsize": base - 0.5,
        "legend.fontsize": base - 0.5,
        "axes.unicode_minus": False,
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })
    return p


if __name__ == "__main__":
    for key in PRESETS:
        p = get_preset(key)
        print(f"{key:10s} {p['width']:.2f} in  {p['font']}  {p['dpi']} DPI")
