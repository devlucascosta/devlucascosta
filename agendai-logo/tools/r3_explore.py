import os, sys, math
sys.path.insert(0, "tools")
from r3_shapes import *
O = "rodada-3/01-estudos/explora"
os.makedirs(O, exist_ok=True)
K = "#0A0F14"
def save(name, parts):
    # parts: list of (geom, fill)
    allg = unary_union([g for g, _ in parts])
    minx, miny, maxx, maxy = allg.bounds
    dx, dy = 128 - (minx + maxx) / 2, 128 - (miny + maxy) / 2 - 2
    body = "".join(f'<path fill="{f}" fill-rule="evenodd" d="{poly_d(place(g, dx, dy))}"/>' for g, f in parts)
    open(f"{O}/{name}.svg", "w").write(svg(256, 256, body, name))
CLIP = box(-50, -50, 300, B)

def legs(**kw):
    outer, inner, info = flat_A(**kw)
    return outer.difference(inner).intersection(CLIP), outer, inner, info

# ---------- R3-A Ponte: an arch springs from the left foot and lands behind the right leg
def ponte(p0, p1, p2, aw=24, gap=7, **kw):
    L, outer, inner, info = legs(**kw)
    pts, c, r = arc_pts(p0, p1, p2)
    arch = LineString(pts).buffer(aw / 2, cap_style=2, join_style=1).intersection(CLIP)
    leftleg = L.intersection(box(-50, -50, 128, 300)); rightleg = L.intersection(box(128, -50, 300, 300))
    leftleg = leftleg.difference(arch.buffer(gap, join_style=2))        # arch in front of the left leg
    arch = arch.difference(rightleg.buffer(gap, join_style=2))          # arch behind the right leg
    arch = arch.difference(rightleg)
    return [(unary_union([leftleg, rightleg]), K), (arch, K)]
save("a1-ponte", ponte((10, 226), (90, 168), (176, 150)))
save("a2-ponte-alta", ponte((14, 226), (96, 160), (180, 138)))
save("a3-ponte-baixa", ponte((24, 226), (100, 180), (170, 168), aw=22))

# ---------- R3-B Fita: soft tapered ribbon, in front of the left leg, behind the right, tip reappears
def fita(p0, p1, p2, w0=30, w1=8, gap=7, ease=0.9, **kw):
    L, outer, inner, info = legs(**kw)
    pts, c, r = arc_pts(p0, p1, p2, n=80)
    rib = tapered(pts, w0, w1, ease)
    leftleg = L.intersection(box(-50, -50, 128, 300)); rightleg = L.intersection(box(128, -50, 300, 300))
    leftleg = leftleg.difference(rib.buffer(gap, join_style=2))
    rib = rib.difference(rightleg.buffer(gap, join_style=2))
    return [(unary_union([leftleg, rightleg]), K), (rib.intersection(CLIP), K)]
save("b1-fita", fita((22, 214), (120, 150), (238, 116)))
save("b2-fita-suave", fita((26, 210), (124, 156), (232, 128), w0=28, w1=10))
save("b3-fita-curta", fita((40, 204), (124, 158), (214, 132), w0=30, w1=12))

# ---------- R3-C Recorte: a solid A; the curve is carved (negative space), not added
def recorte(p0, p1, p2, slit=12, cb_top=150, **kw):
    outer, inner, info = flat_A(**kw)
    solid = outer.intersection(CLIP)
    pts, c, r = arc_pts(p0, p1, p2, n=80)
    # region under the arc (inside the inner triangle) is the lower opening
    under = Polygon(pts + [(p2[0], 400), (p0[0], 400)]).buffer(0)
    opening = inner.intersection(under)
    counter = inner.intersection(box(-50, -50, 300, cb_top))
    cut = LineString(pts).buffer(slit / 2, cap_style=2)               # the carved curve runs through the left leg
    g = solid.difference(counter).difference(opening).difference(cut.intersection(box(-50, -50, info['ap'][0], 300)))
    return [(g, K)]
save("c1-recorte", recorte((0, 236), (90, 186), (190, 160)))
save("c2-recorte-alto", recorte((0, 232), (96, 178), (196, 150), cb_top=140))
save("c3-recorte-suave", recorte((-10, 240), (96, 190), (200, 166), slit=10, cb_top=148))
print("ok")
