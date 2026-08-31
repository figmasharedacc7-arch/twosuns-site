# -*- coding: utf-8 -*-
"""Option A: full bleed sections, so the subject has to sit on the photo side.

The section renders roughly 2.7:1 and background-size:cover shows the full
width of the file, so background-position cannot move anything horizontally.
The only real lever is to crop the file itself. Subject positions below are
read off the photos by eye, which beat every detector tried on this set.
"""
import os
from PIL import Image, ImageOps, ImageEnhance

WARM = set()   # names that need pulling out of blue and into the palette

V2 = "/Users/mohammaddidarulalam/Documents/Claude/twosuns-live"
DROP = os.path.join(V2, "preview", "incoming")   # the originals stay out of the served root

OUT_W, OUT_H = 2200, 1200         # 1.83:1, close to the 3:2 source so little is lost
QUALITY = 82

# name, bleed side, subject centre as a fraction of width, mirror first, tone lift
# imgsec-l = photo bleeds from the left, copy on the right, subject must be LEFT
PLAN = [
    # name, side, subject x, mirror, brightness lift, vertical anchor (0 top, 1 bottom)
    ("area-materials",    "l", 0.25, False, None, 0.45),
    ("area-distribution", "r", 0.47, False, None, 0.40),
    ("area-owners",       "l", 0.28, False, 1.04, 0.48),   # golden-lit towers sit left
    ("area-construction", "r", 0.35, True,  None, 0.35),
    ("area-operations",   "l", 0.30, False, 1.04, 0.78),   # frame low onto the documents, not the torsos
    ("area-institutions", "r", 0.55, False, 1.34, 0.12),   # anchor high, the stage not the headrests
    ("fam-horizon",       "r", 0.45, False, 1.30, 0.50),
    ("fam-pulse",         "l", 0.22, False, 1.04, 0.50),   # keep the blurred left, the placeholder text sits right
    ("plat-integration",  "r", 0.52, False, 1.08, 0.45),
    ("home-work",         "l", 0.30, False, None, 0.52),   # cranes left, open sky right
    ("plat-deploy",       "r", 0.62, False, 1.06, 0.48),
    ("plat-hero",         "r", 0.50, False, 1.02, 0.30),   # crop up, the lower third is flat black
    ("cap-hero",          "r", 0.72, False, 1.30, 0.50),   # dark control room, needs a real lift
    ("uc-hero",           "r", 0.45, True,  1.02, 0.62),   # mirror so the pair sits right, frame low for the crane
    ("company-hero",      "r", 0.72, False, 1.02, 0.42),   # group already sits right, only a light touch
]
WARM.add("plat-integration")
WARM.add("plat-hero")
WARM.add("cap-hero")
WARM.add("uc-hero")
MILD = {"area-operations", "fam-pulse", "area-owners", "company-hero"}     # a gentle nudge, not the night-shot regrade

TARGET = {"l": 0.34, "r": 0.66}   # pulled in from the edges so less width is thrown away
MIN_KEEP = 0.90                    # never crop away more than this much width
KEEP_ALL = {"cap-hero", "company-hero"}   # the group is the subject, keep the full width


def build(name, side, subj, mirror, lift, anchor):
    im = ImageOps.exif_transpose(Image.open(os.path.join(DROP, name + ".jpg"))).convert("RGB")
    if mirror:
        im = ImageOps.mirror(im)
        subj = 1.0 - subj

    t = TARGET[side]
    W, H = im.size

    # narrowest crop that still reaches the target, so we throw away as little as possible
    frac, left_f, landed = 1.0, 0.0, subj
    floor = 100 if name in KEEP_ALL else int(MIN_KEEP * 100)
    for f in [x / 100.0 for x in range(100, floor - 1, -1)]:
        L = subj - f * t
        L = max(0.0, min(1.0 - f, L))
        got = (subj - L) / f
        if abs(got - t) < abs(landed - t):
            frac, left_f, landed = f, L, got
        if abs(got - t) < 0.02:
            break

    cw = int(W * frac)
    left = int(W * left_f)
    ch = int(cw / (OUT_W / OUT_H))
    if ch > H:                       # not enough height, give width back
        ch = H
        cw = int(ch * (OUT_W / OUT_H))
        left = int(max(0, min(W - cw, subj * W - t * cw)))
        landed = (subj * W - left) / cw
    top = int(max(0, min(H - ch, (H - ch) * anchor)))

    crop = im.crop((left, top, left + cw, top + ch)).resize((OUT_W, OUT_H), Image.LANCZOS)
    if name in MILD:
        r, g, b = crop.split()
        crop = Image.merge("RGB", (
            r.point(lambda v: min(255, int(v * 1.06 + 4))),
            g,
            b.point(lambda v: int(v * 0.93))))
        crop = ImageEnhance.Color(crop).enhance(0.92)
    if name in WARM:
        r, g, b = crop.split()
        crop = Image.merge("RGB", (
            r.point(lambda v: min(255, int(v * 1.28 + 14))),
            g.point(lambda v: min(255, int(v * 1.02 + 4))),
            b.point(lambda v: int(v * 0.62))))
        crop = ImageEnhance.Color(crop).enhance(0.80)
    if lift:
        crop = ImageEnhance.Brightness(crop).enhance(lift)
        crop = ImageEnhance.Contrast(crop).enhance(1.05)

    out = os.path.join(V2, name + ".jpg")
    crop.save(out, "JPEG", quality=QUALITY, subsampling=0, optimize=True, progressive=True)
    fov = (cw / W) * (ch / H)
    return mirror, landed, fov, os.path.getsize(out) / 1024


if __name__ == "__main__":
    print("%-16s %-5s %-9s %-10s %-11s %s" % ("image", "side", "mirrored", "lands at", "frame kept", "size"))
    tot = 0
    for name, side, subj, mirror, lift, anchor in PLAN:
        mir, landed, fov, kb = build(name, side, subj, mirror, lift, anchor)
        tot += kb
        ok = "ok" if abs(landed - TARGET[side]) < 0.10 else "OFF TARGET"
        print("%-16s %-5s %-9s %-10.2f %-11s %5.0f KB  %s" % (
            name.replace("area-", ""), side, "yes" if mir else "no", landed,
            "%.0f%%" % (fov * 100), kb, ok))
    print("%-16s %36s %5.0f KB" % ("TOTAL", "", tot))
