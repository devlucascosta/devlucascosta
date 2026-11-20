import os, sys, math
sys.path.insert(0, "tools")
from r3_shapes import *
import r3_explore
from r3_explore import save, legs, CLIP, K
from r3_explore2 import drop_small
O = "rodada-3/01-estudos/explora3"; os.makedirs(O, exist_ok=True); r3_explore.O = O

# Impulso: a soft ribbon comes from behind the left leg, crosses IN FRONT of the right leg and leaves rising
def impulso(p0, p1, p2, w0=26, w1=10, gap=7, ease=1.0, **kw):
    L, outer, inner, info = legs(**kw)
    pts, c, r = arc_pts(p0, p1, p2, n=80)
    rib = tapered(pts, w0, w1, ease).intersection(CLIP)
    leftleg = L.intersection(box(-50, -50, 128, 300)); rightleg = L.intersection(box(128, -50, 300, 300))
    rib = rib.difference(leftleg.buffer(gap, join_style=2)).difference(leftleg)
    rib = drop_small(rib, 300)
    rightleg = rightleg.difference(rib.buffer(gap, join_style=2))
    return [(unary_union([leftleg, rightleg]), K), (rib, K)]
save("b4-impulso", impulso((60, 212), (140, 160), (236, 128)))
save("b5-impulso-suave", impulso((64, 210), (146, 166), (232, 140), w0=26, w1=12))
save("b6-impulso-baixo", impulso((70, 220), (150, 180), (238, 160), w0=24, w1=10))

# Recorte v3: the curve slices the left foot off at an angle (no spike) — the A lifts off on the left
def recorte(p0, p1, p2, cb_top=148, **kw):
    outer, inner, info = flat_A(**kw)
    solid = outer.intersection(CLIP)
    pts, c, r = arc_pts(p0, p1, p2, n=80)
    under = Polygon(pts + [(p2[0] + 80, 400), (p0[0] - 80, 400)]).buffer(0)
    opening = inner.intersection(under)
    counter = inner.intersection(box(-50, -50, 300, cb_top))
    leftcut = under.intersection(box(-50, -50, info['ap'][0], 300))
    g = drop_small(solid.difference(counter).difference(opening).difference(leftcut))
    return [(g, K)]
save("c7-recorte", recorte((20, 196), (96, 176), (196, 156)))
save("c8-recorte", recorte((26, 204), (100, 180), (198, 160)))
save("c9-recorte", recorte((14, 188), (96, 172), (196, 156), cb_top=144))
print("ok")
