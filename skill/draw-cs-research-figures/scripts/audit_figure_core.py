#!/usr/bin/env python3
"""Audit scientific figures for layout, glyph, grayscale, DPI, and PDF-font issues."""
from __future__ import annotations

import argparse
import json
import logging
import math
import re
import sys
import warnings
from pathlib import Path
from xml.etree import ElementTree as ET


SEVERITY = {"INFO": 0, "WARN": 1, "FAIL": 2}
MOJIBAKE_MARKERS = ("�", "锟", "闂", "Ã", "Â", "â€", "æ–", "çš")
CJK_RE = re.compile(r"[\u3400-\u9fff]")
HEX_RE = re.compile(r"#[0-9a-fA-F]{6}")
NUMBER_RE = re.compile(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?")


def issue(severity, code, message, path=None):
    return {"severity": severity, "code": code, "message": message, "path": str(path) if path else None}


def _float(value, default=None):
    if value is None:
        return default
    match = NUMBER_RE.search(str(value))
    return float(match.group()) if match else default


def _hex_rgb(value):
    value = value.lstrip("#")
    return tuple(int(value[i:i+2], 16) / 255 for i in (0, 2, 4))


def _luminance(value):
    rgb = _hex_rgb(value)
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def _saturation(value):
    rgb = _hex_rgb(value)
    hi, lo = max(rgb), min(rgb)
    return 0 if hi == 0 else (hi - lo) / hi


def _style_map(element):
    result = {}
    for part in element.attrib.get("style", "").split(";"):
        key, sep, value = part.partition(":")
        if sep:
            result[key.strip()] = value.strip()
    return result


def _svg_size(root):
    viewbox = root.attrib.get("viewBox")
    if viewbox:
        parts = [float(v) for v in viewbox.replace(",", " ").split()]
        if len(parts) == 4:
            return parts
    return [0.0, 0.0, _float(root.attrib.get("width"), 0.0), _float(root.attrib.get("height"), 0.0)]


def _svg_text_box(element):
    text = "".join(element.itertext()).strip()
    x, y = _float(element.attrib.get("x")), _float(element.attrib.get("y"))
    if x is None or y is None or not text:
        return None
    style = _style_map(element)
    size = _float(element.attrib.get("font-size"), _float(style.get("font-size"), 10.0))
    anchor = element.attrib.get("text-anchor", style.get("text-anchor", "start"))
    width = max(size * 0.52 * len(text), size * 0.6)
    left = x - width / 2 if anchor == "middle" else x - width if anchor == "end" else x
    return {"left": left, "right": left + width, "top": y - size, "bottom": y + size * 0.25, "text": text[:60]}


def _overlap(a, b, tolerance=1.0):
    return min(a["right"], b["right"]) - max(a["left"], b["left"]) > tolerance and min(a["bottom"], b["bottom"]) - max(a["top"], b["top"]) > tolerance


def audit_svg(path):
    issues = []
    try:
        root = ET.parse(path).getroot()
    except Exception as exc:
        return [issue("FAIL", "svg-parse", f"SVG cannot be parsed: {exc}", path)]
    x0, y0, width, height = _svg_size(root)
    boxes, colors, text_content = [], set(), []
    has_redundant_encoding = False
    for element in root.iter():
        tag = element.tag.rsplit("}", 1)[-1]
        style = _style_map(element)
        if tag == "text":
            box = _svg_text_box(element)
            if box:
                boxes.append(box); text_content.append(box["text"])
            transform = element.attrib.get("transform", "")
            for angle in re.findall(r"rotate\(([-+\d.]+)", transform):
                value = abs(float(angle)) % 180
                if min(value, abs(value - 90), abs(value - 180)) > 0.1:
                    issues.append(issue("FAIL", "diagonal-text", f"Diagonal text rotation detected: {angle}°", path))
        if element.attrib.get("stroke-dasharray") or style.get("stroke-dasharray") not in (None, "none"):
            has_redundant_encoding = True
        if tag in {"marker", "circle", "polygon"}:
            has_redundant_encoding = True
        for key in ("fill", "stroke"):
            value = element.attrib.get(key) or style.get(key)
            if value and HEX_RE.fullmatch(value):
                colors.add(value.lower())

    margin = 1.5
    clipped = [b["text"] for b in boxes if b["left"] < x0-margin or b["right"] > x0+width+margin or b["top"] < y0-margin or b["bottom"] > y0+height+margin]
    if clipped:
        issues.append(issue("FAIL", "text-clipping", f"Text may be outside the SVG viewBox: {clipped[:6]}", path))

    overlaps = []
    for i, a in enumerate(boxes):
        for b in boxes[i+1:]:
            if _overlap(a, b, tolerance=1.2) and a["text"] != b["text"]:
                overlaps.append((a["text"], b["text"]))
                if len(overlaps) >= 8:
                    break
        if len(overlaps) >= 8:
            break
    if overlaps:
        issues.append(issue("WARN", "label-overlap", f"Estimated overlapping text labels: {overlaps}", path))

    joined = " ".join(text_content)
    bad = [m for m in MOJIBAKE_MARKERS if m in joined]
    if bad:
        issues.append(issue("FAIL", "mojibake", f"Likely encoding corruption markers found: {bad}", path))
    if CJK_RE.search(joined):
        family_text = " ".join((e.attrib.get("font-family", "") + " " + _style_map(e).get("font-family", "")) for e in root.iter())
        if not any(name.lower() in family_text.lower() for name in ("cjk", "yahei", "simhei", "simsun", "source han", "noto", "pingfang", "songti")):
            issues.append(issue("WARN", "cjk-font-fallback", "Chinese text exists but no explicit CJK-capable font family was found", path))

    chromatic = sorted(c for c in colors if _saturation(c) >= 0.18 and 0.04 < _luminance(c) < 0.92)
    close = []
    for i, a in enumerate(chromatic):
        for b in chromatic[i+1:]:
            if abs(_luminance(a) - _luminance(b)) < 0.065:
                close.append((a, b))
    if close and not has_redundant_encoding:
        issues.append(issue("WARN", "grayscale-ambiguity", f"Colors have similar grayscale luminance without redundant line/marker encoding: {close[:6]}", path))
    elif close:
        issues.append(issue("INFO", "grayscale-redundancy", f"Similar grayscale colors are backed by markers/dashes: {close[:6]}", path))
    return issues


def audit_raster(path, min_dpi=300):
    issues = []
    try:
        from PIL import Image
        image = Image.open(path)
    except Exception as exc:
        return [issue("FAIL", "raster-read", f"Raster image cannot be read: {exc}", path)]
    dpi = image.info.get("dpi")
    if not dpi:
        issues.append(issue("WARN", "dpi-missing", "Raster file has no embedded DPI metadata", path))
    else:
        actual = round(float(dpi[0] if isinstance(dpi, tuple) else dpi))
        if actual < min_dpi:
            issues.append(issue("FAIL", "dpi-low", f"DPI {actual} is below required {min_dpi}", path))
    return issues


def audit_pdf(path):
    issues = []
    try:
        from pypdf import PdfReader
    except ImportError:
        try:
            from PyPDF2 import PdfReader
        except ImportError:
            return [issue("WARN", "pdf-check-unavailable", "Install pypdf to check PDF font embedding", path)]
    try:
        reader = PdfReader(str(path))
        fonts_seen = 0
        for page in reader.pages:
            resources = page.get("/Resources")
            if not resources:
                continue
            fonts = resources.get("/Font")
            if not fonts:
                continue
            fonts = fonts.get_object() if hasattr(fonts, "get_object") else fonts
            for _, ref in fonts.items():
                font = ref.get_object(); fonts_seen += 1
                subtype = str(font.get("/Subtype", "")); base = str(font.get("/BaseFont", "unknown"))
                descriptor = font.get("/FontDescriptor")
                descriptor = descriptor.get_object() if descriptor and hasattr(descriptor, "get_object") else descriptor
                embedded = bool(descriptor and any(k in descriptor for k in ("/FontFile", "/FontFile2", "/FontFile3")))
                if "Type3" in subtype:
                    issues.append(issue("FAIL", "pdf-type3-font", f"Type 3 font found: {base}", path))
                elif not embedded and "Type1" not in subtype:
                    issues.append(issue("WARN", "pdf-font-not-embedded", f"Font may not be embedded: {base}", path))
        if not fonts_seen:
            issues.append(issue("INFO", "pdf-no-font-objects", "No PDF font objects found; text may be outlined", path))
    except Exception as exc:
        issues.append(issue("WARN", "pdf-parse", f"PDF font audit failed: {exc}", path))
    return issues


class _GlyphHandler(logging.Handler):
    def __init__(self):
        super().__init__(); self.messages = []
    def emit(self, record):
        message = record.getMessage()
        if "missing from font" in message or "Glyph" in message:
            self.messages.append(message)


def audit_matplotlib_figure(fig):
    """Run deterministic pre-export checks on a Matplotlib Figure object."""
    import matplotlib.text as mtext
    issues = []
    handler = _GlyphHandler(); logger = logging.getLogger("matplotlib"); logger.addHandler(handler)
    caught = []
    try:
        with warnings.catch_warnings(record=True) as records:
            warnings.simplefilter("always"); fig.canvas.draw(); caught = [str(r.message) for r in records]
    finally:
        logger.removeHandler(handler)
    glyphs = [m for m in caught + handler.messages if "missing from font" in m or "Glyph" in m]
    if glyphs:
        issues.append(issue("FAIL", "missing-glyph", f"Missing glyph/font warnings: {glyphs[:4]}"))
    renderer = fig.canvas.get_renderer(); width, height = fig.bbox.width, fig.bbox.height
    texts = [t for t in fig.findobj(mtext.Text) if t.get_visible() and t.get_text().strip()]
    clipped = []
    for text in texts:
        box = text.get_window_extent(renderer)
        if box.x0 < -2 or box.y0 < -2 or box.x1 > width+2 or box.y1 > height+2:
            clipped.append(text.get_text().replace("\n", " ")[:50])
    if clipped:
        issues.append(issue("FAIL", "text-clipping", f"Text outside canvas: {clipped[:8]}"))
    overlap_count = 0
    for ax in fig.axes:
        for labels, axis in ((ax.get_xticklabels(), "x"), (ax.get_yticklabels(), "y")):
            boxes = [label.get_window_extent(renderer) for label in labels if label.get_visible() and label.get_text().strip()]
            boxes.sort(key=lambda b: b.x0 if axis == "x" else b.y0)
            if any((a.x1 > b.x0+1 if axis == "x" else a.y1 > b.y0+1) for a, b in zip(boxes, boxes[1:])):
                overlap_count += 1
    if overlap_count:
        issues.append(issue("WARN", "tick-overlap", f"Overlapping tick labels detected on {overlap_count} axis/axes"))
    return issues


def audit_path(path, min_dpi=300):
    path = Path(path); ext = path.suffix.lower()
    if not path.exists():
        return [issue("FAIL", "missing-file", "File does not exist", path)]
    if ext == ".svg": return audit_svg(path)
    if ext in {".png", ".tif", ".tiff", ".jpg", ".jpeg"}: return audit_raster(path, min_dpi)
    if ext == ".pdf": return audit_pdf(path)
    return [issue("WARN", "unsupported-format", f"No audit rules for {ext}", path)]


def verdict(issues):
    if not issues: return "PASS"
    level = max(SEVERITY[i["severity"]] for i in issues)
    return {0: "INFO", 1: "WARN", 2: "FAIL"}[level]


def print_report(path, issues):
    result = verdict(issues); print(f"\n--- {path} [{result}] ---")
    if not issues: print("[PASS] no deterministic issues found")
    for item in sorted(issues, key=lambda x: -SEVERITY[x["severity"]]):
        print(f"[{item['severity']}] {item['code']}: {item['message']}")
    return result


def main():
    parser = argparse.ArgumentParser(description="Audit exported scientific figures")
    parser.add_argument("paths", nargs="+"); parser.add_argument("--min-dpi", type=int, default=300)
    parser.add_argument("--strict", action="store_true"); parser.add_argument("--json-out")
    args = parser.parse_args(); reports = []; any_fail = False
    for path in args.paths:
        issues = audit_path(path, args.min_dpi); result = print_report(path, issues)
        reports.append({"path": path, "verdict": result, "issues": issues}); any_fail |= result == "FAIL"
    if args.json_out:
        Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json_out).write_text(json.dumps(reports, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.strict and any_fail: raise SystemExit(2)


if __name__ == "__main__": main()
