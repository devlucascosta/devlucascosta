import os, sys, math
sys.path.insert(0, "tools")
from r2_shapes import *
from r2_explore3 import legsA
O = "rodada-2/01-estudos/explora4"
B = 226
def p01(c, r, a0, a1, aw=24, w=30, cap="flat", clip_x0=None):
    g, out = legsA(w=w)
    a = arc_band(c, r, aw, a0, a1, cap=cap)
    if clip_x0 is not None:
        a = a.intersection(box(clip_x0, -50, 300, 300))
    return centre(unary_union([g, a]).intersection(box(-50, -50, 300, B)))
# n: born inside the left leg, rises gently to the right, exits the right leg (convex curve)
save(f"{O}/p01-n.svg", p01((300, 480), 340, 236, 262, clip_x0=60), "n")
save(f"{O}/p01-o.svg", p01((300, 520), 380, 238, 263, aw=22, clip_x0=60), "o")
save(f"{O}/p01-p.svg", p01((320, 470), 330, 234, 260, aw=26, clip_x0=60, cap="round"), "p")
# q: exits further, sweeping (horizon)
save(f"{O}/p01-q.svg", p01((300, 480), 340, 236, 266, clip_x0=60), "q")
