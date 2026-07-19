# Paper figure benchmark

Use this benchmark when a user asks to redraw new research content using the visual grammar of recent CVPR, NeurIPS, ICML, or ACL papers.

1. Read `references/paper-figure-benchmark/papers.json` and match by topic, figure role, and layout grammar rather than paper title.
2. Treat records marked `candidate_overview` as a shortlist, not a verified gold answer.
3. Before using a paper as a reference, open its official PDF and verify the selected Figure number, page, caption, visual quality, and scientific role.
4. Store downloaded PDFs and source crops only in `.cache/paper-figure-benchmark/`; never commit them.
5. Add verified Figure metadata to `figures.jsonl`, including page, caption, type, visual grammar, reusable patterns, and review score.
6. Transfer reading order, grouping, visual hierarchy, shape family, and color roles only. Rebuild all paper-specific labels, topology, values, icons, and illustrations from the user's content.
7. Generate an editable SVG master, optional PPTX/Draw.io version, PNG comparison, and audit JSON.

Run `python scripts/generate_paper_figure_benchmark.py` after changing the paper seed. It validates the 10-paper-per-venue balance, creates 100 planned Figure records, and regenerates the editable overview SVG and PNG preview.
