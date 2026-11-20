"""Round 8 — one comparison page: Finalista A (wordmark) vs Finalista B (Raiz + Pena), equal conditions."""
import re

F = "rodada-8/02-finalistas"
A, B = f"{F}/A-wordmark", f"{F}/B-raiz-pena"


def inl(path, h=None, w=None):
    s = open(path).read()
    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s)
    vw, vh = float(vb.group(1)), float(vb.group(2))
    if h:
        w = h * vw / vh
    elif w:
        h = w * vh / vw
    return re.sub(r'\swidth="[^"]+"\s+height="[^"]+"', f' width="{w:.1f}" height="{h:.1f}"', s, count=1)


def pair(label, a, b, note=""):
    return (f'<section><h3>{label}</h3>{f"<p class=note>{note}</p>" if note else ""}'
            f'<div class="pair"><div class="c">{a}</div><div class="c">{b}</div></div></section>')


def card(x, cls=""):
    return f'<div class="card {cls}">{x}</div>'


def header(logo, accent_bg, accent_fg, nav_c="#4b5560"):
    return (f'<div class="hdr"><div class="lg">{logo}</div><nav style="color:{nav_c}">Agenda<span>Clientes</span><span>Financeiro</span><span>Relatórios</span></nav>'
            f'<b style="background:{accent_bg};color:{accent_fg}">Entrar</b></div>')


def icons(base):
    out = ""
    for pk, f in (("esmeralda", "icone"), ("esmeralda", "icone-alt"), ("dourado", "icone"), ("dourado", "icone-alt"), ("mono", "icone")):
        k = base.split("/")[-1][0]
        out += f'<i>{inl(f"{base}/{pk}/{k}-{f}.svg", h=76)}</i>'
    return out


def small(base, logo_file, k):
    s = '<div class="row">' + "".join(f'<i class="lbl">{inl(f"{base}/mono/{logo_file}", h=hh)}<em>{hh}px</em></i>' for hh in (40, 28, 20)) + "</div>"
    s += '<div class="row">' + "".join(f'<i class="lbl">{inl(f"{base}/esmeralda/{k}-icone.svg", h=z)}<em>{z}</em></i>' for z in (16, 24, 32, 64))
    s += "".join(f'<i class="lbl">{inl(f"{base}/mono/{k}-{"letra" if k == "A" else "simbolo"}.svg", h=z)}<em>{z}</em></i>' for z in (16, 24, 32)) + "</div>"
    s += (f'<div class="tab">{inl(f"{base}/esmeralda/{k}-icone.svg", h=16)}<span>AgendAI — Agenda</span></div>')
    return s


crit = [
    ("Originalidade", "Bom — a rima dos dois A é própria, mas discreta.", "Forte — silhueta que não existe em outra marca."),
    ("Personalidade", "Contida, editorial.", "Marcante: curva + pena dão caráter imediato."),
    ("Elegância", "Muito alta — sóbria, sem excesso.", "Alta — o contraste de pena é refinado."),
    ("Naturalidade", "Alta — parece uma fonte desenhada para a marca.", "Alta — gesto caligráfico com lógica real de pena."),
    ("Legibilidade", "Máxima: o nome está sempre escrito.", "Nome legível no lockup; símbolo lido como A."),
    ("Reconhecimento", "O nome é a assinatura; o A do ícone é o mesmo da palavra e passa a ser reconhecido por ela.", "Forte: o símbolo se reconhece sozinho; o nome ao lado repete o A (“A AgendAI”)."),
    ("Ícone de app", "Praticamente igual ao B (mesmo A, ~10% mais leve).", "Ligeiramente mais cheio; contraste de pena mais visível."),
    ("Versatilidade", "Wordmark + A; poucos arranjos (sempre horizontal).", "Horizontal, vertical, símbolo isolado, avatar, favicon."),
    ("Reprodução", "Simples; detalhe dos A some abaixo de ~24 px de altura.", "Simples (13 pontos); traço fino do ápice pede ≥ 16 px."),
    ("Longo prazo / SaaS multissegmento", "Neutro e atemporal; serve a qualquer segmento.", "Neutro (é um A, não transporte); constrói um ativo visual próprio."),
]


def main():
    sec = []
    sec.append(pair("1 · Logomarca completa (mesma altura de maiúscula: 64 un.)",
                    card(inl(f"{A}/mono/A-wordmark.svg", h=150), "big"),
                    card(inl(f"{B}/mono/B-horizontal.svg", h=150), "big") + card(inl(f"{B}/mono/B-vertical.svg", h=190), "big")))
    sec.append(pair("2 · Símbolo / letra isolada",
                    card(inl(f"{A}/mono/A-letra.svg", h=200), "sq"), card(inl(f"{B}/mono/B-simbolo.svg", h=200), "sq"),
                    "Os dois são o mesmo A (curva da Raiz + corte de pena); o do wordmark tem peso de texto. A decisão real é de sistema: o A dentro do nome (A) ou ao lado do nome (B)."))
    sec.append(pair("3 · Ícone de aplicativo (Esmeralda, Esmeralda alt., Dourado, Dourado alt., uma cor)",
                    f'<div class="row">{icons(A)}</div>', f'<div class="row">{icons(B)}</div>'))
    sec.append(pair("4 · Cabeçalho do AgendAI SaaS",
                    header(inl(f"{A}/esmeralda/A-wordmark.svg", h=56), "#00D1B2", "#0A0F14") + header(inl(f"{A}/dourado/A-wordmark.svg", h=56), "#D4AF5A", "#0D0D0D"),
                    header(inl(f"{B}/esmeralda/B-horizontal.svg", h=56), "#00D1B2", "#0A0F14") + header(inl(f"{B}/dourado/B-horizontal.svg", h=56), "#D4AF5A", "#0D0D0D")))
    sec.append(pair("5 · Tamanho reduzido (logo a 40/28/20 px de altura · ícone 16–64 · letra/símbolo 16–32 · aba do navegador)",
                    small(A, "A-wordmark.svg", "A"), small(B, "B-horizontal.svg", "B")))
    sec.append(pair("6 · Uma única cor (preto e invertido)",
                    card(inl(f"{A}/mono/A-wordmark.svg", h=96)) + card(inl(f"{A}/mono/A-wordmark-invertido.svg", h=96), "dk"),
                    card(inl(f"{B}/mono/B-horizontal.svg", h=96)) + card(inl(f"{B}/mono/B-horizontal-invertido.svg", h=96), "dk")))
    sec.append(pair("7 · Esmeralda Tech (fundo branco)",
                    card(inl(f"{A}/esmeralda/A-wordmark.svg", h=120)), card(inl(f"{B}/esmeralda/B-horizontal.svg", h=120)) + card(inl(f"{B}/esmeralda/B-vertical.svg", h=170))))
    sec.append(pair("8 · Preto e Dourado (fundo branco)",
                    card(inl(f"{A}/dourado/A-wordmark.svg", h=120)), card(inl(f"{B}/dourado/B-horizontal.svg", h=120)) + card(inl(f"{B}/dourado/B-vertical.svg", h=170))))
    rows = "".join(f"<tr><th>{c}</th><td>{a}</td><td>{b}</td></tr>" for c, a, b in crit)
    sec.append(f'<section><h3>9 · Avaliação</h3><table><tr><th></th><th>A · Wordmark</th><th>B · Raiz + Pena</th></tr>{rows}</table></section>')
    html = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>AgendAI — rodada 8</title><style>
body{{margin:0;background:#fff;color:#0A0F14;font:14px/1.5 system-ui,-apple-system,"Segoe UI",Inter,sans-serif}}
main{{max-width:1320px;margin:0 auto;padding:34px 28px}} h1{{font-size:28px;margin:0}} .sub{{color:#5b6470;margin:4px 0 18px}}
.heads{{display:grid;grid-template-columns:1fr 1fr;gap:28px;position:sticky;top:0;background:#fff;padding:10px 0;border-bottom:2px solid #0A0F14;z-index:2}}
.heads h2{{margin:0;font-size:20px}} .heads p{{margin:2px 0 0;color:#5b6470;font-size:13px}}
section{{padding:16px 0;border-bottom:1px solid #eceeef}} h3{{margin:0 0 10px;font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:#5b6470}}
.note{{margin:-6px 0 10px;color:#5b6470;font-size:12.5px}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:28px}} .c{{display:flex;flex-direction:column;gap:10px}}
.card{{border:1px solid #eceeef;border-radius:12px;padding:14px;display:flex;justify-content:center;align-items:center;background:#fff}}
.card.dk{{background:#0A0F14;border-color:#0A0F14;padding:0;overflow:hidden}} .card svg{{max-width:100%;height:auto}}
.sq{{height:230px}} .row{{display:flex;gap:14px;align-items:flex-end;flex-wrap:wrap}} .row i{{display:flex;flex-direction:column;align-items:center;gap:4px}}
.lbl em{{font-style:normal;font-size:11px;color:#8a929b}}
.hdr{{display:flex;align-items:center;gap:18px;border:1px solid #e6e8ea;border-radius:12px;padding:6px 16px;background:#fff;box-shadow:0 1px 2px rgba(0,0,0,.04)}}
.hdr .lg{{flex:none;display:flex}} .hdr nav{{flex:1;font-size:14px}} .hdr nav span{{margin-left:18px}}
.hdr b{{font-weight:600;font-size:13.5px;padding:8px 14px;border-radius:8px}}
.tab{{display:flex;align-items:center;gap:8px;background:#eef0f2;border-radius:10px 10px 0 0;padding:8px 12px;width:240px;font-size:12.5px}}
table{{border-collapse:collapse;width:100%}} th,td{{text-align:left;vertical-align:top;padding:8px 10px;border-bottom:1px solid #eceeef}} th{{width:200px;color:#5b6470;font-weight:600}}
</style></head><body><main><h1>AgendAI — rodada 8: as duas finalistas</h1>
<p class="sub">Mesma escala, mesma renderização, fundo branco · contornos com arcos e Béziers reais · Plus Jakarta Sans SemiBold · “AI” na cor e I serifado nas duas</p>
<div class="heads"><div><h2>A · Wordmark AgendAI</h2><p>O nome é a marca; os dois A são desenhados (curva da Raiz, corte de pena) e o A vira o ícone.</p></div>
<div><h2>B · Raiz + Pena</h2><p>Símbolo independente caligráfico (ápice a 45°, traço que engrossa até o pé) + nome.</p></div></div>
{''.join(sec)}</main></body></html>"""
    open("rodada-8/05-apresentacao/comparativo-final.html", "w").write(html)
    print("ok")


if __name__ == "__main__":
    import os
    os.makedirs("rodada-8/05-apresentacao", exist_ok=True)
    main()
