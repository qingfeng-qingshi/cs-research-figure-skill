# CS Research Figure Skill

[中文](README.md) | [English](README_EN.md) | Current version: `v0.5.1`

An editable research-figure Skill for computer science and AI papers. It turns method descriptions, reference figures, and experiment CSV files into method diagrams, module explanations, comparison plots, and ablation figures, with data profiling, automatic chart selection, publication presets, and deterministic audits.

## Core capabilities

- Transformer, Attention, RAG, Agent, MoE, LoRA/Adapter, multimodal, and knowledge-graph figures.
- Tensor stacks, token strips, network layers, graph nodes, model icons, loss branches, and zoom callouts.
- Detection of sample sizes, uncertainty columns, variable types, and IQR outliers.
- Automatic selection of comparison, discrete ablation, ordered line, heatmap, or boxplot figures.
- CVPR, NeurIPS, ICML, ACL, IEEE, and Chinese-thesis presets.
- Editable SVG, PDF, PNG, source data, scene JSON, and machine-audit reports.
- Checks for clipping, overlaps, CJK corruption, grayscale ambiguity, DPI, and PDF font embedding.
- Reference-region reconstruction to native editable SVG text, geometry, connectors, and replaceable local assets.
- One `template_manifest.json` for PPTX, SVG, and Draw.io text or image replacement.

## Gallery

### 1. Editable AI method figure

![Editable AI method framework](examples/method-figure/rich-example-preview.png)

Multimodal inputs, tensor stacks, Transformer encoding, graph nodes, fusion, prediction heads, and loss branches. Files: [SVG](examples/method-figure/rich-example.svg) · [Scene JSON](examples/method-figure/rich-example-spec.json)

### 2. Baseline comparison

![Baseline comparison](examples/comparison/demo-comparison.png)

Long method names stay horizontal through a horizontal layout and direct value labels. Files: [SVG](examples/comparison/demo-comparison.svg) · [PDF](examples/comparison/demo-comparison.pdf) · [CSV](examples/comparison/demo-comparison.csv)

### 3. Ordered ablation and sensitivity

![Ordered ablation curves](examples/ablation/demo-ablation-curves.png)

For layer counts, LoRA ranks, expert counts, thresholds, epochs, and iterations. Categorical `w/o module` configurations are never connected as a continuous curve. Files: [SVG](examples/ablation/demo-ablation-curves.svg) · [PDF](examples/ablation/demo-ablation-curves.pdf) · [CSV](examples/ablation/demo-ablation-curves.csv)

### 4. Automatic profiling, selection, and audit

![Automatically selected repeated-run boxplot](examples/auto-selection/auto-boxplot.png)

The input has four methods and eight runs per method. The Skill selects a boxplot with raw points, applies the CVPR double-column preset, and audits SVG, PDF, and PNG. Files: [SVG](examples/auto-selection/auto-boxplot.svg) · [PDF](examples/auto-selection/auto-boxplot.pdf) · [CSV](examples/auto-selection/repeated-runs.csv) · [Profile](examples/auto-selection/profile.json) · [Audit](examples/auto-selection/auto-boxplot-audit.json)

### 5. Unified editable template replacement

![PPTX template replacement demo](examples/templates/demo-replaced-preview.png)

The same semantic values drive [editable SVG](examples/templates/demo-replaced.svg), [Draw.io XML](examples/templates/demo-replaced.drawio), and [editable PPTX](examples/templates/demo-replaced.pptx) through one [template manifest](examples/templates/template_manifest.json). This complex demo covers three multimodal inputs, vision/language/graph encoders, cross-modal attention, a learned relation graph, an adaptive-fusion zoom-in, predictions, and three training objectives. One run replaces eight text slots and three local vector assets without flattening the full figure.
### 6. Hot-topic LLM, multi-agent, vision, and software modules

![Hot-topic editable CS and AI module library](examples/module-library/hot-topic-module-library.png)

The catalog now contains 35 machine-readable modules across LLM/RAG, multi-agent collaboration, vision foundation models, and AI software systems. Each module includes English and Chinese keywords, aliases, a recommended visual primitive, required scientific semantics, and an independent editable SVG asset. All 35 modules have distinct geometry fingerprints; related modules may share palette and shape language, but never the complete illustration. Files: [Module catalog JSON](skill/draw-cs-research-figures/assets/module-catalog.json) · [Editable module overview SVG](examples/module-library/hot-topic-module-library.svg) · [Individual SVG asset directory](skill/draw-cs-research-figures/assets/module-icons)

### 7. Reference-guided redraw with new research content

The synthetic high-quality structure is shown on the left to demonstrate transferable zone proportions, reading order, shape language, edge hierarchy, and palette roles. The right side reconstructs the layout with new research content while preserving scene JSON, stable element IDs, and editable SVG. No paper-specific content is copied.

#### Multi-agent RAG

![Multi-agent RAG reference structure versus editable redraw](examples/imitation/multi-agent-rag/comparison.png)

Files: [Reference SVG](examples/imitation/multi-agent-rag/reference-structure.svg) · [Target editable SVG](examples/imitation/multi-agent-rag/target-redraw.svg) · [Target scene JSON](examples/imitation/multi-agent-rag/target-redraw-spec.json)

#### Vision foundation model

![Vision foundation model reference structure versus editable redraw](examples/imitation/vision-foundation-model/comparison.png)

Files: [Reference SVG](examples/imitation/vision-foundation-model/reference-structure.svg) · [Target editable SVG](examples/imitation/vision-foundation-model/target-redraw.svg) · [Target scene JSON](examples/imitation/vision-foundation-model/target-redraw-spec.json)

#### LLM serving and AI software system

![LLM serving reference structure versus editable redraw](examples/imitation/llm-serving-system/comparison.png)

Files: [Reference SVG](examples/imitation/llm-serving-system/reference-structure.svg) · [Target editable SVG](examples/imitation/llm-serving-system/target-redraw.svg) · [Target scene JSON](examples/imitation/llm-serving-system/target-redraw-spec.json)
## Installation

### Install with Codex

Send this in Codex:

```text
Use skill-installer to install:
https://github.com/qingfeng-qingshi/cs-research-figure-skill/tree/main/skill/draw-cs-research-figures
```

Invoke `$draw-cs-research-figures` in a new task after installation.

For PPTX template replacement, run `npm install` once inside the installed `draw-cs-research-figures` directory.

### Manual installation

```bash
git clone https://github.com/qingfeng-qingshi/cs-research-figure-skill.git
cd cs-research-figure-skill
python -m pip install -r requirements.txt
npm install  # optional: required for PPTX template replacement
cp -R skill/draw-cs-research-figures ~/.codex/skills/
```

## Usage

This repository is not a standalone GUI. Invoke the Skill in Codex and provide one or more of the following:

- method prose, equations, pseudocode, or code;
- experiment CSV data with models, metrics, repeated runs, or uncertainty;
- a reference image used only for layout and visual-language analysis;
- the target venue, column width, language, and output formats.

### Use case 1: method figure from a paper section

```text
Use $draw-cs-research-figures to read method.md.
First extract confirmed facts, unresolved details, and the central visual claim. Then create a method overview and a zoomed innovation module.
Include tensor flow, Transformer layers, graph reasoning, fusion, and loss branches only when supported by the text.
Apply the CVPR double-column style and return editable SVG, scene JSON, PNG preview, and an audit report.
```

Expected outputs:

```text
method.svg
method-spec.json
method-preview.png
method-audit.json
```

### Use case 2: profile experiment data and select a chart

```text
Use $draw-cs-research-figures to read results.csv.
Profile variable types, per-group sample sizes, uncertainty columns, and outliers before plotting.
Explain the recommended chart and why it fits the data. Apply the NeurIPS double-column preset and return SVG, PDF, PNG, profile JSON, and audit JSON.
Keep ordinary text horizontal and split long titles into at most two lines.
```

Automatic selection:

| Data structure | Selected chart |
|---|---|
| `variant, metric, value` | baseline comparison |
| `full / w/o module` | discrete ablation without connecting lines |
| `x, series, value` | ordered line plot |
| dense method × metric matrix | heatmap |
| repeated seed/run values | boxplot with raw points |

### Use case 3: complete paper figure suite

```text
Use $draw-cs-research-figures with method.md, comparison.csv, and ablation.csv.
Plan a coordinated method figure, baseline comparison, and ablation figure with consistent module names, semantic colors, typography, and metric formatting.
Return SVG plus scene JSON for the method figure, and SVG/PDF/PNG plus plotting source for experiment figures. Apply the ACL double-column preset and audit every output.
```

### Use case 4: structural redraw from a reference

```text
Use $draw-cs-research-figures with reference.png and method.md.
Extract only transferable zone proportions, reading order, shape language, edge hierarchy, information density, and palette roles.
Do not copy paper-specific labels, data, icons, or topology.
Search module-catalog.json for semantically valid LLM, multi-agent, vision, or software SVG modules, then rebuild the verified nodes and edges from method.md.
Return reference-structure-spec.json, target-redraw-spec.json, editable target-redraw.svg, and a side-by-side comparison.png.
Audit clipping, edge-label crossings, overlaps, and grayscale distinguishability.
```

### Use case 5: audit an existing figure

```text
Use $draw-cs-research-figures to audit figure.svg, figure.pdf, and figure.png.
Report clipping, overlap, CJK corruption, grayscale ambiguity, DPI, and PDF font embedding. Do not redraw yet; return PASS, WARN, or FAIL with concrete repair suggestions.
```

### Use case 6: reconstruct an editable figure from segmented reference regions

```text
Use $draw-cs-research-figures to analyze reference.png with SAM3/VLM/OCR.
Convert detected panels, text, shapes, connectors, and local icons to region JSON. Rebuild native text and geometry as editable SVG, preserve stable IDs, and create template_manifest.json for later replacement. Use only the reference's general visual grammar and verify every inferred connection against method.md.
```

### Use case 7: update an editable PPTX, SVG, or Draw.io template

```text
Use $draw-cs-research-figures with template_manifest.json and replacement_values.json.
Replace the title, module labels, and local illustration in all available formats. Preserve the template's geometry, typography, palette, and element IDs. Return editable outputs and run the normal quality audit.
```
## CLI

Profile data:

```bash
python skill/draw-cs-research-figures/scripts/profile_results.py results.csv \
  --json-out output/profile.json --report-out output/profile.txt
```

Select, render, and audit automatically:

```bash
python skill/draw-cs-research-figures/scripts/plot_experiments.py \
  --input results.csv --kind auto --preset cvpr --layout double \
  --title "Performance Across Repeated Runs" --out-prefix output/figure
```

`--kind`: `auto`, `comparison`, `ablation`, `heatmap`, `boxplot`. `--preset`: `cvpr`, `neurips`, `icml`, `acl`, `ieee`, `zh-thesis`.

Render a method figure:

```bash
python skill/draw-cs-research-figures/scripts/validate_figure_spec.py method-spec.json
python skill/draw-cs-research-figures/scripts/render_svg.py method-spec.json output/method.svg
```

Apply the same replacement values to editable templates:

```bash
npm install
python skill/draw-cs-research-figures/scripts/apply_template.py \
  --manifest examples/templates/template_manifest.json \
  --values examples/templates/replacement_values.json \
  --format pptx --output output/method.pptx
```

Use `--format svg` or `--format drawio` for the other editable masters. Normalize SAM3/VLM/OCR detections and crop local elements before reconstruction:

```bash
python skill/draw-cs-research-figures/scripts/prepare_reference_segments.py reference.png detections.json --out-dir output/segments
```


```bash
python skill/draw-cs-research-figures/scripts/reconstruct_reference.py \
  output/segments/segments.json --svg-out output/reconstructed.svg \
  --manifest-out output/template_manifest.json
```

Audit existing files:

```bash
python skill/draw-cs-research-figures/scripts/audit_figure.py \
  output/figure.svg output/figure.pdf output/figure.png \
  --min-dpi 300 --strict --json-out output/figure-audit.json
```

Audit verdicts:

- `FAIL`: missing glyphs, corruption, final clipping, low DPI, or Type-3 fonts.
- `WARN`: estimated overlap, grayscale ambiguity, or uncertain font fallback; inspect the PNG preview.
- `PASS`: no deterministic issue found; scientific-semantic review is still required.

## CSV schemas

Comparison:

```csv
variant,metric,value,std,n
Baseline Transformer,Accuracy (%),84.10,0.40,5
Proposed Method,Accuracy (%),87.30,0.30,5
```

Ordered ablation:

```csv
panel,x,series,value,metric,x_label,panel_title
dataset_a,1,rank=4,0.84,AUC,LoRA rank,Dataset A
dataset_a,2,rank=8,0.87,AUC,LoRA rank,Dataset A
```

Repeated runs:

```csv
variant,metric,value,seed
Baseline,Accuracy (%),84.1,1
Baseline,Accuracy (%),84.5,2
Proposed Method,Accuracy (%),87.3,1
```

## Test and package

```bash
python -m unittest discover -s tests -v
python scripts/package_skill.py
```

Current version: `v0.5.1`. Released under the MIT License. Verify the current official author kit before submission.

## 2025–2026 top-conference paper-figure candidate benchmark

![40 papers and 100 planned target Figures](examples/paper-figure-benchmark/candidate-overview.png)

The first candidate release contains 10 papers from each of CVPR, NeurIPS, ICML, and ACL, with 100 planned Figure-review slots. Records are organized by transferable visual role rather than paper title. Every slot remains pending until its PDF page, Figure number, caption, and visual score are verified. NeurIPS 2026 is excluded because acceptance decisions are not available yet; provisional ICML 2026 index records will be refreshed when the final PMLR volume is published.

Files: [editable overview SVG](examples/paper-figure-benchmark/candidate-overview.svg) · [paper seed JSON](skill/draw-cs-research-figures/references/paper-figure-benchmark/papers.json) · [100 Figure slots](skill/draw-cs-research-figures/references/paper-figure-benchmark/figures.jsonl) · [summary](skill/draw-cs-research-figures/references/paper-figure-benchmark/summary.json)
