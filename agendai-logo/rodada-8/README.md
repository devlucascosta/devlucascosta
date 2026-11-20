# AgendAI — rodada 8 (comparação final das duas finalistas)

Situação: **aguardando aprovação expressa**. Nenhum arquivo oficial nem kit foi gerado.

## Revisão técnica
- Novo `tools/svgarc.py`: converte os contornos em retas e **arcos SVG verdadeiros** (cada trecho é ajustado a uma reta ou a um arco único, com tolerância de 0,12 un.). As letras vêm da fonte em curvas Bézier.
  - Raiz + Pena: 179 segmentos viraram 11 comandos (8 retas e 3 arcos). Sobreposição com o desenho original conferida, sem desvio.
- Wordmark corrigido:
  - O A personalizado agora tem o peso da fonte (perna 33 contra haste de 31, traço fino 24, travessão 26) e a largura do A da fonte.
  - Espaçamento óptico: A→g 0,035 · d→A 0,055 · A→I 0,05 da altura das maiúsculas.
  - Centralização vertical considerando a descendente do "g".
  - Pontos: 451 → 159.
- Auditoria (`03-testes/auditoria-svg.txt`): wordmark 99, letra e símbolo 100, lockups 98–99. Nenhum alerta.

## Arquivos
- `02-finalistas/A-wordmark/{mono,esmeralda,dourado}/` e `02-finalistas/B-raiz-pena/{mono,esmeralda,dourado}/`
- Apresentação: `05-apresentacao/comparativo-final.html` e `.png`
- Geradores: `tools/build_r8.py` e `tools/build_r8_sheet.py`
