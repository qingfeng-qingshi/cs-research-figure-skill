import sys
import tempfile
import unittest
from pathlib import Path

import matplotlib.pyplot as plt
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skill" / "draw-cs-research-figures" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from audit_figure import audit_matplotlib_figure, audit_path


class AutomaticAuditTests(unittest.TestCase):
    def test_bad_svg_reports_clipping_encoding_and_grayscale(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.svg"
            path.write_text(
                '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
                '<rect x="5" y="20" width="30" height="20" fill="#ff0000"/>'
                '<rect x="45" y="20" width="30" height="20" fill="#00a000"/>'
                '<text x="94" y="12" font-size="18">锟斤拷 label</text>'
                '</svg>', encoding="utf-8")
            codes = {item["code"] for item in audit_path(path)}
            self.assertIn("text-clipping", codes)
            self.assertIn("mojibake", codes)
            self.assertIn("grayscale-ambiguity", codes)

    def test_low_dpi_png_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "low.png"
            Image.new("RGB", (200, 100), "white").save(path, dpi=(72, 72))
            codes = {item["code"] for item in audit_path(path, min_dpi=300)}
            self.assertIn("dpi-low", codes)

    def test_matplotlib_tick_overlap_is_detected(self):
        fig, ax = plt.subplots(figsize=(2, 1.5))
        ax.plot(range(4), range(4))
        ax.set_xticks(range(4), ["very long category A", "very long category B", "very long category C", "very long category D"])
        codes = {item["code"] for item in audit_matplotlib_figure(fig)}
        plt.close(fig)
        self.assertIn("tick-overlap", codes)


if __name__ == "__main__":
    unittest.main()
