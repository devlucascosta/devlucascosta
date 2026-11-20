"""Round-2 comparison sheet: three proposals × two colour identities, app icons, small sizes, construction, type."""
import os, re

R = "rodada-3"
S = f"{R}/02-simbolos"
CO = f"{R}/04-cores"


def inline(path, size=None):
    s = open(path).read()
    s = re.sub(r"<\?xml[^>]*>", "", s)
    s = re.sub(r'\swidth="[^"]+"\s+height="[^"]+"', ' width="100%" height="100%"', s, count=1)
    return s


P = [
    dict(k="01", slug="01-ponte", nome="Ponte", sub="inspirada na referência 02",
         ideia="A perna esquerda pousa sobre um arco que nasce no chão e passa por trás da perna direita: a curva sustenta a letra, como uma ponte que liga tudo.",
         cons=["A de topo reto (36 un.) com pernas contrastadas: 34 un. à esquerda, 46 un. à direita", "Arco único de circunferência (largura 26) que nasce abaixo da linha de base",
               "Na frente da perna esquerda, por trás da direita: folgas de 7 un. criam profundidade sem degradê", "Dois tons chapados: corpo e curva"],
         tipo="Plus Jakarta Sans SemiBold (600), em pé, −1,5 %; “AI” na cor de destaque e I com serifas curtas",
         fortes=["A mais fiel ao que você gostou na referência 02, só que plana e mais limpa", "Curva estrutural: sem ela a letra não fica de pé",
                 "Elegante e calma; boa nos dois tons"],
         limites=["Em 16 px o arco vira um “pé alongado” — funciona, mas perde a ideia", "Duas folgas finas pedem cuidado em bordado e gravação",
                  "Silhueta mais larga embaixo à esquerda (pede alinhamento óptico)"]),
    dict(k="02", slug="02-impulso", nome="Impulso", sub="inspirada na referência 01",
         ideia="Uma faixa macia sai de trás da perna esquerda, passa na frente da direita e sobe: o movimento atravessa a letra, mas sem lâmina afiada.",
         cons=["Mesmo A de topo reto e pernas contrastadas", "Faixa num arco único, afinando de 26 para 12 un. (nunca chega a ponta)",
               "Por trás da perna esquerda, na frente da direita (folgas de 7 un.)", "A faixa ultrapassa a perna direita em ~24 un."],
         tipo="Plus Jakarta Sans SemiBold (600), em pé, −1,5 %; “AI” na cor de destaque e I com serifas curtas",
         fortes=["A mais dinâmica — “evolução” lida de imediato", "Mais próxima do clima da referência 01", "Ótimo contraste de dois tons no ícone"],
         limites=["É a que mais se aproxima de marcas esportivas (faixa ascendente afinando)", "Em 16 px a faixa se funde com a letra",
                  "Detalhe mais complexo (204 pontos no rascunho)"]),
    dict(k="03", slug="03-recorte", nome="Recorte", sub="síntese autoral",
         ideia="Um A maciço em que a curva não é adicionada — é recortada. O pé esquerdo “decola” do chão: movimento feito de espaço, não de efeito.",
         cons=["Mesmo A de topo reto e pernas contrastadas, em bloco único", "Um só arco de circunferência define a base do travessão e corta o pé esquerdo",
               "Contraforma triangular reta acima — reto em cima, curvo embaixo", "Uma cor, 69 pontos: a construção mais simples das três"],
         tipo="Plus Jakarta Sans SemiBold (600), em pé, −1,5 %; “AI” na cor de destaque e I com serifas curtas",
         fortes=["A mais forte como ícone: massa sólida, lida em 16 px", "Curva integrada de verdade (é a própria forma)", "Discreta, atemporal, sem risco esportivo; fácil de bordar, gravar e recortar"],
         limites=["Perde os dois tons das referências (é monocromática por natureza)", "Mais contida: o movimento é sutil",
                  "O pé esquerdo suspenso precisa de alinhamento óptico com o texto"]),
]
PAL = [("esmeralda", "Esmeralda Tech", "#FFFFFF", "#0A0F14"), ("dourado", "Preto e Dourado", "#F5F2E9", "#0D0D0D")]


def row_colour(p, pk, pname, light, dark):
    k = p["k"]
    return f"""
  <div class="pal"><h4>{pname}</h4>
    <div class="row">
      <figure class="wide" style="background:{light}">{inline(f'{CO}/{pk}/{k}-vertical-claro.svg')}<figcaption>vertical · claro</figcaption></figure>
      <figure class="wide" style="background:{dark}">{inline(f'{CO}/{pk}/{k}-vertical-escuro.svg')}<figcaption class="d">vertical · escuro</figcaption></figure>
      <figure class="wide" style="background:{dark}">{inline(f'{CO}/{pk}/{k}-horizontal-escuro.svg')}<figcaption class="d">horizontal · escuro</figcaption></figure>
      <figure class="ic">{inline(f'{CO}/{pk}/{k}-icone-app.svg')}<figcaption>ícone</figcaption></figure>
      <figure class="ic">{inline(f'{CO}/{pk}/{k}-icone-app-alt.svg')}<figcaption>ícone alt.</figcaption></figure>
      <figure class="sizes" style="background:{dark}"><div class="s">
        {''.join(f'<span style="width:{z}px;height:{z}px">{inline(f"{CO}/{pk}/{k}-icone-app.svg")}</span>' for z in (16, 32, 64))}
      </div><figcaption class="d">ícone 16 · 32 · 64 px</figcaption></figure>
    </div></div>"""


def card(p):
    k, d = p["k"], f"{S}/{p['slug']}"
    li = lambda xs: "".join(f"<li>{x}</li>" for x in xs)
    sizes = "".join(f'<span style="width:{z}px;height:{z}px">{inline(f"{d}/{k}-simbolo.svg")}</span>' for z in (16, 32, 64))
    return f"""
<section class="c">
  <header><span class="tag">Proposta {k[1:]} · {p['sub']}</span><h2>{p['nome']}</h2><p class="ideia">{p['ideia']}</p></header>
  <div class="row">
    <figure class="sq w">{inline(f'{d}/{k}-simbolo.svg')}<figcaption>símbolo isolado (mestre P&amp;B)</figcaption></figure>
    <figure class="sq w">{inline(f'{d}/{k}-construcao.svg')}<figcaption>construção</figcaption></figure>
    <figure class="wide w">{inline(f'{d}/{k}-logotipo-horizontal.svg')}<figcaption>logomarca completa · horizontal</figcaption></figure>
    <figure class="sq w">{inline(f'{d}/{k}-logotipo-vertical.svg')}<figcaption>vertical</figcaption></figure>
    <figure class="sizes w"><div class="s">{sizes}</div><figcaption>16 · 32 · 64 px (monocromático)</figcaption></figure>
  </div>
  {''.join(row_colour(p, *x) for x in PAL)}
  <div class="txt">
    <div><h3>Construção</h3><ul>{li(p['cons'])}</ul></div>
    <div><h3>Tipografia</h3><p>{p['tipo']}</p></div>
    <div><h3>Pontos fortes</h3><ul>{li(p['fortes'])}</ul></div>
    <div><h3>Limitações</h3><ul>{li(p['limites'])}</ul></div>
  </div>
</section>"""


def small_compare():
    cells = ""
    for p in P:
        k, d = p["k"], f"{S}/{p['slug']}"
        cells += f"<tr><th>{k} {p['nome']}</th>"
        for z in (16, 32, 64):
            cells += f'<td><span style="width:{z}px;height:{z}px">{inline(f"{d}/{k}-simbolo.svg")}</span></td>'
        for pk, _, light, dark in PAL:
            for z in (16, 32, 64):
                cells += f'<td style="background:{dark}"><span style="width:{z}px;height:{z}px">{inline(f"{CO}/{pk}/{k}-simbolo-cor.svg")}</span></td>'
        cells += "</tr>"
    head = "<tr><th></th>" + "".join(f"<th>P&amp;B {z}</th>" for z in (16, 32, 64)) + \
           "".join(f"<th>{n.split()[0]} {z}</th>" for _, n, _, _ in PAL for z in (16, 32, 64)) + "</tr>"
    return f'<section class="c"><h2>Comparação em tamanhos reduzidos</h2><table class="cmp">{head}{cells}</table></section>'


html = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>AgendAI — rodada 2</title>
<style>
:root{{--ink:#0A0F14;--mut:#5b6470}}
body{{margin:0;background:#f4f4f2;color:var(--ink);font:15px/1.5 system-ui,-apple-system,"Segoe UI",Inter,sans-serif}}
main{{max-width:1280px;margin:0 auto;padding:40px 32px}}
h1{{font-size:30px;margin:0 0 4px}} .sub{{color:var(--mut);margin:0 0 28px}}
.c{{background:#fff;border:1px solid #e5e5e2;border-radius:16px;padding:28px;margin-bottom:28px}}
.tag{{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--mut)}}
h2{{margin:2px 0 6px;font-size:26px}} .ideia{{font-size:17px;margin:4px 0 18px;max-width:900px}}
h4{{margin:14px 0 8px;font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:var(--mut)}}
.row{{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:6px}}
figure{{margin:0;border-radius:12px;position:relative;display:flex;align-items:center;justify-content:center;padding:14px 14px 30px;box-sizing:border-box}}
figure.w{{background:#fff;border:1px solid #e7e7e4}}
figcaption{{position:absolute;bottom:7px;left:12px;font-size:11.5px;color:var(--mut)}} figcaption.d{{color:#9aa3ad}}
.wide{{flex:1 1 230px;height:170px}} .wide svg{{max-height:130px}}
.sq{{width:140px;height:140px}} .sq svg{{width:100px;height:100px}}
.ic{{width:120px;height:140px;background:#eceeef}} .ic svg{{width:84px;height:84px}}
.sizes{{flex:0 1 210px;height:140px}} .s{{display:flex;align-items:flex-end;gap:14px}} .s span,td span{{display:inline-block}}
.txt{{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-top:16px}} .txt h3{{font-size:13px;letter-spacing:.08em;text-transform:uppercase;margin:6px 0}}
.txt ul{{margin:0;padding-left:18px}} .txt p{{margin:0}}
table.cmp{{border-collapse:separate;border-spacing:6px}} .cmp th{{font-size:12px;color:var(--mut);text-align:left;padding:0 8px}}
.cmp td{{background:#fff;border:1px solid #e7e7e4;border-radius:8px;width:84px;height:84px;text-align:center;vertical-align:middle}}
.note{{background:#fff8e6;border:1px solid #f0dfb0;border-radius:12px;padding:14px 18px;margin-bottom:28px}}
</style></head><body><main>
<h1>AgendAI — rodada 3: a partir das suas referências</h1>
<p class="sub">Construção própria inspirada nas referências 01 e 02 · cores chapadas (sem degradê) · mesma construção nas duas identidades · letras em curvas</p>
<div class="note"><b>Cores:</b> em fundo escuro o símbolo usa os dois verdes (corpo #00A98F, curva #00D1B2) ou os dois dourados (#D4AF5A / #E7CA82); em fundo claro o corpo vai para grafite/preto e a curva para o verde #00A98F (ou dourado escurecido #B8913A, ajuste necessário porque o dourado original some no creme). <b>Contraste (WCAG, elementos gráficos ≥ 3:1):</b> esmeralda #00A98F sobre branco = 2,97:1 · #00D1B2 sobre branco = 1,95:1 ·
dourado #D4AF5A sobre creme #F5F2E9 = 1,86:1. Sobre fundo escuro: #00D1B2 / grafite = 9,9:1 · dourado / preto = 9,3:1.
Conclusão: nas duas identidades a cor do símbolo funciona plenamente sobre fundo escuro; em fundo claro, a cor serve para tamanhos grandes e
o símbolo em grafite/preto deve ser usado nos tamanhos pequenos.</div>
{''.join(card(p) for p in P)}
{small_compare()}
</main></body></html>"""
os.makedirs(f"{R}/05-apresentacao", exist_ok=True)
open(f"{R}/05-apresentacao/comparativo-rodada-3.html", "w").write(html)
print("ok")
