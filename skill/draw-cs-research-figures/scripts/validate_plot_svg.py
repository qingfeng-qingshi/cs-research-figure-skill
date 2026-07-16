#!/usr/bin/env python3
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

NEUTRAL = {"#ffffff", "#203040", "#5f7182", "#dce4ea", "#93a5b4"}

def style_fill(style):
    for part in style.split(";"):
        key, sep, value = part.partition(":")
        if sep and key.strip() == "fill":
            return value.strip().lower()
    return None

def main(path):
    root = ET.parse(path).getroot()
    errors, angles, fills = [], [], set()
    for element in root.iter():
        transform = element.attrib.get("transform", "")
        marker = "rotate("
        if marker in transform:
            payload = transform.split(marker, 1)[1].split(")", 1)[0]
            angle = float(payload.split(",", 1)[0].strip())
            angles.append(angle)
        direct = element.attrib.get("fill")
        styled = style_fill(element.attrib.get("style", ""))
        for value in (direct, styled):
            if value and value.startswith("#") and len(value) == 7:
                fills.add(value.lower())
    nonzero = [value for value in angles if min(abs(value), abs(abs(value)-90)) > 0.01]
    if nonzero:
        errors.append("diagonal text rotations: " + ", ".join(map(str, nonzero)))
    chromatic = fills - NEUTRAL
    if len(chromatic) < 3:
        errors.append(f"palette too narrow: {len(chromatic)} chromatic colors")
    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print(f"Plot SVG valid: no diagonal text; {len(chromatic)} chromatic colors")
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: validate_plot_svg.py FIGURE.svg")
    raise SystemExit(main(sys.argv[1]))
