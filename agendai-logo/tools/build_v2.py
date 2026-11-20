"""Round 2 explorations."""
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from shapely.geometry import Polygon, box, Point, LineString
from shapely.ops import unary_union
from geo import poly_d, pill_d, svg, fmt
from build_v1 import ligadura, save, K, OUT

# A4: full-height slit -> "A" overall, "A I" in detail
def ligadura_split(base_x=36, stem_x=164, stem_w=44, t=42, cb=(152, 186), slit=12, top=32):
    k = (stem_x - base_x) / (224 - top)
    sin = (224 - top) / math.hypot(stem_x - base_x, 224 - top)
    h = t / sin
    xo = lambda y: base_x + (224 - y) * k
    xi = lambda y: xo(y) + h
    right = stem_x - slit
    y_tip = 224 - (right - base_x) / k
    y_ap = 224 - (right - base_x - h) / k
    a = Polygon([(base_x, 224), (right, y_tip), (right, 224)])
    a = a.difference(Polygon([(xi(y_ap), y_ap), (right + 1, y_ap), (right + 1, cb[0]), (xi(cb[0]), cb[0])]))
    a = a.difference(Polygon([(xi(cb[1]), cb[1]), (right + 1, cb[1]), (right + 1, 225), (xi(225), 225)]))
    i = box(stem_x, top, stem_x + stem_w, 224)
    return unary_union([a, i])

save("a4-ligadura-separada", poly_d(ligadura_split()))
save("a5-ligadura-separada-larga", poly_d(ligadura_split(base_x=24, stem_x=172, t=44, slit=14)))

# B: Encaixe — rounded tile cut by an A-shaped channel into modules
def squircle(x0, y0, x1, y1, r, n=24):
    # continuous-ish corner tile approximated for boolean ops
    return box(x0 + r, y0 + r, x1 - r, y1 - r).buffer(r, quad_segs=n)

def encaixe(ch=20, apex=(128, 56), feet=(68, 188), cross=150, up=False, r=60):
    tile = squircle(16, 16, 240, 240, r)
    L = LineString([apex, (apex[0] - (240 - apex[1]) * (apex[0] - feet[0]) / (240 - apex[1]) - 40, 300)])
    # legs as lines from apex through feet extended past tile
    def leg(sign):
        fx = feet[0] if sign < 0 else 256 - feet[0]
        dx = fx - apex[0]; dy = 240 - apex[1]
        return LineString([apex, (apex[0] + dx * 1.6, apex[1] + dy * 1.6)])
    l1, l2 = leg(-1), leg(1)
    # crossbar between the two legs' centre lines at y=cross
    def xat(line, y):
        (x0, y0), (x1, y1) = line.coords
        return x0 + (y - y0) * (x1 - x0) / (y1 - y0)
    cb = LineString([(xat(l1, cross), cross), (xat(l2, cross), cross)])
    parts = [l1.buffer(ch / 2, cap_style=2, join_style=2), l2.buffer(ch / 2, cap_style=2, join_style=2),
             cb.buffer(ch / 2, cap_style=2)]
    # sharp apex: fill the notch at the apex join
    parts.append(Polygon([apex, (apex[0] - ch, apex[1] + 2 * ch), (apex[0] + ch, apex[1] + 2 * ch)]).intersection(
        unary_union(parts[:2]).convex_hull))
    if up:
        parts.append(LineString([(apex[0], apex[1]), (apex[0], 0)]).buffer(ch / 2, cap_style=2))
    cut = unary_union(parts)
    return tile.difference(cut)

save("b3-encaixe", poly_d(encaixe()))
save("b4-encaixe-aberto", poly_d(encaixe(up=True)))
save("b5-encaixe-largo", poly_d(encaixe(ch=24, apex=(128, 48), feet=(56, 0), cross=156)))

# C: Arco + ponto (arch with the "moment" dot)
def arco(r_out=96, t=40, cy=124, dot=24, doty=178):
    outer = Point(128, cy).buffer(r_out, quad_segs=64).union(box(128 - r_out, cy, 128 + r_out, 224))
    inner = Point(128, cy).buffer(r_out - t, quad_segs=64).union(box(128 - r_out + t, cy, 128 + r_out - t, 230))
    arch = outer.difference(inner).intersection(box(0, 0, 256, 224))
    d = poly_d(arch)
    d += f" M{fmt(128 - dot)} {fmt(doty)} A{dot} {dot} 0 1 0 {fmt(128 + dot)} {fmt(doty)} A{dot} {dot} 0 1 0 {fmt(128 - dot)} {fmt(doty)} Z"
    return d

save("c3-arco-ponto", arco(), evenodd=False)
print("ok")
