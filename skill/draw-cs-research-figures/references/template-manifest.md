# Unified editable template manifest

Use one `template_manifest.json` to map semantic slots to format-specific element identifiers.

```json
{
  "schema_version": "1.0",
  "template_id": "multimodal-method",
  "templates": {
    "svg": "template.svg",
    "drawio": "template.drawio",
    "pptx": {"path": "template.pptx", "slides": [1]}
  },
  "slots": [
    {
      "id": "figure_title",
      "kind": "text",
      "required": true,
      "selectors": {
        "svg": {"element_id": "figure-title"},
        "drawio": {"cell_id": "figure-title"},
        "pptx": {"slide": 1, "shape": "FIGURE_TITLE"}
      }
    },
    {
      "id": "local_illustration",
      "kind": "image",
      "selectors": {
        "svg": {"element_id": "local-illustration"},
        "drawio": {"cell_id": "local-illustration"},
        "pptx": {"slide": 1, "shape": "LOCAL_ILLUSTRATION", "fit": "cover"}
      }
    }
  ]
}
```

Replacement values are a JSON object keyed by slot ID. Relative asset paths resolve from the values file.

For PPTX, name template shapes in PowerPoint's Selection Pane. Install the optional Node dependency with `npm install`, then run `scripts/apply_template.py`. PPTX modification uses `pptx-automizer`; SVG and Draw.io use the Python standard library.

Save Draw.io templates as uncompressed XML. SVG fragment replacement remains vector-editable; image replacement remains an individually selectable image object.

