"""Redirect stubs for the old preview URLs.

The site lived at twosuns.ai/preview/ for five days and those links are in
inboxes, bookmarks and open tabs. GitHub Pages has no server redirects, so each
old URL gets a small page that sends the visitor to its new home and tells
search engines where the page really is.

Query strings and fragments are carried across, which matters: every call to
action reaches discuss.html with an ?ask= parameter, and the capability groups
link into use-cases.html with a #fragment.

Run:  python3 redirects.py
"""

import os

from theme import SITE

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "preview"))

PAGES = ["index.html", "platform.html", "capabilities.html", "built-industry.html",
         "use-cases.html", "company.html", "discuss.html", "privacy.html", "terms.html"]

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
    <p>TwoSuns has moved to its own address. Taking you there now.</p>
    <a href="/%(dest)s">Continue to TwoSuns</a>
  </div>
</body>
</html>
"""


def build():
    os.makedirs(OUT, exist_ok=True)
    for p in PAGES:
        dest = "" if p == "index.html" else p
        open(os.path.join(OUT, p), "w").write(STUB % {"site": SITE, "dest": dest})
    print("wrote %d redirect stubs into preview/" % len(PAGES))


if __name__ == "__main__":
    build()
