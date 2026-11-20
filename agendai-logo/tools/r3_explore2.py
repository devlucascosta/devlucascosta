import os, sys, math
sys.path.insert(0, "tools")
from r3_shapes import *
from r3_explore import save, legs, CLIP, K
from shapely.geometry import MultiPolygon
O = "rodada-3/01-estudos/explora2"
os.makedirs(O, exist_ok=True)
import r3_explore; r3_explore.O = O

def drop_small(g, min_area=600):
    if isinstance(g, MultiPolygon):
        return unary_union([p for p in g.geoms if p.area >= min_area])
    return g

# Ponte v2: the left leg stands on the arch (fragment below removed); arch tucks behind the right leg
def ponte(p0, p1, p2, aw=24, gap=7, **kw):
    L, outer, inner, info = legs(**kw)
    pts, c, r = arc_pts(p0, p1, p2)
    arch = LineString(pts).buffer(aw / 2, cap_style=2, join_style=1).intersection(CLIP)
    leftleg = L.intersection(box(-50, -50, 128, 300)); rightleg = L.intersection(box(128, -50, 300, 300))
    under = Polygon(pts + [(p2[0], 400), (p0[0] - 40, 400)]).buffer(0)
    leftleg = drop_small(leftleg.difference(arch.buffer(gap, join_style=2)).difference(under))
    arch = arch.difference(rightleg.buffer(gap, join_style=2))
    return [(unary_union([leftleg, rightleg]), K), (arch, K)]
save("a4-ponte", ponte((14, 226), (92, 166), (178, 146)))
save("a5-ponte-assentada", ponte((20, 226), (96, 172), (182, 154), aw=26))
save("a6-ponte-sem-folga", ponte((20, 226), (96, 172), (182, 154), aw=26, gap=0))

# Recorte v2: the carved band sits BELOW the arc so the crossbar's lower edge is one continuous curve
def recorte(p0, p1, p2, slit=12, cb_top=150, **kw):
    outer, inner, info = flat_A(**kw)
    solid = outer.intersection(CLIP)
    pts, c, r = arc_pts(p0, p1, p2, n=80)
    under = Polygon(pts + [(p2[0] + 80, 400), (p0[0] - 80, 400)]).buffer(0)
    opening = inner.intersection(under)
    counter = inner.intersection(box(-50, -50, 300, cb_top))
    band = under.difference(LineString(pts).parallel_offset(0).buffer(0) if False else Polygon()).intersection(
        Polygon([(p[0], p[1]) for p in pts] + [(p[0] + 0, p[1] + slit) for p in pts[::-1]]).buffer(0))
    cut = band.intersection(box(-50, -50, info['ap'][0], 300))
    g = drop_small(solid.difference(counter).difference(opening).difference(cut))
    return [(g, K)]
save("c4-recorte", recorte((0, 222), (90, 182), (190, 160)))
save("c5-recorte-alto", recorte((0, 214), (96, 172), (196, 150), cb_top=138))
save("c6-recorte-fino", recorte((0, 218), (96, 176), (196, 154), slit=10, cb_top=142))

# Dobra: the left leg bends at the foot and becomes the arch (one stroke, no pen lift)
def dobra(turn_r=26, arch=((None), (100, 176), (180, 150)), aw=26, gap=7, **kw):
    L, outer, inner, info = legs(**kw)
    rightleg = L.intersection(box(128, -50, 300, 300))
    leftleg = L.intersection(box(-50, -50, 128, 300))
    # centre line of the left leg
    wl = kw.get("wl", 34)
    lb, lt = info["lb"], info["lt"]
    ang = math.atan2(lt[1] - lb[1], lt[0] - lb[0])
    nx, ny = math.sin(ang), -math.cos(ang)
    mid_b = (lb[0] - nx * wl / 2, lb[1] - ny * wl / 2)
    # arch from a point on the left leg's centre line (y=200) through p1 to p2
    y0 = 196
    t = (y0 - mid_b[1]) / math.sin(ang)
    p0 = (mid_b[0] + t * math.cos(ang), y0)
    pts, c, r = arc_pts(p0, arch[1], arch[2])
    a = LineString(pts).buffer(aw / 2, cap_style=2, join_style=1)
    # rounded heel joining leg and arch
    heel = Point(p0[0] + 4, p0[1] + 6).buffer(wl * 0.72)
    leftleg = leftleg.intersection(box(-50, -50, 300, y0))
    left = unary_union([leftleg, a, heel]).intersection(CLIP)
    left = left.difference(rightleg.buffer(gap, join_style=2))
    return [(unary_union([left, rightleg]), K)]
save("d1-dobra", dobra())
save("d2-dobra-baixa", dobra(arch=(None, (104, 190), (184, 166))))
print("ok")
