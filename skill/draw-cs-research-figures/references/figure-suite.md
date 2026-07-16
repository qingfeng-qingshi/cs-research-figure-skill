# Figure suite for a paper or thesis chapter

Plan figures as a coordinated suite rather than forcing all information into one canvas.

## Algorithm description

Create:

1. **Method overview:** inputs 鈫?feature extraction 鈫?proposed module 鈫?prediction, with training objectives and phase distinctions.
2. **Innovation zoom-in:** internal tensor operations, attention, routing, graph reasoning, or fusion.
3. **Optional training/inference view:** only when phase behavior materially differs.

Use tensor stacks, token strips, graph nodes, repeated layer cards, model/device/document icons, equations, and boundary loss badges where they communicate real structure.

## Comparison experiments

Extract baselines, datasets, metrics, direction, and uncertainty from tables or files.

- One metric, many methods: ordered horizontal bars or dot plot.
- Several metrics with compatible scales: grouped bars or small multiples.
- Accuracy vs cost/parameters/latency: scatter plot with Pareto frontier.
- Several datasets: heatmap or aligned small multiples.
- Training curves: lines with uncertainty bands where available.

Highlight the proposed method with one accent and keep baselines neutral. Do not truncate axes deceptively or combine incompatible metric scales.

## Ablation experiments

Start from the scientific question:

- Ordered feature-combination, iteration, depth, rank, or hyperparameter experiments: multi-series line plots, using aligned panels for repeated groups.
- Component contribution with unordered remove-one variants: horizontal bars or dots; do not imply continuity with connecting lines.
- Hyperparameter sensitivity: line plot with marked optimum.
- Interaction between two factors: heatmap or faceted lines.
- Layer/head/expert analysis: distribution, matrix, or specialization map.
- Qualitative ablation: aligned examples with identical crops and annotations.

Order variants so the full method and progressive removals are easy to compare. Annotate delta from full model only when values are supplied.

## Cross-figure consistency

Keep the proposed method color, module names, abbreviations, dataset order, and metric formatting consistent across method, comparison, and ablation figures.
