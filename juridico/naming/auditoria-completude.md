# Auditoria de completude — pesquisa dos 21 nomes

**Data:** 20/11/2026 · **Método:** revisão dos arquivos existentes (`juridico/naming/`, `juridico/dados/`), do índice local da RPI e do histórico de execução. Nada foi reindexado nem baixado de novo. Só foram feitas novas consultas onde havia lacuna comprovada, cada uma com o motivo registrado na seção 3.

## 1. Resultado geral

**A pesquisa preliminar dos 21 nomes está concluída, com ressalvas.** Todos os 21 passaram pelas mesmas etapas centrais: busca no índice da RPI, domínios, App Store, busca de mercado e notas de qualidade. A auditoria, porém:

- **encontrou e corrigiu 4 problemas:**
  1. 7 consultas à App Store tinham falhado com erro 403 (uma do finalista Tavena) e foram refeitas.
  2. Os achados das buscas aprofundadas não estavam registrados em `mercado.json`; foram incluídos.
  3. O JSON do INPI dizia "916 edições indexadas", quando eram 696 edições válidas; corrigido.
  4. A afirmação de cobertura de "todo registro vigente" valia só para marcas com nome; ajustada.
- **alterou uma classificação:** **Oltara passou de "promissor" para "risco moderado".** Uma checagem de variantes encontrou **ALTARA** concedida na classe 35 e **ALIENWARE ALTARA (Dell)** concedida na classe 9.
- **acrescentou pendências ao Averto:** o domínio .com.br é de uma empresa de tecnologia, e há um indício não confirmado de app homônimo.

**Finalistas após a auditoria:** **Tavena** e **Caliro** (os mais seguros) e **Averto** (com pendências). Oltara e Orrena ficam como alternativas moderadas.

## 2. Os 21 nomes × etapas

Legenda: **C** = CONCLUÍDA · **P** = PARCIAL · **NR** = NÃO REALIZADA · **NV** = NÃO VERIFICÁVEL.

| Nome | INPI/RPI | Idênticas e semelhantes | Fonética | Classes 9/35/42 | Situação dos processos | Empresas e concorrentes | App Store | Google Play | Domínios | Redes sociais |
|---|---|---|---|---|---|---|---|---|---|---|
| Orvia | C | C | P¹ | C | P² | P³ | C | NR | C | NV |
| Rotiva | C | C | P¹ | C | P² | P³ | C⁴ | NR | C | NV |
| Novera | C | C | P¹ | C | P² | P³ | C | NR | C | NV |
| Vértia | C | C | P¹ | C | P² | P³ | C | NR | C | NV |
| Atempo | C | C | P¹ | C | P² | P³ | C | NR | C | NV |
| Plenna | C | C | P¹ | C | P² | P³ | C | NR | C | NV |
| Avora | C | C | P¹ | C | P² | P³ | C⁴ | NR | C | NV |
| Ordina | C | C | P¹ | C | P² | P³ | C⁴ | NR | C | NV |
| Pontta | C | C | P¹ | C | P² | P³ | C | NR | C | NV |
| Oryza | C | C | P¹ | C | P² | P³ | C | NR | C | NV |
| Nivora | C | C | P¹ | C | P² | P³ | C | NR | C | NV |
| Movent | C | C | P¹ | C | P² | P³ | C⁴ | NR | C | NV |
| Tavora | C | C | P¹ | C | P² | P³ | C | NR | C | NV |
| Elora | C | C | P¹ | C | P² | P³ | C | NR | C | NV |
| Veyra | C | C | P¹ | C | P² | P³ | C | NR | C | NV |
| Solven | C | C | P¹ | C | P² | P³ | C | NR | C | NV |
| Orrena | C | C | P¹ | C | P² | P³ (2 buscas) | C | NR | C | NV |
| **Tavena** | C | C | **C**⁵ | C | P² | P³ (3 buscas) | C⁴ | P⁶ | C | NV |
| **Caliro** | C | C | **C**⁵ | C | P² | P³ (3 buscas) | C | P⁶ | C | NV |
| **Averto** | C | C | **C**⁵ | C | P² | P³ (3 buscas) | C⁷ | P⁶ | C | NV |
| **Oltara** | C | C | **C**⁵ | C | P² | P³ (2 buscas) | C | P⁶ | C | NV |

¹ Normalização fonética aplicada: acentos, y/i, w/v, ph/f, k/c, qu/c, letras duplicadas e h inicial, mais semelhança aproximada ≥ 80%. **Não** foram tratadas as trocas b↔v, s↔z, x↔ch nem a troca da vogal inicial. Para os nomes eliminados, a lacuna não muda a conclusão, porque já há conflitos suficientes.
² Situação **inferida pelo último despacho publicado na RPI até 17/11/2026**, sem confirmação no pePI.
³ Buscas na web e diretórios de software (GetApp, Capterra, B2B Stack, ZoomInfo, Crunchbase). **Juntas Comerciais e Receita Federal (nomes empresariais) não foram consultadas.**
⁴ A consulta inicial falhou com erro 403 e foi **refeita na auditoria com sucesso**.
⁵ Na auditoria, foram verificadas no índice inteiro as variantes Aberto/Abertto/Avertto; Tabena/Tavenna; Kaliro/Calirro/Calyro; Altara/Oltarra/Ultara/Oltera.
⁶ Busca na web incluindo "Google Play"; a loja não foi consultada diretamente.
⁷ Busca refeita na auditoria (BR e EUA): só "Irena Averto". Um buscador indica um app "Averto" da desenvolvedora Smart Path na App Store BR, **não confirmado** pela API da Apple.

## 3. Pesquisas efetivamente realizadas

| Fonte | Situação | O que foi feito |
|---|---|---|
| **INPI — RPI (XML oficial)** | **CONCLUÍDA** | Edições 2220–2915 (23/07/2013–17/11/2026), 696 edições, sem lacunas. Índice local com 5.319.246 processos e 15.277.317 despachos. |
| **INPI — Nice NCL 13-2026** | **CONCLUÍDA** | Lista oficial consultada, com os termos das classes 9, 35, 39 e 42 conferidos. |
| **Registro.br (RDAP)** | **CONCLUÍDA** | .com.br e .app.br dos 21 nomes (42 consultas). As quatro respostas 403 foram refeitas. |
| **Verisign (RDAP .com)** | **CONCLUÍDA** | 21 consultas; todos os .com estão registrados. |
| **Apple App Store (API)** | **CONCLUÍDA** (após a auditoria) | Brasil e EUA, 21 nomes; as 7 falhas foram refeitas. |
| **Buscadores e empresas** | **PARCIAL** | Uma busca padrão por nome (21) + 4 buscas aprofundadas + 4 buscas dedicadas aos finalistas na auditoria. Faltam Juntas Comerciais e Receita Federal. |
| **Verificação de correspondência** | **CONCLUÍDA** | Os 148 processos citados nos relatórios foram conferidos no índice: número e nome batem em 100% dos casos. |
| **Cobertura de vigentes sem nome** | **CONCLUÍDA** | Ver seção 6. Também foi tentado recuperar nomes nas edições antigas em texto (171 arquivos locais): só 32 recuperados, porque esses registros são figurativos. |

**Novas consultas feitas na auditoria, com o motivo de cada uma:**
1. **App Store:** 7 consultas tinham falhado com 403, e uma delas era do finalista Tavena.
2. **Busca local de variantes fonéticas dos 4 finalistas:** a normalização não cobria b/v nem a vogal inicial. Foi assim que surgiu o ALTARA.
3. **4 buscas na web dedicadas aos finalistas** (Brasil e Google Play): a busca de Oltara tinha sido feita em conjunto com Orrena, e o Google Play nunca tinha sido verificado.
4. **Consulta pontual à API da Apple** para checar o indício do app "Averto".

## 4. Pesquisas incompletas ou não realizadas

| Fonte | Situação | Motivo |
|---|---|---|
| **INPI pePI** (andamento atual, petições, recursos, opoentes) | **BLOQUEADA** | O servidor do INPI recusa conexões deste ambiente de nuvem. |
| **WIPO Global Brand Database** | **BLOQUEADA** | Exige verificação anti-robô (ALTCHA). A automação foi negada pelas permissões da sessão e não foi contornada. As designações do Protocolo de Madri para o Brasil **aparecem na RPI** e foram consideradas. |
| **Google Play** | **NÃO REALIZADA** (só busca na web para os finalistas) | Não há API pública, e o domínio não estava liberado. |
| **Redes sociais (@)** | **NÃO VERIFICÁVEL** | Instagram, TikTok e LinkedIn exigem login. |
| **Marcas figurativas e semelhança visual** | **NÃO REALIZADA** | Ainda não há logotipo da nova marca. Cerca de 80 mil figurativas vigentes não podem ser buscadas por nome. |
| **Juntas Comerciais e Receita Federal** | **NÃO REALIZADA** | Fora do escopo técnico disponível. Nomes empresariais iguais não impedem o registro de marca, mas indicam uso. |
| **Uso dos domínios registrados** (site no ar) | **NÃO VERIFICÁVEL** | O acesso aos sites não está liberado; só o RDAP foi consultado. |

## 5. Possíveis erros e falsos positivos

- **Contagens brutas infladas:** os números "ativos_relevantes" do arquivo `inpi_conflitos.json` (por exemplo, Ordina = 344 e Pontta = 728) **incluem falsos positivos** da busca aproximada: "extraORDINÁRIO", "COORDINATI", "PONTA Grossa", "CARNÍVORAS" (para Nivora), "TAVERNA" (para Tavena), "MORENA" (para Orrena). **A classificação de risco não usou essas contagens.** Ela se baseia nos processos revisados manualmente e citados no relatório executivo.
- **Ocorrências fracas na lista de conflitos principais:** a tabela de `analise-individual.md` mostra até 8 ocorrências por nome. Algumas são fracas e **não sustentam a classificação**, por exemplo:
  - Tavena → "Taven Essential" (vestuário, 35);
  - Caliro → "CAIRO" e "KAIRO'S INFORMÁTICA";
  - Orrena → "ORGANIZAÇÃO MORENA" e "MH MORENA HAIR".
- **Situação inferida:** **7 pedidos listados como "em andamento" não têm despacho desde antes de 2022.** Provavelmente estão parados ou já foram decididos fora do período coberto: ATTEMPO 902066315, Ponta de Estoque 906091659, MovMent 906302145, AVERT 901935247, AVERO 830355758, CAIRO 829012885 e ORGANIZAÇÃO MORENA 900198230. Nenhum deles sustenta uma eliminação.
- **Ausência de evidência:** a ausência de ocorrências (por exemplo, "nenhuma 'Tavena' no índice") é **ausência de evidência nas fontes consultadas, não garantia de disponibilidade**. O texto dos relatórios foi ajustado para dizer "no índice da RPI".
- **Classes de cada processo:** o campo de classes vem do último registro publicado do processo. Nas designações do Protocolo de Madri, aparecem várias classes, como esperado.
- **Especificações truncadas:** o índice guarda até 700 caracteres por classe. A análise de afinidade fina precisa do texto completo, que está no pePI ou na RPI de origem.

## 6. Limitações técnicas e jurídicas

**A cobertura desde julho de 2013 é suficiente? Sim para marcas com nome, com exceções conhecidas.**

- **Fundamento:** o registro vale 10 anos, prorrogáveis (arts. 133 e 134 da LPI). Todo registro vigente hoje foi concedido ou prorrogado nos últimos 10 anos, ou seja, depois de 11/2016, que está dentro do período coberto (07/2013–11/2026). A auditoria confirmou no índice:
  - registros vigentes **com nome**: 2.316.722 (1.576.174 mistas + 740.548 nominativas);
  - registros vigentes **com elemento nominativo e sem nome no índice**: apenas **9**.
- **Exceções que o índice não captura por nome:**
  1. **79.589 marcas figurativas e 365 tridimensionais** vigentes, sem elemento nominativo. Só importam para o logotipo, por semelhança visual.
  2. **Pedidos depositados antes de 07/2013 e parados desde então**, sem nenhum despacho posterior. São raros, mas possíveis em casos de sobrestamento longo ou disputa judicial.
  3. **Despachos publicados depois de 17/11/2026** (RPI 2916 em diante).
  4. **Direitos sem registro no INPI:** marca notoriamente conhecida (art. 126), direito de precedência de quem usava de boa-fé (art. 129, §1º), nome empresarial e título de estabelecimento.
- **Situação jurídica:** é sempre **inferida** pelo último despacho publicado. **Não foi confirmada no pePI.**
- **Natureza do levantamento:** técnico, não é parecer jurídico. Afinidade entre classes, notoriedade e a chance de oposição dependem de análise de advogado.

## 7. Pendências que podem alterar os finalistas

| Finalista | Pendência | Pode mudar a classificação? |
|---|---|---|
| **Tavena** | Busca formal no pePI (radical e fonética); WIPO (tavena.io tem marca registrada no exterior?); @ nas redes sociais; Google Play direto; Juntas Comerciais | Baixa probabilidade. Nada encontrado em nenhuma fonte disponível. |
| **Caliro** | As mesmas da Tavena, mais o app "Caliro AI" (FUTURAI): verificar o país e se há marca registrada | Baixa a moderada, se a FUTURAI tiver registro ou designação para o Brasil. |
| **Averto** | (1) averto.com.br pertence à **FUZZON TECNOLOGIA E MÍDIA EIRELI** (CNPJ 11.125.278/0001-01) desde 06/2025: há projeto com esse nome?; (2) indício de app "Averto" (Smart Path) na App Store BR; (3) WIPO (averto.io nos EUA); (4) a associação com "aberto" | **Moderada.** Se a Fuzzon ou a Smart Path usarem "Averto" em software no Brasil, o risco sobe. |
| **Oltara** *(agora moderado)* | Avaliar a confusão com ALTARA (35, 937705527) e ALIENWARE ALTARA (Dell, 9, 939243164); verificar se o titular de oltara.com.br usa o nome | Já foi rebaixado. Pode voltar a "promissor" se o advogado considerar a diferença suficiente. |

## 8. Próximas ações recomendadas

**Prioridade 1 — antes de escolher o nome:**
1. **Busca formal no pePI**, por advogado de propriedade industrial ou por você em um navegador no Brasil, para **Tavena, Caliro e Averto** (e Oltara/Orrena se quiser alternativas). Incluir radical, fonética e semelhança nas classes 9, 35, 42 e 39.
2. **WIPO Global Brand Database**, consultada manualmente no navegador (cerca de 10 minutos), para os 3 a 5 finalistas, com atenção a tavena.io, averto.io, "Caliro AI" e Oltara (Índia).
3. **Disponibilidade dos @** no Instagram, TikTok, LinkedIn e YouTube, e busca direta no **Google Play**, para os finalistas.
4. **Averto:** visitar averto.com.br e pesquisar a Fuzzon Tecnologia e a Smart Path para entender o possível uso.

**Prioridade 2 — logo após a escolha:**
5. Registrar **nome.com.br + nome.app.br** do escolhido. É barato e reversível. Tavena e Caliro têm os dois livres.
6. **Parecer de registrabilidade** e **depósito** nas classes 9, 35 e 42 (avaliar a 39 por causa do transporte executivo) o quanto antes, para garantir prioridade.
7. Consultar **Juntas Comerciais e Receita Federal** (nome empresarial e nome fantasia).

**Prioridade 3 — com o logotipo:**
8. **Busca figurativa** (classificação de Viena) do símbolo da nova marca no INPI e na WIPO.

---

### Arquivos alterados pela auditoria
- `relatorio-executivo.md`: classificação de Oltara, pendências do Averto e texto de limitações.
- `fontes-e-metodologia.md`: justificativa de cobertura e App Store.
- `analise-individual.md`, `matriz-comparativa.csv`, `resultados-estruturados.json`: regenerados.
- `dados/mercado.json`: achados das buscas aprofundadas e das buscas da auditoria registrados.
- `dados/dominios_appstore.json`: consultas refeitas.
- `dados/inpi_semelhantes.json`: descrição da base corrigida.
- **Novos:** `dados/variantes_finalistas.json` e `dados/recuperacao_vigentes_sem_nome.json`.
