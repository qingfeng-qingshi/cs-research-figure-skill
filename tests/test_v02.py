import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skill" / "draw-cs-research-figures" / "scripts"
DEMO = ROOT / "examples" / "auto-selection" / "repeated-runs.csv"


class V02Tests(unittest.TestCase):
    def test_profile_and_auto_boxplot(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            profile = directory / "profile.json"
            result = subprocess.run([sys.executable, str(SCRIPTS / "profile_results.py"), str(DEMO), "--json-out", str(profile)], cwd=ROOT, check=True, capture_output=True, text=True)
            data = json.loads(profile.read_text(encoding="utf-8"))
            self.assertEqual(data["recommendation"]["kind"], "boxplot")
            self.assertEqual(data["sample_sizes"]["median"], 8.0)
            prefix = directory / "auto"
            plotted = subprocess.run([sys.executable, str(SCRIPTS / "plot_experiments.py"), "--input", str(DEMO), "--kind", "auto", "--preset", "cvpr", "--out-prefix", str(prefix)], cwd=ROOT, check=True, capture_output=True, text=True)
            self.assertIn("Auto-selected boxplot", plotted.stdout)
            for ext in (".svg", ".pdf", ".png"):
                self.assertGreater(prefix.with_suffix(ext).stat().st_size, 1000)

    def test_all_presets_load(self):
        sys.path.insert(0, str(SCRIPTS))
        from conference_presets import PRESETS, get_preset
        self.assertEqual(set(PRESETS), {"cvpr", "neurips", "icml", "acl", "ieee", "zh-thesis"})
        for name in PRESETS:
            self.assertGreater(get_preset(name)["width"], 3)


if __name__ == "__main__":
    unittest.main()
