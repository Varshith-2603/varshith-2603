#!/usr/bin/env python3
"""Render a self-contained animated SVG contribution heatmap."""
import json
from datetime import date,timedelta
from pathlib import Path
DATA=Path("data/contributions.json"); OUT=Path("contrib-heatmap.svg")
PALETTE=["#161b22","#0e4429","#006d32","#26a641","#39d353","#69f0a0"]
def main():
    payload=json.loads(DATA.read_text(encoding="utf-8")); days={date.fromisoformat(x["date"]):x for x in payload["days"]}
    if not days: raise RuntimeError("No contribution data found.")
    end=max(days); start=end-timedelta(days=370); start-=timedelta(days=(start.weekday()+1)%7)
    dates=[start+timedelta(days=i) for i in range(371)]
    cell,gap,left,top=13,4,48,40; width,height=48+53*(cell+gap)+18,190
    rects=[]
    for i,d in enumerate(dates):
        col,row=i//7,i%7; item=days.get(d,{"count":0,"level":0}); level=max(0,min(5,int(item["level"])))
        x,y=left+col*(cell+gap),top+row*(cell+gap); delay=(col+row)*.012
        rects.append(f'<rect class="day" x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{PALETTE[level]}" style="animation-delay:{delay:.3f}s"><title>{d}: {item["count"]} contributions</title></rect>')
    total=payload["stats"]["total"]; current=payload["stats"]["current_streak"]; longest=payload["stats"]["longest_streak"]
    legend="".join(f'<rect x="{width-190+i*18}" y="{height-29}" width="12" height="12" rx="3" fill="{c}"/>' for i,c in enumerate(PALETTE))
    svg=f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">
<style>
@keyframes reveal {{from {{opacity:0; transform:translateY(-7px)}} to {{opacity:1; transform:translateY(0)}}}}
.day {{animation:reveal .32s ease-out both; transform-box:fill-box; transform-origin:center}}
</style>
<rect width="{width}" height="{height}" rx="14" fill="#0d1117" stroke="#30363d"/>
<text x="20" y="23" fill="#8b949e" font-family="monospace" font-size="12">github@varshith ~ $ contributions --last-53-weeks</text>
<text x="{width-20}" y="23" text-anchor="end" fill="#7ee787" font-family="monospace" font-size="12">{total:,} contributions</text>
{''.join(rects)}
<text x="20" y="{height-19}" fill="#8b949e" font-family="monospace" font-size="10">streak:{current}d</text>
<text x="105" y="{height-19}" fill="#8b949e" font-family="monospace" font-size="10">longest:{longest}d</text>
<text x="{width-220}" y="{height-19}" fill="#8b949e" font-family="monospace" font-size="10">Less</text>
{legend}
<text x="{width-70}" y="{height-19}" fill="#8b949e" font-family="monospace" font-size="10">More</text>
</svg>"""
    OUT.write_text(svg,encoding="utf-8"); print(f"Wrote {OUT}")
if __name__=="__main__": main()
