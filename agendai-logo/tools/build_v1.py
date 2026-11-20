"""First-round symbol explorations (black on white) for the three AgendAI concepts."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from shapely.geometry import Polygon, box
from shapely.ops import unary_union
from geo import poly_d, pill_d, svg, fmt

OUT = "02-conceitos/exploracoes"
os.makedirs(OUT, exist_ok=True)
K = "#0A0F14"


def save(name, d, evenodd=True):
    rule = ' fill-rule="evenodd"' if evenodd else ""
    open(f"{OUT}/{name}.svg", "w").write(svg(256, 256, f'<path fill="{K}"{rule} d="{d}"/>', f"AgendAI {name}"))


# ---------- A: Ligadura "AI" -------------------------------------------------
def ligadura(apex_y=32, stem_top=32, stem_x=168, stem_w=40, base_x=40, t=40, cb=(156, 188), slit=0):
    # outer diagonal from (base_x,224) to (stem_x, apex_y)
    k = (stem_x - base_x) / (224 - apex_y)          # dx per dy
    import math
    sin = (224 - apex_y) / math.hypot(stem_x - base_x, 224 - apex_y)
    h = t / sin                                     # horizontal leg thickness
    xi = lambda y: base_x + (224 - y) * k + h        # inner edge x at y
    y_ap = 224 - (stem_x - slit - base_x - h) / k    # where inner edge meets stem (or slit)
    body = Polygon([(base_x, 224), (stem_x, apex_y), (stem_x, stem_top), (stem_x + stem_w, stem_top),
                    (stem_x + stem_w, 224)])
    right = stem_x - slit
    counter = Polygon([(xi(y_ap), y_ap), (right, y_ap), (right, cb[0]), (xi(cb[0]), cb[0])])
    gap = Polygon([(xi(cb[1]), cb[1]), (right, cb[1]), (right, 225), (xi(225), 225)])
    g = body.difference(counter).difference(gap)
    if slit:
        g = g.difference(box(stem_x - slit, y_ap, stem_x, 225))
    return g


save("a1-ligadura-fundida", poly_d(ligadura()))
save("a2-ligadura-fenda", poly_d(ligadura(slit=10)))
save("a3-ligadura-haste-alta", poly_d(ligadura(apex_y=76, base_x=56)))


# ---------- B: Anel (ring-bound A) ------------------------------------------
def anel(leg=32, ring=(12, 104, 244, 184), rw=26, gap=7):
    import math
    apex = (128, 28)
    bl, br = (36, 224), (220, 224)
    tri = Polygon([bl, apex, br])
    inner = tri.buffer(-leg, join_style=2)
    ix = list(inner.exterior.coords)[:-1]
    top = min(ix, key=lambda p: p[1])
    bots = sorted([p for p in ix if p != top], key=lambda p: p[0])
    ext = []
    for b in bots:
        f = (300 - top[1]) / (b[1] - top[1])
        ext.append((top[0] + (b[0] - top[0]) * f, 300))
    lam = tri.difference(Polygon([top, ext[1], ext[0]]))
    lam = lam.difference(box(0, 224, 256, 400))
    split = 128
    legL = lam.intersection(box(0, 0, split, 256))
    legR = lam.intersection(box(split, 0, 256, 256))
    x0, y0, x1, y1 = ring
    R = (y1 - y0) / 2
    barT = box(x0 + R, y0, x1 - R, y0 + rw)
    barB = box(x0 + R, y1 - rw, x1 - R, y1)
    # over/under: left leg over top bar, bottom bar over left leg; right leg mirrored
    barT = barT.difference(legL.buffer(gap, join_style=2))
    legL = legL.difference(barB.buffer(gap, join_style=2))
    legR = legR.difference(barT.intersection(box(split, 0, 256, 256)).buffer(gap, join_style=2))
    barB = barB.difference(legR.buffer(gap, join_style=2))
    ri = R - rw
    cy = (y0 + y1) / 2
    capL = (f"M{fmt(x0+R+0.5)} {fmt(y0)} H{fmt(x0+R)} A{fmt(R)} {fmt(R)} 0 0 0 {fmt(x0+R)} {fmt(y1)} H{fmt(x0+R+0.5)} "
            f"V{fmt(cy+ri)} H{fmt(x0+R)} A{fmt(ri)} {fmt(ri)} 0 0 1 {fmt(x0+R)} {fmt(cy-ri)} H{fmt(x0+R+0.5)} Z")
    capR = (f"M{fmt(x1-R-0.5)} {fmt(y0)} H{fmt(x1-R)} A{fmt(R)} {fmt(R)} 0 0 1 {fmt(x1-R)} {fmt(y1)} H{fmt(x1-R-0.5)} "
            f"V{fmt(cy+ri)} H{fmt(x1-R)} A{fmt(ri)} {fmt(ri)} 0 0 0 {fmt(x1-R)} {fmt(cy-ri)} H{fmt(x1-R-0.5)} Z")
    d = " ".join([poly_d(unary_union([legL, legR])), poly_d(barT), poly_d(barB), capL, capR])
    return d


save("b1-anel", anel(), evenodd=False)
save("b2-anel-fino", anel(leg=28, rw=22, ring=(16, 112, 240, 184)), evenodd=False)


# ---------- C: Blocos (agenda rows forming an A) ----------------------------
def blocos(rows):
    return " ".join(pill_d(*r) for r in rows)


H, G = 36, 12
ys = [38 + i * (H + G) for i in range(4)]
c1 = [(96, ys[0], 160, ys[0] + H),
      (72, ys[1], 112, ys[1] + H), (144, ys[1], 184, ys[1] + H),
      (48, ys[2], 208, ys[2] + H),
      (24, ys[3], 76, ys[3] + H), (180, ys[3], 232, ys[3] + H)]
save("c1-blocos-simetrico", blocos(c1), evenodd=False)
# Gantt flavour: 3 rows, legs as one long block each, apex block offset
H3, G3 = 48, 16
y3 = [128 - (3 * H3 + 2 * G3) / 2 + i * (H3 + G3) for i in range(3)]
c2 = [(80, y3[0], 176, y3[0] + H3),
      (40, y3[1], 216, y3[1] + H3),
      (16, y3[2], 96, y3[2] + H3), (160, y3[2], 240, y3[2] + H3)]
save("c2-blocos-3-linhas", blocos(c2), evenodd=False)
print("ok")
