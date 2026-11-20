"""Round 7 — A: Raiz + Pena evoluída · B: Encontro (independent symbol) · C: wordmark AgendAI.
Also builds dark-background lockups for Raiz (r4) and Raiz + Pena (r6) so all five compare on light and dark."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from shapely import affinity
from shapely.ops import unary_union
from r7_shapes import raiz_pena_evo, encontro, H_KW
from r6_shapes import raiz_ref
from r4_shapes import raiz
from build_r4 import PAL, symbol, horizontal, vertical, icon, paths
from build_r3 import write, word, norm
from glyphs import text_path
from geo import poly_d, fmt
from shapely.geometry import box

R = "rodada-7"
DARK = {"esmeralda": ("#0A0F14", "#00D1B2", "#00D1B2", "#FFFFFF", "#00D1B2"),
        "dourado": ("#0D0D0D", "#D4AF5A", "#E7CA82", "#F5F2E9", "#D4AF5A")}

# ---------------------------------------------------------------- C · wordmark
WA = raiz_ref(wl=28, wr=38, nib_cut=12, t=28, flare=22, sag=12, tw=28, half=92)[0]   # the word's own A


def wordmark(cap, base, x, cw, ca, track=-0.012):
    minx, miny, maxx, maxy = WA.bounds
    s = cap / (maxy - miny)
    def A_at(xx, fill):
        g = affinity.translate(affinity.scale(WA, s, s, origin=(minx, miny)), xx - minx, base - cap - miny)
        return f'<path fill="{fill}" fill-rule="evenodd" d="{poly_d(g)}"/>', (maxx - minx) * s
    out, w1 = A_at(x, cw)
    d, w, boxes = text_path("gend", "plus-jakarta-sans", 600, cap, x=x + w1 + cap * 0.01, baseline=base, tracking=track)
    out += f'<path fill="{cw}" d="{d}"/>'
    xa = boxes[-1][3] + cap * 0.07
    a2, w2 = A_at(xa, ca); out += a2
    _, _, bI = text_path("I", "plus-jakarta-sans", 600, cap)
    stem = bI[0][3] - bI[0][1]; ix = xa + w2 + cap * 0.06; sw, sh = stem * 2.3, stem * 0.78
    I = unary_union([box(ix, base - cap, ix + sw, base - cap + sh), box(ix, base - sh, ix + sw, base),
                     box(ix + (sw - stem) / 2, base - cap, ix + (sw + stem) / 2, base)])
    out += f'<path fill="{ca}" d="{poly_d(I)}"/>'
    return out, ix + sw - x


def write_wordmark(path, cw, ca, bg=None, cap=96):
    body, w = wordmark(cap, 128 + cap / 2 - 0.11 * cap, 32, cw, ca)   # optical centre incl. the g descender
    write(path, w + 64, 256, body, "AgendAI — wordmark", bg=bg)


# ---------------------------------------------------------------- build
def sym_set(k, slug, res, label):
    body, curve, _ = res
    if k != "K":                       # keep true-resolution arcs on Encontro's quarter circle
        body = body.simplify(0.2, preserve_topology=True)
    d = f"{R}/02-simbolos/{slug}"
    m = PAL["mono"]["white"]
    write(f"{d}/{k}-simbolo.svg", 256, 256, symbol(body, curve, m[0], m[1]), f"AgendAI — {label}")
    b, W = horizontal(body, curve, *m); write(f"{d}/{k}-logotipo-horizontal.svg", W, 256, b, "horizontal")
    b, W, H = vertical(body, curve, *m); write(f"{d}/{k}-logotipo-vertical.svg", W, H, b, "vertical")
    write(f"{d}/{k}-icone-app.svg", 256, 256, icon(body, curve, *PAL["mono"]["icon"]), "ícone")
    for pk in ("esmeralda", "dourado"):
        C = PAL[pk]; cd = f"{R}/04-cores/{pk}"
        cb, cc, cw, ca = C["white"]; cb = C.get("single_white", cb)
        write(f"{cd}/{k}-simbolo.svg", 256, 256, symbol(body, curve, cb, cc), "símbolo")
        b, W, H = vertical(body, curve, cb, cc, cw, ca); write(f"{cd}/{k}-vertical.svg", W, H, b, "vertical")
        t, _, ic = C["icon"]
        write(f"{cd}/{k}-icone-app.svg", 256, 256, icon(body, curve, t, C["single_icon"], ic), "ícone")
        write(f"{cd}/{k}-icone-app-alt.svg", 256, 256, icon(body, curve, *C["alt"]), "ícone alternativo")
        bg, db, dc, dw, da = DARK[pk]
        b, W = horizontal(body, curve, db, dc, dw, da); write(f"{cd}/{k}-horizontal-escuro.svg", W, 256, b, "escuro", bg=bg)


def main():
    sym_set("R", "R-raiz-r4", raiz(), "Raiz (rodada 4)")                       # reference, dark versions only new
    sym_set("H", "H-raiz-pena-r6", raiz_ref(**H_KW), "Raiz + Pena (rodada 6)")  # reference
    sym_set("J", "J-raiz-pena-evoluida", raiz_pena_evo(), "Raiz + Pena evoluída")
    sym_set("K", "K-encontro", encontro(), "Encontro")
    # C · wordmark (+ its A as the optional icon)
    d = f"{R}/02-simbolos/L-wordmark"
    write_wordmark(f"{d}/L-wordmark.svg", "#0A0F14", "#0A0F14")
    write(f"{d}/L-simbolo.svg", 256, 256, symbol(WA, None, "#0A0F14", "#0A0F14"), "A do wordmark")
    write(f"{d}/L-icone-app.svg", 256, 256, icon(WA, None, "#0A0F14", "#FFFFFF", "#FFFFFF"), "ícone")
    for pk in ("esmeralda", "dourado"):
        C = PAL[pk]; cd = f"{R}/04-cores/{pk}"
        cb, cc, cw, ca = C["white"]
        write_wordmark(f"{cd}/L-wordmark.svg", "#0A0F14" if pk == "esmeralda" else "#0D0D0D", ca)
        bg, db, dc, dw, da = DARK[pk]
        write_wordmark(f"{cd}/L-wordmark-escuro.svg", dw, da, bg=bg)
        t, _, ic = C["icon"]
        write(f"{cd}/L-icone-app.svg", 256, 256, icon(WA, None, t, C["single_icon"], ic), "ícone")
        write(f"{cd}/L-icone-app-alt.svg", 256, 256, icon(WA, None, *C["alt"]), "ícone alternativo")
        write(f"{cd}/L-simbolo.svg", 256, 256, symbol(WA, None, C.get("single_white", cb), cc), "símbolo")
    print("ok")


if __name__ == "__main__":
    main()
