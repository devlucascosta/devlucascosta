"""Round 5 — three structurally new A constructions: Pena (broad nib), Ogiva (convex arcs), Disco (negative)."""
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from shapely.geometry import Polygon, box, LineString, Point, MultiPoint
from shapely.ops import unary_union
from r3_shapes import arc_pts, B
from r4_shapes import drop_small

CLIP = box(-50, -50, 300, B)


# 1. PENA — every stroke is the sweep of one broad nib held at a fixed angle (Minkowski sum of path × nib).
def pena(nib=52, angle=-45, feet=(44, 212), apex=(128, 26), cb=(78, 168, 178, 168), floor=18):
    a = math.radians(angle)
    nx, ny = math.cos(a) * nib / 2, math.sin(a) * nib / 2

    def sweep(p, q):
        return MultiPoint([(p[0] + nx, p[1] + ny), (p[0] - nx, p[1] - ny),
                           (q[0] + nx, q[1] + ny), (q[0] - nx, q[1] - ny)]).convex_hull

    lf, rf = (feet[0], B + 20), (feet[1], B + 20)
    left = sweep(lf, apex)
    right = sweep(apex, rf)
    legs = unary_union([left, right])
    bar = sweep((cb[0], cb[1]), (cb[2], cb[3])).intersection(legs.convex_hull)   # stroke stays inside the legs
    g = unary_union([legs, bar]).intersection(CLIP)
    return drop_small(g, 300), None, dict()


# 2. OGIVA — both sides are convex circular arcs meeting in a point; constant weight; straight crossbar.
def _side(p, q, bulge, n=48):
    mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    dx, dy = q[0] - p[0], q[1] - p[1]; L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    mid = (mx + nx * bulge, my + ny * bulge)
    return arc_pts(p, mid, q, n=n)[0]


def ogiva(bulge=22, w=34, half=100, apex_y=24, cb=(150, 176), apex_round=0):
    lf, rf, ap = (128 - half, B), (128 + half, B), (128, apex_y)
    left = _side(lf, ap, bulge)            # foot -> apex, bulging outward (to the left)
    right = _side(ap, rf, bulge)           # apex -> foot, bulging outward (to the right)
    outer = Polygon(left + right[1:] + [(rf[0], B + 60), (lf[0], B + 60)]).buffer(0)
    if apex_round:
        outer = outer.buffer(-apex_round, join_style=2).buffer(apex_round, join_style=1, quad_segs=16)
    inner = outer.buffer(-w, join_style=2, mitre_limit=10)
    counter = inner.intersection(box(-50, -50, 300, cb[0]))
    opening = inner.intersection(box(-50, cb[1], 300, 400))
    g = outer.difference(counter).difference(opening).intersection(CLIP)
    return drop_small(g, 300), None, dict()


# 3. DISCO — a solid disc; a triangular notch rises from the base and a bridge crosses it.
#    The A is never drawn: it is the shape the void leaves behind.
def disco(r=104, cy=124, notch_top=58, notch_half=56, bridge=(150, 176), flat=True):
    disc = Point(128, cy).buffer(r, quad_segs=32)
    base_y = cy + r
    if flat:                                    # sit the disc on a flat base, like the letters
        base_y = B
        disc = disc.intersection(box(-50, -50, 300, B))
    notch = Polygon([(128, notch_top), (128 + notch_half * 1.9, base_y + 40), (128 - notch_half * 1.9, base_y + 40)])
    g = disc.difference(notch.difference(box(-50, bridge[0], 300, bridge[1])))
    return drop_small(g, 300), None, dict()
