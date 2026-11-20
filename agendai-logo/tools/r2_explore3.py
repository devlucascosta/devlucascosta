import os, sys, math
sys.path.insert(0, "tools")
from r2_shapes import *
O = "rodada-2/01-estudos/explora3"
B = 226

def legsA(w=30, half=94, apex_y=28, apex_round=6):
    out = sym_outline(apex_y, B, half)
    return letter_from_outline(out, w, B, apex_round=apex_round), out

def p01(c, r, a0, a1, aw=24, w=30, clip_left=True, clip_base=True, cap="flat"):
    g, out = legsA(w=w)
    a = arc_band(c, r, aw, a0, a1, cap=cap)
    if clip_base:
        a = a.intersection(box(-50, -50, 300, B))
    return centre(unary_union([g, a]))

# i: born inside right leg, sweeps down-left through left leg, ends on the baseline outside the left foot
save(f"{O}/p01-i.svg", p01((250, 60), 210, 132, 170), "i")
# j: rises from the left foot zone, crosses right leg, ends just outside (perpendicular cut)
save(f"{O}/p01-j.svg", p01((150, 420), 260, 232, 268), "j")
# k: shallow rising curve, starts flush on left outer edge, exits right leg by ~22 units
save(f"{O}/p01-k.svg", p01((110, 470), 300, 243, 281), "k")
# l: like i but gentler and shorter tail
save(f"{O}/p01-l.svg", p01((300, 20), 250, 128, 160), "l")
# m: rising curve with round terminal only on the exit
save(f"{O}/p01-m.svg", p01((150, 420), 260, 232, 266, cap="round"), "m")

def p02(w=38, half=98, apex_y=24, cb=(146, 172), apex_round=28, open_round=24, counter_round=8):
    return centre(letter_from_outline(sym_outline(apex_y, B, half), w, B, cb=cb, apex_round=apex_round,
                                      open_round=open_round, counter_round=counter_round))
save(f"{O}/p02-g.svg", p02(), "g")
save(f"{O}/p02-h.svg", p02(w=34, half=100, cb=(142, 166), apex_round=30, open_round=30, counter_round=6), "h")
print("ok")
