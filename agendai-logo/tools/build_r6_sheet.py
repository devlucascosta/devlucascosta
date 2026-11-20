"""Round 4 side-by-side comparison on white: 3 columns (A Ponte, B Recorte, C Raiz) × sections."""
import re

R = "rodada-4"
S, CO = f"{R}/02-simbolos", f"{R}/04-cores"
R4, R5 = "rodada-4", "rodada-5"
R6 = "rodada-6"
P = [  # (key, folder-root, slug, name, idea, strengths, limits)
 ("A", R4, "A-ponte", "Ponte · referência", "A perna esquerda pousa num arco que passa por trás da direita.",
  "Dois tons; mais próxima das referências.", "Detalhe some abaixo de 24 px."),
 ("C", R4, "C-raiz", "Raiz · rodada 4", "Contorno esquerdo em curva que se abre até o chão; abertura recortada.",
  "Silhueta própria; uma cor; firme em 16 px.", "Ainda um pouco ‘geométrica’ no acabamento."),
 ("G", R6, "G-raiz-refinada", "A · Raiz refinada", "Mesma silhueta; curva esquerda mais suave (flecha 12), pé 4 un. mais contido, topo 34, travessão 28 e abertura com arco mais longo.",
  "Mais equilibrada e calma que a r4, sem perder identidade; a mais segura.", "Mudança sutil: quem não compara lado a lado mal percebe."),
 ("H", R6, "H-raiz-pena", "B · Raiz + Pena", "A estrutura da Raiz desenhada com lógica de pena: ápice cortado a 45°, traço esquerdo fino no alto que engorda até o pé (24→flare), perna direita cheia (52).",
  "A mais humana e elegante sem perder a silhueta própria; contraste que tem razão de ser.", "Traço fino no alto pede cuidado abaixo de 16 px; ícone ligeiramente mais leve."),
 ("I", R6, "I-pena-autoral", "C · Pena autoral", "Dois gestos de pena: a haste fina para antes do traço cheio (a pena foi levantada) e o travessão sobe como na escrita.",
  "Deixa de ser ‘A de fonte’: o gesto é exclusivo; o mais caligráfico.", "A pausa some abaixo de 32 px (vira um A clássico); menos própria como silhueta."),
]


def S(root, slug, k, f): return f"{root}/02-simbolos/{slug}/{k}-{f}.svg"
def CO(root, pk, k, f): return f"{root}/04-cores/{pk}/{k}-{f}.svg"


def inl(p):
    s = open(p).read()
    return re.sub(r'\swidth="[^"]+"\s+height="[^"]+"', ' width="100%" height="100%"', s, count=1)


def cell(inner, cls="", cap=""):
    return f'<div class="cell {cls}">{inner}{f"<span>{cap}</span>" if cap else ""}</div>'


rows = []
rows.append(("", [f'<h2>{n}</h2><p class="idea">{i}</p>' for k, r, sl, n, i, *_ in P]))
rows.append(("Símbolo", [cell(inl(S(r, sl, k, "simbolo")), "sq") for k, r, sl, *_ in P]))
rows.append(("Logomarca · uma cor", [cell(inl(S(r, sl, k, "logotipo-vertical")), "v") for k, r, sl, *_ in P]))
rows.append(("Esmeralda Tech", [cell(inl(CO(r, "esmeralda", k, "vertical")), "v") for k, r, sl, *_ in P]))
rows.append(("Preto e Dourado", [cell(inl(CO(r, "dourado", k, "vertical")), "v") for k, r, sl, *_ in P]))
rows.append(("Ícone de aplicativo", ["".join(cell(inl(CO(r, pk, k, f)), "ic") for pk, f in
         (("esmeralda", "icone-app"), ("esmeralda", "icone-app-alt"), ("dourado", "icone-app"), ("dourado", "icone-app-alt")))
         for k, r, sl, *_ in P]))


def sizes(k, r, sl):
    out = ""
    for src, label in ((S(r, sl, k, "simbolo"), "uma cor"), (CO(r, "esmeralda", k, "icone-app"), "ícone")):
        out += '<div class="sz">' + "".join(f'<i style="width:{z}px;height:{z}px">{inl(src)}</i>' for z in (16, 24, 32)) + f'<em>{label} · 16 · 24 · 32</em></div>'
    return out


rows.append(("16 · 24 · 32 px", [sizes(k, r, sl) for k, r, sl, *_ in P]))
rows.append(("Pontos fortes", [f'<p class="eval">{f}</p>' for *_, f, l in P]))
rows.append(("Limitações", [f'<p class="eval">{l}</p>' for *_, f, l in P]))

body = "".join(f'<div class="row"><div class="lab">{lab}</div>' + "".join(f'<div class="col">{c}</div>' for c in cols) + "</div>" for lab, cols in rows)
html = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>AgendAI — rodada 4</title><style>
body{{margin:0;background:#fff;color:#0A0F14;font:14px/1.5 system-ui,-apple-system,"Segoe UI",Inter,sans-serif}}
main{{max-width:1500px;margin:0 auto;padding:36px 28px}} h1{{font-size:28px;margin:0 0 4px}} .sub{{color:#5b6470;margin:0 0 24px}}
.row{{display:grid;grid-template-columns:96px repeat(5,1fr);gap:18px;padding:14px 0;border-top:1px solid #eceeef}}
.lab{{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:#5b6470;padding-top:6px}}
.col{{display:flex;flex-wrap:wrap;gap:10px;align-content:flex-start}} h2{{margin:0;font-size:20px}} .idea{{margin:6px 0 0;color:#333}}
.cell{{position:relative;display:flex;align-items:center;justify-content:center;border:1px solid #eceeef;border-radius:10px;background:#fff}}
.cell span{{position:absolute;bottom:4px;left:8px;font-size:11px;color:#8a929b}}
.sq{{width:160px;height:160px}} .sq svg{{width:130px;height:130px}} .v{{width:160px;height:160px}} .v svg{{max-width:140px;max-height:140px}}
.h{{width:230px;height:100px}} .h svg{{max-width:210px;max-height:76px}} .ic{{width:74px;height:74px;border:none}} .ic svg{{width:72px;height:72px}}
.sz{{display:flex;align-items:flex-end;gap:12px;padding:8px 10px;border:1px solid #eceeef;border-radius:10px;width:100%;flex-wrap:wrap}} .sz i{{display:inline-block}}
.sz em{{font-style:normal;font-size:11px;color:#8a929b;width:100%}} .eval{{margin:0}}
</style></head><body><main><h1>AgendAI — rodada 6: Raiz e Pena refinadas</h1>
<p class="sub">Ponte e Raiz (rodada 4) como referência · A, B e C são as alternativas desta rodada · fundo branco · Plus Jakarta Sans SemiBold, “AI” na cor e I serifado</p>
{body}</main></body></html>"""
open("rodada-6/05-apresentacao/comparativo-rodada-6.html", "w").write(html)
print("ok")
