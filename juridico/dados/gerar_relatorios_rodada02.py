"""Gera os entregáveis da rodada 2 de naming a partir dos dados coletados (INPI/RPI, RDAP, App Store, web).

Uso: python3 dados/gerar_relatorios_rodada02.py   (executar a partir de juridico/)
As avaliações qualitativas (conceito, notas, veredito) estão neste arquivo; os dados objetivos vêm de naming/rodada-02/dados/.
"""
import csv, glob, json, os, statistics

BASE = "naming/rodada-02"
D = f"{BASE}/dados"
DATA = "20/11/2026"
RPI_BASE = "RPI, seção Marcas, XML oficial: edições 2220 (23/07/2013) a 2915 (17/11/2026), 696 edições, índice local de 5,3 milhões de processos"
CRIT = ["sonoridade", "pronuncia", "escrita", "memorizacao", "originalidade", "distintividade", "aparencia_visual",
        "potencial_expansao", "adequacao_saas"]
CORE_PLUS = {"9", "09", "35", "42", "39"}

# ---------------------------------------------------------------- dados objetivos
INPI = {}
for f in sorted(glob.glob(f"{D}/inpi_conflitos*.json")):
    INPI.update(json.load(open(f)))
VAR = {}
for f in (f"{D}/inpi_variantes_conflitos.json", f"{D}/inpi_variantes2_conflitos.json"):
    VAR.update(json.load(open(f)))
DOM = json.load(open(f"{D}/dominios_appstore.json"))


def proximas(nome, n=5, minimo=88):
    """Marcas ativas mais próximas nas classes 9/35/42/39 (semelhança >= minimo)."""
    out, seen = [], set()
    for o in sorted(INPI[nome]["ocorrencias"], key=lambda o: -o["score"]):
        cls = set((o["classes"] or "").split(","))
        if o["score"] < minimo or not (cls & CORE_PLUS):
            continue
        k = (o["nome"].upper(), o["classes"])
        if k in seen:
            continue
        seen.add(k)
        out.append(o)
        if len(out) >= n:
            break
    return out


def variantes(lista, minimo=92):
    out = []
    for v in lista:
        hits = [o for o in VAR.get(v, {}).get("ocorrencias", []) if o["score"] >= minimo and o["nivel"] != "baixo"]
        out.append({"variante": v, "ocorrencias": [{k: o[k] for k in ("numero", "nome", "classes", "situacao", "titulares", "score")}
                                                    for o in hits[:4]]})
    return out


def dom_status(nome):
    n = nome.lower()
    r = {}
    for tld in ("com.br", "app.br", "com"):
        info = DOM[nome]["dominios"][f"{n}.{tld}"]
        if info["http"] == "404":
            r[tld] = "disponível confirmado"
        elif info["http"] == "200":
            ns = " ".join(info.get("nameservers") or []).lower()
            reg = (info.get("eventos") or {}).get("registration", "")[:10]
            tit = "; ".join(sorted({e["nome"] for e in info.get("entidades", []) if e.get("nome") and "registrant" in (e.get("papel") or []) or (e.get("nome") and tld != "com" and "owner" in str(e.get("papel")))}))
            venda = any(x in ns for x in ("afternic", "buydomains", "sedoparking", "atom.com", "this-domain-for-sale"))
            r[tld] = "registrado" + (" (à venda, DNS de marketplace)" if venda else "") + (f" em {reg}" if reg else "") + (f" — titular: {tit}" if tit else "")
        else:
            r[tld] = f"inconclusivo (HTTP {info['http']})"
    return r


def apps(nome):
    n = nome.lower()
    s = {(a["pais"], a["app"], a["dev"]) for a in DOM[nome]["app_store"] if "app" in a and (n in (a["app"] or "").lower() or n in (a["dev"] or "").lower())}
    return [{"loja": p.upper(), "app": a, "desenvolvedor": d} for p, a, d in sorted(s)]


# ---------------------------------------------------------------- avaliações (qualitativas, revisadas manualmente)
A = {  # nome: dict
 "Salendo": dict(status="promissor", notas=[8, 9, 9, 8, 8, 7, 8, 9, 8], var=["Zalendo", "Salento"],
   conceito="Nome de som latino que remete à ideia de subida contínua (em italiano, \"salendo\" é forma do verbo \"subir\"). Posiciona o produto como aquilo que faz o negócio do profissional crescer de forma organizada, degrau por degrau.",
   personalidade="Ascendente, otimista, dinâmica, com calor latino.",
   mercado="Sem empresa de software ou app com esse nome. Ocorrências esparsas: salendo.nl (empresa neerlandesa com site encerrado, segundo o Trustpilot), um wine bar na Itália (San Galgano) e uma faixa musical de 2026. O salendo.com está anunciado como domínio premium à venda na Atom.",
   urls=["https://www.trustpilot.com/review/salendo.nl", "https://www.atom.com/name/Salendo", "https://www.facebook.com/sangalganosalendowine/"],
   vantagens="Ótima pronúncia em português e espanhol; ideia de crescimento; .com.br e .app.br livres; .com comprável; nenhuma marca semelhante ativa nas classes 9/42.",
   riscos="É palavra comum em italiano (menor distintividade na Itália). Variante \"salento\" (t/d) concedida na classe 35 para vestuário (proc. 935840907), sem afinidade com software. A semelhança gráfica distante com Solven (nome proibido) não vem da mesma raiz, mas convém registrar. [Auditoria final] ALENTO tem pedidos de software nas classes 9 e 42 (procs. 944373321 e 944373216, 07/2026), e Play Valendo tem pedidos nas classes 9 e 42."),
 "Lindaro": dict(status="pendências", notas=[8, 9, 9, 8, 7, 8, 8, 8, 7], var=["Lintaro"],
   conceito="Som de nome próprio latino, com eco de \"lindo\". Sugere trabalho bem-feito, cuidado e acabamento profissional, a sensação de ter tudo arrumado.",
   personalidade="Elegante, acolhedora, confiável, com acabamento premium.",
   mercado="Sem software ou app. Única empresa: lindaro GmbH (Alemanha, atacado de móveis), sem afinidade com SaaS. O lindaro.com foi registrado em 2023 com DNS da Locaweb (provável titular brasileiro, uso não verificado).",
   urls=["https://www.dnb.com/business-directory/company-profiles.lindaro_gmbh.a0de9ca372fb21d6687204a2c69b2e2c.html", "https://www.mow.de/en/exhibitors/lindaro"],
   vantagens="Muito fácil de falar e escrever; soa premium; nenhuma marca semelhante ativa ≥ 88% nas classes 9/35/42/39; .com.br e .app.br livres.",
   riscos="[Revisado na auditoria final de 21/11/2026] LINDARA concedida na classe 35 (proc. 936511826), só a vogal final diferente; o INPI já indeferiu LINDARE citando essa marca (RPI 2911). LINARA tem pedidos de software nas classes 9 e 42 (procs. 945043058 e 945043180, 08/2026). TÍNDARO está concedida nas classes 35 e 42 (procs. 912190442 e 912190884, empresa de TI). O .com tem titular provavelmente brasileiro desde 2023."),
 "Joreva": dict(status="promissor", notas=[7, 8, 8, 7, 9, 9, 7, 8, 7], var=["Joriva", "Jureva"],
   conceito="Nome inventado, sem significado prévio em português, inglês ou espanhol. Pode ser preenchido pela marca com as ideias de jornada e de rotina bem conduzida (associação de posicionamento, não etimologia).",
   personalidade="Própria, firme, humana; neutra o bastante para crescer para outros segmentos.",
   mercado="Sem software ou app. Única ocorrência: página de Facebook \"Joreva Estudi Mobles\" (móveis, provavelmente Catalunha). O joreva.com está em DNS da BuyDomains, \"this domain for sale\".",
   urls=["https://www.facebook.com/JorevaEstudiMobles/"],
   vantagens="Altíssima distintividade: zero marcas ativas semelhantes no INPI, inclusive variantes. .com.br e .app.br livres, .com à venda.",
   riscos="A sílaba tônica pode oscilar (jo-RÉ-va / JO-re-va), e em inglês o J vira \"dj\". [Auditoria final] Óreva tem pedido na classe 35 para comércio de cosméticos (proc. 943905966). Na Espanha existem a Joreva Mobles SL (desde 1995) e a Joreva Estudi SL, ambas de móveis."),
 "Ubiro": dict(status="promissor", notas=[7, 8, 8, 8, 8, 8, 7, 8, 7], var=["Uviro", "Obiro"],
   conceito="Curto, começa por vogal e remete a \"ubíquo\": o negócio acessível de qualquer lugar (celular, navegador, notificações). Associação de posicionamento.",
   personalidade="Ágil, moderna, prática, onipresente sem ser invasiva.",
   mercado="Nenhuma empresa, software ou app com o nome exato. Nomes vizinhos sem conflito direto: Ubio (ub.io, automação B2B, Reino Unido), Ubiko (imóveis, Venezuela) e UBII (serviços).",
   urls=["https://www.crunchbase.com/organization/ub", "https://play.google.com/store/apps/details?id=ve.com.ubiko.app"],
   vantagens="Duas letras-chave (U, B) ótimas para ícone; pronúncia igual em PT/ES/EN; .com.br e .app.br livres; nenhuma semelhante ativa ≥ 92% nas classes centrais.",
   riscos="\"HubyPro\" (classe 9, pedido 944499090, 91%) e a família \"Hubio\" (classe 35) estão a uma distância moderada. O sufixo \"-iro\" coincide com o de Caliro (proibido), mas é genérico e a raiz é outra."),
 "Zemaro": dict(status="promissor", notas=[7, 8, 8, 7, 8, 8, 8, 8, 7], var=["Semaro", "Zemarro"],
   conceito="Nome inventado com inicial Z, forte e rara, que funciona bem como monograma. Sugere firmeza e precisão.",
   personalidade="Firme, segura, tecnológica sem ser fria.",
   mercado="Sem empresa ou app. Só um repositório público no GitHub (\"ZEMARO\", demonstração de marketplace, zemaro.vercel.app), sem indício de empresa constituída.",
   urls=["https://github.com/merajrok839-ops/ZEMARO"],
   vantagens="Ótimo ícone (Z); .com.br e .app.br livres; sem marcas semelhantes no software.",
   riscos="ZEMAR concedida nas classes 35 e 25 (vestuário infantil, proc. 907767656/907767869, 91%), sem afinidade com SaaS. Projeto homônimo no GitHub pode ganhar tração."),
 "Teiano": dict(status="promissor", notas=[7, 7, 8, 7, 8, 8, 7, 7, 7], var=["Deiano", "Taiano"],
   conceito="Remete a \"teia\": a rede que conecta clientes, agenda, finanças e comunicação num só lugar.",
   personalidade="Conectora, colaborativa, organizada.",
   mercado="Nenhuma empresa, software ou app encontrado (busca combinada com Tinaro).",
   urls=[],
   vantagens="Conceito claro de integração; zero marcas semelhantes ativas, inclusive variantes; .com.br e .app.br livres.",
   riscos="Pronúncia pode variar (tei-A-no / te-I-a-no); \"teia\" também evoca \"armadilha\", o que exige direção de marca cuidadosa."),
 "Lerano": dict(status="promissor", notas=[7, 8, 8, 6, 8, 8, 7, 8, 7], var=["Lirano"],
   conceito="Nome inventado de som suave e equilibrado; espaço livre para a marca construir a ideia de rotina leve e sob controle.",
   personalidade="Serena, equilibrada, discreta.",
   mercado="Nenhuma empresa, software ou app encontrado (busca combinada com Darelo).",
   urls=[],
   vantagens="Zero marcas semelhantes ativas no INPI; .com.br e .app.br livres.",
   riscos="Menor memorabilidade (soa genérico); .com registrado desde 2006 com DNS russo (uso não verificado)."),
 "Larimo": dict(status="promissor", notas=[7, 8, 8, 7, 8, 8, 7, 7, 7], var=["Larino"],
   conceito="Nome inventado com eco de \"lar\": o lugar onde o negócio está em ordem.",
   personalidade="Acolhedora, familiar, confiável.",
   mercado="Nenhuma empresa, software ou app encontrado.",
   urls=[],
   vantagens=".com.br e .app.br livres; semelhantes apenas distantes.",
   riscos="LARIO concedida na classe 9 (Dover Europe, instrumentos de medição, proc. 909816980, 91%) e LARIMOON na 35 (boutique, 92%); afinidade baixa."),
 "Fenaro": dict(status="promissor", notas=[7, 8, 8, 7, 7, 7, 8, 7, 7], var=["Venaro", "Phenaro"],
   conceito="Som de nome próprio latino, sóbrio e profissional; abre espaço para a ideia de farol, de guia (associação de posicionamento).",
   personalidade="Sóbria, profissional, orientadora.",
   mercado="Nenhuma empresa ou software. Ocorrência só de sobrenome (Fenara) em diretório italiano.",
   urls=["https://www.dnb.com/business-directory/company-profiles.reiser_srl.fb3612f97b542c4cf18aa74b731b91b9.html"],
   vantagens=".com.br e .app.br livres; nenhuma semelhante ativa ≥ 92% em 9/42.",
   riscos="VENARO (f/v) tem pedido na classe 35 para comércio de alimentos (proc. 934578508); FENAGRO (35, pedido). Afinidade baixa, mas a semelhança fonética exige parecer."),
 "Zaleno": dict(status="promissor", notas=[7, 8, 8, 7, 7, 7, 8, 7, 7], var=["Saleno", "Zalena", "Celeno"],
   conceito="Som próximo de \"zelo\": o cuidado com cada cliente e cada compromisso. Variante preferida de \"Zelano\", que tinha .com.br em uso por empresa.",
   personalidade="Cuidadosa, atenta, prestativa.",
   mercado="Nenhuma empresa, software ou app encontrado. O zaleno.com está em DNS da Afternic (à venda).",
   urls=[],
   vantagens="Zero marcas semelhantes ativas ≥ 88% nas classes centrais; .com.br e .app.br livres; .com comprável.",
   riscos="A variante \"Saleno\" (s/z) aproxima-se de SALERNO (35, concedida) e salento (35), ambas de comércio, sem afinidade com software. A família ZELÃO (35, vários titulares) está a distância moderada."),
 "Nirelo": dict(status="promissor", notas=[7, 8, 8, 6, 8, 8, 7, 7, 6], var=["Niredo"],
   conceito="Nome inventado, leve e fluido; sugere algo que funciona sem atrito.",
   personalidade="Leve, simples, fluida.",
   mercado="Nenhuma empresa, software ou app encontrado (busca combinada com Sarelo/Relano).",
   urls=[],
   vantagens="Sem semelhantes relevantes no INPI; .com.br e .app.br livres.",
   riscos="Memorabilidade e adequação a SaaS medianas. Niello Motoparts (35, pedido, 91%) a distância baixa."),
 "Zimeno": dict(status="promissor", notas=[6, 8, 8, 6, 8, 8, 7, 7, 6], var=["Simeno"],
   conceito="Nome inventado com inicial Z, de leitura direta.",
   personalidade="Objetiva, técnica, direta.",
   mercado="Nenhuma empresa, software ou app encontrado (busca combinada com Dirano). O zimeno.com está em DNS da Afternic (à venda).",
   urls=[],
   vantagens="Zero marcas semelhantes ativas, inclusive variantes; .com.br e .app.br livres; .com comprável.",
   riscos="Lembra os sobrenomes espanhóis Gimeno e Jimeno; sonoridade menos calorosa."),
 "Dirano": dict(status="promissor", notas=[6, 8, 8, 6, 7, 8, 7, 7, 6], var=["Tirano"],
   conceito="Nome inventado com eco de \"direção\" (associação de posicionamento).",
   personalidade="Direta, decidida.",
   mercado="Nenhuma empresa, software ou app encontrado (busca combinada com Zimeno).",
   urls=[],
   vantagens=".com.br e .app.br livres; sem semelhantes relevantes no INPI.",
   riscos="A variante t/d \"Tirano\" tem conotação negativa e marca na classe 41 (Tirano X). Personalidade fraca."),
 "Relano": dict(status="promissor", notas=[6, 8, 7, 6, 7, 7, 7, 7, 6], var=["Rilano"],
   conceito="Nome de som hispânico, sugere \"relação\" (relacionamento com clientes).",
   personalidade="Relacional, próxima.",
   mercado="Sem empresa ou software. Na App Store, aparece apenas como sobrenome de uma desenvolvedora (Leticia Rodriguez Relano), em apps sem relação.",
   urls=[],
   vantagens=".com.br e .app.br livres; semelhantes apenas distantes.",
   riscos="É sobrenome espanhol (Relaño) e lembra \"relleno\" (recheio) em espanhol; ARELANO (42, construtora, 92%) a distância moderada."),
 "Teluma": dict(status="pendências", notas=[8, 9, 9, 8, 8, 7, 8, 8, 8], var=["Deluma", "Teloma"],
   conceito="Som luminoso e macio (eco de \"lume\", luz), que transmite clareza sobre o próprio negócio.",
   personalidade="Clara, calorosa, inteligente.",
   mercado="Nenhuma empresa, software ou app com o nome exato. O teluma.com existe desde 2000 (titular desconhecido).",
   urls=[],
   vantagens="Uma das melhores sonoridades da rodada; .app.br livre; sem marca idêntica.",
   riscos="Tellma concedida na classe 42 (INFO TECNOLOGIA E SISTEMAS, sistemas e IA, proc. 935318887, 91%); IBM TELUM na classe 9 (IBM, proc. 501671446); TELUM CONTABILIDADE na 35 (proc. 921469470). teluma.com.br já registrado (titular oculto no RDAP)."),
 "Tinaro": dict(status="pendências", notas=[8, 9, 9, 8, 7, 7, 8, 8, 8], var=["Dinaro"],
   conceito="Remete a \"tino\": discernimento para tomar boas decisões de agenda, preço e finanças.",
   personalidade="Perspicaz, segura, experiente.",
   mercado="Nenhuma empresa, software ou app encontrado (busca combinada com Teiano).",
   urls=[],
   vantagens="Conceito forte e brasileiro; .com.br e .app.br livres.",
   riscos="TYARO concedida na classe 42 (consultoria em TI, proc. 921075545, 91%) e TÍNDARO concedida na 35 (titular do ramo de manutenção de redes, proc. 912190442, 92%)."),
 "Lealma": dict(status="pendências", notas=[8, 8, 8, 8, 8, 7, 8, 6, 8], var=["Lialma"],
   conceito="Junção de \"leal\" e \"alma\": confiança e cuidado no atendimento.",
   personalidade="Leal, humana, próxima.",
   mercado="Sem empresa ou app com o nome exato. Leal Apps (desenvolvedora brasileira) é nome vizinho.",
   urls=["https://www.zoominfo.com/c/leal-apps/542196234"],
   vantagens="Conceito de confiança muito claro em português; .com.br e .app.br livres.",
   riscos="LEALA GESTÃO REMOTA concedida na classe 35 para administração de empresas e apoio administrativo (proc. 933289626, 91%), com afinidade real. Fora do português o conceito se perde."),
 "Zenara": dict(status="pendências", notas=[8, 9, 9, 8, 7, 7, 8, 8, 7], var=["Senara"],
   conceito="Eco de \"zen\": tranquilidade de ter tudo organizado.",
   personalidade="Calma, equilibrada, moderna.",
   mercado="Na App Store existe um app \"Zenara\" (Zengnia) e outro \"Zenara Shop\". Na web, nenhum software de gestão.",
   urls=[],
   vantagens="Ótima sonoridade; zero marcas semelhantes no INPI; .app.br livre.",
   riscos="Apps homônimos na App Store (categoria a confirmar); zenara.com.br registrado em 07/2026 por pessoa física."),
}

DESC = {  # nome: motivo do descarte (evidência resumida)
 # lote 1
 "Aldora": "Marca idêntica ALDORA concedida na classe 35 (proc. 924?); ver inpi_conflitos.json",
 "Dalvo": "ADALVO / ADALVO+ concedidas nas classes 35/42/44 (Adalvo Ltd.)",
 "Fenara": "Variante preterida de Fenaro: fenara.com.br ocupado e FENDAARA (42, pedido, 92%)",
 "Galtor": "Sonoridade dura; família GATOR (Host Gator, classe 42) a 91%",
 "Halvo": "Foneticamente igual a \"alvo\", palavra comum (centenas de marcas ativas nas classes 35/42)",
 "Kevro": ".com.br e .app.br ocupados; K artificial; som de \"quero\"",
 "Lavira": "Marca idêntica LAVIRA (classe 35, pedido)",
 "Merivo": "App \"Merivo: Calorie Tracker\" na App Store e merivo.com.br de agência de marketing (2026)",
 "Nolvo": "Próximo de \"novo\" (baixa distintividade, 2.241 ocorrências ativas) e Nolvori (42, pedido)",
 "Quivra": "Marca idêntica QUIVRA concedida na classe 42 (Quivra Tecnologia Ltda.)",
 "Ravelo": "RAVELLO concedida na classe 42 (Oracle Ravello Systems), fonética idêntica",
 "Selvo": "Baixa distintividade (selva/selo: 432 ocorrências ativas); Selvori (35, pedido)",
 "Arvelo": "Família MARVELOUS (classe 9) e sobrenome comum",
 "Dorvan": "Derivação de Orvia (nome proibido): contém \"orv\"",
 "Gestra": "Marca idêntica GESTRA AG concedida nas classes 9/42 e GESTRA na 35",
 "Lirvo": "Confunde-se com \"livro\" na escrita; LIVO APP (9) a 89%",
 "Marvo": "Marca idêntica MARVO concedida na classe 9",
 "Olvio": "Lembra \"olvido\" (esquecimento, em espanhol), péssimo para agenda; EVOLVIO (42, pedido)",
 "Prevo": "Família PREV (PREVOR e PrevON na classe 9)",
 "Ressa": "Contida em milhares de marcas (expressa, impressa, Andressa)",
 "Sevra": "3.107 ocorrências ativas semelhantes (Severa/Serra); baixa distintividade",
 "Tarvo": "TARVOS concedida na classe 42 e na 35",
 "Unira": "UNYRA (classe 42, pedido), fonética idêntica",
 "Valto": "VALTORIA (9) e VALTON (35); sonoridade de \"salto/alto\"",
 "Zarvo": "Sonoridade áspera; ZAREVO (35) e ZARV (9)",
 "Coravo": "Próximo de Corvia/Orvia; Coravox (9, pedido, 92%)",
 "Dantro": "Foneticamente próximo de \"dentro\": DENTRO concedida nas classes 35 e 42 (procs. 913313459 e 931691087)",
 "Fiora": "Marca idêntica FIORA (35) e FIORA IC (42, pedido)",
 "Lunera": "Marca idêntica LUNERA concedida na classe 35 (agência de comunicação e marketing)",
 "Merava": "MERKAVA (35) e Merkkava APP (9/42, pedidos), 92%",
 "Norvel": "NORVELL CLEAN (35, pedido), fonética idêntica",
 "Pivra": "Sonoridade fraca; família PIRA/PIVA (175 ocorrências ativas)",
 "Quarno": "Sonoridade fraca; 716 ocorrências ativas (Carrano, Carnot)",
 "Talvo": "Próximo de \"alvo\" e \"talvez\"; FORTALVO (42, pedido)",
 "Venaro": "Marca idêntica VENARO (classe 35, pedido)",
 "Kova": "Marca idêntica Kôva (35) e COVA/Kowa (classe 9), fonética idêntica",
 "Lumio": "Marca idêntica lumio concedida na classe 9 e LUMIO CRM (42, pedido)",
 "Dovra": "Lê-se como \"dobra\" (b/v); DOVERA (35, pedido)",
 "Ardena": "Família GARDENA/CARDENA (1.845 ocorrências ativas); lembra \"arde\"",
 "Belvo": "Marca idêntica BELVO concedida na classe 42 (Belvo Technologies, fintech)",
 "Cavro": "Sonoridade fraca (cavar/carro); 678 ocorrências ativas",
 "Navelo": "Em inglês evoca \"navel\" (umbigo), prejudica a expansão internacional",
 "Ondara": "Marca idêntica ONDARA concedida na classe 35",
 "Vinto": "VINTOR (42) e VINTORE (9), pedidos; Vinto Adega (35)",
 "Domara": "SaaS homônimo de gestão de imóveis (Domara, domara.rent, no Capterra); DOMARIA (39, concedida, 92%)",
 "Avela": "Igual a \"avelã\" (centenas de marcas)",
 "Sorvel": "Família \"sorve-\" (sorvete), baixa distintividade",
 "Tenvo": "Sonoridade fraca; Tenveo (35) e tenowo (42), ambas concedidas",
 "Livano": "LIVARNO (Lidl) concedida na classe 9, 92%",
 "Brenzo": "Apps \"Brenzo\" de dois desenvolvedores na App Store; Breeno (42)",
 "Corvia": "Derivação de Orvia (terminação -via)",
 "Ilvano": "SILVANO (vários, inclusive na classe 39), 92%",
 "Mervel": "Próximo de Marvel (marca notória) e Merrell",
 "Prisma": "Palavra comum, marca idêntica PRISMA (classe 9, pedido)",
 "Trevo": "Palavra comum, marca idêntica TREVO (classe 9) e Treevo (42)",
 "Varo": "Palavra comum; VARÔ (35)",
 # lote 2
 "Damira": "Marca idêntica Damira (classe 35, pedido 945639503)",
 "Fidaro": "FITARO SOLUÇÕES EM SAÚDE concedida na classe 42 para SaaS (proc. 917193881), diferença só t/d; fidaro.com.br ocupado",
 "Lemara": "LEMMARA concedida na classe 39 (fonética idêntica, proc. 830576657)",
 "Rumeo": "Família RUMO (Rumo S.A. e muitas outras)",
 "Zelano": "Preterido pela variante Zaleno: zelano.com.br em uso por empresa (2025) e família ZELÃO (35)",
 "Tramio": "Trampio e Tramo (classe 9, pedidos), 91–92%",
 "Mirelo": "Mirelo AI (startup alemã de IA, US$ 41 mi em 2025) e mirelo.com.br ocupado",
 "Navari": "NAVARRI (35) fonética idêntica; NAVARINI (39)",
 "Pelano": "Pelando (35, portal de ofertas) e família \"plano\"",
 "Ramelo": "Família CARAMELO; K-RAMELO/ZECA RAMELO (35)",
 "Daveno": "Derivação de Tavena (nome proibido): mesmas consoantes V-N",
 "Teravo": "TERRAVO (35) fonética; Teravoz (42) e TERAVOLT (9)",
 "Tivano": "Derivação de Tavena (T-V-N); TIVAN (9, Linde)",
 "Dalira": "DalLira (35) e família DÁLIA",
 "Valmo": "Família VALMONT (classes 42/39) e Valmor",
 "Zirelo": "ZIELO concedida na classe 42 para SaaS (proc. 921059760), 91%",
 "Sabira": "Família SABIÁ (Sábia, classe 42)",
 "Clarea": "Marca idêntica CLAREA concedida na classe 35",
 "Brivo": "Marca idêntica BRIVO (35) e BRIVO ARQUITETURA (42)",
 "Lemio": "Sonoridade fraca; família LEMI/LEMO",
 "Veluno": "Veluno Tech Ltd (empresa de desenvolvimento de software, Crunchbase); veluno.com.br registrado",
 "Sorane": "Sorane Negócios e Serviços Ltda. é titular do .com.br; app \"Sorane\" na App Store",
 "Ilumo": "Marca idêntica ILUMO (35) e ILLUMIO (42)",
 "Belaro": "Marca idêntica BELARO concedida na classe 9",
 "Cadivo": "Marca idêntica CADIVÓ (35)",
 "Dimara": "DIMARAPA (9) e família DIMAR",
 "Esmera": "Marca idêntica ESMERA (35) e AGÊNCIA esmera (42)",
 "Primeo": "Família PRIME (5.356 ocorrências ativas)",
 "Tenaro": "TENNARO (35, pedido), fonética idêntica",
 "Zelvio": "ZELVO/ZELVI (35) e ZELIO (9, Schneider)",
 "Agilo": "AGILOFT (9) e família ÁGIL",
 "Mareno": "Mareeno concedida na classe 9, fonética idêntica",
 "Saluma": "Evoca salume (frios); SALUMAR (35)",
 "Tamiro": "Marca idêntica Tamiro (classe 9, pedido)",
 "Kaliva": "Marca idêntica Kaliva (35) e próxima de Caliro (proibido)",
 "Velino": "Marca idêntica velino concedida na classe 42 (TK Elevator)",
 "Larimo": None,
 "Fluma": "AGÊNCIA FLUMA (35) e família FLUA",
 "Taluno": "Qualidade insuficiente: soa como \"t'aluno\" (teu aluno)",
 "Davira": "Próximo de Avora (proibido); DAIRA/DAVYA (35)",
 "Lumeno": "Família LUMEN (233 ocorrências ativas)",
 "Serivo": "Próximo de \"sério\" e SERVO (classe 9)",
 "Fidena": "fidena.com.br pertence à DATACREDITO (dados de crédito); FIDENZA (35)",
 "Tessaro": "Marca idêntica TESSARO (35) e TESSARO TRAVEL (39)",
 "Galivo": "Derivação de Caliro (C/G, R/V)",
 "Marelo": "Marca idêntica MARELO (35) e MARELLO MOB (39)",
 "Kemara": "Sonoridade fraca; 679 ocorrências ativas",
 "Venzo": "Marca idêntica VENZO (9) e VENZZO (9)",
 "Brumo": "Família BRUMON (Brumon Tecnologia, classe 9)",
 # lote 3
 "Selano": "Selano Health (app de saúde, África do Sul); selano.com.br é de pessoa com esse sobrenome; SELVANO (35)",
 "Kelano": "CELANO concedida na classe 42 (fonética idêntica)",
 "Nelaro": "Próximo de Elora (proibido), troca vocálica",
 "Palumo": "PALUMBO (35) e PALMO (42)",
 "Ramino": "Sonoridade fraca; família ARAMINOX/CARAMINO",
 "Tamelo": "Sonoridade fraca; TAMEL (35)",
 "Valuma": "Marca idêntica VALUMA (classe 9, pedido)",
 "Zaluna": "Marca idêntica ZALUNA (35)",
 "Daluma": "Marca DALUMA (35, várias)",
 "Gemara": "Termo religioso (comentário do Talmude)",
 "Ilaro": "Família VILARO/Cilaro (35)",
 "Jarina": "Marca JARINA (35)",
 "Faluno": "Sonoridade fraca; Fauno (35)",
 "Miralo": "MIRAKLO! (Mirakl, plataforma SaaS) e MIRALOGIC (42)",
 "Lumaro": "LUMARIO (9, pedido, 92%) e LLUMAR",
 "Nexaro": "Apps \"Nexaro\" (Nexaro One B.V., Nexaro Loyalty) e NEXAR (42, Altium)",
 "Curano": "Lembra \"curando\" (conotação médica)",
 "Teara": "1.290 ocorrências ativas; Terara (9/42)",
 "Dialo": "diálo tecnologia concedida na classe 42",
 "Amelo": "AMELLO (35) fonética idêntica",
 "Belano": "Marca idêntica BELANO (35)",
 "Elano": "Marca idêntica ELANO (35)",
 "Ivaro": "ZIVARO (9) e VIVARO (35)",
 "Jumaro": "Sonoridade fraca; Jumar (35)",
 "Mavelo": "Mavielo concedida na classe 42 e pedido na 9 (92%)",
 "Pamelo": "Em espanhol \"pomelo/pamelo\" é fruta; sonoridade fraca",
 "Simaro": "SYMARO (Siemens) concedida na classe 9, fonética idêntica",
 "Tolano": "Começa com \"tolo\"",
 "Varina": "Lembra \"varinha\"",
 "Lunaro": "Lembra \"lunar\" (palavra comum); LUNAR TECNOLOGIA (42)",
 "Maluno": "Lembra \"aluno\"; MALUNGO (35)",
 "Sarelo": "SAMRELLO concedida na classe 9 (92%); sonoridade fraca",
 "Tiramo": "Lembra \"tiramisu/tiramos\"; TIAMO (9)",
 "Belumo": "Sonoridade fraca; BELLUM (35)",
 "Darelo": "TARELLO concedida nas classes 42 (software) e 9 (app), procs. 922974233 e 923830790, diferença só d/t",
 "Moralo": "Lembra \"moral\"",
 "Neluma": "Marca idêntica NELUMA nas classes 9/42 (A. Raymond, pedido)",
 "Sivano": "SILVANO (vários, inclusive 39)",
 # lote 4
 "Velaro": "Marca idêntica Velaro (classe 9, pedido)",
 "Firmano": "Quase igual a Firmao (CRM no mercado); firmano.com.br ocupado",
 "Serelo": "Marca idêntica SERELO (35)",
 "Nitaro": "Família NITRO",
 "Lumelo": "Sonoridade fraca; LUMEL (35)",
 "Ritano": "Família SAMARITANO",
 "Melaro": "Lembra \"melão\"",
 "Paleno": "Sonoridade fraca; paleo (42)",
 "Valeno": "VALENNO (35) fonética idêntica",
 "Itaro": "Marca idêntica ITARO (35); FITARO (42)",
 "Jalumo": "JAUMO (classe 9, app de encontros)",
 "Ulmaro": "Qualidade insuficiente (média 6,3): sonoridade pouco natural",
 "Melune": "Sonoridade fraca",
 "Dalumo": "Sonoridade fraca; DALU MODAS (35)",
 "Fenelo": "Lembra \"fenol\"",
 "Gilaro": "Sonoridade fraca; GIARO (35)",
 "Lunelo": "Lunélo Papelaria (35, pedido)",
 "Marilo": "Marca idêntica mariló (35)",
 "Norelo": "NORELCO (Philips) concedida na classe 9",
 "Sermelo": "Sonoridade fraca; SERELO (35)",
 "Telano": "Sonoridade fraca; família CASTELANO",
 "Velumo": "VELLUM concedida na classe 42",
 "Zorelo": "Lembra \"orelha\"",
 "Bimaro": "Sonoridade fraca",
 "Celaro": "Lembra \"claro\" (Claro S.A.)",
 "Doluma": "Sonoridade fraca (\"dó\")",
 "Elumo": "Celumo (OPPO, classe 9) e ELUMEO (35)",
 "Faleno": "Lembra \"fallen\"; FALENIO (35)",
 "Lavaro": "Lembra \"lavar\"; Lavro (35)",
 "Numaro": "NUMAR concedida na classe 42",
 "Tarelo": "Marca idêntica TARELO (35) e TARELLO (42)",
 "Venelo": "Lembra \"veneno\"",
}
DESC = {k: v for k, v in DESC.items() if v}
# motivo do Aldora com o número exato
_ald = [o for o in INPI["Aldora"]["ocorrencias"] if o["score"] == 100]
if _ald:
    DESC["Aldora"] = f"Marca idêntica ALDORA concedida na classe 35 (proc. {_ald[0]['numero']})"

CATEG = {}
for n, m in DESC.items():
    if "Derivação" in m or "proibido" in m:
        CATEG[n] = "derivação de nome proibido"
    elif any(x in m for x in ("Marca idêntica", "fonética idêntica", "concedida na classe 42", "concedida na classe 9", "concedidas nas classes", "concedida nas classes")):
        CATEG[n] = "conflito no INPI"
    elif any(x in m for x in ("App", "app", "Tech", "SaaS", "startup", ".com.br", "Health", "CRM")):
        CATEG[n] = "uso de mercado / domínio"
    elif any(x in m for x in ("Sonoridade", "Lembra", "Qualidade", "Evoca", "evoca", "Termo", "Confunde", "Começa", "Em espanhol", "Em inglês", "Igual", "Palavra comum", "Família", "soa")):
        CATEG[n] = "qualidade / palavra comum"
    else:
        CATEG[n] = "conflito no INPI"

# ---------------------------------------------------------------- consolidação
reg = []
for nome, a in A.items():
    media = round(statistics.mean(a["notas"]), 1)
    reg.append(dict(nome=nome, **a, media=media, dominios=dom_status(nome), app_store=apps(nome),
                    inpi_total_semelhantes=INPI[nome]["total_semelhantes"],
                    inpi_por_nivel=INPI[nome]["por_nivel"],
                    inpi_mais_proximas=[{k: o[k] for k in ("numero", "nome", "classes", "situacao", "titulares", "score", "motivo")}
                                        for o in proximas(nome)],
                    inpi_variantes=variantes(a["var"])))
ordem_status = {"promissor": 0, "pendências": 1}


def dig(r):
    d = r["dominios"]
    return (5 if d["com.br"].startswith("disp") else 0) + (3 if d["app.br"].startswith("disp") else 0) + (2 if "à venda" in d["com"] or d["com"].startswith("disp") else 0)


reg.sort(key=lambda r: (ordem_status[r["status"]], -r["media"], -dig(r)))
for i, r in enumerate(reg, 1):
    r["ranking"] = i
    r["disponibilidade_digital"] = dig(r)

gerados = sorted(set(DESC) | set(A))
json.dump({"data_consulta": DATA, "base_inpi": RPI_BASE, "total_gerados": len(gerados),
           "aprovados": len(reg), "promissores": sum(r["status"] == "promissor" for r in reg),
           "com_pendencias": sum(r["status"] == "pendências" for r in reg),
           "ranking": reg,
           "descartados": [{"nome": n, "categoria": CATEG[n], "motivo": DESC[n]} for n in sorted(DESC)]},
          open(f"{BASE}/resultados.json", "w"), ensure_ascii=False, indent=1)

with open(f"{BASE}/matriz-comparativa.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["ranking", "nome", "classificacao", *CRIT, "media", "inpi_semelhantes_total", "inpi_criticos", "inpi_altos",
                "marca_mais_proxima", "dominio_com_br", "dominio_app_br", "dominio_com", "app_store_homonimo",
                "disponibilidade_digital_0a10", "principal_risco"])
    for r in reg:
        mp = r["inpi_mais_proximas"][0] if r["inpi_mais_proximas"] else None
        w.writerow([r["ranking"], r["nome"], r["status"], *r["notas"], r["media"], r["inpi_total_semelhantes"],
                    r["inpi_por_nivel"]["crítico"], r["inpi_por_nivel"]["alto"],
                    f"{mp['nome']} ({mp['classes']}, {mp['situacao']}, {mp['score']}%, proc. {mp['numero']})" if mp else "nenhuma ≥ 88%",
                    r["dominios"]["com.br"], r["dominios"]["app.br"], r["dominios"]["com"],
                    "; ".join(f"{a['app']} ({a['desenvolvedor']})" for a in r["app_store"]) or "nenhum",
                    r["disponibilidade_digital"], r["riscos"]])
    for d in sorted(DESC):
        w.writerow(["", d, f"descartado ({CATEG[d]})", *[""] * len(CRIT), "", INPI.get(d, {}).get("total_semelhantes", ""), INPI.get(d, {}).get("por_nivel", {}).get("crítico", ""),
                    INPI.get(d, {}).get("por_nivel", {}).get("alto", ""), "", "", "", "", "", "", DESC[d]])

# ---------------------------------------------------------------- markdown
def fmt_marca(o):
    return f"{o['nome']} (classe {o['classes']}, {o['situacao']}, {o['score']}%, proc. {o['numero']}, {(o['titulares'] or '').split('(')[0].strip()[:45]})"


top = reg[:5]
L = [f"# Rodada 2 de naming — 20 novos nomes (triagem)\n",
     f"**Data:** {DATA} · **Natureza:** levantamento técnico de disponibilidade e qualidade de marca; **não é parecer jurídico nem garantia de registro**.\n",
     "> **Revisão de 21/11/2026:** a auditoria final (`auditoria-final-3-finalistas.md`) achou falsos negativos para Lindaro (LINDARA, LINARA e TÍNDARO), que passou a \"com pendências\", e ajustou os riscos de Joreva e Salendo.\n",
     "## Resultado em uma frase\n",
     f"Foram gerados **{len(gerados)} nomes** e triados no INPI (RPI), em domínios, na App Store e na web. **Só {len(reg)} passaram nos critérios sem rebaixar a régua**: "
     f"{sum(r['status']=='promissor' for r in reg)} promissores e {sum(r['status']=='pendências' for r in reg)} com pendências. "
     f"Por isso a lista tem **{len(reg)} nomes, e não 20**. Os outros {len(DESC)} foram descartados com motivo registrado.\n",
     "## Top 5\n",
     "| # | Nome | Média | INPI (classes 9/35/42/39) | .com.br | .app.br | .com | Mercado |",
     "|---|---|---|---|---|---|---|---|"]
for r in top:
    mp = r["inpi_mais_proximas"][0] if r["inpi_mais_proximas"] else None
    L.append(f"| {r['ranking']} | **{r['nome']}** | {r['media']:.1f} | {'nenhuma semelhante ≥ 88%' if not mp else 'mais próxima: ' + mp['nome'] + ' (' + mp['classes'] + ', ' + str(mp['score']) + '%)'} | "
             f"{r['dominios']['com.br'].split(' —')[0]} | {r['dominios']['app.br'].split(' —')[0]} | {r['dominios']['com'].split(' —')[0]} | {r['mercado'].split('.')[0]}. |")
L += ["", "## Ranking completo (ordem de preferência)\n",
      "A ordem considera primeiro o risco (promissores antes dos nomes com pendências), depois a média de qualidade e por fim a disponibilidade digital.\n",
      "| # | Nome | Classificação | Média | Conceito |", "|---|---|---|---|---|"]
for r in reg:
    L.append(f"| {r['ranking']} | **{r['nome']}** | {r['status']} | {r['media']:.1f} | {r['conceito']} |")
for titulo, st in (("Candidatos promissores", "promissor"), ("Candidatos com pendências", "pendências")):
    L += ["", f"## {titulo}\n"]
    for r in [x for x in reg if x["status"] == st]:
        L += [f"### {r['ranking']}. {r['nome']}\n",
              f"- **Conceito:** {r['conceito']}",
              f"- **Personalidade:** {r['personalidade']}",
              "- **Notas (0–10):** " + ", ".join(f"{c.replace('_', ' ')} {n}" for c, n in zip(CRIT, r["notas"])) + f" → **média {r['media']:.1f}**",
              f"- **Vantagens:** {r['vantagens']}",
              f"- **Riscos:** {r['riscos']}",
              f"- **Domínios:** .com.br {r['dominios']['com.br']}; .app.br {r['dominios']['app.br']}; .com {r['dominios']['com']}",
              ""]
L += ["## Descartados\n",
      "Ficam separados dos recomendados. A evidência completa está em `pesquisa-inpi.md`, `pesquisa-mercado.md` e `resultados.json`.\n",
      "| Nome | Categoria | Motivo |", "|---|---|---|"]
for n in sorted(DESC, key=lambda x: (CATEG[x], x)):
    L.append(f"| {n} | {CATEG[n]} | {DESC[n]} |")
L += ["", "> Os significados e associações acima são **conceitos de posicionamento**, não etimologias comprovadas."]
open(f"{BASE}/20-novos-nomes.md", "w").write("\n".join(L) + "\n")

# pesquisa-inpi.md
L = ["# Pesquisa INPI — rodada 2\n", f"**Base:** {RPI_BASE}. **pePI:** inacessível a partir deste ambiente (conexão recusada pelo servidor). "
     "A situação de cada processo é inferida pelo **último despacho publicado** e deve ser confirmada no pePI (https://busca.inpi.gov.br/pePI/).\n",
     "**Critério:** marcas ativas (concedidas, pedidos em andamento e indeferidas com recurso) com semelhança ≥ 88% nas classes 9, 35, 42 e 39. "
     "Inclui marcas nominativas e mistas e designações do Protocolo de Madri publicadas na RPI. Também foram buscadas **variantes de grafia** que a normalização fonética não cobre (b/v, f/v, t/d, s/z, troca de vogal inicial), com corte de 92%.\n"]
for r in reg:
    L += [f"## {r['ranking']}. {r['nome']} ({r['status']})\n",
          f"- Ocorrências semelhantes no índice (todas as classes e situações): {r['inpi_total_semelhantes']}; ativas e relevantes por nível: {r['inpi_por_nivel']}"]
    if r["inpi_mais_proximas"]:
        L.append("- Marcas ativas mais próximas nas classes 9/35/42/39:")
        L += [f"  - {fmt_marca(o)} — {o['motivo']}" for o in r["inpi_mais_proximas"]]
    else:
        L.append("- **Nenhuma marca ativa com semelhança ≥ 88% nas classes 9/35/42/39.**")
    for v in r["inpi_variantes"]:
        L.append(f"- Variante **{v['variante']}**: " + ("; ".join(f"{o['nome']} ({o['classes']}, {o['situacao']}, proc. {o['numero']})" for o in v["ocorrencias"]) or "nenhuma ocorrência ativa ≥ 92% nas classes relevantes"))
    L.append("")
L += ["## Principais conflitos que eliminaram candidatos\n", "| Nome | Motivo |", "|---|---|"]
L += [f"| {n} | {DESC[n]} |" for n in sorted(DESC) if CATEG[n] == "conflito no INPI"]
open(f"{BASE}/pesquisa-inpi.md", "w").write("\n".join(L) + "\n")

# pesquisa-mercado.md
L = ["# Pesquisa de mercado — rodada 2\n",
     "Buscas na web por nome (empresas brasileiras e estrangeiras, SaaS/CRM/ERP/agenda, diretórios como Capterra, Crunchbase e GetApp, App Store e Google Play). "
     "Os cinco primeiros do ranking tiveram busca **estendida**, incluindo Google Play. Alguns nomes de menor prioridade foram pesquisados em buscas combinadas (dois ou três nomes por consulta), o que é indicado.\n"]
for r in reg:
    L += [f"## {r['ranking']}. {r['nome']}\n", r["mercado"],
          "\n- App Store (API oficial, BR e EUA): " + ("; ".join(f"{a['app']} — {a['desenvolvedor']} ({a['loja']})" for a in r["app_store"]) or "nenhum app com o nome."),
          ("- Fontes: " + " · ".join(r["urls"])) if r["urls"] else "- Fontes: resultados de busca sem ocorrência do nome.", ""]
L += ["## Descartes por uso de mercado ou domínio\n", "| Nome | Evidência |", "|---|---|"]
L += [f"| {n} | {DESC[n]} |" for n in sorted(DESC) if CATEG[n] == "uso de mercado / domínio"]
L += ["", "Fontes dos descartes: Mirelo AI — https://techcrunch.com/2025/12/15/mirelo-raises-41m-from-index-and-a16z-to-solve-ai-videos-silent-problem/ · "
      "Domara — https://www.capterra.com/p/10038293/Domara/ · Veluno Tech — https://www.crunchbase.com/organization/veluno-tech-ltd · "
      "Firmao — https://www.appvizer.es/relacion-cliente/software-crm/firmao"]
open(f"{BASE}/pesquisa-mercado.md", "w").write("\n".join(L) + "\n")

# dominios-e-aplicativos.md
L = ["# Domínios e aplicativos — rodada 2\n",
     "**Fontes:** RDAP oficial do Registro.br (.com.br, .app.br) e da Verisign (.com); API oficial de busca da Apple (lojas do Brasil e dos EUA, até 25 resultados). "
     "HTTP 404 no RDAP = **disponível confirmado**. \"À venda\" = DNS de marketplace (Afternic, BuyDomains, Sedo, Atom). Uso dos domínios registrados **não verificado** (acesso aos sites não liberado).\n",
     "| # | Nome | .com.br | .app.br | .com | App Store (nome exato) | Disponibilidade (0–10) |", "|---|---|---|---|---|---|---|"]
for r in reg:
    L.append(f"| {r['ranking']} | {r['nome']} | {r['dominios']['com.br']} | {r['dominios']['app.br']} | {r['dominios']['com']} | "
             f"{'; '.join(a['app'] + ' (' + a['desenvolvedor'] + ')' for a in r['app_store']) or 'nenhum'} | {r['disponibilidade_digital']} |")
L += ["", "Disponibilidade digital: .com.br livre = 5; .app.br livre = 3; .com livre ou à venda = 2. **Domínio livre não significa marca livre.**",
      "", "Google Play: sem API pública e domínio não liberado; verificado só por busca na web para os cinco primeiros (nenhum app com o nome exato)."]
open(f"{BASE}/dominios-e-aplicativos.md", "w").write("\n".join(L) + "\n")
print("ok", len(reg), "aprovados;", len(DESC), "descartados;", len(gerados), "gerados")
for r in reg:
    print(r["ranking"], r["nome"], r["status"], r["media"], r["disponibilidade_digital"])
