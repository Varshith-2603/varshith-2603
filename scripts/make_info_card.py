#!/usr/bin/env python3
"""Generate a neofetch-style profile info SVG."""
from pathlib import Path
import os
OUT=Path("info-card.svg"); STATIC=os.getenv("STATIC")=="1"
rows=[("ROLE","AI/ML Engineer"),("FOCUS","Applied AI • Computer Vision"),("DOMAIN","Robotics • Mechatronics"),("STACK","Python • PyTorch • TensorFlow"),("TOOLS","OpenCV • FastAPI • Streamlit"),("BUILDING","Intelligent Systems"),("LEARNING","LLMs • RAG • ML Systems"),("MINDSET","Build • Test • Learn • Improve")]
parts=["""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 490">
<style>@keyframes line {from {opacity:0;transform:translateX(-10px)} to {opacity:1;transform:translateX(0)}} .item {animation:line .3s ease-out both}</style>
<rect width="850" height="490" rx="14" fill="#0d1117" stroke="#30363d"/>
<rect x="1" y="1" width="848" height="35" rx="14" fill="#161b22"/>
<circle cx="22" cy="18" r="5" fill="#ff7b72"/><circle cx="40" cy="18" r="5" fill="#d29922"/><circle cx="58" cy="18" r="5" fill="#3fb950"/>
<text x="78" y="23" fill="#8b949e" font-family="monospace" font-size="12">varshith@github ~ $ neofetch</text>
<text x="42" y="76" fill="#7dd3fc" font-family="monospace" font-size="24" font-weight="700">THALLA VARSHITH</text>
<text x="42" y="99" fill="#8b949e" font-family="monospace" font-size="12">B.Tech Mechatronics • India 🇮🇳</text>
"""]
for i,(k,v) in enumerate(rows):
    delay=0 if STATIC else i*.08
    parts.append(f'<g class="item" style="animation-delay:{delay:.2f}s"><text x="42" y="{140+i*38}" fill="#7ee787" font-family="monospace" font-size="13">{k:10}</text><text x="165" y="{140+i*38}" fill="#c9d1d9" font-family="monospace" font-size="13">{v}</text></g>')
parts.append("""<line x1="42" y1="456" x2="808" y2="456" stroke="#30363d"/>
<text x="42" y="478" fill="#8b949e" font-family="monospace" font-size="11">mechatronics → software → data → AI → intelligent systems</text>
</svg>""")
OUT.write_text("".join(parts),encoding="utf-8"); print(f"Wrote {OUT}")
if __name__=="__main__": main()
