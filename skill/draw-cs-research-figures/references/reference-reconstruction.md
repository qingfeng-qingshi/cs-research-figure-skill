# Reference reconstruction

Use reference figures as structural and stylistic evidence, not as content to copy.

## Pipeline

1. Ask a VLM to identify panels, text boxes, geometric modules, connectors, icons, tensor stacks, graph regions, and zoom callouts.
2. Use SAM3 or another segmenter for local icon masks and bounding boxes. Use OCR for text; never rasterize text into the editable master. Normalize detections and crop local elements with `scripts/prepare_reference_segments.py`.
3. Normalize the result to the region JSON accepted by `scripts/reconstruct_reference.py`.
4. Rebuild text and simple geometry as native SVG. Keep complex icon crops as individually replaceable `<image>` slots until a vector reconstruction is available.
5. Run `scripts/audit_figure.py` and visually compare reading order, grouping, alignment, and information density.
6. Replace paper-specific labels, data, logos, and proprietary illustrations with the user's own content.

## Region JSON

```json
{
  "canvas": {"width": 1200, "height": 700, "background": "#ffffff"},
  "source": "reference.png",
  "regions": [
    {"id": "title", "kind": "text", "bbox": [60, 30, 500, 40], "text": "Editable title"},
    {"id": "module-a", "kind": "shape", "shape": "rect", "bbox": [80, 150, 220, 130]},
    {"id": "arrow-a-b", "kind": "connector", "bbox": [300, 190, 160, 20]},
    {"id": "local-icon", "kind": "image", "bbox": [500, 150, 180, 130], "asset": "icon.png"}
  ]
}
```

Treat automatically inferred region types and connections as hypotheses. Confirm them against the method text before drawing.

