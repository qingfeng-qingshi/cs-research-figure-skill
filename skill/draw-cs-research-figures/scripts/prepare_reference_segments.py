#!/usr/bin/env python3
"""Normalize SAM3/VLM/OCR detections and crop replaceable local elements."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from PIL import Image


TEXT_LABELS = {"text", "title", "label", "caption", "formula"}
CONNECTOR_LABELS = {"arrow", "connector", "line", "edge"}
SHAPE_LABELS = {"box", "rectangle", "rect", "ellipse", "circle", "shape", "panel"}


def safe_id(value: str, index: int) -> str:
    value = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip()).strip("-").lower()
    return value or f"region-{index:03d}"


def normalize_box(box, box_format: str):
    if not isinstance(box, (list, tuple)) or len(box) != 4:
        raise ValueError("every detection needs a four-number bbox")
    a, b, c, d = map(float, box)
    if box_format == "xyxy":
        return [a, b, max(1.0, c - a), max(1.0, d - b)]
    return [a, b, max(1.0, c), max(1.0, d)]


def classify(label: str) -> str:
    token = label.lower().strip()
    if token in TEXT_LABELS or any(part in token for part in ("text", "title", "label")):
        return "text"
    if token in CONNECTOR_LABELS or any(part in token for part in ("arrow", "connector")):
        return "connector"
    if token in SHAPE_LABELS:
        return "shape"
    return "image"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image")
    parser.add_argument("detections", help="SAM3/VLM/OCR JSON with detections or boxes")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--bbox-format", choices=("xywh", "xyxy"), default="xyxy")
    parser.add_argument("--segments-name", default="segments.json")
    args = parser.parse_args()

    image_path = Path(args.image).resolve()
    detections_path = Path(args.detections).resolve()
    out_dir = Path(args.out_dir).resolve()
    assets_dir = out_dir / "assets"
    out_dir.mkdir(parents=True, exist_ok=True)
    assets_dir.mkdir(exist_ok=True)
    source = Image.open(image_path).convert("RGBA")
    raw = json.loads(detections_path.read_text(encoding="utf-8-sig"))
    detections = raw.get("detections", raw.get("boxes", raw if isinstance(raw, list) else []))
    if not isinstance(detections, list):
        raise ValueError("detections JSON must contain a detections or boxes array")

    regions = []
    used = set()
    for index, detection in enumerate(detections, 1):
        label = str(detection.get("label", detection.get("prompt", detection.get("class", "image"))))
        region_id = safe_id(str(detection.get("id", label)), index)
        if region_id in used:
            region_id = f"{region_id}-{index:03d}"
        used.add(region_id)
        box = detection.get("bbox", detection.get("box", detection.get("xyxy")))
        box_format = "xyxy" if "xyxy" in detection else args.bbox_format
        x, y, w, h = normalize_box(box, box_format)
        x = max(0.0, min(x, source.width - 1))
        y = max(0.0, min(y, source.height - 1))
        w = min(w, source.width - x)
        h = min(h, source.height - y)
        kind = detection.get("kind", classify(label))
        region = {"id": region_id, "kind": kind, "bbox": [x, y, w, h]}
        for key in ("fill", "stroke", "stroke_width", "font_size", "font_weight", "shape", "points", "arrow"):
            if key in detection:
                region[key] = detection[key]
        if kind == "text":
            region["text"] = detection.get("text", label)
        elif kind == "image":
            crop_name = f"{region_id}.png"
            crop = source.crop((round(x), round(y), round(x + w), round(y + h)))
            crop.save(assets_dir / crop_name)
            region["asset"] = f"assets/{crop_name}"
        regions.append(region)

    result = {
        "template_id": safe_id(image_path.stem, 0),
        "source": image_path.name,
        "canvas": {"width": source.width, "height": source.height, "background": "#ffffff"},
        "regions": regions,
        "provenance": {"detections": detections_path.name, "bbox_format": args.bbox_format},
    }
    target = out_dir / args.segments_name
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote normalized regions: {target}")
    print(f"Cropped {sum(region['kind'] == 'image' for region in regions)} local element(s): {assets_dir}")


if __name__ == "__main__":
    main()
