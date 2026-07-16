# Working from incomplete research descriptions

Treat incomplete input as normal. Do not require the user to supply a finished algorithm flow.

## Evidence ledger

Extract statements into three classes:

- **Confirmed:** explicitly stated in method text, equations, pseudocode, tables, captions, or code.
- **Likely:** strongly implied by standard terminology or adjacent statements; show as a proposed presentation choice.
- **Unknown:** topology, dimensions, losses, phase, or metrics that cannot be inferred safely.

Never convert “likely” into a scientific claim. Use neutral labels such as “feature interaction” until the manuscript supports a specific operation.

## Minimum-input workflow

1. Read the algorithm description, method section, experiment tables, ablation text, and captions.
2. Extract nouns as candidate components, verbs as transformations, and equations as constraints.
3. Detect inputs, outputs, repeated operations, branches, objectives, and contribution phrases.
4. Draft two alternative Figure Briefs when the topology is ambiguous.
5. Continue with the safest brief. Ask only questions whose answers would change scientific meaning.
6. Use placeholders only in the editable specification and list them for replacement; do not show editorial placeholders in the publication preview.

## Safe inference examples

- “multi-scale features are fused” permits multiple feature tensors entering a fusion module; it does not permit inventing concatenation or addition.
- “graph reasoning” permits typed nodes and message flow; it does not permit inventing edge types.
- “adapter tuning” permits a frozen base path and trainable side module; it does not permit inventing rank or bottleneck size.
- “compared with baselines” permits planning a grouped comparison plot; values must come from a table or data file.
- “ablation removes module A” permits a component-effect chart; it does not permit inventing scores.

## Density target

Aim for meaningful density, not occupancy. A method overview normally needs 3–6 semantic regions, 8–18 primary objects, one clear innovation focus, and 1–3 local explanatory insets. Leave whitespace between semantic groups, not large unused page regions.
