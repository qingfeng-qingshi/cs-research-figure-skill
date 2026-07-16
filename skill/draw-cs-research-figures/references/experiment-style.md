# Experimental figure visual system

Use a restrained colorblind-friendly palette, not an almost-monochrome figure.

## Palette roles

- Proposed/full method: deep blue `#2F6F9F`.
- Baseline families: muted teal `#78A89C`, ochre `#D8A24A`, violet `#8E7DB5`, terracotta `#C87864`, and steel blue `#7095B5`.
- Ablated variants: use muted module-linked colors when the method figure defines them.
- Text: dark navy `#203040`; secondary text `#5F7182`; grid `#DCE4EA`.

Color distinguishes method families or component roles. Do not use rainbow order, gradients, or saturated colors for every mark.

## Typography and labels

- Keep all ordinary labels horizontal at 0 degrees.
- Never rotate delta annotations or category labels diagonally. A conventional 90-degree y-axis title is allowed.
- For long categories, prefer horizontal bars. Otherwise wrap labels over 2 lines or widen the canvas.
- Use sentence-case titles with moderate weight. Keep short titles on one line; split long titles at a semantic boundary into at most two horizontal lines. Keep both lines as editable SVG text.
- Place values outside bar ends with enough axis headroom.
- Show ablation deltas horizontally in parentheses after the score.
- Keep SVG text editable with `svg.fonttype = none`.

## Scientific rigor

- Start bar axes at zero unless the figure is explicitly a difference plot.
- State metric name and units.
- Preserve uncertainty and sample counts when supplied.
- Use consistent method colors across comparison, ablation, efficiency, and sensitivity plots.
- Highlight the proposed method without suppressing baseline legibility.
- Prefer direct labels to legends when the number of series is small.

## Ablation chart selection

- Prefer multi-series line plots when the x-axis is ordered: iteration, epoch, layer count, rank, expert count, threshold, or hyperparameter value.
- Use 2–6 aligned panels when the same ordered experiment is repeated across datasets, feature groups, or evaluation settings.
- Give each series a stable color and marker so the figure remains readable in grayscale.
- Do not connect categorical remove-one variants with lines. Use horizontal bars or dots for `full`, `w/o A`, and `w/o B` because those configurations have no continuous order.

Curve-ablation CSV uses `x`, `series`, and `value`, with optional `panel`, `metric`, `x_label`, and `panel_title`. Discrete ablation uses `variant`, `metric`, and `value`. The plotting script detects the schema automatically.