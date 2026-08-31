# -*- coding: utf-8 -*-
"""Port the existing Privacy and Terms copy into the new 7 page template.

The legal wording is carried over verbatim. Only the surrounding chrome changes.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme import head, chrome_nav, TAIL

SRC = "/Users/mohammaddidarulalam/Documents/Claude/nexsun"
OUT = "/Users/mohammaddidarulalam/Documents/Claude/twosuns-live"

LEGAL_CSS = """
  .legal{max-width:860px;}
  .legal h2{font-size:23px;font-weight:800;color:var(--navy);margin:42px 0 12px;padding-top:20px;
    border-top:1px solid var(--border-soft);}
  .legal h3{font-size:17.5px;font-weight:800;color:var(--navy);margin:26px 0 8px;}
  .legal p{color:var(--text-muted);font-size:15.5px;line-height:1.82;margin-bottom:14px;}
  .legal ul{margin:0 0 18px 0;list-style:none;}
  .legal li{position:relative;padding-left:22px;color:var(--text-muted);font-size:15.5px;line-height:1.75;margin-bottom:9px;}
  .legal li::before{content:'';position:absolute;left:0;top:10px;width:7px;height:7px;border-radius:2px;
    background:linear-gradient(135deg,var(--sun),var(--gold));}
  .legal strong{color:var(--navy);font-weight:700;}
  .legal a{color:var(--sun-deep);font-weight:600;text-decoration:underline;}
"""

KEEP = re.compile(r'</?(h2|h3|p|ul|li|strong|em|br)\b[^>]*>', re.I)


def extract(path):
    s = open(path).read()
    body = s[s.find('<body'):]
    # drop chrome and scripts
    for tag in ('nav', 'footer', 'script', 'style', 'canvas'):
        body = re.sub(r'<%s\b.*?</%s>' % (tag, tag), '', body, flags=re.S | re.I)
    body = re.sub(r'<!--.*?-->', '', body, flags=re.S)

    # first h1 is the page title, everything from the first h2 onward is the body
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', body, re.S | re.I)
    title = re.sub(r'<[^>]+>', '', h1.group(1)).strip() if h1 else ""

    intro = ""
    if h1:
        after = body[h1.end():]
        p = re.search(r'<p[^>]*>(.*?)</p>', after, re.S | re.I)
        if p:
            intro = re.sub(r'<[^>]+>', '', p.group(1)).strip()
            intro = ' '.join(intro.split())

    i = body.lower().find('<h2')
    content = body[i:] if i > 0 else body

    out = []
    for m in re.finditer(r'<(h2|h3|p|ul)\b[^>]*>(.*?)</\1>', content, re.S | re.I):
        tag, inner = m.group(1).lower(), m.group(2)
        if tag == 'ul':
            lis = re.findall(r'<li\b[^>]*>(.*?)</li>', inner, re.S | re.I)
            items = "".join('<li>%s</li>' % clean(x) for x in lis if clean(x).strip())
            if items:
                out.append('<ul>%s</ul>' % items)
        else:
            c = clean(inner)
            if c.strip():
                out.append('<%s>%s</%s>' % (tag, c, tag))
    return title, intro, "\n".join(out)


def clean(frag):
    """Keep inline emphasis and mail links, drop everything else."""
    frag = re.sub(r'<a\b[^>]*href="(mailto:[^"]+)"[^>]*>(.*?)</a>',
                  lambda m: '<a href="%s">%s</a>' % (m.group(1), strip(m.group(2))), frag, flags=re.S | re.I)
    frag = re.sub(r'<a\b[^>]*>(.*?)</a>', r'\1', frag, flags=re.S | re.I)
    frag = re.sub(r'<(strong|b)\b[^>]*>(.*?)</\1>', r'<strong>\2</strong>', frag, flags=re.S | re.I)
    frag = re.sub(r'<(em|i)\b[^>]*>(.*?)</\1>', r'<em>\2</em>', frag, flags=re.S | re.I)
    frag = re.sub(r'<(?!/?(strong|em|a)\b)[^>]+>', '', frag)
    return ' '.join(frag.split())


def strip(x):
    return ' '.join(re.sub(r'<[^>]+>', '', x).split())


def build(src, dest, active):
    title, intro, content = extract(os.path.join(SRC, src))
    page = head(title + " | TwoSuns", intro[:180], dest, extra_css=LEGAL_CSS) + chrome_nav(active)
    page += """<section class="hero">
  <div class="hero-glow"></div>
  <div class="container">
    <div class="hero-eyebrow"><span class="dot"></span>Legal</div>
    <h1 style="max-width:20ch;">%s</h1>
    <p class="hero-sub">%s</p>
  </div>
</section>
<div class="sun-divider"></div>
<section>
  <div class="container">
    <div class="legal">
%s
    </div>
  </div>
</section>
""" % (title, intro, content)
    page += TAIL
    open(os.path.join(OUT, dest), "w").write(page)
    return dest, len(page), content.count('<h2>'), content.count('<li>')


if __name__ == "__main__":
    for a, b in (("privacy.html", "privacy.html"), ("terms.html", "terms.html")):
        print("%-14s %6d bytes  h2:%d  li:%d" % build(a, b, None))
