"""Round 4 side-by-side comparison on white: 3 columns (A Ponte, B Recorte, C Raiz) × sections."""
import re

R = "rodada-4"
S, CO = f"{R}/02-simbolos", f"{R}/04-cores"
P = [("A", "A-ponte", "Ponte refinada",
      "O arco nasce sob o pé esquerdo, carrega a perna e passa por trás da perna direita. Mais curto e mais curvo que na rodada 3: a base ficou equilibrada e a folga, uniforme.",
      "Dois tons; a curva é estrutural (sem ela a letra não fica de pé). Limite: em 16 px o arco vira só um pé alongado."),
     ("B", "B-recorte", "Recorte refinado",
      "Massa única; a base do travessão e o corte do pé esquerdo são o mesmo arco, e agora o topo do travessão acompanha esse arco (espessura constante de 30).",
      "O mais legível em 16 px e o mais fácil de reproduzir. Limite: na prateleira é o que mais se aproxima de um “A negrito”."),
     ("C", "C-raiz", "Raiz · híbrido",
      "O contorno esquerdo da letra é uma única curva que se abre até o chão (a integração da Ponte); a abertura de baixo é recortada por outro arco (a simplicidade do Recorte). Uma cor, uma massa.",
      "Silhueta mais própria das três, curva legível de 16 px ao ícone. Limite: o pé alargado exige respiro à esquerda nas composições.")]


def inl(p):
    s = open(p).read()
    return re.sub(r'\swidth="[^"]+"\s+height="[^"]+"', ' width="100%" height="100%"', s, count=1)


def cell(inner, cls="", cap=""):
    return f'<div class="cell {cls}">{inner}{f"<span>{cap}</span>" if cap else ""}</div>'


rows = []
rows.append(("", [f'<h2>{k} · {n}</h2><p class="idea">{i}</p>' for k, sl, n, i, _ in P]))
rows.append(("Símbolo isolado", [cell(inl(f"{S}/{sl}/{k}-simbolo.svg"), "sq") + cell(inl(f"{S}/{sl}/{k}-construcao.svg"), "sq", "construção") for k, sl, *_ in P]))
rows.append(("Logomarca · uma cor", [cell(inl(f"{S}/{sl}/{k}-logotipo-vertical.svg"), "v") for k, sl, *_ in P]))
rows.append(("Esmeralda Tech", [cell(inl(f"{CO}/esmeralda/{k}-vertical.svg"), "v") + cell(inl(f"{CO}/esmeralda/{k}-horizontal.svg"), "h") for k, sl, *_ in P]))
rows.append(("Preto e Dourado", [cell(inl(f"{CO}/dourado/{k}-vertical.svg"), "v") + cell(inl(f"{CO}/dourado/{k}-horizontal.svg"), "h") for k, sl, *_ in P]))
rows.append(("Ícone de aplicativo", ["".join(cell(inl(f"{d}/{k}-{f}.svg"), "ic") for d, f in
                                            ((f"{CO}/esmeralda", "icone-app"), (f"{CO}/esmeralda", "icone-app-alt"), (f"{CO}/dourado", "icone-app"), (f"{CO}/dourado", "icone-app-alt")))
                                    for k, sl, *_ in P]))


def sizes(k, sl):
    out = ""
    for src, label in ((f"{S}/{sl}/{k}-simbolo.svg", "uma cor"), (f"{CO}/esmeralda/{k}-icone-app.svg", "ícone esmeralda"), (f"{CO}/dourado/{k}-icone-app.svg", "ícone dourado")):
        out += '<div class="sz">' + "".join(f'<i style="width:{z}px;height:{z}px">{inl(src)}</i>' for z in (16, 24, 32, 64)) + f'<em>{label} · 16 · 24 · 32 · 64</em></div>'
    return out


rows.append(("Tamanhos pequenos", [sizes(k, sl) for k, sl, *_ in P]))
rows.append(("Avaliação", [f'<p class="eval">{e}</p>' for *_, e in P]))

body = "".join(f'<div class="row"><div class="lab">{lab}</div>' + "".join(f'<div class="col">{c}</div>' for c in cols) + "</div>" for lab, cols in rows)
html = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>AgendAI — rodada 4</title><style>
body{{margin:0;background:#fff;color:#0A0F14;font:14px/1.5 system-ui,-apple-system,"Segoe UI",Inter,sans-serif}}
main{{max-width:1360px;margin:0 auto;padding:36px 28px}} h1{{font-size:28px;margin:0 0 4px}} .sub{{color:#5b6470;margin:0 0 24px}}
.row{{display:grid;grid-template-columns:120px repeat(3,1fr);gap:18px;padding:14px 0;border-top:1px solid #eceeef}}
.lab{{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:#5b6470;padding-top:6px}}
.col{{display:flex;flex-wrap:wrap;gap:10px;align-content:flex-start}} h2{{margin:0;font-size:20px}} .idea{{margin:6px 0 0;color:#333}}
.cell{{position:relative;display:flex;align-items:center;justify-content:center;border:1px solid #eceeef;border-radius:10px;background:#fff}}
.cell span{{position:absolute;bottom:4px;left:8px;font-size:11px;color:#8a929b}}
.sq{{width:150px;height:150px}} .sq svg{{width:120px;height:120px}} .v{{width:170px;height:170px}} .v svg{{max-width:150px;max-height:150px}}
.h{{width:230px;height:100px}} .h svg{{max-width:210px;max-height:76px}} .ic{{width:88px;height:88px;border:none}} .ic svg{{width:84px;height:84px}}
.sz{{display:flex;align-items:flex-end;gap:12px;padding:8px 10px;border:1px solid #eceeef;border-radius:10px;width:100%;flex-wrap:wrap}} .sz i{{display:inline-block}}
.sz em{{font-style:normal;font-size:11px;color:#8a929b;width:100%}} .eval{{margin:0}}
</style></head><body><main><h1>AgendAI — rodada 4: Ponte, Recorte e Raiz</h1>
<p class="sub">Fundo branco, cores aplicadas direto no símbolo e na tipografia · Plus Jakarta Sans SemiBold, “AI” na cor e I com serifas curtas · mesma construção nas duas paletas</p>
{body}</main></body></html>"""
open(f"{R}/05-apresentacao/comparativo-rodada-4.html", "w").write(html)
print("ok")
