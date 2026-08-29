# -*- coding: utf-8 -*-
"""The platform architecture diagram.

Horizon and Pulse as two overlapping domains, Core as the governed context
sitting across the overlap, Ray spanning beneath, with flow arrows carrying
context in and coordinated action back out.

Drawn as SVG plus positioned HTML so every label stays selectable text that
scales with the container. Below 900px it stacks.
"""

VB_W, VB_H = 2000, 1130
VB_Y0, VB_VIS = 195, 990   # crop the viewBox to where the drawing actually starts

HX, HY, HR = 660, 575, 278          # Horizon disc
PX, PY, PR = 1400, 575, 278         # Pulse disc
CX, CY, CW, CH = 1005, 578, 384, 468   # Core panel
GOLD, ORANGE, DEEP = "#E0B33A", "#F97316", "#C45213"

CSS = r"""
  /* PLATFORM ARCHITECTURE */
  .arx{position:relative;width:100%;max-width:1180px;margin:22px auto 0;aspect-ratio:2000/990;
    container-type:inline-size;}
  .arx svg{position:absolute;inset:0;width:100%;height:100%;}
  .arx-lab{position:absolute;transform:translate(-50%,-50%);text-align:center;}
  .arx-k{font-size:11px;font-size:.72cqw;font-weight:800;letter-spacing:.22em;text-transform:uppercase;}
  .arx-n{font-size:34px;font-size:2.5cqw;font-weight:900;letter-spacing:-.01em;line-height:1;margin-top:.5cqw;}
  .arx-rule{height:1px;margin:1.1cqw auto .9cqw;}
  .arx-list{list-style:none;margin:0;padding:0;text-align:left;display:grid;gap:.55cqw;}
  .arx-list li{position:relative;padding-left:1.35cqw;font-size:15px;font-size:1.02cqw;line-height:1.35;}
  .arx-list li::before{content:'';position:absolute;left:0;top:.42em;width:.42cqw;height:.42cqw;
    border-radius:50%;background:currentColor;opacity:.65;}
  .arx-domain{width:19.5%;color:#2A231B;}
  .arx-core{width:19.2%;color:#F6EEDE;}
  .arx-core .arx-lines{display:grid;gap:.6cqw;font-size:15px;font-size:1.02cqw;line-height:1.35;}
  .arx-orbit{position:absolute;transform:translate(-50%,-50%);display:flex;align-items:center;gap:.5cqw;
    font-size:11px;font-size:.7cqw;font-weight:800;letter-spacing:.18em;text-transform:uppercase;
    color:#6E6152;white-space:nowrap;}
  .arx-orbit i{width:.5cqw;height:.5cqw;border-radius:50%;flex-shrink:0;}
  .arx-ray{position:absolute;left:50%;transform:translateX(-50%);background:#fff;border-radius:999px;
    box-shadow:0 14px 40px rgba(60,50,30,.14);display:flex;align-items:center;justify-content:center;
    flex-direction:column;gap:.7cqw;}
  .arx-ray-top{display:flex;align-items:baseline;gap:.85cqw;}
  .arx-ray-name{font-size:30px;font-size:2.1cqw;font-weight:900;color:#B8860B;letter-spacing:.01em;}
  .arx-ray-sub{font-size:18px;font-size:1.25cqw;font-weight:800;color:#2A231B;}
  .arx-ray-items{display:flex;gap:2.2cqw;font-size:15px;font-size:1.02cqw;color:#5A554C;}
  .arx-ray-items span{display:flex;align-items:center;gap:.5cqw;}
  .arx-ray-items i{width:.45cqw;height:.45cqw;border-radius:50%;}
  .arx-foot{margin-top:22px;text-align:center;font-size:14.5px;font-weight:800;color:#5A554C;}
  .arx-fallback{display:none;}

  @media(max-width:900px){
    .arx{display:none;}
    .arx-fallback{display:grid;gap:14px;margin-top:28px;}
    .arxf{border-radius:18px;padding:22px 22px 24px;}
    .arxf .k{font-size:10.5px;font-weight:800;letter-spacing:.2em;text-transform:uppercase;}
    .arxf .n{font-size:26px;font-weight:900;line-height:1;margin-top:4px;}
    .arxf ul{list-style:none;margin:14px 0 0;padding:0;display:grid;gap:8px;}
    .arxf li{position:relative;padding-left:18px;font-size:14.5px;line-height:1.5;}
    .arxf li::before{content:'';position:absolute;left:0;top:.55em;width:6px;height:6px;border-radius:50%;
      background:currentColor;opacity:.6;}
    .arxf-h{background:linear-gradient(140deg,#F6DE93,#E0B33A);color:#2A231B;}
    .arxf-c{background:linear-gradient(140deg,#2A2520,#171310);color:#F6EEDE;}
    .arxf-c .n{color:#fff;}
    .arxf-p{background:linear-gradient(140deg,#FDBA74,#F97316);color:#2A231B;}
    .arxf-r{background:#fff;border:1px solid var(--border);color:#5A554C;}
    .arxf-r .n{color:#B8860B;}
  }
"""


def _pct(x, y):
    return "left:%.2f%%;top:%.2f%%" % (x / VB_W * 100, (y - VB_Y0) / VB_VIS * 100)


def section(heading, sub, explore_btn="", tag="Architecture", band="band-alt",
            foot="One governed context. Two operating domains. Continuous enterprise awareness."):
    """The diagram, wrapped in its own band. Home introduces it as the architecture,
    Platform reuses it to show the same context circulating."""
    s = ['<svg viewBox="0 %d %d %d" role="img" aria-label="Horizon and Pulse as two operating '
         'domains, Core as the governed context between them, Ray spanning beneath.">' % (VB_Y0, VB_W, VB_VIS)]
    s.append("""<defs>
      <radialGradient id="axh" cx="36%%" cy="30%%">
        <stop offset="0" stop-color="#FBEBB4"/><stop offset=".55" stop-color="#EFCE6B"/>
        <stop offset="1" stop-color="%s"/></radialGradient>
      <radialGradient id="axp" cx="36%%" cy="30%%">
        <stop offset="0" stop-color="#FFD3A8"/><stop offset=".5" stop-color="#FBA05A"/>
        <stop offset="1" stop-color="%s"/></radialGradient>
      <linearGradient id="axc" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stop-color="#2E2822"/><stop offset="1" stop-color="#141110"/></linearGradient>
      <marker id="axag" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">
        <path d="M0 0 L10 5 L0 10 z" fill="%s"/></marker>
      <marker id="axao" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">
        <path d="M0 0 L10 5 L0 10 z" fill="%s"/></marker>
    </defs>""" % (GOLD, ORANGE, GOLD, ORANGE))

    # the wide field the domains sit in
    s.append('<ellipse cx="1020" cy="575" rx="840" ry="336" fill="none" stroke="rgba(140,101,0,.30)" '
             'stroke-dasharray="3 11"/>')
    s.append('<ellipse cx="1020" cy="575" rx="792" ry="300" fill="none" stroke="rgba(224,100,30,.10)" '
             'stroke-width="26"/>')

    # the two domains
    s.append('<circle cx="%d" cy="%d" r="%d" fill="url(#axh)"/>' % (HX, HY, HR))
    s.append('<circle cx="%d" cy="%d" r="%d" fill="url(#axp)"/>' % (PX, PY, PR))

    # context in, coordinated action back out
    s.append('<path d="M470 352 C640 236 860 250 946 292" fill="none" stroke="%s" stroke-width="7" '
             'stroke-linecap="round" opacity=".85" marker-end="url(#axag)"/>' % GOLD)
    s.append('<path d="M1584 300 C1420 238 1180 250 1074 292" fill="none" stroke="%s" stroke-width="7" '
             'stroke-linecap="round" opacity=".85" marker-end="url(#axao)"/>' % ORANGE)
    s.append('<path d="M660 848 C790 906 930 878 1012 846" fill="none" stroke="%s" stroke-width="7" '
             'stroke-linecap="round" opacity=".8" marker-end="url(#axag)"/>' % GOLD)
    s.append('<path d="M1382 848 C1268 906 1140 878 1074 846" fill="none" stroke="%s" stroke-width="7" '
             'stroke-linecap="round" opacity=".8" marker-end="url(#axao)"/>' % ORANGE)
    s.append('<line x1="1005" y1="820" x2="1005" y2="884" stroke="rgba(60,50,30,.30)" stroke-width="3"/>')

    # the governed context, sitting across the overlap
    s.append('<rect x="%d" y="%d" width="%d" height="%d" rx="30" fill="#fff"/>'
             % (CX - CW / 2 - 9, CY - CH / 2 - 9, CW + 18, CH + 18))
    s.append('<rect x="%d" y="%d" width="%d" height="%d" rx="24" fill="url(#axc)"/>'
             % (CX - CW / 2, CY - CH / 2, CW, CH))
    s.append('<rect x="%d" y="%d" width="%d" height="%d" rx="20" fill="none" stroke="rgba(224,178,80,.35)"/>'
             % (CX - CW / 2 + 8, CY - CH / 2 + 8, CW - 16, CH - 16))
    # a faint mesh, so the panel reads as a system not a slab
    mesh = [(872, 430), (1005, 396), (1140, 432), (1150, 560), (1006, 604), (866, 566),
            (884, 700), (1010, 742), (1132, 700)]
    for i, (mx, my) in enumerate(mesh):
        for jx, jy in mesh[i + 1:]:
            if abs(mx - jx) + abs(my - jy) < 210:
                s.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="rgba(224,178,80,.16)"/>'
                         % (mx, my, jx, jy))
    for mx, my in mesh:
        s.append('<circle cx="%d" cy="%d" r="4" fill="rgba(224,178,80,.45)"/>' % (mx, my))
    # the three tone dots under the Core copy
    s.append('<line x1="948" y1="756" x2="1062" y2="756" stroke="rgba(246,238,222,.35)" stroke-width="2"/>')
    for dx, col in ((948, GOLD), (1005, "#fff"), (1062, ORANGE)):
        s.append('<circle cx="%d" cy="756" r="7" fill="%s"/>' % (dx, col))
    s.append("</svg>")

    def domain(x, y, kicker, name, items, tone, rule):
        return """<div class="arx-lab arx-domain" style="%s;">
      <div class="arx-k" style="color:%s;">%s</div>
      <div class="arx-n">%s</div>
      <div class="arx-rule" style="background:%s;"></div>
      <ul class="arx-list">%s</ul>
    </div>""" % (_pct(x, y), tone, kicker, name, rule,
                 "".join("<li>%s</li>" % i for i in items))

    horizon = domain(596, HY - 6, "Commercial intelligence", "HORIZON",
                     ["Market and account intelligence", "Revenue coordination", "GTM execution"],
                     "#8A6A12", "rgba(90,70,15,.35)")
    pulse = domain(1454, PY - 6, "Operational execution", "PULSE",
                   ["Operational workflows", "Supply and resource coordination", "Performance management"],
                   "#8C3D0B", "rgba(120,55,10,.35)")

    core = """<div class="arx-lab arx-core" style="%s;">
      <div class="arx-k" style="color:#E0B33A;">Governed context</div>
      <div class="arx-n" style="color:#fff;">CORE</div>
      <div class="arx-rule" style="background:rgba(224,178,80,.4);"></div>
      <div class="arx-lines">
        <div>Governance and permissions</div>
        <div>Organizational memory and logs</div>
        <div>Decision continuity</div>
      </div>
    </div>""" % _pct(CX, CY - 34)

    orbits = ""
    for x, y, label, col, align in [
            (300, 352, "Markets", GOLD, "left"),
            (330, 790, "Customers", GOLD, "left"),
            (1596, 330, "Operations", ORANGE, "left"),
            (1672, 806, "People and systems", ORANGE, "left")]:
        orbits += ('<div class="arx-orbit" style="%s;transform:translateY(-50%%);">'
                   '<i style="background:%s;"></i>%s</div>') % (_pct(x, y).replace("top:", "top:"), col, label)

    ray = """<div class="arx-ray" style="left:50%%;top:%.2f%%;width:%.2f%%;padding:1.9cqw 2.4cqw;">
      <div class="arx-ray-top">
        <span class="arx-ray-name">RAY</span>
        <span class="arx-ray-sub">Persistent enterprise companion</span>
      </div>
      <div class="arx-ray-items">
        <span><i style="background:%s;"></i>Contextual continuity</span>
        <span><i style="background:%s;"></i>Enterprise awareness</span>
        <span><i style="background:%s;"></i>Coordinated action</span>
      </div>
    </div>""" % ((952 - VB_Y0) / VB_VIS * 100, 1090 / VB_W * 100, GOLD, ORANGE, "#B8860B")

    fb = """<div class="arx-fallback">
      <div class="arxf arxf-h"><div class="k">Commercial intelligence</div><div class="n">HORIZON</div>
        <ul><li>Market and account intelligence</li><li>Revenue coordination</li><li>GTM execution</li></ul></div>
      <div class="arxf arxf-c"><div class="k">Governed context</div><div class="n">CORE</div>
        <ul><li>Governance and permissions</li><li>Organizational memory and logs</li>
        <li>Decision continuity</li></ul></div>
      <div class="arxf arxf-p"><div class="k">Operational execution</div><div class="n">PULSE</div>
        <ul><li>Operational workflows</li><li>Supply and resource coordination</li>
        <li>Performance management</li></ul></div>
      <div class="arxf arxf-r"><div class="k">Persistent enterprise companion</div><div class="n">RAY</div>
        <ul><li>Contextual continuity</li><li>Enterprise awareness</li><li>Coordinated action</li></ul></div>
    </div>"""

    tail = ('<div style="margin-top:30px;">%s</div>' % explore_btn) if explore_btn else ""
    return """<section class="%s">
  <div class="container">
    <div class="section-tag">%s</div>
    <h2 class="section-heading">%s</h2>
    <p class="section-sub">%s</p>
    <div class="arx">%s%s%s%s%s%s</div>
    %s
    <div class="arx-foot">%s</div>
    %s
  </div>
</section>
""" % (band, tag, heading, sub, "".join(s), horizon, core, pulse, orbits, ray, fb, foot, tail)
