import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill" / "draw-cs-research-figures"
SCRIPTS = SKILL / "scripts"
DEMO = ROOT / "examples" / "templates"


class TemplateWorkflowTests(unittest.TestCase):
    def run_script(self, name, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPTS / name), *map(str, args)],
            cwd=ROOT, check=True, capture_output=True, text=True,
        )

    def test_manifest_validates(self):
        sys.path.insert(0, str(SCRIPTS))
        from template_manifest_core import load_manifest
        manifest, base = load_manifest(DEMO / "template_manifest.json")
        self.assertEqual(manifest["schema_version"], "1.0")
        self.assertEqual(base, DEMO.resolve())
        self.assertGreaterEqual(len(manifest["slots"]), 11)
        self.assertEqual(sum(slot["kind"] == "text" for slot in manifest["slots"]), 8)
        self.assertEqual(sum(slot["kind"] == "image" for slot in manifest["slots"]), 3)

    def test_svg_and_drawio_replacement(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            svg = directory / "result.svg"
            drawio = directory / "result.drawio"
            for fmt, output in (("svg", svg), ("drawio", drawio)):
                self.run_script("apply_template.py", "--manifest", DEMO / "template_manifest.json", "--values", DEMO / "replacement_values.json", "--format", fmt, "--output", output)
                self.assertGreater(output.stat().st_size, 1000)
            self.assertIn("Graph-Guided Multimodal", svg.read_text(encoding="utf-8"))
            self.assertIn("Graph-Guided Multimodal", drawio.read_text(encoding="utf-8"))
            self.assertGreaterEqual(svg.read_text(encoding="utf-8").count("data:image/svg+xml;base64"), 3)

    def test_prepare_segment_crops(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            image = directory / "reference.png"
            canvas = Image.new("RGB", (240, 160), "white")
            for x in range(80, 160):
                for y in range(45, 115):
                    canvas.putpixel((x, y), (83, 148, 190))
            canvas.save(image)
            detections = directory / "detections.json"
            detections.write_text(json.dumps({"detections": [
                {"id": "title", "label": "text", "bbox": [20, 10, 220, 35], "text": "Editable title"},
                {"id": "graph-icon", "label": "icon", "bbox": [75, 40, 165, 120]}
            ]}), encoding="utf-8")
            out = directory / "segments"
            self.run_script("prepare_reference_segments.py", image, detections, "--out-dir", out)
            data = json.loads((out / "segments.json").read_text(encoding="utf-8"))
            self.assertEqual([region["kind"] for region in data["regions"]], ["text", "image"])
            self.assertTrue((out / "assets" / "graph-icon.png").is_file())
    def test_pptx_automizer_replacement_when_installed(self):
        if not (ROOT / "node_modules" / "pptx-automizer").is_dir():
            self.skipTest("run npm install to enable PPTX adapter test")
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "result.pptx"
            self.run_script("apply_template.py", "--manifest", DEMO / "template_manifest.json", "--values", DEMO / "replacement_values.json", "--format", "pptx", "--output", output)
            with zipfile.ZipFile(output) as archive:
                slide_xml = "\n".join(
                    archive.read(name).decode("utf-8")
                    for name in archive.namelist()
                    if name.startswith("ppt/slides/slide") and name.endswith(".xml")
                )
            self.assertIn("Graph-Guided Multimodal Learning with Adaptive Relation Fusion", slide_xml)
            self.assertIn("Adaptive Graph-Guided Fusion", slide_xml)
            self.assertIn("Relational Graph Encoder", slide_xml)
    def test_reference_reconstruction(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            svg = directory / "reference.svg"
            manifest = directory / "template_manifest.json"
            self.run_script("reconstruct_reference.py", DEMO / "reference_segments.json", "--svg-out", svg, "--manifest-out", manifest)
            tree = ET.parse(svg)
            ids = {element.get("id") for element in tree.getroot().iter()}
            self.assertIn("input-label", ids)
            self.assertIn("local-icon", ids)
            data = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual({slot["id"] for slot in data["slots"]}, {"title", "input-label", "local-icon"})


if __name__ == "__main__":
    unittest.main()
