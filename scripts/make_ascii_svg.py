#!/usr/bin/env python3
"""Convert source-prepped.png into an animated monochrome ASCII SVG."""
from pathlib import Path
import cv2
SOURCE=Path("source-prepped.png"); OUT=Path("avi-ascii.svg"); RAMP=" .`:-=+*cs#%@"
def main():
    image=cv2.imread(str(SOURCE),cv2.IMREAD_GRAYSCALE)
    if image is None: raise SystemExit("source-prepped.png not found. Run prep_photo.py first.")
    image=cv2.resize(image,(82,48),interpolation=cv2.INTER_AREA); groups=[]
    for y in range(48):
        row=""
        for x in range(82):
            idx=max(0,min(len(RAMP)-1,int((255-int(image[y,x]))/256*len(RAMP)))); row+=RAMP[idx]
        safe=row.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
        groups.append(f'<text class="row" x="18" y="{28+y*9}" style="animation-delay:{y*.055:.3f}s">{safe}</text>')
    svg=f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 490">
<style>@keyframes print {{from {{opacity:0;transform:translateX(-12px)}} to {{opacity:1;transform:translateX(0)}}}} .row {{animation:print .28s ease-out both}}</style>
<rect width="760" height="490" rx="14" fill="#0d1117" stroke="#30363d"/>
<text x="22" y="19" fill="#8b949e" font-family="monospace" font-size="10">varshith@github ~ $ cat portrait.txt</text>
<g fill="#c9d1d9" font-family="monospace" font-size="8" xml:space="preserve">{''.join(groups)}</g>
<text x="22" y="477" fill="#7dd3fc" font-family="monospace" font-size="12">THALLA VARSHITH</text>
</svg>"""
    OUT.write_text(svg,encoding="utf-8"); print(f"Wrote {OUT}")
if __name__=="__main__": main()
