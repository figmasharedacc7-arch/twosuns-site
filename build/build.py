# -*- coding: utf-8 -*-
"""Render the TwoSuns 7 page site from the master copy."""
import os, sys, html, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import theme
from theme import head, chrome_nav, TAIL
import herorot
from content import HOME, PLATFORM, CAPABILITIES, HORIZON_GROUPS, PULSE_GROUPS
from content2 import (BUILT, USECASES, UC_THEMES, UC_ITEMS, COMPANY, DISCUSS,
                      UC_AREA_LABELS, UC_GROUP_LABELS, UC_TAGS, CAP_LINKS)
import eclipse
import arch

OUT = "/Users/mohammaddidarulalam/Documents/Claude/twosuns-live/preview"
ACCENTS = ["var(--a1)", "var(--a2)", "var(--a3)", "var(--a4)", "var(--a5)", "var(--a6)"]


def e(s):
    return html.escape(s, quote=False)


def ask(label):
    """Every invitation leads to the same short form, carrying its own label."""
    return "discuss.html?ask=" + urllib.parse.quote_plus(label)


def btn(label, href=None, ghost=False):
    url = href if href else ask(label)
    cls = "btn-ghost" if ghost else "btn-cta"
    return '<a class="%s" href="%s">%s</a>' % (cls, url, e(label))


def hero(d, tall=False, wide=False):
    cls = "hero" + (" tall" if tall else "") + (" wide" if wide else "")
    return """<section class="%s">
  <div class="hero-glow"></div>
  <div class="container">
    <div class="hero-eyebrow"><span class="dot"></span>%s</div>
    <h1>%s</h1>
    <p class="hero-sub">%s</p>
    <div class="hero-actions">%s</div>
  </div>
</section>
<div class="sun-divider"></div>
""" % (cls, e(d["eyebrow"]), e(d["h1"]), e(d["sub"]), "%s")


def vid_band(video, heading, para, primary, secondary, sec_href=None):
    """Closing band with a muted looping video behind it, as on the cement microsite."""
    return """<section class="vidband %s" style="padding:96px 0;">
  <video autoplay muted loop playsinline preload="metadata" poster="%s-poster.jpg" aria-hidden="true">
    <source src="%s.mp4" type="video/mp4">
  </video>
  <div class="container">
    <h2>%s</h2>
    <p>%s</p>
    <div class="cta-actions">%s %s</div>
  </div>
</section>
""" % (video, video, video, e(heading), e(para), btn(primary), btn(secondary, sec_href, ghost=True))


def cta_band(heading, para, primary, secondary, sec_href=None):
    return """<section class="cta-band">
  <div class="container">
    <h2>%s</h2>
    <p>%s</p>
    <div class="cta-actions">%s %s</div>
  </div>
</section>
""" % (e(heading), e(para), btn(primary), btn(secondary, sec_href, ghost=True))


def slug(title):
    """Stable anchor for a use case, so capability groups can link straight to it."""
    s = "".join(c.lower() if c.isalnum() else "-" for c in title)
    while "--" in s:
        s = s.replace("--", "-")
    return "uc-" + s.strip("-")


def arch3(horizon, core, pulse, ray, notes=None):
    """Horizon and Pulse flanking Core, Ray spanning beneath."""
    n = notes or {}
    def note(k):
        return ('<div class="a3-note">%s</div>' % e(n[k])) if k in n else ""
    return """<div class="arch3">
  <div class="arch3-band">
    <div class="a3 a3-h">
      <div class="a3-name" style="color:#B07E00;">Horizon</div>
      <p>%s</p>%s
    </div>
    <div class="a3 a3-core">
      <div class="a3-name" style="color:#E0641E;">Core</div>
      <p>%s</p>%s
    </div>
    <div class="a3 a3-p">
      <div class="a3-name" style="color:#C45213;">Pulse</div>
      <p>%s</p>%s
    </div>
  </div>
  <div class="a3-ray">
    <div class="a3-name" style="color:#E0641E;">Ray</div>
    <p>%s</p>
  </div>
</div>
""" % (e(horizon), note("horizon"), e(core), note("core"), e(pulse), note("pulse"), e(ray))


def ticks(items):
    return '<ul class="tick">' + "".join("<li>%s</li>" % e(i) for i in items) + "</ul>"


REQUIRED_CSS = [
    ".ecl{", ".ecl-lab", ".ecl-fallback",          # lifecycle diagram
    ".imgsec{", ".imgsec-r::after", ".vidband",     # photo and video sections
    ".arch3-band", ".a3-core::before",              # architecture
    ".hero-vid", ".hero-vid video.on", ".uc-frow", ".acc-rel",   # hero, filters, cross links
    ".split2", ".steps", ".uc-grid",
]


# the hero cycles through these, first one eager, the rest deferred by herorot
HERO_CLIPS = [
    ("hero-build.mp4", "hero-build-poster.jpg"),
    ("hero-crane.mp4", "hero-crane-poster.jpg"),
    ("hero-rise.mp4", "hero-rise-poster.jpg"),
]


def check_css(page, name):
    missing = [k for k in REQUIRED_CSS if k not in page]
    if missing:
        raise SystemExit("STYLESHEET INCOMPLETE in %s, missing: %s" % (name, ", ".join(missing)))


def write(name, body):
    path = os.path.join(OUT, name)
    with open(path, "w") as f:
        f.write(body)
    return path


# ================================================================ HOME
def build_home():
    d = HOME
    s = head(d["title"], d["desc"]) + chrome_nav("index.html")

    s += """<section class="hero tall has-vid">
  <div class="hero-vid">
    """ + herorot.markup(HERO_CLIPS) + """
  </div>
  <div class="hero-glow"></div>
  <div class="container">
    <div class="hero-eyebrow"><span class="dot"></span>%s</div>
    <h1>%s</h1>
    <p class="hero-sub">%s</p>
    <div class="hero-actions">%s</div>
  </div>
</section>
<div class="sun-divider"></div>
""" % (e(d["eyebrow"]), e(d["h1"]), e(d["sub"]),
       btn(d["primary"][0]) + btn(d["secondary"][0], d["secondary"][1], ghost=True))

    s += """<section style="padding:88px 0 78px;">
  <div class="container">
    <div class="section-tag">The shift</div>
    <h2 class="section-heading">%s</h2>
    <div class="stmt">%s</div>
  </div>
</section>
""" % (e(d["evolving_h"]), "".join("<p>%s</p>" % e(p) for p in d["evolving"]))

    s += arch.section(
        "Enterprise context becomes coordinated action",
        "Commercial intelligence and operational execution, connected through one governed enterprise context.",
        btn("Explore the Platform", "platform.html", ghost=True))

    areas = ""
    for i, a in enumerate(d["industry_areas"]):
        areas += """<div class="card">
      <span class="card-num" style="background:%s;">%d</span>
      <h3>%s</h3>
    </div>""" % (ACCENTS[i], i + 1, e(a))

    s += """<section class="imgsec imgsec-r img-construction">
  <div class="container">
   <div class="sec-split">
    <div class="section-tag">Built industry</div>
    <h2 class="section-heading">%s</h2>
    <p class="section-sub">%s</p>
    <div class="grid3">%s</div>
    <div style="margin-top:30px;">%s</div>
   </div>
  </div>
</section>
""" % (e(d["industry_h"]), e(d["industry_sub"]), areas,
       btn("Explore the Built Industry", "built-industry.html", ghost=True))

    work = ""
    for i, (h, p) in enumerate(d["work"]):
        work += """<div class="card">
      <span class="card-num" style="background:%s;">%d</span>
      <h3>%s</h3><p>%s</p>
    </div>""" % (ACCENTS[i], i + 1, e(h), e(p))

    s += """<section class="imgsec imgsec-l imgsec-work area-sec">
  <video autoplay muted loop playsinline preload="metadata" poster="vid-work-poster.jpg" aria-hidden="true">
    <source src="vid-work.mp4" type="video/mp4">
  </video>
  <div class="container">
   <div class="sec-split">
    <div class="section-tag">Where to start</div>
    <h2 class="section-heading">%s</h2>
    <div class="grid3">%s</div>
    <div style="margin-top:30px;">%s</div>
   </div>
  </div>
</section>
""" % (e(d["work_h"]), work, btn("Explore Use Cases", "use-cases.html", ghost=True))

    s += vid_band("vid-aerial", d["close_h"], d["close_p"], d["close_primary"], d["close_secondary"])
    return s + herorot.SCRIPT + TAIL


# ================================================================ PLATFORM
def build_platform():
    d = PLATFORM
    s = head(d["title"], d["desc"]) + chrome_nav("platform.html")
    s += (hero(d, wide=True).replace('<section class="hero wide"',
                                     '<section class="hero wide hero-photo wall-platform"')
          % (btn(d["primary"]) + btn(d["secondary"], ghost=True)))

    s += """<section>
  <div class="container">
    <div class="section-tag">Core</div>
    <h2 class="section-heading">%s</h2>
    %s
    <div class="layer">%s</div>
  </div>
</section>
""" % (e(d["core_h"]), "".join('<p class="lede">%s</p>' % e(p) for p in d["core_p"]),
       ticks(d["core_bullets"]))

    s += """<section class="band-alt">
  <div class="container">
    <div class="section-tag">Ray</div>
    <h2 class="section-heading">%s</h2>
    <p class="lede">%s</p>
    <div class="layer">%s</div>
  </div>
</section>
""" % (e(d["ray_h"]), e(d["ray_p"]), ticks(d["ray_bullets"]))

    s += """<section>
  <div class="container">
    <div class="section-tag">Capability families</div>
    <div class="grid2" style="margin-top:0;">
      <div class="layer" style="margin-top:0;">
        <div class="layer-head"><span class="layer-chip" style="background:var(--a1);">Horizon</span></div>
        <h3 class="sub-heading">%s</h3>
        <p>%s</p>
        <div style="margin-top:20px;">%s</div>
      </div>
      <div class="layer" style="margin-top:0;">
        <div class="layer-head"><span class="layer-chip" style="background:var(--a4);">Pulse</span></div>
        <h3 class="sub-heading">%s</h3>
        <p>%s</p>
        <div style="margin-top:20px;">%s</div>
      </div>
    </div>
  </div>
</section>
""" % (e(d["horizon_h"]), e(d["horizon_p"]),
       btn("Explore Horizon Capabilities", "capabilities.html#horizon", ghost=True),
       e(d["pulse_h"]), e(d["pulse_p"]),
       btn("Explore Pulse Capabilities", "capabilities.html#pulse", ghost=True))

    s += """<section class="band-warm">
  <div class="container">
    <div class="section-tag">Continuity</div>
    <h2 class="section-heading">%s</h2>
    <p class="lede">%s</p>
    %s
  </div>
</section>
""" % (e(d["circ_h"]), e(d["circ_p"]),
       arch3("Market-facing work drawing on the shared context.",
             "Inputs enter here. Activities and results return here as continuing context.",
             "Delivery and operating work drawing on the same context.",
             "Context-aware support spanning the full environment."))

    s += """<section class="imgsec imgsec-l img-operations">
  <div class="container">
   <div class="sec-split">
    <div class="section-tag">Inputs</div>
    <h2 class="section-heading">%s</h2>
    <p class="section-sub">%s</p>
    <div class="grid2">%s</div>
   </div>
  </div>
</section>
""" % (e(d["inputs_h"]), e(d["inputs_p"]),
       "".join('<div class="card"><p style="font-size:15.5px;color:var(--navy);font-weight:600;">%s</p></div>' % e(i)
               for i in d["inputs"]))

    s += """<section class="imgsec imgsec-r bg-integration area-sec">
  <div class="container">
   <div class="sec-split">
    <div class="section-tag">Integration</div>
    <h2 class="section-heading">%s</h2>
    %s
   </div>
  </div>
</section>
""" % (e(d["connect_h"]), "".join('<p class="lede">%s</p>' % e(p) for p in d["connect_p"]))

    s += """<section class="imgsec imgsec-r bg-deploy area-sec">
  <div class="container">
   <div class="sec-split">
    <div class="section-tag">Deployment</div>
    <h2 class="section-heading">%s</h2>
    <p class="lede">%s</p>
    <div class="steps">%s</div>
    <div class="callout"><h3>%s</h3><p>%s</p></div>
   </div>
  </div>
</section>
""" % (e(d["deploy_h"]), e(d["deploy_p"]),
       "".join('<div class="step">%s</div>' % e(x) for x in d["deploy_steps"]),
       e(d["packs_h"]), e(d["packs_p"]))

    s += """<section class="imgsec imgsec-r img-industrial">
  <div class="container">
   <div class="sec-split">
    <div class="section-tag">Governance</div>
    <h2 class="section-heading">%s</h2>
    %s
   </div>
  </div>
</section>
""" % (e(d["gov_h"]), "".join('<p class="lede">%s</p>' % e(p) for p in d["gov_p"]))

    s += vid_band("vid-port", "See the platform in your context",
                  "We can walk through the environment, the configured workflows and the deployment path that fits "
                  "your organization.", d["close_primary"], d["close_secondary"])
    return s + TAIL


# ================================================================ CAPABILITIES
def acc_group(groups, base_accent):
    out = ""
    for i, (name, desc, bullets) in enumerate(groups):
        col = ACCENTS[(base_accent + i) % len(ACCENTS)]
        rel = ""
        if name in CAP_LINKS:
            items = "".join(
                '<li><a href="use-cases.html#%s">%s</a></li>' % (slug(t), e(t))
                for t in CAP_LINKS[name])
            rel = ('<div class="acc-rel"><div class="k">Related use cases</div>'
                   '<ul>%s</ul></div>') % items
        out += """<details class="acc">
  <summary>
    <span class="acc-bar" style="background:%s;"></span>
    <span><span class="acc-title">%s</span><span class="acc-desc">%s</span></span>
  </summary>
  <div class="acc-body">%s%s</div>
</details>
""" % (col, e(name), e(desc), ticks(bullets), rel)
    return out

def build_capabilities():
    d = CAPABILITIES
    s = head(d["title"], d["desc"]) + chrome_nav("capabilities.html")
    s += (hero(d, wide=True).replace('<section class="hero wide"',
                                     '<section class="hero wide hero-photo wall-capabilities"')
          % (btn(d["primary"]) + btn(d["secondary"][0], d["secondary"][1], ghost=True)))

    s += """<section id="horizon" class="imgsec imgsec-r bg-horizon area-sec fam-band">
  <div class="container">
   <div class="sec-split">
    <div class="section-tag">Capability family</div>
    <h2 class="section-heading">Horizon</h2>
    <p class="section-sub">%s</p>
   </div>
  </div>
</section>
<section style="padding:44px 0 88px;">
  <div class="container">%s</div>
</section>
""" % (e(d["horizon_sub"]), acc_group(HORIZON_GROUPS, 0))

    s += """<section id="pulse" class="imgsec imgsec-l bg-pulse area-sec fam-band">
  <div class="container">
   <div class="sec-split">
    <div class="section-tag">Capability family</div>
    <h2 class="section-heading">Pulse</h2>
    <p class="section-sub">%s</p>
   </div>
  </div>
</section>
<section class="band-alt" style="padding:44px 0 88px;">
  <div class="container">%s</div>
</section>
""" % (e(d["pulse_sub"]), acc_group(PULSE_GROUPS, 3))

    s += """<section class="band-warm">
  <div class="container">
    <div class="section-tag">Adaptable</div>
    <h2 class="section-heading">%s</h2>
    <p class="lede">%s</p>
  </div>
</section>
""" % (e(d["adapt_h"]), e(d["adapt_p"]))

    s += cta_band("Configure the capabilities around your workflow",
                  "Tell us the workflow, the operating environment and the outcome you need, and we will map the "
                  "capabilities that apply.",
                  d["close_primary"], d["close_secondary"], "use-cases.html")
    return s + TAIL


# ================================================================ BUILT INDUSTRY
def build_built():
    d = BUILT
    s = head(d["title"], d["desc"]) + chrome_nav("built-industry.html")
    s += (hero(d, wide=True).replace('<section class="hero wide"', '<section class="hero wide hero-photo wall-construction"')
          % (btn(d["primary"][0], d["primary"][1]) + btn(d["secondary"], ghost=True)))

    # six alternating full bleed sections, each photo pre cropped so its subject
    # sits on the side the copy leaves visible
    SLOTS = [("materials", "l"), ("distribution", "r"), ("owners", "l"),
             ("construction", "r"), ("operations", "l"), ("institutions", "r")]
    NO_PHOTO = set()

    s += """<section style="padding:88px 0 40px;">
  <div class="container">
    <div class="section-tag">Operating areas</div>
    <h2 class="section-heading">%s</h2>
  </div>
</section>
""" % e(d["areas_h"])

    for i, (name, desc, bullets) in enumerate(d["areas"]):
        slot, side = SLOTS[i]
        if slot in NO_PHOTO:
            s += """<section class="band-warm area-sec" style="min-height:0;padding:84px 0;">
  <div class="container">
   <div class="split2">
    <div>
     <span class="card-num" style="background:%s;">%d</span>
     <h2 class="section-heading">%s</h2>
     <p class="section-sub">%s</p>
    </div>
    <div class="split2-panel">
     <h4>What it covers</h4>
     %s
    </div>
   </div>
  </div>
</section>
""" % (ACCENTS[i], i + 1, e(name), e(desc), ticks(bullets))
            continue
        s += """<section class="imgsec imgsec-%s bg-%s area-sec">
  <div class="container">
   <div class="sec-split">
    <span class="card-num" style="background:%s;">%d</span>
    <h2 class="section-heading">%s</h2>
    <p class="section-sub">%s</p>
    %s
   </div>
  </div>
</section>
""" % (side, slot, ACCENTS[i], i + 1, e(name), e(desc), ticks(bullets))

    s += eclipse.section(e(d["life_h"]), e(d["life_p"]), d["life_stages"],
                         [a[0] for a in d["areas"]])

    s += """<section>
  <div class="container">
    <div class="section-tag">Shared conditions</div>
    <h2 class="section-heading">%s</h2>
    <div class="grid2">%s</div>
  </div>
</section>
""" % (e(d["cond_h"]),
       "".join('<div class="card"><p style="font-size:15.5px;color:var(--navy);font-weight:600;">%s</p></div>' % e(c)
               for c in d["cond"]))

    s += """<section class="band-warm">
  <div class="container">
    <div class="section-tag">Connected work</div>
    <h2 class="section-heading">%s</h2>
    <p class="lede">%s</p>
  </div>
</section>
""" % (e(d["flow_h"]), e(d["flow_p"]))

    s += cta_band("Start from your part of the industry",
                  "Tell us where your organization sits across the built industry and the workflow you want to "
                  "advance.", d["close_primary"], d["close_secondary"], "use-cases.html")
    return s + TAIL


# ================================================================ USE CASES
def build_usecases():
    d = USECASES
    s = head(d["title"], d["desc"]) + chrome_nav("use-cases.html")
    s += (hero(d, wide=True).replace('<section class="hero wide"',
                                     '<section class="hero wide hero-photo wall-usecases"')
          % (btn(d["primary"]) + btn(d["secondary"], ghost=True)))

    def frow(label, dim, opts, prefix):
        btns = '<button class="uc-filter on" data-dim="%s" data-f="all">All</button>' % dim
        for i, t in enumerate(opts):
            btns += ('<button class="uc-filter" data-dim="%s" data-f="%s%d">%s</button>'
                     % (dim, prefix, i, e(t)))
        return ('<div class="uc-frow"><div class="lab">%s</div>'
                '<div class="uc-filters" style="margin-top:0;">%s</div></div>') % (e(label), btns)

    filters = (frow("Objective", "theme", UC_THEMES, "t")
               + frow("Industry area", "area", UC_AREA_LABELS, "a")
               + frow("User group", "group", UC_GROUP_LABELS, "g")
               + frow("Platform", "lens", ["Horizon", "Pulse", "Core", "Ray"], "l"))

    LENSES = ["Horizon", "Pulse", "Core", "Ray"]
    cards = ""
    for (ti, title, users, inputs, wf, out, lens) in UC_ITEMS:
        areas, groups = UC_TAGS[title]
        tags = ["t%d" % ti]
        tags += ["a%d" % a for a in areas]
        tags += ["g%d" % g for g in groups]
        tags += ["l%s" % L for L in LENSES if L in lens]
        chips = "".join('<span class="uc-tag">%s</span>' % e(UC_AREA_LABELS[a]) for a in areas[:2])
        chips += "".join('<span class="uc-tag">%s</span>' % e(UC_GROUP_LABELS[g]) for g in groups[:1])
        cards += """<article class="uc" id="%s" data-tags="%s">
  <h3>%s</h3>
  <dl>
    <dt>Typical users</dt><dd>%s</dd>
    <dt>Inputs</dt><dd>%s</dd>
    <dt>Configured workflow</dt><dd>%s</dd>
    <dt>Outputs and value</dt><dd>%s</dd>
  </dl>
  <span class="uc-lens">%s</span>
  <div class="uc-tags">%s</div>
</article>
""" % (slug(title), " ".join(tags), e(title), e(users), e(inputs), e(wf), e(out), e(lens), chips)

    s += """<section>
  <div class="container">
    <div class="section-tag">Filter</div>
    <h2 class="section-heading">Representative workflows</h2>
    <p class="section-sub">Filter by objective, by where you sit in the built industry, by who does
      the work, or by the part of the platform involved. Filters combine.</p>
    <div class="uc-filterset">%s</div>
    <button class="uc-clear" id="ucclear" hidden type="button">Clear all filters</button>
    <div class="uc-grid" id="ucgrid">%s<div class="uc-ask" id="ucask">
      <div class="lab">Not listed here</div>
      <h3>Your workflow probably looks a little different</h3>
      <p>These are representative, not exhaustive. Describe the work you are trying to
        advance and we will show you how it would be configured.</p>
      %s
    </div></div>
    <p class="form-note" id="uccount"></p>
  </div>
</section>
""" % (filters, cards, btn("Describe Your Workflow", ghost=True))

    s += """<section class="band-warm">
  <div class="container">
    <div class="section-tag">Your workflow</div>
    <h2 class="section-heading">%s</h2>
    %s
  </div>
</section>
""" % (e(d["close_h"]), "".join('<p class="lede">%s</p>' % e(p) for p in d["close_p"]))

    s += cta_band("Configure TwoSuns around the work you need to advance",
                  "Start from a use case described here or bring us a workflow of your own.",
                  d["close_primary"], d["close_secondary"])

    s += """<script>
(function(){
  var grid=document.getElementById('ucgrid'),
      cards=[].slice.call(grid.querySelectorAll('.uc')),
      cnt=document.getElementById('uccount'),
      clear=document.getElementById('ucclear'),
      btns=[].slice.call(document.querySelectorAll('.uc-filter')),
      picked={theme:'all',area:'all',group:'all',lens:'all'};

  function apply(){
    var wanted=[];
    for(var k in picked){ if(picked[k]!=='all') wanted.push(picked[k]); }
    var shown=0;
    cards.forEach(function(c){
      var tags=' '+c.getAttribute('data-tags')+' ', ok=true;
      wanted.forEach(function(w){ if(tags.indexOf(' '+w+' ')<0) ok=false; });
      c.style.display = ok ? '' : 'none';
      if(ok) shown++;
    });
    cnt.textContent = shown===cards.length
      ? 'Showing all ' + cards.length + ' use cases.'
      : 'Showing ' + shown + ' of ' + cards.length + ' use cases.';
    clear.hidden = !wanted.length;
    var askc = document.getElementById('ucask');
    if(askc) askc.classList.toggle('wide', shown % 2 === 0);
  }

  btns.forEach(function(b){
    b.addEventListener('click',function(){
      var dim=b.getAttribute('data-dim');
      picked[dim]=b.getAttribute('data-f');
      btns.forEach(function(o){
        if(o.getAttribute('data-dim')===dim) o.classList.toggle('on', o===b);
      });
      apply();
    });
  });

  clear.addEventListener('click',function(){
    for(var k in picked) picked[k]='all';
    btns.forEach(function(o){ o.classList.toggle('on', o.getAttribute('data-f')==='all'); });
    apply();
  });

  apply();

  // arriving from a capability group: reveal that card whatever the filters say
  function jump(){
    var id=location.hash.slice(1); if(!id) return;
    var el=document.getElementById(id); if(!el) return;
    for(var k in picked) picked[k]='all';
    btns.forEach(function(o){ o.classList.toggle('on', o.getAttribute('data-f')==='all'); });
    apply();
    el.classList.add('flash');
    setTimeout(function(){ el.scrollIntoView({block:'center',behavior:'smooth'}); }, 60);
    setTimeout(function(){ el.classList.remove('flash'); }, 2600);
  }
  jump();
  window.addEventListener('hashchange', jump);
})();
</script>
"""
    return s + TAIL


# ================================================================ COMPANY
def build_company():
    d = COMPANY
    s = head(d["title"], d["desc"]) + chrome_nav("company.html")
    s += (hero(d, wide=True).replace('<section class="hero wide"',
                                     '<section class="hero wide hero-photo wall-company"')
          % btn(d["primary"]))

    s += """<section>
  <div class="container">
    <div class="section-tag">Purpose</div>
    <h2 class="section-heading">%s</h2>
    %s
  </div>
</section>
""" % (e(d["purpose_h"]), "".join('<p class="lede">%s</p>' % e(p) for p in d["purpose"]))

    alt = False
    for gname, is_lead, people in d["groups"]:
        cards = ""
        for (nm, role, bio) in people:
            cards += """<div class="person%s">
      <div class="nm">%s</div>
      <div class="rl">%s</div>
      <p>%s</p>
    </div>""" % (" lead" if is_lead else "", e(nm), e(role), e(bio))
        s += """<section%s>
  <div class="container">
    <div class="section-tag">%s</div>
    <h2 class="section-heading">%s</h2>
    <div class="people">%s</div>
  </div>
</section>
""" % (' class="band-alt"' if alt else "", e(gname), e(gname), cards)
        alt = not alt

    s += """<section class="band-warm">
  <div class="container">
    <div class="section-tag">Endorsement</div>
    <h2 class="section-heading">%s</h2>
    <p class="lede">%s</p>
  </div>
</section>
""" % (e(d["aepg_h"]), e(d["aepg_p"]))

    s += cta_band("Work with the team behind the platform",
                  "Tell us what you are trying to advance and we will bring the right people into the conversation.",
                  d["close_primary"], "Explore the Platform", "platform.html")
    return s + TAIL


# ================================================================ DISCUSS
def build_discuss():
    d = DISCUSS
    opts = "".join('<option value="%s">%s</option>' % (e(a), e(a)) for a in d["areas"])

    s = head(d["title"], d["desc"]) + chrome_nav("discuss.html")
    s += """<section class="hero">
  <div class="hero-glow"></div>
  <div class="container">
    <div class="hero-eyebrow"><span class="dot"></span>%s</div>
    <h1 style="max-width:20ch;">%s</h1>
    <p class="hero-sub">%s</p>
  </div>
</section>
<div class="sun-divider"></div>
""" % (e(d["eyebrow"]), e(d["h1"]), e(d["sub"]))

    s += """<section>
  <div class="container">
    <div class="form-card" id="formwrap">
      <div class="ctx-chip" id="ctxchip"></div>
      <form id="discussForm" novalidate>
        <label for="f_name">Name</label>
        <input id="f_name" name="name" type="text" required autocomplete="name">

        <label for="f_org">Organization</label>
        <input id="f_org" name="company" type="text" required autocomplete="organization">

        <label for="f_role">Role <span class="opt">(optional)</span></label>
        <input id="f_role" name="job_title" type="text" autocomplete="organization-title">

        <label for="f_email">Email</label>
        <input id="f_email" name="email" type="email" required autocomplete="email">

        <label for="f_area">Area of interest <span class="opt">(optional)</span></label>
        <select id="f_area" name="area">
          <option value="">Select an area</option>
          %s
        </select>

        <label for="f_msg">Tell us about the pain point, opportunity or workflow you want to address.</label>
        <textarea id="f_msg" name="message" required></textarea>

        <label for="f_file">Attachment <span class="opt">(optional, up to 4 MB)</span></label>
        <input id="f_file" name="attachment" type="file">

        <button type="submit" id="f_submit">Discuss Your Needs</button>
        <p class="form-note" id="f_note">We will review the context before following up. Your details are used only
          for this conversation.</p>
      </form>
    </div>
    <div class="form-ok" id="formok" style="max-width:720px;">
      <h3>%s</h3>
      <p>%s</p>
    </div>
  </div>
</section>
""" % (opts, e(d["confirm_h"]), e(d["confirm_p"]))

    s += """<section class="band-alt">
  <div class="container">
    <div class="section-tag">Supporting material</div>
    <h2 class="section-heading">%s</h2>
    <p class="section-sub">%s</p>
    <div class="layer">%s</div>
  </div>
</section>
""" % (e(d["support_h"]), e(d["support_p"]), ticks(d["support"]))

    s += """<script>
(function(){
  var ENDPOINT="https://script.google.com/macros/s/AKfycbyz4qCsmkMasAHUe8ZZqTva4VvVGo-Q3vy3K_sTMIJY4Q3Mhnq_1HMg_-Z4DF_CUu9z/exec";
  var MAILFALLBACK="https://formsubmit.co/ajax/info@twosuns.ai";

  function param(k){
    var m=new RegExp('[?&]'+k+'=([^&]*)').exec(location.search);
    return m ? decodeURIComponent(m[1].replace(/\\+/g,' ')) : '';
  }
  // Retain the originating page and the selected invitation as hidden form context.
  var invitation = param('ask') || 'Discuss Your Needs';
  var origin = param('from') || document.referrer || '';
  var chip=document.getElementById('ctxchip');
  if(param('ask')){ chip.textContent='\\u2600 '+invitation; chip.style.display='inline-flex'; }

  var form=document.getElementById('discussForm'),
      btn=document.getElementById('f_submit'),
      note=document.getElementById('f_note'),
      wrap=document.getElementById('formwrap'),
      ok=document.getElementById('formok');

  form.addEventListener('submit', function(ev){
    ev.preventDefault();
    var E=form.elements;
    var name=E['name'].value.trim(), org=E['company'].value.trim(),
        email=E['email'].value.trim(), msg=E['message'].value.trim();
    if(!name||!org||!email||!msg){ note.textContent='Please complete name, organization, email and your message.'; return; }
    btn.disabled=true; btn.textContent='Sending...';

    var file=document.getElementById('f_file').files[0];
    if(file && file.size>4*1024*1024){
      note.textContent='That attachment is larger than 4 MB. Please send it to info@twosuns.ai after submitting.';
      btn.disabled=false; btn.textContent='Discuss Your Needs'; return;
    }

    function send(attachName, attachData){
      var area=E['area'].value;
      var body={
        form:'Discuss Your Needs',
        campaign:invitation,
        name:name, email:email, company:org,
        job_title:E['job_title'].value.trim(),
        message:(area?('Area of interest: '+area+'\\n\\n'):'')+msg+(attachName?('\\n\\nAttachment: '+attachName):''),
        page:origin||location.href
      };
      if(attachName){ body.attachment_name=attachName; body.attachment_b64=attachData; }
      var enc=Object.keys(body).map(function(k){return encodeURIComponent(k)+'='+encodeURIComponent(body[k]);}).join('&');

      fetch(ENDPOINT,{method:'POST',mode:'no-cors',
        headers:{'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8'},body:enc}).catch(function(){});

      fetch(MAILFALLBACK,{method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify({_subject:'TwoSuns enquiry: '+invitation,
          Name:name,Organization:org,Role:body.job_title,Email:email,
          Invitation:invitation,Page:body.page,Message:body.message})}).catch(function(){});

      setTimeout(function(){ wrap.style.display='none'; ok.style.display='block';
        window.scrollTo({top:ok.offsetTop-120,behavior:'smooth'}); }, 700);
    }

    if(file){
      var r=new FileReader();
      r.onload=function(){ send(file.name, String(r.result).split(',')[1]||''); };
      r.onerror=function(){ send('', ''); };
      r.readAsDataURL(file);
    } else { send('', ''); }
  });
})();
</script>
"""
    return s + TAIL


# ================================================================ RUN
if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    pages = {
        "index.html": build_home(),
        "platform.html": build_platform(),
        "capabilities.html": build_capabilities(),
        "built-industry.html": build_built(),
        "use-cases.html": build_usecases(),
        "company.html": build_company(),
        "discuss.html": build_discuss(),
    }
    for n, b in pages.items():
        check_css(b, n)
        write(n, b)
        print("%-22s %6d bytes" % (n, len(b)))
