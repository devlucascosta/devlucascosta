# AgendAI — rodada 5 (novas direções)

Situação: **aguardando a escolha** entre Ponte, Raiz (rodada 4), Pena, Ogiva e Disco.

## Ideias iniciais
| Ideia | Destino |
|---|---|
| **Pena**: o A traçado por uma pena larga a 45° | ✅ finalista (variante 1d) |
| **Ogiva**: lados em arcos convexos que se encontram em ponta | ✅ finalista (variante 2f) |
| **Disco**: círculo sólido; o A aparece no vazio | ✅ finalista (variante 3d) |
| Laçada: o A cursivo com laço | ❌ laço fechado já foi lido como "4" na rodada 4 |
| Páginas: o A no vão entre duas páginas | ❌ a silhueta lembra uma calça |
| Estêncil: o A com uma interrupção | ❌ soa industrial |
| Semente: silhueta de semente com abertura | ❌ repete o Arco da rodada 2 |

Exploração: `01-estudos/explora` (1a–3c) e `explora2`. Na primeira, a Ogiva saiu côncava (parecia tenda ou pagode) e a Pena tinha ápice duplo; os dois problemas foram corrigidos na segunda.

## Testes refeitos apenas nos SVGs novos
- `03-testes/auditoria-svg.txt`: símbolos com nota 99 ou 100. Os alertas de ângulo vêm das curvas aproximadas em polígonos; na versão final elas serão redesenhadas com arcos verdadeiros.
- `03-testes/folha-de-testes.html`: as cinco direções lado a lado, mais a comparação com concorrentes.

## Arquivos
- Comparativo: `05-apresentacao/comparativo-rodada-5.html` e `.png`.
- Geradores: `tools/r5_shapes.py`, `tools/build_r5.py` e `tools/build_r5_sheet.py`.
