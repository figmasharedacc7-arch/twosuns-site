"""The social card.

One 1200x630 image for every page, built from the hero still with the same cream
scrim the hero uses, so a shared link looks like the site rather than a bare URL.

Run:  python3 ogimage.py
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
SRC = os.path.join(ROOT, "preview", "hero-build-poster.jpg")
OUT = os.path.join(ROOT, "og-twosuns.jpg")

W, H = 1200, 630
CREAM = (255, 246, 226)
NAVY = (30, 26, 20)
SUN = (224, 100, 30)
GOLD = (204, 153, 0)
BRONZE = (140, 101, 0)
BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def font(px):
    return ImageFont.truetype(BOLD, px)


def build():
    src = SRC if os.path.exists(SRC) else os.path.join(ROOT, "hero-build-poster.jpg")
    im = Image.open(src).convert("RGB")
    # cover crop to 1200x630
    s = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * s + 1), int(im.height * s + 1)), Image.LANCZOS)
    im = im.crop((0, 0, W, H))

    # the hero's own scrim: opaque cream at the left, clearing to the right
    scrim = Image.new("L", (W, 1))
    for x in range(W):
        f = x / float(W - 1)
        if f < .30:
            a = 250
        elif f < .62:
            a = int(250 - (f - .30) / .32 * 140)
        else:
            a = int(110 - (f - .62) / .38 * 92)
        scrim.putpixel((x, 0), max(a, 16))
    im = Image.composite(Image.new("RGB", (W, H), CREAM), im, scrim.resize((W, H)))

    d = ImageDraw.Draw(im)

    # the wordmark, with the dot of the logo standing in for the o
    x, y = 72, 74
    d.text((x, y), "tw", font=font(58), fill=NAVY)
    wtw = d.textlength("tw", font=font(58))
    d.ellipse([x + wtw + 6, y + 16, x + wtw + 46, y + 56], fill=SUN)
    d.ellipse([x + wtw + 18, y + 2, x + wtw + 42, y + 26], fill=GOLD)
    d.text((x + wtw + 52, y), "suns", font=font(58), fill=NAVY)

    d.text((72, 214), "ADAPTIVE ENTERPRISE CAPABILITY", font=font(21), fill=BRONZE)

    line1, line2 = "Grow, operate and coordinate", "complex work through shared"
    line3 = "enterprise context."
    d.text((72, 262), line1, font=font(52), fill=NAVY)
    d.text((72, 322), line2, font=font(52), fill=NAVY)
    d.text((72, 382), line3, font=font(52), fill=NAVY)

    d.text((72, 476), "An adaptive enterprise platform for the built industry.",
           font=font(24), fill=(90, 85, 76))

    d.rectangle([72, 542, 172, 548], fill=SUN)
    d.text((72, 566), "TWOSUNS BY AEPG", font=font(19), fill=BRONZE)

    im.save(OUT, quality=88, optimize=True)
    print("og-twosuns.jpg  %.0f KB  %dx%d" % (os.path.getsize(OUT) / 1024.0, W, H))


if __name__ == "__main__":
    build()
