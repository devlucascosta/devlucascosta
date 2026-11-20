# Fontes e metodologia — auditoria de naming (21 candidatos)

**Data da consulta:** 20/11/2026 (horário de Brasília) · **Ambiente:** sessão em nuvem com acesso de rede restrito, usando o ambiente pessoal "devlucascosta". Endereços liberados: revistas.inpi.gov.br, www.gov.br, busca.inpi.gov.br, branddb.wipo.int, api.branddb.wipo.int, rdap.registro.br, rdap.verisign.com e itunes.apple.com.

## 1. INPI (Brasil)

| Item | Detalhe |
|---|---|
| Fonte | **Revista da Propriedade Industrial (RPI), seção Marcas, arquivos XML oficiais**: `https://revistas.inpi.gov.br/txt/RM{nº}.zip` |
| Cobertura | **Edições 2220 (23/07/2013) a 2915 (17/11/2026)**: 696 edições, sem lacunas. As edições 2511, 2776 e 2777 falharam na primeira tentativa e foram reprocessadas com sucesso. |
| Edições 2000–2219 (2009–2013) | Publicadas em formato texto antigo, não processado no índice. **Para marcas nominativas e mistas, isso não afeta a cobertura de vigentes.** Todo registro em vigor teve concessão ou prorrogação depois de julho de 2013 (o prazo é de 10 anos). A auditoria conferiu que, dos registros vigentes, 2.316.722 (mistas e nominativas) estão no índice com nome, e apenas **9** com elemento nominativo ficaram sem nome. **Exceções:** (a) 79.589 marcas **figurativas** e 365 **tridimensionais** vigentes, que não têm nome; (b) pedidos depositados antes de 07/2013 e parados desde então, sem despacho posterior; (c) direitos não registrados, como marca notoriamente conhecida (art. 126 da LPI) e uso anterior de boa-fé (art. 129, §1º), que não aparecem na RPI. Detalhes em `auditoria-completude.md`. |
| Índice local | `rpi_marcas.sqlite`: **5,3 milhões de processos e 15,3 milhões de despachos**. Ficou no ambiente temporário, com 5,8 GB, grande demais para o git. Os scripts permitem reconstruí-lo. |
| Busca | Para cada candidato, compara cada palavra do nome de todas as marcas por: (a) igualdade; (b) igualdade fonética após normalização para o português (acentos, y→i, w→v, ph→f, k→c, qu→c, letras duplicadas, h inicial); (c) o nome contido em uma palavra; (d) semelhança aproximada ≥ 80% (rapidfuzz). |
| Situação | Calculada pelo último despacho relevante: concedido, pedido em andamento, indeferido (com ou sem recurso), arquivado, extinto ou caducado. Os conflitos considerados são as marcas **ativas**. |
| Relevância | "Crítico" = semelhança ≥ 92 nas classes 9/35/42; "alto" = 88–91 nas classes 9/35/42; "moderado" = classes próximas (16, 36, 38, 39, 41, 45); "baixo" = demais classes. Cada conflito principal foi revisado manualmente para descartar falsos positivos, como Ordina dentro de "Coordinati" ou Pontta × "Ponta Grossa". |
| Classificação de Nice | **Lista oficial NCL 13-2026** do INPI (https://www.gov.br/inpi/pt-br/servicos/marcas/classificacao-marcas/ListadeNiceNCL132026.pdf). Termos conferidos: Software como serviço [SaaS] (42, 420221), Programas de computador baixáveis (9, 090659), Serviços de marcação de compromissos [funções de escritório] (35, 350130) e Reservas para transporte (39, 390084). |
| pePI | **Inacessível**: o servidor do INPI recusou as conexões vindas deste ambiente. O link de consulta de cada processo é a busca por número em https://busca.inpi.gov.br/pePI/. |

## 2. Internacional

- **WIPO Global Brand Database:** **não consultada.** A página exige uma verificação anti-robô (ALTCHA). A tentativa de automatizá-la foi bloqueada pelas regras de permissão desta sessão, e essa restrição não foi contornada.
- **Designações do Protocolo de Madri com efeito no Brasil:** estão incluídas, porque são publicadas na RPI (natureza "Madri"). Exemplos: FORVIA, SOLVENTUM, CHROMAVERTO, AGENDIA.
- **Ocorrências apenas estrangeiras:** vieram de buscas na web (GetApp, Capterra, B2B Stack, SaaSBrowser, ZoomInfo, Crunchbase e sites oficiais), registradas em `dados/mercado.json`.

## 3. Mercado e lojas de apps

- **Buscas na web:** 21 buscas padrão, uma por nome, mais 4 buscas estendidas para os candidatos com menos ocorrências (Tavena, Caliro, Averto, Oltara/Orrena). As URLs estão em `dados/mercado.json` e em `analise-individual.md`.
- **App Store:** API oficial de busca da Apple (`itunes.apple.com/search`), lojas do Brasil e dos EUA, até 25 resultados por nome. Sete consultas falharam com erro 403 (Rotiva/BR, Avora/EUA, Ordina/BR e EUA, Movent/EUA, Tavena/BR) e **foram refeitas com sucesso na auditoria**. Os dados estão em `dados/dominios_appstore.json`.
- **Google Play:** não consultado diretamente. Não há API pública, e o domínio não estava liberado. Para os quatro finalistas, foram feitas buscas na web incluindo "Google Play", sem ocorrências do nome exato.
- **Redes sociais:** não verificadas. A disponibilidade de @ exige login ou serviços de terceiros.

## 4. Domínios

- **.com.br e .app.br:** RDAP oficial do Registro.br (`rdap.registro.br/domain/…`). HTTP 404 significa domínio inexistente, classificado como "Disponível confirmado". Houve quatro respostas 403 (limite de requisições), refeitas com intervalo maior.
- **.com:** RDAP da Verisign (`rdap.verisign.com/com/v1/domain/…`).
- **Uso aparente:** o acesso aos sites não foi liberado. Os domínios registrados aparecem como "uso não verificado", exceto quando o DNS indica estacionamento ou venda (Afternic).

## 5. Qualidade da marca

As notas de 0 a 10 (sonoridade, pronúncia, escrita, memorização, distintividade, aparência de software e potencial de expansão) são **avaliação profissional qualitativa**, com justificativa em `analise-individual.md`. A "disponibilidade digital" é objetiva: .com.br livre vale 5, .app.br livre vale 3 e .com livre vale 2. **As notas não compensam conflitos jurídicos.**

## 6. Arquivos e scripts (reprodutíveis)

| Arquivo | Função |
|---|---|
| `../dados/indexar_rpi.py` | Baixa e indexa as edições da RPI (XML) em SQLite |
| `../dados/buscar_nomes.py` | Busca nomes semelhantes no índice (exatos, fonéticos e aproximados) |
| `../dados/classificar_conflitos.py` | Classifica a situação e a relevância de cada ocorrência |
| `../dados/dominios_apps.py` | Consulta RDAP (Registro.br/Verisign) e App Store |
| `../dados/gerar_relatorios_naming.py` | Gera a matriz, o JSON e a análise individual |
| `dados/inpi_semelhantes.json` · `dados/inpi_conflitos.json` | Resultados completos do INPI por candidato |
| `dados/dominios_appstore.json` · `dados/mercado.json` · `dados/qualidade.json` | Dados de domínios, lojas, mercado e notas |

## 7. Ressalvas

- Nenhum nome é declarado juridicamente livre. A classificação reflete apenas as fontes acima.
- Os dados da RPI mostram o último despacho **publicado** até 17/11/2026. Petições e decisões posteriores precisam ser confirmadas no pePI.
- A pesquisa de AgendAI (`../verificacao-nome-agendai.md`) ficou arquivada e **não foi reaproveitada como resultado** dos novos candidatos. Foram reaproveitados apenas a metodologia, o ambiente e as fontes.
