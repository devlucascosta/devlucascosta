"""Round 3 geometry: flat-topped A with contrasted legs + integrated curves (bridge, ribbon, carved)."""
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from shapely.geometry import Polygon, box, LineString, Point
from shapely.ops import unary_union
from shapely import affinity
from geo import poly_d, svg, fmt

B = 226


def _off(p, q, d, inside):
    """Offset line p->q by distance d toward point `inside`. Returns (p', q')."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    if (inside[0] - p[0]) * nx + (inside[1] - p[1]) * ny < 0:
        nx, ny = -nx, -ny
    return (p[0] + nx * d, p[1] + ny * d), (q[0] + nx * d, q[1] + ny * d)


def _isect(a1, a2, b1, b2):
    x1, y1 = a1; x2, y2 = a2; x3, y3 = b1; x4, y4 = b2
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / den
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / den
    return px, py


def flat_A(half=106, apex_y=30, tw=36, wl=34, wr=46, cx=128, ext=320):
    """Outer silhouette (flat top) and inner (counter) triangle, both extended below the baseline."""
    lb, lt = (cx - half, B), (cx - tw / 2, apex_y)
    rb, rt = (cx + half, B), (cx + tw / 2, apex_y)
    k_l = (lt[0] - lb[0]) / (lt[1] - lb[1]); k_r = (rt[0] - rb[0]) / (rt[1] - rb[1])
    outer = Polygon([(lb[0] + (ext - B) * k_l, ext), lt, rt, (rb[0] + (ext - B) * k_r, ext)])
    inside = (cx, 170)
    l1, l2 = _off(lb, lt, wl, inside)
    r1, r2 = _off(rb, rt, wr, inside)
    ap = _isect(l1, l2, r1, r2)
    kl = (l2[0] - l1[0]) / (l2[1] - l1[1]); kr = (r2[0] - r1[0]) / (r2[1] - r1[1])
    inner = Polygon([ap, (ap[0] + (ext - ap[1]) * kr, ext), (ap[0] + (ext - ap[1]) * kl, ext)])
    return outer, inner, dict(ap=ap, kl=kl, kr=kr, lt=lt, rt=rt, lb=lb, rb=rb)


def circ3(p1, p2, p3):
    ax, ay = p1; bx, by = p2; cx, cy = p3
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax**2 + ay**2) * (by - cy) + (bx**2 + by**2) * (cy - ay) + (cx**2 + cy**2) * (ay - by)) / d
    uy = ((ax**2 + ay**2) * (cx - bx) + (bx**2 + by**2) * (ax - cx) + (cx**2 + cy**2) * (bx - ax)) / d
    return (ux, uy), math.hypot(ax - ux, ay - uy)


def arc_pts(p0, p1, p2, n=48):
    c, r = circ3(p0, p1, p2)
    a0 = math.atan2(p0[1] - c[1], p0[0] - c[0]); a2 = math.atan2(p2[1] - c[1], p2[0] - c[0])
    a1 = math.atan2(p1[1] - c[1], p1[0] - c[0])
    # choose the sweep direction that passes through p1
    def between(a, s, e):
        if s < e:
            return s <= a <= e
        return a >= s or a <= e
    if not between(a1 % (2 * math.pi), a0 % (2 * math.pi), a2 % (2 * math.pi)):
        a0, a2 = a0, a2 - 2 * math.pi if a2 > a0 else a2
    else:
        if a2 < a0:
            a2 += 2 * math.pi
    # pick the direction whose midpoint is nearest p1
    cand = []
    for e in (a2, a2 - 2 * math.pi, a2 + 2 * math.pi):
        m = (a0 + e) / 2
        cand.append((math.hypot(c[0] + r * math.cos(m) - p1[0], c[1] + r * math.sin(m) - p1[1]), e))
    a2 = min(cand)[1]
    return [(c[0] + r * math.cos(a0 + (a2 - a0) * i / n), c[1] + r * math.sin(a0 + (a2 - a0) * i / n)) for i in range(n + 1)], c, r


def tapered(pts, w0, w1, ease=1.0):
    """Polygon along a polyline with width easing from w0 to w1."""
    left, right = [], []
    n = len(pts) - 1
    for i, p in enumerate(pts):
        q = pts[min(i + 1, n)]; o = pts[max(i - 1, 0)]
        dx, dy = q[0] - o[0], q[1] - o[1]; L = math.hypot(dx, dy)
        nx, ny = -dy / L, dx / L
        t = (i / n) ** ease
        w = w0 + (w1 - w0) * t
        left.append((p[0] + nx * w / 2, p[1] + ny * w / 2)); right.append((p[0] - nx * w / 2, p[1] - ny * w / 2))
    return Polygon(left + right[::-1]).buffer(0)


def centre(g, optical=-2):
    minx, miny, maxx, maxy = g.bounds
    return affinity.translate(g, 128 - (minx + maxx) / 2, 128 - (miny + maxy) / 2 + optical)


def place(g, dx, dy):
    return affinity.translate(g, dx, dy)
