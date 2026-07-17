#!/usr/bin/env python3
"""Profile experiment CSV data and recommend a scientifically suitable chart."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd


ERROR_NAMES = {"error", "err", "std", "sd", "sem", "stderr", "ci", "ci_low", "ci_high", "lower", "upper"}
N_NAMES = {"n", "count", "sample_size", "samples"}
ORDERED_NAMES = {"x", "epoch", "iteration", "step", "rank", "layer", "layers", "experts", "threshold"}
GROUP_NAMES = ("variant", "method", "model", "group", "dataset", "metric", "series", "panel")


def load_csv(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError("CSV contains no data rows")
    return df


def infer_type(series: pd.Series) -> str:
    clean = series.dropna()
    unique = clean.nunique()
    if pd.api.types.is_numeric_dtype(series):
        if unique <= max(8, int(math.sqrt(max(len(clean), 1)))):
            return "numeric-discrete"
        return "numeric-continuous"
    if unique == len(clean) and len(clean) > 8:
        return "identifier-or-label"
    return "categorical"


def _group_columns(df: pd.DataFrame) -> list[str]:
    return [name for name in GROUP_NAMES if name in df.columns]


def recommend_chart(df: pd.DataFrame) -> dict:
    cols = set(df.columns)
    reasons = []
    if {"row", "column", "value"}.issubset(cols):
        return {"kind": "heatmap", "reason": "row/column/value define a numeric matrix"}
    if {"x", "series", "value"}.issubset(cols):
        return {"kind": "ablation-curve", "reason": "x is ordered and multiple series should be compared as curves"}

    group_col = next((c for c in ("variant", "method", "model", "group") if c in cols), None)
    if group_col and "value" in cols:
        grouping = [group_col] + (["metric"] if "metric" in cols else []) + (["dataset"] if "dataset" in cols else [])
        repetitions = df.groupby(grouping, dropna=False).size()
        if len(repetitions) and repetitions.median() >= 3:
            return {"kind": "boxplot", "reason": f"repeated raw observations are available (median n={repetitions.median():.0f} per group)"}

    if {"variant", "metric", "value"}.issubset(cols):
        labels = " ".join(df["variant"].astype(str).str.lower().unique())
        if any(token in labels for token in ("w/o", "without", "remove", "full model")):
            return {"kind": "ablation-discrete", "reason": "variants are categorical remove-one/full-model configurations"}
        shape = (df["variant"].nunique(), df["metric"].nunique())
        if shape[0] >= 4 and shape[1] >= 4:
            return {"kind": "heatmap", "reason": f"the {shape[0]}×{shape[1]} method-metric matrix is denser than grouped bars"}
        reasons.append("aggregated method/metric/value rows support a baseline comparison")
        return {"kind": "comparison", "reason": "; ".join(reasons)}

    if "value" in cols and group_col:
        return {"kind": "comparison", "reason": f"one numeric measure is grouped by {group_col}"}
    raise ValueError("cannot recommend a chart; provide value plus grouping columns, x/series, or row/column")


def profile_dataframe(df: pd.DataFrame) -> dict:
    columns = []
    outliers = {}
    for name in df.columns:
        s = df[name]
        role = "data"
        lower = name.lower()
        if lower in ERROR_NAMES:
            role = "uncertainty"
        elif lower in N_NAMES:
            role = "sample-size"
        elif lower in ORDERED_NAMES:
            role = "ordered-axis"
        elif lower in GROUP_NAMES:
            role = "grouping"
        columns.append({
            "name": name,
            "type": infer_type(s),
            "role": role,
            "non_null": int(s.notna().sum()),
            "missing": int(s.isna().sum()),
            "unique": int(s.nunique(dropna=True)),
        })
        if pd.api.types.is_numeric_dtype(s) and lower not in ERROR_NAMES | N_NAMES:
            clean = s.dropna().astype(float)
            if len(clean) >= 4:
                q1, q3 = clean.quantile([0.25, 0.75])
                iqr = q3 - q1
                mask = (clean < q1 - 1.5 * iqr) | (clean > q3 + 1.5 * iqr)
                outliers[name] = {"count": int(mask.sum()), "values": [float(v) for v in clean[mask].head(8)]}

    group_cols = _group_columns(df)
    sample_sizes = {}
    if group_cols:
        keys = group_cols[:3]
        sizes = df.groupby(keys, dropna=False).size()
        sample_sizes = {
            "grouped_by": keys,
            "min": int(sizes.min()),
            "median": float(sizes.median()),
            "max": int(sizes.max()),
            "groups": int(len(sizes)),
        }
    return {
        "rows": int(len(df)),
        "columns": columns,
        "error_columns": [c for c in df.columns if c.lower() in ERROR_NAMES],
        "sample_size_columns": [c for c in df.columns if c.lower() in N_NAMES],
        "sample_sizes": sample_sizes,
        "outliers_iqr": outliers,
        "recommendation": recommend_chart(df),
    }


def render_report(profile: dict) -> str:
    rec = profile["recommendation"]
    lines = [
        "Experiment data profile",
        "=======================",
        f"Rows: {profile['rows']}",
        f"Recommended chart: {rec['kind']}",
        f"Reason: {rec['reason']}",
        f"Error columns: {', '.join(profile['error_columns']) or 'none'}",
        f"Sample-size columns: {', '.join(profile['sample_size_columns']) or 'none'}",
    ]
    if profile["sample_sizes"]:
        s = profile["sample_sizes"]
        lines.append(f"Observed group sizes: min={s['min']}, median={s['median']:.1f}, max={s['max']} ({s['groups']} groups)")
    for name, item in profile["outliers_iqr"].items():
        lines.append(f"IQR outliers in {name}: {item['count']}")
    lines.append("\nColumns:")
    for c in profile["columns"]:
        lines.append(f"- {c['name']}: {c['type']}, role={c['role']}, n={c['non_null']}, missing={c['missing']}")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Profile a research-results CSV and recommend a chart")
    parser.add_argument("input")
    parser.add_argument("--json-out")
    parser.add_argument("--report-out")
    args = parser.parse_args()
    profile = profile_dataframe(load_csv(args.input))
    report = render_report(profile)
    print(report, end="")
    if args.json_out:
        Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json_out).write_text(json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.report_out:
        Path(args.report_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.report_out).write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
