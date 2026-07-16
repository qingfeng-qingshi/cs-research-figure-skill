---
name: draw-cs-research-figures
description: Create, reconstruct, and revise publication-ready editable figures for computer science and AI papers. Use for method overviews, Transformer or attention modules, RAG and agent pipelines, multimodal systems, MoE routing, LoRA/Adapter modules, knowledge graphs, tensor flows, experiment plots, SVG/PPTX reconstruction, or editable template replacement.
---

# Draw CS Research Figures

Turn research content into an accurate visual argument and deliver editable artifacts. Use references for visual grammar, never as permission to copy paper-specific content.

## Required workflow

1. Inspect the method text, data, reference figure, and requested format.
2. Separate facts from presentation choices. Treat incomplete descriptions as normal and apply `references/incomplete-input.md`. Never invent modules, tensor sizes, metrics, or results.
3. Write a Figure Brief: claim, reading order, inputs, transformations, outputs, innovations, phase-specific paths, losses, and uncertainties.
4. Plan a coordinated method/comparison/ablation suite with `references/figure-suite.md`, then select a macro-layout and visual primitives from `references/style-language.md` and `references/module-library.md`.
5. Build a scene graph before drawing. Read `references/figure-schema.md` for JSON.
6. Render an editable master, normally SVG. For PowerPoint, use native shapes and keep an SVG master when possible. For data plots, deliver plotting code plus SVG/PDF.
7. Run the validator, render a preview, and apply every gate in `references/quality-gates.md`.
8. Deliver editable source, preview, editable-group legend, and unresolved scientific assumptions.

## Layout decision

- Use **parallel lanes** for multi-view, multimodal, teacher-student, or train/inference comparisons.
- Use **stacked architecture** for Transformer layers, residual blocks, attention internals, or tensor stages.
- Use **zoned pipeline** for document AI, RAG, agents, knowledge graphs, human feedback, or long workflows.
- Use **hub-and-spoke routing** for MoE, tool selection, retrieval, memory, or expert dispatch.
- Use **overview plus zoom-in** when a local mechanism is the novelty.
- Use **small multiples or conventional plots** for experiments; retain axes, uncertainty, baselines, and units. Apply `references/experiment-style.md`; keep ordinary labels horizontal and use horizontal bars or wrapping for long categories.

## Visual rules

- Put text inside its owning shape with explicit padding; size shapes from text.
- Route edges between boundaries or named ports. Keep arrowheads outside nodes and labels away from paths.
- Use color for semantic family, line style for phase or optionality, and thickness only for emphasis.
- Keep the main path dominant; losses, feedback, and auxiliary branches remain quieter.
- Use restrained pastel fills, dark neutral text, consistent radii, and one accent per semantic family. Integrate tensors, token strips, graph nodes, layer stacks, icons, plots, and zoom callouts whenever they encode actual structure; do not represent every concept as a labeled rectangle.
- Do not render scaffolds such as 闂傚倷鑳堕崑銊╁磿閺屻儲鍤戦柛宥咁劇E 1闂? bounding boxes, or guide labels unless explicitly requested.
- Preserve equations as text or vector paths and keep notation consistent with the manuscript. Split long figure titles at a semantic boundary into at most two horizontal, editable text lines.
- Show tensor shapes only when known and important. Show repeated layers with depth cues and a repetition label.

## Reference routing

- Read `references/style-language.md` for the distilled visual grammar. Read `references/inspiration-sources.md` only when source provenance or a new figure family matters.
- Read `references/module-library.md` for domain modules and edge semantics. Read `references/incomplete-input.md` when the user has only prose or partial details. Read `references/figure-suite.md` for algorithm, comparison, and ablation chapters. Read `references/experiment-style.md` before plotting experiments.
- Read `references/figure-schema.md` before scene-graph JSON.
- Read `references/quality-gates.md` before delivery.
- Run `python scripts/validate_figure_spec.py spec.json`.
- Run `python scripts/render_svg.py spec.json output.svg` for editable method figures; node kinds include tensor, tokens, graph, stack, attention, document, model, plot, and loss.
- Run `python scripts/plot_experiments.py --input results.csv --kind comparison|ablation --ablation-mode auto --title "..." --out-prefix figure`. Ordered ablation data (`x`,`series`,`value`) becomes a line plot; categorical remove-one data remains discrete.
- Run `python scripts/validate_plot_svg.py figure.svg` to reject non-horizontal text and palettes with fewer than three chromatic colors.

## Output contract

Return an editable master, a PNG preview, the Figure Brief or scene graph, validation status, and scientific assumptions. For reconstruction, preserve meaning but redraw with an original visual system. For template replacement, map stable object IDs and preserve grouping, anchors, alignment, and text containment.
