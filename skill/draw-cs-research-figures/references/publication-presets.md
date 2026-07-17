# Publication presets

`scripts/conference_presets.py` provides practical starting presets for `cvpr`, `neurips`, `icml`, `acl`, `ieee`, and `zh-thesis`.

Each preset controls single/double-column width, font fallback, base font size, DPI, editable SVG text, Type-42 PDF fonts, and a restrained colorblind-friendly palette. Use:

```bash
python scripts/plot_experiments.py --input results.csv --kind auto --preset cvpr --layout double --out-prefix figure
```

Conference author kits change. Verify the current official template before final submission; treat these values as reproducible defaults rather than legal submission specifications.
