import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from shapely.geometry import Polygon, box, Point, LineString
from shapely.ops import unary_union
from geo import poly_d, svg, fmt
from build_v1 import save

def ponteiros(apex=(128, 52), ang=22, L=(184, 184), w=36, pivot=30, cross=None, gap=0, hollow=0):
    parts = []
    for side, ln in zip((-1, 1), L):
        a = math.radians(ang)
        end = (apex[0] + side * ln * math.sin(a), apex[1] + ln * math.cos(a))
        parts.append(LineString([apex, end]).buffer(w / 2, cap_style=1, quad_segs=32))
    g = unary_union(parts)
    if cross:
        y, ww = cross
        a = math.radians(ang)
        half = (y - apex[1]) * math.tan(a)
        g = g.union(LineString([(apex[0] - half, y), (apex[0] + half, y)]).buffer(ww / 2, cap_style=1, quad_segs=32))
    piv = Point(apex).buffer(pivot, quad_segs=48)
    if gap:
        g = g.difference(Point(apex).buffer(pivot + gap, quad_segs=48))
    g = g.union(piv)
    if hollow:
        g = g.difference(Point(apex).buffer(hollow, quad_segs=48))
    return g

save("c4-ponteiros", poly_d(ponteiros(cross=(168, 30))))
save("c5-ponteiros-pivo-solto", poly_d(ponteiros(cross=(168, 30), gap=10, pivot=26)))
save("c6-ponteiros-assimetrico", poly_d(ponteiros(apex=(128, 56), L=(186, 132), cross=None, gap=10, pivot=26)))
save("b6-encaixe-limpo", __import__('build_v2').poly_d(__import__('build_v2').encaixe(ch=22, apex=(128, 52), feet=(62, 0), cross=154)))
