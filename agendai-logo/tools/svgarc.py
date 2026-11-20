"""Shapely polygon -> SVG path with TRUE circular arcs (A) and straight lines (L).

The geometry of every round is built from circular arcs and straight lines, but shapely stores it as polylines.
This module recovers the construction: each ring is split greedily into the longest runs that fit a straight
line or a single circular arc within `tol` units, and each run is written as one L or one A command.
"""
import math
from shapely.geometry import Polygon, MultiPolygon


def _fmt(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def _circle(a, b, c):
    ax, ay = a; bx, by = b; cx, cy = c
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if abs(d) < 1e-9:
        return None
    ux = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
    uy = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
    return (ux, uy), math.hypot(ax - ux, ay - uy)


def _line_ok(pts, tol):
    (x0, y0), (x1, y1) = pts[0], pts[-1]
    L = math.hypot(x1 - x0, y1 - y0)
    if L < 1e-9:
        return False
    for x, y in pts[1:-1]:
        if abs((x1 - x0) * (y0 - y) - (x0 - x) * (y1 - y0)) / L > tol:
            return False
        t = ((x - x0) * (x1 - x0) + (y - y0) * (y1 - y0)) / (L * L)
        if t < -1e-6 or t > 1 + 1e-6:
            return False
    return True


def _turn(pts):
    """Signed total turning along a polyline (radians)."""
    tot = 0
    for i in range(1, len(pts) - 1):
        a = math.atan2(pts[i][1] - pts[i - 1][1], pts[i][0] - pts[i - 1][0])
        b = math.atan2(pts[i + 1][1] - pts[i][1], pts[i + 1][0] - pts[i][0])
        d = b - a
        while d > math.pi: d -= 2 * math.pi
        while d < -math.pi: d += 2 * math.pi
        tot += d
    return tot


def _arc_ok(pts, tol, max_turn=math.radians(170)):
    if len(pts) < 3:
        return None
    # consistent turning direction and small per-vertex turns (a real curve, not a corner)
    turns = []
    for i in range(1, len(pts) - 1):
        a = math.atan2(pts[i][1] - pts[i - 1][1], pts[i][0] - pts[i - 1][0])
        b = math.atan2(pts[i + 1][1] - pts[i][1], pts[i + 1][0] - pts[i][0])
        d = b - a
        while d > math.pi: d -= 2 * math.pi
        while d < -math.pi: d += 2 * math.pi
        turns.append(d)
    if any(abs(t) > math.radians(25) for t in turns):
        return None
    if not (all(t >= -1e-4 for t in turns) or all(t <= 1e-4 for t in turns)):
        return None
    if abs(sum(turns)) > max_turn:
        return None
    c = _circle(pts[0], pts[len(pts) // 2], pts[-1])
    if not c:
        return None
    (cx, cy), r = c
    if r > 5000:
        return None
    for x, y in pts:
        if abs(math.hypot(x - cx, y - cy) - r) > tol:
            return None
    # chord midpoints must also sit on the arc (a long straight edge would fall inside it)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        sag = r - math.sqrt(max(r * r - (math.hypot(x1 - x0, y1 - y0) / 2) ** 2, 0))
        if abs(math.hypot(mx - cx, my - cy) - (r - sag)) > tol or sag > tol * 4:
            return None
    return r, sum(turns)


def _dedupe(pts):
    out = []
    for p in pts:
        if not out or math.hypot(p[0] - out[-1][0], p[1] - out[-1][1]) > 1e-6:
            out.append(p)
    if len(out) > 1 and math.hypot(out[0][0] - out[-1][0], out[0][1] - out[-1][1]) < 1e-6:
        out.pop()
    return out


def ring_path(coords, tol=0.12):
    pts = _dedupe(list(coords))
    n = len(pts)
    if n < 3:
        return ""
    # start at the sharpest corner so no arc is split by the seam
    def turn_at(i):
        a, b, c = pts[i - 1], pts[i], pts[(i + 1) % n]
        u = math.atan2(b[1] - a[1], b[0] - a[0]); v = math.atan2(c[1] - b[1], c[0] - b[0])
        d = abs(v - u)
        return min(d, 2 * math.pi - d)
    s = max(range(n), key=turn_at)
    pts = pts[s:] + pts[:s] + [pts[s]]
    out = [f"M{_fmt(pts[0][0])} {_fmt(pts[0][1])}"]
    i = 0
    N = len(pts) - 1
    while i < N:
        best = (i + 1, "L", None)
        j = i + 2
        while j <= N:
            seg = pts[i:j + 1]
            if _line_ok(seg, tol):
                best = (j, "L", None)
            else:
                a = _arc_ok(seg, tol)
                if a:
                    best = (j, "A", a)
                elif j - i > 3:
                    break
            j += 1
        j, kind, a = best
        x, y = pts[j]
        if kind == "L" or a is None:
            out.append(f"L{_fmt(x)} {_fmt(y)}")
        else:
            r, turn = a
            sweep = 1 if turn > 0 else 0          # SVG y-down: positive turning = clockwise on screen
            large = 1 if abs(turn) > math.pi else 0
            out.append(f"A{_fmt(r)} {_fmt(r)} 0 {large} {sweep} {_fmt(x)} {_fmt(y)}")
        i = j
    out[-1] = "Z" if out[-1].startswith("L") else out[-1] + " Z"
    return " ".join(out)


def geom_path(g, tol=0.12):
    geoms = g.geoms if isinstance(g, MultiPolygon) else [g]
    parts = []
    for p in geoms:
        parts.append(ring_path(p.exterior.coords, tol))
        for h in p.interiors:
            parts.append(ring_path(h.coords, tol))
    return " ".join(x for x in parts if x)
