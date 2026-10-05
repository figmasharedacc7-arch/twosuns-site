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


# ---------------------------------------------------------------------------
# The legal copy is lifted verbatim out of the old Nexsun site, which sold a
# commodity and energy market intelligence product. Nobody wrote legal pages
# for TwoSuns at the rebrand, so these two pages still described that product
# on a live site selling enterprise software to the built industry.
#
# Everything below removes a statement that is not true of TwoSuns, or adds a
# disclosure that was missing. Nothing here rewrites an actual legal provision:
# liability, warranties, indemnification, confidentiality and governing law are
# untouched and still need a lawyer's read. Each entry is (page, old, new),
# and new = "" means delete. Every one must match exactly once or the build
# fails, so a change upstream cannot silently skip a fix.
# ---------------------------------------------------------------------------
FIXES = [
    # 1. The old site's chat widget and cookie banner leaked into the extracted
    #    copy as ordinary paragraphs. They are chrome, not legal text, and the
    #    chat line describes the wrong product.
    ("both", "<p>Typically replies within 1 business day</p>", ""),
    ("both", '<p>\U0001F44B Welcome to <strong>TwoSuns</strong>, the decision layer for '
             'traded markets.How can we help you today?</p>', ""),
    ("both", '<p>\U0001F36A We use cookies to improve your experience, analyze site traffic, '
             'and personalize content. By clicking <strong>Accept All</strong>, you agree to '
             'our use of cookies. Privacy Policy \u00b7 Cookie Policy</p>', ""),

    # 2. Privacy 2.3 described commodity, energy and financial market searches,
    #    watchlists and market intelligence exports. None of that is TwoSuns.
    ("privacy",
     "<h3>2.3 Market Data Queries</h3>\n<ul><li>Queries submitted to TwoSuns's AI intelligence "
     "capabilities, including commodity, energy, and financial market search inputs</li>"
     "<li>Saved reports, watchlists, and dashboard configurations associated with your account</li>"
     "<li>Export and download activity of market intelligence outputs</li></ul>",
     "<h3>2.3 Platform Content and Queries</h3>\n<ul><li>Information you and your organization "
     "submit to or connect with the platform, including documents, records and operational data "
     "from your own systems</li><li>Queries and instructions submitted to the platform's "
     "intelligence and workflow capabilities</li><li>Saved views, configurations and reports "
     "associated with your account</li><li>Export and download activity of platform outputs</li></ul>"),

    # 3. LeadLander runs on every page of this website and was disclosed nowhere.
    ("privacy",
     "<p>We use cookies and similar tracking technologies to operate and improve our Services. "
     "For a full description of the cookies we use and how to manage your preferences, please "
     "see our Cookie Policy.</p>",
     "<p>We use cookies and similar tracking technologies to operate and improve our Services.</p>\n"
     "<p>On this website we also use LeadLander, a visitor identification service. It records "
     "information such as IP address, the organization associated with that address, the pages "
     "visited and session activity, and we use it to understand which organizations are "
     "interested in TwoSuns. It runs in a cookieless mode and does not place cookies on your "
     "device. If you would prefer we did not record your visits, write to "
     '<a href="mailto:privacy@twosuns.ai">privacy@twosuns.ai</a>.</p>'),

    # 4. Securities language. TwoSuns does not produce financial research, so
    #    these describe obligations and risks that do not arise.
    ("terms",
     "<li>Using Platform outputs to facilitate market manipulation or insider trading</li>", ""),
    ("terms",
     "<li>Representing Platform-generated intelligence as independently verified financial "
     "research or advice to third parties</li>",
     "<li>Representing Platform outputs as independently verified professional advice to "
     "third parties</li>"),
    ("terms",
     "<li>Reselling, sublicensing, or redistributing Platform outputs or market intelligence data "
     "as a standalone data product or service to third parties without a separate data "
     "distribution agreement with TwoSuns</li>",
     "<li>Reselling, sublicensing, or redistributing Platform outputs as a standalone data "
     "product or service to third parties without a separate agreement with TwoSuns</li>"),

    # 5. The whole disclaimer was written for a market intelligence product. The
    #    substance worth keeping is that outputs are decision support, may be
    #    wrong, and do not replace professional advice.
    ("terms",
     "<h2>5. Market Intelligence Disclaimer</h2>", "<h2>5. Platform Output Disclaimer</h2>"),
    ("terms",
     "<p><strong>Important:</strong> All market intelligence, analysis, forecasts, and insights "
     "generated by the TwoSuns platform are provided for <strong>informational and "
     "decision-support purposes only</strong>. They do not constitute financial advice, "
     "investment recommendations, trading instructions, or legal advice. TwoSuns is not a "
     "registered investment adviser, broker-dealer, commercial orchestration adviser, or "
     "financial planner in any jurisdiction.</p>",
     "<p><strong>Important:</strong> Analysis, recommendations and other outputs generated by "
     "the TwoSuns platform are provided for <strong>informational and decision-support purposes "
     "only</strong>. They do not constitute professional, engineering, legal or financial "
     "advice, and they do not replace the judgement of the people accountable for a decision.</p>"),
    ("terms",
     "<li>All investment, trading, and commercial decisions are made solely at your own risk "
     "and discretion</li>",
     "<li>All operational and commercial decisions are made solely at your own risk and "
     "discretion</li>"),
    ("terms",
     "<li>Platform outputs are based on publicly available data, AI-assisted analysis, and "
     "algorithmic processing, and may contain errors, omissions, or outdated information</li>",
     "<li>Platform outputs are based on the data connected to it, AI-assisted analysis and "
     "automated processing, and may contain errors, omissions or outdated information</li>"),
    ("terms",
     "<li>Past performance data presented on the Platform does not guarantee or predict future "
     "results</li>", ""),
    ("terms",
     "<li>You should seek independent professional financial, legal, or regulatory advice before "
     "making material commercial or investment decisions</li>",
     "<li>You should seek independent professional advice before making material commercial, "
     "engineering or regulatory decisions</li>"),
    ("terms",
     "<li>TwoSuns's Persistent Orchestration provides explainability of AI reasoning but does not "
     "guarantee the accuracy of underlying data sources or market forecasts</li>",
     "<li>The platform records the context behind a result so that reasoning can be reviewed, "
     "but this does not guarantee the accuracy of the underlying data sources</li>"),

    # 6. Two of the four claimed marks are unverified, so they come out until
    #    someone confirms them. Name and logo stay.
    ("terms",
     '<p>The TwoSuns name, logo, "Persistent Orchestration", "TwoSuns Core\u2122", and related '
     "marks are trademarks of AEPG Inc. You may not use these marks without our prior written "
     "consent.</p>",
     "<p>The TwoSuns name, logo and related marks are trademarks of AEPG Inc. You may not use "
     "these marks without our prior written consent.</p>"),

    # 7. A newsletter about market intelligence is not a thing TwoSuns sends.
    ("privacy",
     "<li><strong>Communications:</strong> Sending service notifications, security alerts, "
     "product updates, and where you have subscribed our market intelligence newsletter</li>",
     "<li><strong>Communications:</strong> Sending service notifications, security alerts, "
     "product updates, and where you have subscribed our newsletter</li>"),

    # 8. Both pages refer to a Cookie Policy that does not exist on this site.
    ("terms",
     "<p>These Terms, together with any applicable ELA, Privacy Policy, and Cookie Policy, "
     "constitute the entire agreement",
     "<p>These Terms, together with any applicable ELA and Privacy Policy, constitute the "
     "entire agreement"),
]


def apply_fixes(which, content):
    for page, old, new in FIXES:
        if page not in ("both", which):
            continue
        n = content.count(old)
        if n != 1:
            raise SystemExit(
                "legal.py: fix for %s matched %d times, expected 1.\n  %s"
                % (which, n, old[:110]))
        content = content.replace(old, new)
    return re.sub(r"\n{3,}", "\n\n", content)


def build(src, dest, active):
    title, intro, content = extract(os.path.join(SRC, src))
    content = apply_fixes(dest.replace('.html', ''), content)
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
