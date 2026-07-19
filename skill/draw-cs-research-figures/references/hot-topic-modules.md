# Hot-topic CS and AI modules

Use `assets/module-catalog.json` as the source of truth. It contains English and Chinese names, aliases, visual primitives, required semantics, and a reusable SVG asset for each module.

Search it before drawing when the request mentions an unfamiliar or abbreviated component:

```bash
python scripts/search_module_catalog.py "multi-agent RAG shared memory"
python scripts/search_module_catalog.py "视觉基础模型 特征金字塔 分割"
```

## Families

- **Large language models:** decoder-only LLM, prompts, RAG, vector databases, rerankers, LoRA/Adapter, MoE, KV cache, SFT/RLHF/DPO, and tool calling.
- **Multi-agent systems:** planners, role agents, collaboration graphs, shared memory, message buses, critics/verifiers, environment loops, and tool sandboxes.
- **Computer vision:** ViT, patch embedding, feature pyramids, detection, segmentation, VLMs, diffusion, temporal tracking, and 3D vision.
- **Software and AI systems:** API gateways, schedulers, model serving, microservices, event streams, caches/storage, container orchestration, and observability.

Give every named module a distinct structural fingerprint. Related functions may share palette, stroke, or a primitive family, but do not reuse the complete icon geometry. The module-library test normalizes colors and rejects duplicate SVG geometry.

Select a module only when the method description supports its semantics. Adapt labels and ports, but preserve the visual primitive's meaning. Treat the SVG icons as editable starting points, not decorations.

## Reference-guided redraw

For a strong reference figure, retain only transferable visual grammar: reading order, zone proportions, grouping, shape family, edge hierarchy, and palette roles. Replace paper-specific modules, text, results, icons, and topology with the user's verified content. Save the reference scene, target scene, editable SVG, and a side-by-side preview.

The repository examples under `examples/imitation/` demonstrate this workflow for multi-agent RAG, vision foundation models, and agentic LLM serving.
