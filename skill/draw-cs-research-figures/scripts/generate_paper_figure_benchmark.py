#!/usr/bin/env python3
"""Validate the candidate paper benchmark and render its editable overview."""

from __future__ import annotations

import csv
import html
import json
import textwrap
from collections import Counter
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


SKILL = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[3]
SEED = SKILL / "references" / "paper-figure-benchmark" / "papers.json"
DATA_DIR = SKILL / "references" / "paper-figure-benchmark"
OUT_DIR = ROOT / "examples" / "paper-figure-benchmark"

WIDTH, HEIGHT = 2240, 1760
MARGIN = 34
TOP = 215
COL_GAP = 20
CARD_GAP = 10
COL_W = (WIDTH - 2 * MARGIN - 3 * COL_GAP) // 4
CARD_H = 137

VENUES = ["CVPR", "NeurIPS", "ICML", "ACL"]
COLORS = {
    "CVPR": (55, 126, 184),
    "NeurIPS": (120, 94, 164),
    "ICML": (57, 145, 112),
    "ACL": (221, 126, 64),
}
ROLE_LABELS = {
    "overview_pipeline": "Overview",
    "method_architecture": "Method",
    "module_zoom": "Zoom-in",
    "tensor_flow": "Tensor",
    "agent_graph": "Agents",
    "retrieval_graph": "RAG/Graph",
    "feedback_loop": "Feedback",
    "qualitative_grid": "Qualitative",
    "comparison_plot": "Compare",
    "ablation_plot": "Ablation",
    "heatmap": "Heatmap",
    "attention_map": "Attention",
    "system_diagram": "System",
}


def load_font(size: int, bold: bool = False):
    candidates = [
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


FONTS = {
    "title": load_font(34, True),
    "subtitle": load_font(19),
    "venue": load_font(24, True),
    "paper": load_font(18, True),
    "meta": load_font(14),
    "chip": load_font(12, True),
}


def validate(payload: dict) -> list[dict]:
    papers = payload.get("papers", [])
    if len(papers) != 40:
        raise ValueError(f"expected 40 papers, found {len(papers)}")
    ids = [paper["id"] for paper in papers]
    if len(set(ids)) != len(ids):
        raise ValueError("paper ids must be unique")
    venue_counts = Counter(paper["venue"] for paper in papers)
    if venue_counts != Counter({venue: 10 for venue in VENUES}):
        raise ValueError(f"expected 10 papers per venue, found {dict(venue_counts)}")
    figures = []
    for paper in papers:
        for index, role in enumerate(paper["target_roles"], 1):
            if role not in ROLE_LABELS:
                raise ValueError(f"unknown role {role!r} in {paper['id']}")
            figures.append({
                "id": f"{paper['id']}-target-{index:02d}",
                "paper_id": paper["id"],
                "venue": paper["venue"],
                "year": paper["year"],
                "planned_role": role,
                "source_figure_number": None,
                "pdf_page": None,
                "caption": None,
                "review_status": "pending_pdf_visual_audit",
                "official_url": paper["official_url"],
            })
    if len(figures) != 100:
        raise ValueError(f"expected 100 planned Figure records, found {len(figures)}")
    return figures


def wrap(text: str, width: int, limit: int = 2) -> list[str]:
    lines = textwrap.wrap(text, width=width, break_long_words=False)
    if len(lines) > limit:
        lines = lines[:limit]
        lines[-1] = lines[-1].rstrip(" .") + "…"
    return lines


def svg_text(x, y, text, size, weight="400", fill="#20364A", anchor="start"):
    return (
        f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{html.escape(str(text))}</text>'
    )


def render_svg(papers: list[dict], destination: Path):
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        '<rect width="100%" height="100%" fill="#F7F9FC"/>',
        svg_text(WIDTH / 2, 54, "2025–2026 Top-Conference Paper Figure Candidate Benchmark", 34, "700", "#172B4D", "middle"),
        svg_text(WIDTH / 2, 84, "40 papers · 100 planned target Figures · official proceedings only · candidate stage for visual audit", 18, "400", "#52677D", "middle"),
    ]
    stat_items = [("40", "papers"), ("100", "Figure slots"), ("4", "venues"), ("13", "visual roles")]
    sx = WIDTH / 2 - 390
    for index, (value, label) in enumerate(stat_items):
        x = sx + index * 260
        parts.append(f'<g id="stat-{index}"><rect x="{x}" y="105" width="210" height="62" rx="16" fill="#FFFFFF" stroke="#D5DEE8"/>')
        parts.append(svg_text(x + 42, 145, value, 27, "700", "#172B4D", "middle"))
        parts.append(svg_text(x + 118, 142, label, 15, "400", "#52677D", "middle") + "</g>")

    by_venue = {venue: [p for p in papers if p["venue"] == venue] for venue in VENUES}
    for col, venue in enumerate(VENUES):
        r, g, b = COLORS[venue]
        color = f"#{r:02X}{g:02X}{b:02X}"
        pale = f"#{(r + 220) // 2:02X}{(g + 230) // 2:02X}{(b + 240) // 2:02X}"
        x = MARGIN + col * (COL_W + COL_GAP)
        parts.append(f'<g id="venue-{venue.lower()}">')
        parts.append(f'<rect x="{x}" y="{TOP - 38}" width="{COL_W}" height="{HEIGHT - TOP - 42}" rx="24" fill="{pale}" fill-opacity="0.30" stroke="{color}" stroke-opacity="0.25"/>')
        parts.append(f'<rect x="{x}" y="{TOP - 38}" width="{COL_W}" height="56" rx="20" fill="{color}"/>')
        parts.append(svg_text(x + 20, TOP - 2, venue, 24, "700", "#FFFFFF"))
        years = Counter(p["year"] for p in by_venue[venue])
        year_text = " · ".join(f"{year}: {count}" for year, count in sorted(years.items()))
        parts.append(svg_text(x + COL_W - 18, TOP - 4, year_text, 14, "400", "#FFFFFF", "end"))
        for row, paper in enumerate(by_venue[venue]):
            y = TOP + 30 + row * (CARD_H + CARD_GAP)
            parts.append(f'<g id="paper-{paper["id"]}">')
            parts.append(f'<rect x="{x + 10}" y="{y}" width="{COL_W - 20}" height="{CARD_H}" rx="16" fill="#FFFFFF" stroke="#D5DEE8"/>')
            parts.append(f'<rect x="{x + 10}" y="{y}" width="8" height="{CARD_H}" rx="4" fill="{color}"/>')
            parts.append(f'<rect x="{x + 30}" y="{y + 14}" width="54" height="25" rx="12" fill="{color}" fill-opacity="0.12"/>')
            parts.append(svg_text(x + 57, y + 32, paper["year"], 13, "700", color, "middle"))
            title_lines = wrap(paper["short_title"], 34, 2)
            for line_index, line in enumerate(title_lines):
                parts.append(svg_text(x + 96, y + 31 + line_index * 20, line, 18, "700", "#20364A"))
            parts.append(svg_text(x + 30, y + 75, paper["grammar"], 14, "400", "#52677D"))
            chip_x = x + 30
            for role in paper["target_roles"]:
                label = ROLE_LABELS[role]
                chip_w = max(68, 14 + len(label) * 8)
                parts.append(f'<rect x="{chip_x}" y="{y + 94}" width="{chip_w}" height="25" rx="12" fill="{color}" fill-opacity="0.11" stroke="{color}" stroke-opacity="0.35"/>')
                parts.append(svg_text(chip_x + chip_w / 2, y + 111, label, 12, "700", color, "middle"))
                chip_x += chip_w + 7
            status = paper.get("source_status", "published_official_proceedings")
            if status != "published_official_proceedings":
                parts.append(svg_text(x + COL_W - 30, y + 129, "provisional index", 11, "400", "#A46722", "end"))
            parts.append("</g>")
        parts.append("</g>")

    legend_y = HEIGHT - 34
    parts.append(svg_text(MARGIN, legend_y, "Next gate: verify PDF page + Figure number + caption + visual score before promotion to gold reference.", 15, "600", "#52677D"))
    parts.append(svg_text(WIDTH - MARGIN, legend_y, "Editable SVG · no source paper artwork redistributed", 15, "400", "#52677D", "end"))
    parts.append("</svg>")
    destination.write_text("\n".join(parts) + "\n", encoding="utf-8")


def draw_center(draw, xy, text, font, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    draw.text((xy[0] - (bbox[2] - bbox[0]) / 2, xy[1] - (bbox[3] - bbox[1]) / 2), text, font=font, fill=fill)


def render_png(papers: list[dict], destination: Path):
    image = Image.new("RGB", (WIDTH, HEIGHT), "#F7F9FC")
    draw = ImageDraw.Draw(image)
    draw_center(draw, (WIDTH / 2, 47), "2025–2026 Top-Conference Paper Figure Candidate Benchmark", FONTS["title"], "#172B4D")
    draw_center(draw, (WIDTH / 2, 82), "40 papers · 100 planned target Figures · official proceedings only · candidate stage for visual audit", FONTS["subtitle"], "#52677D")
    stat_items = [("40", "papers"), ("100", "Figure slots"), ("4", "venues"), ("13", "visual roles")]
    sx = WIDTH / 2 - 390
    for index, (value, label) in enumerate(stat_items):
        x = sx + index * 260
        draw.rounded_rectangle((x, 105, x + 210, 167), radius=16, fill="#FFFFFF", outline="#D5DEE8", width=2)
        draw_center(draw, (x + 42, 137), value, load_font(27, True), "#172B4D")
        draw_center(draw, (x + 123, 137), label, load_font(15), "#52677D")
    by_venue = {venue: [p for p in papers if p["venue"] == venue] for venue in VENUES}
    for col, venue in enumerate(VENUES):
        color = COLORS[venue]
        pale = tuple((c + target) // 2 for c, target in zip(color, (245, 247, 250)))
        x = MARGIN + col * (COL_W + COL_GAP)
        draw.rounded_rectangle((x, TOP - 38, x + COL_W, HEIGHT - 42), radius=24, fill=pale, outline=tuple((c + 255) // 2 for c in color), width=2)
        draw.rounded_rectangle((x, TOP - 38, x + COL_W, TOP + 18), radius=20, fill=color)
        draw.text((x + 20, TOP - 27), venue, font=FONTS["venue"], fill="white")
        years = Counter(p["year"] for p in by_venue[venue])
        year_text = " · ".join(f"{year}: {count}" for year, count in sorted(years.items()))
        bbox = draw.textbbox((0, 0), year_text, font=FONTS["meta"])
        draw.text((x + COL_W - 18 - bbox[2], TOP - 23), year_text, font=FONTS["meta"], fill="white")
        for row, paper in enumerate(by_venue[venue]):
            y = TOP + 30 + row * (CARD_H + CARD_GAP)
            draw.rounded_rectangle((x + 10, y, x + COL_W - 10, y + CARD_H), radius=16, fill="white", outline="#D5DEE8", width=2)
            draw.rounded_rectangle((x + 10, y, x + 18, y + CARD_H), radius=4, fill=color)
            draw.rounded_rectangle((x + 30, y + 14, x + 84, y + 39), radius=12, fill=pale)
            draw_center(draw, (x + 57, y + 26), str(paper["year"]), FONTS["chip"], color)
            for line_index, line in enumerate(wrap(paper["short_title"], 34, 2)):
                draw.text((x + 96, y + 14 + line_index * 21), line, font=FONTS["paper"], fill="#20364A")
            draw.text((x + 30, y + 61), paper["grammar"], font=FONTS["meta"], fill="#52677D")
            chip_x = x + 30
            for role in paper["target_roles"]:
                label = ROLE_LABELS[role]
                chip_w = max(68, 14 + len(label) * 8)
                draw.rounded_rectangle((chip_x, y + 94, chip_x + chip_w, y + 119), radius=12, fill=pale, outline=color, width=1)
                draw_center(draw, (chip_x + chip_w / 2, y + 106), label, FONTS["chip"], color)
                chip_x += chip_w + 7
    draw.text((MARGIN, HEIGHT - 32), "Next gate: verify PDF page + Figure number + caption + visual score before promotion to gold reference.", font=FONTS["meta"], fill="#52677D")
    footer = "Editable SVG · no source paper artwork redistributed"
    bbox = draw.textbbox((0, 0), footer, font=FONTS["meta"])
    draw.text((WIDTH - MARGIN - bbox[2], HEIGHT - 32), footer, font=FONTS["meta"], fill="#52677D")
    image.save(destination, dpi=(300, 300))


def main():
    payload = json.loads(SEED.read_text(encoding="utf-8"))
    papers = payload["papers"]
    figures = validate(payload)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with (DATA_DIR / "figures.jsonl").open("w", encoding="utf-8") as handle:
        for figure in figures:
            handle.write(json.dumps(figure, ensure_ascii=False) + "\n")
    with (DATA_DIR / "papers.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["id", "venue", "year", "short_title", "grammar", "figure_slots", "official_url"])
        writer.writeheader()
        for paper in papers:
            writer.writerow({
                "id": paper["id"], "venue": paper["venue"], "year": paper["year"],
                "short_title": paper["short_title"], "grammar": paper["grammar"],
                "figure_slots": len(paper["target_roles"]), "official_url": paper["official_url"],
            })
    summary = {
        "selection_stage": payload["selection_stage"],
        "papers": len(papers),
        "planned_figures": len(figures),
        "venue_counts": dict(Counter(p["venue"] for p in papers)),
        "year_counts": dict(Counter(str(p["year"]) for p in papers)),
        "role_counts": dict(Counter(f["planned_role"] for f in figures)),
        "pending_visual_audit": len(figures),
    }
    (DATA_DIR / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    render_svg(papers, OUT_DIR / "candidate-overview.svg")
    render_png(papers, OUT_DIR / "candidate-overview.png")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
