"""Round-1 concept artwork for AgendAI (black first). Writes symbol + horizontal lockup + construction drawing
for each of the three selected concepts into 02-conceitos/.

All letterforms are outlined paths (no <text>) — fonts: Sora, Montserrat, Manrope (SIL OFL 1.1, via @fontsource).
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from shapely.geometry import Polygon, box, Point, LineString
from shapely.ops import unary_union
from shapely import affinity
from geo import poly_d, svg, fmt
from glyphs import text_path, metrics

K = "#0A0F14"
ROOT = "02-conceitos"


def write(path, w, h, body, title):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write(svg(w, h, body, title))


def p(d, evenodd=True, fill=K):
    return f'<path fill="{fill}"{" fill-rule=\"evenodd\"" if evenodd else ""} d="{d}"/>'


# =====================================================================================
# A — LIGADURA "AI": an A whose right leg is a separate I. Whole = "A"; detail = "A I".
# Slope 3:2 (56.3°) on every diagonal, constant 38-unit weight, 14-unit slit.
# =====================================================================================
def ligadura(t=38, stem_w=38, slit=14, cb=(154, 186), top=32, tip_over=4, base=224):
    k = 2 / 3                                  # dx per dy (3:2 slope)
    H = base - (top - tip_over)
    right = 0                                  # build at origin, centre later
    base_x = right - H * k
    sin = 1 / math.hypot(k, 1)
    h = t / sin
    xi = lambda y: base_x + (base - y) * k + h
    y_ap = base - (right - base_x - h) / k
    a = Polygon([(base_x, base), (right, top - tip_over), (right, base)])
    a = a.difference(Polygon([(xi(y_ap), y_ap), (right + 1, y_ap), (right + 1, cb[0]), (xi(cb[0]), cb[0])]))
    a = a.difference(Polygon([(xi(cb[1]), cb[1]), (right + 1, cb[1]), (right + 1, base + 1), (xi(base + 1), base + 1)]))
    i = box(right + slit, top, right + slit + stem_w, base)
    g = unary_union([a, i])
    minx, _, maxx, _ = g.bounds
    return affinity.translate(g, 128 - (minx + maxx) / 2, 0), dict(y_ap=y_ap, cb=cb, h=h)


def concept_a():
    sym, info = ligadura()
    write(f"{ROOT}/A-ligadura/A-simbolo.svg", 256, 256, p(poly_d(sym)), "AgendAI — Ligadura AI")
    # Wordmark: "Agend" in Sora SemiBold + the ligature drawn at the same cap height (it IS the symbol)
    cap = 104
    base = 166
    d, w, boxes = text_path("Agend", "Sora", 600, cap, x=0, baseline=base, tracking=-0.012)
    s = cap / 192.0
    lig = affinity.scale(sym, s, s, origin=(0, 0))
    lx0, ly0, lx1, ly1 = lig.bounds
    gap = cap * 0.10
    last_right = boxes[-1][3]
    lig = affinity.translate(lig, last_right + gap - lx0, base - ly1)
    _, _, lx1, _ = lig.bounds
    pad = 24
    total = lx1 + pad * 2
    body = f'<g transform="translate({pad} 0)">{p(d, False)}{p(poly_d(lig))}</g>'
    write(f"{ROOT}/A-ligadura/A-logotipo-horizontal.svg", total, 256, body, "AgendAI — logotipo (Ligadura)")
    # small-size wordmark preview is the same file; construction drawing:
    cons = construction_a(sym, info)
    write(f"{ROOT}/A-ligadura/A-construcao.svg", 256, 256, cons, "Construção — Ligadura AI")


def construction_a(sym, info):
    minx, miny, maxx, maxy = sym.bounds
    lines = []
    for y in (32, info["cb"][0], info["cb"][1], 224):
        lines.append(f'<line x1="8" x2="248" y1="{fmt(y)}" y2="{fmt(y)}"/>')
    # 3:2 slope guide through the outer diagonal
    lines.append(f'<line x1="{fmt(minx - 12)}" y1="{fmt(224 + 18)}" x2="{fmt(minx + (224 - 14) * 2 / 3 + 12 * 2/3)}" y2="{fmt(14 - 0)}"/>')
    return (f'<rect width="256" height="256" fill="#fff"/>'
            f'<path fill="#0A0F14" fill-opacity="0.12" fill-rule="evenodd" d="{poly_d(sym)}"/>'
            f'<g fill="none" stroke="#00A98F" stroke-width="1">{"".join(lines)}</g>'
            f'<path fill="none" stroke="#0A0F14" stroke-width="1.5" d="{poly_d(sym)}"/>')


# =====================================================================================
# B — ENCAIXE: a tile split into modules; the seams between the modules draw the A.
# =====================================================================================
def encaixe(ch=24, apex=(128, 72), foot_dx=190 * math.tan(math.radians(25)), cross=172, r=56):
    tile = box(16 + r, 16 + r, 240 - r, 240 - r).buffer(r, quad_segs=24)
    a = LineString([(apex[0] - foot_dx * 1.4, apex[1] + 190 * 1.4), apex,
                    (apex[0] + foot_dx * 1.4, apex[1] + 190 * 1.4)]).buffer(ch / 2, cap_style=2, join_style=2, mitre_limit=8)
    half = (cross - apex[1]) * foot_dx / 190
    bar = box(apex[0] - half - 4, cross - ch / 2 * 0.9, apex[0] + half + 4, cross + ch / 2 * 0.9)
    return tile.difference(unary_union([a, bar]))


def slab_I(cap, stem, x, base, serif=2.5, bar=0.85):
    w = stem * serif
    bh = stem * bar
    return unary_union([box(x, base - cap, x + w, base - cap + bh), box(x, base - bh, x + w, base),
                        box(x + (w - stem) / 2, base - cap, x + (w + stem) / 2, base)]), w


def word_with_slab_I(prefix, family, weight, cap, base, tracking, x=0, weight_ai=None, ai_gap=0.0):
    d, w, boxes = text_path(prefix, family, weight, cap, x=x, baseline=base, tracking=tracking)
    out = [d]
    cur = x + w
    wa = weight_ai or weight
    em = cap / metrics(family, wa)["cap"] * metrics(family, wa)["upm"]
    cur += tracking * em + ai_gap * cap
    dA, wA, bA = text_path("A", family, wa, cap, x=cur, baseline=base)
    out.append(dA)
    _, _, bI = text_path("I", family, wa, cap)
    stem = bI[0][3] - bI[0][1]
    ix = bA[0][3] + cap * 0.07
    I, iw = slab_I(cap, stem, ix, base)
    return " ".join(out), poly_d(I), ix + iw


def lockup(sym_geom_d, sym_evenodd, word_d, word_I_d, word_right, S, cap, gap, title, path, sym_size=256):
    s = S / sym_size
    total_w = S + gap + word_right + 24 * 2
    ty = (256 - S) / 2
    body = (f'<g transform="translate(24 {fmt(ty)}) scale({fmt(s)})">{p(sym_geom_d, sym_evenodd)}</g>'
            f'<g transform="translate({fmt(24 + S + gap)} 0)">{p(word_d, False)}{p(word_I_d)}</g>')
    write(path, total_w, 256, body, title)


def concept_b():
    g = encaixe()
    d = poly_d(g)
    write(f"{ROOT}/B-encaixe/B-simbolo.svg", 256, 256, p(d), "AgendAI — Encaixe")
    cap = 70
    base = 128 + cap / 2
    wd, Id, right = word_with_slab_I("Agend", "Montserrat", 600, cap, base, -0.015)
    lockup(d, True, wd, Id, right, S=168, cap=cap, gap=40, title="AgendAI — logotipo (Encaixe)",
           path=f"{ROOT}/B-encaixe/B-logotipo-horizontal.svg")
    lines = (f'<g fill="none" stroke="#00A98F" stroke-width="1">'
             f'<line x1="128" y1="8" x2="128" y2="248"/><line x1="8" y1="172" x2="248" y2="172"/>'
             f'<line x1="8" y1="72" x2="248" y2="72"/><circle cx="72" cy="72" r="56"/></g>')
    write(f"{ROOT}/B-encaixe/B-construcao.svg", 256, 256,
          f'<rect width="256" height="256" fill="#fff"/><path fill="#0A0F14" fill-opacity="0.12" fill-rule="evenodd" d="{d}"/>'
          f'{lines}<path fill="none" stroke="#0A0F14" stroke-width="1.5" d="{d}"/>', "Construção — Encaixe")


# =====================================================================================
# C — PIVÔ: two rounded hands hinged on one point (clock hands / drafting compass) form the A.
# =====================================================================================
def pivo(apex=(128, 48), ang=math.degrees(math.atan(0.4)), L=184, w=36, pivot=26, gap=10, cross=(164, 30)):
    a = math.radians(ang)
    legs = []
    for side in (-1, 1):
        end = (apex[0] + side * L * math.sin(a), apex[1] + L * math.cos(a))
        legs.append(LineString([apex, end]).buffer(w / 2, cap_style=1, quad_segs=32))
    g = unary_union(legs)
    y, ww = cross
    half = (y - apex[1]) * math.tan(a)
    g = g.union(box(apex[0] - half, y - ww / 2, apex[0] + half, y + ww / 2))
    g = g.difference(Point(apex).buffer(pivot + gap, quad_segs=48))
    minx, miny, maxx, maxy = unary_union([g, Point(apex).buffer(pivot)]).bounds
    dy = 128 - (miny + maxy) / 2 - 3          # optical centre: a touch above geometric
    g = affinity.translate(g, 0, dy)
    c = (apex[0], apex[1] + dy)
    dot = f" M{fmt(c[0] - pivot)} {fmt(c[1])} A{pivot} {pivot} 0 1 0 {fmt(c[0] + pivot)} {fmt(c[1])} A{pivot} {pivot} 0 1 0 {fmt(c[0] - pivot)} {fmt(c[1])} Z"
    return poly_d(g) + dot, c


def concept_c():
    d, c = pivo()
    write(f"{ROOT}/C-pivo/C-simbolo.svg", 256, 256, p(d, False), "AgendAI — Pivô")
    cap = 72
    base = 128 + cap / 2
    wd, Id, right = word_with_slab_I("Agend", "Manrope", 500, cap, base, -0.01, weight_ai=800, ai_gap=0.02)
    lockup(d, False, wd, Id, right, S=176, cap=cap, gap=30, title="AgendAI — logotipo (Pivô)",
           path=f"{ROOT}/C-pivo/C-logotipo-horizontal.svg")
    lines = (f'<g fill="none" stroke="#00A98F" stroke-width="1">'
             f'<circle cx="{fmt(c[0])}" cy="{fmt(c[1])}" r="26"/><circle cx="{fmt(c[0])}" cy="{fmt(c[1])}" r="36"/>'
             f'<line x1="{fmt(c[0])}" y1="{fmt(c[1])}" x2="{fmt(c[0] - 184 * 0.371391)}" y2="{fmt(c[1] + 184 * 0.928477)}"/>'
             f'<line x1="{fmt(c[0])}" y1="{fmt(c[1])}" x2="{fmt(c[0] + 184 * 0.371391)}" y2="{fmt(c[1] + 184 * 0.928477)}"/>'
             f'<line x1="{fmt(c[0])}" y1="0" x2="{fmt(c[0])}" y2="256"/></g>')
    write(f"{ROOT}/C-pivo/C-construcao.svg", 256, 256,
          f'<rect width="256" height="256" fill="#fff"/><path fill="#0A0F14" fill-opacity="0.12" d="{d}"/>'
          f'{lines}<path fill="none" stroke="#0A0F14" stroke-width="1.5" d="{d}"/>', "Construção — Pivô")


if __name__ == "__main__":
    concept_a(); concept_b(); concept_c()
    print("ok")
