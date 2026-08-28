# -*- coding: utf-8 -*-
"""Scratch page: the real photos in both candidate treatments, so the choice is visual."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme import head, chrome_nav, TAIL
from content2 import BUILT

OUT = "/Users/mohammaddidarulalam/Documents/Claude/nexsun/draft/v2/compare.html"
V2 = os.path.dirname(OUT)

# slot -> which of the six areas it fills, in BUILT["areas"] order
SLOTS = ["area-materials", "area-distribution", "area-owners",
         "area-construction", "area-operations", "area-institutions"]

EXTRA = """
  .cardimg{border-radius:16px;overflow:hidden;background:#fff;border:1px solid var(--border);
    box-shadow:var(--shadow);transition:all .3s;display:flex;flex-direction:column;}
  .cardimg:hover{transform:translateY(-5px);box-shadow:0 12px 40px rgba(224,100,30,.14);
    border-color:rgba(224,100,30,.4);}
  .cardimg .ph{aspect-ratio:16/9;background-size:cover;background-position:center 45%;
    background-color:#F3E6C8;}
  .cardimg .ph.empty{display:flex;align-items:center;justify-content:center;
    color:#B9A87E;font-size:11.5px;font-weight:800;letter-spacing:1.6px;text-transform:uppercase;
    text-align:center;padding:12px;}
  .cardimg .bd{padding:22px 24px 26px;}
  .cardimg h3{font-size:17.5px;font-weight:800;color:var(--navy);margin-bottom:8px;}
  .cardimg p{font-size:14px;color:var(--text-muted);line-height:1.7;}
  .opt-label{background:var(--navy);color:#fff;font-size:12px;font-weight:800;letter-spacing:2px;
    text-transform:uppercase;padding:8px 18px;border-radius:6px;display:inline-block;}
  .verdict{background:#fff;border-left:4px solid var(--sun);border-radius:10px;padding:18px 22px;
    margin-top:20px;font-size:15px;color:var(--text-muted);line-height:1.75;max-width:860px;}
  .verdict.bad{border-left-color:#C00000;}
  .imgsec-con::before{background-image:url('area-construction.jpg');}
  .imgsec-dis::before{background-image:url('area-distribution.jpg');}
"""

s = head("Treatment comparison | TwoSuns", "Scratch page comparing image treatments.", extra_css=EXTRA)
s += chrome_nav(None)

s += """<section style="padding:52px 0 30px;">
  <div class="container">
    <div class="section-tag">Scratch page</div>
    <h1 class="section-heading" style="font-size:clamp(26px,3.4vw,40px);">Two ways to use the six area photos</h1>
    <p class="section-sub">Your real photos, at real page width. Pick A or B and I will build the
      Built Industry page that way, then delete this page.</p>
  </div>
</section>
<div class="sun-divider"></div>
"""


def full_bleed(cls, idx, tag):
    a = BUILT["areas"][idx]
    return """<section class="imgsec %s" style="padding:78px 0;">
  <div class="container">
   <div class="sec-split">
    <div class="section-tag">%s</div>
    <h2 class="section-heading">%s</h2>
    <p class="section-sub">%s</p>
    <ul class="tick">%s</ul>
   </div>
  </div>
</section>
""" % (cls, tag, a[0], a[1], "".join("<li>%s</li>" % b for b in a[2]))


s += """<section style="padding:44px 0 8px;"><div class="container">
  <span class="opt-label">Option A &nbsp;&middot;&nbsp; Full bleed section</span>
  <p class="section-sub" style="margin-top:16px;">Works when the photo has a quiet side. The
    construction shot below has open sky on the right, so the copy sits cleanly on it.</p>
</div></section>
"""
s += full_bleed("imgsec-l imgsec-con", 3, "Operating area 4")

s += """<section style="padding:30px 0 8px;"><div class="container">
  <div class="verdict bad"><strong>And when it does not.</strong> The timber yard below is busy edge to
    edge with the people dead centre, so the copy lands on texture and the three workers end up under
    the headline. Two of your four photos so far have this shape. Full bleed only flatters photos
    composed with empty space on one side.</div>
</div></section>
"""
s += full_bleed("imgsec-r imgsec-dis", 1, "Operating area 2")

s += """<section style="padding:26px 0 60px;"><div class="container">
  <div class="verdict"><strong>What Option A costs.</strong> Each area becomes its own full width
    section, so the Built Industry page grows to roughly three times its length, and each photo ships
    at 2400px. Six of them is around 4.5 MB on one page.</div>
</div></section>
<div class="sun-divider"></div>
"""

cards = ""
for i, (name, desc, bullets) in enumerate(BUILT["areas"]):
    card = SLOTS[i] + "-card.jpg"
    if os.path.exists(os.path.join(V2, card)):
        ph = '<div class="ph" style="background-image:url(\'%s\');"></div>' % card
    else:
        ph = '<div class="ph empty">%s<br>not downloaded yet</div>' % SLOTS[i]
    cards += '<div class="cardimg">%s<div class="bd"><h3>%s</h3><p>%s</p></div></div>' % (ph, name, desc)

s += """<section class="band-alt" style="padding:46px 0 76px;">
  <div class="container">
    <span class="opt-label">Option B &nbsp;&middot;&nbsp; Photo headed cards</span>
    <h2 class="section-heading" style="margin-top:18px;">Six connected operating areas</h2>
    <div class="grid3">%s</div>
    <div class="verdict"><strong>What Option B costs.</strong> The page keeps its length, the six areas
      stay side by side and comparable, and composition stops mattering because no text sits on the
      photo. Each card image ships at 1000px, roughly 150 KB, so all six come to about 1 MB.</div>
  </div>
</section>
""" % cards

s += """<section class="cta-band" style="padding:66px 0;">
  <div class="container">
    <h2>A or B?</h2>
    <p>Tell me which and I will build it, then this page goes away.</p>
  </div>
</section>
"""

open(OUT, "w").write(s + TAIL)
print("wrote compare.html,", len(s + TAIL), "bytes")
