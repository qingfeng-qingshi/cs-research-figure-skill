import hashlib
import json
import re
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill" / "draw-cs-research-figures"
CATALOG = SKILL / "assets" / "module-catalog.json"
EXAMPLES = ROOT / "examples" / "imitation"


class HotTopicLibraryTests(unittest.TestCase):
    def test_catalog_has_four_families_and_editable_assets(self):
        data = json.loads(CATALOG.read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(data["modules"]), 35)
        counts = Counter(module["family"] for module in data["modules"])
        for family in ("llm", "agent", "vision", "software"):
            self.assertGreaterEqual(counts[family], 8)
        signatures = {}
        for module in data["modules"]:
            self.assertTrue(module["aliases"])
            self.assertTrue(module["primitive"])
            self.assertTrue(module["semantics"])
            asset = SKILL / "assets" / module["asset"]
            self.assertTrue(asset.is_file(), module["id"])
            root = ET.parse(asset).getroot()
            geometry = list(root)[-1]
            geometry.attrib.pop("id", None)
            normalized = ET.tostring(geometry, encoding="unicode")
            normalized = re.sub(r"#[0-9A-Fa-f]{6}", "COLOR", normalized)
            signature = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
            self.assertNotIn(signature, signatures, f"duplicate geometry: {module['id']} and {signatures.get(signature)}")
            signatures[signature] = module["id"]
        self.assertEqual(len(signatures), len(data["modules"]))
        gallery = ET.parse(ROOT / "examples" / "module-library" / "hot-topic-module-library.svg")
        gallery_ids = {element.get("id") for element in gallery.getroot().iter()}
        self.assertEqual(sum(str(value).startswith("catalog-") for value in gallery_ids), len(data["modules"]))

    def test_bilingual_catalog_search(self):
        script = SKILL / "scripts" / "search_module_catalog.py"
        result = subprocess.run(
            [sys.executable, str(script), "视觉基础模型 特征金字塔 分割", "--limit", "6"],
            cwd=ROOT, check=True, capture_output=True, text=True,
        )
        self.assertIn("feature-pyramid", result.stdout)
        self.assertIn("segmentation-decoder", result.stdout)

    def test_reference_guided_redraw_examples(self):
        for slug in ("multi-agent-rag", "vision-foundation-model", "llm-serving-system"):
            folder = EXAMPLES / slug
            reference = json.loads((folder / "reference-structure-spec.json").read_text(encoding="utf-8"))
            target = json.loads((folder / "target-redraw-spec.json").read_text(encoding="utf-8"))
            self.assertNotEqual(reference["title"], target["title"])
            self.assertGreaterEqual(len(target["nodes"]), 7)
            tree = ET.parse(folder / "target-redraw.svg")
            ids = {item.get("id") for item in tree.getroot().iter()}
            self.assertIn("figure-title", ids)
            self.assertTrue({node["id"] for node in target["nodes"]}.issubset(ids))
            with Image.open(folder / "comparison.png") as image:
                self.assertEqual(image.format, "PNG")
                self.assertEqual(image.size, (1920, 650))

    def test_readmes_show_all_comparisons(self):
        for filename in ("README.md", "README_EN.md"):
            text = (ROOT / filename).read_text(encoding="utf-8")
            for slug in ("multi-agent-rag", "vision-foundation-model", "llm-serving-system"):
                self.assertIn(f"examples/imitation/{slug}/comparison.png", text)


if __name__ == "__main__":
    unittest.main()
