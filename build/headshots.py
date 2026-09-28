"""Team headshots.

Square avatars for the Company page, cropped to a consistent head and shoulders
framing so the cards line up. Faces get no colour grading: the warm regrade used
on the industry photography turns skin tones orange.

Run:  python3 headshots.py
"""

import os

from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, ".."))
SIZE = 400
QUALITY = 86

# name, source, face centre as a fraction of width and height, crop side as a
# fraction of the shorter edge. Read off the photos by eye, checked in the render.
PLAN = [
    ("face-aiman", "~/Downloads/1. Aiman.jpg", 0.48, 0.25, 1.05),
    ("face-ryan", "~/Downloads/Images/Personal Photos/RyanHeadShot(HQ).jpg", 0.49, 0.28, 1.15),
]


def build(name, src, fx, fy, scale):
    im = ImageOps.exif_transpose(Image.open(os.path.expanduser(src))).convert("RGB")
    W, H = im.size
    side = int(min(W, H) * scale)
    cx, cy = int(W * fx), int(H * fy)
    left = max(0, min(W - side, cx - side // 2))
    top = max(0, min(H - side, cy - side // 2))
    if side > min(W, H):                    # not enough room, take what there is
        side = min(W, H)
        left = max(0, min(W - side, cx - side // 2))
        top = max(0, min(H - side, cy - side // 2))
    crop = im.crop((left, top, left + side, top + side)).resize((SIZE, SIZE), Image.LANCZOS)
    path = os.path.join(OUT, name + ".jpg")
    crop.save(path, "JPEG", quality=QUALITY, optimize=True, progressive=True)
    print("  %-14s %dx%d from %dx%d   %.0f KB" % (name + ".jpg", SIZE, SIZE, W, H,
                                                  os.path.getsize(path) / 1024.0))


if __name__ == "__main__":
    for row in PLAN:
        build(*row)
