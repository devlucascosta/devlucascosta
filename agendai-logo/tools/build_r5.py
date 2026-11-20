"""Round 5 — finalists Pena, Ogiva, Disco (monochrome masters + the two palettes on white). Reuses round-4 builders."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from r5_shapes import pena, ogiva, disco
from build_r4 import PAL, symbol, horizontal, vertical, icon
from build_r3 import write

R = "rodada-5"
PROPS = [
    dict(k="D", slug="D-pena", nome="Pena", res=pena(nib=54, angle=-45, cb=(70, 178, 186, 156))),
    dict(k="E", slug="E-ogiva", nome="Ogiva", res=ogiva(bulge=-14, w=36, half=104, cb=(146, 172), apex_round=10)),
    dict(k="F", slug="F-disco", nome="Disco", res=disco(notch_top=50, notch_half=50, bridge=(146, 172))),
]


def main():
    for P in PROPS:
        body, curve, _ = P["res"]; body = body.simplify(0.2, preserve_topology=True); k = P["k"]; d = f"{R}/02-simbolos/{P['slug']}"
        m = PAL["mono"]["white"]
        write(f"{d}/{k}-simbolo.svg", 256, 256, symbol(body, curve, m[0], m[1]), f"AgendAI — {P['nome']}")
        b, W = horizontal(body, curve, *m); write(f"{d}/{k}-logotipo-horizontal.svg", W, 256, b, "horizontal")
        b, W, H = vertical(body, curve, *m); write(f"{d}/{k}-logotipo-vertical.svg", W, H, b, "vertical")
        write(f"{d}/{k}-icone-app.svg", 256, 256, icon(body, curve, *PAL["mono"]["icon"]), "ícone")
        for pk in ("esmeralda", "dourado"):
            C = PAL[pk]; cd = f"{R}/04-cores/{pk}"
            cb, cc, cw, ca = C["white"]
            cb = C.get("single_white", cb)
            write(f"{cd}/{k}-simbolo.svg", 256, 256, symbol(body, curve, cb, cc), "símbolo")
            b, W = horizontal(body, curve, cb, cc, cw, ca); write(f"{cd}/{k}-horizontal.svg", W, 256, b, "horizontal")
            b, W, H = vertical(body, curve, cb, cc, cw, ca); write(f"{cd}/{k}-vertical.svg", W, H, b, "vertical")
            t, _, ic = C["icon"]
            write(f"{cd}/{k}-icone-app.svg", 256, 256, icon(body, curve, t, C["single_icon"], ic), "ícone")
            write(f"{cd}/{k}-icone-app-alt.svg", 256, 256, icon(body, curve, *C["alt"]), "ícone alternativo")
    print("ok")


if __name__ == "__main__":
    main()
