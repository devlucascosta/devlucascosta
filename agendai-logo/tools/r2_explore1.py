import os, sys, math
sys.path.insert(0, "tools")
from r2_shapes import *
O = "rodada-2/01-estudos/explora"

# ---- P01: A + curved stroke ----
def p01(arc_c, arc_r, a0, a1, w=30, aw=26, half=92, apex=(128, 30), base=226, rnd=False):
    L, top = legs(apex, base, half, w)
    A = arc_band(arc_c, arc_r, aw, a0, a1, cap="round" if rnd else "flat")
    return centre(unary_union([L, A]))
save(f"{O}/p01-a.svg", p01((128, 330), 168, 236, 304), "p01a arco convexo")
save(f"{O}/p01-b.svg", p01((40, 300), 160, 270, 330, rnd=True), "p01b arco sobe à direita")
save(f"{O}/p01-c.svg", p01((300, 120), 170, 150, 205), "p01c arco côncavo lateral")
save(f"{O}/p01-d.svg", p01((128, 60), 120, 25, 155), "p01d arco tigela")

# ---- P02: continuous A, curved bottom opening ----
def p02(r_apex=44, half=100, w=36, arch_r=34, cb=40, base=226, apex_y=26):
    tri = Polygon([(128 - half, base), (128, apex_y), (128 + half, base)])
    solid = tri.buffer(-r_apex, join_style=2).buffer(r_apex, join_style=1, quad_segs=Q).intersection(box(0, 0, 256, base))
    inner = tri.buffer(-w, join_style=2)
    iy = inner.bounds
    # counter: inner triangle above crossbar
    counter = inner.intersection(box(0, 0, 256, base - arch_r - cb - 10)).buffer(-6, join_style=1, quad_segs=Q).buffer(6, join_style=1, quad_segs=Q)
    # arch opening: rectangle + semicircle top
    arch = unary_union([Point(128, base - arch_r * 1.0).buffer(arch_r, quad_segs=Q), box(128 - arch_r, base - arch_r, 128 + arch_r, base + 5)])
    return centre(solid.difference(counter).difference(arch))
save(f"{O}/p02-a.svg", p02(), "p02a")
save(f"{O}/p02-b.svg", p02(r_apex=70, half=104, arch_r=44, cb=34), "p02b")
save(f"{O}/p02-c.svg", p02(r_apex=24, half=96, w=34, arch_r=30, cb=44), "p02c")

# ---- P03: sail A — straight left leg, curved right side ----
def p03(w=32, base=226, apex=(104, 28), foot_r=(214, 226), bulge=36, cb=150, cbw=26):
    # right side: circular arc through apex and right foot, bulging outward
    ax, ay = apex; fx, fy = foot_r
    mx, my = (ax + fx) / 2, (ay + fy) / 2
    dx, dy = fx - ax, fy - ay; L = math.hypot(dx, dy)
    nx, ny = dy / L, -dx / L                        # outward normal (to the right/up)
    # sagitta s=bulge -> radius
    R = (L * L / 4 + bulge * bulge) / (2 * bulge)
    cx, cy = mx - nx * (R - bulge), my - ny * (R - bulge)
    a0 = math.degrees(math.atan2(ay - cy, ax - cx)); a1 = math.degrees(math.atan2(fy - cy, fx - cx))
    right = arc_band((cx, cy), R - w / 2, w, a0, a1)
    left = band((ax - 6, ay - 4), (40, base + 30), w).intersection(box(0, 0, 256, base))
    right = right.intersection(box(0, 0, 256, base))
    # crossbar
    bar = box(40, cb - cbw / 2, 220, cb + cbw / 2)
    outline = unary_union([left, right]).convex_hull
    bar = bar.intersection(outline)
    g = unary_union([left, right, bar])
    g = g.union(Point(ax, ay + 10).buffer(w / 2 + 1, quad_segs=Q))
    return centre(g)
save(f"{O}/p03-a.svg", p03(), "p03a")
save(f"{O}/p03-b.svg", p03(bulge=52, foot_r=(220, 226)), "p03b")
save(f"{O}/p03-c.svg", p03(apex=(118, 28), bulge=28, cb=156), "p03c")
print("ok")
