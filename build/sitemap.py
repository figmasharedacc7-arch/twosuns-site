"""robots.txt and sitemap.xml.

Nine pages, written next to them so the two never drift apart. The cement
microsite keeps its own life and is listed but not rebuilt here.

Run:  python3 sitemap.py YYYY-MM-DD
"""

import os
import sys

from theme import SITE

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))

# page, change frequency, priority
PAGES = [
    ("",                     "weekly",  "1.0"),
    ("platform.html",        "monthly", "0.9"),
    ("capabilities.html",    "monthly", "0.9"),
    ("built-industry.html",  "monthly", "0.9"),
    ("use-cases.html",       "monthly", "0.9"),
    ("company.html",         "monthly", "0.7"),
    ("events.html",          "weekly",  "0.7"),
    ("discuss.html",         "monthly", "0.8"),
    ("privacy.html",         "yearly",  "0.2"),
    ("terms.html",           "yearly",  "0.2"),
]

ROBOTS = """User-agent: *
Allow: /

Sitemap: %s/sitemap.xml
""" % SITE


def build(stamp):
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for page, freq, pri in PAGES:
        out.append("  <url>")
        out.append("    <loc>%s/%s</loc>" % (SITE, page))
        out.append("    <lastmod>%s</lastmod>" % stamp)
        out.append("    <changefreq>%s</changefreq>" % freq)
        out.append("    <priority>%s</priority>" % pri)
        out.append("  </url>")
    out.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w").write("\n".join(out) + "\n")
    open(os.path.join(ROOT, "robots.txt"), "w").write(ROBOTS)
    print("sitemap.xml  %d urls, lastmod %s" % (len(PAGES), stamp))
    print("robots.txt   allow all, sitemap declared")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("usage: python3 sitemap.py YYYY-MM-DD")
    build(sys.argv[1])
