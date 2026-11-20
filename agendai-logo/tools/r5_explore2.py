import os, sys
sys.path.insert(0, "tools")
from r5_shapes import *
import r4_explore
from r4_explore import save
O = "rodada-5/01-estudos/explora2"; os.makedirs(O, exist_ok=True); r4_explore.O = O
save("1d-pena", pena(nib=54, angle=-45, cb=(70, 178, 186, 156)))
save("1e-pena", pena(nib=50, angle=-42, feet=(46, 210), cb=(72, 176, 184, 158)))
save("2d-ogiva", ogiva(bulge=-14, w=34, half=100))
save("2e-ogiva", ogiva(bulge=-22, w=34, half=96, apex_round=4))
save("2f-ogiva", ogiva(bulge=-14, w=36, half=104, cb=(146, 172), apex_round=10))
save("3d-disco", disco(notch_top=50, notch_half=50, bridge=(146, 172)))
