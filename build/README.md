# TwoSuns site build

The nine pages under `../preview/` are **generated**. Do not hand-edit them, a
rebuild overwrites everything. Edit the source here and rebuild.

## Rebuild

```bash
cd /Users/mohammaddidarulalam/Documents/Claude/twosuns-live/build
python3 build.py        # the seven content pages
python3 legal.py        # privacy.html and terms.html, ported from the old site
```

`build.py` refuses to write a page missing any of fifteen required stylesheet
blocks, so a lost CSS block fails loudly instead of shipping an unstyled page.

## What each file owns

| File | Owns |
|---|---|
| `theme.py` | The whole stylesheet, the nav, the footer, the particle canvas |
| `content.py` | Home, Platform, Capabilities copy |
| `content2.py` | Built Industry, Use Cases, Company, Discuss copy, plus the filter and cross-link tables |
| `build.py` | Page assembly, `OUT` points at `../preview` |
| `eclipse.py` | The lifecycle diagram, its own CSS and SVG geometry |
| `herorot.py` | The hero clip rotation, its own CSS and script |
| `herovid.py` | Cuts and colour matches the hero clips from the Envato originals |
| `reveal.py` | Scroll reveals, its own CSS and scripts |
| `legal.py` | Reads Privacy and Terms out of `nexsun/` and reskins them |
| `sideaware.py` | Turns originals in `../preview/incoming/` into the cropped, graded files the pages use |
| `process_images.py` | Simpler image prep, superseded by `sideaware.py` for backgrounds |
| `palette_alt.py`, `palette_alt2.py` | The two palette comparison pages |
| `lab.py`, `compare.py` | Scratch comparison pages, safe to delete |

**All copy comes from `TwoSuns Website Master Copy August 22 2026.docx`.** Every
line was diffed against it. Do not paraphrase when editing.

## Images

Originals live in `../preview/incoming/` and are gitignored. `sideaware.py`
crops each one so its subject lands on the side the copy leaves visible,
mirrors where needed, and grades cool sources into the warm palette. Its `PLAN`
list is the whole configuration: name, which side the photo bleeds from, where
the subject sits as a fraction of width, whether to mirror, a brightness lift,
and a vertical anchor.

Adding an image: drop the original in `incoming/`, add a `PLAN` row, run
`python3 sideaware.py`, then `python3 build.py`.

## Hero clips

The hero cycles through `hero-build.mp4`, `hero-crane.mp4` and `hero-rise.mp4`,
7.5 seconds each with a 1.4 second crossfade. `herovid.py` cuts the last two
from the Envato originals in `~/Downloads`; it encodes each one twice, measuring
its mean channel levels after the first pass and applying the gain that lands it
on `hero-build.mp4`, so the three read as one continuous piece of footage rather
than three stock clips. Change `PLAN` and `HERO_CLIPS` in `build.py` to swap a
clip.

`hero-build.mp4` was cut from `apartment-construction-site-at-golden-sunset`.
Do not take a second window from that source for the rotation, it reads as the
hero stuttering. A frame comparison is the quick way to tell: the same source
scores about 1.4 mean difference per channel, an unrelated one about 35.

Only the first clip is in the document with a source. The others carry
`data-src` and are attached once the page is idle, so the rotation costs nothing
on first paint.

## Checking work

The `.mjs` files drive headless Chrome over the DevTools protocol. Start Chrome
first:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --remote-debugging-port=9333 \
  --user-data-dir=/tmp/cdp-profile about:blank &
```

Then:

- `probe.mjs 9333 <width> <height> file://…/page.html` — real device-emulated
  layout check. Reports horizontal overflow and whether the mobile nav is
  correct. **Headless screenshots lie about mobile, this does not.**
- `sweep.mjs 9333 file://…/preview <dir>` — every page at five scroll positions,
  looking for anything on screen still invisible.
- `fullpage.mjs` — full-length page captures.

Always run `probe.mjs` at 1440, 768 and 390 before pushing a layout change.
