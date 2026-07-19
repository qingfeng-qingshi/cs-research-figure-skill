#!/usr/bin/env python3
"""Apply one template_manifest.json to SVG, Draw.io, or PPTX templates."""

from __future__ import annotations

import argparse
import base64
import copy
import mimetypes
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote
import xml.etree.ElementTree as ET

from template_manifest_core import (
    ManifestError,
    load_manifest,
    read_json,
    replacement_value,
    template_path,
)


XLINK = "http://www.w3.org/1999/xlink"
ET.register_namespace("", "http://www.w3.org/2000/svg")
ET.register_namespace("xlink", XLINK)


def _selector(slot, fmt):
    selector = slot.get("selectors", {}).get(fmt)
    if selector is None:
        return None
    if isinstance(selector, str):
        key = "element_id" if fmt == "svg" else "cell_id"
        return {key: selector}
    if not isinstance(selector, dict):
        raise ManifestError(f"{slot['id']}: invalid {fmt} selector")
    return selector


def _asset_path(value, values_base: Path) -> Path:
    path = Path(str(value))
    if not path.is_absolute():
        path = values_base / path
    path = path.resolve()
    if not path.is_file():
        raise ManifestError(f"replacement asset does not exist: {path}")
    return path


def _data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def _find_id(root: ET.Element, element_id: str) -> ET.Element | None:
    return next((element for element in root.iter() if element.get("id") == element_id), None)


def _replace_svg_fragment(target: ET.Element, asset: Path, selector: dict) -> None:
    fragment_root = ET.parse(asset).getroot()
    view_box = fragment_root.get("viewBox")
    if not view_box:
        view_box = f"0 0 {fragment_root.get('width', '100')} {fragment_root.get('height', '100')}"
    for child in list(target):
        target.remove(child)
    nested = ET.SubElement(target, "{http://www.w3.org/2000/svg}svg", {
        "x": str(selector.get("x", 0)), "y": str(selector.get("y", 0)),
        "width": str(selector.get("w", "100%")), "height": str(selector.get("h", "100%")),
        "viewBox": view_box, "preserveAspectRatio": selector.get("fit", "xMidYMid meet"),
    })
    for child in list(fragment_root):
        nested.append(copy.deepcopy(child))


def apply_svg(manifest, manifest_base, values, values_base, output: Path) -> None:
    source = template_path(manifest, manifest_base, "svg")
    tree = ET.parse(source)
    root = tree.getroot()
    for slot in manifest["slots"]:
        selector = _selector(slot, "svg")
        value = replacement_value(values, slot)
        if selector is None or value is None:
            continue
        target = _find_id(root, selector.get("element_id", ""))
        if target is None:
            raise ManifestError(f"{slot['id']}: SVG element not found")
        if slot["kind"] == "text":
            for child in list(target):
                target.remove(child)
            target.text = str(value)
        elif slot["kind"] == "image":
            href = _data_uri(_asset_path(value, values_base))
            target.set("href", href)
            target.set(f"{{{XLINK}}}href", href)
        elif slot["kind"] == "svg-fragment":
            _replace_svg_fragment(target, _asset_path(value, values_base), selector)
    output.parent.mkdir(parents=True, exist_ok=True)
    tree.write(output, encoding="utf-8", xml_declaration=True)


def _drawio_model(root: ET.Element) -> ET.Element:
    tag = root.tag.rsplit("}", 1)[-1]
    if tag == "mxGraphModel":
        return root
    if tag != "mxfile":
        raise ManifestError("Draw.io template must contain mxfile or mxGraphModel")
    diagram = root.find("diagram")
    if diagram is None or not list(diagram):
        raise ManifestError("compressed Draw.io diagrams are not supported; save as uncompressed XML")
    model = list(diagram)[0]
    if model.tag.rsplit("}", 1)[-1] != "mxGraphModel":
        raise ManifestError("Draw.io diagram does not contain mxGraphModel")
    return model


def _set_style(style: str, key: str, value: str) -> str:
    parts = [part for part in style.split(";") if part and not part.startswith(key + "=")]
    parts.append(f"{key}={value}")
    return ";".join(parts) + ";"


def apply_drawio(manifest, manifest_base, values, values_base, output: Path) -> None:
    source = template_path(manifest, manifest_base, "drawio")
    tree = ET.parse(source)
    root = tree.getroot()
    model = _drawio_model(root)
    for slot in manifest["slots"]:
        selector = _selector(slot, "drawio")
        value = replacement_value(values, slot)
        if selector is None or value is None:
            continue
        cell = next((item for item in model.iter() if item.get("id") == selector.get("cell_id")), None)
        if cell is None:
            raise ManifestError(f"{slot['id']}: Draw.io cell not found")
        if slot["kind"] == "text":
            cell.set("value", str(value))
        elif slot["kind"] in {"image", "svg-fragment"}:
            uri = quote(_data_uri(_asset_path(value, values_base)), safe=":/,;=+")
            style = _set_style(cell.get("style", ""), "shape", "image")
            style = _set_style(style, "image", uri)
            cell.set("style", style)
    output.parent.mkdir(parents=True, exist_ok=True)
    tree.write(output, encoding="utf-8", xml_declaration=True)


def apply_pptx(manifest_path: Path, values_path: Path, output: Path) -> None:
    script = Path(__file__).with_name("apply_pptx_template.mjs")
    command = ["node", str(script), str(manifest_path), str(values_path), str(output)]
    try:
        subprocess.run(command, check=True)
    except FileNotFoundError as exc:
        raise ManifestError("Node.js is required for PPTX template replacement") from exc
    except subprocess.CalledProcessError as exc:
        raise ManifestError(f"pptx-automizer failed with exit code {exc.returncode}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--values", required=True)
    parser.add_argument("--format", choices=("svg", "drawio", "pptx"), required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    manifest_path = Path(args.manifest).resolve()
    values_path = Path(args.values).resolve()
    output = Path(args.output).resolve()
    try:
        manifest, manifest_base = load_manifest(manifest_path)
        values = read_json(values_path)
        if args.format == "svg":
            apply_svg(manifest, manifest_base, values, values_path.parent, output)
        elif args.format == "drawio":
            apply_drawio(manifest, manifest_base, values, values_path.parent, output)
        else:
            template_path(manifest, manifest_base, "pptx")
            apply_pptx(manifest_path, values_path, output)
    except ManifestError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(f"Wrote editable {args.format.upper()}: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
