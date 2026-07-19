---
name: draw-cs-research-figures
description: Create, reconstruct, and revise publication-ready editable figures for computer science, software systems, and AI papers. Use for method diagrams, LLM/RAG and multi-agent pipelines, vision foundation models, model-serving systems, Transformer or attention modules, MoE routing, LoRA/Adapter modules, knowledge graphs, tensor flows, experimental-data profiling, automatic chart selection, comparison and ablation plots, reference-guided redraw, publication presets, deterministic figure auditing, SVG/PPTX reconstruction, or editable template replacement.
---

# Draw CS Research Figures

Turn research content and experimental data into an accurate visual argument with editable artifacts.

## Required workflow

1. Inspect the method text, data, reference figure, and requested format.
2. Separate facts from presentation choices. Apply `references/incomplete-input.md`; never invent modules, tensor sizes, metrics, uncertainty, sample sizes, or results.
3. Write a Figure Brief: claim, reading order, inputs, transformations, outputs, innovations, losses, and uncertainties.
4. For experimental CSV data, run `scripts/profile_results.py`. Read `references/chart-selection.md` and use its recommendation unless the paper's claim requires a justified alternative.
5. Select the target preset from `references/publication-presets.md`. Treat presets as reproducible defaults and verify the current author kit before submission.
6. Plan the figure suite with `references/figure-suite.md`; select visual primitives from `references/style-language.md` and `references/module-library.md`. For LLM, multi-agent, computer-vision, or software-system requests, read `references/hot-topic-modules.md` and search `assets/module-catalog.json`.
   For recent top-conference style matching, read `references/paper-figure-benchmark.md` and select by visual grammar and Figure role, never by title similarity alone.
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
- Give each named module a distinct structural icon. Related modules may share visual grammar, but never reuse the complete geometry under a different label.

## Reference reconstruction and editable templates

- For reference-guided reconstruction, read `references/reference-reconstruction.md`. Normalize SAM3/VLM/OCR results with `scripts/prepare_reference_segments.py`, then run `scripts/reconstruct_reference.py`. Rebuild text, simple geometry, and connectors as native SVG; keep complex crops as individually replaceable slots.
- For layout imitation, preserve only transferable visual grammar and rebuild the user's verified topology. Save reference and target scene JSON, editable target SVG, and a side-by-side preview; use `examples/imitation/` as the output contract.
- Treat the 2025–2026 paper benchmark as a candidate index until its PDF page, Figure number, caption, and visual score are verified. Never present a planned Figure slot as a reviewed gold example.
- For an existing template, read `references/template-manifest.md`. Require stable SVG IDs, Draw.io cell IDs, or PowerPoint Selection Pane names. Never locate elements by visual guess when a stable identifier is available.
- Use one `template_manifest.json` for PPTX, SVG, and Draw.io. Apply replacements with `scripts/apply_template.py`.
- Use `pptx-automizer` for PPTX text and image replacement. Install the optional Node dependencies in the installed Skill directory with `npm install`.
- Preserve the existing module library, experiment plotting, publication presets, and automatic audit after template application. A successful replacement is not a substitute for semantic and visual QA.
## Automatic audit

- Call `audit_matplotlib_figure(fig)` before custom Matplotlib exports to detect renderer clipping, tick overlap, and missing glyphs.
- Run `python scripts/audit_figure.py figure.svg figure.pdf figure.png --strict --json-out figure-audit.json` for SVG bounds/overlap/encoding/grayscale, raster DPI, and PDF font embedding.
- Treat missing glyphs, corrupted text, final clipping, low DPI, and Type-3 PDF fonts as blocking failures.
- Treat estimated overlap, grayscale ambiguity, and uncertain CJK fallback as warnings requiring preview review.

## Commands

- `python scripts/search_module_catalog.py "multi-agent RAG shared memory"`
- `python scripts/generate_paper_figure_benchmark.py`
- `python scripts/generate_hot_topic_library.py`
- `python scripts/validate_figure_spec.py spec.json`
- `python scripts/render_svg.py spec.json output.svg`
- `python scripts/profile_results.py results.csv`
- `python scripts/plot_experiments.py --input results.csv --kind auto --preset neurips --out-prefix figure`
- `python scripts/audit_figure.py figure.svg figure.pdf figure.png --strict`
- `python scripts/reconstruct_reference.py segments.json --svg-out reconstructed.svg --manifest-out template_manifest.json`
- `python scripts/apply_template.py --manifest template_manifest.json --values values.json --format svg --output result.svg`

## Output contract

Return an editable master, PNG preview, source data or scene graph, validation status, machine-audit JSON, chart-selection reason, active publication preset, and unresolved scientific assumptions.
