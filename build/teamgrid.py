# -*- coding: utf-8 -*-
"""The Company page team grid, in the Zema management style.

Full bleed portrait tiles rather than white cards: the photo fills the tile,
a flat brand wash sits over a desaturated image, and the name and role are laid
over the bottom. People without a portrait get the same tile as a monogram, so a
row still reads as one block. The bio, which that style has no room for, comes up
on hover and focus.
"""

import re

TONES = {
    # slug: (wash colour, wash opacity, monogram panel)
    "warm": ("#C45213", ".58", "linear-gradient(150deg,#8C3D0B,#4E2206)"),
    "dark": ("#1E1A14", ".62", "linear-gradient(150deg,#2E2822,#141110)"),
}

CSS = r"""
  /* TEAM GRID */
  .team{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:28px;}
  .tmb{position:relative;aspect-ratio:720/756;overflow:hidden;background:var(--navy);
    border-radius:4px;}
  .tmb-img{position:absolute;inset:0;background-size:cover;background-position:50% 12%;
    filter:grayscale(1) contrast(1.04);}
  .tmb-wash{position:absolute;inset:0;background:var(--tmb-wash);opacity:var(--tmb-op);}
  .tmb-mono{position:absolute;inset:0;background:var(--tmb-mono);display:flex;
    align-items:center;justify-content:center;font-size:58px;font-weight:300;
    letter-spacing:.04em;color:rgba(255,255,255,.62);}
  .tmb-scrim{position:absolute;inset:auto 0 0;height:62%;
    background:linear-gradient(to top,rgba(10,8,5,.72),rgba(10,8,5,0));}
  .tmb-dl{position:absolute;inset:auto 0 0;padding:22px 22px 20px;z-index:2;}
  .tmb-nm{font-size:22px;font-weight:300;line-height:1.2;color:#fff;}
  .tmb-rl{margin-top:7px;font-size:11.5px;font-weight:700;letter-spacing:2.3px;
    text-transform:uppercase;color:rgba(255,255,255,.88);}
  .tmb-bio{position:absolute;inset:0;z-index:3;padding:26px 24px;display:flex;
    align-items:center;background:rgba(14,11,7,.9);color:rgba(255,255,255,.9);
    font-size:14px;line-height:1.65;opacity:0;transition:opacity .28s ease;}
  .tmb:hover .tmb-bio,.tmb:focus-within .tmb-bio{opacity:1;}
  .tmb-lead .tmb-nm{font-size:25px;}

  @media(max-width:900px){
    .team{grid-template-columns:repeat(2,1fr);}
    .tmb-nm{font-size:19px;}
    .tmb-bio{opacity:1;position:static;background:none;padding:14px 0 0;color:var(--text-muted);}
    .tmb{aspect-ratio:auto;}
  }
"""


def _mono(name):
    parts = [w for w in name.split() if w[:1].isalpha()]
    if len(parts) == 1:
        # one-word names like AbdelAziz carry the second initial inside the word
        inner = re.findall(r"[A-Z][a-z]*", parts[0]) or [parts[0]]
        parts = inner
    return "".join(w[0] for w in parts[:2]).upper()


def tile(name, role, photo, bio, lead=False, e=lambda s: s):
    if photo:
        art = '<div class="tmb-img" style="background-image:url(%s);"></div>' % e(photo)
        wash = '<div class="tmb-wash"></div>'
    else:
        art = '<div class="tmb-mono">%s</div>' % e(_mono(name))
        wash = ""
    return ("""<div class="tmb%s" tabindex="0">%s%s
      <div class="tmb-scrim"></div>
      <div class="tmb-dl"><div class="tmb-nm">%s</div><div class="tmb-rl">%s</div></div>
      <div class="tmb-bio"><div>%s</div></div>
    </div>""" % (" tmb-lead" if lead else "", art, wash, e(name), e(role), e(bio)))


def grid(people, lead=False, e=lambda s: s):
    """people: the roster rows as content2 stores them, 4 long with a photo."""
    out = []
    for p in people:
        if len(p) == 4:
            nm, role, photo, bio = p
        else:
            nm, role, bio = p
            photo = ""
        out.append(tile(nm, role, photo, bio, lead=lead, e=e))
    return '<div class="team">%s</div>' % "".join(out)


def vars_for(tone):
    wash, op, mono = TONES[tone]
    return "--tmb-wash:%s;--tmb-op:%s;--tmb-mono:%s;" % (wash, op, mono)
