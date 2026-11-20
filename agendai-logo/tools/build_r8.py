"""Round 8 — final comparison of the two finalists, with true-arc SVG masters.

A · Wordmark AgendAI (rodada 7 · C), corrected: the custom A matched to the font's weight (right stroke 33 = stem 31
    + diagonal compensation, hairline 24, crossbar 26), narrowed to the font's A width, optical spacing, centred.
B · Raiz + Pena (rodada 6 · B), unchanged design; outline rewritten with true arcs.
All shapely geometry is written through svgarc.geom_path (L + A commands only); type comes from the font as Béziers.
"""
import os, sys, re
sys.path.insert(0, os.path.dirname(__file__))
from shapely import affinity
from shapely.geometry import box
from shapely.ops import unary_union
from r6_shapes import raiz_ref
from r7_shapes import H_KW
from svgarc import geom_path
from glyphs import text_path
from geo import svg, fmt

R = "rodada-8"
FONT, WT = "plus-jakarta-sans", 600
WA = raiz_ref(wl=24, wr=33, nib_cut=12, t=26, flare=20, sag=12, tw=26, half=84)[0]   # A · the word's own A
SYM = raiz_ref(**H_KW)[0]                                                             # B · Raiz + Pena

PAL = {
    "mono": dict(word="#0A0F14", ai="#0A0F14", sym="#0A0F14", tile="#0A0F14", on_tile="#FFFFFF", alt=None),
    "esmeralda": dict(word="#0A0F14", ai="#00A98F", sym="#00A98F", tile="#0A0F14", on_tile="#00D1B2", alt=("#00D1B2", "#0A0F14")),
    "dourado": dict(word="#0D0D0D", ai="#D4AF5A", sym="#D4AF5A", tile="#0D0D0D", on_tile="#D4AF5A", alt=("#D4AF5A", "#0D0D0D")),
}


def fit(g, h, x, y):
    """Scale geometry to height h, place its bbox top-left at (x, y); return (path, width)."""
    minx, miny, maxx, maxy = g.bounds
    s = h / (maxy - miny)
    t = affinity.translate(affinity.scale(g, s, s, origin=(minx, miny)), x - minx, y - miny)
    return geom_path(t), (maxx - minx) * s


def slab_I(cap, base, x):
    _, _, bI = text_path("I", FONT, WT, cap)
    stem = bI[0][3] - bI[0][1]; sw, sh = stem * 2.3, stem * 0.78
    I = unary_union([box(x, base - cap, x + sw, base - cap + sh), box(x, base - sh, x + sw, base),
                     box(x + (sw - stem) / 2, base - cap, x + (sw + stem) / 2, base)])
    return geom_path(I), sw


def p(d, fill):
    return f'<path fill="{fill}" fill-rule="evenodd" d="{d}"/>'


# ---------------------------------------------------------------- A · wordmark (custom A's)
def wordmark(cap, base, x, cw, ca):
    out = ""
    dA, wA = fit(WA, cap, x, base - cap); out += p(dA, cw)
    lsb_g = 0.059 * cap
    d, w, boxes = text_path("gend", FONT, WT, cap, x=x + wA + 0.035 * cap - lsb_g, baseline=base, tracking=-0.012)
    out += f'<path fill="{cw}" d="{d}"/>'
    xa = boxes[-1][3] + 0.055 * cap                      # d stem -> A diagonal
    dA2, wA2 = fit(WA, cap, xa, base - cap); out += p(dA2, ca)
    dI, wI = slab_I(cap, base, xa + wA2 + 0.05 * cap); out += p(dI, ca)
    return out, xa + wA2 + 0.05 * cap + wI - x


# ---------------------------------------------------------------- B · standard wordmark for the lockup
def word_std(cap, base, x, cw, ca):
    d, w, boxes = text_path("Agend", FONT, WT, cap, x=x, baseline=base, tracking=-0.012)
    dA, wA, bA = text_path("A", FONT, WT, cap, x=boxes[-1][3] + cap * 0.05, baseline=base)
    dI, wI = slab_I(cap, base, bA[0][3] + cap * 0.085)
    return f'<path fill="{cw}" d="{d}"/><path fill="{ca}" d="{dA}"/>' + p(dI, ca), bA[0][3] + cap * 0.085 + wI - x


CAP = 64            # same cap height for both finalists (fair scale)
PAD = 24


def build_wordmark(pk, bg=None, cw=None, ca=None):
    P = PAL[pk]
    body, w = wordmark(CAP, 128 + CAP / 2 - 0.11 * CAP, PAD, cw or P["word"], ca or P["ai"])
    return body, w + 2 * PAD


def build_lockup_h(pk, cs=None, cw=None, ca=None):
    P = PAL[pk]
    H = CAP * 2.05
    base = 128 + CAP / 2
    ds, ws = fit(SYM, H, PAD, base - CAP / 2 - H / 2 - 1)
    wd, ww = word_std(CAP, base, PAD + ws + CAP * 0.62, cw or P["word"], ca or P["ai"])
    return p(ds, cs or P["sym"]) + wd, PAD + ws + CAP * 0.62 + ww + PAD


def build_lockup_v(pk, cap=46):
    P = PAL[pk]
    _, ww = word_std(cap, 0, 0, "#000", "#000")
    H = 150
    minx, miny, maxx, maxy = SYM.bounds
    ws = (maxx - minx) * H / (maxy - miny)
    W = max(ws, ww) + 56
    ds, _ = fit(SYM, H, (W - ws) / 2, 26)
    base = 26 + H + 30 + cap
    wd, _ = word_std(cap, base, (W - ww) / 2, P["word"], P["ai"])
    return p(ds, P["sym"]) + wd, W, base + 26


def letter(g, fill, size=256, fill_ratio=0.80):
    minx, miny, maxx, maxy = g.bounds
    h = size * fill_ratio * min(1, (maxy - miny) / (maxx - minx))
    w = (maxx - minx) * h / (maxy - miny)
    d, _ = fit(g, h, (size - w) / 2, (size - h) / 2 - size * 0.008)
    return p(d, fill)


def icon(g, tile, fill, size=256, ratio=0.58):
    minx, miny, maxx, maxy = g.bounds
    k = size * ratio / max(maxx - minx, maxy - miny)
    w, h = (maxx - minx) * k, (maxy - miny) * k
    d, _ = fit(g, h, (size - w) / 2, (size - h) / 2 - size * 0.012)
    return f'<rect width="{size}" height="{size}" rx="{size * 0.2237:.1f}" fill="{tile}"/>' + p(d, fill)


def write(path, w, h, body, title, bg=None):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if bg:
        body = f'<rect width="{fmt(w)}" height="{fmt(h)}" fill="{bg}"/>' + body
    open(path, "w").write(svg(round(w), round(h), body, title))


def main():
    for pk in ("mono", "esmeralda", "dourado"):
        P = PAL[pk]
        dA, dB = f"{R}/02-finalistas/A-wordmark/{pk}", f"{R}/02-finalistas/B-raiz-pena/{pk}"
        b, w = build_wordmark(pk); write(f"{dA}/A-wordmark.svg", w, 256, b, "AgendAI — wordmark")
        write(f"{dA}/A-letra.svg", 256, 256, letter(WA, P["word"] if pk != "esmeralda" else "#0A0F14"), "A do wordmark")
        write(f"{dA}/A-icone.svg", 256, 256, icon(WA, P["tile"], P["on_tile"]), "ícone")
        b, w = build_lockup_h(pk); write(f"{dB}/B-horizontal.svg", w, 256, b, "AgendAI — Raiz + Pena")
        b, w, h = build_lockup_v(pk); write(f"{dB}/B-vertical.svg", w, h, b, "AgendAI — Raiz + Pena vertical")
        write(f"{dB}/B-simbolo.svg", 256, 256, letter(SYM, P["sym"]), "símbolo")
        write(f"{dB}/B-icone.svg", 256, 256, icon(SYM, P["tile"], P["on_tile"]), "ícone")
        if P["alt"]:
            write(f"{dA}/A-icone-alt.svg", 256, 256, icon(WA, *P["alt"]), "ícone alternativo")
            write(f"{dB}/B-icone-alt.svg", 256, 256, icon(SYM, *P["alt"]), "ícone alternativo")
    # one-colour reversed (white on black)
    for kind in ("A", "B"):
        d = f"{R}/02-finalistas/{'A-wordmark' if kind == 'A' else 'B-raiz-pena'}/mono"
        if kind == "A":
            b, w = build_wordmark("mono", cw="#FFFFFF", ca="#FFFFFF"); write(f"{d}/A-wordmark-invertido.svg", w, 256, b, "invertido", bg="#0A0F14")
        else:
            b, w = build_lockup_h("mono", cs="#FFFFFF", cw="#FFFFFF", ca="#FFFFFF"); write(f"{d}/B-horizontal-invertido.svg", w, 256, b, "invertido", bg="#0A0F14")
    print("ok")


if __name__ == "__main__":
    main()
