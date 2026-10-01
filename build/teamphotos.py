# -*- coding: utf-8 -*-
"""Team portraits for the Company page.

Portrait tiles, not round avatars: the Zema style fills the whole card with the
photo and lays the name over it. Crops are head and shoulders down to the chest,
anchored so every face lands at the same height in its tile.

No colour grading. The warm regrade used on the industry photography turns skin
tones orange.

Run:  python3 teamphotos.py
"""

import os

from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, ".."))
W, H = 720, 756          # 0.952, the Zema tile ratio
FACE_Y = 0.30            # where the face centre sits inside the tile
QUALITY = 84

SRC = "~/Downloads/Individual Headshots/"

# slug, source, face centre x and y as a fraction of the source, tile height as a
# fraction of the source height. Read off the photos, checked in the contact sheet.
PLAN = [
    ("team-aiman",    "1. Aiman.jpg",     0.48, 0.25, 0.78),
    ("team-ryan",     "2. Ryan.jpg",      0.49, 0.28, 0.80),
    # replaced 2026-10-01, the original is kept in preview/incoming
    ("team-michelle", "~/Documents/Claude/twosuns-live/preview/incoming/michelle-new.jpg",
                                         0.50, 0.24, 0.70),
    ("team-raihaan",  "5. Raihaan.jpg",   0.49, 0.29, 0.80),
    ("team-nour",     "6. Nour.jpg",      0.49, 0.31, 0.78),
    ("team-alexa",    "7. Alexa.jpg",     0.50, 0.28, 0.80),
    ("team-sara",     "8. Sara.jpg",      0.49, 0.32, 0.78),
]


def build(name, src, fx, fy, scale):
    path = src if src.startswith(("~", "/")) else SRC + src
    im = ImageOps.exif_transpose(Image.open(os.path.expanduser(path))).convert("RGB")
    sw, sh = im.size
    bh = int(sh * scale)
    bw = int(bh * W / float(H))
    if bw > sw:                         # not enough width, take what there is
        bw = sw
        bh = int(bw * H / float(W))
    cx, cy = sw * fx, sh * fy
    left = int(max(0, min(sw - bw, cx - bw / 2.0)))
    top = int(max(0, min(sh - bh, cy - bh * FACE_Y)))
    crop = im.crop((left, top, left + bw, top + bh)).resize((W, H), Image.LANCZOS)
    path = os.path.join(OUT, name + ".jpg")
    crop.save(path, "JPEG", quality=QUALITY, optimize=True, progressive=True)
    return path


if __name__ == "__main__":
    sheet = Image.new("RGB", (W // 3 * len(PLAN), H // 3), "white")
    for i, row in enumerate(PLAN):
        p = build(*row)
        print("  %-16s %6.0f KB" % (os.path.basename(p), os.path.getsize(p) / 1024.0))
        sheet.paste(Image.open(p).resize((W // 3, H // 3), Image.LANCZOS), (i * (W // 3), 0))
    sheet.save("/private/tmp/claude-501/-Users-mohammaddidarulalam-Documents-Claude/"
               "3a36e285-c47a-4b23-bddd-6a00b286a08a/scratchpad/team-sheet.jpg",
               "JPEG", quality=88)
