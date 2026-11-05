# -*- coding: utf-8 -*-
"""Redirect stubs for the cement microsite pages the rebuild retires.

The old microsite had 42 pages. Eleven replace them, four of which take the same
URLs (index, platform, use-cases and events), so 38 old URLs need somewhere to
go. Those URLs are in inboxes, decks and search indexes, and GitHub Pages has no
server redirects, so each one gets a small page that sends the visitor on and
tells search engines where the content really is.

industries.html is among them: the microsite serves one industry, cement, so the
page that lists the sectors a producer sells into is called sectors.html now.

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
# A destination without a "cement/" prefix leaves the microsite for the main
# site, because the stub refreshes to /<dest>. Only send a visitor out when the
# microsite has no page that covers it: discuss, privacy and terms. Everything
# else now has a cement equivalent and stays inside /cement/.
TARGETS = {
    "cement.html": "cement/",
    "404.html": "cement/",
    "product.html": "cement/platform.html",
    "technology.html": "cement/platform.html",
    "why-twosuns.html": "cement/platform.html",
    "videos.html": "cement/platform.html",
    "how-it-works.html": "cement/platform.html",
    "trust.html": "cement/platform.html",
    "modules.html": "cement/capabilities.html",
    "solutions-contract-analytics.html": "cement/capabilities.html",
    "solutions-market-intelligence.html": "cement/capabilities.html",
    "solutions-risk-management.html": "cement/capabilities.html",
    "applications.html": "cement/use-cases.html",
    "resources.html": "cement/use-cases.html",
    "about.html": "cement/company.html",
    "careers.html": "cement/company.html",
    "press.html": "cement/company.html",
    "blog.html": "cement/company.html",
    "community.html": "discuss.html",
    "contact.html": "discuss.html",
    "engage.html": "discuss.html",
    "book-discovery.html": "discuss.html",
    "pricing.html": "discuss.html",
    "privacy.html": "privacy.html",
    "cookies.html": "privacy.html",
    "terms.html": "terms.html",
    "industries.html": "cement/sectors.html",
    "mining.html": "cement/sectors.html",
    "finance.html": "cement/sectors.html",
    # the microsite has no manufacturing sector page, the hub covers it
    "manufacturing.html": "cement/sectors.html",
    "blog/ai-ip-discipline-gap.html": "cement/company.html",
    "blog/ai-operational-intelligence-cement-decarbonization.html": "cement/platform.html",
    "blog/decision-intelligence-vs-analytics.html": "cement/platform.html",
    "blog/glassbox-ai-explainability.html": "cement/capabilities.html",
    "blog/industrial-ai-orchestrated-intelligence.html": "cement/platform.html",
    "blog/logistics-intelligence-gap.html": "cement/sectors.html",
    "blog/post-9.html": "cement/capabilities.html",
    "blog/system-decision-record.html": "cement/platform.html",
}

# Old microsite URLs that survive the rebuild, so a stub would redirect them to
# themselves. Listed so the count below can be checked against the old site.
KEPT = ["index.html", "platform.html", "events.html", "use-cases.html"]

# Everything cement.py generates. A stub written over one of these would destroy
# a real page, and the two lists are edited in different files, so assert rather
# than trust. KEPT is the subset of these that the old site also had.
PAGES = ["index.html", "context.html", "platform.html", "capabilities.html",
         "sectors.html", "construction.html", "concrete.html",
         "distribution.html", "use-cases.html", "company.html", "events.html"]

# Old URLs under cement/ar/. The Arabic microsite mirrors the English one, so a
# page that moves leaves two URLs behind, not one, and the table above only
# covers the English half. Destinations here carry the ar/ segment themselves.
AR_TARGETS = {
    "industries.html": "cement/ar/sectors.html",
}

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
    assert set(KEPT) <= set(PAGES), "KEPT lists a page cement.py does not build: %s" % (
        sorted(set(KEPT) - set(PAGES)),)
    for old, dest in sorted(TARGETS.items()):
        assert old not in PAGES, "%s is a page the rebuild generates, not a redirect" % old
        assert not dest.startswith("/"), "%s: dest is root-relative without a slash" % old
        if dest.startswith("cement/"):
            assert dest[len("cement/"):] in PAGES or dest == "cement/", (
                "%s points at %s, which the microsite does not build" % (old, dest))
        path = os.path.join(OUT, old)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w").write(STUB % {"site": SITE, "dest": dest})
    for old, dest in sorted(AR_TARGETS.items()):
        assert old not in PAGES, "%s is a page the rebuild generates, not a redirect" % old
        assert dest.startswith("cement/ar/"), "%s: an Arabic stub must stay in ar/" % old
        assert dest[len("cement/ar/"):] in PAGES, (
            "%s points at %s, which the microsite does not build" % (old, dest))
        path = os.path.join(OUT, "ar", old)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w").write(STUB % {"site": SITE, "dest": dest})
    print("wrote %d redirect stubs into cement/ and %d into cement/ar/"
          % (len(TARGETS), len(AR_TARGETS)))
    print("%d old pages accounted for (%d redirected, %d kept at the same URL)"
          % (len(TARGETS) + len(KEPT), len(TARGETS), len(KEPT)))


if __name__ == "__main__":
    build()
