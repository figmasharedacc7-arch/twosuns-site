# -*- coding: utf-8 -*-
"""Render the TwoSuns cement microsite, English and Arabic.

Three pages per language, generated from cement_copy.py in the twosuns.ai
theme. English at /cement/, Arabic at /cement/ar/. Assets are referenced
from the site root so both depths resolve.
"""
import os, sys, html, json, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import theme
import reveal
from cement_copy import LANGS

OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "cement"))
SITE = "https://twosuns.ai"
BASE = "/cement/"
DISCUSS = "https://twosuns.ai/discuss.html"


def e(s):
    return html.escape(s, quote=False)


# Arabic CTA labels resolve back to their English counterpart, because
# discuss.html is English and renders ?ask= verbatim as a chip. Values that
# are the same in both languages are excluded, so the lookup cannot misfire.
_EN_VALUES = set(v for v in LANGS["en"].values() if isinstance(v, str))
AR_TO_EN = dict((v, LANGS["en"][k]) for k, v in LANGS["ar"].items()
                if isinstance(v, str) and isinstance(LANGS["en"].get(k), str)
                and v != LANGS["en"][k] and v not in _EN_VALUES)


def ask(label):
    """CTA target. An Arabic label sends its English equivalent so the English
    form shows a chip it can render, plus a marker recording the Arabic origin."""
    en = AR_TO_EN.get(label)
    if en is None:
        return DISCUSS + "?ask=" + urllib.parse.quote_plus(label)
    return DISCUSS + "?ask=" + urllib.parse.quote_plus(en) + "&amp;lang=ar"


def btn(label, href=None, ghost=False):
    cls = "btn-ghost" if ghost else "btn-cta"
    return '<a class="%s" href="%s">%s</a>' % (cls, href or ask(label), e(label))


# --------------------------------------------------------------- microsite CSS
CEM_CSS = r"""
  /* ---- microsite chrome ---- */
  .cmnav{position:sticky;top:0;z-index:100;background:rgba(255,248,236,.95);
    backdrop-filter:blur(16px);border-bottom:1px solid rgba(224,100,30,.15);
    box-shadow:0 1px 20px rgba(224,100,30,.08);}
  .cmnav-in{max-width:1240px;margin:0 auto;padding:0 32px;display:flex;align-items:center;
    height:70px;gap:26px;}
  .cmnav-in a.brand img{height:46px;width:auto;display:block;}
  .cmlinks{display:flex;align-items:center;gap:24px;margin-inline-start:auto;}
  .cmlinks a{font-size:14px;font-weight:600;color:var(--ink);white-space:nowrap;transition:color .2s;}
  .cmlinks a:hover,.cmlinks a.active{color:var(--sun-deep);}
  .cmlang{display:inline-flex;align-items:center;gap:9px;font-size:13px;font-weight:700;
    padding-inline:14px;border-inline:1px solid rgba(140,101,0,.22);}
  .cmlang .on{color:var(--sun-deep);}
  .cmlang a{color:var(--text-muted);}
  .cmtoggle{display:none;margin-inline-start:auto;background:none;border:0;font-size:24px;
    color:var(--navy);cursor:pointer;line-height:1;}
  .cmskip{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);
    white-space:nowrap;inset-inline-start:12px;top:10px;}
  .cmskip:focus{width:auto;height:auto;overflow:visible;clip-path:none;z-index:200;
    background:#fff;padding:8px 14px;border-radius:8px;border:2px solid var(--sun);}

  /* ---- hero with the washed plant photo ---- */
  .cmhero{position:relative;overflow:hidden;padding:104px 0 90px;
    background-image:linear-gradient(105deg,rgba(255,245,221,.97) 0%,rgba(255,243,205,.93) 38%,
      rgba(252,226,188,.72) 66%,rgba(255,242,214,.42) 100%),url('/cement/cement-banner.jpg');
    background-size:cover,cover;background-position:center,center 38%;}
  html[dir="rtl"] .cmhero{background-image:linear-gradient(255deg,rgba(255,245,221,.97) 0%,
      rgba(255,243,205,.93) 38%,rgba(252,226,188,.72) 66%,rgba(255,242,214,.42) 100%),
      url('/cement/cement-banner.jpg');}
  .cmhero h1{font-size:clamp(32px,4.4vw,54px);font-weight:900;line-height:1.1;color:var(--navy);
    margin-bottom:20px;max-width:19ch;}
  .cmhero p.hero-sub{max-width:660px;}
  .cmhero.plain{background-image:none;background:linear-gradient(160deg,#FFF5DD 0%,#FFF3CD 30%,
    #FCE2BC 60%,#FEF9C3 100%);}

  /* ---- platform family cards ---- */
  .cmfam{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:30px;}
  .cmfam>*{min-width:0;}
  .cmfam .f{background:#fff;border:1px solid var(--border);border-radius:16px;padding:24px 22px;
    box-shadow:var(--shadow);border-top:4px solid var(--sun);transition:all .3s;}
  .cmfam .f:nth-child(2){border-top-color:var(--gold);}
  .cmfam .f:nth-child(3){border-top-color:var(--sun-deep);}
  .cmfam .f:nth-child(4){border-top-color:var(--a4);}
  .cmfam .f:hover{transform:translateY(-5px);box-shadow:0 12px 40px rgba(224,100,30,.14);}
  .cmfam h3{font-size:19px;font-weight:800;color:var(--navy);margin-bottom:8px;}
  .cmfam .d{font-size:14.5px;color:var(--text-muted);line-height:1.65;margin-bottom:10px;}
  .cmfam .x{font-size:13px;color:#8C6500;line-height:1.6;font-weight:600;
    border-top:1px solid var(--border-soft);padding-top:10px;}

  /* ---- labelled rows: configuration, governance ---- */
  .cmrows{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:28px;}
  .cmrows>*{min-width:0;}
  .cmrows .r{background:#fff;border:1px solid var(--border-soft);border-radius:14px;
    padding:20px 22px;box-shadow:var(--shadow);font-size:14.5px;color:var(--text-muted);
    line-height:1.68;}
  .cmrows .r b{display:block;color:var(--navy);font-weight:800;margin-bottom:5px;font-size:15px;}
  .cmrows.two{grid-template-columns:repeat(2,1fr);}

  /* ---- architecture tiers ---- */
  .cmtier{background:#fff;border:1px solid var(--border);border-radius:20px;padding:26px 28px;
    box-shadow:var(--shadow);margin-top:18px;}
  .cmtier-h{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;margin-bottom:6px;}
  .cmtier-n{font-size:12px;font-weight:900;color:var(--sun-deep);letter-spacing:2px;}
  .cmtier-k{font-size:11.5px;font-weight:800;letter-spacing:2px;text-transform:uppercase;
    color:var(--navy);}
  .cmtier-a{font-size:11.5px;font-weight:700;color:#8C6500;margin-inline-start:auto;
    background:var(--gold-soft);border-radius:20px;padding:3px 12px;}
  .cmtier-who{font-size:13.5px;color:var(--text-muted);margin-bottom:14px;line-height:1.6;}
  .cmchips{display:flex;flex-wrap:wrap;gap:9px;}
  .cmchips li{list-style:none;background:var(--bg2);border:1px solid var(--border-soft);
    border-radius:9px;padding:9px 14px;font-size:13.5px;font-weight:700;color:var(--navy);}
  .cmnote{font-size:13px;color:var(--text-muted);margin-top:14px;line-height:1.65;font-style:italic;}
  .cmmods{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;margin-top:4px;}
  .cmmods>*{min-width:0;}
  .cmmod{border:1px solid var(--border-soft);border-radius:14px;padding:18px 18px 20px;
    background:linear-gradient(170deg,#FFFBF0,#FFF6E4);}
  .cmmod.core{background:linear-gradient(170deg,#FEF6DA,#FBE9BE);border-color:rgba(204,153,0,.3);}
  .cmmod h3{font-size:17px;font-weight:900;color:var(--navy);margin-bottom:2px;}
  .cmmod .d{font-size:12.5px;color:#8C6500;font-weight:700;margin-bottom:12px;}
  .cmmod ul{list-style:none;}
  .cmmod li{font-size:13.5px;color:var(--text-muted);line-height:1.5;padding:6px 0;
    border-top:1px solid rgba(140,101,0,.12);}
  .cmmod li:first-child{border-top:0;}
  .cmray{display:flex;align-items:center;gap:12px;background:linear-gradient(135deg,var(--sun),var(--sun-deep));
    color:#fff;border-radius:12px;padding:13px 20px;font-weight:800;font-size:15px;margin-bottom:14px;}
  .cmunits{margin-top:22px;background:var(--gold-soft);border:1px solid rgba(140,101,0,.25);
    border-radius:12px;padding:16px 20px;font-size:13.5px;color:#7A5A08;line-height:1.7;}

  /* ---- inputs table ---- */
  .cmtblw{margin-top:26px;overflow-x:auto;border:1px solid var(--border);border-radius:16px;
    box-shadow:var(--shadow);background:#fff;}
  .cmtblw:focus-visible{outline:3px solid var(--sun);outline-offset:2px;}
  .cmtbl{width:100%;border-collapse:collapse;min-width:720px;}
  .cmtbl th{text-align:start;font-size:11px;font-weight:800;letter-spacing:1.6px;
    text-transform:uppercase;color:#8C6500;background:var(--gold-soft);padding:13px 18px;
    border-bottom:1px solid rgba(140,101,0,.22);}
  .cmtbl td{text-align:start;font-size:14px;color:var(--text-muted);padding:14px 18px;
    border-bottom:1px solid var(--border-soft);line-height:1.6;vertical-align:top;}
  .cmtbl tr:last-child td{border-bottom:0;}
  .cmtbl td:first-child{font-weight:700;color:var(--navy);}
  .cmtbl tr:hover td{background:rgba(255,246,226,.7);}

  /* ---- events ---- */
  .cmev{background:#fff;border:1px solid var(--border);border-radius:20px;padding:28px 30px;
    box-shadow:var(--shadow);margin-top:20px;}
  .cmev-when{font-size:13px;font-weight:800;color:#8C6500;letter-spacing:.4px;margin-bottom:8px;}
  .cmev h3{font-size:clamp(19px,2.2vw,25px);font-weight:800;color:var(--navy);line-height:1.25;
    margin-bottom:10px;}
  .cmev p{font-size:15px;color:var(--text-muted);line-height:1.72;}
  .cmev .acts{display:flex;flex-wrap:wrap;gap:12px;margin-top:20px;}
  .cmev.feat{border:1px solid rgba(224,100,30,.4);
    background:linear-gradient(165deg,#FFFBF0 0%,#FEF3DA 100%);}
  .cmbadge{display:inline-block;background:var(--navy);color:#FFD9A8;font-size:10.5px;
    font-weight:800;letter-spacing:1.6px;text-transform:uppercase;padding:5px 14px;
    border-radius:20px;margin-bottom:14px;}
  .cmses{display:grid;grid-template-columns:96px 1fr;gap:0;background:#fff;
    border:1px solid var(--border-soft);border-radius:18px;overflow:hidden;
    box-shadow:var(--shadow);margin-top:18px;}
  .cmses-d{background:linear-gradient(150deg,var(--sun),var(--sun-deep));color:#fff;
    display:flex;flex-direction:column;align-items:center;justify-content:center;padding:20px 8px;}
  .cmses-d .dd{font-size:32px;font-weight:900;line-height:1;}
  .cmses-d .mm{font-size:12px;font-weight:800;letter-spacing:2px;text-transform:uppercase;margin-top:4px;}
  .cmses-b{padding:22px 26px;}
  .cmmeta{display:flex;flex-wrap:wrap;gap:8px 18px;margin-top:14px;font-size:13.5px;
    color:var(--text-muted);font-weight:600;}
  .cmmeta span{display:inline-flex;align-items:center;gap:7px;}
  .cmmeta span::before{content:'';width:6px;height:6px;border-radius:50%;background:var(--sun);flex-shrink:0;}

  /* ---- agenda ---- */
  .cmag{margin-top:22px;border:1px solid var(--border);border-radius:18px;overflow:hidden;
    background:#fff;box-shadow:var(--shadow);}
  .cmag-r{display:grid;grid-template-columns:148px 1fr;gap:0;
    border-bottom:1px solid var(--border-soft);}
  .cmag-r:last-child{border-bottom:0;}
  .cmag-t{padding:16px 18px;font-size:13.5px;font-weight:800;color:#8C6500;
    background:rgba(255,246,226,.75);border-inline-end:1px solid var(--border-soft);}
  .cmag-b{padding:16px 22px;}
  .cmag-b h3{font-size:15.5px;font-weight:800;color:var(--navy);margin-bottom:3px;
    display:flex;align-items:center;gap:10px;flex-wrap:wrap;}
  .split2-panel h3{font-size:11px;font-weight:800;letter-spacing:2px;text-transform:uppercase;
    color:#8C6500;margin-bottom:14px;}
  html[dir="rtl"] .split2-panel h3{letter-spacing:0;}
  .cmag-k{font-size:9.5px;font-weight:800;letter-spacing:1.4px;text-transform:uppercase;
    color:var(--sun-deep);border:1px solid rgba(224,100,30,.4);border-radius:20px;padding:2px 9px;}
  .cmag-b p{font-size:13.5px;color:var(--text-muted);line-height:1.6;}
  .cmag-b ul{list-style:none;margin-top:7px;}
  .cmag-b li{font-size:13px;color:var(--text-muted);padding-inline-start:14px;position:relative;
    line-height:1.6;}
  .cmag-b li::before{content:'';position:absolute;inset-inline-start:0;top:9px;width:5px;height:5px;
    border-radius:50%;background:var(--gold);}

  /* ---- practical details ---- */
  .cmpd{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:26px;}
  .cmpd>*{min-width:0;}
  .cmpd .p{background:#fff;border:1px solid var(--border-soft);border-radius:14px;padding:18px 20px;
    box-shadow:var(--shadow);}
  .cmpd .k{font-size:10.5px;font-weight:800;letter-spacing:1.6px;text-transform:uppercase;
    color:#8C6500;margin-bottom:6px;}
  .cmpd .v{font-size:14px;color:var(--navy);font-weight:700;line-height:1.55;}

  /* ---- past events ---- */
  .cmpast{list-style:none;margin-top:24px;display:grid;gap:12px;}
  .cmpast li{background:rgba(255,255,255,.72);border:1px solid var(--border-soft);
    border-radius:12px;padding:15px 20px;font-size:14.5px;color:var(--text-muted);}
  .cmpast b{color:var(--navy);font-weight:800;}

  /* ---- microsite footer ---- */
  .cmfoot{background:var(--bg);border-top:3px solid var(--sun);padding:48px 0 28px;
    position:relative;z-index:2;}
  .cmfoot-top{display:flex;flex-wrap:wrap;gap:26px;align-items:flex-start;justify-content:space-between;}
  .cmfoot-brand img{height:42px;margin-bottom:10px;display:block;}
  .cmfoot-brand .by{font-size:12.5px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;
    color:#8C6500;}
  .cmfoot-brand .cn{font-size:13.5px;color:var(--text-muted);margin-top:8px;line-height:1.7;}
  .cmfoot-links{display:flex;flex-wrap:wrap;gap:8px 20px;align-items:center;}
  .cmfoot-links a{font-size:14px;font-weight:600;color:var(--text-muted);}
  .cmfoot-links a:hover{color:var(--sun-deep);}
  .cmfoot-bot{margin-top:28px;padding-top:18px;border-top:1px solid var(--border-soft);
    display:flex;flex-wrap:wrap;gap:10px 20px;justify-content:space-between;font-size:13px;
    color:var(--text-muted);}

  @media(max-width:1000px){
    .cmfam,.cmrows,.cmrows.two,.cmmods{grid-template-columns:repeat(2,1fr);}
    .cmpd{grid-template-columns:repeat(2,1fr);}
  }
  @media(max-width:820px){
    .cmtoggle{display:block;}
    .cmlinks{display:none;position:absolute;top:70px;inset-inline:0;background:rgba(255,250,240,.99);
      flex-direction:column;align-items:stretch;gap:0;padding:10px 24px 18px;
      border-bottom:1px solid var(--border);box-shadow:0 14px 30px rgba(60,50,30,.14);}
    .cmlinks.open{display:flex;}
    .cmlinks a{padding:11px 0;}
    .cmlang{border-inline:0;padding-inline:0;border-top:1px solid var(--border-soft);
      padding-top:10px;margin-top:4px;}
  }
  @media(max-width:620px){
    .cmfam,.cmrows,.cmrows.two,.cmmods,.cmpd{grid-template-columns:1fr;}
    .cmag-r,.cmses{grid-template-columns:1fr;}
    .cmag-t{border-inline-end:0;border-bottom:1px solid var(--border-soft);}
    .cmses-d{flex-direction:row;gap:10px;padding:12px;}
    .cmhero{padding:72px 0 62px;}
  }
"""

# the theme stylesheet is authored left to right, so mirror what it hard-codes
RTL_CSS = r"""
  html[dir="rtl"] .tick li{padding-left:0;padding-right:22px;}
  html[dir="rtl"] .tick li::before{left:auto;right:0;}
  html[dir="rtl"] .step{padding:20px 68px 20px 22px;}
  html[dir="rtl"] .step::before{left:auto;right:22px;}
  html[dir="rtl"] .split2-panel::after{right:auto;left:-50px;}
  html[dir="rtl"] .hero-glow{right:auto;left:-90px;}
  html[dir="rtl"] .btn-cta,html[dir="rtl"] .btn-ghost{letter-spacing:0;}
  html[dir="rtl"] .section-tag,html[dir="rtl"] .hero-eyebrow,
  html[dir="rtl"] .cmtier-k,html[dir="rtl"] .cmpd .k,html[dir="rtl"] .cmtbl th,
  html[dir="rtl"] .cmbadge,html[dir="rtl"] .cmag-k,html[dir="rtl"] .cmfoot-brand .by,
  html[dir="rtl"] .cmses-d .mm,html[dir="rtl"] .cmtier-n{letter-spacing:0;}
  html[dir="rtl"] body{font-family:'Segoe UI','Noto Sans Arabic','Geeza Pro',Tahoma,
    system-ui,-apple-system,sans-serif;}
  html[dir="rtl"] .cmhero.plain{background-image:none;
    background:linear-gradient(200deg,#FFF5DD 0%,#FFF3CD 30%,#FCE2BC 60%,#FEF9C3 100%);}
  html[dir="rtl"] .cmhero h1{max-width:24ch;line-height:1.3;}
  html[dir="rtl"] .hero h1{line-height:1.3;}
  html[dir="rtl"] .section-heading{line-height:1.35;}
  html[dir="rtl"] .cta-band h2{line-height:1.4;}
  html[dir="rtl"] .cmev h3{line-height:1.4;}
"""


def head(d, title, desc, page):
    """Page head. Arabic sits one level deeper, so canonical and alternates differ."""
    sub = "ar/" if d["lang"] == "ar" else ""
    canon = SITE + BASE + sub + ("" if page == "index.html" else page)
    en_url = SITE + BASE + ("" if page == "index.html" else page)
    ar_url = SITE + BASE + "ar/" + ("" if page == "index.html" else page)
    esc_t, esc_d = title.replace('"', "&quot;"), desc.replace('"', "&quot;")
    return f"""<!DOCTYPE html>
<html lang="{d['lang']}" dir="{d['dir']}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="ar" href="{ar_url}">
<link rel="alternate" hreflang="x-default" href="{en_url}">
<meta name="theme-color" content="#FFF5DD">
<meta property="og:type" content="website">
<meta property="og:site_name" content="TwoSuns">
<meta property="og:locale" content="{'ar_EG' if d['lang'] == 'ar' else 'en_CA'}">
<meta property="og:title" content="{esc_t}">
<meta property="og:description" content="{esc_d}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}/og-twosuns.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc_t}">
<meta name="twitter:description" content="{esc_d}">
<meta name="twitter:image" content="{SITE}/og-twosuns.jpg">
<link rel="icon" type="image/svg+xml" href="/logo-mini.svg">
<style>{theme.CSS}{theme.REVEAL_CSS}{CEM_CSS}{RTL_CSS}</style>
{theme.REVEAL_HEAD}
{theme.LEADLANDER}
</head>
<body>
<a class="cmskip" href="#main">{e(d['skip'])}</a>
<canvas id="sun-canvas" aria-hidden="true"></canvas>
"""


def nav(d, active):
    """Microsite nav. The language toggle keeps the visitor on the same page."""
    pre = "../" if d["lang"] == "ar" else "ar/"
    def mark(u):
        here = u.split("#")[0] == active and (active != "index.html" or "#" not in u)
        return ' class="active" aria-current="page"' if here else ""
    links = "".join('<a href="%s"%s>%s</a>' % (u, mark(u), e(n)) for n, u in d["nav"])
    other = pre + ("" if active == "index.html" else active)
    lang = ('<span class="cmlang"><span class="on">%s</span>'
            '<a href="%s" lang="%s" hreflang="%s">%s</a></span>'
            % (e(d["self_label"]), other, d["other"], d["other"], e(d["other_label"])))
    return """<nav class="cmnav">
  <div class="cmnav-in">
    <a class="brand" href="./"><img src="/logo-color.svg" alt="TwoSuns"></a>
    <button class="cmtoggle" aria-label="%s" aria-controls="cml" aria-expanded="false"
      onclick="var l=document.getElementById('cml');l.classList.toggle('open');
        this.setAttribute('aria-expanded',l.classList.contains('open'));">&#9776;</button>
    <div class="cmlinks" id="cml">%s%s
      <a class="btn-cta" href="%s">%s</a>
    </div>
  </div>
</nav>
<main id="main" tabindex="-1">
""" % (e(d["menu_label"]), links, lang, ask(d["nav_cta"]), e(d["nav_cta"]))


def footer(d):
    links = "".join('<a href="%s">%s</a>' % (u, e(n)) for n, u in d["foot_links"])
    return """</main>
<footer class="cmfoot">
  <div class="container">
    <div class="cmfoot-top">
      <div class="cmfoot-brand">
        <img src="/logo-color.svg" alt="TwoSuns">
        <div class="by">%s</div>
        <div class="cn"><a href="mailto:info@twosuns.ai">%s</a><br>%s</div>
      </div>
      <div class="cmfoot-links">%s</div>
    </div>
    <div class="cmfoot-bot">
      <div>%s</div>
      <div><a href="%s/privacy.html">%s</a> &nbsp;|&nbsp; <a href="%s/terms.html">%s</a>
        &nbsp;|&nbsp; <a href="%s/">%s</a></div>
    </div>
  </div>
</footer>
""" % (e(d["by"]), e(d["foot_email"]), e(d["foot_wa"]), links, e(d["foot_rights"]),
       SITE, e(d["foot_privacy"]), SITE, e(d["foot_terms"]), SITE, e(d["main_site"]))


TAIL_JS = theme.PARTICLES + reveal.body_script() + "\n</body>\n</html>\n"


def hero(d, eyebrow, h1, sub, acts, plain=False):
    return """<section class="cmhero%s">
  <div class="hero-glow"></div>
  <div class="container">
    <div class="hero-eyebrow"><span class="dot"></span>%s</div>
    <h1>%s</h1>
    <p class="hero-sub">%s</p>
    <div class="hero-actions">%s</div>
  </div>
</section>
<div class="sun-divider"></div>
""" % (" plain" if plain else "", e(eyebrow), e(h1), e(sub), acts)


def cta_band(heading, para, acts):
    return """<section class="cta-band">
  <div class="container">
    <h2>%s</h2>
    <p>%s</p>
    <div class="cta-actions">%s</div>
  </div>
</section>
""" % (e(heading), e(para), acts)


def rows(items, two=False):
    cells = "".join('<div class="r"><b>%s</b>%s</div>' % (e(k), e(v)) for k, v in items)
    return '<div class="cmrows%s">%s</div>' % (" two" if two else "", cells)


def chips(items):
    return '<ul class="cmchips">%s</ul>' % "".join("<li>%s</li>" % e(i) for i in items)


def ticks(items):
    return '<ul class="tick">%s</ul>' % "".join("<li>%s</li>" % e(i) for i in items)


def steps(items):
    return '<div class="steps">%s</div>' % "".join(
        '<div class="step"><b>%s</b> %s</div>' % (e(a), e(b)) for a, b in items)


# ================================================================ HOME
def build_home(d):
    s = head(d, d["home_title"], d["home_desc"], "index.html") + nav(d, "index.html")
    s += hero(d, d["home_eyebrow"], d["home_h1"], d["home_sub"],
              btn(d["home_cta1"]) + " " + btn(d["home_cta2"], "platform.html", ghost=True))

    fams = "".join('<div class="f"><h3>%s</h3><div class="d">%s</div><div class="x">%s</div></div>'
                   % (e(n), e(a), e(b)) for n, a, b in d["fams"])
    s += """<section id="about">
  <div class="container">
    <div class="section-tag">%s</div>
    <h2 class="section-heading">%s</h2>
    <p class="lede">%s</p>
    <p class="lede">%s</p>
    <h3 class="sub-heading" style="margin-top:34px;font-size:22px;">%s</h3>
    <div class="cmfam">%s</div>
  </div>
</section>
""" % (e(d["about_tag"]), e(d["about_h"]), e(d["about_p1"]), e(d["about_p2"]),
       e(d["about_fam_h"]), fams)

    s += """<section id="context" class="band-alt">
  <div class="container">
    <div class="split2" style="align-items:start;">
      <div>
        <div class="section-tag">%s</div>
        <h2 class="section-heading">%s</h2>
        <p class="section-sub">%s</p>
        <p class="section-sub" style="margin-top:16px;">%s</p>
      </div>
      <div class="split2-panel"><h3>%s</h3>%s</div>
    </div>
    <div class="callout">
      <h3>%s</h3>
      <p>%s</p>
    </div>
  </div>
</section>
""" % (e(d["ctx_tag"]), e(d["ctx_h"]), e(d["ctx_p1"]), e(d["ctx_p2"]),
       e(d["ctx_cond_h"]), ticks(d["ctx_cond"]),
       e(d["ctx_flow_h"]), e(d["ctx_flow_p"]))

    s += """<section class="band-warm">
  <div class="container">
    <div class="section-tag">%s</div>
    <h2 class="section-heading">%s</h2>
    <p class="section-sub">%s</p>
    %s
  </div>
</section>
""" % (e(d["cfg_tag"]), e(d["cfg_h"]), e(d["cfg_p"]), rows(d["cfg_rows"]))

    s += cta_band(d["home_close_h"], d["home_close_p"],
                  btn(d["home_close_cta1"]) + " " + btn(d["home_close_cta2"], ghost=True))
    return s + footer(d) + TAIL_JS


# ================================================================ PLATFORM
def build_platform(d):
    s = head(d, d["plat_title"], d["plat_desc"], "platform.html") + nav(d, "platform.html")
    s += hero(d, d["plat_eyebrow"], d["plat_h1"], d["plat_sub"],
              btn(d["plat_cta1"]) + " " + btn(d["plat_cta2"], ghost=True), plain=True)

    s += """<section>
  <div class="container">
    <div class="section-tag">%s</div>
    <h2 class="section-heading">%s</h2>
    %s
    <div class="split2" style="margin-top:34px;align-items:start;">
      <div class="split2-panel"><h3>%s</h3>%s</div>
      <div class="callout" style="margin-top:0;"><p>%s</p></div>
    </div>
  </div>
</section>
""" % (e(d["how_tag"]), e(d["how_h"]), steps(d["how_steps"]),
       e(d["how_carry_h"]), ticks(d["how_carry"]), e(d["how_note"]))

    def mod(cls, h, dd, cnt, items):
        c = '<div class="d">%s%s</div>' % (e(dd), (" · " + e(cnt)) if cnt else "")
        return ('<div class="cmmod %s"><h3>%s</h3>%s<ul>%s</ul></div>'
                % (cls, e(h), c, "".join("<li>%s</li>" % e(i) for i in items)))

    s += """<section class="band-alt">
  <div class="container">
    <div class="section-tag">%s</div>
    <h2 class="section-heading">%s</h2>
    <p class="section-sub">%s</p>

    <div class="cmtier">
      <div class="cmtier-h"><span class="cmtier-n">%s</span>
        <span class="cmtier-k">%s</span><span class="cmtier-a">%s</span></div>
      <div class="cmtier-who">%s</div>
      %s
      <p class="cmnote">%s</p>
    </div>

    <div class="cmtier">
      <div class="cmtier-h"><span class="cmtier-n">%s</span>
        <span class="cmtier-k">%s</span><span class="cmtier-a">%s</span></div>
      <div class="cmmods">%s%s%s</div>
    </div>

    <div class="cmtier">
      <div class="cmtier-h"><span class="cmtier-n">%s</span>
        <span class="cmtier-k">%s</span><span class="cmtier-a">%s</span></div>
      <div class="cmray">%s</div>
      %s
      <p class="cmnote">%s</p>
    </div>

    <div class="cmunits">%s</div>
  </div>
</section>
""" % (e(d["arch_tag"]), e(d["arch_h"]), e(d["arch_p"]),
       e(d["arch_t1_n"]), e(d["arch_t1_k"]), e(d["arch_t1_a"]), e(d["arch_t1_who"]),
       chips(d["arch_t1"]), e(d["arch_t1_note"]),
       e(d["arch_t2_n"]), e(d["arch_t2_k"]), e(d["arch_t2_a"]),
       mod("", d["arch_hz_h"], d["arch_hz_d"], d["arch_hz_c"], d["arch_hz"]),
       mod("core", d["arch_core_h"], d["arch_core_d"], "", d["arch_core"]),
       mod("", d["arch_pl_h"], d["arch_pl_d"], d["arch_pl_c"], d["arch_pl"]),
       e(d["arch_t3_n"]), e(d["arch_t3_k"]), e(d["arch_t3_a"]),
       e(d["arch_ray"]), chips(d["arch_t3"]), e(d["arch_t3_note"]),
       e(d["arch_units"]))

    head_cells = "".join("<th>%s</th>" % e(c) for c in d["data_cols"])
    body_rows = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % e(c) for c in r)
                        for r in d["data_rows"])
    s += """<section>
  <div class="container">
    <div class="section-tag">%s</div>
    <h2 class="section-heading">%s</h2>
    <p class="section-sub">%s</p>
    <div class="cmtblw" tabindex="0" role="region" aria-label="%s"><table class="cmtbl">
      <thead><tr>%s</tr></thead><tbody>%s</tbody>
    </table></div>
    <p class="lede" style="margin-top:24px;">%s</p>
    <p class="lede">%s</p>
  </div>
</section>
""" % (e(d["data_tag"]), e(d["data_h"]), e(d["data_p"]), e(d["table_label"]),
       head_cells, body_rows,
       e(d["data_p2"]), e(d["data_p3"]))

    s += """<section class="band-warm">
  <div class="container">
    <div class="section-tag">%s</div>
    <h2 class="section-heading">%s</h2>
    %s
    <p class="lede" style="margin-top:22px;">%s</p>
    <div class="split2-panel" style="margin-top:22px;max-width:700px;"><h3>%s</h3>%s</div>
  </div>
</section>
""" % (e(d["dep_tag"]), e(d["dep_h"]), steps(d["dep_steps"]), e(d["dep_p"]),
       e(d["dep_prov_h"]), ticks(d["dep_prov"]))

    s += """<section>
  <div class="container">
    <div class="section-tag">%s</div>
    <h2 class="section-heading">%s</h2>
    %s
  </div>
</section>
""" % (e(d["gov_tag"]), e(d["gov_h"]), rows(d["gov_rows"], two=True))

    s += cta_band(d["plat_close_h"], d["plat_close_p"],
                  btn(d["plat_cta1"]) + " " + btn(d["plat_cta2"], ghost=True))
    return s + footer(d) + TAIL_JS


# ================================================================ EVENTS
def events_jsonld(d):
    """Event structured data for the three dated items on the events page.
    Times are Africa/Cairo, which is UTC+2 in November. The invitation-only
    items carry no offers, because there is no ticket to price."""
    sub = "ar/" if d["lang"] == "ar" else ""
    page = SITE + BASE + sub + "events.html"
    cairo = {"@type": "PostalAddress", "addressLocality": "Cairo",
             "addressCountry": "EG"}
    base = {"eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
            "eventStatus": "https://schema.org/EventScheduled",
            "inLanguage": d["lang"], "url": page}
    conf_id = page + "#aicce29"
    conf = dict(base, **{
        "@type": "Event", "@id": conf_id,
        "name": d["ev1_h"], "description": d["ev1_p"],
        "startDate": "2026-11-23", "endDate": "2026-11-25",
        "location": {"@type": "Place", "name": d["ev1_where"], "address": cairo},
        "organizer": {"@type": "Organization",
                      "name": "Arab Union for Cement and Building Materials",
                      "alternateName": "AUCBM"},
    })
    session = dict(base, **{
        "@type": "Event", "@id": page + "#session-10-7",
        "name": d["ses_h"], "description": d["ses_p"],
        "identifier": d["ses_code"],
        "startDate": "2026-11-24T13:30:00+02:00",
        "endDate": "2026-11-24T13:45:00+02:00",
        "superEvent": {"@id": conf_id},
        "location": {"@type": "Place", "name": d["ses_place"], "address": cairo},
        "performer": {"@type": "Person", "name": "Aiman El-Ramly",
                      "jobTitle": "Chief Executive Officer",
                      "worksFor": {"@type": "Organization", "name": "TwoSuns"}},
    })
    reception = dict(base, **{
        "@type": "Event", "@id": page + "#future-of-cement",
        "name": d["ev2_h"], "description": d["ev2_p"],
        "startDate": "2026-11-25T16:00:00+02:00",
        "endDate": "2026-11-25T23:00:00+02:00",
        "location": {"@type": "Place", "name": d["ev2_place"], "address": cairo},
        "organizer": [{"@type": "Organization", "name": "TwoSuns"},
                      {"@type": "Organization", "name": "Korayem Group"}],
    })
    graph = {"@context": "https://schema.org",
             "@graph": [conf, session, reception]}
    blob = json.dumps(graph, ensure_ascii=False, separators=(",", ":"))
    return ('<script type="application/ld+json">%s</script>\n'
            % blob.replace("<", "\\u003c"))


def build_events(d):
    s = head(d, d["ev_title"], d["ev_desc"], "events.html") + nav(d, "events.html")
    s += hero(d, d["ev_eyebrow"], d["ev_h1"], d["ev_sub"],
              btn(d["ev_cta1"]) + " " + btn(d["ev_cta2"], ghost=True), plain=True)

    s += """<section>
  <div class="container">
    <div class="section-tag">%s</div>
    <h2 class="section-heading">%s</h2>
    <p class="section-sub">%s</p>

    <div class="cmev">
      <div class="cmev-when">%s &middot; %s</div>
      <h3>%s</h3>
      <p>%s</p>
      <div class="acts">%s</div>
    </div>

    <div class="cmses">
      <div class="cmses-d"><span class="dd">%s</span><span class="mm">%s</span></div>
      <div class="cmses-b">
        <div class="cmev-when">%s &middot; %s</div>
        <h3 style="font-size:20px;">%s</h3>
        <p style="font-weight:700;color:var(--navy);margin-bottom:6px;">%s</p>
        <p>%s</p>
        <div class="cmmeta"><span>%s</span><span>%s</span><span>%s</span></div>
      </div>
    </div>
  </div>
</section>
""" % (e(d["ev_up_tag"]), e(d["ev_up_h"]), e(d["ev_up_p"]),
       e(d["ev1_when"]), e(d["ev1_where"]), e(d["ev1_h"]), e(d["ev1_p"]),
       btn(d["ev1_cta"]),
       e(d["ses_day"]), e(d["ses_mon"]), e(d["ses_tag"]), e(d["ses_code"]),
       e(d["ses_h"]), e(d["ses_who"]), e(d["ses_p"]),
       e(d["ses_when"]), e(d["ses_time"]), e(d["ses_place"]))

    ag = ""
    for t, h, kind, p, who in d["ag_rows"]:
        k = '<span class="cmag-k">%s</span>' % e(kind) if kind else ""
        body = "<h3>%s%s</h3>" % (e(h), k)
        if p:
            body += "<p>%s</p>" % e(p)
        if who:
            body += "<ul>%s</ul>" % "".join("<li>%s</li>" % e(w) for w in who)
        ag += ('<div class="cmag-r"><div class="cmag-t">%s</div>'
               '<div class="cmag-b">%s</div></div>' % (e(t), body))

    pd = "".join('<div class="p"><div class="k">%s</div><div class="v">%s</div></div>'
                 % (e(k), e(v)) for k, v in d["pd_rows"])

    s += """<section class="band-alt">
  <div class="container">
    <div class="cmev feat">
      <div class="cmbadge">%s</div>
      <h3>%s</h3>
      <p style="font-weight:700;color:var(--navy);">%s</p>
      <p style="margin-bottom:12px;">%s</p>
      <div class="cmmeta"><span>%s</span><span>%s</span><span>%s</span><span>%s</span></div>
      <p style="margin-top:16px;">%s</p>
      <div class="acts">%s %s</div>
      <p class="cmnote">%s</p>
    </div>

    <h3 class="sub-heading" style="margin-top:38px;font-size:22px;">%s</h3>
    <div class="cmag">%s</div>
    <p class="cmnote">%s</p>

    <h3 class="sub-heading" style="margin-top:38px;font-size:22px;">%s</h3>
    <div class="cmpd">%s</div>
  </div>
</section>
""" % (e(d["ev2_badge"]), e(d["ev2_h"]), e(d["ev2_kicker"]), e(d["ev2_line"]),
       e(d["ev2_when"]), e(d["ev2_time"]), e(d["ev2_place"]), e(d["ev2_dress"]),
       e(d["ev2_p"]), btn(d["ev2_cta1"]), btn(d["ev2_cta2"], ghost=True), e(d["ev2_note"]),
       e(d["ag_h"]), ag, e(d["ag_note"]), e(d["pd_tag"]), pd)

    past = "".join("<li><b>%s</b> &middot; %s &middot; %s</li>" % (e(a), e(b), e(c))
                   for a, b, c in d["past_rows"])
    s += """<section>
  <div class="container">
    <div class="section-tag">%s</div>
    <h2 class="section-heading">%s</h2>
    <p class="section-sub">%s</p>
    <ul class="cmpast">%s</ul>
  </div>
</section>
""" % (e(d["past_tag"]), e(d["past_h"]), e(d["past_p"]), past)

    s += cta_band(d["ev_close_h"], d["ev_close_p"],
                  btn(d["ev_cta2"]) + " " + btn(d["ev_cta1"], ghost=True))
    return s + events_jsonld(d) + footer(d) + TAIL_JS


# ================================================================ CHECKS
BANNED = ["—", "–", "revolutionary", "cutting-edge", "seamless", "leverage",
          "unlock", "empower", "AI-powered", "robust", "game-chang", "best-in-class",
          "transform the", "supercharge", "effortless", "turnkey solution"]


def check(body, name):
    low = body.lower()
    for b in BANNED:
        if b.lower() in low:
            raise SystemExit("cement.py: %s contains banned token %r" % (name, b))
    for tag in ("div", "section", "ul", "table"):
        o = body.count("<%s" % tag)
        c = body.count("</%s>" % tag)
        if o != c:
            raise SystemExit("cement.py: %s unbalanced <%s>: %d open, %d close"
                             % (name, tag, o, c))
    if body.count("<html") != 1 or body.count("</html>") != 1:
        raise SystemExit("cement.py: %s bad html wrapper" % name)
    # the reveal CSS hides content until the body script runs. Ship both or neither.
    if "classList.add('rv')" in body and "IntersectionObserver(function" not in body:
        raise SystemExit("cement.py: %s loads the reveal CSS without the reveal "
                         "body script, so revealed sections would stay invisible" % name)


if __name__ == "__main__":
    total = 0
    for code, d in LANGS.items():
        out = OUT if code == "en" else os.path.join(OUT, "ar")
        os.makedirs(out, exist_ok=True)
        pages = {"index.html": build_home(d),
                 "platform.html": build_platform(d),
                 "events.html": build_events(d)}
        for n, b in pages.items():
            check(b, "%s/%s" % (code, n))
            with open(os.path.join(out, n), "w") as f:
                f.write(b)
            total += len(b)
            print("%-8s %-14s %7d bytes" % (code, n, len(b)))
    print("total %d bytes" % total)
