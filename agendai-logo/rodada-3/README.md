# AgendAI — rodada 3 (a partir das referências enviadas)

Situação: **aguardando a escolha**. Nenhum kit definitivo foi produzido.

## Leitura das referências (`01-estudos/referencias-enviadas.png`)
**Aproveitado como direção:**
- A com topo reto e pernas robustas.
- Pernas com espessuras diferentes (contraste caligráfico).
- Curva que entra na letra e cria profundidade.
- "AI" destacado na cor.

**Deixado de fora (conflita com o briefing):**
- Degradês e brilho: viraram dois tons chapados.
- Lâmina afiada, com risco de lembrar o "swoosh": a curva ficou com largura constante ou afinando pouco.
- Palavra em itálico pesado: o texto ficou em pé.

## Exploração (todas as iterações em `01-estudos/explora*`)
- Ponte a1–a3: sobrava uma lasca do pé esquerdo sob o arco. Em a4–a6 a perna passou a pousar no arco. ✅ a5 → **01 Ponte**
- Fita b1–b3: a ponta reaparecia como um traço solto. ❌ Em b4–b6 a faixa passou a cruzar na frente da perna direita. ✅ b5 → **02 Impulso**
- Recorte c1–c6: degrau na junção, espinho e lascas. Corrigido em c7–c9. ✅ c8 → **03 Recorte**
- Dobra d1–d2: perna e arco em um traço só; o ápice quebrou e o calcanhar virou uma bolha. ❌

## Construção compartilhada
- A de topo reto (36 un.).
- Perna esquerda de 34 un. e perna direita de 46 un.
- Curvas sempre de um único arco de circunferência.
- Tipografia: Plus Jakarta Sans SemiBold (SIL OFL), em pé, com o I serifado. Ver `tools/build_r3.py`.

## Testes
- `03-testes/auditoria-svg.txt`: símbolos com nota 99, 99 e 100.
- `03-testes/folha-de-testes.html`: escala, pixel, fundos, desfoque, espelhamento, rotação, contextos e comparação com concorrentes.

## Cores
- **Fundo escuro:** corpo #00A98F e curva #00D1B2, ou dourado #D4AF5A e #E7CA82.
- **Fundo claro:** corpo em grafite/preto e curva em #00A98F.
- **Dourado em fundo claro:** a curva usa #B8913A, um dourado escurecido que **não faz parte da paleta original**. É sugerido só porque #D4AF5A some sobre o creme (contraste de 1,86:1). Precisa da sua aprovação.

## Arquivos
- `02-simbolos/`: mestres em preto e branco (símbolo, construção, horizontal, vertical, ícone).
- `04-cores/esmeralda|dourado/`: versões coloridas.
- `05-apresentacao/`: visão geral, comparativo em HTML e PNG, e apresentações com mockups nas duas identidades.
