#!/usr/bin/env python3
"""Publication presets with grayscale-separated conference colors."""
from __future__ import annotations

import conference_presets_core as _core


_core.PALETTES["conference"] = [
    "#1B4F72",  # focal blue, low luminance
    "#D95F59",  # red
    "#8BCB88",  # light green
    "#F2C14E",  # ochre
    "#8064A2",  # violet
    "#45A6A6",  # teal
]

PALETTES = _core.PALETTES
PRESETS = _core.PRESETS
get_preset = _core.get_preset
apply_preset = _core.apply_preset


if __name__ == "__main__":
    for key in PRESETS:
        preset = get_preset(key)
        print(f"{key:10s} {preset['width']:.2f} in  {preset['font']}  {preset['dpi']} DPI")
