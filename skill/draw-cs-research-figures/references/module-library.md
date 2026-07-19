# CS and AI module library

Select only modules supported by the method description.

For current LLM, multi-agent, computer-vision, and software-system vocabulary plus reusable SVG assets, read `hot-topic-modules.md` and search `../assets/module-catalog.json` with `scripts/search_module_catalog.py`.

| Family | Visual primitive | Required semantics |
|---|---|---|
| Tokens / embeddings | row of cells or matrix | sequence/patch axis; optional dimension |
| Tensor / feature map | layered planes | spatial/temporal/channel axes when known |
| Encoder / decoder | tapered block or card | modality and trainable/frozen state |
| Transformer block | stacked card | attention, FFN, residual, norm order |
| Attention | Q/K/V ports plus score path | self vs cross; mask if causal |
| LoRA / Adapter | narrow side branch | frozen base, low-rank/bottleneck update, merge |
| MoE | router, expert bank, combine | routing score, top-k, shared/routed experts |
| RAG | query, retriever, index, evidence, generator | retrieval boundary, top-k, provenance |
| Agent | perception, planner, memory, tools, executor, environment | observation/action loop and tool results |
| Multimodal LLM | modality encoders, bridge, LLM, heads | frozen/trainable state and token interface |
| Graph / KG | typed nodes and edges | types, message passing or retrieval direction |
| Diffusion | noisy timeline plus denoiser | forward noise, reverse denoising, conditioning |
| Loss / objective | small boundary badge | predictions and targets compared |
| Experiment plot | standard chart grammar | axes, units, direction, uncertainty, baselines |

## Edge semantics

- Solid arrow: forward data or control flow.
- Dashed arrow: loss, supervision, optional branch, or feedback; label which.
- Double arrow: genuine bidirectional exchange only.
- Bracket or brace: grouping/repetition, not data flow.
- Thick arrow: use sparingly for the contribution path.

## Training and inference

When they differ, add a legend and separate lanes or mute training-only objectives. Do not leave retrieval, routing, sampling, labels, or human feedback phase ambiguous.

## Experimental figures

Prefer line plots for trends, grouped bars for discrete comparisons, scatter plots for trade-offs, heatmaps for pairwise structure, and small multiples for ablations. Preserve supplied values, use consistent method colors, and do not use pseudo-3D bars or decorative gradients.
