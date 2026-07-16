#!/usr/bin/env python3
import json
import sys
from pathlib import Path

REQ = {
    "panels": ("id", "label", "x", "y", "w", "h"),
    "nodes": ("id", "label", "x", "y", "w", "h"),
    "edges": ("id", "source", "target"),
}

def overlap(a, b):
    return a["x"] < b["x"] + b["w"] and a["x"] + a["w"] > b["x"] and a["y"] < b["y"] + b["h"] and a["y"] + a["h"] > b["y"]

def main(path):
    spec = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    errors, warnings = [], []
    canvas = spec.get("canvas", {})
    width, height = canvas.get("width", 0), canvas.get("height", 0)
    if width <= 0 or height <= 0:
        errors.append("canvas width and height must be positive")
    ids = {}
    for collection, required in REQ.items():
        for i, item in enumerate(spec.get(collection, [])):
            missing = [key for key in required if key not in item]
            if missing:
                errors.append(f"{collection}[{i}] missing: {', '.join(missing)}")
                continue
            ident = item["id"]
            if ident in ids:
                errors.append(f"duplicate id: {ident}")
            ids[ident] = collection
            if collection != "edges":
                if item["w"] <= 0 or item["h"] <= 0:
                    errors.append(f"{ident}: width and height must be positive")
                if item["x"] < 0 or item["y"] < 0 or item["x"] + item["w"] > width or item["y"] + item["h"] > height:
                    errors.append(f"{ident}: outside canvas")
                estimate = max(len(line) for line in str(item["label"]).splitlines()) * 8 + 32
                if estimate > item["w"]:
                    warnings.append(f"{ident}: label may not fit width")
    node_ids = {n.get("id") for n in spec.get("nodes", [])}
    for edge in spec.get("edges", []):
        if edge.get("source") not in node_ids or edge.get("target") not in node_ids:
            errors.append(f"{edge.get('id', '?')}: dangling endpoint")
        if edge.get("source") == edge.get("target"):
            warnings.append(f"{edge.get('id', '?')}: self-loop requires deliberate routing")
    nodes = spec.get("nodes", [])
    for i, first in enumerate(nodes):
        for second in nodes[i + 1:]:
            if overlap(first, second):
                warnings.append(f"{first.get('id')} overlaps {second.get('id')}")
    for node in nodes:
        panel_id = node.get("panel")
        if panel_id and ids.get(panel_id) != "panels":
            errors.append(f"{node.get('id')}: unknown panel {panel_id}")
    print(f"Validation: {len(errors)} error(s), {len(warnings)} warning(s)")
    for item in errors:
        print(f"ERROR: {item}")
    for item in warnings:
        print(f"WARN: {item}")
    return 1 if errors else 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: validate_figure_spec.py SPEC.json")
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1]))
