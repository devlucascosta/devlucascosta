# Auditoria final dos 3 finalistas: Salendo, Joreva, Lindaro

**Data:** 21/11/2026 · **Natureza:** levantamento técnico preliminar. **Não é parecer jurídico.** Nenhum dos três nomes está confirmado como livre por fonte oficial.

## Conclusão

| Posição | Nome | Leitura |
|---|---|---|
| **1º** | **Joreva** | O mais limpo no INPI: nenhuma marca próxima com software nas classes 9 ou 42. Todos os domínios brasileiros estão livres e o .com está à venda. A marca é menos evocativa e exige investimento de memória. |
| **2º** | **Salendo** | A marca mais forte (som, conceito de crescimento, expansão). Há dois pedidos de software a distância moderada (ALENTO e Play Valendo, classes 9 e 42). Os domínios brasileiros estão livres e o .com está à venda. |
| **3º** | **Lindaro** | **Rebaixado.** A rodada 2 tinha um falso negativo. LINDARA (só a vogal final muda) está concedida na classe 35, e **o INPI já indeferiu LINDARE citando LINDARA**. Há ainda LINARA (software, classes 9 e 42) e TÍNDARO (TI, classes 35 e 42). |

**Recomendação:** levar **Joreva** primeiro ao advogado de propriedade industrial, com **Salendo** como alternativa na mesma consulta. O custo extra é pequeno, e os dois têm perfis complementares: um é mais seguro, o outro mais forte como marca.

---

## 1. O que foi feito

- **INPI/RPI:** reaproveitei o índice local da rodada 2 (RPI, XML oficial, edições 2220 a 2915, de 23/07/2013 a 17/11/2026; 5,3 milhões de processos), **sem reindexar nem baixar nada de novo**. Fiz uma varredura nova e mais ampla só para os três nomes (`../../dados/auditoria_finalistas.py`). Cada palavra de cada marca, em todas as classes, foi comparada de três formas:
  - distância de até 2 letras na grafia e na forma fonética;
  - distância de até 1 numa chave fonética "frouxa", que iguala d/t, v/f, b/p, g/c, z/s e ignora a vogal final;
  - presença do nome dentro de outra palavra.

  O resultado foi filtrado para similaridade ≥ 86% e as marcas próximas tiveram especificação e despachos revisados à mão. Evidência: `dados/auditoria_3_finalistas_inpi.json`.
- **pePI** (busca.inpi.gov.br), nova tentativa em 21/11/2026: conexão recusada pelo servidor ("connection reset"). **Não consultado.**
- **WIPO Global Brand Database**, nova tentativa: a página continua exigindo verificação anti-robô (ALTCHA), e a API respondeu HTTP 403. **Não consultada, e o bloqueio não foi contornado.** Para o exterior, usei buscas na web (registros comerciais, Trademarkia, Justia).
- **Domínios:** consulta nova ao RDAP do Registro.br e da Verisign em 21/11/2026, com repetição após limite de requisições.
- **Mercado e redes sociais:** buscas estendidas na web. O App Store foi consultado pela API oficial (BR/EUA) na rodada 2, sem app com nenhum dos três nomes. Instagram e LinkedIn exigem login, então só vale o que aparece indexado em buscadores.

## 2. Falsos negativos e correções na rodada 2

| Nome | Rodada 2 dizia | Auditoria encontrou | Causa |
|---|---|---|---|
| **Lindaro** | "Nenhuma marca ativa ≥ 88% nas classes 9/35/42/39"; promissor | **LINDARA** (35, concedida), **LINARA** (9/42, pedidos de software), **TÍNDARO** (35/42, concedidas) | A similaridade bruta ficou em 86%, abaixo do corte de 88%. Diferença de uma letra em nome de 7 letras escapa desse corte. |
| **Joreva** | "Zero marcas semelhantes" | **Óreva** (35, pedido, comércio de cosméticos) | O pré-filtro da busca exige o nome contido na marca ou o mesmo início fonético. "Óreva" é "Joreva" sem o J. |
| **Salendo** | "Nenhuma semelhante ≥ 88%" | **ALENTO** (9/42, pedidos de software) e **Play Valendo** (9/35/42, pedidos) | Mesmo motivo: diferença na letra inicial. |

**Correção aplicada:** Lindaro passou a "com pendências" em `20-novos-nomes.md`, `resultados.json` e `matriz-comparativa.csv`, que foram regenerados. Os riscos de Joreva e Salendo foram atualizados.

**Lição para próximas rodadas:** para finalistas, a busca precisa usar distância de edição, e não só a porcentagem com corte de 88%.

## 3. INPI: análise por nome

Situação inferida pelo **último despacho publicado** até a RPI 2915 (17/11/2026). **Confirmar no pePI.**

Na coluna "Avaliação":
- **Conflito real** = semelhança forte com afinidade de serviços;
- **Atenção** = semelhança moderada em classe central;
- **Superficial** = palavra diferente ou serviço sem afinidade.

### Joreva
- **Marca idêntica (qualquer situação):** nenhuma.

| Marca | Classe | Situação | Processo | Titular / especificação | Avaliação |
|---|---|---|---|---|---|
| Óreva | 35 | pedido (publicado para oposição, RPI 2897) | 943905966 | Star Place Distribuidora de Perfumes; comércio de cosméticos | **Atenção baixa:** semelhança gráfica alta (Joreva = J + oreva), mas sem afinidade com software. O mesmo titular usa "oreva" na classe 3 (cosméticos). |
| GEOREF TOPOGRAFIA | 42 | concedida | 932244602 | Engenharia | Superficial |
| JOEVI CONFECÇÕES | 35 | pedido | 901269590 | Confecções | Superficial |

- **Classes 9 e 42 (software):** nenhuma marca próxima.
- **Classe 39:** nenhuma.

### Salendo
- **Marca idêntica (qualquer situação):** nenhuma.

| Marca | Classe | Situação | Processo | Titular / especificação | Avaliação |
|---|---|---|---|---|---|
| ALENTO | 42 e 9 | pedidos (07/2026, publicados para oposição) | 944373216 (42), 944373321 (9) | Silvan Santana de Barros; software, PaaS, aplicativos | **Atenção:** a sílaba tônica "-LEN-" é a mesma. Mas "Alento" é palavra do português, com sentido próprio, e a diferença está no início (S) e no fim (do/to). |
| Play Valendo | 42, 9, 35 | pedidos (08/2026) | 944919820, 944920047, 944497012 | Wagner Paulo Barbosa de Andrade; software, apps | **Atenção baixa:** marca composta com a palavra comum "valendo"; o elemento "Play" diferencia. |
| salento | 35 | concedida (04/2026) | 935840907 | Comércio de vestuário | Superficial: sem afinidade |
| SALIENT (Countersurge Salient) | 9/41 | designação de Madri, concedida | 501841898 | Gryph Frontier (Singapura) | Superficial |
| Saleta Arquitetura / SCALENO | 42 | pedido / concedida | 943298288 / 913817503 | Arquitetura | Superficial |

- **Exterior (web):** SOLENDO, pedido nos EUA da Boston Scientific (cateteres médicos). Sem afinidade.

### Lindaro
- **Marca idêntica (qualquer situação):** nenhuma.

| Marca | Classe | Situação | Processo | Titular / especificação | Avaliação |
|---|---|---|---|---|---|
| **LINDARA** | 35 | **concedida em 26/05/2026**, vigência até 2036 | **936511826** | Rennan Baia de Morais; anúncio e comércio de vestuário, joias, ótica | **Conflito real na classe 35:** muda só a vogal final. **O INPI indeferiu LINDARE (proc. 939257165, RPI 2911) com base no art. 124, XIX, citando LINDARA.** No caso de LINDARE os serviços eram os mesmos; para um SaaS a afinidade é menor, mas o precedente mostra o rigor do exame. |
| **LINARA** | 9 e 42 | pedidos (31/08/2026, publicados na RPI 2911) | 945043058 (9), 945043180 (42) | Rodrigo de Freitas; programas de computador, software, hospedagem de plataformas | **Atenção alta:** mesma área do SaaS, com prioridade anterior. Lin-DA-ro × li-NA-ra fica a duas letras. |
| **TÍNDARO** | 35, 42 (+36, 38) | concedidas (2018, vigência até 2028) | 912190442 (35), 912190884 (42) | HS Serviço de Manutenção de Redes em TI; mecanismos de busca, comércio online | **Atenção:** rima e muda só a inicial (T/L), numa empresa de TI. |
| TÍNDARO | 39 | concedida | 933978553 | Tindaro Agência Marítima | Atenção baixa (transporte marítimo) |
| LYNDRA | 42/5 | designação de Madri, concedida | 501665039 | Lyndra Therapeutics (EUA); farmacêutica | Superficial |

## 4. Mercado, domínios e presença digital

| | Joreva | Salendo | Lindaro |
|---|---|---|---|
| **.com.br** | **disponível** (RDAP 404) | **disponível** | **disponível** |
| **.app.br** | **disponível** | **disponível** | **disponível** |
| **.net.br** | **disponível** | **disponível** | **disponível** |
| **.com** | registrado (2016), **à venda** (BuyDomains) | registrado (2009), **à venda** como "premium" (Atom), preço não informado | registrado (2023), **DNS da Locaweb**, provavelmente titular brasileiro; uso não verificado |
| **Empresas** | **Joreva Mobles SL** (Sant Cugat, Espanha, desde 1995, varejo de móveis, usa "Joreva" como marca) e **Joreva Estudi SL** (La Garriga, desde 2013, interiorismo, jorevastudi.com) | salendo.nl (Países Baixos, site encerrado); wine bar na Itália; conto de 1951 e faixa musical de 2026 | lindaro GmbH (Alemanha, atacado de móveis) |
| **Software / apps** | nenhum (App Store BR/EUA, web, Google Play via web) | nenhum | nenhum |
| **Instagram (indexado)** | nenhum perfil encontrado | nenhum perfil encontrado | **@lindaro** (788 seguidores, conteúdo não identificado) e **@lindaro_official** (moda feminina, Dubai) |
| **Registro no exterior (web)** | nada encontrado; as empresas espanholas podem ter marca na OEPM (não verificado) | nada idêntico; SOLENDO nos EUA (médico) | nada encontrado |

Nenhum perfil encontrado em buscador não significa que o @ esteja livre; isso precisa ser checado manualmente. As redes sociais não foram consultadas diretamente.

## 5. Força de marca para um SaaS amplo (motoristas, autônomos, pequenas empresas)

| Critério | Joreva | Salendo | Lindaro |
|---|---|---|---|
| **Pronúncia em português** | Boa, mas a tônica pode oscilar (jo-RÉ-va / JO-re-va) | **Excelente**: soa natural, como "valendo" ou "sabendo" | **Excelente** |
| **Escrita** | Direta; risco leve de "Joreba" | Direta; risco leve de "Salenddo" | Direta; risco de "Lyndaro" e de confusão com "Lindara" |
| **Memorização** | Média (inventado, sem âncora) | **Alta** (rima com palavras comuns, ideia de "subindo") | Alta (eco de "lindo") |
| **Distinção** | **Muito alta** | Alta no Brasil; menor na Itália, onde é palavra comum | **Baixa** diante de LINDARA, LINARA e TÍNDARO |
| **Força comercial** | Neutra, sóbria, acolhedora | **Otimista, de crescimento**, combina com finanças e evolução | Elegante, mas puxa para o estético |
| **Amplitude** (não limita a agenda ou transporte) | **Total**: nome vazio de significado | **Total**: crescimento serve a qualquer atividade | Total |
| **Identidade visual** | J e o redondo "ev" funcionam bem em monograma | S dinâmico; permite um símbolo de ascensão | L elegante; o monograma é comum |
| **Expansão internacional** | Boa; o J vira "dj" em inglês; há homônimo de móveis na Espanha | Boa em PT/ES/EN; na Itália é verbo comum | Boa; homônimos de móveis (Alemanha) e moda (Dubai) |

## 6. Pontos positivos e negativos

**Joreva**
- **A favor:**
  - menor risco jurídico preliminar dos três (nada próximo em software);
  - domínios brasileiros todos livres e .com comprável;
  - neutro o bastante para crescer para qualquer segmento.
- **Contra:**
  - pouca carga de significado, então a memória precisa ser construída com marketing;
  - tônica ambígua;
  - homônimo comercial de móveis na Catalunha;
  - pedido Óreva na classe 35 (cosméticos) para o advogado avaliar.

**Salendo**
- **A favor:**
  - melhor nome como marca (som, conceito de crescimento, internacional);
  - domínios brasileiros livres e .com à venda;
  - nenhum uso em software.
- **Contra:**
  - pedidos de software ALENTO e Play Valendo (classes 9/42) a distância moderada;
  - palavra comum em italiano;
  - .com "premium", provavelmente caro.

**Lindaro**
- **A favor:**
  - pronúncia e elegância;
  - domínios brasileiros livres.
- **Contra:**
  - LINDARA concedida na 35, com indeferimento de LINDARE como precedente;
  - LINARA em software (9/42);
  - TÍNDARO em TI (35/42);
  - .com e @lindaro ocupados.

## 7. Ranking final e justificativa

1. **Joreva:** é o único sem nenhuma marca próxima nas classes de software (9 e 42). Os riscos encontrados são comerciais e estão fora do Brasil (móveis na Espanha), não jurídicos no INPI. Tem a melhor disponibilidade digital (.com.br, .app.br e .net.br livres, .com à venda). A desvantagem é de força de marca, que se resolve com identidade visual e comunicação, enquanto um conflito de marca não se resolve.
2. **Salendo:** é a marca mais forte e continua viável. Mas dois pedidos recentes de software (ALENTO e Play Valendo) dividem a sílaba "-LEN-"/"-ALEN-", o que pode gerar exigência ou oposição. Vale levar junto ao advogado como alternativa.
3. **Lindaro:** a revisão mostrou risco concreto. O próprio INPI já tratou a troca de uma vogal (LINDARE × LINDARA) como imitação, e há pedidos de software parecidos (LINARA). Não recomendo seguir com ele.

**Levar primeiro ao advogado: Joreva.** O que pedir:
1. busca formal no pePI, nominativa e figurativa, nas classes 9, 35, 42 e 39;
2. busca na WIPO e no TMview, incluindo a OEPM espanhola, por causa da Joreva Mobles;
3. opinião sobre o pedido Óreva (943905966);
4. parecer de registrabilidade e depósito rápido nas classes 9, 35 e 42.

Pedir também a opinião sobre **Salendo** frente a ALENTO (944373216/944373321) e Play Valendo (944919820/944920047). Em paralelo, registrar os domínios .com.br e .app.br dos dois, que é barato e reversível, e checar os @ nas redes sociais.

## 8. Limitações

- **pePI e WIPO não foram consultados** (pePI recusou a conexão; WIPO exige captcha e a API respondeu 403). Por isso **nenhum nome é declarado juridicamente livre**, e **não há estimativa de chance de registro**.
- A situação dos processos vem do último despacho publicado até 17/11/2026. Oposições e decisões posteriores não aparecem.
- Marcas só figurativas (sem nome) não podem ser buscadas por texto. Direitos não registrados (marca notória, uso anterior de boa-fé) não aparecem na RPI.
- Redes sociais: só perfis indexados em buscadores. Juntas Comerciais não foram consultadas.
- Nada foi alterado no código, no banco de dados ou na identidade visual do SaaS.

## Fontes

- **INPI, RPI seção Marcas (XML oficial):** `https://revistas.inpi.gov.br/txt/RM{nº}.zip`. Edições citadas: 2897 (Óreva), 2902/2904 (ALENTO), 2909 (Play Valendo), 2890 (concessão de LINDARA), 2911 (indeferimento de LINDARE e publicação de LINARA). Consulta dos processos: https://busca.inpi.gov.br/pePI/
- **Domínios:** https://rdap.registro.br/domain/joreva.com.br (e demais), https://rdap.verisign.com/com/v1/domain/joreva.com
- **Joreva:**
  - [Joreva Mobles SL (Empresite)](https://empresite.eleconomista.es/JOREVA-MOBLES.html)
  - [Joreva Estudi SL (Iberinform)](https://www.iberinform.es/empresa/5907018/joreva-estudi)
  - [jorevastudi.com](https://jorevastudi.com/)
  - [Joreva Estudi (Archiproducts)](https://www.archiproducts.com/es/revendedores/joreva-estudi_744643)
- **Salendo:**
  - [salendo.com à venda (Atom)](https://www.atom.com/name/Salendo)
  - [salendo.nl (Trustpilot)](https://www.trustpilot.com/review/salendo.nl)
  - [Salendo wine bar](https://www.facebook.com/sangalganosalendowine/)
  - [SOLENDO (Justia)](https://trademarks.justia.com/878/59/solendo-87859862.html)
- **Lindaro:**
  - [lindaro GmbH (D&B)](https://www.dnb.com/business-directory/company-profiles.lindaro_gmbh.a0de9ca372fb21d6687204a2c69b2e2c.html)
  - [@lindaro](https://www.instagram.com/lindaro/)
  - [@lindaro_official](https://www.instagram.com/lindaro_official/)
