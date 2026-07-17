import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill" / "draw-cs-research-figures"
SCRIPTS = SKILL / "scripts"
EXAMPLES = ROOT / "examples"


def run(*args):
    return subprocess.run(
        [sys.executable, *map(str, args)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )


class RepositoryTests(unittest.TestCase):
    def test_skill_structure(self):
        skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8-sig")
        self.assertTrue(skill_text.startswith("---"))
        self.assertIn("name: draw-cs-research-figures", skill_text)
        self.assertNotIn("TODO", skill_text)
        self.assertTrue((SKILL / "agents" / "openai.yaml").is_file())
        self.assertFalse((SKILL / "README.md").exists())

    def test_method_svg_generation(self):
        spec = EXAMPLES / "method-figure" / "rich-example-spec.json"
        ET.parse(EXAMPLES / "method-figure" / "rich-example.svg")
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "method.svg"
            result = run(SCRIPTS / "validate_figure_spec.py", spec)
            self.assertIn("0 error(s)", result.stdout)
            run(SCRIPTS / "render_svg.py", spec, output)
            root = ET.parse(output).getroot()
            ids = {element.attrib.get("id") for element in root.iter()}
            self.assertIn("figure-title-1", ids)
            self.assertIn("fusion", ids)

    def test_readme_preview_is_not_an_xml_error_page(self):
        preview = EXAMPLES / "method-figure" / "rich-example-preview.png"
        with Image.open(preview) as image:
            self.assertEqual(image.format, "PNG")
            self.assertEqual(image.size, (1800, 1000))
            top = image.convert("RGB").crop((0, 0, image.width, 260))
            pixels = list(top.getdata())
            pink = sum(
                1 for red, green, blue in pixels
                if red > 240 and 185 < green < 238 and 185 < blue < 238
            )
            self.assertLess(pink / len(pixels), 0.08)

    def test_comparison_plot_generation(self):
        source = EXAMPLES / "comparison" / "demo-comparison.csv"
        with tempfile.TemporaryDirectory() as directory:
            prefix = Path(directory) / "comparison"
            run(
                SCRIPTS / "plot_experiments.py",
                "--input", source,
                "--kind", "comparison",
                "--title", "Comparison with Baselines",
                "--out-prefix", prefix,
            )
            for suffix in (".svg", ".pdf", ".png"):
                self.assertGreater(prefix.with_suffix(suffix).stat().st_size, 1000)
            result = run(SCRIPTS / "validate_plot_svg.py", prefix.with_suffix(".svg"))
            self.assertIn("no diagonal text", result.stdout)

    def test_curve_ablation_and_two_line_title(self):
        source = EXAMPLES / "ablation" / "demo-ablation-curves.csv"
        title = (
            "Sensitivity Analysis of Feature-Combination Depth "
            "Across Multiple Evaluation Settings"
        )
        with tempfile.TemporaryDirectory() as directory:
            prefix = Path(directory) / "ablation"
            run(
                SCRIPTS / "plot_experiments.py",
                "--input", source,
                "--kind", "ablation",
                "--ablation-mode", "auto",
                "--title", title,
                "--out-prefix", prefix,
            )
            svg = prefix.with_suffix(".svg")
            result = run(SCRIPTS / "validate_plot_svg.py", svg)
            self.assertIn("no diagonal text", result.stdout)
            text = svg.read_text(encoding="utf-8")
            self.assertIn("Sensitivity Analysis of Feature-Combination", text)
            self.assertIn("Depth Across Multiple Evaluation Settings", text)
            self.assertIn("<text", text)

    def test_repository_has_no_duplicate_packager(self):
        self.assertFalse((ROOT / "scriptspackage_skill.py").exists())


if __name__ == "__main__":
    unittest.main()
