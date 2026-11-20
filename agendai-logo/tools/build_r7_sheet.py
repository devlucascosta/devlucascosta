"""Round 7 — one comparison sheet, five directions (Raiz r4, Raiz + Pena r6, and three new)."""
import re
R = "rodada-7"
S = lambda k, sl, f: f"{R}/02-simbolos/{sl}/{k}-{f}.svg"
C = lambda pk, k, f: f"{R}/04-cores/{pk}/{k}-{f}.svg"
P = [
 ("R", "R-raiz-r4", "Raiz · rodada 4", "Curva esquerda que se abre até o chão; abertura recortada.",
  "Silhueta própria; firme em 16 px; uma cor.", "Acabamento ainda geométrico, pouco ‘humano’."),
 ("H", "H-raiz-pena-r6", "Raiz + Pena · rodada 6", "Estrutura da Raiz com lógica de pena: ápice a 45°, traço esquerdo que engrossa até o pé.",
  "Humana e elegante; silhueta reconhecível.", "Traço fino no alto pede cuidado < 16 px."),
 ("J", "J-raiz-pena-evoluida", "A · Raiz + Pena evoluída", "A mesma pena corta as duas pontas do traço principal: o ápice e o pé direito, ambos a 45°.",
  "A mais coerente: toda a letra obedece a uma só ferramenta; mais memorável.", "O corte do pé é sutil abaixo de 32 px; evolução, não ruptura."),
 ("K", "K-encontro", "B · Encontro (símbolo livre)", "Uma curva (quarto de círculo) e uma forma reta (quadrado) se tocam num único ponto: o compromisso marcado.",
  "Ícone de app sólido e simples; não depende da letra; conceito claro.", "Solto em 16–24 px parece um xadrez; geometria de tendência ‘Bauhaus/startup’; não remete ao nome."),
 ("L", "L-wordmark", "C · Wordmark AgendAI", "O nome é a marca: os dois A da palavra são desenhados na lógica da Raiz (pé que se abre em curva) e rimam entre si.",
  "Nome protagonista e inconfundível; assinatura discreta; o A vira o ícone.", "Mais longa para espaços pequenos; o detalhe pede tamanho de título para ser percebido."),
]


def inl(p):
    return re.sub(r'\swidth="[^"]+"\s+height="[^"]+"', ' width="100%" height="100%"', open(p).read(), count=1)


def cell(x, cls, cap=""):
    return f'<div class="cell {cls}">{inl(x)}{f"<span>{cap}</span>" if cap else ""}</div>'


def logo(k, sl, pk=None, dark=False):
    if k == "L":
        if pk is None: return cell(S(k, sl, "wordmark"), "w")
        return cell(C(pk, k, "wordmark-escuro" if dark else "wordmark"), "w")
    if pk is None: return cell(S(k, sl, "logotipo-vertical"), "v")
    return cell(C(pk, k, "horizontal-escuro"), "w") if dark else cell(C(pk, k, "vertical"), "v")


def sizes(k, sl):
    out = ""
    for src, lab in ((S(k, sl, "simbolo"), "uma cor"), (C("esmeralda", k, "icone-app"), "ícone")):
        out += '<div class="sz">' + "".join(f'<i style="width:{z}px;height:{z}px">{inl(src)}</i>' for z in (16, 24, 32, 64)) + f"<em>{lab} · 16 · 24 · 32 · 64</em></div>"
    return out


rows = [
 ("", [f"<h2>{n}</h2><p class='idea'>{i}</p>" for k, sl, n, i, f, l in P]),
 ("Símbolo", [cell(S(k, sl, "simbolo"), "sq", "A do wordmark" if k == "L" else "") for k, sl, *_ in P]),
 ("Logomarca · uma cor", [logo(k, sl) for k, sl, *_ in P]),
 ("Esmeralda Tech", [logo(k, sl, "esmeralda") for k, sl, *_ in P]),
 ("Preto e Dourado", [logo(k, sl, "dourado") for k, sl, *_ in P]),
 ("Fundo escuro", [logo(k, sl, "esmeralda", True) + logo(k, sl, "dourado", True) for k, sl, *_ in P]),
 ("Ícone de aplicativo", ["".join(cell(C(pk, k, f), "ic") for pk, f in (("esmeralda", "icone-app"), ("esmeralda", "icone-app-alt"), ("dourado", "icone-app"), ("dourado", "icone-app-alt"))) for k, sl, *_ in P]),
 ("16 · 24 · 32 · 64 px", [sizes(k, sl) for k, sl, *_ in P]),
 ("Pontos fortes", [f"<p>{f}</p>" for *_, f, l in P]),
 ("Limitações", [f"<p>{l}</p>" for *_, l in P]),
]
body = "".join(f'<div class="row"><div class="lab">{lab}</div>' + "".join(f'<div class="col">{c}</div>' for c in cols) + "</div>" for lab, cols in rows)
html = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>AgendAI — rodada 7</title><style>
body{{margin:0;background:#fff;color:#0A0F14;font:13.5px/1.5 system-ui,-apple-system,"Segoe UI",Inter,sans-serif}}
main{{max-width:1560px;margin:0 auto;padding:34px 26px}} h1{{font-size:28px;margin:0 0 4px}} .sub{{color:#5b6470;margin:0 0 22px}}
.row{{display:grid;grid-template-columns:92px repeat(5,1fr);gap:16px;padding:12px 0;border-top:1px solid #eceeef}}
.lab{{font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;color:#5b6470;padding-top:6px}}
.col{{display:flex;flex-wrap:wrap;gap:8px;align-content:flex-start}} h2{{margin:0;font-size:18px}} .idea{{margin:6px 0 0;color:#333}} p{{margin:0}}
.cell{{position:relative;display:flex;align-items:center;justify-content:center;border:1px solid #eceeef;border-radius:10px;background:#fff;overflow:hidden}}
.cell span{{position:absolute;bottom:3px;left:8px;font-size:10.5px;color:#8a929b}}
.sq{{width:150px;height:150px}} .sq svg{{width:124px;height:124px}} .v{{width:160px;height:160px}} .v svg{{max-width:140px;max-height:140px}}
.w{{width:100%;height:82px}} .w svg{{max-height:82px;max-width:100%}} .ic{{width:62px;height:62px;border:none}} .ic svg{{width:62px;height:62px}}
.sz{{display:flex;align-items:flex-end;gap:10px;padding:7px 9px;border:1px solid #eceeef;border-radius:10px;width:100%;flex-wrap:wrap}} .sz i{{display:inline-block}}
.sz em{{font-style:normal;font-size:10.5px;color:#8a929b;width:100%}}
</style></head><body><main><h1>AgendAI — rodada 7: cinco direções</h1>
<p class="sub">Raiz (r4) e Raiz + Pena (r6) como concorrentes · A, B e C são novas · fundo branco nas aplicações principais, com teste em fundo escuro · Plus Jakarta Sans SemiBold, “AI” na cor e I serifado</p>
{body}</main></body></html>"""
open(f"{R}/05-apresentacao/comparativo-rodada-7.html", "w").write(html)
print("ok")
