import os, sys
sys.path.insert(0, "tools")
from r6_shapes import *
import r4_explore
from r4_explore import save
O = "rodada-6/01-estudos/explora"; os.makedirs(O, exist_ok=True); r4_explore.O = O
save("a1-raiz", raiz_ref())
save("a2-raiz", raiz_ref(flare=24, sag=14, t=30, tw=30))
save("b1-raiz-pena", raiz_ref(wl=26, wr=50, nib_cut=16))
save("b2-raiz-pena", raiz_ref(wl=24, wr=52, nib_cut=20, t=26, flare=28, sag=14))
save("c1-pena-pausa", pena2(lift=8))
save("c2-pena-bico", pena2(beak=22))
save("c3-pena-pausa", pena2(lift=8))
save("c4-pena-pausa", pena2(nib=56, lift=10, cb=(66, 180, 188, 154)))
