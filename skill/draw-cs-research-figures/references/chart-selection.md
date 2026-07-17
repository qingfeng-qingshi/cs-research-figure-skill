# CS/AI experiment chart selection

Run `scripts/profile_results.py` before plotting, or use `plot_experiments.py --kind auto`.

| Data evidence | Chart | Scientific interpretation |
|---|---|---|
| `x, series, value` | ordered line plot | sensitivity across epochs, ranks, layers, thresholds, or expert counts |
| categorical `full / w/o ...` | discrete ablation bars/dots | configurations have no continuous order; do not connect them |
| repeated raw values per method | boxplot plus points | expose seed/run distribution and outliers |
| dense method × metric matrix | heatmap | reduce clutter while preserving exact cells |
| aggregated method/metric/value | comparison plot | compare baselines with the proposed method |

Keep uncertainty columns (`std`, `sd`, `sem`, `error`, `ci_low`, `ci_high`) and sample-size columns (`n`, `sample_size`). Never silently reinterpret SD as SEM. Use the recommendation as a default, not as permission to override the scientific claim.
