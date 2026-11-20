# Metodologia e limitações — rodada 2 de naming

**Data da consulta:** 20/11/2026 · **Ambiente:** sessão em nuvem com rede restrita (ambiente "devlucascosta"). Endereços liberados: revistas.inpi.gov.br, busca.inpi.gov.br, www.gov.br, branddb.wipo.int, api.branddb.wipo.int, rdap.registro.br, rdap.verisign.com e itunes.apple.com.

## 1. Criação dos nomes

- **192 nomes inventados**, gerados em quatro lotes (60 + 51 + 44 + 37). Cada lote foi gerado depois de ver o que o anterior eliminou, para buscar sonoridades menos ocupadas.
- **Regras de criação:** 2 a 4 sílabas; leitura direta em português; sem AI/Tech/App/Digital; sem palavras comuns; sem variações de marcas conhecidas.
- **Nomes proibidos:** Orvia, Rotiva, Novera, Vértia, Atempo, Plenna, Avora, Ordina, Pontta, Oryza, Nivora, Movent, Tavora, Elora, Veyra, Solven, Averto, Tavena, Oltara, Caliro, Orrena, AgendAI e Agendaí. Foram evitadas também as terminações e raízes desses nomes (-vora, -elora, -via, "orv", T-V-N de Tavena, C-L-R de Caliro). Oito candidatos que escaparam na geração foram descartados por isso, na revisão: Corvia, Dorvan, Daveno, Tivano, Davira, Galivo, Kaliva e Nelaro.
- **Não houve redução de critério:** só **18** nomes passaram. A lista tem 18, não 20.

## 2. Funil de triagem

| Etapa | Fonte | Eliminados |
|---|---|---|
| 1. INPI, nome exato e fonético | Índice local da RPI | Marca idêntica ou de fonética idêntica ativa nas classes 9/35/42/39; famílias com centenas de marcas ativas |
| 2. Revisão de qualidade e derivação | Avaliação profissional | Palavra comum, conotação ruim (Olvio ≈ "olvido", Navelo ≈ "navel", Tolano ≈ "tolo"), derivação de nome proibido |
| 3. Domínios e App Store | RDAP oficial, API da Apple | .com.br de empresa ativa no ramo, apps homônimos |
| 4. Mercado | Buscas na web (padrão e estendidas) | Empresas e SaaS homônimos (Mirelo AI, Domara, Veluno Tech, Firmao/Firmano, Nexaro) |
| 5. Variantes de grafia | Índice local da RPI | Marcas a uma letra de distância nas classes 9/42 (FITARO × Fidaro, TARELLO × Darelo, ZIELO × Zirelo, DENTRO × Dantro) |
| 6. Notas de qualidade | Avaliação profissional | Média abaixo de 6,5 (Ulmaro, 6,3) |

## 3. INPI (Brasil)

- **Fonte:** Revista da Propriedade Industrial (RPI), seção Marcas, arquivos XML oficiais (`https://revistas.inpi.gov.br/txt/RM{nº}.zip`), **edições 2220 (23/07/2013) a 2915 (17/11/2026), 696 edições**. O índice local tem 5,3 milhões de processos e 15,3 milhões de despachos. Ele foi **reaproveitado sem reindexação** e sem novo download.
- **Busca:** a mesma da rodada 1 (`../../dados/buscar_nomes.py`). Compara cada palavra de cada marca por igualdade, igualdade fonética após normalização para o português, inclusão do nome e semelhança aproximada ≥ 80%.
- **Classificação:** `../../dados/classificar_conflitos.py` calcula a situação pelo último despacho e marca os níveis crítico/alto (classes 9/35/42) e moderado (classes vizinhas, inclusive 39).
- **Variantes extras:** a normalização não cobre b/v, f/v, t/d, s/z nem a troca de vogal inicial, lacuna apontada na auditoria de completude da rodada 1. Por isso foram pesquisadas 42 variantes dos finalistas (`dados/inpi_variantes*_conflitos.json`). **Quatro finalistas caíram nessa etapa.**
- **Cobertura:** marcas nominativas e mistas e designações do Protocolo de Madri publicadas na RPI. **Ficam fora:** cerca de 80 mil marcas vigentes só figurativas ou tridimensionais (sem nome); pedidos antigos sem despacho desde 07/2013; direitos não registrados, como marca notória (art. 126 da LPI) e uso anterior de boa-fé (art. 129, §1º).
- **pePI:** inacessível, pois o servidor recusa as conexões deste ambiente. **A situação dos processos é inferida pelo último despacho publicado até 17/11/2026 e precisa ser confirmada no pePI.**

## 4. Internacional

- **WIPO Global Brand Database:** **não consultada.** Ela exige verificação anti-robô (ALTCHA), e a automação foi bloqueada pelas regras de permissão desta sessão, restrição que não foi contornada. **Por isso nenhum nome é declarado livre no plano internacional.**
- Designações internacionais com efeito no Brasil aparecem na RPI e foram consideradas, como IBM TELUM, LIVARNO (Lidl), SYMARO (Siemens), NELUMA (A. Raymond) e RAVELLO (Oracle).
- O uso apenas estrangeiro veio de buscas na web (Crunchbase, Capterra, TechCrunch, Trustpilot, D&B, GitHub, App Store).

## 5. Mercado, apps e domínios

- **Web:** busca padrão para todos os sobreviventes da etapa 3 e **busca estendida** para os cinco primeiros, incluindo Google Play. Nomes de prioridade menor foram pesquisados em consultas combinadas, que são menos precisas; isso está indicado em `pesquisa-mercado.md`.
- **App Store:** API oficial da Apple, lojas do Brasil e dos EUA, até 25 resultados por nome. Respostas 403 foram refeitas automaticamente, com espera crescente.
- **Google Play:** não há API pública e o domínio não está liberado. Foi verificado só por busca na web, para os cinco primeiros.
- **Domínios:** RDAP do Registro.br (.com.br, .app.br) e da Verisign (.com). HTTP 404 = disponível confirmado. Domínios registrados com DNS de marketplace (Afternic, BuyDomains, Sedo, Atom) estão marcados "à venda". **Nenhum .com está livre**; os de Salendo, Joreva, Zaleno e Zimeno parecem estar à venda.
- **Redes sociais e Juntas Comerciais:** não verificadas, porque exigem login ou não estão liberadas.

## 6. Notas de qualidade

São nove critérios de 0 a 10: sonoridade, pronúncia, escrita, memorização, originalidade, distintividade, aparência visual, potencial de expansão e adequação ao SaaS. As notas são **avaliação profissional qualitativa** e não compensam riscos jurídicos. O ranking ordena primeiro por risco (promissor antes de "com pendências"), depois pela média e por fim pela disponibilidade digital (.com.br livre = 5, .app.br livre = 3, .com livre ou à venda = 2).

Os significados e associações são **conceitos de posicionamento**, nunca etimologias comprovadas.

## 7. Arquivos

| Arquivo | Conteúdo |
|---|---|
| `20-novos-nomes.md` | Ranking, top 5, fichas, descartados |
| `pesquisa-inpi.md` | Marcas mais próximas e variantes por candidato |
| `pesquisa-mercado.md` | Empresas, apps e fontes |
| `dominios-e-aplicativos.md` | RDAP e App Store |
| `matriz-comparativa.csv` · `resultados.json` | Dados estruturados (aprovados e descartados) |
| `dados/inpi_conflitos*.json` | Ocorrências ativas classificadas por lote |
| `dados/inpi_variantes*_conflitos.json` | Variantes de grafia |
| `dados/dominios_appstore.json` | Respostas RDAP e App Store |
| `../../dados/gerar_relatorios_rodada02.py` | Gera os relatórios a partir dos dados e das avaliações |

Os arquivos brutos de semelhança (cerca de 500 MB, todas as ocorrências) passam do limite do GitHub. Eles ficaram no ambiente temporário e podem ser recriados com `buscar_nomes.py`.

## 8. Ressalvas

- **Nenhum nome é declarado juridicamente disponível.** A ausência no índice é ausência de evidência, não garantia.
- Antes de adotar qualquer nome, recomenda-se:
  1. busca formal no pePI, inclusive figurativa, nas classes 9, 35, 42 e 39;
  2. consulta à WIPO;
  3. parecer de advogado de propriedade industrial;
  4. depósito rápido do nome escolhido.
- Nada no SaaS (código, banco de dados) nem na identidade visual foi alterado. Nenhum logo foi criado nesta etapa.
