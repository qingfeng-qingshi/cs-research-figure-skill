# Quality gates

Approve only when every applicable gate passes.

## Scientific fidelity

- Every node, edge, dimension, equation, loss, and value is supported or marked as an assumption.
- The overview expresses the contribution rather than a generic pipeline.
- Training/inference, frozen/trainable, shared, and repeated components are distinguishable when relevant.

## Geometry

- Text is inside its shape with visible padding at final size.
- No unintended overlap, edge-through-text, cropped arrowhead, or clipped label.
- Repeated elements share dimensions, alignment, spacing, radius, and stroke.
- Connections terminate on ports or boundaries rather than arbitrary interiors.

## Readability and editability

- Main reading order is clear at thumbnail scale; the main path dominates.
- Font is legible at target size and color meaning is consistent. Ordinary labels remain horizontal; long labels use wrapping or horizontal charts.
- SVG text remains text except incompatible math; PPTX uses native grouped shapes.
- Plot source and data accompany SVG/PDF; stable IDs support template replacement.

## Visual QA loop

1. Run JSON validation.
2. Render SVG or PPTX to PNG.
3. Inspect at 100% and thumbnail scale.
4. Fix collision classes globally, then local exceptions.
5. Repeat until validation and visual inspection both pass.
