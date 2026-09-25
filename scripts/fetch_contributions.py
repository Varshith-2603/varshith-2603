#!/usr/bin/env python3
"""Fetch the public GitHub contribution calendar without an API token."""
import json, re
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
import requests
from bs4 import BeautifulSoup
USERNAME = "Varshith-2603"
URL = f"https://github.com/users/{USERNAME}/contributions"
OUT = Path("data/contributions.json")
def parse_count(text):
    m=re.search(r"(\d[\d,]*)\s+contribution",text or "",re.I)
    return int(m.group(1).replace(",","")) if m else 0
def main():
    r=requests.get(URL,headers={"User-Agent":"Mozilla/5.0 Varshith-Profile-Art"},timeout=30); r.raise_for_status()
    soup=BeautifulSoup(r.text,"html.parser"); cells=soup.select("td[data-date]")
    if not cells: raise RuntimeError("GitHub contribution cells were not found.")
    days=[]
    for cell in cells:
        iso=cell.get("data-date")
        if not iso: continue
        label=cell.get("aria-label") or cell.get("data-tooltip-text") or ""
        title=cell.find("title")
        if not label and title: label=title.get_text(" ",strip=True)
        try: level=int(cell.get("data-level","0"))
        except ValueError: level=0
        days.append({"date":iso,"count":parse_count(label),"level":level})
    days.sort(key=lambda x:x["date"]); streak=longest=0; prev=None
    for item in days:
        d=date.fromisoformat(item["date"])
        if item["count"]: streak=streak+1 if prev and d==prev+timedelta(days=1) else 1; longest=max(longest,streak)
        else: streak=0
        prev=d
    current=0
    for item in reversed(days):
        if item["count"]: current+=1
        else: break
    monthly=Counter()
    for x in days: monthly[x["date"][:7]]+=x["count"]
    best=max(days,key=lambda x:x["count"]) if days else None
    payload={"username":USERNAME,"fetched_at":datetime.now(timezone.utc).isoformat(),"days":days,"stats":{"total":sum(x["count"] for x in days),"current_streak":current,"longest_streak":longest,"best_day":best,"monthly_totals":dict(sorted(monthly.items()))}}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")
    print(f"Wrote {len(days)} days to {OUT}")
if __name__=="__main__": main()
