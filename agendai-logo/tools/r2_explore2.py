import os, sys, math
sys.path.insert(0, "tools")
from r2_shapes import *
O = "rodada-2/01-estudos/explora2"
B = 226

# P01 — A com movimento: legs + a curved stroke that replaces the crossbar and exits the right leg
def p01(w=30, half=94, apex_y=28, arc=((128, 300), 175, 236, 292), aw=24, apex_round=6, rnd=False):
    g = letter_from_outline(sym_outline(apex_y, B, half), w, B, apex_round=apex_round)
    a = arc_band(arc[0], arc[1], aw, arc[2], arc[3], cap="round" if rnd else "flat")
    # clip the arc start to the left leg's outer edge
    outer = sym_outline(apex_y, B, half)
    a = a.difference(Polygon([(0, 0), (128, apex_y), (128 - half - 300, 600), (-300, 600)]))
    return centre(unary_union([g, a]))
save(f"{O}/p01-e.svg", p01(), "e")
save(f"{O}/p01-f.svg", p01(arc=((60, 330), 200, 268, 312)), "f")
save(f"{O}/p01-g.svg", p01(arc=((40, 360), 230, 283, 318), aw=26), "g")
save(f"{O}/p01-h.svg", p01(arc=((200, 330), 160, 212, 262), rnd=True), "h")

# P02 — A contínuo: soft apex, larger counter, arched lower opening
def p02(w=38, half=98, apex_y=24, cb=(150, 176), apex_round=34, open_round=26, counter_round=8):
    return centre(letter_from_outline(sym_outline(apex_y, B, half), w, B, cb=cb, apex_round=apex_round,
                                      open_round=open_round, counter_round=counter_round))
save(f"{O}/p02-d.svg", p02(), "d")
save(f"{O}/p02-e.svg", p02(w=34, half=104, cb=(146, 172), apex_round=48, open_round=34), "e")
save(f"{O}/p02-f.svg", p02(w=40, half=96, cb=(156, 180), apex_round=22, open_round=40, counter_round=4), "f")

# P03 — vela: straight left side, curved right side, constant weight
def p03(apex=(108, 26), fl=(40, B), fr=(214, B), bulge=34, w=32, cb=(146, 172), apex_round=4):
    out, _ = sail_outline(apex, fl, fr, bulge)
    return centre(letter_from_outline(out, w, B, cb=cb, apex_round=apex_round))
save(f"{O}/p03-d.svg", p03(), "d")
save(f"{O}/p03-e.svg", p03(apex=(116, 26), bulge=44, fr=(218, B), cb=(150, 174)), "e")
save(f"{O}/p03-f.svg", p03(apex=(100, 26), bulge=26, w=34, cb=(144, 170), apex_round=10), "f")
print("ok")
