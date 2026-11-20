"""Round 2 — three new AgendAI proposals: black master, construction, lockup, and the two colour identities.

P01 Traço  — two straight legs; the crossbar is one circular arc born at the left foot that crosses the
             structure and leaves through the right leg, rising.                     Type: Instrument Sans 500
P02 Arco   — one continuous solid A: soft apex, rounded counter, the lower opening is an arch.
                                                                                      Type: Plus Jakarta Sans 500
P03 Vela   — straight left side, circular-arc right side, constant weight, straight crossbar.
                                                                                      Type: DM Sans 500
All letters outlined (no <text>). The "I" gets short slab serifs so AgendAI never reads AgendAl.
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from shapely.geometry import Polygon, box, Point
from shapely.ops import unary_union
from shapely import affinity
from r2_shapes import (letter_from_outline, sym_outline, sail_outline, arc_band, centre, K)
from geo import poly_d, svg, fmt
from glyphs import text_path, metrics

R = "rodada-2"
B = 226
PALETTES = {
    "esmeralda": dict(nome="Esmeralda Tech", light_bg="#FFFFFF", dark_bg="#0A0F14", sym_light="#00A98F",
                      sym_dark="#00D1B2", word_light="#0A0F14", word_dark="#FFFFFF", tile="#0A0F14", tile_sym="#00D1B2",
                      tile2="#00D1B2", tile2_sym="#0A0F14"),
    "dourado": dict(nome="Preto e Dourado", light_bg="#F5F2E9", dark_bg="#0D0D0D", sym_light="#D4AF5A",
                    sym_dark="#D4AF5A", word_light="#0D0D0D", word_dark="#F5F2E9", tile="#0D0D0D", tile_sym="#D4AF5A",
                    tile2="#D4AF5A", tile2_sym="#0D0D0D"),
}


# ------------------------------------------------------------------ symbols
def circ3(p1, p2, p3):
    ax, ay = p1; bx, by = p2; cx, cy = p3
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax**2 + ay**2) * (by - cy) + (bx**2 + by**2) * (cy - ay) + (cx**2 + cy**2) * (ay - by)) / d
    uy = ((ax**2 + ay**2) * (cx - bx) + (bx**2 + by**2) * (ax - cx) + (cx**2 + cy**2) * (bx - ax)) / d
    return (ux, uy), math.hypot(ax - ux, ay - uy)


def p01():
    w, half, apex_y = 30, 94, 28
    out = sym_outline(apex_y, B, half)
    legs = letter_from_outline(out, w, B, apex_round=6)
    pts = ((70, 196), (160, 160), (226, 150))
    c, r = circ3(*pts)
    ang = lambda p: math.degrees(math.atan2(p[1] - c[1], p[0] - c[0]))
    arc = arc_band(c, r, 26, ang(pts[0]), ang(pts[2]))
    g = unary_union([legs, arc]).intersection(box(-50, -50, 300, B))
    info = dict(c=c, r=r, half=half, apex_y=apex_y, w=w)
    return g, info


def p02():
    out = sym_outline(24, B, 98)
    g = letter_from_outline(out, 35, B, cb=(150, 174), apex_round=28, open_round=24, counter_round=8)
    return g, dict(apex_round=28, open_round=24)


def p03():
    out, (cx, cy, Rr) = sail_outline((112, 26), (40, B), (216, B), 38)
    g = letter_from_outline(out, 32, B, cb=(148, 172), apex_round=4)
    return g, dict(c=(cx, cy), r=Rr)


PROPOSTAS = [
    dict(k="P01", slug="P01-traco", nome="Traço", font="instrument-sans", wt=500, build=p01),
    dict(k="P02", slug="P02-arco", nome="Arco", font="plus-jakarta-sans", wt=500, build=p02),
    dict(k="P03", slug="P03-vela", nome="Vela", font="dm-sans", wt=500, build=p03),
]


# ------------------------------------------------------------------ wordmark
def wordmark(font, wt, cap, base=0, tracking=-0.012):
    d, w, boxes = text_path("AgendA", font, wt, cap, x=0, baseline=base, tracking=tracking)
    _, _, bI = text_path("I", font, wt, cap)
    stem = bI[0][3] - bI[0][1]
    ix = boxes[-1][3] + cap * 0.085
    sw, sh = stem * 2.3, stem * 0.78
    I = unary_union([box(ix, base - cap, ix + sw, base - cap + sh), box(ix, base - sh, ix + sw, base),
                     box(ix + (sw - stem) / 2, base - cap, ix + (sw + stem) / 2, base)])
    right = ix + sw
    # descender of g for vertical bounds
    ys = [b[2] for b in boxes] + [b[4] for b in boxes]
    return d, poly_d(I), right, min(ys), max(ys)


def path(d, fill, evenodd=True):
    return f'<path fill="{fill}"{" fill-rule=\"evenodd\"" if evenodd else ""} d="{d}"/>'


def lockup_body(sym_g, font, wt, sym_fill, word_fill, cap=64):
    """Horizontal lockup: symbol height = 2.0 × cap, vertically centred on the cap band, gap = 0.75 × cap."""
    minx, miny, maxx, maxy = sym_g.bounds
    H = cap * 2.0
    s = H / (maxy - miny)
    sg = affinity.scale(sym_g, s, s, origin=(minx, miny))
    sg = affinity.translate(sg, -minx, -miny)
    sw = (maxx - minx) * s
    base = 128 + cap / 2
    sg = affinity.translate(sg, 0, (base - cap / 2) - H / 2 - 1)     # centred on cap band, optical lift 1
    gap = cap * 0.75
    wd, Id, right, ytop, ybot = wordmark(font, wt, cap, base=base)
    pad = 24
    body = (f'<g transform="translate({pad} 0)">{path(poly_d(sg), sym_fill)}'
            f'<g transform="translate({fmt(sw + gap)} 0)">{path(wd, word_fill, False)}{path(Id, word_fill)}</g></g>')
    return body, pad * 2 + sw + gap + right


def stacked_body(sym_g, font, wt, sym_fill, word_fill, cap=40):
    minx, miny, maxx, maxy = sym_g.bounds
    H = 150
    s = H / (maxy - miny)
    sg = affinity.translate(affinity.scale(sym_g, s, s, origin=(minx, miny)), -minx, -miny)
    sw = (maxx - minx) * s
    wd, Id, right, ytop, ybot = wordmark(font, wt, cap, base=0)
    W = max(sw, right) + 48
    sg = affinity.translate(sg, (W - sw) / 2, 20)
    tx, ty = (W - right) / 2, 20 + H + 22 + cap
    body = (f'{path(poly_d(sg), sym_fill)}<g transform="translate({fmt(tx)} {fmt(ty)})">'
            f'{path(wd, word_fill, False)}{path(Id, word_fill)}</g>')
    return body, W, ty + 18


def icon_body(sym_g, tile, fill, size=256, ratio=0.62):
    minx, miny, maxx, maxy = sym_g.bounds
    s = size * ratio / max(maxx - minx, maxy - miny)
    sg = affinity.translate(affinity.scale(sym_g, s, s, origin=(minx, miny)), -minx, -miny)
    w, h = (maxx - minx) * s, (maxy - miny) * s
    sg = affinity.translate(sg, (size - w) / 2, (size - h) / 2 - size * 0.012)
    return (f'<rect width="{size}" height="{size}" rx="{size * 0.2237:.1f}" fill="{tile}"/>' + path(poly_d(sg), fill))


def construction(g, k, info):
    guides = []
    if k == "P01":
        c, r = info["c"], info["r"]
        guides.append(f'<circle cx="{fmt(c[0])}" cy="{fmt(c[1])}" r="{fmt(r)}"/>')
        guides.append(f'<line x1="0" y1="{B}" x2="256" y2="{B}"/><line x1="128" y1="0" x2="128" y2="256"/>')
    elif k == "P02":
        guides.append('<line x1="0" y1="146" x2="256" y2="146"/><line x1="0" y1="172" x2="256" y2="172"/>'
                      f'<line x1="128" y1="0" x2="128" y2="256"/><line x1="0" y1="{B}" x2="256" y2="{B}"/>')
    else:
        c, r = info["c"], info["r"]
        guides.append(f'<circle cx="{fmt(c[0])}" cy="{fmt(c[1])}" r="{fmt(r)}"/>'
                      f'<line x1="0" y1="148" x2="256" y2="148"/><line x1="0" y1="172" x2="256" y2="172"/>'
                      f'<line x1="0" y1="{B}" x2="256" y2="{B}"/>')
    return (f'<rect width="256" height="256" fill="#fff"/><path fill="#0A0F14" fill-opacity="0.10" fill-rule="evenodd" d="{poly_d(g)}"/>'
            f'<g fill="none" stroke="#00A98F" stroke-width="0.9">{"".join(guides)}</g>'
            f'<path fill="none" stroke="#0A0F14" stroke-width="1.4" d="{poly_d(g)}"/>')


def write(p, w, h, body, title, bg=None):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if bg:
        body = f'<rect width="{fmt(w)}" height="{fmt(h)}" fill="{bg}"/>' + body
    open(p, "w").write(svg(w, h, body, title))


def main():
    for P in PROPOSTAS:
        raw, info = P["build"]()
        # construction is drawn in the un-centred frame so guides line up
        d = f"{R}/02-simbolos/{P['slug']}"
        write(f"{d}/{P['k']}-construcao.svg", 256, 256, construction(raw, P["k"], info), f"Construção — {P['nome']}")
        g = centre(raw)
        P["geom"] = g
        write(f"{d}/{P['k']}-simbolo.svg", 256, 256, path(poly_d(g), K), f"AgendAI — {P['nome']}")
        body, W = lockup_body(g, P["font"], P["wt"], K, K)
        write(f"{d}/{P['k']}-logotipo-horizontal.svg", W, 256, body, f"AgendAI — logotipo ({P['nome']})")
        body, W, H = stacked_body(g, P["font"], P["wt"], K, K)
        write(f"{d}/{P['k']}-logotipo-vertical.svg", W, H, body, f"AgendAI — logotipo vertical ({P['nome']})")
        write(f"{d}/{P['k']}-icone-app.svg", 256, 256, icon_body(g, "#0A0F14", "#FFFFFF"), f"AgendAI — ícone ({P['nome']})")
        for pk, pal in PALETTES.items():
            cd = f"{R}/04-cores/{pk}"
            write(f"{cd}/{P['k']}-simbolo-claro.svg", 256, 256, path(poly_d(g), pal["sym_light"]), "símbolo", bg=pal["light_bg"])
            write(f"{cd}/{P['k']}-simbolo-escuro.svg", 256, 256, path(poly_d(g), pal["sym_dark"]), "símbolo", bg=pal["dark_bg"])
            write(f"{cd}/{P['k']}-simbolo-cor.svg", 256, 256, path(poly_d(g), pal["sym_dark"]), "símbolo (transparente)")
            body, W = lockup_body(g, P["font"], P["wt"], pal["sym_light"], pal["word_light"])
            write(f"{cd}/{P['k']}-horizontal-claro.svg", W, 256, body, "logotipo claro", bg=pal["light_bg"])
            body, W = lockup_body(g, P["font"], P["wt"], pal["sym_dark"], pal["word_dark"])
            write(f"{cd}/{P['k']}-horizontal-escuro.svg", W, 256, body, "logotipo escuro", bg=pal["dark_bg"])
            body, W = lockup_body(g, P["font"], P["wt"], pal["sym_dark"], pal["word_dark"])
            write(f"{cd}/{P['k']}-horizontal-escuro-transparente.svg", W, 256, body, "logotipo escuro (transparente)")
            write(f"{cd}/{P['k']}-icone-app.svg", 256, 256, icon_body(g, pal["tile"], pal["tile_sym"]), "ícone")
            write(f"{cd}/{P['k']}-icone-app-alt.svg", 256, 256, icon_body(g, pal["tile2"], pal["tile2_sym"]), "ícone alternativo")
    print("ok")
    return PROPOSTAS


if __name__ == "__main__":
    main()
