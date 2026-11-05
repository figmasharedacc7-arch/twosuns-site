"""robots.txt and sitemap.xml.

The main pages plus the cement microsite, written next to them so the three
never drift apart. The cement pages come in an English and an Arabic version of
each, so every cement entry declares both as alternates of one another.

Each page is dated by its own last commit, so publishing one page does not
claim the other twelve changed today. The date on the command line is the
fallback for a page git has not seen yet, which is how a new page gets dated
the first time it ships.

Run:  python3 sitemap.py YYYY-MM-DD
"""

import os
import subprocess
import sys

from theme import SITE

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))

# page, change frequency, priority
PAGES = [
    ("",                     "weekly",  "1.0"),
    ("platform.html",        "monthly", "0.9"),
    ("capabilities.html",    "monthly", "0.9"),
    ("industries.html",       "monthly", "0.9"),
    ("use-cases.html",       "monthly", "0.9"),
    ("company.html",         "monthly", "0.7"),
    ("events.html",          "weekly",  "0.7"),
    ("building-materials.html", "monthly", "0.8"),
    ("construction.html",     "monthly", "0.8"),
    ("manufacturing.html",    "monthly", "0.8"),
    ("discuss.html",         "monthly", "0.8"),
    ("privacy.html",         "yearly",  "0.2"),
    ("terms.html",           "yearly",  "0.2"),
]

# cement microsite: page under /cement/, change frequency, priority. Each one
# is published in English and in Arabic, so each produces two sitemap entries.
CEMENT = [
    ("",                  "monthly", "0.8"),
    ("platform.html",     "monthly", "0.8"),
    ("capabilities.html", "monthly", "0.8"),
    ("sectors.html",      "monthly", "0.7"),
    ("construction.html", "monthly", "0.6"),
    ("concrete.html",     "monthly", "0.6"),
    ("distribution.html", "monthly", "0.6"),
    ("use-cases.html",    "monthly", "0.7"),
    ("company.html",      "monthly", "0.6"),
    ("events.html",       "weekly",  "0.7"),
]

ROBOTS = """User-agent: *
Allow: /

Sitemap: %s/sitemap.xml
""" % SITE


def modified(rel, stamp):
    """Last commit date for a file, or the given stamp if git has no record."""
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", rel],
                             cwd=ROOT, capture_output=True, text=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        return stamp
    return out.stdout.strip() or stamp


def url(loc, stamp, freq, pri, alts=()):
    out = ["  <url>",
           "    <loc>%s</loc>" % loc,
           "    <lastmod>%s</lastmod>" % stamp,
           "    <changefreq>%s</changefreq>" % freq,
           "    <priority>%s</priority>" % pri]
    for lang, href in alts:
        out.append('    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>'
                   % (lang, href))
    out.append("  </url>")
    return out


def build(stamp):
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
           '        xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for page, freq, pri in PAGES:
        when = modified(page or "index.html", stamp)
        out += url("%s/%s" % (SITE, page), when, freq, pri)
    for page, freq, pri in CEMENT:
        en = "%s/cement/%s" % (SITE, page)
        ar = "%s/cement/ar/%s" % (SITE, page)
        alts = (("en", en), ("ar", ar), ("x-default", en))
        out += url(en, modified("cement/" + (page or "index.html"), stamp),
                   freq, pri, alts)
        out += url(ar, modified("cement/ar/" + (page or "index.html"), stamp),
                   freq, pri, alts)
    out.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w").write("\n".join(out) + "\n")
    open(os.path.join(ROOT, "robots.txt"), "w").write(ROBOTS)
    print("sitemap.xml  %d urls (%d main, %d cement), lastmod %s"
          % (len(PAGES) + 2 * len(CEMENT), len(PAGES), 2 * len(CEMENT), stamp))
    print("robots.txt   allow all, sitemap declared")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("usage: python3 sitemap.py YYYY-MM-DD")
    build(sys.argv[1])
