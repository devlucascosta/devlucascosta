import os, sys
sys.path.insert(0, "tools")
from r5_shapes import *
import r4_explore
from r4_explore import save
O = "rodada-5/01-estudos/explora"; os.makedirs(O, exist_ok=True); r4_explore.O = O
save("1a-pena", pena())
save("1b-pena", pena(nib=56, angle=-40, floor=20))
save("1c-pena", pena(nib=50, angle=-48, feet=(40, 214), cb=(84, 160, 176, 172)))
save("2a-ogiva", ogiva())
save("2b-ogiva", ogiva(bulge=32, w=34, half=96))
save("2c-ogiva", ogiva(bulge=16, w=36, half=104, apex_round=6))
save("3a-disco", disco())
save("3b-disco", disco(notch_top=50, notch_half=50, bridge=(146, 172)))
save("3c-disco", disco(r=108, cy=118, notch_top=62, notch_half=60, bridge=(154, 180)))
