import os, sys
sys.path.insert(0, "tools")
from r4_shapes import *
import r4_explore
from r4_explore import save
O = "rodada-4/01-estudos/explora2"; os.makedirs(O, exist_ok=True); r4_explore.O = O
save("a4-ponte", ponte(p0=(16, 246), p1=(100, 176), p2=(186, 158)))
save("a5-ponte", ponte(p0=(10, 248), p1=(98, 180), p2=(186, 162), aw=28))
save("c4-raiz", raiz())
save("c5-raiz", raiz(flare=46, sag=24))
save("c6-raiz", raiz(flare=26, sag=10, p_open=((70, 232), (114, 194), (196, 172))))
