#!/usr/bin/env python3
"""Public audit interface with safe SVG, raster, and PDF fallbacks."""
from __future__ import annotations

from pathlib import Path

import audit_figure_core as _core


_base_text_box = _core._svg_text_box
_base_pdf_audit = _core.audit_pdf


def _transform_safe_text_box(element):
    if element.attrib.get("transform"):
        return None
    return _base_text_box(element)


def audit_raster(path, min_dpi=300):
    issues = []
    try:
        from PIL import Image
        with Image.open(path) as image:
            dpi = image.info.get("dpi")
    except Exception as exc:
        return [_core.issue("FAIL", "raster-read", f"Raster image cannot be read: {exc}", path)]
    if not dpi:
        issues.append(_core.issue("WARN", "dpi-missing", "Raster file has no embedded DPI metadata", path))
    else:
        actual = round(float(dpi[0] if isinstance(dpi, tuple) else dpi))
        if actual < min_dpi:
            issues.append(_core.issue("FAIL", "dpi-low", f"DPI {actual} is below required {min_dpi}", path))
    return issues


def audit_pdf(path):
    data = Path(path).read_bytes()
    issues = _base_pdf_audit(path)
    embedded_marker = any(marker in data for marker in (b"/FontFile ", b"/FontFile2", b"/FontFile3"))
    if embedded_marker:
        issues = [item for item in issues if item["code"] != "pdf-font-not-embedded"]
    if not any(item["code"] == "pdf-check-unavailable" for item in issues):
        return issues
    issues = [item for item in issues if item["code"] != "pdf-check-unavailable"]
    if b"/Type3" in data:
        issues.append(_core.issue("FAIL", "pdf-type3-font", "Type 3 font marker found in PDF", path))
    font_objects = data.count(b"/Type /Font") + data.count(b"/Type/Font")
    if font_objects and not embedded_marker:
        issues.append(_core.issue("WARN", "pdf-font-not-embedded", "PDF font objects were found but no embedded font stream marker was detected", path))
    if not font_objects:
        issues.append(_core.issue("INFO", "pdf-no-font-objects", "No PDF font objects found; text may be outlined", path))
    return issues


_core._svg_text_box = _transform_safe_text_box
_core.audit_raster = audit_raster
_core.audit_pdf = audit_pdf

SEVERITY = _core.SEVERITY
audit_svg = _core.audit_svg
audit_matplotlib_figure = _core.audit_matplotlib_figure
audit_path = _core.audit_path
verdict = _core.verdict
print_report = _core.print_report
main = _core.main


if __name__ == "__main__":
    main()
