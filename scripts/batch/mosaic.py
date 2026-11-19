"""Mosaic of chosen contact-sheet tiles: python3 scripts/batch/mosaic.py out.jpg Genus:1,2,5 Genus2:3 ..."""
import sys
from PIL import Image, ImageDraw
import os
SH = os.environ.get("SHEETS", "/tmp/sheets/repo")
cw, ch, cols = 330, 300, 4
tiles = []
for arg in sys.argv[2:]:
    g, ks = arg.split(":")
    sheet = Image.open(f"{SH}/{g}.jpg")
    for k in [int(x) for x in ks.split(",") if x]:
        i = k - 1
        x, y = (i % cols) * cw, (i // cols) * ch
        t = sheet.crop((x, y, x + cw, y + ch - 36)).resize((198, 158))
        tiles.append((f"{g[:12]} {k}", t))
n = 6
W = Image.new("RGB", (n * 200, ((len(tiles) + n - 1) // n) * 175), "white")
d = ImageDraw.Draw(W)
for j, (lab, t) in enumerate(tiles):
    x, y = (j % n) * 200, (j // n) * 175
    W.paste(t, (x + 1, y))
    d.text((x + 3, y + 160), lab, fill="black")
W.save(sys.argv[1], quality=75)
