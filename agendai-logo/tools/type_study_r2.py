import sys; sys.path.insert(0, "tools")
from glyphs import text_path
rows = [("plus-jakarta-sans",500),("plus-jakarta-sans",600),("dm-sans",500),("figtree",500),("figtree",600),
        ("instrument-sans",500),("instrument-sans",600),("outfit",400),("outfit",500),("urbanist",600),("manrope",600)]
y=0; parts=[]
for fam,w in rows:
    y+=96
    d,wd,_=text_path("AgendAI",fam,w,52,x=40,baseline=y,tracking=-0.01)
    parts.append(f'<path d="{d}" fill="#0A0F14"/>')
    d2,_,_=text_path(f"{fam} {w}","manrope",500,13,x=500,baseline=y)
    parts.append(f'<path d="{d2}" fill="#888"/>')
    d3,_,_=text_path("AgendAI",fam,w,8,x=760,baseline=y)
    parts.append(f'<path d="{d3}" fill="#0A0F14"/>')
svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 {y+40}" width="880" height="{y+40}"><rect width="100%" height="100%" fill="#fff"/>{"".join(parts)}</svg>'
open("rodada-2/01-estudos/estudo-tipografico-r2.svg","w").write(svg)
