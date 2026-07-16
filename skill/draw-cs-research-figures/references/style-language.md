# Style language

This library describes reusable composition patterns, not figures to copy.

## A. Symmetric scientific framework

Best for multi-view learning, missing data, graph fusion, co-training, and paired modalities.

- Mirror view-specific lanes around a central fusion or shared objective.
- Represent encoders and decoders with tapered blocks; samples or tokens with compact matrices.
- Use a pale background band for each lane and a distinct central band for the novel mechanism.
- Solid arrows carry data. Dashed arrows carry supervision, reconstruction, constraints, or feedback.
- Put losses at the boundary rather than across the main flow.

## B. Deep stacked architecture

Best for Transformer, diffusion, recurrent refinement, and repeated neural layers.

- Show one detailed layer in front of a shallow card stack and label repetition explicitly.
- Draw residual paths as external bypasses with clear merge points.
- Use orange for attention/gating, green for normalization/merge, blue-gray for projection/FFN.
- Align Q/K/V or tensor ports; show cross-attention memory as a separately labeled input.
- Pair the macro-stack with one zoomed micro-panel only when the novelty is inside a block.

## C. Zoned end-to-end system

Best for document AI, RAG, agents, knowledge graphs, human feedback, and enterprise workflows.

- Divide the story into 4–6 softly tinted stages with descriptive headings, not editor labels.
- Use small, consistent outline icons for documents, tables, images, databases, tools, users, and outputs.
- Allow rich content inside zones, but keep the global reading direction unmistakable.
- Reserve dashed return paths for feedback and iterative refinement.
- Use nested layers for metadata/layout/semantics or perception/planning/action when hierarchy matters.

## D. Canonical CS/AI patterns

Use these structural lessons without reproducing paper artwork.

- **Encoder–decoder stack:** repeated layers, residual paths, and cross-attention memory.
- **Dual-tower contrastive learning:** aligned encoders feeding a similarity matrix and paired objectives.
- **Retrieval-augmented generation:** query encoder → search/index → top-k evidence → generator, with provenance visible.
- **Multimodal bridge:** modality encoder → adapter/query bridge → language model; distinguish training from inference.
- **Sparse MoE:** router probabilities → top-k dispatch → expert bank → weighted combine.
- **Attention micro-view:** Q/K/V projections → score/scale/mask → softmax → weighted values → output projection.

## Composition defaults

- Choose final paper-column or slide dimensions before font size.
- Use one sans-serif family plus a math font and at most three type levels.
- Use dark navy/charcoal text with low-saturation blue, green, orange, violet, and rose fills.
- Keep panel padding at least twice node padding and preserve a quiet outer border.
- Use consistent outline icons; avoid photorealistic clip art.

## Anti-copy rule

Borrow layout grammar, semantic color logic, and abstraction level. Replace paper-specific labels, topology, numbers, icons, and stylistic signatures with content justified by the user's method.
