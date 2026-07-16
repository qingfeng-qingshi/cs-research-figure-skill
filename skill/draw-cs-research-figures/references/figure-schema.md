# Figure scene-graph schema

Use JSON with `canvas`, optional `title`, and arrays of `panels`, `nodes`, and `edges`.

Coordinates are absolute SVG units; x,y are top-left. IDs must be unique. Edge endpoints reference node IDs. Edge styles: `solid`, `dashed`, `feedback`.

Required panel fields: id, label, x, y, w, h. Required node fields: id, label, x, y, w, h. Required edge fields: id, source, target. Optional fields include panel, kind, fill, stroke, text_color, radius, subtitle, group, frozen, emphasis, style, color, width, source_port, and target_port.

The baseline renderer automatically connects node boundaries and creates editable SVG groups with stable IDs.
