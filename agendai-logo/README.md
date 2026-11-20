# AgendAI — logomarca oficial (rodada 1: conceitos)

Processo conduzido com a skill **logo-design**. Situação: **aguardando a escolha de uma direção**. O kit final não foi produzido.

| Pasta | Conteúdo |
|---|---|
| `01-brief/` | Briefing, pesquisa, clichês, mapa de palavras, lista inicial de 11 conceitos com notas, estudo tipográfico |
| `02-conceitos/A-ligadura/` | Conceito A: símbolo, logotipo horizontal e desenho de construção (SVG) |
| `02-conceitos/B-encaixe/` | Conceito B: idem |
| `02-conceitos/C-pivo/` | Conceito C: idem |
| `02-conceitos/exploracoes/` | Todas as iterações, inclusive as descartadas |
| `03-testes/` | Folha de testes (HTML) e auditoria dos SVGs |
| `04-apresentacao/` | Visão geral (PNG), ficha técnica comparativa, apresentação com mockups (HTML + slides PNG) |
| `tools/` | Scripts de construção geométrica (Python) que geram os SVGs |

Fontes: Sora, Montserrat e Manrope (SIL Open Font License 1.1). Todas as letras foram convertidas em curvas, sem `<text>`.

Para regenerar os arquivos: `pip install fonttools shapely`; baixe as fontes com `npm pack @fontsource/{sora,manrope,montserrat}` e extraia em `$FONT_DIR`; depois rode `python3 tools/build_concepts.py` a partir desta pasta.
