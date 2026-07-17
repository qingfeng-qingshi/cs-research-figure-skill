import sys
import unittest
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skill" / "draw-cs-research-figures" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from profile_results import profile_dataframe, recommend_chart


class AutoSelectionMatrixTests(unittest.TestCase):
    def test_five_chart_families(self):
        comparison = pd.DataFrame({"variant": ["A", "B"], "metric": ["Acc", "Acc"], "value": [80, 82]})
        discrete = pd.DataFrame({"variant": ["Full model", "w/o graph"], "metric": ["Acc", "Acc"], "value": [88, 85]})
        curve = pd.DataFrame({"x": [1, 2, 1, 2], "series": ["r=4", "r=4", "r=8", "r=8"], "value": [80, 82, 81, 83]})
        heatmap = pd.DataFrame([{"variant": f"M{i}", "metric": f"D{j}", "value": i + j} for i in range(4) for j in range(4)])
        boxplot = pd.DataFrame({"variant": ["A"] * 3 + ["B"] * 3, "metric": ["Acc"] * 6, "value": [1, 2, 3, 2, 3, 4]})
        self.assertEqual(recommend_chart(comparison)["kind"], "comparison")
        self.assertEqual(recommend_chart(discrete)["kind"], "ablation-discrete")
        self.assertEqual(recommend_chart(curve)["kind"], "ablation-curve")
        self.assertEqual(recommend_chart(heatmap)["kind"], "heatmap")
        self.assertEqual(recommend_chart(boxplot)["kind"], "boxplot")

    def test_uncertainty_and_sample_size_roles(self):
        df = pd.DataFrame({"variant": ["A", "B"], "metric": ["Acc", "Acc"], "value": [80, 82], "std": [0.4, 0.3], "n": [5, 5]})
        profile = profile_dataframe(df)
        self.assertEqual(profile["error_columns"], ["std"])
        self.assertEqual(profile["sample_size_columns"], ["n"])


if __name__ == "__main__":
    unittest.main()
