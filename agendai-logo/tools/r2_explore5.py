import os, sys, math
sys.path.insert(0, "tools")
from r2_shapes import *
from r2_explore3 import legsA
O = "rodada-2/01-estudos/explora5"
B = 226
def circ(p1, p2, p3):
    ax, ay = p1; bx, by = p2; cx, cy = p3
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax**2 + ay**2) * (by - cy) + (bx**2 + by**2) * (cy - ay) + (cx**2 + cy**2) * (ay - by)) / d
    uy = ((ax**2 + ay**2) * (cx - bx) + (bx**2 + by**2) * (ax - cx) + (cx**2 + cy**2) * (bx - ax)) / d
    return (ux, uy), math.hypot(ax - ux, ay - uy)
def ang(c, p): return math.degrees(math.atan2(p[1] - c[1], p[0] - c[0]))
def p01(p0, p1, p2, aw=24, cap="flat", w=30):
    g, out = legsA(w=w)
    c, r = circ(p0, p1, p2)
    a = arc_band(c, r, aw, ang(c, p0), ang(c, p2), cap=cap)
    return centre(unary_union([g, a]).intersection(box(-50, -50, 300, B)))
save(f"{O}/p01-r.svg", p01((66, 204), (170, 150), (238, 136)), "r")
save(f"{O}/p01-s.svg", p01((66, 204), (170, 150), (238, 136), cap="round"), "s")
save(f"{O}/p01-t.svg", p01((70, 196), (160, 160), (226, 150), aw=26), "t")
save(f"{O}/p01-u.svg", p01((60, 214), (150, 160), (236, 128), aw=24, cap="round"), "u")
