#!/usr/bin/env python3
import html, json, sys
from pathlib import Path

def e(v): return html.escape(str(v), quote=True)

def lines(label, width):
    words=str(label).split(); out=[]; cur=[]; limit=max(8,int((width-24)/9))
    for word in words:
        if cur and len(" ".join(cur+[word]))>limit: out.append(" ".join(cur)); cur=[word]
        else: cur.append(word)
    if cur: out.append(" ".join(cur))
    return out or [""]

def title_lines(value, limit=62):
    value=" ".join(str(value).split())
    if len(value)<=limit: return [value]
    words=value.split(); choices=[]
    for i in range(1,len(words)):
        left,right=" ".join(words[:i])," ".join(words[i:])
        choices.append((max(len(left),len(right)),abs(len(left)-len(right)),left,right))
    _,_,left,right=min(choices)
    return [left,right]

def boundary(a,b):
    acx,acy=a["x"]+a["w"]/2,a["y"]+a["h"]/2; bcx,bcy=b["x"]+b["w"]/2,b["y"]+b["h"]/2
    dx,dy=bcx-acx,bcy-acy
    if abs(dx)/max(a["w"],1)>=abs(dy)/max(a["h"],1):
        return (a["x"]+(a["w"] if dx>=0 else 0),acy),(b["x"]+(0 if dx>=0 else b["w"]),bcy)
    return (acx,a["y"]+(a["h"] if dy>=0 else 0)),(bcx,b["y"]+(0 if dy>=0 else b["h"]))

def icon(kind,n):
    x,y,w,h=n["x"],n["y"],n["w"],n["h"]; cx=x+w/2
    s=[]; top=y+18; bottom=y+h-42; ink="#3D6078"; accent="#4B98C8"
    if kind=="tensor":
        for k in range(3):
            ox=k*13; oy=(2-k)*10
            s.append(f'<rect x="{x+32+ox}" y="{top+oy}" width="{w-90}" height="{max(42,h-92)}" rx="5" fill="{["#D8EEF5","#C5E3F0","#A9D5E8"][k]}" stroke="{ink}" stroke-width="2"/>')
        for j in range(1,4):
            xx=x+58+j*(w-115)/4; s.append(f'<line x1="{xx}" y1="{top+20}" x2="{xx}" y2="{bottom-4}" stroke="#FFFFFF" stroke-width="1.5" opacity=".9"/>')
    elif kind=="tokens":
        count=7; gap=5; cw=(w-48-(count-1)*gap)/count
        for i in range(count):
            fill=["#76B7D8","#90C6A0","#E9B66C","#B39AD5"][i%4]
            s.append(f'<rect x="{x+24+i*(cw+gap):.1f}" y="{top+15+(i%2)*8}" width="{cw:.1f}" height="{max(30,h-92)}" rx="4" fill="{fill}" stroke="{ink}" stroke-width="1.5"/>')
    elif kind=="graph":
        pts=[(.22,.32),(.5,.18),(.78,.35),(.32,.68),(.62,.72),(.82,.62)]
        coords=[(x+px*w,y+22+py*(h-70)) for px,py in pts]
        for a,b in [(0,1),(1,2),(0,3),(1,4),(2,5),(3,4),(4,5),(2,4)]:
            s.append(f'<line x1="{coords[a][0]}" y1="{coords[a][1]}" x2="{coords[b][0]}" y2="{coords[b][1]}" stroke="{ink}" stroke-width="2"/>')
        colors=["#9DC7E0","#F0BC8C","#A9D3A5","#C2AEDC","#F2A7A7","#9DC7E0"]
        for (px,py),c in zip(coords,colors): s.append(f'<circle cx="{px}" cy="{py}" r="10" fill="{c}" stroke="{ink}" stroke-width="2"/>')
    elif kind in ("stack","attention"):
        for k in range(3,0,-1):
            s.append(f'<rect x="{x+25-k*5}" y="{top+k*6}" width="{w-45}" height="{max(58,h-98)}" rx="9" fill="#E8EEF4" stroke="{ink}" stroke-width="1.5" opacity="{.45+k*.16}"/>')
        inner_y=top+22
        blocks=[("Cross-Attention","#F3A37E"),("Add & Norm","#9BCF9B"),("FFN","#AFC7DC")] if kind=="attention" else [("Projection","#AFC7DC"),("Gated Fusion","#F3B978"),("Normalization","#9BCF9B")]
        bh=max(18,(h-120)/3)
        for i,(lab,fill) in enumerate(blocks):
            yy=inner_y+i*(bh+6); s.append(f'<rect x="{x+42}" y="{yy}" width="{w-84}" height="{bh}" rx="5" fill="{fill}" stroke="{ink}" stroke-width="1.5"/>')
            if h>165: s.append(f'<text x="{cx}" y="{yy+bh/2+5}" text-anchor="middle" font-family="Arial" font-size="14" fill="#19324A">{e(lab)}</text>')
    elif kind=="document":
        px=x+w*.34; py=top; pw=w*.32; ph=max(55,h-75)
        s.append(f'<path d="M {px} {py} H {px+pw*.7} L {px+pw} {py+ph*.25} V {py+ph} H {px} Z" fill="#FFFFFF" stroke="{ink}" stroke-width="2.5"/>')
        s.append(f'<path d="M {px+pw*.7} {py} V {py+ph*.25} H {px+pw}" fill="none" stroke="{ink}" stroke-width="2"/>')
        for i in range(3): s.append(f'<line x1="{px+12}" y1="{py+ph*.43+i*13}" x2="{px+pw-12}" y2="{py+ph*.43+i*13}" stroke="#9BAFBD" stroke-width="2"/>')
    elif kind=="plot":
        bx=x+38; by=bottom-5; pw=w-76; ph=max(45,h-100)
        s.append(f'<path d="M {bx} {top+10} V {by} H {bx+pw}" fill="none" stroke="{ink}" stroke-width="2"/>')
        vals=[.45,.72,.58,.88]; bw=pw/7
        for i,v in enumerate(vals): s.append(f'<rect x="{bx+18+i*bw*1.45}" y="{by-v*ph}" width="{bw}" height="{v*ph}" rx="3" fill="{["#AFC7DC","#B8B8C4","#B8B8C4","#4B98C8"][i]}"/>')
    elif kind=="model":
        cols=[[(-.22,0),(-.22,.45)],[(0,-.1),(0,.28),(0,.62)],[(.22,.1),(.22,.5)]]
        pts=[]
        for ci,col in enumerate(cols):
            cp=[]
            for px,py in col:
                cp.append((cx+px*w,y+28+py*max(40,h-100)))
            pts.append(cp)
        for a in pts[0]:
            for b in pts[1]: s.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#9AB0BF" stroke-width="1.5"/>')
        for a in pts[1]:
            for b in pts[2]: s.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#9AB0BF" stroke-width="1.5"/>')
        for col in pts:
            for px,py in col: s.append(f'<circle cx="{px}" cy="{py}" r="8" fill="#8FC2DC" stroke="{ink}" stroke-width="2"/>')
    else: return []
    return s

def main(src,dst):
    spec=json.loads(Path(src).read_text(encoding="utf-8-sig")); c=spec["canvas"]; w,h=c["width"],c["height"]
    nodes={n["id"]:n for n in spec.get("nodes",[])}
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
    '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0 L10 5 L0 10z" fill="context-stroke"/></marker><filter id="shadow" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#20364A" flood-opacity=".12"/></filter></defs>',
    f'<rect width="{w}" height="{h}" fill="{e(c.get("background","#fff"))}"/>']
    if spec.get("title"):
        title=title_lines(spec["title"])
        start=43 if len(title)==2 else 58
        for i,line in enumerate(title): out.append(f'<text id="figure-title-{i+1}" x="{w/2}" y="{start+i*34}" text-anchor="middle" font-family="Arial" font-size="31" font-weight="700" fill="#172B4D">{e(line)}</text>')
    for p in spec.get("panels",[]):
        out += [f'<g id="{e(p["id"])}"><rect x="{p["x"]}" y="{p["y"]}" width="{p["w"]}" height="{p["h"]}" rx="26" fill="{e(p.get("fill","#F4F6F8"))}" stroke="#CAD5DE" stroke-width="2"/>',
        f'<text x="{p["x"]+24}" y="{p["y"]+42}" font-family="Arial" font-size="23" font-weight="700" fill="#172B4D">{e(p["label"])}</text></g>']
    for edge in spec.get("edges",[]):
        if edge["source"] not in nodes or edge["target"] not in nodes: continue
        (sx,sy),(tx,ty)=boundary(nodes[edge["source"]],nodes[edge["target"]]); color=edge.get("color","#47789E")
        dash=' stroke-dasharray="10 8"' if edge.get("style") in ("dashed","feedback") else ""
        path=f'M {sx:.1f} {sy:.1f} L {tx:.1f} {ty:.1f}'
        out.append(f'<g id="{e(edge["id"])}"><path d="{path}" fill="none" stroke="{e(color)}" stroke-width="{edge.get("width",4)}"{dash} marker-end="url(#arrow)"/>')
        if edge.get("label"):
            mx,my=(sx+tx)/2,(sy+ty)/2-10
            out.append(f'<text x="{mx:.1f}" y="{my:.1f}" text-anchor="middle" font-family="Arial" font-size="16" fill="#52677D" paint-order="stroke" stroke="#FFFFFF" stroke-width="8">{e(edge["label"])}</text>')
        out.append('</g>')
    visual={"tensor","tokens","graph","stack","attention","document","plot","model"}
    for n in spec.get("nodes",[]):
        kind=n.get("kind","model"); radius=36 if kind=="loss" else n.get("radius",16)
        out.append(f'<g id="{e(n["id"])}" filter="url(#shadow)"><rect x="{n["x"]}" y="{n["y"]}" width="{n["w"]}" height="{n["h"]}" rx="{radius}" fill="{e(n.get("fill","#E5EEF5"))}" stroke="{e(n.get("stroke","#426986"))}" stroke-width="2.5"/>')
        out.extend(icon(kind,n))
        ls=lines(n["label"],n["w"])
        if kind in visual:
            base=n["y"]+n["h"]-18-(len(ls)-1)*20
        else:
            base=n["y"]+n["h"]/2-(len(ls)-1)*11+7
        for i,line in enumerate(ls):
            out.append(f'<text x="{n["x"]+n["w"]/2}" y="{base+i*22}" text-anchor="middle" font-family="Arial" font-size="{18 if kind in visual else 20}" font-weight="600" fill="{e(n.get("text_color","#172B4D"))}">{e(line)}</text>')
        out.append('</g>')
    for a in spec.get("annotations",[]):
        out.append(f'<g id="{e(a["id"])}"><rect x="{a["x"]}" y="{a["y"]}" width="{a["w"]}" height="{a["h"]}" rx="12" fill="none" stroke="{e(a.get("color","#E07B67"))}" stroke-width="3" stroke-dasharray="9 7"/><text x="{a["x"]+12}" y="{a["y"]-10}" font-family="Arial" font-size="17" font-weight="700" fill="{e(a.get("color","#E07B67"))}">{e(a.get("label","Zoom-in"))}</text></g>')
    out.append('</svg>'); Path(dst).write_text("\n".join(out),encoding="utf-8"); print(f"Wrote editable SVG: {dst}")

if __name__=="__main__":
    if len(sys.argv)!=3: raise SystemExit("usage: render_svg.py SPEC.json OUTPUT.svg")
    main(sys.argv[1],sys.argv[2])
