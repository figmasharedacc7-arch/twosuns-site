# -*- coding: utf-8 -*-
"""Built Industry rendered with a functional palette, for comparison only.

The brand's primary voice is untouched: hero, CTAs, dividers and the warm cream
ground all stay. What changes is the categorical set, so the six operating areas
read as six distinct things rather than six shades of one.
"""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build, eclipse

# hue AND lightness both vary, so the set survives colour-blindness and greyscale
ALT = ["#C0522A",  # 1 Materials          terracotta, keeps the brand link
       "#1E6F63",  # 2 Distribution       deep teal
       "#3D4F8A",  # 3 Owners             indigo
       "#B07E00",  # 4 Construction       ochre, already in the palette
       "#7B3F63",  # 5 Transactions       plum
       "#4F6B2A"]  # 6 Institutions       olive

OUT = os.path.join(build.OUT, "built-industry-alt.html")

build.ACCENTS = ALT[:]
eclipse.TONES = ALT[:]

page = build.build_built()

banner = """<div style="position:fixed;left:0;right:0;bottom:0;z-index:200;background:#1E1A14;color:#FFF3DC;
  padding:11px 20px;font-size:12.5px;font-weight:700;letter-spacing:.4px;text-align:center;">
  Comparison only &nbsp;&middot;&nbsp; same page, functional palette on the six areas.
  The brand voice, hero, buttons and cream ground are unchanged.
</div>"""
page = page.replace("</body>", banner + "\n</body>")
page = page.replace("<title>Built Industry | TwoSuns</title>",
                    "<title>Built Industry, functional palette | TwoSuns</title>")

open(OUT, "w").write(page)
print("wrote", os.path.basename(OUT), len(page), "bytes")

# prove the swap actually reached both the cards and the diagram
s = open(OUT).read()
for i, c in enumerate(ALT, 1):
    print("  %d %-8s occurrences: %d" % (i, c, s.count(c)))
old = ["var(--a1)", "var(--a2)", "var(--a3)", "var(--a4)", "var(--a5)", "var(--a6)"]
print("  old accent vars left:", sum(s.count(o) for o in old))
