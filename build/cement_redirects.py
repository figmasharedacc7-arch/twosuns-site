# -*- coding: utf-8 -*-
"""Redirect stubs for the cement microsite pages the rebuild retires.

The old microsite had 42 pages. Six replace them, three of which take the same
URLs (index.html, platform.html, events.html), so 39 old URLs need somewhere to
go. Those URLs are in inboxes, decks and search indexes, and GitHub Pages has no
server redirects, so each one gets a small page that sends the visitor on and
tells search engines where the content really is.

Query strings and fragments are carried across, the same as redirects.py does
for the old /preview/ URLs.

Run:  python3 cement_redirects.py
"""

import os

from theme import SITE

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "cement"))

# Old page -> where its subject now lives. The three pages the rebuild keeps at
# the same URL are absent on purpose: the new page is the destination.
TARGETS = {
    "cement.html": "cement/",
    "404.html": "cement/",
    "product.html": "platform.html",
    "technology.html": "platform.html",
    "why-twosuns.html": "platform.html",
    "videos.html": "platform.html",
    "how-it-works.html": "cement/platform.html",
    "trust.html": "cement/platform.html",
    "modules.html": "capabilities.html",
    "solutions-contract-analytics.html": "capabilities.html",
    "solutions-market-intelligence.html": "capabilities.html",
    "solutions-risk-management.html": "capabilities.html",
    "applications.html": "use-cases.html",
    "use-cases.html": "use-cases.html",
    "resources.html": "use-cases.html",
    "about.html": "company.html",
    "careers.html": "company.html",
    "press.html": "company.html",
    "blog.html": "company.html",
    "community.html": "discuss.html",
    "contact.html": "discuss.html",
    "engage.html": "discuss.html",
    "book-discovery.html": "discuss.html",
    "pricing.html": "discuss.html",
    "privacy.html": "privacy.html",
    "cookies.html": "privacy.html",
    "terms.html": "terms.html",
    "industries.html": "industries.html",
    "mining.html": "industries.html",
    "finance.html": "industries.html",
    "manufacturing.html": "manufacturing.html",
    "blog/ai-ip-discipline-gap.html": "company.html",
    "blog/ai-operational-intelligence-cement-decarbonization.html": "cement/platform.html",
    "blog/decision-intelligence-vs-analytics.html": "platform.html",
    "blog/glassbox-ai-explainability.html": "capabilities.html",
    "blog/industrial-ai-orchestrated-intelligence.html": "platform.html",
    "blog/logistics-intelligence-gap.html": "industries.html",
    "blog/post-9.html": "capabilities.html",
    "blog/system-decision-record.html": "platform.html",
}

# These three URLs survive the rebuild, so a stub would redirect them to
# themselves. Listed so the count below can be checked against the old site.
KEPT = ["index.html", "platform.html", "events.html"]

STUB = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Moved to %(site)s/%(dest)s</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="%(site)s/%(dest)s">
<meta http-equiv="refresh" content="0; url=/%(dest)s">
<link rel="icon" type="image/svg+xml" href="/logo-mini.svg">
<style>
  *{margin:0;padding:0;box-sizing:border-box;}
  body{min-height:100vh;display:flex;align-items:center;justify-content:center;padding:32px;
    background:linear-gradient(160deg,#FFF5DD 0%%,#FFF3CD 35%%,#FCE2BC 100%%);
    font-family:'Segoe UI',system-ui,-apple-system,sans-serif;color:#3A3A3A;text-align:center;}
  .card{max-width:520px;}
  img{width:230px;max-width:70%%;height:auto;display:block;margin:0 auto 30px;}
  p{font-size:17px;line-height:1.75;color:#5A554C;margin-bottom:22px;}
  a{display:inline-block;background:linear-gradient(135deg,#E0641E,#C45213);color:#fff;
    font-weight:700;font-size:15px;padding:12px 26px;border-radius:8px;text-decoration:none;}
</style>
<script>location.replace("/%(dest)s" + location.search + location.hash);</script>
</head>
<body>
  <div class="card">
    <img src="/logo-color.svg" alt="TwoSuns">
    <p>This page has been replaced. Taking you to the page that covers it now.</p>
    <a href="/%(dest)s">Continue to TwoSuns</a>
  </div>
</body>
</html>
"""


def build():
    for old, dest in sorted(TARGETS.items()):
        assert old not in KEPT, "%s is a page the rebuild keeps, not a redirect" % old
        assert not dest.startswith("/"), "%s: dest is root-relative without a slash" % old
        path = os.path.join(OUT, old)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w").write(STUB % {"site": SITE, "dest": dest})
    print("wrote %d redirect stubs into cement/" % len(TARGETS))
    print("%d old pages accounted for (%d redirected, %d kept at the same URL)"
          % (len(TARGETS) + len(KEPT), len(TARGETS), len(KEPT)))


if __name__ == "__main__":
    build()
