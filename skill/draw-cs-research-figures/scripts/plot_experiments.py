#!/usr/bin/env python3
"""Render an experiment figure with automatic preflight and exported-file audits."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from matplotlib.figure import Figure

from audit_figure import audit_matplotlib_figure, audit_path, print_report
from plot_experiments_core import main as render_main


def _argument(name):
    try:
        return sys.argv[sys.argv.index(name) + 1]
    except (ValueError, IndexError):
        return None


def _install_preflight():
    original = Figure.savefig
    audited = set()

    def checked_savefig(fig, *args, **kwargs):
        if id(fig) not in audited:
            audited.add(id(fig))
            issues = audit_matplotlib_figure(fig)
            # bbox_inches='tight' deliberately expands around edge tick labels;
            # keep renderer clipping as a warning and let the exported SVG
            # viewBox audit decide whether final output is actually clipped.
            for item in issues:
                if item["code"] == "text-clipping" and item["severity"] == "FAIL":
                    item["severity"] = "WARN"
                    item["message"] += " (final exported bounds will be checked)"
            result = print_report("Matplotlib Figure preflight", issues)
            if result == "FAIL":
                raise RuntimeError("Matplotlib Figure preflight failed")
        return original(fig, *args, **kwargs)

    Figure.savefig = checked_savefig
    return original


def main():
    original_savefig = _install_preflight()
    try:
        render_main()
    finally:
        Figure.savefig = original_savefig
    prefix_value = _argument("--out-prefix")
    if not prefix_value:
        raise SystemExit("--out-prefix is required for automatic audit")
    prefix = Path(prefix_value); reports = []; failed = False
    for suffix in (".svg", ".pdf", ".png"):
        path = prefix.with_suffix(suffix); issues = audit_path(path, min_dpi=300)
        result = print_report(path, issues)
        reports.append({"path": str(path), "verdict": result, "issues": issues}); failed |= result == "FAIL"
    output = prefix.with_name(prefix.name + "-audit.json")
    output.write_text(json.dumps(reports, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Audit report: {output}")
    if failed:
        raise SystemExit("automatic figure audit failed")


if __name__ == "__main__":
    main()
