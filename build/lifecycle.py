# -*- coding: utf-8 -*-
"""The industry lifecycle band.

Replaces the two-circle eclipse diagram on the three industry pages. That one
hung every operating area off a thin leader line, which broke whenever an area
was added or removed, and it hid the lifecycle stages inside SVG <title>
tooltips where nobody saw them.

This uses the language of the home page architecture strip instead: the areas
as clean numbered blocks, then one dark governed band underneath carrying the
stages as visible text.
"""

TONES = ["#E0641E", "#CC9900", "#C45213", "#B07E00", "#D9822B", "#8C6500"]

CSS = r"""
  /* INDUSTRY LIFECYCLE BAND */
  .lcy{margin-top:30px;}
  .lcy-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;}
  .lcy-card{position:relative;background:#fff;border:1px solid var(--border-soft);
    border-radius:16px;padding:22px 22px 24px;box-shadow:var(--shadow);overflow:hidden;}
  .lcy-card::before{content:"";position:absolute;inset:0 0 auto;height:4px;background:var(--lc);}
  .lcy-num{display:inline-flex;align-items:center;justify-content:center;width:30px;height:30px;
    border-radius:9px;background:var(--lc);color:#fff;font-size:13px;font-weight:800;
    letter-spacing:.02em;}
  .lcy-t{margin-top:14px;font-size:17.5px;font-weight:800;line-height:1.3;color:var(--navy);}
  .lcy-flow{margin-top:16px;border-radius:18px;padding:24px 26px 26px;
    background:linear-gradient(140deg,#2E2822,#141110);color:#F6EEDE;}
  .lcy-flow-k{font-size:11px;font-weight:800;letter-spacing:.22em;text-transform:uppercase;
    color:#E0B33A;}
  .lcy-flow-v{margin-top:6px;font-size:19px;font-weight:800;color:#fff;}
  .lcy-steps{margin-top:18px;display:flex;flex-wrap:wrap;align-items:center;gap:8px 0;}
  .lcy-step{font-size:13.5px;font-weight:700;color:#F6EEDE;white-space:nowrap;}
  .lcy-sep{width:26px;height:1px;background:rgba(224,178,80,.5);margin:0 10px;flex:none;}

  /* option: gradient blocks in place of white cards */
  .lcy-grid.g .lcy-card{background:var(--lcg);border-color:transparent;box-shadow:0 14px 34px rgba(90,60,10,.16);}
  .lcy-grid.g .lcy-card::before{display:none;}
  .lcy-grid.g .lcy-num{background:rgba(40,28,10,.30);}
  .lcy-grid.g .lcy-t{color:#2A231B;}

  /* option: the two-circle mark kept beside the heading */
  .lcy-mark{display:flex;align-items:center;gap:14px;}
  .lcy-mark svg{flex:none;width:52px;height:38px;}

  /* option: the stages as a numbered track */
  .lcy-track{margin-top:20px;display:grid;grid-template-columns:repeat(10,1fr);gap:0;position:relative;}
  .lcy-track::before{content:"";position:absolute;left:5%;right:5%;top:13px;height:1px;
    background:rgba(224,178,80,.45);}
  .lcy-tstep{position:relative;text-align:center;}
  .lcy-tnum{width:26px;height:26px;margin:0 auto;border-radius:50%;background:#2E2822;
    border:1px solid rgba(224,178,80,.55);color:#E0B33A;font-size:11px;font-weight:800;
    display:flex;align-items:center;justify-content:center;}
  .lcy-tlab{margin-top:9px;font-size:11.5px;font-weight:700;color:#F6EEDE;line-height:1.25;}

  @media(max-width:900px){
    .lcy-track{grid-template-columns:repeat(2,1fr);gap:14px 10px;}
    .lcy-track::before{display:none;}
    .lcy-grid{grid-template-columns:1fr;}
    .lcy-steps{display:grid;grid-template-columns:repeat(2,1fr);gap:10px 14px;}
    .lcy-sep{display:none;}
  }
"""


MARK = ('<svg viewBox="0 0 104 76" aria-hidden="true">'
        '<circle cx="40" cy="38" r="30" fill="#CC9900" opacity=".85"/>'
        '<circle cx="64" cy="38" r="30" fill="#E0641E" opacity=".85"/>'
        '<path d="M52 9.5 A30 30 0 0 1 52 66.5 A30 30 0 0 1 52 9.5 Z" fill="#FFF6DC" opacity=".92"/>'
        '</svg>')


def _grad(tone):
    return "linear-gradient(140deg,%s22,%s)" % (tone, tone)


def section(tag, heading, lede, areas, stages, flow_k, flow_v, band="band-alt",
            cards_style="plain", mark=False, steps_style="text"):
    grad = cards_style == "gradient"
    cards = "".join(
        '<div class="lcy-card" style="--lc:%s;--lcg:%s;"><div class="lcy-num">%02d</div>'
        '<div class="lcy-t">%s</div></div>'
        % (TONES[i % len(TONES)], _grad(TONES[i % len(TONES)]), i + 1, a)
        for i, a in enumerate(areas))
    if steps_style == "track":
        steps = ('<div class="lcy-track">' + "".join(
            '<div class="lcy-tstep"><div class="lcy-tnum">%d</div>'
            '<div class="lcy-tlab">%s</div></div>' % (i + 1, s)
            for i, s in enumerate(stages)) + "</div>")
    else:
        steps = ('<div class="lcy-steps">' + '<span class="lcy-sep"></span>'.join(
            '<span class="lcy-step">%s</span>' % s for s in stages) + "</div>")
    return """<section class="%s">
  <div class="container">
    <div class="section-tag">%s</div>
    %s
    <p class="lede">%s</p>
    <div class="lcy">
      <div class="lcy-grid%s">%s</div>
      <div class="lcy-flow">
        <div class="lcy-flow-k">%s</div>
        <div class="lcy-flow-v">%s</div>
        %s
      </div>
    </div>
  </div>
</section>
""" % (band, tag,
       ('<div class="lcy-mark">%s<h2 class="section-heading" style="margin:0;">%s</h2></div>'
        % (MARK, heading)) if mark else ('<h2 class="section-heading">%s</h2>' % heading),
       lede, " g" if grad else "", cards, flow_k, flow_v, steps)
