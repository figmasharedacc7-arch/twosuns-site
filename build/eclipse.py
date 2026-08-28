# -*- coding: utf-8 -*-
"""The Eclipse lifecycle diagram, production build.

Serves the Built Industry visual direction: the built-asset lifecycle at the
centre, the six operating areas around it, connecting lines showing exchange.
Drawn as SVG plus positioned HTML so every label stays real text.
"""
import math

VB_W, VB_H = 1280, 800          # wide enough that the outer labels stay inside the frame
CX1, CX2, CY, R = 544, 736, 366, 236
MID = (CX1 + CX2) / 2
TONES = ["#E0641E", "#CC9900", "#C45213", "#B07E00", "#D9822B", "#8C6500"]
# 1 to 3 read down the left disc, 4 to 6 down the right, matching the numbered
# list the page falls back to on phones
ANGLES = [215, 180, 145, 325, 0, 35]

CSS = r"""
  /* ECLIPSE: the two suns are the diagram, the overlap is the lifecycle */
  .ecl{position:relative;width:100%;max-width:1140px;margin:34px auto 0;aspect-ratio:1280/800;
    container-type:inline-size;}
  .ecl svg{position:absolute;inset:0;width:100%;height:100%;}
  .ecl-lab{position:absolute;transform:translateY(-50%);width:15.5%;}
  .ecl-lab .i{font-size:10px;font-size:.86cqw;font-weight:800;letter-spacing:2px;}
  .ecl-lab .r{height:1px;opacity:.45;margin:5px 0 6px;}
  .ecl-lab .t{font-size:13px;font-size:1.12cqw;font-weight:700;color:var(--navy);line-height:1.36;}
  .ecl-core{position:absolute;left:50%;transform:translate(-50%,-50%);width:20%;text-align:center;
    background:#FFFBF0;padding:12px 8px 14px;border-radius:8px;}
  .ecl-core .k{font-size:9.5px;font-size:.82cqw;font-weight:800;letter-spacing:2.6px;
    text-transform:uppercase;color:#8C6500;}
  .ecl-core .v{font-size:19px;font-size:1.62cqw;font-weight:900;color:var(--navy);line-height:1.2;margin-top:5px;}
  .ecl-core .c{font-size:11.5px;font-size:1.0cqw;color:var(--text-muted);margin-top:5px;}
  .ecl-fallback{display:none;}

  @media(max-width:860px){
    .ecl{display:none;}
    .ecl-fallback{display:block;margin-top:26px;}
    .ecl-mini{position:relative;height:150px;margin:0 auto 22px;max-width:300px;}
    .ecl-mini svg{width:100%;height:100%;}
    .ecl-list{display:grid;gap:10px;}
    .ecl-list li{list-style:none;display:flex;gap:12px;align-items:flex-start;
      background:#fff;border:1px solid var(--border-soft);border-radius:12px;padding:12px 14px;}
    .ecl-list .n{flex-shrink:0;width:24px;height:24px;border-radius:8px;color:#fff;font-size:12px;
      font-weight:900;display:flex;align-items:center;justify-content:center;}
    .ecl-list .t{font-size:14px;font-weight:700;color:var(--navy);line-height:1.4;}
  }
"""


def _defs(suffix=""):
    return """<defs>
    <radialGradient id="eg%s" cx="34%%" cy="30%%">
      <stop offset="0" stop-color="#FFFDF0"/><stop offset=".34" stop-color="#F6E4A4"/>
      <stop offset=".72" stop-color="#DFC15C"/><stop offset="1" stop-color="#CC9900"/></radialGradient>
    <radialGradient id="eo%s" cx="34%%" cy="30%%">
      <stop offset="0" stop-color="#FFF4E8"/><stop offset=".32" stop-color="#FFB077"/>
      <stop offset=".70" stop-color="#F2762A"/><stop offset="1" stop-color="#E0641E"/></radialGradient>
    <radialGradient id="ec%s"><stop offset=".55" stop-color="rgba(224,100,30,.20)"/>
      <stop offset="1" stop-color="rgba(224,100,30,0)"/></radialGradient>
    <filter id="eng%s" x="0" y="0" width="100%%" height="100%%">
      <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="4" stitchTiles="stitch"/>
      <feColorMatrix type="saturate" values="0"/></filter>
    <clipPath id="el%s"><circle cx="%d" cy="%d" r="%d"/></clipPath>
  </defs>""" % (suffix, suffix, suffix, suffix, suffix, CX1, CY, R)


def section(heading, para, stages, areas):
    def pol(cx, cy, r, deg):
        a = math.radians(deg)
        return cx + r * math.cos(a), cy + r * math.sin(a)

    svg = ['<svg viewBox="0 0 %d %d" role="img" aria-label="The built-asset lifecycle at the centre, '
           'with the six operating areas around it.">' % (VB_W, VB_H), _defs()]
    svg.append('<circle cx="%.0f" cy="%d" r="420" fill="url(#ec)"/>' % (MID, CY))
    svg.append('<circle cx="%d" cy="%d" r="%d" fill="url(#eg)"/>' % (CX1, CY, R))
    svg.append('<circle cx="%d" cy="%d" r="%d" fill="url(#eo)" opacity=".9"/>' % (CX2, CY, R))
    svg.append('<g clip-path="url(#el)"><circle cx="%d" cy="%d" r="%d" fill="#FFFBF0" opacity=".96"/></g>'
               % (CX2, CY, R))
    svg.append('<g clip-path="url(#el)"><circle cx="%d" cy="%d" r="%d" fill="none" stroke="#FFF6DC" '
               'stroke-width="3" opacity=".9"/></g>' % (CX2, CY, R))
    svg.append('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="rgba(140,101,0,.45)"/>' % (CX1, CY, R))
    svg.append('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="rgba(196,82,19,.45)"/>' % (CX2, CY, R))

    # one tick per lifecycle stage, running down the overlap
    n = len(stages)
    top = CY - (n - 1) * 30 / 2
    for i in range(n):
        y = top + i * 30
        svg.append('<line x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f" stroke="rgba(140,101,0,.5)" '
                   'stroke-width="1.5"><title>%s</title></line>' % (MID - 26, y, MID + 26, y, stages[i]))

    labels = []
    for i, deg in enumerate(ANGLES):
        base = CX1 if 120 < deg < 300 else CX2
        px, py = pol(base, CY, R, deg)
        ex, ey = pol(base, CY, R + 62, deg)
        svg.append('<line x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f" stroke="%s" stroke-width="1.5" opacity=".6"/>'
                   % (px, py, ex, ey, TONES[i]))
        svg.append('<circle cx="%.0f" cy="%.0f" r="5" fill="%s"/>' % (px, py, TONES[i]))
        svg.append('<circle cx="%.0f" cy="%.0f" r="9.5" fill="none" stroke="%s" stroke-width="1" opacity=".4"/>'
                   % (px, py, TONES[i]))
        right = ex >= MID
        pos = ("left:%.2f%%" % ((ex + 14) / VB_W * 100)) if right else \
              ("right:%.2f%%" % ((VB_W - ex + 14) / VB_W * 100))
        labels.append("""<div class="ecl-lab" style="%s;top:%.2f%%;text-align:%s;">
        <div class="i" style="color:%s;">%02d</div>
        <div class="r" style="background:%s;"></div>
        <div class="t">%s</div>
      </div>""" % (pos, ey / VB_H * 100, "left" if right else "right", TONES[i], i + 1, TONES[i], areas[i]))
    svg.append('<rect width="%d" height="%d" filter="url(#eng)" opacity=".055"/>' % (VB_W, VB_H))
    svg.append("</svg>")

    core = """<div class="ecl-core" style="top:%.2f%%;">
      <div class="k">Where they overlap</div>
      <div class="v">The built-asset lifecycle</div>
      <div class="c">Eleven stages</div>
    </div>""" % (CY / VB_H * 100)

    mini = """<div class="ecl-mini"><svg viewBox="0 0 %d %d" aria-hidden="true">%s
      <circle cx="%d" cy="%d" r="%d" fill="url(#egm)"/>
      <circle cx="%d" cy="%d" r="%d" fill="url(#eom)" opacity=".9"/>
      <g clip-path="url(#elm)"><circle cx="%d" cy="%d" r="%d" fill="#FFFBF0" opacity=".96"/></g>
    </svg></div>""" % (VB_W, VB_H, _defs("m"), CX1, CY, R, CX2, CY, R, CX2, CY, R)

    lst = "".join('<li><span class="n" style="background:%s;">%d</span><span class="t">%s</span></li>'
                  % (TONES[i], i + 1, a) for i, a in enumerate(areas))

    return """<section class="band-alt">
  <div class="container">
    <div class="section-tag">Lifecycle</div>
    <h2 class="section-heading">%s</h2>
    <p class="lede">%s</p>
    <div class="ecl">%s%s%s</div>
    <div class="ecl-fallback">%s<ul class="ecl-list">%s</ul></div>
  </div>
</section>
""" % (heading, para, "".join(svg), core, "".join(labels), mini, lst)
