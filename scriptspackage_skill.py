import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
SOURCE = ROOT / "skill" / "draw-cs-research-figures"
DIST = ROOT / "dist"


def main():
    if not (SOURCE / "SKILL.md").is_file():
        raise SystemExit("Skill source is incomplete")
    DIST.mkdir(exist_ok=True)
    archive = DIST / f"draw-cs-research-figures-v{VERSION}.zip"
    excluded = {"rich-example.svg"}
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as package:
        for path in SOURCE.rglob("*"):
            if not path.is_file():
                continue
            if path.name in excluded or "__pycache__" in path.parts:
                continue
            package.write(path, Path(SOURCE.name) / path.relative_to(SOURCE))
    print(f"Created {archive.relative_to(ROOT)} ({archive.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
