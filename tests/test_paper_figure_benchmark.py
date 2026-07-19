import json
import unittest
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill" / "draw-cs-research-figures"
DATA = SKILL / "references" / "paper-figure-benchmark"
EXAMPLE = ROOT / "examples" / "paper-figure-benchmark"


class PaperFigureBenchmarkTests(unittest.TestCase):
    def test_candidate_balance_and_official_sources(self):
        payload = json.loads((DATA / "papers.json").read_text(encoding="utf-8"))
        papers = payload["papers"]
        self.assertEqual(len(papers), 40)
        self.assertEqual(Counter(p["venue"] for p in papers), Counter({
            "CVPR": 10, "NeurIPS": 10, "ICML": 10, "ACL": 10,
        }))
        allowed = (
            "https://openaccess.thecvf.com/",
            "https://proceedings.neurips.cc/",
            "https://proceedings.mlr.press/",
            "https://icml.cc/",
            "https://aclanthology.org/",
        )
        self.assertTrue(all(p["official_url"].startswith(allowed) for p in papers))
        self.assertFalse(any(p["venue"] == "NeurIPS" and p["year"] == 2026 for p in papers))

    def test_planned_figure_records_are_explicitly_pending(self):
        records = [json.loads(line) for line in (DATA / "figures.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertEqual(len(records), 100)
        self.assertTrue(all(item["review_status"] == "pending_pdf_visual_audit" for item in records))
        self.assertTrue(all(item["source_figure_number"] is None for item in records))

    def test_overview_artifacts(self):
        svg = EXAMPLE / "candidate-overview.svg"
        png = EXAMPLE / "candidate-overview.png"
        root = ET.parse(svg).getroot()
        ids = {element.attrib.get("id") for element in root.iter()}
        self.assertIn("venue-cvpr", ids)
        self.assertIn("paper-acl26-flowsearch", ids)
        with Image.open(png) as image:
            self.assertEqual(image.size, (2240, 1760))
            self.assertEqual(image.format, "PNG")


if __name__ == "__main__":
    unittest.main()
