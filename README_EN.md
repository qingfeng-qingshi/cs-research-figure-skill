# CS Research Figure Skill

[中文](README.md) | [English](README_EN.md)

An editable research-figure Skill for computer science and AI papers, with method diagrams, experiment-data profiling, automatic chart selection, publication presets, and deterministic quality audits.

## New in v0.3

Every generated experiment figure is automatically checked for:

- text clipping and overlapping labels or ticks;
- missing Chinese glyphs and likely encoding corruption;
- grayscale distinguishability and redundant marker/line-style encoding;
- PNG/TIFF DPI;
- Type-3 or potentially unembedded PDF fonts.

The pipeline writes `*-audit.json` and blocks delivery when a FAIL remains.

## Automatic analysis, selection, and audit demo

![Automatically selected repeated-run boxplot](examples/auto-selection/auto-boxplot.png)

The input contains four methods with eight repeated runs each. The Skill selects a boxplot with raw points, applies the CVPR double-column preset, and audits SVG, PDF, and PNG outputs.

- [Input CSV](examples/auto-selection/repeated-runs.csv)
- [Data profile](examples/auto-selection/profile.txt)
- [Editable SVG](examples/auto-selection/auto-boxplot.svg)
- [PDF](examples/auto-selection/auto-boxplot.pdf)
- [Automatic audit report](examples/auto-selection/auto-boxplot-audit.json)

## Install

Ask Codex:

```text
Use skill-installer to install https://github.com/qingfeng-qingshi/cs-research-figure-skill/tree/main/skill/draw-cs-research-figures
```

## Use

```text
Use $draw-cs-research-figures to profile results.csv, select a chart, apply the CVPR double-column preset, generate SVG/PDF/PNG, and audit clipping, overlaps, Chinese glyphs, grayscale, DPI, and PDF font embedding.
```

CLI:

```bash
python skill/draw-cs-research-figures/scripts/plot_experiments.py --input results.csv --kind auto --preset cvpr --layout double --out-prefix output/figure
python skill/draw-cs-research-figures/scripts/audit_figure.py output/figure.svg output/figure.pdf output/figure.png --strict --json-out output/figure-audit.json
```

## Existing capabilities

- Transformer, Attention, RAG, Agent, MoE, LoRA/Adapter, multimodal, and knowledge-graph method figures.
- Tensor stacks, token strips, graph nodes, model icons, and zoom callouts.
- Comparison, discrete ablation, ordered line, heatmap, and boxplot figures.
- CVPR, NeurIPS, ICML, ACL, IEEE, and Chinese-thesis presets.

## Test

```bash
python -m unittest discover -s tests -v
python scripts/package_skill.py
```

Released under the MIT License. Verify the current official author kit before submission.
