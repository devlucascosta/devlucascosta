import sys; sys.path.insert(0, "tools")
from glyphs import text_path
rows = [("Sora",400),("Sora",500),("Sora",600),("Manrope",500),("Manrope",600),("Manrope",700),("Montserrat",500),("Montserrat",600)]
y=0; parts=[]
for fam,w in rows:
    y+=110
    d,wd,_=text_path("AgendAI",fam,w,60,x=40,baseline=y,tracking=-0.01)
    parts.append(f'<path d="{d}" fill="#0A0F14"/>')
    d2,_,_=text_path(f"{fam} {w}","Manrope",500,14,x=560,baseline=y)
    parts.append(f'<path d="{d2}" fill="#888"/>')
    d3,_,_=text_path("AgendAI",fam,w,9,x=760,baseline=y)
    parts.append(f'<path d="{d3}" fill="#0A0F14"/>')
svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 {y+40}" width="900" height="{y+40}"><rect width="100%" height="100%" fill="#fff"/>{"".join(parts)}</svg>'
open("01-brief/estudo-tipografico.svg","w").write(svg)
