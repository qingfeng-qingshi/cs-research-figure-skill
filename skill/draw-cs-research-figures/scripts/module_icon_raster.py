#!/usr/bin/env python3
"""Semantic raster previews for the editable module SVG library."""

from __future__ import annotations

import math


INK = "#233B53"
BLUE = "#4C86B6"
GREEN = "#5B9561"
ORANGE = "#D48345"
PURPLE = "#8062A8"
RED = "#C96863"


def draw_module_icon(draw, kind, box):
    """Draw one semantically distinct preview icon in a normalized 100x70 box."""
    x, y, w, h = box
    px = lambda value: x + value * w / 100
    py = lambda value: y + value * h / 70
    sw = max(1, round(min(w, h) / 45))

    def rect(a, b, c, d, fill="#E8EFF4", outline=INK, radius=4, width=sw):
        draw.rounded_rectangle((px(a), py(b), px(c), py(d)), radius=max(2, radius*w/100), fill=fill, outline=outline, width=width)

    def line(a, b, c, d, fill=INK, width=sw):
        draw.line((px(a), py(b), px(c), py(d)), fill=fill, width=width)

    def circle(a, b, radius=5, fill="#A9D1E6", outline=INK, width=sw):
        rx, ry = radius*w/100, radius*h/70
        draw.ellipse((px(a)-rx, py(b)-ry, px(a)+rx, py(b)+ry), fill=fill, outline=outline, width=width)

    def arrow(a, b, c, d, fill=BLUE, width=sw):
        line(a,b,c,d,fill,width)
        angle=math.atan2(py(d)-py(b),px(c)-px(a)); size=max(4,min(w,h)*.055)
        end=(px(c),py(d))
        draw.polygon([end,(end[0]-size*math.cos(angle-.5),end[1]-size*math.sin(angle-.5)),(end[0]-size*math.cos(angle+.5),end[1]-size*math.sin(angle+.5))],fill=fill)

    if kind == "llm":
        for i in range(4): rect(28+i*5,12+i*4,72+i*5,48+i*4,["#EDF3F7","#DBE9F2","#C8DFEC","#AED3E6"][i],BLUE,4)
        for i in range(6): rect(22+i*10,59,29+i*10,67,["#7FB7D5","#9BC79E","#E4B06D"][i%3],INK,1)
        arrow(83,15,83,49,PURPLE)
    elif kind == "prompt":
        rect(24,8,65,59,"#FFFFFF",BLUE,3); line(31,23,56,23,"#9BACB8"); line(31,32,56,32,"#9BACB8"); line(31,41,50,41,"#9BACB8")
        rect(70,18,91,48,"#F3E5CF",ORANGE,5); arrow(64,34,70,34,ORANGE)
    elif kind == "rag":
        circle(18,33,8,"#FFFFFF",BLUE); line(23,39,30,47,BLUE,2)
        rect(35,12,58,55,"#FFFFFF",BLUE,3); rect(68,14,91,54,"#E7F1E5",GREEN,7)
        arrow(28,33,35,33,BLUE); arrow(58,33,68,33,GREEN); line(73,25,86,25,"#9CACB6"); line(73,34,86,34,"#9CACB6")
    elif kind == "vector-db":
        draw.ellipse((px(27),py(8),px(75),py(23)),fill="#E3EFF6",outline=BLUE,width=sw); draw.rectangle((px(27),py(15),px(75),py(56)),fill="#E3EFF6",outline=BLUE,width=sw); draw.arc((px(27),py(47),px(75),py(62)),0,180,fill=BLUE,width=sw)
        for i,hh in enumerate((16,29,21,35,25)): rect(35+i*7,49-hh*.7,39+i*7,49,["#77B7D8","#8FC398","#E2AE69"][i%3],INK,1,1)
        arrow(79,34,94,34,PURPLE)
    elif kind == "reranker":
        for i,(yy,ww) in enumerate(((8,58),(27,48),(46,38))): rect(29,yy,29+ww,yy+14,["#C3DDEB","#DCE9F1","#F3E3CD"][i],BLUE,3)
        for i,yy in enumerate((15,34,53),1):
            circle(18,yy,6,"#FFFFFF",ORANGE); draw.text((px(15),py(yy-5)),str(i),fill=INK)
    elif kind == "lora":
        rect(40,7,72,61,"#DDE5EB",INK,5); rect(12,17,27,50,"#F4E1C5",ORANGE,3); rect(78,18,92,49,"#E7DDF0",PURPLE,3)
        arrow(27,25,40,25,ORANGE); arrow(72,43,78,43,PURPLE); line(18,28,22,39,ORANGE,2); line(22,39,26,28,ORANGE,2)
    elif kind == "moe":
        rect(8,23,27,47,"#F1DFC5",ORANGE,4); draw.polygon([(px(37),py(21)),(px(56),py(35)),(px(37),py(49))],fill="#DCCEE8",outline=PURPLE)
        arrow(27,35,37,35,ORANGE)
        for yy,color in ((5,"#D8EAF4"),(27,"#E5F0E2"),(49,"#F3E1DE")): rect(66,yy,94,yy+16,color,BLUE,4)
        for yy in (13,35,57): arrow(56,35,66,yy,PURPLE)
    elif kind == "kv-cache":
        rect(10,11,44,59,"#D9E9F3",BLUE,5); rect(56,11,90,59,"#E8E0F1",PURPLE,5)
        draw.text((px(24),py(27)),"K",fill=INK); draw.text((px(70),py(27)),"V",fill=INK)
        for i in range(3): rect(16+i*9,43,22+i*9,54,"#FFFFFF",INK,1,1); rect(62+i*9,43,68+i*9,54,"#FFFFFF",INK,1,1)
    elif kind == "alignment":
        rect(8,11,34,31,"#DDEBF4",BLUE,4); rect(8,42,34,62,"#F4E3CF",ORANGE,4); circle(63,35,13,"#E8DFF1",PURPLE)
        arrow(34,21,52,30,BLUE); arrow(34,52,52,40,ORANGE); rect(80,23,96,47,"#E6F1E3",GREEN,5); arrow(76,35,80,35,GREEN)
    elif kind == "tool":
        rect(8,10,92,61,"#F4E8D8",ORANGE,7); rect(17,18,65,52,"#FFFFFF",INK,3)
        line(25,28,34,35,BLUE,2); line(34,35,25,42,BLUE,2); line(40,43,56,43,BLUE,2)
        circle(79,34,8,"#E6F1E3",GREEN); line(79,25,79,43,GREEN,3); line(70,34,88,34,GREEN,3)
    elif kind == "planner":
        circle(50,14,7,"#F0BE79",ORANGE); line(50,21,50,31,PURPLE,2)
        for xx in (18,50,82): rect(xx-11,34,xx+11,56,"#EEE7F4",PURPLE,4)
        arrow(50,30,18,34,PURPLE); arrow(50,30,50,34,PURPLE); arrow(50,30,82,34,PURPLE)
        for xx in (18,50,82): line(xx-5,45,xx-1,49,GREEN,2); line(xx-1,49,xx+6,40,GREEN,2)
    elif kind == "agent":
        circle(40,22,10,"#E4D8EE",PURPLE); rect(25,34,55,61,"#EEE8F4",PURPLE,10); rect(61,18,94,48,"#FFFFFF",BLUE,5)
        line(67,28,87,28,"#9BACB7"); line(67,37,83,37,"#9BACB7"); arrow(56,40,61,34,BLUE)
    elif kind == "multi-agent":
        pts=[(18,19),(50,9),(82,19),(31,53),(69,53)]
        for a,b in ((0,1),(1,2),(0,3),(1,3),(1,4),(2,4),(3,4)): line(*pts[a],*pts[b],PURPLE,2)
        for i,(xx,yy) in enumerate(pts): circle(xx,yy,6,["#9ECBE2","#EDBB78","#9DCAA3","#C5B0DA","#E99F9B"][i])
        for xx in (31,69): rect(xx-9,60,xx+9,68,"#FFFFFF",PURPLE,2)
    elif kind == "memory":
        for i in range(3): rect(18+i*8,9+i*6,68+i*8,43+i*6,["#F0E8F5","#E4D9ED","#D7C7E5"][i],PURPLE,5)
        arrow(8,24,18,24,BLUE); arrow(91,47,82,47,GREEN); draw.text((px(7),py(9)),"R",fill=BLUE); draw.text((px(88),py(51)),"W",fill=GREEN)
    elif kind == "message-bus":
        rect(8,29,92,43,"#FFFFFF",PURPLE,5)
        for xx,color in ((18,BLUE),(39,ORANGE),(60,GREEN),(81,RED)): rect(xx-5,31,xx+5,41,color,INK,2,1)
        for xx in (18,50,82): circle(xx,12,6,"#E8E0F1",PURPLE); arrow(xx,18,xx,29,PURPLE)
        for xx in (34,66): circle(xx,60,6,"#DDEBF4",BLUE); arrow(xx,43,xx,54,BLUE)
    elif kind == "verifier":
        draw.polygon([(px(50),py(5)),(px(77),py(15)),(px(72),py(48)),(px(50),py(64)),(px(28),py(48)),(px(23),py(15))],fill="#E7F1E4",outline=GREEN)
        line(36,33,46,43,GREEN,4); line(46,43,65,22,GREEN,4); arrow(79,51,91,51,RED); arrow(91,51,91,17,RED)
    elif kind == "environment":
        circle(50,35,16,"#E3F0E3",GREEN); circle(50,35,5,"#9CC9A2",GREEN)
        for a,b,c,d in ((50,5,79,17),(86,24,83,50),(73,61,34,63),(20,54,13,28),(20,16,42,7)): arrow(a,b,c,d,BLUE)
    elif kind == "sandbox":
        rect(12,7,88,64,"#F3E5D2",ORANGE,8); rect(21,18,78,56,"#FFFFFF",INK,4); rect(68,6,90,29,"#E7F1E4",GREEN,5)
        draw.arc((px(73),py(0),px(85),py(17)),180,360,fill=GREEN,width=sw*2); line(30,30,39,36,BLUE,2); line(39,36,30,43,BLUE,2); line(46,44,64,44,BLUE,2)
    elif kind == "vit":
        rect(5,10,33,48,"#E5F0E3",GREEN,2)
        for i in range(1,3): line(5+i*9.3,10,5+i*9.3,48,"#FFFFFF"); line(5,10+i*12.7,33,10+i*12.7,"#FFFFFF")
        for i in range(5): rect(41+i*8,18+(i%2)*7,47+i*8,49,["#7FB8D6","#9BC69E","#E5B16E"][i%3],INK,1,1)
        rect(82,12,97,56,"#D8E8F2",BLUE,4); arrow(34,30,41,30,BLUE); arrow(78,35,82,35,PURPLE)
    elif kind == "patches":
        rect(9,9,48,61,"#E4F0E2",GREEN,3)
        for i in range(1,4): line(9+i*9.75,9,9+i*9.75,61,"#FFFFFF"); line(9,9+i*13,48,9+i*13,"#FFFFFF")
        for i in range(6): rect(62+i*5,17+(i%2)*8,66+i*5,54,["#78B7D8","#91C49A","#E6B16D"][i%3],INK,1,1)
        arrow(49,35,60,35,BLUE)
    elif kind == "fpn":
        for i,(a,b,c,d) in enumerate(((9,8,75,56),(25,15,82,53),(43,23,90,50))): rect(a,b,c,d,["#C9E1D2","#B6D7C1","#9BC8AB"][i],GREEN,3)
        arrow(17,63,82,63,GREEN); for_x=[21,45,70]
        for xx in for_x: line(xx,59,xx,67,GREEN,2)
    elif kind == "detection":
        rect(8,8,67,62,"#E7F1E5",GREEN,3); draw.rectangle((px(18),py(20),px(38),py(43)),outline=RED,width=sw*2); draw.rectangle((px(42),py(27),px(60),py(52)),outline=ORANGE,width=sw*2)
        rect(76,12,95,29,"#DCEAF3",BLUE,3); rect(76,41,95,58,"#F2E3D0",ORANGE,3); arrow(67,29,76,21,BLUE); arrow(67,41,76,49,ORANGE)
    elif kind == "segmentation":
        rect(7,7,70,63,"#E7F1E5",GREEN,3)
        draw.polygon([(px(8),py(48)),(px(23),py(26)),(px(40),py(38)),(px(54),py(18)),(px(70),py(29)),(px(70),py(63)),(px(8),py(63))],fill="#8FC89A")
        rect(78,17,96,53,"#DCEAF3",BLUE,4)
        for yy in (25,35,45): line(82,yy,92,yy,BLUE)
    elif kind == "vlm":
        rect(5,14,31,56,"#DDEBF4",BLUE,3); rect(69,14,95,56,"#F3E5D2",ORANGE,3); circle(50,35,11,"#E5DAED",PURPLE)
        arrow(31,35,39,35,BLUE); arrow(69,35,61,35,ORANGE)
        for i in range(3): rect(43+i*6,58,47+i*6,66,[BLUE,GREEN,ORANGE][i],INK,1,1)
    elif kind == "diffusion":
        for i in range(4):
            rect(3+i*25,17,22+i*25,53,["#C9C9C9","#CEDAE4","#B5D8C1","#8EC89B"][i],GREEN,2)
            if i<3: arrow(22+i*25,35,28+i*25,35,PURPLE)
        for xx,yy in ((8,24),(14,42),(33,28),(40,45)): circle(xx,yy,1.5,"#666666","#666666",1)
    elif kind == "tracking":
        for i in range(3): rect(3+i*33,12,30+i*33,58,"#E7F0F5",BLUE,2)
        positions=[(14,28),(47,34),(80,40)]
        for xx,yy in positions: draw.rectangle((px(xx-5),py(yy-8),px(xx+5),py(yy+8)),outline=RED,width=sw*2)
        line(14,28,47,34,RED,2); line(47,34,80,40,RED,2)
    elif kind == "3d":
        rect(4,42,19,58,"#F3E4D0",ORANGE,2); circle(12,50,3,"#FFFFFF",ORANGE)
        points=[(45,14),(61,20),(74,34),(65,51),(46,55),(35,36)]
        for a,b in ((0,1),(1,2),(2,3),(3,4),(4,5),(5,0),(0,3),(1,4)): line(*points[a],*points[b],BLUE,1)
        for xx,yy in points: circle(xx,yy,3,"#9BC6DE",BLUE,1)
        line(19,47,45,14,ORANGE,1); line(19,47,65,51,ORANGE,1); rect(82,20,98,51,"#E5F0E3",GREEN,2)
    elif kind == "gateway":
        for yy in (12,35,58): arrow(2,yy,25,yy,ORANGE)
        draw.polygon([(px(25),py(6)),(px(50),py(18)),(px(50),py(52)),(px(25),py(64))],fill="#F1DFC5",outline=ORANGE)
        for yy in (12,35,58): arrow(50,35,77,yy,BLUE); rect(77,yy-7,97,yy+7,"#E5EEF4",BLUE,3)
    elif kind == "scheduler":
        for i in range(4): rect(2+i*11,12,10+i*11,25,["#F2E2CB","#DCEAF3","#E5F0E2"][i%3],INK,1,1)
        circle(57,35,15,"#FFFFFF",ORANGE); line(57,35,57,24,ORANGE,2); line(57,35,67,40,ORANGE,2); arrow(73,35,82,35,BLUE)
        for yy in (13,31,49): rect(82,yy,98,yy+12,"#DCEAF3",BLUE,2)
    elif kind == "gpu-worker":
        for i in range(3):
            rect(5+i*32,15,31+i*32,55,["#D8E9F3","#E4EDF3","#E8E0F1"][i],BLUE,3); circle(18+i*32,35,7,"#F0BD78",ORANGE)
            for yy in (20,50): line(8+i*32,yy,28+i*32,yy,INK,1)
        arrow(2,63,96,63,GREEN)
    elif kind == "service":
        rect(5,9,35,29,"#DDEBF4",BLUE,3); rect(65,9,95,29,"#E6F1E3",GREEN,3); rect(35,46,65,66,"#F3E4D0",ORANGE,3)
        arrow(35,19,65,19,BLUE); arrow(20,29,43,46,GREEN); arrow(80,29,57,46,ORANGE)
    elif kind == "event-stream":
        circle(8,18,6,"#E9E0F1",PURPLE); circle(8,52,6,"#E9E0F1",PURPLE); rect(20,26,80,44,"#F3E3CC",ORANGE,4)
        for xx,color in ((29,BLUE),(42,GREEN),(55,RED),(68,PURPLE)): circle(xx,35,3,color,INK,1)
        arrow(14,18,20,30,ORANGE); arrow(14,52,20,40,ORANGE); arrow(80,35,94,18,BLUE); arrow(80,35,94,52,BLUE)
    elif kind == "storage":
        for i in range(3): rect(4+i*15,8,17+i*15,28,["#F2E2CB","#DDEBF4","#E6F1E3"][i],ORANGE,2)
        draw.ellipse((px(50),py(25),px(94),py(38)),fill="#DDEAF3",outline=BLUE,width=sw); draw.rectangle((px(50),py(31),px(94),py(57)),fill="#DDEAF3",outline=BLUE,width=sw); draw.arc((px(50),py(50),px(94),py(63)),0,180,fill=BLUE,width=sw)
        arrow(43,18,59,28,GREEN)
    elif kind == "container":
        rect(3,4,97,66,"#F5EBDD",ORANGE,8)
        for i in range(3): rect(12+i*29,18,34+i*29,52,"#FFFFFF",ORANGE,3); line(17+i*29,28,29+i*29,28,BLUE,2); line(17+i*29,37,29+i*29,37,GREEN,2)
        arrow(12,59,86,59,PURPLE)
    elif kind == "monitor":
        rect(5,7,69,62,"#E8EFF4",BLUE,4); line(14,52,14,18,INK); line(14,52,61,52,INK)
        line(17,46,28,35,BLUE,2); line(28,35,39,42,BLUE,2); line(39,42,50,21,GREEN,2); line(50,21,62,29,GREEN,2)
        rect(76,10,96,24,"#F3E3CD",ORANGE,2); rect(76,29,96,43,"#E5F0E2",GREEN,2); rect(76,48,96,62,"#E8DFF1",PURPLE,2)
    else:
        rect(12,10,88,60,"#E8EFF4",BLUE,7); circle(50,35,11,"#FFFFFF",BLUE)
