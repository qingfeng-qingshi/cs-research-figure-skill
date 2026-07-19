#!/usr/bin/env python3
"""Search the machine-readable CS/AI research module catalog."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


CATALOG = Path(__file__).resolve().parents[1] / "assets" / "module-catalog.json"


def tokens(value: str):
    return {item for item in re.split(r"[^\w\u4e00-\u9fff]+", value.lower()) if item}


def score(module, query):
    fields = [module["id"], module["name"], module.get("zh", ""), module["family"], *module.get("aliases", [])]
    haystack = " ".join(fields).lower()
    query_tokens = tokens(query)
    value = sum(4 for token in query_tokens if token in haystack)
    value += sum(2 for alias in module.get("aliases", []) if alias.lower() in query.lower())
    if module["family"] in query.lower():
        value += 2
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="English or Chinese research keywords")
    parser.add_argument("--limit", type=int, default=8)
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args()
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    ranked = sorted(((score(module, args.query), module) for module in data["modules"]), key=lambda item: (-item[0], item[1]["id"]))
    selected = [module for value, module in ranked if value > 0][:args.limit]
    if args.json:
        print(json.dumps(selected, ensure_ascii=False, indent=2))
    else:
        for module in selected:
            print(f"{module['id']}: {module['name']} / {module['zh']} | {module['primitive']} | {module['asset']}")


if __name__ == "__main__":
    main()
