"""Round-2 comparison sheet: three proposals × two colour identities, app icons, small sizes, construction, type."""
import os, re

R = "rodada-2"
S = f"{R}/02-simbolos"
CO = f"{R}/04-cores"


def inline(path, size=None):
    s = open(path).read()
    s = re.sub(r"<\?xml[^>]*>", "", s)
    s = re.sub(r'\swidth="[^"]+"\s+height="[^"]+"', ' width="100%" height="100%"', s, count=1)
    return s


P = [
    dict(k="P01", slug="P01-traco", nome="Traço", sub="A com movimento",
         ideia="Duas pernas retas e um único traço curvo que nasce no pé esquerdo, atravessa a estrutura e sai pela perna direita, subindo — o gesto de quem anota e segue em frente.",
         cons=["Pernas de 30 un., ápice com raio 6", "Travessão = arco de circunferência único (3 pontos: 70,196 · 160,160 · 226,150), largura 26",
               "A curva sai 26 un. além da perna direita, com corte perpendicular", "Sem efeito: a curva é a própria estrutura da letra"],
         tipo="Instrument Sans Medium (500), −1,2 %, I com serifas curtas",
         fortes=["Movimento e evolução sem velocidade agressiva", "Traço humano, de 'assinatura'", "Reconhecível em 16 px pela saída da curva"],
         limites=["A curva saindo à direita pode lembrar a ideia de 'seta' (ex.: o A dos Vingadores) — sem flecha, mas vale a busca",
                  "Silhueta assimétrica pede mais respiro no ícone", "Ponta da curva fica fina em 16 px"]),
    dict(k="P02", slug="P02-arco", nome="Arco", sub="A contínuo",
         ideia="Uma única forma sólida, sem emendas: ápice macio, contraforma arredondada e uma abertura inferior em arco que dá leveza à base.",
         cons=["Silhueta triangular com ápice de raio 28", "Paredes de 35 un. (deslocamento constante do contorno)",
               "Contraforma com cantos de raio 8", "Abertura inferior com topo em arco de raio 24"],
         tipo="Plus Jakarta Sans Medium (500), −1,2 %, I com serifas curtas",
         fortes=["O mais calmo, estável e atemporal", "Excelente como bloco de cor no ícone", "Zero risco de leitura esportiva"],
         limites=["Em tamanhos pequenos vira um 'A negrito' genérico — os arcos somem", "Menos memorável e menos autoral", "Ao lado de 'AgendAI' pode soar como 'A AgendAI'"]),
    dict(k="P03", slug="P03-vela", nome="Vela", sub="Híbrido autoral",
         ideia="Um lado reto e firme, o outro curvo e aberto, como uma vela que recebe vento: organização e movimento na mesma letra, desenhada num traço só.",
         cons=["Lado esquerdo reto; lado direito = arco de circunferência com flecha de 38 un.", "Peso constante de 32 un. (deslocamento do contorno)",
               "Travessão reto entre 148 e 172 — o único elemento horizontal", "Ápice com raio 4: preciso, sem ponta agressiva"],
         tipo="DM Sans Medium (500), −1,2 %, I com serifas curtas",
         fortes=["Personalidade própria: não é um A de fonte, é um A desenhado", "Equilíbrio exato entre reto (ordem) e curvo (evolução)",
                 "Lê bem de 16 px a fachada; silhueta reconhecível sem o nome"],
         limites=["A assimetria exige alinhamento óptico cuidadoso nas composições", "Curva grande pode parecer 'D' em leituras muito rápidas (não ocorreu nos testes)", "Precisa ser redesenhado com arcos verdadeiros no arquivo final"]),
]
PAL = [("esmeralda", "Esmeralda Tech", "#FFFFFF", "#0A0F14"), ("dourado", "Preto e Dourado", "#F5F2E9", "#0D0D0D")]


def row_colour(p, pk, pname, light, dark):
    k = p["k"]
    return f"""
  <div class="pal"><h4>{pname}</h4>
    <div class="row">
      <figure class="wide" style="background:{light}">{inline(f'{CO}/{pk}/{k}-horizontal-claro.svg')}<figcaption>fundo claro</figcaption></figure>
      <figure class="wide" style="background:{dark}">{inline(f'{CO}/{pk}/{k}-horizontal-escuro.svg')}<figcaption class="d">fundo escuro</figcaption></figure>
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
.wide{{flex:1 1 330px;height:140px}} .wide svg{{max-height:96px}}
.sq{{width:140px;height:140px}} .sq svg{{width:100px;height:100px}}
.ic{{width:120px;height:140px;background:#eceeef}} .ic svg{{width:84px;height:84px}}
.sizes{{flex:0 1 210px;height:140px}} .s{{display:flex;align-items:flex-end;gap:14px}} .s span,td span{{display:inline-block}}
.txt{{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-top:16px}} .txt h3{{font-size:13px;letter-spacing:.08em;text-transform:uppercase;margin:6px 0}}
.txt ul{{margin:0;padding-left:18px}} .txt p{{margin:0}}
table.cmp{{border-collapse:separate;border-spacing:6px}} .cmp th{{font-size:12px;color:var(--mut);text-align:left;padding:0 8px}}
.cmp td{{background:#fff;border:1px solid #e7e7e4;border-radius:8px;width:84px;height:84px;text-align:center;vertical-align:middle}}
.note{{background:#fff8e6;border:1px solid #f0dfb0;border-radius:12px;padding:14px 18px;margin-bottom:28px}}
</style></head><body><main>
<h1>AgendAI — rodada 2: três novas propostas</h1>
<p class="sub">Mestres em preto e branco · mesma construção aplicada nas identidades Esmeralda Tech e Preto e Dourado · letras convertidas em curvas</p>
<div class="note"><b>Contraste (WCAG, elementos gráficos ≥ 3:1):</b> esmeralda #00A98F sobre branco = 2,97:1 · #00D1B2 sobre branco = 1,95:1 ·
dourado #D4AF5A sobre creme #F5F2E9 = 1,86:1. Sobre fundo escuro: #00D1B2 / grafite = 9,9:1 · dourado / preto = 9,3:1.
Conclusão: nas duas identidades a cor do símbolo funciona plenamente sobre fundo escuro; em fundo claro, a cor serve para tamanhos grandes e
o símbolo em grafite/preto deve ser usado nos tamanhos pequenos.</div>
{''.join(card(p) for p in P)}
{small_compare()}
</main></body></html>"""
os.makedirs(f"{R}/05-apresentacao", exist_ok=True)
open(f"{R}/05-apresentacao/comparativo-rodada-2.html", "w").write(html)
print("ok")
