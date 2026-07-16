#!/usr/bin/env python3
import json, math, sys, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FONT = Path(r"C:\Windows\Fonts\arial.ttf")
BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")

def font(size, bold=False):
    return ImageFont.truetype(str(BOLD if bold else FONT), size)

def center_text(draw, box, text, size=21, bold=False, fill="#172B4D"):
    x, y, w, h = box
    lines = textwrap.wrap(str(text), max(8, int((w - 28) / (size * .52)))) or [""]
    f = font(size, bold)
    heights = [draw.textbbox((0, 0), line, font=f)[3] for line in lines]
    total = sum(heights) + (len(lines)-1)*6
    cy = y + (h-total)/2
    for line, lh in zip(lines, heights):
        bbox = draw.textbbox((0, 0), line, font=f)
        draw.text((x+(w-(bbox[2]-bbox[0]))/2, cy), line, font=f, fill=fill)
        cy += lh + 6

def boundary(a, b):
    ac=(a["x"]+a["w"]/2,a["y"]+a["h"]/2); bc=(b["x"]+b["w"]/2,b["y"]+b["h"]/2)
    dx,dy=bc[0]-ac[0],bc[1]-ac[1]
    if abs(dx)/a["w"] >= abs(dy)/a["h"]:
        return (a["x"]+(a["w"] if dx>=0 else 0),ac[1]),(b["x"]+(0 if dx>=0 else b["w"]),bc[1])
    return (ac[0],a["y"]+(a["h"] if dy>=0 else 0)),(bc[0],b["y"]+(0 if dy>=0 else b["h"]))

def arrow(draw, start, end, color, width, dashed=False):
    sx,sy=start; tx,ty=end
    if dashed:
        length=math.hypot(tx-sx,ty-sy); ux=(tx-sx)/length; uy=(ty-sy)/length
        pos=0
        while pos < length-16:
            a=pos; b=min(pos+12,length-16)
            draw.line((sx+ux*a,sy+uy*a,sx+ux*b,sy+uy*b),fill=color,width=width)
            pos += 20
    else: draw.line((sx,sy,tx,ty),fill=color,width=width)
    ang=math.atan2(ty-sy,tx-sx); s=15
    pts=[(tx,ty),(tx-s*math.cos(ang-.48),ty-s*math.sin(ang-.48)),(tx-s*math.cos(ang+.48),ty-s*math.sin(ang+.48))]
    draw.polygon(pts,fill=color)

def main(src,dst):
    spec=json.loads(Path(src).read_text(encoding="utf-8-sig")); c=spec["canvas"]
    im=Image.new("RGB",(c["width"],c["height"]),c.get("background","#FFFFFF")); d=ImageDraw.Draw(im)
    if spec.get("title"): center_text(d,(0,18,c["width"],55),spec["title"],30,True)
    for p in spec.get("panels",[]):
        d.rounded_rectangle((p["x"],p["y"],p["x"]+p["w"],p["y"]+p["h"]),radius=24,fill=p.get("fill","#F4F6F8"),outline="#C9D3DD",width=2)
        center_text(d,(p["x"],p["y"]+12,p["w"],48),p["label"],24,True)
    nodes={n["id"]:n for n in spec.get("nodes",[])}
    for e in spec.get("edges",[]):
        if e["source"] not in nodes or e["target"] not in nodes: continue
        s,t=boundary(nodes[e["source"]],nodes[e["target"]]); color=e.get("color","#436E95")
        arrow(d,s,t,color,int(e.get("width",4)),e.get("style") in ("dashed","feedback"))
        if e.get("label"):
            mx,my=(s[0]+t[0])/2,(s[1]+t[1])/2-25
            box=d.textbbox((0,0),e["label"],font=font(17))
            d.rectangle((mx-(box[2]-box[0])/2-5,my-2,mx+(box[2]-box[0])/2+5,my+(box[3]-box[1])+3),fill="#FFFFFF")
            d.text((mx-(box[2]-box[0])/2,my),e["label"],font=font(17),fill="#52677D")
    for n in spec.get("nodes",[]):
        d.rounded_rectangle((n["x"],n["y"],n["x"]+n["w"],n["y"]+n["h"]),radius=n.get("radius",16),fill=n.get("fill","#E5EEF5"),outline=n.get("stroke","#426986"),width=3)
        center_text(d,(n["x"],n["y"],n["w"],n["h"]),n["label"],21,True,n.get("text_color","#172B4D"))
    im.save(dst)
    print(f"Wrote preview PNG: {dst}")

if __name__=="__main__":
    if len(sys.argv)!=3: raise SystemExit("usage: render_preview.py SPEC.json OUTPUT.png")
    main(sys.argv[1],sys.argv[2])
