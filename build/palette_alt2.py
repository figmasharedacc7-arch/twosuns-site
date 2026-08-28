# -*- coding: utf-8 -*-
"""Use Cases with colour actually doing work: area filters and area tags carry their own hue."""
import os, re, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build
from content2 import UC_AREA_LABELS

ALT = ["#C0522A", "#1E6F63", "#3D4F8A", "#B07E00", "#7B3F63", "#4F6B2A"]
src = os.path.join(build.OUT, "use-cases.html")
dst = os.path.join(build.OUT, "use-cases-alt.html")
s = open(src).read()

# 1. the six area filter buttons take their own colour
for i, c in enumerate(ALT):
    pat = r'(<button class="uc-filter" data-dim="area" data-f="a%d")>' % i
    rep = r'\1 style="border-color:%s;color:%s;">' % (c, c)
    s, n = re.subn(pat, rep, s)
    assert n == 1, "area filter %d not found" % i

# 2. an active area filter fills with its colour
s = s.replace(".uc-filter.on{background:linear-gradient(135deg,var(--sun),var(--sun-deep));color:#fff;border-color:transparent;}",
              ".uc-filter.on{background:linear-gradient(135deg,var(--sun),var(--sun-deep));color:#fff;border-color:transparent;}\n"
              + "\n".join(
                  '  .uc-filter[data-f="a%d"].on{background:%s!important;color:#fff!important;border-color:%s!important;}'
                  % (i, c, c) for i, c in enumerate(ALT)))

# 3. area tags on the cards match, so a filtered result is visibly the thing you asked for
for i, (lab, c) in enumerate(zip(UC_AREA_LABELS, ALT)):
    esc = html.escape(lab, quote=False)
    s = s.replace('<span class="uc-tag">%s</span>' % esc,
                  '<span class="uc-tag" style="border-color:%s;color:%s;">%s</span>' % (c, c, esc))

s = s.replace("<title>Use Cases | TwoSuns</title>",
              "<title>Use Cases, functional palette | TwoSuns</title>")
s = s.replace("</body>", """<div style="position:fixed;left:0;right:0;bottom:0;z-index:200;background:#1E1A14;
  color:#FFF3DC;padding:11px 20px;font-size:12.5px;font-weight:700;text-align:center;">
  Comparison only &nbsp;&middot;&nbsp; area filters and area tags carry their own hue, so a filtered result is
  visibly the thing you asked for.</div>
</body>""")
open(dst, "w").write(s)
print("wrote use-cases-alt.html", len(s), "bytes")
print("  coloured filter buttons:", sum(s.count('data-f="a%d" style' % i) for i in range(6)))
print("  coloured area tags     :", sum(s.count('uc-tag" style="border-color:%s' % c) for c in ALT))
