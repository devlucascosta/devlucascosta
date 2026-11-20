"""Round 6 — Raiz refined, Raiz + Pena, Pena autoral."""
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from shapely.geometry import Polygon, box, LineString, MultiPoint
from shapely.ops import unary_union
from r4_shapes import raiz, drop_small, CLIP
from r3_shapes import B


def raiz_ref(flare=22, sag=12, t=28, tw=34, p_open=((72, 232), (118, 196), (198, 176)), wl=34, wr=46, nib_cut=0, half=106):
    """A: subtle refinement of Raiz (same silhouette). B: with nib_cut>0 and contrasted weights (Raiz + Pena)."""
    kw = dict(half=half, apex_y=30, tw=tw, wl=wl, wr=wr)
    g, _, info = raiz(flare=flare, sag=sag, t=t, p_open=p_open, kw=kw)
    if nib_cut:
        # broad-nib entry: the top-left corner is cut at 45°, as a pen held at 45° would leave it
        x0 = 128 - tw / 2
        cutter = Polygon([(x0 - 60, 30 + nib_cut + 60), (x0 + nib_cut + 60, 30 - 60), (-50, -50)]).buffer(0)
        cutter = Polygon([(x0 - 80, 30 + nib_cut + 80), (x0 + nib_cut, 30), (x0 + nib_cut + 80, 30 - 80), (-80, -80)])
        g = g.difference(cutter)
    return drop_small(g, 600), None, info


def pena2(nib=54, angle=-45, feet=(44, 212), apex=(128, 26), cb=(70, 178, 186, 156), lift=0, beak=0):
    """C: broad-nib A drawn in two pen strokes. lift = gap where the hairline stops short of the main stroke
    (the pen was lifted); beak = short entry flick at the apex."""
    a = math.radians(angle)
    nx, ny = math.cos(a) * nib / 2, math.sin(a) * nib / 2
    sweep = lambda p, q: MultiPoint([(p[0] + nx, p[1] + ny), (p[0] - nx, p[1] - ny), (q[0] + nx, q[1] + ny), (q[0] - nx, q[1] - ny)]).convex_hull
    lf, rf = (feet[0], B + 20), (feet[1], B + 20)
    right = sweep(apex, rf)
    if beak:
        right = right.union(sweep((apex[0] - beak, apex[1] + beak * 0.65), apex))
    top = apex
    if lift:
        t = lift / math.hypot(apex[0] - lf[0], apex[1] - lf[1])
        top = (apex[0] - (apex[0] - lf[0]) * t * 3.2, apex[1] + (lf[1] - apex[1]) * t * 3.2)
    left = sweep(lf, top)
    if lift:
        left = left.difference(right.buffer(lift, join_style=2))
        if left.geom_type == "MultiPolygon":                   # keep the hairline, drop slivers
            left = max(left.geoms, key=lambda p: p.area)
    legs = unary_union([left, right])
    bar = sweep((cb[0], cb[1]), (cb[2], cb[3])).intersection(unary_union([sweep(lf, apex), right]).convex_hull)
    g = unary_union([legs, bar]).intersection(CLIP)
    return drop_small(g, 300), None, dict()
