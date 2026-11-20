"""Small geometry helpers: shapely polygons -> clean SVG path data, pills, rings."""
import math
from shapely.geometry import Polygon, MultiPolygon, box
from shapely.ops import unary_union


def fmt(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def ring_d(coords):
    pts = list(coords)
    if pts[0] == pts[-1]:
        pts = pts[:-1]
    ded = []
    for q in pts:
        if not ded or abs(q[0] - ded[-1][0]) > 1e-6 or abs(q[1] - ded[-1][1]) > 1e-6:
            ded.append(q)
    if len(ded) > 1 and abs(ded[0][0] - ded[-1][0]) < 1e-6 and abs(ded[0][1] - ded[-1][1]) < 1e-6:
        ded.pop()
    pts = ded
    # drop collinear points
    out = []
    n = len(pts)
    for i in range(n):
        a, b, c = pts[i - 1], pts[i], pts[(i + 1) % n]
        cross = (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])
        if abs(cross) > 1e-6:
            out.append(b)
    return "M" + " L".join(f"{fmt(x)} {fmt(y)}" for x, y in out) + " Z"


def poly_d(geom):
    if geom.is_empty:
        return ""
    geoms = geom.geoms if isinstance(geom, MultiPolygon) else [geom]
    parts = []
    for g in geoms:
        parts.append(ring_d(g.exterior.coords))
        for h in g.interiors:
            parts.append(ring_d(h.coords))
    return " ".join(parts)


def pill_d(x0, y0, x1, y1):
    """Horizontal pill (stadium) with exact arcs."""
    r = (y1 - y0) / 2
    return (f"M{fmt(x0 + r)} {fmt(y0)} H{fmt(x1 - r)} A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x1 - r)} {fmt(y1)} "
            f"H{fmt(x0 + r)} A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x0 + r)} {fmt(y0)} Z")


def pill_poly(x0, y0, x1, y1, n=48):
    r = (y1 - y0) / 2
    cy = (y0 + y1) / 2
    pts = []
    for i in range(n + 1):
        a = -math.pi / 2 + math.pi * i / n
        pts.append((x1 - r + r * math.cos(a), cy + r * math.sin(a)))
    for i in range(n + 1):
        a = math.pi / 2 + math.pi * i / n
        pts.append((x0 + r + r * math.cos(a), cy + r * math.sin(a)))
    return Polygon(pts)


def svg(viewbox_w, viewbox_h, body, title="AgendAI"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fmt(viewbox_w)} {fmt(viewbox_h)}" '
            f'width="{fmt(viewbox_w)}" height="{fmt(viewbox_h)}" role="img" aria-labelledby="title">'
            f'<title id="title">{title}</title>{body}</svg>\n')
