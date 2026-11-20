"""Round 7 — Raiz + Pena evolved, independent symbol "Encontro", custom wordmark helpers."""
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from shapely.geometry import Polygon, box, Point
from shapely.ops import unary_union
from r6_shapes import raiz_ref
from r4_shapes import drop_small
from r3_shapes import B

H_KW = dict(wl=24, wr=52, nib_cut=20, t=26, flare=28, sag=14)      # rodada 6 · B


def raiz_pena_evo(foot_cut=18, half=None, **over):
    """A: Raiz + Pena where both ends of the main stroke are cut by the same 45° nib (apex and right foot)."""
    kw = dict(H_KW); kw.update(over)
    g, _, info = raiz_ref(**kw)
    if foot_cut:
        minx, miny, maxx, maxy = g.bounds
        # 45° chamfer on the outer-bottom corner of the right leg, parallel to the apex cut
        g = g.difference(Polygon([(maxx - foot_cut - 2, B + 1), (maxx + 40, B + 1), (maxx + 40, B - foot_cut - 42)]))
    return drop_small(g, 600), None, info


def encontro(r=100, gap=0, mode="curva-reta"):
    """B: two quadrants meet at one point. 'curva-reta': a quarter-disc (top-left) meets a square (bottom-right);
    'curvas': two quarter-discs facing out."""
    c = (128, 128)
    q = Point(c).buffer(r, quad_segs=32).intersection(box(c[0] - r, c[1] - r, c[0], c[1]))
    if mode == "curvas":
        other = Point(c).buffer(r, quad_segs=32).intersection(box(c[0], c[1], c[0] + r, c[1] + r))
    else:
        other = box(c[0], c[1], c[0] + r * 0.82, c[1] + r * 0.82)
    from shapely import affinity
    q = affinity.translate(q, -gap / 2, -gap / 2); other = affinity.translate(other, gap / 2, gap / 2)
    return unary_union([q, other]), None, dict()


def word_A(cap):
    """The wordmark's own A: Raiz logic at text weight (lighter strokes), returned in symbol units."""
    g, _, _ = raiz_ref(wl=30, wr=40, nib_cut=0, t=30, flare=24, sag=12, tw=30)
    return g
