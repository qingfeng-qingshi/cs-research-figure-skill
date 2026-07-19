#!/usr/bin/env python3
"""Generate the complex editable SVG/Draw.io template demo and its manifest."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "examples" / "templates"


def write(name: str, content: str):
    (OUT / name).write_text(content.strip() + "\n", encoding="utf-8")


def svg_template():
    return r'''<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1000" viewBox="0 0 1800 1000">
<defs>
  <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0L10 5L0 10z" fill="context-stroke"/></marker>
  <filter id="shadow" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#20364A" flood-opacity=".10"/></filter>
</defs>
<rect width="1800" height="1000" fill="#FFFFFF"/>
<text id="figure-title" x="900" y="55" text-anchor="middle" font-family="Arial" font-size="31" font-weight="700" fill="#172B4D">{{FIGURE_TITLE}}</text>

<g id="zones" font-family="Arial" fill="#172B4D">
  <rect x="30" y="92" width="300" height="820" rx="24" fill="#F3F7FA" stroke="#C9D6DF" stroke-width="2"/>
  <rect x="355" y="92" width="430" height="820" rx="24" fill="#EDF5FA" stroke="#C9D6DF" stroke-width="2"/>
  <rect x="810" y="92" width="650" height="820" rx="24" fill="#F7F2FA" stroke="#D7CADF" stroke-width="2"/>
  <rect x="1485" y="92" width="285" height="820" rx="24" fill="#F2F8F1" stroke="#CCDCCB" stroke-width="2"/>
  <text x="52" y="132" font-size="23" font-weight="700">Multimodal Inputs</text>
  <text x="378" y="132" font-size="23" font-weight="700">View-specific Encoding</text>
  <text x="833" y="132" font-size="23" font-weight="700">Graph-Guided Fusion &amp; Zoom-in</text>
  <text x="1508" y="132" font-size="23" font-weight="700">Predictions &amp; Objectives</text>
</g>

<g id="connectors" fill="none" stroke="#47789E" stroke-width="4" marker-end="url(#arrow)">
  <path d="M285 245 L410 245"/><path d="M285 490 L410 490"/><path d="M285 745 L410 745"/>
  <path d="M725 245 L870 245"/><path d="M725 490 L870 360"/><path d="M725 745 L1120 360"/>
  <path d="M1065 270 L1120 270"/><path d="M1000 400 L1000 500"/><path d="M1240 400 L1185 500"/>
  <path d="M1110 700 L1110 785"/><path d="M1270 650 L1510 250"/><path d="M1270 695 L1510 480"/>
</g>
<g id="objective-connectors" fill="none" stroke-width="3" stroke-dasharray="10 8" marker-end="url(#arrow)">
  <path d="M1625 330 L1625 675" stroke="#C96E66"/><path d="M1000 400 L1560 785" stroke="#8062A8"/><path d="M1240 400 L1675 785" stroke="#55945B"/>
</g>

<g id="input-cards" filter="url(#shadow)" font-family="Arial" text-anchor="middle" fill="#172B4D">
  <rect x="70" y="165" width="215" height="160" rx="16" fill="#E1EEF6" stroke="#426986" stroke-width="2.5"/><text x="177" y="302" font-size="19" font-weight="600">Image / Document</text>
  <rect x="70" y="410" width="215" height="160" rx="16" fill="#EEF0F7" stroke="#5D6F91" stroke-width="2.5"/><g transform="translate(100 447)"><rect width="22" height="54" rx="4" fill="#76B7D8"/><rect x="30" y="10" width="22" height="44" rx="4" fill="#90C6A0"/><rect x="60" y="0" width="22" height="54" rx="4" fill="#E9B66C"/><rect x="90" y="14" width="22" height="40" rx="4" fill="#B39AD5"/><rect x="120" y="5" width="22" height="49" rx="4" fill="#76B7D8"/></g><text x="177" y="548" font-size="19" font-weight="600">Text Tokens</text>
  <rect x="70" y="655" width="215" height="180" rx="16" fill="#EEF5EA" stroke="#5A805E" stroke-width="2.5"/><circle cx="125" cy="720" r="12" fill="#8FC2DC"/><circle cx="180" cy="692" r="12" fill="#F0BC8C"/><circle cx="230" cy="735" r="12" fill="#B8D7A8"/><circle cx="165" cy="785" r="12" fill="#C2AEDC"/><path d="M125 720L180 692L230 735L165 785L125 720M180 692L165 785" fill="none" stroke="#355D78" stroke-width="3"/><text x="177" y="817" font-size="19" font-weight="600">Metadata Graph</text>
</g>

<g id="encoder-cards" filter="url(#shadow)" font-family="Arial" text-anchor="middle" fill="#172B4D">
  <rect x="410" y="160" width="315" height="180" rx="17" fill="#D9ECF5" stroke="#426986" stroke-width="2.5"/><image id="visual-tensor-slot" x="455" y="182" width="225" height="100" preserveAspectRatio="xMidYMid meet"/><text id="visual-label" x="567" y="318" font-size="18" font-weight="600">{{VISUAL_ENCODER}}</text>
  <rect x="410" y="395" width="315" height="205" rx="17" fill="#E3EBF3" stroke="#426986" stroke-width="2.5"/><g transform="translate(445 425)"><rect x="18" y="18" width="215" height="105" rx="9" fill="#D5E0EA" stroke="#426986"/><rect x="9" y="9" width="215" height="105" rx="9" fill="#E2EAF1" stroke="#426986"/><rect width="215" height="105" rx="9" fill="#F0F4F7" stroke="#426986"/><rect x="20" y="18" width="175" height="25" rx="4" fill="#F3A37E"/><rect x="20" y="55" width="175" height="19" rx="4" fill="#9BCF9B"/><rect x="20" y="83" width="175" height="16" rx="4" fill="#AFC7DC"/></g><text id="language-label" x="567" y="577" font-size="18" font-weight="600">{{LANGUAGE_ENCODER}}</text>
  <rect x="410" y="655" width="315" height="180" rx="17" fill="#E2F0E0" stroke="#5A805E" stroke-width="2.5"/><image id="graph-slot" x="455" y="680" width="225" height="105" preserveAspectRatio="xMidYMid meet"/><text id="graph-label" x="567" y="815" font-size="18" font-weight="600">{{GRAPH_ENCODER}}</text>
</g>

<g id="fusion-cards" filter="url(#shadow)" font-family="Arial" text-anchor="middle" fill="#172B4D">
  <rect x="870" y="160" width="195" height="240" rx="17" fill="#F7DFD3" stroke="#C77945" stroke-width="2.5"/><image id="attention-slot" x="900" y="188" width="135" height="120" preserveAspectRatio="xMidYMid meet"/><text x="967" y="343" font-size="17" font-weight="600">Cross-modal</text><text x="967" y="365" font-size="17" font-weight="600">Attention</text>
  <rect x="1120" y="160" width="240" height="240" rx="17" fill="#E6F1E3" stroke="#55945B" stroke-width="2.5"/><circle cx="1175" cy="250" r="11" fill="#8FC2DC"/><circle cx="1230" cy="205" r="11" fill="#F0BC8C"/><circle cx="1300" cy="245" r="11" fill="#B8D7A8"/><circle cx="1210" cy="325" r="11" fill="#C2AEDC"/><circle cx="1305" cy="325" r="11" fill="#F2A7A7"/><path d="M1175 250L1230 205L1300 245L1305 325L1210 325L1175 250M1230 205L1210 325M1300 245L1210 325" fill="none" stroke="#355D78" stroke-width="3"/><text x="1240" y="372" font-size="17" font-weight="600">Relation Graph</text>
  <rect x="930" y="500" width="360" height="210" rx="20" fill="#E9DFF2" stroke="#7E5AA6" stroke-width="3"/><rect x="975" y="535" width="270" height="38" rx="6" fill="#F3A37E"/><rect x="975" y="586" width="270" height="38" rx="6" fill="#9BCF9B"/><rect x="975" y="637" width="270" height="38" rx="6" fill="#AFC7DC"/><text x="1110" y="560" font-size="15">Graph-conditioned Gating</text><text x="1110" y="611" font-size="15">Residual Alignment</text><text x="1110" y="662" font-size="15">Adaptive Normalization</text><text id="fusion-label" x="1110" y="696" font-size="18" font-weight="700">{{FUSION_MODULE}}</text>
  <rect x="955" y="785" width="310" height="95" rx="15" fill="#D9E8F4" stroke="#426986" stroke-width="2.5"/><g transform="translate(990 810)"><rect x="24" y="10" width="190" height="36" rx="4" fill="#A9D5E8" stroke="#426986"/><rect x="12" y="5" width="190" height="36" rx="4" fill="#C5E3F0" stroke="#426986"/><rect width="190" height="36" rx="4" fill="#D8EEF5" stroke="#426986"/></g><text x="1110" y="866" font-size="17" font-weight="600">Joint Representation</text>
  <rect x="845" y="475" width="480" height="260" rx="24" fill="none" stroke="#A25B8B" stroke-width="3" stroke-dasharray="9 7"/><text x="860" y="463" text-anchor="start" font-size="17" font-weight="700" fill="#A25B8B">Innovation zoom-in</text>
</g>

<g id="output-cards" filter="url(#shadow)" font-family="Arial" text-anchor="middle" fill="#172B4D">
  <rect x="1510" y="170" width="235" height="160" rx="17" fill="#E1F1DF" stroke="#55945B" stroke-width="2.5"/><path d="M1545 285V210M1545 285H1710" stroke="#355D78" stroke-width="2"/><rect x="1570" y="245" width="24" height="40" fill="#AFC7DC"/><rect x="1610" y="225" width="24" height="60" fill="#76B7D8"/><rect x="1650" y="195" width="24" height="90" fill="#55945B"/><text id="prediction-label" x="1627" y="315" font-size="18" font-weight="600">{{PREDICTION_HEAD}}</text>
  <rect x="1510" y="410" width="235" height="165" rx="17" fill="#F5ECD8" stroke="#B98B42" stroke-width="2.5"/><circle cx="1570" cy="480" r="12" fill="#8FC2DC"/><circle cx="1625" cy="445" r="12" fill="#F0BC8C"/><circle cx="1690" cy="485" r="12" fill="#B8D7A8"/><circle cx="1625" cy="535" r="12" fill="#C2AEDC"/><path d="M1570 480L1625 445L1690 485L1625 535L1570 480M1625 445L1625 535" fill="none" stroke="#355D78" stroke-width="3"/><text x="1627" y="558" font-size="17" font-weight="600">Graph Explanation</text>
  <rect x="1515" y="660" width="220" height="60" rx="26" fill="#F8DFDC" stroke="#C96E66" stroke-width="2.5"/><text id="task-loss-label" x="1625" y="698" font-size="17" font-weight="600">{{TASK_LOSS}}</text>
  <rect x="1515" y="755" width="220" height="60" rx="26" fill="#E9E0F4" stroke="#8062A8" stroke-width="2.5"/><text id="align-loss-label" x="1625" y="793" font-size="17" font-weight="600">{{ALIGNMENT_LOSS}}</text>
  <rect x="1515" y="845" width="220" height="60" rx="26" fill="#E3F0E0" stroke="#55945B" stroke-width="2.5"/><text x="1625" y="883" font-size="17" font-weight="600">Graph Regularization</text>
</g>

<g font-family="Arial" font-size="15" fill="#52677D" text-anchor="middle"><text x="348" y="230">patches</text><text x="348" y="475">tokens</text><text x="348" y="730">nodes</text><text x="795" y="230">visual tokens</text><text x="795" y="432">text tokens</text><text x="820" y="710">structural prior</text></g>
</svg>'''


def drawio_template():
    cells = [
        '<mxCell id="0"/>', '<mxCell id="1" parent="0"/>',
        '<mxCell id="figure-title" value="{{FIGURE_TITLE}}" style="text;html=1;align=center;fontSize=24;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="500" y="20" width="800" height="50" as="geometry"/></mxCell>',
    ]
    zones = [
        ("zone-input", "Multimodal Inputs", 30, 90, 300, 820, "#f3f7fa", "#c9d6df"),
        ("zone-encoder", "View-specific Encoding", 355, 90, 430, 820, "#edf5fa", "#c9d6df"),
        ("zone-fusion", "Graph-Guided Fusion &amp; Zoom-in", 810, 90, 650, 820, "#f7f2fa", "#d7cadf"),
        ("zone-output", "Predictions &amp; Objectives", 1485, 90, 285, 820, "#f2f8f1", "#ccdccb"),
    ]
    for ident, label, x, y, w, h, fill, stroke in zones:
        cells.append(f'<mxCell id="{ident}" value="{label}" style="rounded=1;whiteSpace=wrap;html=1;verticalAlign=top;spacingTop=12;fontStyle=1;fontSize=18;fillColor={fill};strokeColor={stroke};" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    nodes = [
        ("image-input", "Image / Document", 70, 165, 215, 160, "#e1eef6", "#426986"),
        ("text-input", "Text Tokens", 70, 410, 215, 160, "#eef0f7", "#5d6f91"),
        ("graph-input", "Metadata Graph", 70, 655, 215, 180, "#eef5ea", "#5a805e"),
        ("visual-encoder", "{{VISUAL_ENCODER}}", 410, 160, 315, 180, "#d9ecf5", "#426986"),
        ("language-encoder", "{{LANGUAGE_ENCODER}}", 410, 395, 315, 205, "#e3ebf3", "#426986"),
        ("graph-encoder", "{{GRAPH_ENCODER}}", 410, 655, 315, 180, "#e2f0e0", "#5a805e"),
        ("attention", "Cross-modal Attention", 870, 160, 195, 240, "#f7dfd3", "#c77945"),
        ("relation", "Relation Graph", 1120, 160, 240, 240, "#e6f1e3", "#55945b"),
        ("fusion-module", "{{FUSION_MODULE}}", 930, 500, 360, 210, "#e9dff2", "#7e5aa6"),
        ("joint", "Joint Representation", 955, 785, 310, 95, "#d9e8f4", "#426986"),
        ("prediction", "{{PREDICTION_HEAD}}", 1510, 170, 235, 160, "#e1f1df", "#55945b"),
        ("explanation", "Graph Explanation", 1510, 410, 235, 165, "#f5ecd8", "#b98b42"),
        ("task-loss", "{{TASK_LOSS}}", 1515, 660, 220, 60, "#f8dfdc", "#c96e66"),
        ("align-loss", "{{ALIGNMENT_LOSS}}", 1515, 755, 220, 60, "#e9e0f4", "#8062a8"),
        ("graph-loss", "Graph Regularization", 1515, 845, 220, 60, "#e3f0e0", "#55945b"),
    ]
    for ident, label, x, y, w, h, fill, stroke in nodes:
        cells.append(f'<mxCell id="{ident}" value="{label}" style="rounded=1;whiteSpace=wrap;html=1;fontSize=15;fontStyle=1;fillColor={fill};strokeColor={stroke};strokeWidth=2;" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    for ident, x, y, w, h in [("visual-tensor-slot", 455, 182, 225, 95), ("graph-slot", 455, 680, 225, 100), ("attention-slot", 900, 188, 135, 115)]:
        cells.append(f'<mxCell id="{ident}" value="" style="shape=image;imageAspect=0;aspect=fixed;" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    edges = [("image-input","visual-encoder"),("text-input","language-encoder"),("graph-input","graph-encoder"),("visual-encoder","attention"),("language-encoder","attention"),("graph-encoder","relation"),("attention","fusion-module"),("relation","fusion-module"),("fusion-module","joint"),("joint","prediction"),("joint","explanation"),("prediction","task-loss")]
    for index, (source, target) in enumerate(edges, 1):
        cells.append(f'<mxCell id="edge-{index}" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=block;strokeColor=#47789e;strokeWidth=2;" edge="1" parent="1" source="{source}" target="{target}"><mxGeometry relative="1" as="geometry"/></mxCell>')
    return '<?xml version="1.0" encoding="UTF-8"?>\n<mxfile host="app.diagrams.net" compressed="false"><diagram id="complex" name="Complex Method"><mxGraphModel dx="1800" dy="1000" grid="1" gridSize="10" page="1" pageWidth="1800" pageHeight="1000"><root>\n' + "\n".join(cells) + '\n</root></mxGraphModel></diagram></mxfile>'


def manifest():
    text_slots = [
        ("figure_title", "figure-title", "figure-title", "FIGURE_TITLE"),
        ("visual_encoder", "visual-label", "visual-encoder", "VISUAL_ENCODER"),
        ("language_encoder", "language-label", "language-encoder", "LANGUAGE_ENCODER"),
        ("graph_encoder", "graph-label", "graph-encoder", "GRAPH_ENCODER"),
        ("fusion_module", "fusion-label", "fusion-module", "FUSION_MODULE"),
        ("prediction_head", "prediction-label", "prediction", "PREDICTION_HEAD"),
        ("task_loss", "task-loss-label", "task-loss", "TASK_LOSS"),
        ("alignment_loss", "align-loss-label", "align-loss", "ALIGNMENT_LOSS"),
    ]
    slots = []
    for slot_id, svg_id, drawio_id, pptx_name in text_slots:
        slots.append({"id": slot_id, "kind": "text", "required": True, "selectors": {"svg": {"element_id": svg_id}, "drawio": {"cell_id": drawio_id}, "pptx": {"slide": 1, "shape": pptx_name}}})
    for slot_id, target, pptx_name in [("visual_tensor", "visual-tensor-slot", "VISUAL_TENSOR"), ("graph_illustration", "graph-slot", "GRAPH_ILLUSTRATION"), ("attention_map", "attention-slot", "ATTENTION_MAP")]:
        slots.append({"id": slot_id, "kind": "image", "selectors": {"svg": {"element_id": target}, "drawio": {"cell_id": target}, "pptx": {"slide": 1, "shape": pptx_name}}})
    return {"schema_version": "1.0", "template_id": "complex-graph-guided-multimodal-demo", "templates": {"svg": "template.svg", "drawio": "template.drawio", "pptx": {"path": "template.pptx", "slides": [1]}}, "slots": slots}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    write("template.svg", svg_template())
    write("template.drawio", drawio_template())
    (OUT / "template_manifest.json").write_text(json.dumps(manifest(), ensure_ascii=False, indent=2), encoding="utf-8")
    values = {
        "figure_title": "Graph-Guided Multimodal Learning with Adaptive Relation Fusion",
        "visual_encoder": "Multi-scale Vision Encoder",
        "language_encoder": "Contextual Language Encoder",
        "graph_encoder": "Relational Graph Encoder",
        "fusion_module": "Adaptive Graph-Guided Fusion",
        "prediction_head": "Task Prediction Head",
        "task_loss": "Task Supervision",
        "alignment_loss": "Cross-modal Alignment",
        "visual_tensor": "tensor-stack.svg",
        "graph_illustration": "replacement-icon.svg",
        "attention_map": "attention-map.svg"
    }
    (OUT / "replacement_values.json").write_text(json.dumps(values, ensure_ascii=False, indent=2), encoding="utf-8")
    write("tensor-stack.svg", '''<svg xmlns="http://www.w3.org/2000/svg" width="260" height="120" viewBox="0 0 260 120"><rect x="42" y="28" width="178" height="70" rx="7" fill="#D8EEF5" stroke="#355D78" stroke-width="3"/><rect x="30" y="20" width="178" height="70" rx="7" fill="#C5E3F0" stroke="#355D78" stroke-width="3"/><rect x="18" y="12" width="178" height="70" rx="7" fill="#A9D5E8" stroke="#355D78" stroke-width="3"/><g stroke="#fff" stroke-width="2"><path d="M62 12V82M106 12V82M150 12V82"/><path d="M18 35H196M18 58H196"/></g></svg>''')
    write("attention-map.svg", '''<svg xmlns="http://www.w3.org/2000/svg" width="160" height="140" viewBox="0 0 160 140"><rect x="15" y="10" width="120" height="120" rx="8" fill="#FFF8F3" stroke="#8B5B42" stroke-width="3"/><g stroke="#fff" stroke-width="2"><path d="M45 10V130M75 10V130M105 10V130M15 40H135M15 70H135M15 100H135"/></g><g fill="#F18F6D"><rect x="16" y="11" width="28" height="28"/><rect x="76" y="71" width="28" height="28"/><rect x="106" y="41" width="28" height="28"/></g><g fill="#F7C9B7"><rect x="46" y="41" width="28" height="28"/><rect x="16" y="101" width="28" height="28"/><rect x="106" y="101" width="28" height="28"/></g></svg>''')
    print(f"Wrote complex template demo sources to {OUT}")


if __name__ == "__main__":
    main()
