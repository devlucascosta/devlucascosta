"""Builds the naming deliverables (juridico/naming/) from the collected data files."""
import csv, json, re, unicodedata
from datetime import date

N = "/home/user/devlucascosta/juridico/naming"
D = f"{N}/dados"
dom = json.load(open(f"{D}/dominios_appstore.json"))
mkt = json.load(open(f"{D}/mercado.json"))
qual = json.load(open(f"{D}/qualidade.json"))
inpi = json.load(open(f"{D}/inpi_conflitos.json"))
NOMES = list(qual)
PEPI = "https://busca.inpi.gov.br/pePI/ (Marcas › Pesquisa por número do processo)"
HOJE = "20/11/2026"


def a(s):
    return unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()


# ---------------------------------------------------------------- manual verdicts (from reviewing the evidence)
V = {
 "Vértia": ("Conflito relevante", "VERTIA é marca da SOFTPLAN S/A (grande empresa brasileira de software) com registros concedidos nas classes 9 e 42 e pedido na 35 — idêntico, mesmo segmento."),
 "Atempo": ("Conflito relevante", "ATEMPO concedida na classe 35 (ATEMPO LTDA, SC) e 'Attempo' (fonética idêntica) concedida nas classes 42 e 35 (BRR TECH GEOSOLUTIONS); empresa francesa de software Atempo; expressão descritiva ('a tempo')."),
 "Elora": ("Conflito relevante", "ELORA concedida na classe 42 (LDC DESIGN PARA NEGÓCIOS) e pedidos 'Elora' nas classes 42 (BEOS IA SYSTEMS) e 9/42 (outro titular); dezenas de marcas 'Elora' na 35; Elorus/Eloria no mercado de software."),
 "Novera": ("Conflito relevante", "Pedidos idênticos 'NOVERA' na classe 35 e 'Novera' na classe 9, além de 'NOVERA COMMERCE' na 9 (três titulares diferentes); produto 'Novera' B2B no exterior."),
 "Nivora": ("Conflito relevante", "Pedidos idênticos 'NIVORA' nas classes 9 e 35 por dois titulares distintos (B S FRANQUI e RELAXMEDIC), depositados em 2025–2026."),
 "Avora": ("Conflito relevante", "Ao menos 12 marcas ativas com 'AVORA' nas classes 35/42 (AVORA BANK, AVORA PAY, AVORA CAPITAL, AVORA SECURITIZADORA concedida, Ávora Engenharia 42) e plataforma de analytics 'Avora' listada no Brasil."),
 "Plenna": ("Conflito relevante", "PLENNA concedida na classe 35 (PLENNA ESPECIALIDADES) e outras 12 marcas 'Plenna' ativas nas classes 9/35/42; app 'Plenna' de uma empresa brasileira de agendamento ('Bus serviços de agendamento ltda'); centenas de marcas 'Plena'."),
 "Veyra": ("Conflito relevante", "Pedidos idênticos 'VEYRA' na classe 42 e 'Veyra' na classe 9 (2025–2026) e 'Veyra Salonsoftware' (CRM para salões) no mercado; confusão com o sobrenome 'Vieira'."),
 "Orvia": ("Risco elevado", "'Orvya' (fonética idêntica) em pedido na classe 35; 'ORVIAN', 'OH! ORVIAH' e 'TORVIA' na classe 9; FORVIA (multinacional) concedida nas classes 9/42; software 'ORVIA' de gestão empresarial em nuvem listado no Capterra/GetApp."),
 "Oryza": ("Risco elevado", "'ORYZA & SOY' concedida na classe 42 (consultoria agronômica) e 'ORIZZA' (fonética idêntica) em pedidos nas classes 9, 35 e 42; empresa vietnamita Oryza System Technology com suíte de software."),
 "Movent": ("Risco elevado", "'MOUVENT' (Bobst, Suíça) concedida nas classes 9 e 35; 'MOVENTE' (CRESCERA ECOSYSTEM) em pedido na 42; 'Movento' concedida nas classes 9/35; pronúncia pouco natural em português."),
 "Ordina": ("Risco elevado", "Ordina N.V./Sopra Steria é grande empresa europeia de TI; 'ordena' concedida na classe 9 (Inovasul, programas de computador) e 'Ordena Aqui' concedida na 42 (Lunar TI) — Ordina × Ordena são foneticamente próximos; 'DONA ORDINA' na 35."),
 "Pontta": ("Risco elevado", "Sem marca 'Pontta' exata ativa, mas centenas de 'Ponta' nas classes 35/42; 'Pontta Technology' (Brasil) com registro de 'Pontta ERP' e pontta.com.br ativo desde 2008; o público tende a escrever 'Ponta'."),
 "Rotiva": ("Risco elevado", "'ROTIVA LOG ARMAZENAGEM E DISTRIBUIÇÃO' (palavra idêntica) em pedido na classe 39 — logística; 'rotiv' concedida na classe 9 e 'ROTIV-IA' (ROTIV TECNOLOGIA) em pedido na 42; nome associado a 'rota' (limita a expansão)."),
 "Tavora": ("Risco moderado", "Sobrenome comum: 15 marcas ativas com 'Távora' (classes 35, 36, 41 etc.), nenhuma nas classes 9/42; baixa distintividade por ser patronímico; tavora.com à venda (Afternic)."),
 "Solven": ("Risco moderado", "'SOLVEN' (palavra idêntica) em pedido na classe 01 (química — SOLVEN SOLVENTES E QUÍMICOS, solven.com.br desde 1999); SOLVENTUM concedida em várias classes incl. 9/42; evocativo de 'solvente/solve'."),
 "Orrena": ("Risco moderado", "'ORENNA' (fonética idêntica) concedida na classe 35 (CONVERT IMPORTAÇÃO — comércio); família 'Ordena' (classe 9 concedida, 42 concedida) a avaliar; RR duplo dificulta a escrita."),
 "Averto": ("Candidato promissor", "Nenhuma marca ativa 'Averto' no INPI; semelhantes distantes (AVERT/AVETO na 35, CHROMAVERTO 9/42 — designação estrangeira); usos internacionais sem atuação no Brasil (averto.io — app de segurança; Averto Ltd — suporte de TI, Escócia)."),
 "Tavena": ("Candidato promissor", "Nenhuma marca ativa 'Tavena' no INPI; semelhantes apenas 'Taverna' (restaurantes, classe 35); .com.br e .app.br livres; uso internacional tavena.io (serviços para criadores), sem atuação conhecida no Brasil."),
 "Caliro": ("Candidato promissor", "Nenhuma marca ativa 'Caliro' no INPI; semelhantes distantes (Caleiro, Calibro na 35; KAIRO'S INFORMÁTICA 9/35); .com.br e .app.br livres; app 'Caliro AI' (FUTURAI) na App Store."),
 "Oltara": ("Candidato promissor", "Nenhuma marca ativa 'Oltara' no INPI; única semelhante 'OLARA' (confecções, classe 35); .app.br livre (.com.br registrado em 2025); usos internacionais: Oltara (energia solar, Índia)."),
}
ORDER = {"Candidato promissor": 0, "Risco moderado": 1, "Risco elevado": 2, "Conflito relevante": 3}


def dom_status(info):
    if info["http"] == "404":
        return "Disponível confirmado (RDAP: inexistente)"
    if info["http"] == "200":
        ns = " ".join(info.get("nameservers") or []).lower()
        if "afternic" in ns or "parking" in ns or "sedo" in ns:
            return "Registrado sem uso aparente (estacionado/à venda)"
        if not ns:
            return "Registrado — situação/uso inconclusivo (sem DNS publicado)"
        return "Registrado — uso não verificado (inconclusivo)"
    return f"Informação inconclusiva (HTTP {info['http']})"


def key_conflicts(n, k=8):
    occ = inpi[n]["ocorrencias"]
    ca = a(n)
    ex = [r for r in occ if r["score"] >= 96 or ca in re.findall(r"[a-z0-9]+", a(r["nome"]))]
    hi = [r for r in occ if r not in ex and r["nivel"] in ("crítico", "alto") and r["score"] >= 90 and not re.search(r"ordinar|extraordin|coordin|ponta|pontal|pontão|taverna|carnivor", a(r["nome"]))]
    out = []
    for r in ex[:6] + hi[: max(0, k - len(ex[:6]))]:
        out.append({"processo": r["numero"], "marca": r["nome"], "apresentacao": r["apresentacao"], "classes": r["classes"],
                    "titular": r["titulares"], "deposito": r["deposito"], "concessao": r["concessao"], "vigencia": r["vigencia"],
                    "situacao": r["situacao"], "semelhanca": f'{r["score"]} — {r["motivo"]}', "especificacao": (r["especificacao"] or "")[:300],
                    "fonte_rpi": r["fonte_rpi"], "consulta_pepi": f"{PEPI} — nº {r['numero']}"})
    return out


def usos(n, risco, dd):
    livre_br = dd[f"{a(n)}.com.br"]["http"] == "404"
    livre_app = dd[f"{a(n)}.app.br"]["http"] == "404"
    apps = [x for x in dom[n]["app_store"] if x.get("app") and a(n) in a(x["app"])]
    base = {"Conflito relevante": "Desaconselhado", "Risco elevado": "Desaconselhado sem parecer jurídico",
            "Risco moderado": "Possível com ressalvas", "Candidato promissor": "Aparentemente viável (sujeito a busca formal)"}[risco]
    return {
        "nome_principal": base,
        "marca_nominativa": base if risco != "Candidato promissor" else "Aparentemente viável — depositar nas classes 9, 35 e 42 após busca formal",
        "marca_mista": base if risco != "Candidato promissor" else "Viável; reforça a distintividade, mas não substitui o nominativo",
        "elemento_figurativo": "Viável em qualquer caso (símbolo próprio), desde que não reproduza marcas de terceiros",
        "nome_app_lojas": ("Possível; há apps homônimos (" + ", ".join(sorted({x['app'] for x in apps})[:3]) + ") — usar complemento ('Nome — Gestão')") if apps else "Possível; nenhum app homônimo encontrado na App Store (BR/EUA)",
        "dominio_saas": ("Possível com .com.br" if livre_br else ("Possível com .app.br" if livre_app else "Exige variação (ex.: usenome.com.br / nome.app) — .com.br e .app.br ocupados")) + "; .com ocupado",
        "identidade_visual": "Viável" if risco in ("Candidato promissor", "Risco moderado") else "Não investir antes de resolver o risco jurídico",
        "expansao_segmentos": "Boa (nome sem significado ligado a transporte)" if n not in ("Rotiva", "Orvia", "Movent") else "Limitada (remete a rota/via/movimento)",
    }


rows, structured = [], {}
for n in NOMES:
    risco, motivo = V[n]
    dd = dom[n]["dominios"]
    q = qual[n]
    kc = key_conflicts(n)
    structured[n] = {
        "nome": n, "classificacao": risco, "motivo": motivo,
        "inpi": {"semelhantes_encontrados": inpi[n]["total_semelhantes"], "ativos_relevantes": inpi[n]["ativos_relevantes"],
                 "por_nivel": inpi[n]["por_nivel"], "conflitos_principais": kc},
        "mercado": mkt[n], "dominios": {d: {"situacao": dom_status(i), "registro": (i.get("eventos") or {}).get("registration"),
                                            "nameservers": i.get("nameservers")} for d, i in dd.items()},
        "app_store": sorted({f'{x["app"]} — {x["dev"]}' for x in dom[n]["app_store"] if x.get("app") and a(n) in a(x["app"])}),
        "qualidade": q, "usos": usos(n, risco, dd),
    }
    notas = [q[k] for k in ("sonoridade", "pronuncia", "escrita", "memorizacao", "distintividade", "aparencia_software", "expansao", "disponibilidade_digital")]
    rows.append([n, risco, inpi[n]["ativos_relevantes"], sum(1 for c in kc if set((c["classes"] or "").split(",")) & {"9", "09", "35", "42"}),
                 *[structured[n]["dominios"][d]["situacao"] for d in dd], len(structured[n]["app_store"]), mkt[n]["nivel"], *notas,
                 round(sum(notas) / len(notas), 1), motivo])

hdr = ["nome", "classificacao", "inpi_ativos_semelhantes", "inpi_conflitos_principais_9_35_42", "dominio_com_br", "dominio_app_br", "dominio_com",
       "apps_homonimos_app_store", "uso_mercado", "sonoridade", "pronuncia", "escrita", "memorizacao", "distintividade",
       "aparencia_software", "expansao", "disponibilidade_digital", "media_qualidade", "motivo_principal"]
rows.sort(key=lambda r: (ORDER[r[1]], -r[17]))
with open(f"{N}/matriz-comparativa.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(hdr); w.writerows(rows)
json.dump({"data_consulta": HOJE, "candidatos": structured}, open(f"{N}/resultados-estruturados.json", "w"), ensure_ascii=False, indent=1)

# ---------------------------------------------------------------- analise-individual.md
L = [f"# Análise individual — 21 candidatos\n\nConsulta em {HOJE}. Ordem: do mais promissor ao mais arriscado. "
     "Semelhança INPI: 100 = idêntico; 96 = fonética idêntica; 92 = contém o nome; 80–91 = semelhante. "
     "Fonte de cada processo: edição da RPI indicada (XML oficial) e consulta no pePI pelo número.\n"]
for r in rows:
    n = r[0]; s = structured[n]; q = s["qualidade"]
    L.append(f"\n---\n\n## {n} — **{s['classificacao']}**\n\n{s['motivo']}\n")
    L.append(f"**INPI:** {s['inpi']['semelhantes_encontrados']} marcas semelhantes no índice; {s['inpi']['ativos_relevantes']} ativas com semelhança forte "
             f"(crítico {s['inpi']['por_nivel']['crítico']} · alto {s['inpi']['por_nivel']['alto']} · moderado {s['inpi']['por_nivel']['moderado']} · baixo {s['inpi']['por_nivel']['baixo']}).\n")
    if s["inpi"]["conflitos_principais"]:
        L.append("| Processo | Marca | Classes | Titular | Situação | Semelhança | Fonte |\n|---|---|---|---|---|---|---|")
        for c in s["inpi"]["conflitos_principais"]:
            L.append(f"| {c['processo']} | {c['marca']} | {c['classes']} | {(c['titular'] or '')[:60]} | {c['situacao']} | {c['semelhanca']} | [RPI]({c['fonte_rpi']}) |")
        L.append("")
    else:
        L.append("Nenhuma marca ativa idêntica ou fortemente semelhante nas classes relevantes.\n")
    L.append(f"**Mercado:** {s['mercado']['resumo']}" + (" Fontes: " + " · ".join(f"[{i+1}]({u})" for i, u in enumerate(s['mercado']['fontes'])) if s['mercado']['fontes'] else "") + "\n")
    L.append("**Domínios:** " + " · ".join(f"`{d}`: {v['situacao']}" + (f" (registro {v['registro'][:10]})" if v['registro'] else "") for d, v in s["dominios"].items()) + "\n")
    L.append("**App Store (BR/EUA):** " + (", ".join(s["app_store"][:6]) if s["app_store"] else "nenhum app homônimo") + "\n")
    L.append("**Formas de uso:** " + "; ".join(f"*{k.replace('_', ' ')}*: {v}" for k, v in s["usos"].items()) + "\n")
    L.append(f"**Qualidade (0–10):** sonoridade {q['sonoridade']} · pronúncia {q['pronuncia']} · escrita {q['escrita']} · memorização {q['memorizacao']} · "
             f"distintividade {q['distintividade']} · aparência de software {q['aparencia_software']} · expansão {q['expansao']} · "
             f"disponibilidade digital {q['disponibilidade_digital']}. {q['justificativa']}\n")
open(f"{N}/analise-individual.md", "w").write("\n".join(L))
print("ok", [(r[0], r[1]) for r in rows])
