"""Convert text set in an OFL font into outlined SVG path data (no <text> in the logos).

Fonts come from the @fontsource npm packages (SIL Open Font License 1.1), cached in FONT_DIR.
"""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

FONT_DIR = os.environ.get("FONT_DIR", "/tmp/claude-0/fonts")
_cache = {}


def font_path(family, weight):
    fam = family.lower()
    return f"{FONT_DIR}/fontsource-{fam}-5.3.0/package/files/{fam}-latin-{weight}-normal.woff"


def load(family, weight):
    key = (family, weight)
    if key not in _cache:
        _cache[key] = TTFont(font_path(family, weight))
    return _cache[key]


def metrics(family, weight):
    f = load(family, weight)
    os2 = f["OS/2"]
    return {"upm": f["head"].unitsPerEm, "cap": os2.sCapHeight, "x": os2.sxHeight}


def _kern_value(f, left, right):
    """Pair kerning from GPOS PairPos (format 1 and 2), best effort."""
    if "GPOS" not in f:
        return 0
    gpos = f["GPOS"].table
    for lookup in gpos.LookupList.Lookup:
        for st in lookup.SubTable:
            if lookup.LookupType == 9:
                st = st.ExtSubTable
            if getattr(st, "LookupType", lookup.LookupType) not in (2,) and lookup.LookupType not in (2, 9):
                continue
            if not hasattr(st, "Format") or not hasattr(st, "Coverage"):
                continue
            if left not in st.Coverage.glyphs:
                continue
            if st.Format == 1:
                idx = st.Coverage.glyphs.index(left)
                for pvr in st.PairSet[idx].PairValueRecord:
                    if pvr.SecondGlyph == right and pvr.Value1 is not None:
                        return getattr(pvr.Value1, "XAdvance", 0) or 0
            elif st.Format == 2:
                c1 = st.ClassDef1.classDefs.get(left, 0)
                c2 = st.ClassDef2.classDefs.get(right, 0)
                rec = st.Class1Record[c1].Class2Record[c2]
                if rec.Value1 is not None:
                    v = getattr(rec.Value1, "XAdvance", 0) or 0
                    if v:
                        return v
    return 0


def text_path(text, family, weight, cap_px, x=0, baseline=0, tracking=0.0, kern=None, use_gpos=True):
    """Return (d, width, per-glyph boxes). cap_px = desired cap height in px.
    tracking in em units of the font size (e.g. -0.02); kern = {index: extra_px} added before glyph i."""
    f = load(family, weight)
    m = metrics(family, weight)
    s = cap_px / m["cap"]
    cmap = f.getBestCmap()
    gs = f.getGlyphSet()
    pen = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
    cx = x
    prev = None
    boxes = []
    em_px = m["upm"] * s
    for i, ch in enumerate(text):
        g = cmap[ord(ch)]
        if prev is not None and use_gpos:
            cx += _kern_value(f, prev, g) * s
        if kern and i in kern:
            cx += kern[i]
        tp = TransformPen(pen, (s, 0, 0, -s, cx, baseline))
        gs[g].draw(tp)
        bp = BoundsPen(gs)
        gs[g].draw(bp)
        if bp.bounds:
            b = bp.bounds
            boxes.append((ch, cx + b[0] * s, baseline - b[3] * s, cx + b[2] * s, baseline - b[1] * s))
        cx += gs[g].width * s + tracking * em_px
        prev = g
    return pen.getCommands(), cx - x - tracking * em_px, boxes


def glyph_path(ch, family, weight, cap_px, x=0, baseline=0):
    d, w, b = text_path(ch, family, weight, cap_px, x, baseline, use_gpos=False)
    return d, w, b
