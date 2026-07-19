#!/usr/bin/env python3
"""Generate a dense research-method PNG from the documented user prompt."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "examples" / "user-prompt-demo" / "multi-agent-multimodal-rag.png"
W, H = 1900, 1080

INK = "#17324D"
MUTED = "#60758A"
BLUE = "#337FB4"
ORANGE = "#E18435"
PURPLE = "#7A5AB5"
GREEN = "#4F965B"
RED = "#D45B5B"


def font(size, bold=False):
    candidates = [
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


F = {"title": font(34, True), "subtitle": font(18), "panel": font(22, True), "card": font(17, True), "small": font(13), "tiny": font(12, True)}


def centered(draw, box, text, fnt, fill=INK, max_lines=2, spacing=3):
    x, y, w, h = box
    words = str(text).split()
    lines, current = [], []
    for word in words:
        trial = " ".join(current + [word])
        if current and draw.textbbox((0, 0), trial, font=fnt)[2] > w - 16:
            lines.append(" ".join(current)); current = [word]
        else:
            current.append(word)
    if current:
        lines.append(" ".join(current))
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip(" .") + "…"
    heights = [draw.textbbox((0, 0), line, font=fnt)[3] for line in lines]
    total = sum(heights) + spacing * (len(lines) - 1)
    yy = y + (h - total) / 2
    for line, height in zip(lines, heights):
        bbox = draw.textbbox((0, 0), line, font=fnt)
        draw.text((x + (w - (bbox[2] - bbox[0])) / 2, yy), line, font=fnt, fill=fill)
        yy += height + spacing


def shadow_card(draw, box, fill, stroke, radius=16, width=2):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle((x1 + 5, y1 + 7, x2 + 5, y2 + 7), radius=radius, fill="#D7E0E8")
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=stroke, width=width)


def arrow(draw, points, color=BLUE, width=4, dashed=False):
    for a, b in zip(points, points[1:]):
        if dashed:
            dx, dy = b[0] - a[0], b[1] - a[1]
            length = max(1, math.hypot(dx, dy)); ux, uy = dx / length, dy / length
            pos = 0
            while pos < length - 4:
                end = min(pos + 10, length)
                draw.line((a[0] + ux * pos, a[1] + uy * pos, a[0] + ux * end, a[1] + uy * end), fill=color, width=width)
                pos += 18
        else:
            draw.line((*a, *b), fill=color, width=width, joint="curve")
    a, b = points[-2], points[-1]
    angle = math.atan2(b[1] - a[1], b[0] - a[0]); size = 14
    draw.polygon([b, (b[0] - size * math.cos(angle - .48), b[1] - size * math.sin(angle - .48)), (b[0] - size * math.cos(angle + .48), b[1] - size * math.sin(angle + .48))], fill=color)


def token_icon(draw, box):
    x1, y1, x2, y2 = box; colors = ["#62AADD", "#F0B35E", "#8BC58B", "#B99BDD"]
    n, gap = 7, 5; bw = (x2 - x1 - gap * (n - 1)) / n
    for i in range(n):
        yy = y1 + (i % 2) * 8
        draw.rounded_rectangle((x1 + i * (bw + gap), yy, x1 + i * (bw + gap) + bw, y2), radius=4, fill=colors[i % 4], outline="#42647F", width=1)


def tensor_icon(draw, box):
    x1, y1, x2, y2 = box
    for i, color in enumerate(["#D7ECF6", "#B9DCEC", "#92C8E0"]):
        ox, oy = i * 12, (2 - i) * 8
        draw.rounded_rectangle((x1 + ox, y1 + oy, x2 - 24 + ox, y2 - 16 + oy), radius=7, fill=color, outline="#42647F", width=2)
        for j in range(1, 4):
            xx = x1 + ox + j * (x2 - x1 - 24) / 4
            draw.line((xx, y1 + oy + 5, xx, y2 - 16 + oy - 5), fill="#FFFFFF", width=2)


def graph_icon(draw, box, accent=GREEN):
    x1, y1, x2, y2 = box
    pts = [(x1 + .12*(x2-x1), y1 + .55*(y2-y1)), (x1 + .42*(x2-x1), y1 + .18*(y2-y1)), (x1 + .75*(x2-x1), y1 + .35*(y2-y1)), (x1 + .35*(x2-x1), y1 + .78*(y2-y1)), (x1 + .83*(x2-x1), y1 + .75*(y2-y1))]
    for a, b in [(0,1),(1,2),(0,3),(1,3),(2,4),(3,4),(2,3)]: draw.line((*pts[a], *pts[b]), fill="#46667E", width=2)
    fills = ["#8EC4DE", "#F1B873", "#9CCC9D", "#BEA6DA", "#F19B9B"]
    for pt, fill in zip(pts, fills): draw.ellipse((pt[0]-8,pt[1]-8,pt[0]+8,pt[1]+8), fill=fill, outline="#36546D", width=2)


def agent_icon(draw, box, color):
    x1, y1, x2, y2 = box; cx=(x1+x2)/2
    draw.ellipse((cx-15,y1,cx+15,y1+30),fill=color,outline="#3D5870",width=2)
    draw.rounded_rectangle((cx-30,y1+34,cx+30,y2),radius=12,fill="#FFFFFF",outline="#3D5870",width=2)
    draw.line((cx-17,y1+49,cx+17,y1+49),fill=color,width=4)


def database_icon(draw, box):
    x1,y1,x2,y2=box
    draw.ellipse((x1,y1,x2,y1+24),fill="#F5C782",outline="#8A6535",width=2)
    draw.rectangle((x1,y1+12,x2,y2-12),fill="#F9DDAE",outline="#8A6535",width=2)
    draw.ellipse((x1,y2-24,x2,y2),fill="#F5C782",outline="#8A6535",width=2)
    draw.arc((x1,y1+18,x2,y1+43),0,180,fill="#8A6535",width=2)


def card(draw, box, title, fill, stroke, icon=None, icon_color=None):
    shadow_card(draw, box, fill, stroke)
    x1,y1,x2,y2=box
    ib=(x1+24,y1+17,x2-24,y2-48)
    if icon == "tokens": token_icon(draw, ib)
    elif icon == "tensor": tensor_icon(draw, ib)
    elif icon == "graph": graph_icon(draw, ib, icon_color or GREEN)
    elif icon == "agent": agent_icon(draw, ib, icon_color or PURPLE)
    elif icon == "database": database_icon(draw, ib)
    centered(draw,(x1+10,y2-43,x2-x1-20,35),title,F["card"],max_lines=2)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    image=Image.new("RGB",(W,H),"#FFFFFF"); draw=ImageDraw.Draw(image)
    centered(draw,(0,16,W,42),"Confidence-Aware Multi-Agent Multimodal RAG",F["title"],max_lines=1)
    centered(draw,(0,55,W,30),"Dynamic Routing, Shared Evidence Memory and Verifier-Guided Retrieval",F["subtitle"],MUTED,max_lines=1)

    panels=[
        (28,105,335,995,"1  Multimodal Task","#F0F6FA",BLUE),
        (360,105,765,995,"2  Perception & Retrieval","#FFF6EA",ORANGE),
        (790,105,1510,995,"3  Agentic Reasoning Workspace","#F6F1FB",PURPLE),
        (1535,105,1872,995,"4  Verifiable Output","#F0F8F0",GREEN),
    ]
    for x1,y1,x2,y2,label,fill,stroke in panels:
        draw.rounded_rectangle((x1,y1,x2,y2),radius=24,fill=fill,outline="#CBD6E0",width=2)
        draw.rounded_rectangle((x1+12,y1+12,x2-12,y1+58),radius=16,fill=stroke)
        draw.text((x1+27,y1+23),label,font=F["panel"],fill="white")

    # Connections are drawn before cards.
    arrow(draw,[(287,250),(398,250)],BLUE)
    arrow(draw,[(287,455),(375,455),(375,430),(398,430)],BLUE)
    arrow(draw,[(287,690),(375,690),(375,620),(398,620)],ORANGE)
    arrow(draw,[(287,865),(375,865),(375,810),(398,810)],ORANGE)
    arrow(draw,[(715,250),(835,250)],BLUE)
    arrow(draw,[(715,430),(790,430),(790,330),(835,330)],ORANGE)
    arrow(draw,[(715,620),(790,620),(790,410),(835,410)],ORANGE)
    arrow(draw,[(715,810),(820,810),(820,745),(875,745)],ORANGE)
    arrow(draw,[(1045,255),(1110,255)],PURPLE)
    arrow(draw,[(1045,335),(1110,420)],PURPLE)
    arrow(draw,[(1045,415),(1110,585)],PURPLE)
    arrow(draw,[(1220,310),(1220,390)],PURPLE)
    arrow(draw,[(1220,505),(1220,545)],PURPLE)
    arrow(draw,[(1220,660),(1220,705)],PURPLE)
    arrow(draw,[(1340,790),(1575,790)],GREEN)
    arrow(draw,[(1340,790),(1470,790),(1470,315),(1575,315)],GREEN)
    arrow(draw,[(1340,790),(1495,790),(1495,555),(1575,555)],GREEN)
    arrow(draw,[(1115,880),(900,930),(680,930),(680,845)],RED,4,True)
    arrow(draw,[(1115,850),(950,850),(950,735),(1040,735)],RED,3,True)

    # Input and retrieval cards.
    card(draw,(68,185,287,315),"Text Query","#E4F1F8",BLUE,"tokens")
    card(draw,(68,385,287,525),"Image / Video","#EAF1F7",BLUE,"tensor")
    card(draw,(68,610,287,760),"Domain Corpus","#FFF0DB",ORANGE,"database")
    card(draw,(68,805,287,925),"Knowledge Graph","#EAF4E8",GREEN,"graph")
    card(draw,(398,175,715,325),"Multimodal Token Encoder","#E1EFF7",BLUE,"tensor")
    card(draw,(398,365,715,500),"Hybrid Dense Retriever","#FFF0DC",ORANGE,"database")
    card(draw,(398,550,715,690),"Graph Evidence Retriever","#EAF4E8",GREEN,"graph")
    card(draw,(398,745,715,875),"Evidence Cache","#F4E8D8",ORANGE,"tokens")

    # Planner, routing, specialists and verification.
    card(draw,(835,185,1045,465),"Task-Graph Planner","#E9DFF4",PURPLE,"graph")
    shadow_card(draw,(1110,195,1330,310),"#F4E9FA",PURPLE)
    draw.polygon([(1220,212),(1280,252),(1220,292),(1160,252)],fill="#C8AFE0",outline=PURPLE)
    centered(draw,(1120,268,200,34),"Dynamic Router",F["card"])
    card(draw,(1085,390,1265,505),"Visual Analyst","#E2F0F7",BLUE,"agent",BLUE)
    card(draw,(1300,390,1480,505),"KG Reasoner","#E9F4E8",GREEN,"agent",GREEN)
    card(draw,(1085,545,1265,660),"Tool Executor","#FFF0DC",ORANGE,"agent",ORANGE)
    card(draw,(1300,545,1480,660),"Shared Memory","#EFE7F6",PURPLE,"tokens")
    card(draw,(875,705,1095,885),"Evidence Fusion","#E2EDF7",BLUE,"tensor")
    card(draw,(1115,705,1340,885),"Critic / Verifier","#FBE7E5",RED,"agent",RED)

    # Outputs.
    card(draw,(1575,205,1835,405),"Grounded Answer","#E5F3E5",GREEN,"tokens")
    card(draw,(1575,465,1835,645),"Evidence Citations","#FFF3DE",ORANGE,"graph")
    shadow_card(draw,(1575,720,1835,865),"#E6F2E7",GREEN)
    draw.line((1610,820,1610,760),fill=INK,width=2); draw.line((1610,820,1800,820),fill=INK,width=2)
    vals=[.52,.71,.86]; cols=["#B8C9D5","#8DB8D1",GREEN]
    for i,(v,c) in enumerate(zip(vals,cols)): draw.rounded_rectangle((1640+i*50,820-v*65,1670+i*50,820),radius=3,fill=c)
    centered(draw,(1590,826,230,32),"Confidence & Uncertainty",F["card"])

    # Innovation callout and semantic legend.
    draw.rounded_rectangle((1062,175,1498,682),radius=20,outline="#A35791",width=3)
    for x in range(1075,1490,22): draw.line((x,175,min(x+11,1498),175),fill="#A35791",width=3)
    draw.rounded_rectangle((1078,158,1288,187),radius=13,fill="#FFFFFF",outline="#A35791",width=2)
    centered(draw,(1085,159,195,26),"Innovation zoom-in",F["tiny"],"#A35791",max_lines=1)

    legend=[(BLUE,"representation"),(ORANGE,"retrieval/tool"),(PURPLE,"reasoning"),(GREEN,"verified evidence"),(RED,"feedback")]
    lx=850
    for color,label in legend:
        draw.rounded_rectangle((lx,1015,lx+18,1033),radius=4,fill=color)
        draw.text((lx+25,1015),label,font=F["small"],fill=MUTED)
        lx += 135 + len(label)*3

    image.save(OUT,dpi=(300,300))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
