import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DocumentationTests(unittest.TestCase):
    def test_readme_demo_images_exist(self):
        for filename in ("README.md", "README_EN.md"):
            text = (ROOT / filename).read_text(encoding="utf-8")
            images = re.findall(r"!\[[^]]*\]\(([^)]+)\)", text)
            self.assertGreaterEqual(len(images), 4)
            for relative in images:
                self.assertTrue((ROOT / relative).is_file(), f"missing {relative} in {filename}")

    def test_detailed_usage_and_version(self):
        chinese = (ROOT / "README.md").read_text(encoding="utf-8")
        english = (ROOT / "README_EN.md").read_text(encoding="utf-8")
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertIn("## 使用", chinese)
        self.assertIn("### 用法五：检查已有科研图", chinese)
        self.assertIn("## 命令行使用", chinese)
        self.assertIn("## Usage", english)
        self.assertIn("### Use case 5: audit an existing figure", english)
        self.assertIn("## CLI", english)
        self.assertEqual(version, "0.3.1")
        self.assertFalse((ROOT / "RELEASE.md").exists())


if __name__ == "__main__":
    unittest.main()
