# AgendAI — rodada 2 (refinamento)

Situação: **aguardando a escolha**. Nenhum kit definitivo foi produzido.

## O que mudou no briefing
A marca deve ser natural, elegante, discreta, atemporal, autoral e humana. Deve evitar aparência esportiva, agressiva ou futurista, e a curva precisa fazer parte da construção da letra. Por isso o conceito A da rodada 1 (Ligadura), cuja inclinação soava esportiva, **não** foi carregado automaticamente para esta rodada. O que se aproveitou dele foi o aprendizado: o problema "AI"/"Al", o método de testes e o pipeline de SVG.

Observação: as referências "Conceito 01" e "Conceito 03 revisado" não correspondem aos conceitos A/B/C da rodada 1. Foram interpretadas pelas descrições do briefing.

## Exploração (todas as iterações em `01-estudos/`)
| Arquivo | Ideia | Destino |
|---|---|---|
| explora/p01-a, p01-d | arco convexo / tigela atravessando o A | ❌ parece telhado oriental / tigela |
| explora/p01-b, p01-c | curva lateral | ❌ desequilibrado / quebrado |
| explora2/p01-e…h, explora3/p01-i…m, explora4 | trajetórias da curva | ❌ cortes estranhos, curva solta na contraforma, "X" |
| **explora5/p01-t** | curva que nasce no pé esquerdo e sai subindo pela direita | ✅ **P01 Traço** |
| explora/p02-a | A contínuo arredondado | ❌ parece um fantasminha |
| **explora3/p02-g** (ajustado) | A sólido com abertura em arco | ✅ **P02 Arco** |
| explora/p03-a…c, explora2/p03-d…f | "vela": lado reto + lado em arco | ✅ **P03 Vela** (entre p03-d e p03-e) |

## Tipografia (`01-estudos/estudo-tipografico-r2.png`)
Foram testadas Plus Jakarta Sans, DM Sans, Figtree, Instrument Sans, Outfit, Urbanist e Manrope. Todas confundem "AI" com "Al". Solução única: um **I com serifas curtas**, desenhado à mão e com o mesmo peso da fonte.
- P01: Instrument Sans 500
- P02: Plus Jakarta Sans 500
- P03: DM Sans 500

Todas têm licença SIL OFL 1.1 e foram convertidas em curvas.

## Testes
- `svg_audit.py`: símbolos com nota 99, 100 e 99. Ver `03-testes/auditoria-svg.txt`.
- `preview_sheet.py`: escala, pixel, fundos, monocromia, desfoque, espelhamento, rotação, contextos e comparação com concorrentes. Ver `03-testes/folha-de-testes.html`.
- **Contraste:** esmeralda #00A98F sobre branco = 2,97:1; #00D1B2 sobre branco = 1,95:1; dourado sobre creme = 1,86:1. Sobre fundo escuro, ambos passam de 9:1.
- Observação técnica: as curvas estão em polígonos finos (de 66 a 107 pontos). Na versão definitiva, a proposta escolhida será redesenhada com arcos verdadeiros.

## Arquivos
- `02-simbolos/P0x-*/`: símbolo, construção, logotipo horizontal, logotipo vertical e ícone (preto e branco).
- `04-cores/esmeralda/` e `04-cores/dourado/`: mesma construção nas duas identidades (claro, escuro, ícone, ícone alternativo).
- `05-apresentacao/`: `visao-geral-rodada-2.png`, `comparativo-rodada-2.html` e `.png`, e as apresentações com mockups (`apresentacao-esmeralda.html`, `apresentacao-dourado.html` e os slides em PNG).
- Scripts que geram tudo: `tools/build_r2.py` e `tools/build_r2_sheet.py`.
