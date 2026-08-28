# -*- coding: utf-8 -*-
"""Prepare Envato drops for the v2 site.

Downsizes to a sensible web ceiling, never upscales, keeps 4:4:4 chroma so the
warm gradients over the top do not band. Reports every decision.
"""
import os, sys, glob
from PIL import Image, ImageOps

V2 = "/Users/mohammaddidarulalam/Documents/Claude/twosuns-live/preview"
DROP = os.path.join(V2, "incoming")

# background photos are shown wide and cropped, so 2400 is the useful ceiling
MAX_W = 2400
QUALITY = 84   # these sit under a heavy cream scrim, 4:4:4 kept for clean detail

EXPECTED = {
    "area-materials", "area-distribution", "area-owners",
    "area-construction", "area-operations", "area-institutions",
    "fam-horizon", "fam-pulse",
    "home-work", "plat-integration", "plat-deploy", "company-team",
}


def process(path):
    stem, ext = os.path.splitext(os.path.basename(path))
    if ext.lower() in (".mp4", ".mov", ".webm"):
        return stem, "video, left for ffmpeg", None

    im = Image.open(path)
    im = ImageOps.exif_transpose(im).convert("RGB")
    w0, h0 = im.size

    if w0 > MAX_W:
        im = im.resize((MAX_W, round(h0 * MAX_W / w0)), Image.LANCZOS)
        note = "downsized"
    else:
        note = "kept native"

    out = os.path.join(V2, stem + ".jpg")
    im.save(out, "JPEG", quality=QUALITY, subsampling=0, optimize=True, progressive=True)

    # a 16:9 card rendition: displayed small, so it can be far lighter and stay crisp
    cw, ch = 1000, 563
    card = ImageOps.fit(im, (cw, ch), Image.LANCZOS, centering=(0.5, 0.45))
    cout = os.path.join(V2, stem + "-card.jpg")
    card.save(cout, "JPEG", quality=86, subsampling=0, optimize=True, progressive=True)

    return stem, "%dx%d -> bg %dx%d %.0fKB + card %dx%d %.0fKB (%s)" % (
        w0, h0, im.width, im.height, os.path.getsize(out) / 1024,
        cw, ch, os.path.getsize(cout) / 1024, note), im.size


if __name__ == "__main__":
    files = [f for f in sorted(glob.glob(os.path.join(DROP, "*")))
             if not f.lower().endswith((".md", ".txt")) and os.path.isfile(f)]
    if not files:
        print("Nothing in %s yet." % DROP)
        sys.exit(0)

    seen = set()
    for f in files:
        stem, msg, size = process(f)
        seen.add(stem)
        flag = "" if stem in EXPECTED else "   <- unexpected name, check the manifest"
        print("  %-22s %s%s" % (stem, msg, flag))
        if size and size[0] < 1800:
            print("      warning: only %dpx wide, this will look soft as a full-bleed background" % size[0])

    missing = sorted(EXPECTED - seen)
    if missing:
        print("\n  still missing: " + ", ".join(missing))
