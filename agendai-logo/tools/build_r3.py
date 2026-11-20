"""Round 3 — three proposals from the user's two style references (flat-top A, integrated curve, two flat tones).

01 Ponte   — the left leg stands on an arch that springs from the baseline and tucks behind the right leg (ref. 02).
02 Impulso — a soft ribbon comes out from behind the left leg, crosses in front of the right leg and rises (ref. 01).
03 Recorte — a solid A; the curve is carved out of it, so the left leg lifts off the ground (own synthesis).
Shared letter: flat top 36, left leg 34, right leg 46 (calligraphic contrast), outer half-width 106.
Wordmark: Plus Jakarta Sans SemiBold, upright, "AI" in the accent colour and an "I" with short serifs.
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from shapely.geometry import Polygon, box, LineString, MultiPolygon
from shapely.ops import unary_union
from shapely import affinity
from r3_shapes import flat_A, arc_pts, tapered, B
from geo import poly_d, svg, fmt
from glyphs import text_path

R = "rodada-3"
CLIP = box(-50, -50, 300, B)
KW = dict(half=106, apex_y=30, tw=36, wl=34, wr=46)
FONT, WT = "plus-jakarta-sans", 600


def drop_small(g, min_area=300):
    if isinstance(g, MultiPolygon):
        return unary_union([p for p in g.geoms if p.area >= min_area])
    return g


def base_legs():
    outer, inner, info = flat_A(**KW)
    L = outer.difference(inner).intersection(CLIP)
    return L, outer, inner, info


def ponte():
    L, outer, inner, info = base_legs()
    p = ((8, 244), (96, 172), (182, 154))
    pts, c, r = arc_pts(*p)
    arch = LineString(pts).buffer(13, cap_style=2, join_style=1).intersection(CLIP)
    ll = L.intersection(box(-50, -50, 128, 300)); rl = L.intersection(box(128, -50, 300, 300))
    under = Polygon(pts + [(p[2][0], 400), (p[0][0] - 40, 400)]).buffer(0)
    ll = drop_small(ll.difference(arch.buffer(7, join_style=2)).difference(under), 600)
    arch = arch.difference(rl.buffer(7, join_style=2))
    return unary_union([ll, rl]), arch, dict(c=c, r=r)


def impulso():
    L, outer, inner, info = base_legs()
    p = ((64, 210), (146, 166), (232, 140))
    pts, c, r = arc_pts(*p, n=80)
    rib = tapered(pts, 26, 12).intersection(CLIP)
    ll = L.intersection(box(-50, -50, 128, 300)); rl = L.intersection(box(128, -50, 300, 300))
    rib = drop_small(rib.difference(ll.buffer(7, join_style=2)).difference(ll))
    rl = rl.difference(rib.buffer(7, join_style=2))
    return unary_union([ll, rl]), rib, dict(c=c, r=r)


def recorte():
    outer, inner, info = flat_A(**KW)
    solid = outer.intersection(CLIP)
    p = ((26, 204), (100, 180), (198, 160))
    pts, c, r = arc_pts(*p, n=80)
    under = Polygon(pts + [(p[2][0] + 80, 400), (p[0][0] - 80, 400)]).buffer(0)
    opening = inner.intersection(under)
    counter = inner.intersection(box(-50, -50, 300, 148))
    leftcut = under.intersection(box(-50, -50, info["ap"][0], 300))
    g = drop_small(solid.difference(counter).difference(opening).difference(leftcut), 600)
    return g, None, dict(c=c, r=r)


PROPS = [
    dict(k="01", slug="01-ponte", nome="Ponte", build=ponte),
    dict(k="02", slug="02-impulso", nome="Impulso", build=impulso),
    dict(k="03", slug="03-recorte", nome="Recorte", build=recorte),
]

COLORS = {
    "mono": dict(light=("#FFFFFF", "#0A0F14", "#0A0F14", "#0A0F14", "#0A0F14"),
                 dark=("#0A0F14", "#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF"), tile=("#0A0F14", "#FFFFFF", "#FFFFFF")),
    # (bg, body, curve, word, ai)
    "esmeralda": dict(light=("#FFFFFF", "#0A0F14", "#00A98F", "#0A0F14", "#00A98F"),
                      dark=("#0A0F14", "#00A98F", "#00D1B2", "#FFFFFF", "#00D1B2"),
                      tile=("#0A0F14", "#00A98F", "#00D1B2"), tile2=("#00D1B2", "#0A0F14", "#FFFFFF")),
    "dourado": dict(light=("#F5F2E9", "#0D0D0D", "#B8913A", "#0D0D0D", "#0D0D0D"),
                    dark=("#0D0D0D", "#D4AF5A", "#E7CA82", "#F5F2E9", "#D4AF5A"),
                    tile=("#0D0D0D", "#D4AF5A", "#E7CA82"), tile2=("#D4AF5A", "#0D0D0D", "#F5F2E9")),
}


def norm(body, curve):
    allg = unary_union([g for g in (body, curve) if g is not None])
    minx, miny, maxx, maxy = allg.bounds
    return minx, miny, maxx, maxy


def tx(g, s, dx, dy, ox, oy):
    return affinity.translate(affinity.scale(g, s, s, origin=(ox, oy)), dx - ox, dy - oy)


def sym_paths(body, curve, s, x, y, cb, cc):
    minx, miny, maxx, maxy = norm(body, curve)
    if curve is None and cc not in ("#0A0F14", "#0D0D0D", "#FFFFFF") and cb not in ("#0A0F14", "#0D0D0D"):
        cb = cc   # single-shape symbol: use the brighter accent on dark grounds
    out = f'<path fill="{cb}" fill-rule="evenodd" d="{poly_d(tx(body, s, x, y, minx, miny))}"/>'
    if curve is not None:
        out += f'<path fill="{cc}" fill-rule="evenodd" d="{poly_d(tx(curve, s, x, y, minx, miny))}"/>'
    return out, (maxx - minx) * s, (maxy - miny) * s


def word(cap, base, x, cw, ca):
    d, w, boxes = text_path("Agend", FONT, WT, cap, x=x, baseline=base, tracking=-0.015)
    xa = x + w - 0.015 * cap / 0.75 * 0  # tracking already applied inside
    dA, wA, bA = text_path("A", FONT, WT, cap, x=boxes[-1][3] + cap * 0.06, baseline=base)
    _, _, bI = text_path("I", FONT, WT, cap)
    stem = bI[0][3] - bI[0][1]
    ix = bA[0][3] + cap * 0.085
    sw, sh = stem * 2.3, stem * 0.78
    I = unary_union([box(ix, base - cap, ix + sw, base - cap + sh), box(ix, base - sh, ix + sw, base),
                     box(ix + (sw - stem) / 2, base - cap, ix + (sw + stem) / 2, base)])
    return (f'<path fill="{cw}" d="{d}"/><path fill="{ca}" d="{dA}"/><path fill="{ca}" d="{poly_d(I)}"/>'), ix + sw - x


def write(p, w, h, body, title, bg=None):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if bg:
        body = f'<rect width="{fmt(w)}" height="{fmt(h)}" fill="{bg}"/>' + body
    open(p, "w").write(svg(w, h, body, title))


def symbol_file(body, curve, cb, cc, bg=None):
    minx, miny, maxx, maxy = norm(body, curve)
    s = 204 / max(maxx - minx, maxy - miny)
    w, h = (maxx - minx) * s, (maxy - miny) * s
    out, _, _ = sym_paths(body, curve, s, (256 - w) / 2, (256 - h) / 2 - 2, cb, cc)
    return out


def horizontal(body, curve, cols, cap=62):
    bg, cb, cc, cw, ca = cols
    minx, miny, maxx, maxy = norm(body, curve)
    H = cap * 2.05
    s = H / (maxy - miny)
    base = 128 + cap / 2
    sp, sw, sh = sym_paths(body, curve, s, 24, base - cap / 2 - H / 2 - 1, cb, cc)
    wd, ww = word(cap, base, 24 + sw + cap * 0.62, cw, ca)
    return sp + wd, 24 + sw + cap * 0.62 + ww + 24


def vertical(body, curve, cols, cap=46):
    bg, cb, cc, cw, ca = cols
    minx, miny, maxx, maxy = norm(body, curve)
    H = 150
    s = H / (maxy - miny)
    sw = (maxx - minx) * s
    _, ww = word(cap, 0, 0, cw, ca)
    W = max(sw, ww) + 56
    sp, _, _ = sym_paths(body, curve, s, (W - sw) / 2, 26, cb, cc)
    base = 26 + H + 30 + cap
    wd, _ = word(cap, base, (W - ww) / 2, cw, ca)
    return sp + wd, W, base + 26


def icon(body, curve, tile, cb, cc, size=256, ratio=0.60):
    minx, miny, maxx, maxy = norm(body, curve)
    s = size * ratio / max(maxx - minx, maxy - miny)
    w, h = (maxx - minx) * s, (maxy - miny) * s
    sp, _, _ = sym_paths(body, curve, s, (size - w) / 2, (size - h) / 2 - size * 0.012, cb, cc)
    return f'<rect width="{size}" height="{size}" rx="{size * 0.2237:.1f}" fill="{tile}"/>' + sp


def construction(body, curve, info):
    allg = unary_union([g for g in (body, curve) if g is not None])
    c, r = info["c"], info["r"]
    outer, inner, fi = flat_A(**KW)
    guides = (f'<circle cx="{fmt(c[0])}" cy="{fmt(c[1])}" r="{fmt(r)}"/>'
              f'<polygon points="{" ".join(f"{fmt(x)},{fmt(y)}" for x, y in list(outer.intersection(box(-50,-50,300,B)).exterior.coords))}"/>'
              f'<line x1="0" y1="{B}" x2="256" y2="{B}"/><line x1="0" y1="30" x2="256" y2="30"/>')
    return (f'<rect width="256" height="256" fill="#fff"/><path fill="#0A0F14" fill-opacity="0.10" fill-rule="evenodd" d="{poly_d(allg)}"/>'
            f'<g fill="none" stroke="#00A98F" stroke-width="0.9">{guides}</g>'
            f'<path fill="none" stroke="#0A0F14" stroke-width="1.4" d="{poly_d(allg)}"/>')


def main():
    for P in PROPS:
        body, curve, info = P["build"]()
        P["body"], P["curve"] = body, curve
        d = f"{R}/02-simbolos/{P['slug']}"
        k = P["k"]
        write(f"{d}/{k}-construcao.svg", 256, 256, construction(body, curve, info), f"Construção — {P['nome']}")
        m = COLORS["mono"]
        write(f"{d}/{k}-simbolo.svg", 256, 256, symbol_file(body, curve, "#0A0F14", "#0A0F14"), f"AgendAI — {P['nome']}")
        b, W = horizontal(body, curve, m["light"]); write(f"{d}/{k}-logotipo-horizontal.svg", W, 256, b, "logotipo horizontal")
        b, W, H = vertical(body, curve, m["light"]); write(f"{d}/{k}-logotipo-vertical.svg", W, H, b, "logotipo vertical")
        write(f"{d}/{k}-icone-app.svg", 256, 256, icon(body, curve, "#0A0F14", "#FFFFFF", "#FFFFFF"), "ícone")
        for pk in ("esmeralda", "dourado"):
            C = COLORS[pk]; cd = f"{R}/04-cores/{pk}"
            for mode in ("light", "dark"):
                bg, cb, cc, cw, ca = C[mode]
                tag = "claro" if mode == "light" else "escuro"
                write(f"{cd}/{k}-simbolo-{tag}.svg", 256, 256, symbol_file(body, curve, cb, cc), "símbolo", bg=bg)
                b, W = horizontal(body, curve, C[mode]); write(f"{cd}/{k}-horizontal-{tag}.svg", W, 256, b, "horizontal", bg=bg)
                b, W, H = vertical(body, curve, C[mode]); write(f"{cd}/{k}-vertical-{tag}.svg", W, H, b, "vertical", bg=bg)
                if mode == "dark":
                    write(f"{cd}/{k}-simbolo-cor.svg", 256, 256, symbol_file(body, curve, cb, cc), "símbolo transparente")
                    b, W = horizontal(body, curve, C[mode]); write(f"{cd}/{k}-horizontal-escuro-transparente.svg", W, 256, b, "horizontal")
                    b, W, H = vertical(body, curve, C[mode]); write(f"{cd}/{k}-vertical-escuro-transparente.svg", W, H, b, "vertical")
            write(f"{cd}/{k}-icone-app.svg", 256, 256, icon(body, curve, *C["tile"]), "ícone")
            write(f"{cd}/{k}-icone-app-alt.svg", 256, 256, icon(body, curve, *C["tile2"]), "ícone alternativo")
    print("ok")


if __name__ == "__main__":
    main()
