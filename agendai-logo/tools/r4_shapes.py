"""Round 4 geometry: refined Ponte, refined Recorte and the Ponte+Recorte hybrid ("Laço")."""
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from shapely.geometry import Polygon, box, LineString, Point, MultiPolygon
from shapely.ops import unary_union
from r3_shapes import flat_A, arc_pts, B

CLIP = box(-50, -50, 300, B)
KW = dict(half=106, apex_y=30, tw=36, wl=34, wr=46)


def drop_small(g, min_area=300):
    if isinstance(g, MultiPolygon):
        return unary_union([p for p in g.geoms if p.area >= min_area])
    return g


def legs(kw=KW):
    outer, inner, info = flat_A(**kw)
    return outer.difference(inner).intersection(CLIP), outer, inner, info


# ---------------------------------------------------------------- A. Ponte refinada
def ponte(p0=(34, 246), p1=(104, 178), p2=(186, 158), aw=28, gap=6, kw=KW):
    L, outer, inner, info = legs(kw)
    pts, c, r = arc_pts(p0, p1, p2, n=64)
    arch = LineString(pts).buffer(aw / 2, cap_style=2, join_style=1).intersection(CLIP)
    ll = L.intersection(box(-50, -50, 128, 300)); rl = L.intersection(box(128, -50, 300, 300))
    under = Polygon(pts + [(p2[0], 400), (p0[0] - 60, 400)]).buffer(0)
    ll = drop_small(ll.difference(arch.buffer(gap, join_style=2)).difference(under), 600)
    arch = drop_small(arch.difference(rl.buffer(gap, join_style=2)), 300)
    return unary_union([ll, rl]), arch, dict(c=c, r=r)


# ---------------------------------------------------------------- B. Recorte refinado
def recorte(p0=(26, 204), p1=(100, 180), p2=(198, 160), t=None, flat_cb=148, kw=KW):
    """t=None: flat counter bottom (rodada 3). t=number: the counter's bottom follows the same arc, offset by t."""
    outer, inner, info = flat_A(**kw)
    solid = outer.intersection(CLIP)
    pts, c, r = arc_pts(p0, p1, p2, n=80)
    under = Polygon(pts + [(p2[0] + 80, 400), (p0[0] - 80, 400)]).buffer(0)
    opening = inner.intersection(under)
    if t is None:
        counter = inner.intersection(box(-50, -50, 300, flat_cb))
    else:
        counter = inner.difference(under.buffer(t, quad_segs=16))
    leftcut = under.intersection(box(-50, -50, info["ap"][0], 300))
    g = drop_small(solid.difference(counter).difference(opening).difference(leftcut), 600)
    return g, None, dict(c=c, r=r)


# ---------------------------------------------------------------- C. Híbrido "Laço"
def _fillet(A, C, Bp, R, n=24):
    """Polyline A -> (rounded corner at C with radius R) -> Bp."""
    def unit(p, q):
        d = math.hypot(q[0] - p[0], q[1] - p[1]); return ((q[0] - p[0]) / d, (q[1] - p[1]) / d)
    u1 = unit(C, A); u2 = unit(C, Bp)
    ang = math.acos(max(-1, min(1, u1[0] * u2[0] + u1[1] * u2[1])))      # interior angle at C
    tlen = R / math.tan(ang / 2)
    T1 = (C[0] + u1[0] * tlen, C[1] + u1[1] * tlen); T2 = (C[0] + u2[0] * tlen, C[1] + u2[1] * tlen)
    bis = (u1[0] + u2[0], u1[1] + u2[1]); bl = math.hypot(*bis); bis = (bis[0] / bl, bis[1] / bl)
    dc = R / math.sin(ang / 2)
    O = (C[0] + bis[0] * dc, C[1] + bis[1] * dc)
    a1 = math.atan2(T1[1] - O[1], T1[0] - O[0]); a2 = math.atan2(T2[1] - O[1], T2[0] - O[0])
    d = a2 - a1
    while d > math.pi: d -= 2 * math.pi
    while d < -math.pi: d += 2 * math.pi
    arc = [(O[0] + R * math.cos(a1 + d * i / n), O[1] + R * math.sin(a1 + d * i / n)) for i in range(n + 1)]
    return [A] + arc + [Bp]


def laco(corner_y=214, end_y=176, R=30, w=None, kw=KW):
    """One stroke: the left leg runs down and turns, without lifting the pen, into the crossbar,
    which flows into the right leg. The heel replaces the left foot (Ponte's integration, Recorte's single mass)."""
    L, outer, inner, info = legs(kw)
    wl = kw["wl"]; w = w or wl
    lb, lt = info["lb"], info["lt"]
    # left-leg centre line (offset inward by wl/2 from the outer edge)
    dx, dy = lt[0] - lb[0], lt[1] - lb[1]; Ln = math.hypot(dx, dy)
    nx, ny = -dy / Ln, dx / Ln
    if nx < 0: nx, ny = -nx, -ny
    k = dx / dy
    cx0 = lambda y: lb[0] + (y - lb[1]) * k + nx * wl / 2 / abs(nx) * abs(nx) * (1 / math.sqrt(1)) * 0 + (wl / 2) / math.cos(math.atan(abs(k)))
    A = (cx0(kw["apex_y"] - 10), kw["apex_y"] - 10)
    C = (cx0(corner_y), corner_y)
    # right-leg centre line at end_y
    rb, rt = info["rb"], info["rt"]; kr = (rt[0] - rb[0]) / (rt[1] - rb[1])
    xr = rb[0] + (end_y - rb[1]) * kr - (kw["wr"] / 2) / math.cos(math.atan(abs(kr)))
    Bp = (xr, end_y)
    path = _fillet(A, C, Bp, R)
    stroke = LineString(path).buffer(w / 2, cap_style=2, join_style=1, quad_segs=16)
    rl = L.intersection(box(128, -50, 300, 300))
    top = outer.intersection(box(-50, -50, 300, kw["apex_y"] + 60)).difference(inner)
    g = unary_union([stroke, rl, top]).intersection(outer.buffer(0.01)).intersection(CLIP)
    return drop_small(g, 600), None, dict(c=None, r=None, path=path)


# ---------------------------------------------------------------- C. Híbrido "Raiz"
def raiz(flare=26, sag=10, t=30, p_open=((70, 232), (114, 194), (196, 172)), kw=KW):
    """Solid A whose left contour is one concave arc flaring into the ground (the Ponte's curve becomes the
    letter's own edge); the lower opening is carved by a second arc (the Recorte's construction). One mass."""
    outer0, inner, info = flat_A(**kw)
    lt, lb, rt, rb = info["lt"], info["lb"], info["rt"], info["rb"]
    foot = (lb[0] - flare, B)
    mx, my = (lt[0] + foot[0]) / 2, (lt[1] + foot[1]) / 2
    dx, dy = foot[0] - lt[0], foot[1] - lt[1]; L = math.hypot(dx, dy)
    nx, ny = dy / L, -dx / L
    if nx < 0: nx, ny = -nx, -ny
    left, _, _ = arc_pts(lt, (mx + nx * sag, my + ny * sag), foot, n=48)
    kr = (rt[0] - rb[0]) / (rt[1] - rb[1])
    outer = Polygon(left + [(foot[0], B + 40), (rb[0] + 40 * kr, B + 40), rt]).buffer(0)
    pts, c, r = arc_pts(*p_open, n=64)
    under = Polygon(pts + [(p_open[2][0] + 80, 400), (p_open[0][0] - 120, 400)]).buffer(0)
    x0 = pts[0][0]
    reach = inner.union(Polygon([pts[0], (x0, 400), (inner.bounds[2], 400)]).buffer(0))
    cut = under.intersection(box(x0, -50, 300, 400)).intersection(reach)
    counter = inner.difference(under.buffer(t, quad_segs=16))
    g = drop_small(outer.intersection(CLIP).difference(counter).difference(cut), 600)
    return g, None, dict(c=c, r=r, left=left)
