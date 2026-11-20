"""Round 9 — the approved wordmark in real applications, Esmeralda Tech vs Preto e Dourado, side by side.
Reuses the round-8 masters (WA geometry, true-arc writer, font pipeline). No structural change to the wordmark."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from build_r8 import WA, fit, slab_I, p, FONT, WT, icon as icon_body
from glyphs import text_path
from geo import fmt

OUT = "rodada-9"


# ---------------------------------------------------------------- contrast
def _lum(h):
    h = h.lstrip("#"); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def cr(a, b):
    x, y = _lum(a), _lum(b); return (max(x, y) + 0.05) / (min(x, y) + 0.05)


# ---------------------------------------------------------------- brand marks (inline SVG)
def wordmark_svg(c_agend, c_ai, h, c_first=None, title="AgendAI"):
    cap, base, x0 = 100, 112, 6
    out = ""
    dA, wA = fit(WA, cap, x0, base - cap); out += p(dA, c_first or c_agend)
    d, w, boxes = text_path("gend", FONT, WT, cap, x=x0 + wA + 0.035 * cap - 0.059 * cap, baseline=base, tracking=-0.012)
    out += f'<path fill="{c_agend}" d="{d}"/>'
    xa = boxes[-1][3] + 0.055 * cap
    dA2, wA2 = fit(WA, cap, xa, base - cap); out += p(dA2, c_ai)
    dI, wI = slab_I(cap, base, xa + wA2 + 0.05 * cap); out += p(dI, c_ai)
    W, H = xa + wA2 + 0.05 * cap + wI + x0, 142
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fmt(W)} {H}" height="{h}" width="{fmt(h * W / H)}" '
            f'role="img" aria-label="{title}">{out}</svg>')


def a_svg(fill, h):
    d, w = fit(WA, 200, 0, 0)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-4 -4 {fmt(w + 8)} 208" height="{h}" width="{fmt(h * (w + 8) / 208)}">{p(d, fill)}</svg>'


def icon_svg(tile, fill, size, radius=True):
    body = icon_body(WA, tile, fill)
    if not radius:
        body = body.replace('rx="57.3"', 'rx="0"')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="{size}" height="{size}">{body}</svg>'


def avatar_svg(tile, fill, size):
    d, w = fit(WA, 116, 0, 0)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="{size}" height="{size}"><circle cx="128" cy="128" r="128" fill="{tile}"/>'
            f'<g transform="translate({fmt(128 - w / 2)} {fmt(128 - 58 - 3)})">{p(d, fill)}</g></svg>')


# ---------------------------------------------------------------- palettes (UI tokens derived only from each palette)
PAL = {
 "esmeralda": dict(nome="Esmeralda Tech", primary="#00D1B2", second="#00A98F", ink="#0A0F14", white="#FFFFFF",
   light=dict(bg="#FFFFFF", surf="rgba(10,15,20,.04)", line="rgba(10,15,20,.10)", ink="#0A0F14", mut="rgba(10,15,20,.58)",
              agend="#0A0F14", ai="#00A98F", accent="#00A98F", btn_bg="#0A0F14", btn_fg="#FFFFFF", chip="rgba(0,169,143,.12)", chip_fg="#00775F"[0:0] or "#0A0F14"),
   dark=dict(bg="#0A0F14", surf="rgba(255,255,255,.05)", line="rgba(255,255,255,.10)", ink="#FFFFFF", mut="rgba(255,255,255,.62)",
             agend="#FFFFFF", ai="#00D1B2", accent="#00D1B2", btn_bg="#00D1B2", btn_fg="#0A0F14", chip="rgba(0,209,178,.14)", chip_fg="#00D1B2"),
   icon=("#0A0F14", "#00D1B2"), icon_alt=("#00D1B2", "#0A0F14"), icon_dark=("#000000", "#00D1B2")),
 "dourado": dict(nome="Preto e Dourado", primary="#D4AF5A", second="#E7CA82", ink="#0D0D0D", white="#F5F2E9",
   light=dict(bg="#F5F2E9", surf="rgba(13,13,13,.04)", line="rgba(13,13,13,.10)", ink="#0D0D0D", mut="rgba(13,13,13,.58)",
              agend="#0D0D0D", ai="#0D0D0D", accent="#0D0D0D", btn_bg="#0D0D0D", btn_fg="#D4AF5A", chip="rgba(212,175,90,.22)", chip_fg="#0D0D0D"),
   dark=dict(bg="#0D0D0D", surf="rgba(245,242,233,.05)", line="rgba(245,242,233,.10)", ink="#F5F2E9", mut="rgba(245,242,233,.62)",
             agend="#F5F2E9", ai="#D4AF5A", accent="#D4AF5A", btn_bg="#D4AF5A", btn_fg="#0D0D0D", chip="rgba(212,175,90,.16)", chip_fg="#E7CA82"),
   icon=("#0D0D0D", "#D4AF5A"), icon_alt=("#D4AF5A", "#0D0D0D"), icon_dark=("#000000", "#D4AF5A")),
}
PAL["esmeralda"]["light"]["chip_fg"] = "#0A0F14"


# ---------------------------------------------------------------- 1. colour-composition study
def study(pk):
    P = PAL[pk]
    if pk == "esmeralda":
        rows = [("Agend grafite + AI #00A98F", "#FFFFFF", "#0A0F14", "#00A98F", None, "Recomendada (claro)"),
                ("Agend grafite + AI #00D1B2", "#FFFFFF", "#0A0F14", "#00D1B2", None, "AI some no branco"),
                ("Dois verdes: #00A98F + #00D1B2", "#FFFFFF", "#00A98F", "#00D1B2", None, "Fraco no branco"),
                ("Agend branco + AI #00D1B2", "#0A0F14", "#FFFFFF", "#00D1B2", None, "Recomendada (escuro)"),
                ("Dois verdes no grafite", "#0A0F14", "#00A98F", "#00D1B2", None, "Bom, menos nítido"),
                ("A inicial verde + texto grafite", "#FFFFFF", "#0A0F14", "#0A0F14", "#00A98F", "Alternativa sóbria")]
    else:
        rows = [("Agend preto + AI dourado", "#F5F2E9", "#0D0D0D", "#D4AF5A", None, "AI some no creme"),
                ("Tudo preto (dourado só no ícone)", "#F5F2E9", "#0D0D0D", "#0D0D0D", None, "Recomendada (claro)"),
                ("Dourado predominante + detalhe preto", "#F5F2E9", "#D4AF5A", "#0D0D0D", None, "Reprovada: ilegível"),
                ("Agend creme + AI dourado", "#0D0D0D", "#F5F2E9", "#D4AF5A", None, "Recomendada (escuro)"),
                ("Dourado predominante no preto", "#0D0D0D", "#D4AF5A", "#F5F2E9", None, "Excelente, mais ‘luxo’"),
                ("A inicial dourado + texto preto", "#F5F2E9", "#0D0D0D", "#0D0D0D", "#D4AF5A", "A some no creme")]
    cells = ""
    for name, bg, ca, cai, cf, verdict in rows:
        worst = min(cr(ca, bg), cr(cai, bg), cr(cf, bg) if cf else 99)
        ok = "ok" if worst >= 3 else ("warn" if worst >= 2.5 else "bad")
        cells += (f'<div class="sw" style="background:{bg}">{wordmark_svg(ca, cai, 40, cf)}'
                  f'<div class="swl"><b>{name}</b><span class="{ok}">{verdict} · menor contraste {worst:.1f}:1</span></div></div>')
    return f'<div class="study">{cells}</div>'


# ---------------------------------------------------------------- 2. app icons
GREYS = ["#d9dce0", "#c7ccd2", "#b5bcc4", "#e4e1db", "#cfd6d4", "#d8d2c8", "#bfc6cf", "#e0e3e7"]


def home_grid(P, dark):
    tiles = ""
    for i in range(12):
        if i == 5:
            t, f = (P["icon_dark"] if dark else P["icon"])
            tiles += f'<div class="app">{icon_svg(t, f, 46)}<em>AgendAI</em></div>'
        else:
            g = GREYS[i % len(GREYS)] if not dark else ["#2a2d31", "#33373c", "#3b3f45", "#2f3236"][i % 4]
            tiles += f'<div class="app"><i style="background:{g}"></i><em>App</em></div>'
    return tiles


def icons(pk):
    P = PAL[pk]
    tinted = icon_svg("#1c1c1e", "#c9c9c9", 64)
    sizes = "".join(f'<span class="szb">{icon_svg(*P["icon"], z)}<em>{z}</em></span>' for z in (20, 29, 40, 60, 120))
    return (f'<div class="row">'
            f'<span class="szb">{icon_svg(*P["icon"], 96)}<em>padrão</em></span>'
            f'<span class="szb">{icon_svg(*P["icon_alt"], 96)}<em>alternativo</em></span>'
            f'<span class="szb">{icon_svg(*P["icon_dark"], 96)}<em>iOS escuro</em></span>'
            f'<span class="szb">{icon_svg("#2c2c2e", "#d8d8d8", 96)}<em>iOS tingido</em></span>'
            f'<span class="szb bgk" style="background:{P["dark"]["bg"]}">{a_svg(P["primary"], 84)}<em>A isolado (escuro)</em></span>'
            f'<span class="szb">{a_svg(P["ink"], 96)}<em>A em uma cor</em></span></div>'
            f'<div class="row">{sizes}<span class="szb">{a_svg(P["ink"], 16)}<em>16</em></span><span class="szb">{a_svg(P["ink"], 24)}<em>24</em></span></div>'
            f'<div class="row homes"><div class="home lt">{home_grid(P, False)}</div><div class="home dk">{home_grid(P, True)}</div></div>')


# ---------------------------------------------------------------- 3. iPhone app light / dark
def phone_app(P, mode):
    T = P[mode]
    rows = "".join(f'<div class="li" style="border-color:{T["line"]}"><b style="color:{T["ink"]}">{h}</b><span style="color:{T["mut"]}">{s}</span>'
                   f'<i style="background:{T["chip"]};color:{T["chip_fg"]}">{tag}</i></div>'
                   for h, s, tag in (("09:30 · Reunião com cliente", "Av. Paulista, 1000", "Hoje"),
                                     ("13:00 · Corrida executiva", "Aeroporto → Centro", "R$ 180")))
    return (f'<div class="phone"><div class="scr" style="background:{T["bg"]}">'
            f'<div class="sb" style="color:{T["ink"]}">9:41</div>'
            f'<div class="ph">{wordmark_svg(T["agend"], T["ai"], 22)}<span style="background:{T["surf"]};color:{T["ink"]}">LV</span></div>'
            f'<div class="kpi" style="background:{T["surf"]}"><span style="color:{T["mut"]}">Receita da semana</span><b style="color:{T["ink"]}">R$ 3.840</b>'
            f'<div class="bars">{"".join(f"<i style=\"height:{h}%;background:{T["accent"] if j == 4 else T["line"]}\"></i>" for j, h in enumerate((40, 65, 50, 80, 95, 55, 70)))}</div></div>'
            f'<div class="sec" style="color:{T["mut"]}">Agenda de hoje</div>{rows}'
            f'<div class="fab" style="background:{T["btn_bg"]};color:{T["btn_fg"]}">+ Novo agendamento</div>'
            f'<div class="tab" style="border-color:{T["line"]}">{"".join(f"<span style=\"color:{T["accent"] if k == 0 else T["mut"]}\">{t}</span>" for k, t in enumerate(("Agenda", "Clientes", "Finanças", "Mais")))}</div>'
            f'</div></div>')


def phone_home(P, dark):
    return f'<div class="phone"><div class="scr hs {"dk" if dark else "lt"}"><div class="sb">9:41</div><div class="grid">{home_grid(P, dark)}</div></div></div>'


# ---------------------------------------------------------------- 4. Instagram
def instagram(P):
    T = P["dark"]
    promo = (f'<div class="post promo" style="background:{T["bg"]}">{wordmark_svg(T["agend"], T["ai"], 30)}'
             f'<p style="color:{T["ink"]}">Agenda, clientes e financeiro<br>em um só lugar.</p>'
             f'<span style="background:{T["btn_bg"]};color:{T["btn_fg"]}">Conheça</span></div>')
    lightpost = (f'<div class="post" style="background:{P["light"]["bg"]}">{a_svg(P["light"]["ink"], 58)}</div>')
    detail = f'<div class="post" style="background:{T["bg"]}">{a_svg(T["accent"], 58)}</div>'
    return (f'<div class="ig"><div class="igh">{avatar_svg(*P["icon"], 74)}<div><b>agendai.app</b><span>AgendAI</span>'
            f'<small>Gestão profissional e operacional em um só lugar.</small></div></div>'
            f'<div class="igs"><span>{avatar_svg(*P["icon"], 44)}<em>44</em></span><span>{avatar_svg(*P["icon"], 32)}<em>32</em></span>'
            f'<span>{avatar_svg(*P["icon"], 24)}<em>24</em></span><span>{avatar_svg(*P["icon_alt"], 44)}<em>alt.</em></span></div>'
            f'<div class="igg">{promo}{lightpost}{detail}</div></div>')


# ---------------------------------------------------------------- 5. site + dashboard
def site_header(P, mode):
    T = P[mode]
    return (f'<div class="sh" style="background:{T["bg"]};border-color:{T["line"]}">{wordmark_svg(T["agend"], T["ai"], 26)}'
            f'<nav style="color:{T["mut"]}">Produto<span>Planos</span><span>Contato</span></nav>'
            f'<b style="background:{T["btn_bg"]};color:{T["btn_fg"]}">Começar grátis</b></div>')


def dashboard(P, mode):
    T = P[mode]
    side = "".join(f'<span style="color:{T["accent"] if i == 0 else T["mut"]};background:{T["chip"] if i == 0 else "transparent"}">{t}</span>'
                   for i, t in enumerate(("Painel", "Agenda", "Clientes", "Corridas", "Financeiro", "Frota")))
    kpis = "".join(f'<div class="k" style="background:{T["surf"]}"><span style="color:{T["mut"]}">{a}</span><b style="color:{T["ink"]}">{b}</b></div>'
                   for a, b in (("Receita do mês", "R$ 14.920"), ("Corridas", "86"), ("Clientes ativos", "41")))
    bars = "".join(f'<i style="height:{h}%;background:{T["accent"] if j in (8, 9) else T["line"]}"></i>' for j, h in enumerate((30, 45, 38, 60, 52, 70, 64, 78, 88, 72, 58, 66)))
    return (f'<div class="dash" style="background:{T["bg"]};border-color:{T["line"]}"><aside style="border-color:{T["line"]}">{wordmark_svg(T["agend"], T["ai"], 18)}{side}</aside>'
            f'<div class="main"><div class="kp">{kpis}</div><div class="chart" style="background:{T["surf"]}">'
            f'<span style="color:{T["mut"]}">Faturamento · últimas 12 semanas</span><div class="cb">{bars}</div></div></div></div>')


# ---------------------------------------------------------------- 6. commercial piece
def flyer(P, mode):
    T = P[mode]
    return (f'<div class="fly" style="background:{T["bg"]};border-color:{T["line"]}">{wordmark_svg(T["agend"], T["ai"], 34)}'
            f'<h4 style="color:{T["ink"]}">Sua operação organizada.<br>Do agendamento ao financeiro.</h4>'
            f'<ul style="color:{T["mut"]}"><li>Agenda e clientes</li><li>Corridas e serviços</li><li>Custos, frota e relatórios</li></ul>'
            f'<b style="background:{T["btn_bg"]};color:{T["btn_fg"]}">agendai.app</b></div>')


def column(pk):
    P = PAL[pk]
    return {
        "study": study(pk), "icons": icons(pk),
        "iphone": f'<div class="row phones">{phone_home(P, False)}{phone_home(P, True)}{phone_app(P, "light")}{phone_app(P, "dark")}</div>',
        "ig": instagram(P),
        "site": site_header(P, "light") + site_header(P, "dark") + dashboard(P, "light") + dashboard(P, "dark"),
        "fly": f'<div class="row">{flyer(P, "light")}{flyer(P, "dark")}</div>',
    }


SECTIONS = [("study", "1 · Composições de cor (contraste medido)"), ("icons", "2 · Ícone e A isolado — padrão, alternativo, iOS escuro, iOS tingido, tamanhos e tela inicial"),
            ("iphone", "3 · iPhone — tela inicial clara/escura e app nos modos claro e escuro"), ("ig", "4 · Instagram — perfil, avatar pequeno e publicação"),
            ("site", "5 · Site e SaaS — cabeçalho claro/escuro e dashboard claro/escuro"), ("fly", "6 · Peça comercial — clara e escura")]

CSS = """
body{margin:0;background:#fff;color:#0A0F14;font:13.5px/1.45 system-ui,-apple-system,"Segoe UI",Inter,sans-serif}
main{max-width:1500px;margin:0 auto;padding:30px 26px} h1{margin:0;font-size:27px} .sub{color:#5b6470;margin:4px 0 16px}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:30px} .colh{font-size:19px;font-weight:700;padding:8px 0;border-bottom:2px solid #0A0F14}
section{border-top:1px solid #eceeef;padding:14px 0} h3{margin:0 0 10px;font-size:12.5px;letter-spacing:.06em;text-transform:uppercase;color:#5b6470}
.row{display:flex;flex-wrap:wrap;gap:12px;align-items:flex-end;margin-bottom:10px}
.study{display:grid;grid-template-columns:1fr 1fr;gap:8px} .sw{border:1px solid #e6e8ea;border-radius:10px;padding:12px 12px 8px;display:flex;flex-direction:column;gap:6px}
.swl{font-size:11.5px;display:flex;flex-direction:column} .sw[style*="#0A0F14"] .swl,.sw[style*="#0D0D0D"] .swl{color:#e8e8e8}
.ok{color:#11845b}.warn{color:#b7791f}.bad{color:#c53030} .sw[style*="#0A0F14"] .ok,.sw[style*="#0D0D0D"] .ok{color:#5ee0b0}
.szb{display:flex;flex-direction:column;align-items:center;gap:3px} .szb em{font-style:normal;font-size:10.5px;color:#8a929b}
.szb.bgk{background:#fff;border:1px solid #eceeef;border-radius:12px;padding:6px}
.home{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;padding:14px;border-radius:16px;width:260px}
.home.lt{background:linear-gradient(160deg,#e9edf2,#d7dde6)} .home.dk{background:linear-gradient(160deg,#1b1f25,#0d0f12)}
.app{display:flex;flex-direction:column;align-items:center;gap:3px} .app i{width:46px;height:46px;border-radius:10.3px;display:block}
.app em{font-style:normal;font-size:9.5px} .home.lt em{color:#222}.home.dk em{color:#ddd} .app svg{display:block}
.phones{gap:8px;flex-wrap:nowrap} .phone{width:162px;height:340px;flex:none;border-radius:30px;background:#111;padding:6px;box-sizing:border-box}
.scr{width:100%;height:100%;border-radius:25px;overflow:hidden;position:relative;font-size:9.5px}
.scr.hs.lt{background:linear-gradient(160deg,#e9edf2,#cfd7e2)} .scr.hs.dk{background:linear-gradient(160deg,#1b1f25,#07080a)}
.sb{font-size:9px;font-weight:600;padding:8px 14px 2px} .hs.lt .sb{color:#111}.hs.dk .sb{color:#eee}
.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:7px;padding:10px} .grid .app i,.grid .app svg{width:30px;height:30px;border-radius:7px}
.grid .app em{font-size:7px} .hs.lt .app em{color:#222} .hs.dk .app em{color:#ddd}
.ph{display:flex;justify-content:space-between;align-items:center;padding:6px 12px} .ph span{width:22px;height:22px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:8px;font-weight:700}
.kpi{margin:6px 10px;border-radius:12px;padding:8px 10px;display:flex;flex-direction:column} .kpi b{font-size:15px}
.bars{display:flex;align-items:flex-end;gap:4px;height:34px;margin-top:4px} .bars i{flex:1;border-radius:3px;display:block}
.sec{padding:6px 12px 2px;font-weight:600} .li{margin:0 10px;padding:6px 2px;border-bottom:1px solid;display:grid;grid-template-columns:1fr auto}
.li span{grid-column:1} .li i{grid-row:1/3;grid-column:2;align-self:center;font-style:normal;font-size:8px;padding:2px 6px;border-radius:8px;font-weight:600}
.fab{margin:8px 10px;border-radius:10px;padding:7px;text-align:center;font-weight:700}
.tab{position:absolute;bottom:0;left:0;right:0;border-top:1px solid;display:flex;justify-content:space-around;padding:8px 0 12px;font-weight:600;font-size:8.5px}
.ig{border:1px solid #e6e8ea;border-radius:14px;padding:14px;display:flex;flex-direction:column;gap:10px}
.igh{display:flex;gap:14px;align-items:center} .igh div{display:flex;flex-direction:column} .igh span{color:#5b6470} .igh small{color:#333}
.igs{display:flex;gap:14px;align-items:flex-end} .igs span{display:flex;flex-direction:column;align-items:center} .igs em{font-style:normal;font-size:10px;color:#8a929b}
.igg{display:grid;grid-template-columns:repeat(3,1fr);gap:3px} .post{aspect-ratio:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px}
.post p{margin:0;text-align:center;font-size:10px;font-weight:600} .post span{font-size:9px;font-weight:700;padding:3px 9px;border-radius:6px}
.sh{display:flex;align-items:center;gap:16px;border:1px solid;border-radius:12px;padding:10px 16px;margin-bottom:8px}
.sh nav{flex:1;font-size:13px}.sh nav span{margin-left:16px}.sh b{font-size:12.5px;padding:7px 12px;border-radius:8px}
.dash{display:grid;grid-template-columns:140px 1fr;border:1px solid;border-radius:12px;overflow:hidden;margin-bottom:8px;height:220px}
.dash aside{border-right:1px solid;padding:12px 8px;display:flex;flex-direction:column;gap:4px} .dash aside svg{margin:0 6px 8px}
.dash aside span{padding:5px 8px;border-radius:7px;font-size:12px;font-weight:600}
.main{padding:12px;display:flex;flex-direction:column;gap:10px} .kp{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.k{border-radius:10px;padding:8px 10px;display:flex;flex-direction:column} .k span{font-size:11px}.k b{font-size:17px}
.chart{border-radius:10px;padding:8px 10px;flex:1;display:flex;flex-direction:column} .chart span{font-size:11px}
.cb{flex:1;display:flex;align-items:flex-end;gap:5px;margin-top:6px} .cb i{flex:1;border-radius:3px;display:block}
.fly{width:300px;aspect-ratio:4/5;border:1px solid;border-radius:14px;padding:22px;box-sizing:border-box;display:flex;flex-direction:column;gap:12px}
.fly h4{margin:6px 0 0;font-size:18px;line-height:1.25} .fly ul{margin:0;padding-left:16px;flex:1} .fly b{align-self:flex-start;padding:8px 14px;border-radius:9px}
table{border-collapse:collapse;width:100%} th,td{text-align:left;vertical-align:top;padding:7px 10px;border-bottom:1px solid #eceeef} th{width:190px;color:#5b6470}
"""

EVAL = [("Elegância e personalidade", "Tecnológica, limpa, contemporânea.", "Mais ‘premium/executiva’; muito elegante no escuro."),
        ("Legibilidade e contraste", "Escuro: AI #00D1B2 = 9,9:1. Claro: AI #00A98F = 3,0:1 (ok em logo).", "Escuro: dourado = 9,3:1. Claro: dourado = 1,9:1 — no claro a marca precisa ser toda preta."),
        ("Claro e escuro", "Funciona nos dois mantendo o verde visível.", "Brilha no escuro; no claro perde o dourado."),
        ("iPhone", "Ícone grafite + A verde se destaca em telas claras e escuras.", "Ícone preto + A dourado excelente; some menos no escuro."),
        ("Instagram", "Avatar legível em 24 px; feed com cara de produto.", "Avatar elegante; feed tende ao ‘luxo’."),
        ("Site e SaaS", "Interface clara natural; verde serve a botões, gráficos e estados.", "Interface clara sem dourado útil (contraste); dourado só como detalhe."),
        ("Consistência", "Mesma lógica de cor no logo, no ícone e na interface.", "A cor muda de papel entre claro e escuro."),
        ("Reprodução", "Verdes vivos variam na impressão (CMYK) — exigem prova.", "Dourado chapado imprime bem; metálico (hot stamping) é opcional."),
        ("Longo prazo / multissegmento", "Neutra para qualquer segmento de serviço.", "Associada a transporte executivo e luxo; restringe outros segmentos.")]


def main():
    E, D = column("esmeralda"), column("dourado")
    body = '<div class="cols"><div class="colh">Opção 1 · Esmeralda Tech</div><div class="colh">Opção 2 · Preto e Dourado</div></div>'
    for key, title in SECTIONS:
        body += f'<section><h3>{title}</h3><div class="cols"><div>{E[key]}</div><div>{D[key]}</div></div></section>'
    rows = "".join(f"<tr><th>{c}</th><td>{a}</td><td>{b}</td></tr>" for c, a, b in EVAL)
    body += f'<section><h3>7 · Comparação</h3><table><tr><th></th><th>Esmeralda Tech</th><th>Preto e Dourado</th></tr>{rows}</table></section>'
    html = (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>AgendAI — identidades</title><style>{CSS}</style></head>'
            f'<body><main><h1>AgendAI — rodada 9: o wordmark nas duas identidades</h1>'
            f'<p class="sub">Wordmark aprovado (rodada 8, sem alteração estrutural) · mesmos contextos lado a lado · nenhuma cor de uma paleta usada na outra (interfaces usam apenas transparências das próprias cores)</p>'
            f'{body}</main></body></html>')
    os.makedirs(f"{OUT}/05-apresentacao", exist_ok=True)
    open(f"{OUT}/05-apresentacao/identidades.html", "w").write(html)
    # reusable colour masters of this round
    os.makedirs(f"{OUT}/02-cores", exist_ok=True)
    for pk in PAL:
        for mode in ("light", "dark"):
            T = PAL[pk][mode]
            s = wordmark_svg(T["agend"], T["ai"], 142).replace('role="img"', 'role="img"')
            s = s.replace(">", f'><rect width="100%" height="100%" fill="{T["bg"]}"/>', 1)
            open(f"{OUT}/02-cores/wordmark-{pk}-{'claro' if mode == 'light' else 'escuro'}.svg", "w").write(s + "\n")
        open(f"{OUT}/02-cores/icone-{pk}.svg", "w").write(icon_svg(*PAL[pk]["icon"], 256) + "\n")
    print("ok")


if __name__ == "__main__":
    main()
