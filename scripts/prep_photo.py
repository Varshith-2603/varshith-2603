#!/usr/bin/env python3
"""Prepare a portrait for ASCII conversion. Run locally when the photo changes."""
import sys
from pathlib import Path
import cv2,numpy as np
from PIL import Image
try: from rembg import remove
except ImportError: remove=None
OUT=Path("source-prepped.png")
def main():
    if len(sys.argv)!=2: raise SystemExit("Usage: python scripts/prep_photo.py source-photo.jpg")
    image=Image.open(sys.argv[1]).convert("RGBA")
    if remove: image=remove(image)
    rgba=np.array(image); rgb=rgba[:,:,:3]; alpha=rgba[:,:,3:4]/255.0
    comp=(rgb*alpha+255*(1-alpha)).astype(np.uint8); gray=cv2.cvtColor(comp,cv2.COLOR_RGB2GRAY)
    gray=cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8)).apply(gray); cv2.imwrite(str(OUT),gray)
    print(f"Wrote {OUT}")
if __name__=="__main__": main()
