#!/usr/bin/env python3
"""Rebuild a segmented reference figure as editable SVG plus a template manifest.

The segmentation JSON is intentionally model-neutral: SAM3, a VLM, OCR, or a
human can provide the regions. Text and geometric regions become native SVG;
icon regions remain individually replaceable image slots.
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import mimetypes
from pathlib import Path
import xml.etree.ElementTree as ET


SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)


def _read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _bbox(region):
    box = region.get("bbox")
    if not isinstance(box, list) or len(box) != 4:
        raise ValueError(f"{region.get('id', '?')}: bbox must be [x, y, w, h]")
    return [float(value) for value in box]


def _data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def build_svg(spec, spec_base: Path, output: Path):
    canvas = spec.get("canvas", {})
    width, height = canvas.get("width"), canvas.get("height")
    if not width or not height:
        raise ValueError("canvas.width and canvas.height are required")
    root = ET.Element(f"{{{SVG}}}svg", {
        "width": str(width), "height": str(height), "viewBox": f"0 0 {width} {height}",
    })
    defs = ET.SubElement(root, f"{{{SVG}}}defs")
    marker = ET.SubElement(defs, f"{{{SVG}}}marker", {
        "id": "arrow", "viewBox": "0 0 10 10", "refX": "9", "refY": "5",
        "markerWidth": "7", "markerHeight": "7", "orient": "auto-start-reverse",
    })
    ET.SubElement(marker, f"{{{SVG}}}path", {"d": "M0 0L10 5L0 10z", "fill": "context-stroke"})
    ET.SubElement(root, f"{{{SVG}}}rect", {
        "width": str(width), "height": str(height), "fill": canvas.get("background", "#ffffff"),
    })
    for region in spec.get("regions", []):
        region_id = region["id"]
        kind = region.get("kind", "shape")
        x, y, w, h = _bbox(region)
        common = {"id": region_id, "data-region-kind": kind}
        if kind == "text":
            element = ET.SubElement(root, f"{{{SVG}}}text", {
                **common, "x": str(x), "y": str(y + h * 0.78),
                "font-family": region.get("font_family", "Arial"),
                "font-size": str(region.get("font_size", max(10, h * 0.68))),
                "font-weight": str(region.get("font_weight", 400)),
                "fill": region.get("fill", "#172B4D"),
            })
            element.text = str(region.get("text", region_id))
        elif kind == "connector":
            points = region.get("points", [[x, y + h / 2], [x + w, y + h / 2]])
            ET.SubElement(root, f"{{{SVG}}}path", {
                **common, "d": "M " + " L ".join(f"{a} {b}" for a, b in points),
                "fill": "none", "stroke": region.get("stroke", "#47789E"),
                "stroke-width": str(region.get("stroke_width", 2.5)),
                "marker-end": "url(#arrow)" if region.get("arrow", True) else "",
            })
        elif kind == "image":
            href = ""
            if region.get("asset"):
                asset = (spec_base / region["asset"]).resolve()
                href = _data_uri(asset)
            ET.SubElement(root, f"{{{SVG}}}image", {
                **common, "x": str(x), "y": str(y), "width": str(w), "height": str(h),
                "href": href, "preserveAspectRatio": region.get("fit", "xMidYMid meet"),
            })
        else:
            shape = region.get("shape", "rect")
            attrs = {
                **common, "fill": region.get("fill", "#E5EEF5"),
                "stroke": region.get("stroke", "#426986"),
                "stroke-width": str(region.get("stroke_width", 2)),
            }
            if shape == "ellipse":
                attrs.update({"cx": str(x + w / 2), "cy": str(y + h / 2), "rx": str(w / 2), "ry": str(h / 2)})
                ET.SubElement(root, f"{{{SVG}}}ellipse", attrs)
            else:
                attrs.update({"x": str(x), "y": str(y), "width": str(w), "height": str(h), "rx": str(region.get("radius", 8))})
                ET.SubElement(root, f"{{{SVG}}}rect", attrs)
    output.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(output, encoding="utf-8", xml_declaration=True)


def build_manifest(spec, svg_name: str, output: Path):
    slots = []
    for region in spec.get("regions", []):
        if region.get("kind") not in {"text", "image"} or region.get("replaceable", True) is False:
            continue
        slots.append({
            "id": region["id"],
            "kind": region["kind"],
            "required": False,
            "selectors": {"svg": {"element_id": region["id"]}},
        })
    manifest = {
        "schema_version": "1.0",
        "template_id": spec.get("template_id", "reconstructed-reference"),
        "templates": {"svg": svg_name},
        "slots": slots,
        "provenance": {
            "source": spec.get("source"),
            "method": "segmentation-to-editable-svg",
            "note": "Reuse visual grammar only; verify scientific content and rights before publication.",
        },
    }
    output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("segments", help="model-neutral SAM3/VLM/OCR region JSON")
    parser.add_argument("--svg-out", required=True)
    parser.add_argument("--manifest-out", required=True)
    args = parser.parse_args()
    source = Path(args.segments).resolve()
    svg_out = Path(args.svg_out).resolve()
    manifest_out = Path(args.manifest_out).resolve()
    spec = _read(source)
    build_svg(spec, source.parent, svg_out)
    build_manifest(spec, svg_out.name, manifest_out)
    print(f"Wrote editable SVG: {svg_out}")
    print(f"Wrote template manifest: {manifest_out}")


if __name__ == "__main__":
    main()

