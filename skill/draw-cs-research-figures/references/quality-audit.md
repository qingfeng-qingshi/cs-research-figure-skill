# Automatic figure audit

Use `scripts/audit_figure.py` after every export. It checks:

- SVG text outside the viewBox and estimated label collisions.
- diagonal text, encoding-corruption markers, and missing CJK font fallbacks.
- grayscale luminance collisions and whether markers/dashes provide redundant encoding.
- PNG/TIFF embedded DPI.
- PDF Type-3 and potentially unembedded fonts.

For Matplotlib, call `audit_matplotlib_figure(fig)` before `savefig` to catch renderer-level clipping, overlapping ticks, and missing-glyph warnings. File-level SVG estimation is conservative: a warning requires visual review, while a failure must be fixed before delivery.

```python
from audit_figure import audit_matplotlib_figure, verdict
issues = audit_matplotlib_figure(fig)
if verdict(issues) == "FAIL":
    raise RuntimeError(issues)
```

Run a strict exported-file audit:

```bash
python scripts/audit_figure.py figure.svg figure.pdf figure.png --min-dpi 300 --strict --json-out figure-audit.json
```
