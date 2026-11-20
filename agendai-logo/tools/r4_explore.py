import os, sys
sys.path.insert(0, "tools")
from r4_shapes import *
from geo import poly_d, svg
from shapely import affinity
O = "rodada-4/01-estudos/explora"; os.makedirs(O, exist_ok=True)
def save(name, res):
    body, curve, _ = res
    allg = unary_union([g for g in (body, curve) if g is not None])
    minx, miny, maxx, maxy = allg.bounds
    s = 204 / max(maxx - minx, maxy - miny)
    f = lambda g: affinity.translate(affinity.scale(g, s, s, origin=(minx, miny)), (256 - (maxx-minx)*s)/2 - minx, (256-(maxy-miny)*s)/2 - 2 - miny)
    b = "".join(f'<path fill="#0A0F14" fill-rule="evenodd" d="{poly_d(f(g))}"/>' for g in (body, curve) if g is not None)
    open(f"{O}/{name}.svg", "w").write(svg(256, 256, b, name))
save("a1-ponte", ponte())
save("a2-ponte", ponte(p0=(30, 246), p1=(100, 186), p2=(188, 168)))
save("a3-ponte", ponte(p0=(40, 248), p1=(106, 176), p2=(184, 152), aw=30))
save("b1-recorte", recorte(t=30))
save("b2-recorte", recorte(p0=(22, 200), p1=(100, 176), p2=(200, 158), t=28))
save("b3-recorte", recorte(p0=(30, 208), p1=(104, 184), p2=(198, 166), t=32))
save("c1-laco", laco())
save("c2-laco", laco(corner_y=222, end_y=170, R=36))
save("c3-laco", laco(corner_y=208, end_y=182, R=24, w=32))
