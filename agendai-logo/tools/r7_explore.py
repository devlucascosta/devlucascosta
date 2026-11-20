import os, sys
sys.path.insert(0, "tools")
from r7_shapes import *
import r4_explore
from r4_explore import save
O = "rodada-7/01-estudos/explora"; os.makedirs(O, exist_ok=True); r4_explore.O = O
save("a1-evo", raiz_pena_evo())
save("a2-evo", raiz_pena_evo(foot_cut=22, tw=30, wr=54))
save("b1-encontro", encontro())
save("b2-encontro-curvas", encontro(mode="curvas"))
save("b3-encontro-folga", encontro(gap=10))
