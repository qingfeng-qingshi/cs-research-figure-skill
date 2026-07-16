import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
SOURCE = ROOT / "skill" / "draw-cs-research-figures"
DIST = ROOT / "dist"


def main():
    if not (SOURCE / "SKILL.md").is_file():
        raise SystemExit("Skill source is incomplete")
    DIST.mkdir(exist_ok=True)
    base = DIST / f"draw-cs-research-figures-v{VERSION}"
    archive = Path(shutil.make_archive(str(base), "zip", SOURCE.parent, SOURCE.name))
    print(f"Created {archive.relative_to(ROOT)} ({archive.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
