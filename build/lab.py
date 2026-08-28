# -*- coding: utf-8 -*-
"""Experiment page: two takes on the Built Industry visual direction.

  "Place the built-asset lifecycle at the centre. Arrange the six operating
   areas around it and use connecting lines to show continuing exchange."
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme import head, chrome_nav, TAIL
from content2 import BUILT

OUT = "/Users/mohammaddidarulalam/Documents/Claude/nexsun/draft/v2/lab.html"

STAGES = BUILT["life_stages"]                      # 11
AREAS = [a[0] for a in BUILT["areas"]]             # 6
SHORT = ["Materials and<br>Manufacturing", "Distribution and<br>Logistics",
         "Asset Owners<br>and Investors", "Construction and<br>Professional Services",
         "Asset Transactions<br>and Operations", "Industry Institutions<br>and Enablement"]
TONE = ["#E0641E", "#CC9900", "#C45213", "#B07E00", "#D9822B", "#8C6500"]

W, H = 1000, 780
CX, CY = W / 2, H / 2
R_WHEEL = 118          # lifecycle disc
R_TICK = 128           # stage ticks
R_LABEL = 156          # stage labels
RX, RY = 342, 286      # where the six areas sit

CSS = """
  .lab-note{background:#fff;border-left:4px solid var(--sun);border-radius:10px;padding:16px 20px;
    margin:18px 0 30px;font-size:15px;color:var(--text-muted);line-height:1.75;max-width:880px;}
  .lab-tag{background:var(--navy);color:#fff;font-size:12px;font-weight:800;letter-spacing:2px;
    text-transform:uppercase;padding:8px 18px;border-radius:6px;display:inline-block;}

  /* ---- take one: radial hub ---- */
  .hub{position:relative;max-width:1000px;margin:34px auto 0;aspect-ratio:1000/780;}
  .hub svg{position:absolute;inset:0;width:100%;height:100%;}
  .hub-node{position:absolute;transform:translate(-50%,-50%);width:190px;text-align:center;
    background:#fff;border:1px solid rgba(140,101,0,.28);border-radius:14px;padding:13px 12px;
    box-shadow:0 8px 24px rgba(60,50,30,.12);cursor:default;
    transition:transform .3s cubic-bezier(.22,1,.36,1),box-shadow .3s,border-color .3s;}
  .hub-node:hover{transform:translate(-50%,-50%) scale(1.07);box-shadow:0 16px 38px rgba(224,100,30,.24);
    border-color:rgba(224,100,30,.55);}
  .hub-node .n{display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;
    border-radius:8px;color:#fff;font-size:12px;font-weight:900;margin-bottom:7px;}
  .hub-node .t{font-size:13px;font-weight:800;color:var(--navy);line-height:1.35;}
  .hub-core{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);text-align:center;
    width:190px;pointer-events:none;}
  .hub-core .k{font-size:10.5px;font-weight:800;letter-spacing:2px;text-transform:uppercase;color:#8C6500;}
  .hub-core .v{font-size:19px;font-weight:900;color:var(--navy);line-height:1.2;margin-top:4px;}
  .hub-core .c{font-size:12px;color:var(--text-muted);margin-top:5px;}
  .stage-lab{position:absolute;transform:translate(-50%,-50%);font-size:10px;font-weight:700;
    letter-spacing:.3px;color:#7A6A4A;white-space:nowrap;pointer-events:none;}
  .wire{stroke:rgba(196,82,19,.28);stroke-width:2;fill:none;}
  .wire-flow{stroke:#E0641E;stroke-width:2.4;fill:none;stroke-linecap:round;
    stroke-dasharray:7 190;animation:labflow 3.4s linear infinite;}
  @keyframes labflow{to{stroke-dashoffset:-197;}}
  .ring{fill:none;stroke:rgba(140,101,0,.22);stroke-width:1.5;}
  .ring-live{fill:none;stroke:#CC9900;stroke-width:3;stroke-linecap:round;
    stroke-dasharray:70 674;animation:labring 9s linear infinite;}
  @keyframes labring{to{stroke-dashoffset:-744;}}
  .tick{stroke:rgba(140,101,0,.45);stroke-width:2;stroke-linecap:round;}

  /* ---- take two: spine ---- */
  .spine{margin-top:34px;}
  .spine-row{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;}
  .spine-card{background:#fff;border:1px solid rgba(140,101,0,.24);border-radius:14px;padding:16px 18px;
    box-shadow:0 8px 24px rgba(60,50,30,.09);transition:transform .3s,box-shadow .3s;}
  .spine-card:hover{transform:translateY(-4px);box-shadow:0 16px 36px rgba(224,100,30,.20);}
  .spine-card .t{font-size:14px;font-weight:800;color:var(--navy);line-height:1.35;}
  .spine-bar{position:relative;margin:26px 0;height:74px;border-radius:14px;
    background:linear-gradient(90deg,#FFF1D6,#FDE2B4,#FFF1D6);border:1px solid rgba(140,101,0,.28);
    display:flex;align-items:center;justify-content:space-between;padding:0 22px;overflow:hidden;}
  .spine-bar::after{content:'';position:absolute;top:0;bottom:0;width:130px;
    background:linear-gradient(90deg,transparent,rgba(255,255,255,.75),transparent);
    animation:labsweep 5s linear infinite;}
  @keyframes labsweep{0%{left:-130px}100%{left:100%}}
  .spine-stage{position:relative;z-index:2;font-size:10.5px;font-weight:800;letter-spacing:.4px;
    color:#7A6A4A;text-align:center;line-height:1.25;}
  .spine-stage span{display:block;width:9px;height:9px;border-radius:50%;background:var(--sun);
    margin:0 auto 6px;box-shadow:0 0 0 3px rgba(224,100,30,.16);}
  .spine-legs{display:grid;grid-template-columns:repeat(6,1fr);height:26px;}
  .spine-legs i{border-left:2px dashed rgba(196,82,19,.35);height:100%;margin:0 auto;width:0;}

  @media(max-width:900px){
    .hub{display:none;}
    .hub-fallback{display:block;}
    .spine-row{grid-template-columns:1fr;}
    .spine-bar{flex-wrap:wrap;height:auto;padding:16px;gap:12px;justify-content:center;}
    .spine-legs{display:none;}
  }
  .hub-fallback{display:none;}
  .hub-fallback .card{margin-bottom:12px;}
  @media(prefers-reduced-motion:reduce){
    .wire-flow,.ring-live,.spine-bar::after{animation:none;}
  }
"""


def polar(cx, cy, rx, ry, deg):
    r = math.radians(deg)
    return cx + rx * math.cos(r), cy + ry * math.sin(r)


def take_one():
    angles = [-90, -30, 30, 90, 150, 210]
    wires, nodes, labels = "", "", ""

    for i, deg in enumerate(angles):
        x, y = polar(CX, CY, RX, RY, deg)
        # start just outside the label ring, stop just before the card
        sx, sy = polar(CX, CY, R_LABEL + 26, R_LABEL + 26, deg)
        ex, ey = polar(CX, CY, RX - 58, RY - 52, deg)
        wires += '<path class="wire" d="M%.0f %.0f L%.0f %.0f"/>' % (sx, sy, ex, ey)
        wires += '<path class="wire-flow" d="M%.0f %.0f L%.0f %.0f" style="animation-delay:%.1fs"/>' % (
            sx, sy, ex, ey, i * .55)
        nodes += ('<div class="hub-node" style="left:%.2f%%;top:%.2f%%;">'
                  '<span class="n" style="background:%s">%d</span>'
                  '<div class="t">%s</div></div>') % (x / W * 100, y / H * 100, TONE[i], i + 1, SHORT[i])

    ticks = ""
    step = 360.0 / len(STAGES)
    for j, st in enumerate(STAGES):
        deg = -90 + j * step
        x1, y1 = polar(CX, CY, R_WHEEL, R_WHEEL, deg)
        x2, y2 = polar(CX, CY, R_TICK, R_TICK, deg)
        ticks += '<line class="tick" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (x1, y1, x2, y2)
        lx, ly = polar(CX, CY, R_LABEL, R_LABEL, deg)
        labels += '<div class="stage-lab" style="left:%.2f%%;top:%.2f%%;">%s</div>' % (
            lx / W * 100, ly / H * 100, st)

    fallback = "".join(
        '<div class="card"><span class="card-num" style="background:%s;">%d</span><h3>%s</h3></div>'
        % (TONE[i], i + 1, a) for i, a in enumerate(AREAS))

    return """<div class="hub">
  <svg viewBox="0 0 %d %d" aria-hidden="true">
    %s
    <circle class="ring" cx="%.0f" cy="%.0f" r="%d"/>
    <circle class="ring-live" cx="%.0f" cy="%.0f" r="%d"/>
    %s
  </svg>
  %s
  <div class="hub-core">
    <div class="k">At the centre</div>
    <div class="v">The built-asset lifecycle</div>
    <div class="c">Eleven stages, continuously exchanging</div>
  </div>
  %s
</div>
<div class="hub-fallback"><div class="grid3" style="margin-top:24px;">%s</div></div>
""" % (W, H, wires, CX, CY, R_WHEEL, CX, CY, R_WHEEL, ticks, nodes, labels, fallback)


def take_two():
    top = "".join(
        '<div class="spine-card"><span class="card-num" style="background:%s;">%d</span>'
        '<div class="t">%s</div></div>' % (TONE[i], i + 1, AREAS[i]) for i in range(3))
    bot = "".join(
        '<div class="spine-card"><span class="card-num" style="background:%s;">%d</span>'
        '<div class="t">%s</div></div>' % (TONE[i], i + 1, AREAS[i]) for i in range(3, 6))
    stages = "".join('<div class="spine-stage"><span></span>%s</div>' % s.replace(" or ", "<br>or ")
                     for s in STAGES)
    legs = '<div class="spine-legs">' + "<i></i>" * 6 + "</div>"
    return """<div class="spine">
  <div class="spine-row">%s</div>
  %s
  <div class="spine-bar">%s</div>
  %s
  <div class="spine-row">%s</div>
</div>
""" % (top, legs, stages, legs, bot)


s = head("Lifecycle diagram experiment | TwoSuns", "Two takes on the Built Industry visual direction.",
         extra_css=CSS)
s += chrome_nav(None)
s += """<section style="padding:52px 0 26px;">
  <div class="container">
    <div class="section-tag">Experiment</div>
    <h1 class="section-heading" style="font-size:clamp(26px,3.4vw,40px);">The built-asset lifecycle, two ways</h1>
    <p class="section-sub">The document asks to place the lifecycle at the centre, arrange the six
      operating areas around it, and use connecting lines to show continuing exchange. Two takes below.
      Nothing here touches the Built Industry page. Pick one and I will build it there.</p>
  </div>
</section>
<div class="sun-divider"></div>

<section class="band-alt">
  <div class="container">
    <span class="lab-tag">Take one &nbsp;&middot;&nbsp; Radial hub</span>
    <div class="lab-note">Literal reading of the brief. The lifecycle sits at the centre with its eleven
      stages marked around the disc, the six operating areas orbit it, and pulses travel the connecting
      lines outward. Strongest argument that the industry is one connected system. Costs vertical space
      and needs a stacked fallback on phones.</div>
""" + take_one() + """
  </div>
</section>

<div class="sun-divider"></div>
<section>
  <div class="container">
    <span class="lab-tag">Take two &nbsp;&middot;&nbsp; Lifecycle spine</span>
    <div class="lab-note">Looser reading. The lifecycle runs as a horizontal spine with the six areas
      branching above and below, connected by dashed legs. Every stage label stays horizontal and
      readable, it survives mobile without a fallback, and it fits the page rhythm. Less dramatic, and
      it reads as a sequence rather than a system.</div>
""" + take_two() + """
  </div>
</section>

<section class="cta-band" style="padding:64px 0;">
  <div class="container">
    <h2>One or two?</h2>
    <p>Tell me which and I will build it into Built Industry, then this page goes away.</p>
  </div>
</section>
"""
s += TAIL
open(OUT, "w").write(s)
print("wrote lab.html,", len(s), "bytes")
