# AgendAI — rodada 4 (refinamento: Ponte, Recorte, híbrido)

Situação: **aguardando a escolha**. O Impulso foi descartado a pedido. Reaproveitados: briefing, pesquisa, A-base (topo reto de 36, pernas de 34/46), tipografia e pipeline da rodada 3.

| | Iterações (`01-estudos/`) | Escolhida |
|---|---|---|
| A Ponte | a1–a3: a folga virou uma cunha que fecha em tamanho pequeno · a5: saliência excessiva à esquerda | **a4** |
| B Recorte | b2 e b3: arco mais alto ou mais baixo; o travessão perde equilíbrio | **b1** (travessão curvo de espessura constante) |
| C Híbrido | c1–c3 "Laço": lido como "4" em 32 px ❌ · c4 e c5: curva exagerada e degrau no pé | **c6 "Raiz"** |

Testes refeitos apenas nos SVGs novos:
- `03-testes/auditoria-svg.txt`: símbolos com nota 99/100. Os alertas de complexidade nos logotipos verticais vêm das curvas aproximadas em polígonos, que serão redesenhadas com arcos na versão final.
- `03-testes/folha-de-testes.html`: escala, pixel, fundos, desfoque, espelhamento, rotação, contextos e comparação com concorrentes.

Cores sobre fundo branco:
- **Esmeralda:** corpo #00A98F, curva #00D1B2, "AI" #00A98F.
- **Dourado:** símbolo de uma cor em #D4AF5A. Na Ponte, o corpo é #0D0D0D e a curva #D4AF5A, porque o #E7CA82 desaparece sobre o branco.

Apresentação: `05-apresentacao/comparativo-rodada-4.html` e `.png`. Geradores: `tools/r4_shapes.py`, `tools/build_r4.py` e `tools/build_r4_sheet.py`.
