---
name: draw-cs-research-figures
description: Create, reconstruct, and revise publication-ready editable figures for computer science and AI papers. Use for method diagrams, Transformer or attention modules, RAG and agent pipelines, multimodal systems, MoE routing, LoRA/Adapter modules, knowledge graphs, tensor flows, experimental-data profiling, automatic chart selection, comparison and ablation plots, publication presets, deterministic figure auditing, SVG/PPTX reconstruction, or editable template replacement.
---

# Draw CS Research Figures

Turn research content and experimental data into an accurate visual argument with editable artifacts.

## Required workflow

1. Inspect the method text, data, reference figure, and requested format.
2. Separate facts from presentation choices. Apply `references/incomplete-input.md`; never invent modules, tensor sizes, metrics, uncertainty, sample sizes, or results.
3. Write a Figure Brief: claim, reading order, inputs, transformations, outputs, innovations, losses, and uncertainties.
4. For experimental CSV data, run `scripts/profile_results.py`. Read `references/chart-selection.md` and use its recommendation unless the paper's claim requires a justified alternative.
5. Select the target preset from `references/publication-presets.md`. Treat presets as reproducible defaults and verify the current author kit before submission.
6. Plan the figure suite with `references/figure-suite.md`; select visual primitives from `references/style-language.md` and `references/module-library.md`.
7. Build a scene graph before drawing a method figure. Read `references/figure-schema.md`.
8. Render an editable master. Prefer SVG for method figures; deliver plotting code plus SVG/PDF for data plots.
9. Run the automatic checks in `references/quality-audit.md`, render a PNG preview, and apply `references/quality-gates.md`. Fix every FAIL before delivery and visually review every WARN.

## Experimental figures

- Run `python scripts/profile_results.py results.csv --json-out profile.json --report-out profile.txt` to identify variable types, observed sample sizes, uncertainty columns, IQR outliers, and a chart recommendation.
- Run `python scripts/plot_experiments.py --input results.csv --kind auto --preset cvpr --layout double --out-prefix figure`. It selects a comparison, discrete ablation, ordered line, heatmap, or boxplot and automatically writes `figure-audit.json`.
- Preserve SD/SEM/CI and `n` when supplied. Never silently convert one uncertainty definition into another.
- Use ordered lines only for genuinely ordered settings. Do not connect categorical remove-one ablations.
- Keep ordinary labels horizontal. Wrap long labels or use horizontal layouts.

## Method figures

- Use parallel lanes for multimodal or teacher-student comparisons.
- Use stacked architecture for Transformer layers and attention internals.
- Use zoned pipelines for RAG, agents, document AI, and knowledge graphs.
- Use hub-and-spoke routing for MoE, tools, memory, and retrieval.
- Use overview plus zoom-in when a local mechanism is the novelty.
- Integrate tensors, token strips, graph nodes, layer stacks, icons, plots, and zoom callouts only when they encode real structure.

## Automatic audit

- Call `audit_matplotlib_figure(fig)` before custom Matplotlib exports to detect renderer clipping, tick overlap, and missing glyphs.
- Run `python scripts/audit_figure.py figure.svg figure.pdf figure.png --strict --json-out figure-audit.json` for SVG bounds/overlap/encoding/grayscale, raster DPI, and PDF font embedding.
- Treat missing glyphs, corrupted text, final clipping, low DPI, and Type-3 PDF fonts as blocking failures.
- Treat estimated overlap, grayscale ambiguity, and uncertain CJK fallback as warnings requiring preview review.

## Commands

- `python scripts/validate_figure_spec.py spec.json`
- `python scripts/render_svg.py spec.json output.svg`
- `python scripts/profile_results.py results.csv`
- `python scripts/plot_experiments.py --input results.csv --kind auto --preset neurips --out-prefix figure`
- `python scripts/audit_figure.py figure.svg figure.pdf figure.png --strict`

## Output contract

Return an editable master, PNG preview, source data or scene graph, validation status, machine-audit JSON, chart-selection reason, active publication preset, and unresolved scientific assumptions.
