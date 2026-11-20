"""Round 4 — final refinement of Ponte and Recorte + hybrid "Raiz". White-background colour applications."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from shapely.ops import unary_union
from r4_shapes import ponte, recorte, raiz
from build_r3 import norm, tx, word, write, B
from geo import poly_d, fmt

R = "rodada-4"
PROPS = [
    dict(k="A", slug="A-ponte", nome="Ponte refinada", res=ponte(p0=(16, 246), p1=(100, 176), p2=(186, 158))),
    dict(k="B", slug="B-recorte", nome="Recorte refinado", res=recorte(t=30)),
    dict(k="C", slug="C-raiz", nome="Raiz (híbrido)", res=raiz()),
]
# palette: (body, curve, word, ai) on WHITE  +  icon (tile, body, curve)  +  alt icon
PAL = {
    "mono": dict(white=("#0A0F14", "#0A0F14", "#0A0F14", "#0A0F14"), icon=("#0A0F14", "#FFFFFF", "#FFFFFF")),
    "esmeralda": dict(white=("#00A98F", "#00D1B2", "#0A0F14", "#00A98F"), icon=("#0A0F14", "#00A98F", "#00D1B2"),
                      single_icon="#00D1B2", alt=("#00D1B2", "#0A0F14", "#0A0F14")),
    "dourado": dict(white=("#0D0D0D", "#D4AF5A", "#0D0D0D", "#D4AF5A"), single_white="#D4AF5A",
                    icon=("#0D0D0D", "#D4AF5A", "#E7CA82"), single_icon="#D4AF5A", alt=("#D4AF5A", "#0D0D0D", "#0D0D0D")),
}


def paths(body, curve, s, x, y, cb, cc):
    minx, miny, maxx, maxy = norm(body, curve)
    out = f'<path fill="{cb}" fill-rule="evenodd" d="{poly_d(tx(body, s, x, y, minx, miny))}"/>'
    if curve is not None:
        out += f'<path fill="{cc}" fill-rule="evenodd" d="{poly_d(tx(curve, s, x, y, minx, miny))}"/>'
    return out, (maxx - minx) * s, (maxy - miny) * s


def symbol(body, curve, cb, cc, size=256, fill=204):
    minx, miny, maxx, maxy = norm(body, curve)
    s = fill / max(maxx - minx, maxy - miny)
    w, h = (maxx - minx) * s, (maxy - miny) * s
    return paths(body, curve, s, (size - w) / 2, (size - h) / 2 - 2, cb, cc)[0]


def horizontal(body, curve, cb, cc, cw, ca, cap=62):
    minx, miny, maxx, maxy = norm(body, curve)
    H = cap * 2.05; s = H / (maxy - miny); base = 128 + cap / 2
    sp, sw, _ = paths(body, curve, s, 24, base - cap / 2 - H / 2 - 1, cb, cc)
    wd, ww = word(cap, base, 24 + sw + cap * 0.62, cw, ca)
    return sp + wd, 24 + sw + cap * 0.62 + ww + 24


def vertical(body, curve, cb, cc, cw, ca, cap=46):
    minx, miny, maxx, maxy = norm(body, curve)
    H = 150; s = H / (maxy - miny); sw = (maxx - minx) * s
    _, ww = word(cap, 0, 0, cw, ca)
    W = max(sw, ww) + 56
    sp, _, _ = paths(body, curve, s, (W - sw) / 2, 26, cb, cc)
    base = 26 + H + 30 + cap
    wd, _ = word(cap, base, (W - ww) / 2, cw, ca)
    return sp + wd, W, base + 26


def icon(body, curve, tile, cb, cc, size=256, ratio=0.60):
    minx, miny, maxx, maxy = norm(body, curve)
    s = size * ratio / max(maxx - minx, maxy - miny)
    w, h = (maxx - minx) * s, (maxy - miny) * s
    sp, _, _ = paths(body, curve, s, (size - w) / 2, (size - h) / 2 - size * 0.012, cb, cc)
    return f'<rect width="{size}" height="{size}" rx="{size * 0.2237:.1f}" fill="{tile}"/>' + sp


def construction(body, curve, info):
    allg = unary_union([g for g in (body, curve) if g is not None])
    guides = ""
    if info.get("c"):
        c, r = info["c"], info["r"]
        guides += f'<circle cx="{fmt(c[0])}" cy="{fmt(c[1])}" r="{fmt(r)}"/>'
    if info.get("left"):
        guides += '<polyline points="' + " ".join(f"{fmt(x)},{fmt(y)}" for x, y in info["left"]) + '"/>'
    guides += f'<line x1="0" y1="{B}" x2="256" y2="{B}"/><line x1="0" y1="30" x2="256" y2="30"/>'
    return (f'<rect width="256" height="256" fill="#fff"/><path fill="#0A0F14" fill-opacity="0.10" fill-rule="evenodd" d="{poly_d(allg)}"/>'
            f'<g fill="none" stroke="#00A98F" stroke-width="0.9">{guides}</g>'
            f'<path fill="none" stroke="#0A0F14" stroke-width="1.4" d="{poly_d(allg)}"/>')


def main():
    for P in PROPS:
        body, curve, info = P["res"]; k = P["k"]
        d = f"{R}/02-simbolos/{P['slug']}"
        write(f"{d}/{k}-construcao.svg", 256, 256, construction(body, curve, info), f"Construção — {P['nome']}")
        m = PAL["mono"]["white"]
        write(f"{d}/{k}-simbolo.svg", 256, 256, symbol(body, curve, m[0], m[1]), f"AgendAI — {P['nome']}")
        b, W = horizontal(body, curve, *m); write(f"{d}/{k}-logotipo-horizontal.svg", W, 256, b, "horizontal")
        b, W, H = vertical(body, curve, *m); write(f"{d}/{k}-logotipo-vertical.svg", W, H, b, "vertical")
        write(f"{d}/{k}-icone-app.svg", 256, 256, icon(body, curve, *PAL["mono"]["icon"]), "ícone")
        for pk in ("esmeralda", "dourado"):
            C = PAL[pk]; cd = f"{R}/04-cores/{pk}"
            cb, cc, cw, ca = C["white"]
            if curve is None and C.get("single_white"):
                cb = C["single_white"]
            write(f"{cd}/{k}-simbolo.svg", 256, 256, symbol(body, curve, cb, cc), "símbolo")
            b, W = horizontal(body, curve, cb, cc, cw, ca); write(f"{cd}/{k}-horizontal.svg", W, 256, b, "horizontal")
            b, W, H = vertical(body, curve, cb, cc, cw, ca); write(f"{cd}/{k}-vertical.svg", W, H, b, "vertical")
            t, ib, ic = C["icon"]
            if curve is None:
                ib = C["single_icon"]
            write(f"{cd}/{k}-icone-app.svg", 256, 256, icon(body, curve, t, ib, ic), "ícone")
            write(f"{cd}/{k}-icone-app-alt.svg", 256, 256, icon(body, curve, *C["alt"]), "ícone alternativo")
    print("ok")


if __name__ == "__main__":
    main()
