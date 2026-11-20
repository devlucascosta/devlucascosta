"""Round-2 shape helpers (shapely) and explorations for the three new AgendAI proposals."""
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from shapely.geometry import Polygon, box, Point, LineString
from shapely.ops import unary_union
from shapely import affinity
from geo import poly_d, svg, fmt

K = "#0A0F14"
Q = 8  # arc resolution (segments per quarter circle)


def band(p0, p1, w):
    """Straight band of width w with flat (butt) ends along p0->p1."""
    return LineString([p0, p1]).buffer(w / 2, cap_style=2, join_style=2)


def arc_band(c, r, w, a0, a1, cap="flat", n=36):
    """Constant-width arc band centred on radius r, from angle a0 to a1 (degrees, SVG y-down)."""
    pts = [(c[0] + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
            c[1] + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
    return LineString(pts).buffer(w / 2, cap_style=1 if cap == "round" else 2, join_style=1, quad_segs=Q)


def legs(apex, base_y, half_w, w, apex_round=0):
    """Two straight legs meeting at apex; outer edges pass through (apex.x ± half_w, base_y)."""
    tri = Polygon([(apex[0] - half_w, base_y), apex, (apex[0] + half_w, base_y)])
    inner = tri.buffer(-w, join_style=2)
    ix = list(inner.exterior.coords)[:-1]
    top = min(ix, key=lambda p: p[1])
    bots = sorted([p for p in ix if p != top], key=lambda p: p[0])
    ext = [(top[0] + (b[0] - top[0]) * (400 - top[1]) / (b[1] - top[1]), 400) for b in bots]
    g = tri.difference(Polygon([top, ext[1], ext[0]]))
    if apex_round:
        g = g.buffer(-apex_round, join_style=1, quad_segs=Q).buffer(apex_round, join_style=1, quad_segs=Q)
        g = g.union(box(0, base_y - apex_round - 2, 256, base_y)).intersection(
            tri.difference(Polygon([top, ext[1], ext[0]])).buffer(0.01, join_style=2).union(box(0, 0, 0, 0)))
    return g, top


def centre(g, cy=128, optical=-2):
    minx, miny, maxx, maxy = g.bounds
    return affinity.translate(g, 128 - (minx + maxx) / 2, cy - (miny + maxy) / 2 + optical)


def save(path, g, title):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write(svg(256, 256, f'<path fill="{K}" fill-rule="evenodd" d="{poly_d(g)}"/>', title))


def letter_from_outline(outer_ext, w, base, cb=None, apex_round=0, inner_join=2, open_round=0, counter_round=0):
    """Constant-weight letter from an outer silhouette extended below the baseline.
    cb=(top,bottom) of crossbar; open_round rounds the top of the lower opening (arch)."""
    if apex_round:
        outer_ext = outer_ext.buffer(-apex_round, join_style=2).buffer(apex_round, join_style=1, quad_segs=Q)
    inner = outer_ext.buffer(-w, join_style=inner_join, quad_segs=Q)
    g = outer_ext
    if cb:
        counter = inner.intersection(box(-50, -50, 300, cb[0]))
        opening = inner.intersection(box(-50, cb[1], 300, 500))
        if counter_round:
            counter = counter.buffer(-counter_round, join_style=1, quad_segs=Q).buffer(counter_round, join_style=1, quad_segs=Q)
        if open_round:
            op2 = opening.buffer(-open_round, join_style=1, quad_segs=Q).buffer(open_round, join_style=1, quad_segs=Q)
            # keep the bottom square (rounding only matters at the top)
            opening = op2.union(opening.intersection(box(-50, cb[1] + open_round, 300, 500)))
        g = g.difference(counter).difference(opening)
    else:
        g = g.difference(inner)
    return g.intersection(box(-50, -50, 300, base))


def sym_outline(apex_y, base, half, ext=300):
    """Symmetric triangle with legs extended below base to y=ext."""
    k = half / (base - apex_y)
    return Polygon([(128 - half - (ext - base) * k, ext), (128, apex_y), (128 + half + (ext - base) * k, ext)])


def sail_outline(apex, foot_l, foot_r, bulge, ext=300, n=40):
    """Straight left side apex->foot_l, circular-arc right side apex->foot_r (bulging outward), extended to y=ext."""
    ax, ay = apex; fx, fy = foot_r
    mx, my = (ax + fx) / 2, (ay + fy) / 2
    dx, dy = fx - ax, fy - ay; L = math.hypot(dx, dy)
    nx, ny = dy / L, -dx / L
    R = (L * L / 4 + bulge * bulge) / (2 * bulge)
    cx, cy = mx - nx * (R - bulge), my - ny * (R - bulge)
    a0 = math.atan2(ay - cy, ax - cx); a1 = math.atan2(fy - cy, fx - cx)
    # continue the arc a little past the foot (below base)
    a1x = a1 + (a1 - a0) * 0.25
    arc = [(cx + R * math.cos(a0 + (a1x - a0) * i / n), cy + R * math.sin(a0 + (a1x - a0) * i / n)) for i in range(n + 1)]
    arc = [p for p in arc if p[1] <= ext]
    lx, ly = foot_l
    kx = (lx - ax) / (ly - ay)
    left_ext = (ax + (ext - ay) * kx, ext)
    return Polygon([(ax, ay)] + arc + [(arc[-1][0], ext), left_ext]), (cx, cy, R)
