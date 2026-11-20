"""Comparative technical sheet: construction, typography, light/dark, one-colour, strengths & limits."""
import os, re, base64

ROOT = "02-conceitos"
K, W = "#0A0F14", "#FFFFFF"


def inline(path, color=None):
    s = open(path).read()
    s = re.sub(r"<\?xml[^>]*>", "", s)
    s = re.sub(r'\swidth="[^"]+"\s+height="[^"]+"', ' width="100%" height="100%"', s, count=1)
    if color:
        s = s.replace(f'fill="{K}"', f'fill="{color}"')
    return s


C = [
    dict(k="A", dir="A-ligadura", name="Ligadura AI", tipo="Lettermark (monograma A+I)",
         ideia="Um A inclinado que só se completa com o I ao lado: de longe, uma letra; de perto, “AI”.",
         cons=["Inclinação única 3:2 (56,3°) em todas as diagonais", "Peso constante: 38 un. (haste e perna)",
               "Fenda de 14 un. separa o A do I", "Ponta do A com 4 un. de overshoot", "13 pontos de ancoragem"],
         tipo_txt="Sora SemiBold (600) em “Agend”; o “AI” é o próprio símbolo, desenhado na mesma altura de maiúscula.",
         fortes=["Mais original na comparação com concorrentes", "Nome e símbolo são a mesma peça",
                 "Excelente em 16 px e em uma cor", "Tecnológico sem clichê de IA"],
         limites=["A inclinação traz energia/velocidade — pode soar esportiva", "Duas formas de A na mesma palavra",
                  "“AI” é recorrente em marcas de IA: busca no INPI obrigatória"]),
    dict(k="B", dir="B-encaixe", name="Encaixe", tipo="Letterform em espaço negativo + contêiner",
         ideia="Um bloco dividido em módulos que se encaixam; as juntas entre eles desenham o A.",
         cons=["Quadrado arredondado 224 un., raio 56", "Canais de 24 un.; pernas a 25° da vertical",
               "Travessão na altura 172 (≈ 2/3)", "Quatro módulos: dois laterais, topo e base"],
         tipo_txt="Montserrat SemiBold (600), espaçamento −1,5 %, I com serifas retas para nunca ler “AgendAl”.",
         fortes=["Nasce pronto para ícone de app e favicon", "Muito estável em tamanhos mínimos",
                 "Transmite estrutura, gestão e solidez"],
         limites=["“Letra em bloco” é solução frequente em apps — menos memorável",
                  "Depende do contêiner para existir", "A ideia de módulos precisa ser explicada"]),
    dict(k="C", dir="C-pivo", name="Pivô", tipo="Letterform monolinear com eixo",
         ideia="Dois ponteiros articulados em um único ponto formam o A: o tempo organizado a partir de um centro.",
         cons=["Traços de 36 un. com terminais redondos", "Inclinação 2:5 (21,8° da vertical)",
               "Eixo: círculo de raio 26 com folga de 10", "Travessão de 30 un. (horizontais mais finas)"],
         tipo_txt="Manrope: “Agend” em Medium (500) e “AI” em ExtraBold (800), I serifado — diferenciação clara entre Agend e AI.",
         fortes=["O mais amigável e o mais legível como “A”", "Sugere tempo sem desenhar relógio ou calendário",
                 "Compasso = planejamento, precisão"],
         limites=["Pode ser lido como bonequinho (cabeça + pernas) ou como “Å”",
                  "Traço arredondado soa menos premium", "Menos distinto na tela de apps"]),
]


def card(c):
    d = f"{ROOT}/{c['dir']}"
    sym = f"{d}/{c['k']}-simbolo.svg"
    lock = f"{d}/{c['k']}-logotipo-horizontal.svg"
    cons = f"{d}/{c['k']}-construcao.svg"
    li = lambda xs: "".join(f"<li>{x}</li>" for x in xs)
    return f"""
<section class="c">
  <header><span class="tag">Conceito {c['k']}</span><h2>{c['name']}</h2><p class="tipo">{c['tipo']}</p>
  <p class="ideia">{c['ideia']}</p></header>
  <div class="row">
    <figure class="box light wide">{inline(lock)}<figcaption>Logomarca · fundo claro</figcaption></figure>
    <figure class="box dark wide">{inline(lock, W)}<figcaption>Logomarca · fundo escuro (invertida)</figcaption></figure>
  </div>
  <div class="row">
    <figure class="box light sq">{inline(sym)}<figcaption>Símbolo isolado</figcaption></figure>
    <figure class="box dark sq">{inline(sym, W)}<figcaption>Símbolo invertido</figcaption></figure>
    <figure class="box mid sq">{inline(sym, K)}<figcaption>Uma cor sobre cinza</figcaption></figure>
    <figure class="box light sq">{inline(cons)}<figcaption>Construção</figcaption></figure>
    <figure class="box light sizes"><div class="s">
      <span style="width:16px;height:16px">{inline(sym)}</span><span style="width:24px;height:24px">{inline(sym)}</span>
      <span style="width:32px;height:32px">{inline(sym)}</span><span style="width:48px;height:48px">{inline(sym)}</span></div>
      <figcaption>16 · 24 · 32 · 48 px</figcaption></figure>
  </div>
  <div class="txt">
    <div><h3>Construção</h3><ul>{li(c['cons'])}</ul></div>
    <div><h3>Tipografia</h3><p>{c['tipo_txt']}</p></div>
    <div><h3>Pontos fortes</h3><ul>{li(c['fortes'])}</ul></div>
    <div><h3>Limitações</h3><ul>{li(c['limites'])}</ul></div>
  </div>
</section>"""


html = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>AgendAI — ficha técnica dos conceitos</title>
<style>
:root{{--ink:#0A0F14;--mut:#5b6470;--bg:#f6f6f4}}
body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,-apple-system,"Segoe UI",Inter,sans-serif}}
main{{max-width:1240px;margin:0 auto;padding:40px 32px}}
h1{{font-size:30px;margin:0 0 4px}} .sub{{color:var(--mut);margin:0 0 28px}}
.c{{background:#fff;border:1px solid #e5e5e2;border-radius:16px;padding:28px;margin-bottom:28px}}
.tag{{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--mut)}}
h2{{margin:2px 0 0;font-size:26px}} .tipo{{margin:0;color:var(--mut)}} .ideia{{font-size:18px;margin:10px 0 18px}}
.row{{display:flex;gap:14px;margin-bottom:14px;flex-wrap:wrap}}
figure{{margin:0;border-radius:12px;position:relative;display:flex;align-items:center;justify-content:center;padding:18px 18px 34px}}
figcaption{{position:absolute;bottom:8px;left:12px;font-size:12px;color:var(--mut)}}
.dark figcaption{{color:#9aa3ad}}
.light{{background:#fff;border:1px solid #e7e7e4}} .dark{{background:#0A0F14}} .mid{{background:#d9dcdf}}
.wide{{flex:1 1 440px;height:150px}} .wide svg{{max-height:110px}}
.sq{{width:150px;height:150px}} .sq svg{{width:120px;height:120px}}
.sizes{{flex:1 1 200px;height:150px}} .s{{display:flex;align-items:flex-end;gap:16px}} .s span{{display:inline-block}}
.txt{{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}} .txt h3{{font-size:13px;letter-spacing:.08em;text-transform:uppercase;margin:6px 0}}
.txt ul{{margin:0;padding-left:18px}} .txt p{{margin:0}}
@media (max-width:900px){{.txt{{grid-template-columns:1fr 1fr}}}}
</style></head><body><main>
<h1>AgendAI — ficha técnica dos três conceitos</h1>
<p class="sub">Rodada 1 · preto e branco (a paleta Esmeralda Tech entra após a escolha) · todas as letras convertidas em curvas</p>
{''.join(card(c) for c in C)}
</main></body></html>"""
os.makedirs("04-apresentacao", exist_ok=True)
open("04-apresentacao/ficha-tecnica-conceitos.html", "w").write(html)
print("ok")
