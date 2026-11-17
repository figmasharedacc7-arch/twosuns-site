# TwoSuns website, handoff

Written 2026-08-28. Everything a fresh session needs.

## In flight, 2026-11-16

Two commits sit on main. The first is pushed and live, the second is not.

**`14b750c`, pushed and live.** "No line left standing on its own". One rule
in `theme.CSS`, `text-wrap:balance` on headings, ledes, subs, paragraphs, list
items, definition rows and captions. It cleared all 205 one and two word
orphan last lines across the 35 content pages, and no page changed height by a
pixel. `pretty` was tried first and only rescues single word last lines, which
left 125 standing, so it was replaced.

**`d3466bb`, committed, NOT pushed. This is the one to ship.** Every video
re-cut from its master. Resolutions and bitrates are in the commit message.
Headlines: nothing is upscaled, CRF 28 with a ceiling picked off a measured
sweep, hero-build goes 1920 to 2560 for a third of a megabyte, and the main
site finally lazy-loads its bands, so total video weight goes 12.7 MB to
31.3 MB while the home page's first load goes 6.2 MB down to 3.4 MB.

To ship it:

```bash
cd ~/Documents/Claude/twosuns-live && git push origin main
```

Then confirm the Pages run for `d3466bb` reports completed/success at
`https://api.github.com/repos/figmasharedacc7-arch/twosuns-site/actions/runs?per_page=3`.

**Where the masters are, if anything needs recutting.** All in `~/Downloads`.

| clip | master | cut |
|---|---|---|
| hero-build | apartment-construction-site-at-golden-sunset | t=0.0, 15.9s, ungraded, `BASE` in herovid.py |
| hero-crane | building-construction-crane-sunset-industrial-arch | t=6.0, herovid.py |
| hero-rise | aerial-shot-of-a-new-high-rise-building-under-cons | t=1.0, herovid.py |
| vid-work | 561Z_11_hand_upload.mov, 4K ProRes | t=0.0, 12.92s, bandvid.py |
| vid-aerial | aerial-view-of-a-large-cement-plant-and-industrial | t=1.0, 14.0s, bandvid.py |
| vid-port | hong-kong-container-port-terminal | 7.12s master, forward then back |
| band-dusk, band-works | named in cementvid.py's own PLAN | unchanged cuts |
| mixer-truck | `animated-flat-design-cement-mixer-truck-driving...zip`, which holds `concrete-mixing-truck.mov`, ProRes 4444 with alpha | unchanged crop |

**Two traps worth keeping.** `cementfig.py` takes its source as an argument
and names it nowhere, and there is a second, wrong file in Downloads called
`3d-animated-cement-mixer-truck-with-construction-w...mov` which is also
ProRes 4444 and is a different truck entirely. It was used by mistake once and
had to be restored from git. The right one is the flat design zip above.
`cementfig.py` also used to place its ground line in raw pixels against a
1110x612 frame; it now holds the position as a fraction, or the line draws
through the wheels the moment the output grows.

**Verifying video lazy-load needs a rendered page.** The browser pane does not
render when its window is closed, and an unrendered page never fires an
IntersectionObserver or a requestAnimationFrame, so the bands look broken when
they are fine. Use headless Chrome and vary the window height:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --user-data-dir=/tmp/cud --window-size=1440,4200 --virtual-time-budget=9000 --dump-dom http://127.0.0.1:8777/index.html | grep -o '<video[^>]*vid-[^>]*>'
```

At 1440x900 the bands must stay unattached, at 1440x4200 both home bands
attach, and platform's attaches by 7000px where it actually sits.

**Parked, not started, at the owner's instruction.** `research/arch-reference/
workshop-architecture-reference.html`, copied out of Downloads on 2026-11-16.
The owner likes the platform architecture design in it and wants it considered
for the site after the videos land. That is the next thing to pick up.

**Still unreferenced, still not deleted.** `cement/band-plant.mp4` is a byte
identical copy of `vid-aerial.mp4`'s old version and `cement/cement-plant.mp4`
is linked from nowhere. About 1.5 MB between them. Flagged, never authorised.

**Careful with build.py.** `OUT` on line 24 is an absolute path to the live
tree, so running it from any copy of the repo writes into the live site. Run
it only from `twosuns-live/build`. Checked on 2026-11-16: it regenerates the
root pages faithfully, so it is safe there.

## What exists right now

**twosuns.ai** serves three separate things from one repo, `twosuns-site`:

| URL | What | State |
|---|---|---|
| `twosuns.ai/` | The nine-page site | **Launched 2026-08-29.** Indexable, canonical, sitemap declared |
| `twosuns.ai/cement/` | Cement campaign microsite, 34 pages | Live, self-contained, deliberately separate |
| `twosuns.ai/contact.html` | Old contact form | Kept only because eight cement pages link to it |
| `twosuns.ai/preview/*` | The old preview URLs | Redirect stubs to the root pages, carrying query and fragment |

The site is built from the **TwoSuns Website Master Copy August 22 2026.docx**,
which is the source of truth for all copy. `preview/` now holds only
`incoming/`, the image originals the build reads from. The maintenance page and
`index.live-backup.html` are gone from the served root; git history has both.

## The single most important thing

**The pages under `preview/` are generated.** Editing them by hand is thrown
away on the next rebuild. Source and instructions are in `build/README.md`.

## Decisions already made, do not relitigate

- **Coordination, not orchestration.** The August master copy reversed an
  earlier decree. The preview says coordination throughout. `/cement/` still
  says orchestration and stays that way.
- **The Company page names all 20 people**, reversing a July privacy scrub.
  Confirmed spellings: **Raihaan Mohammad**, **Kalpesh Bathella**. Two people
  have first names only, AbdelAziz and AbdelRahmen.
- **`/cement/` is untouched.** "Keep the cement microsite separate."
- **No em dashes anywhere.** Commas instead. CEO rule.
- **Palette is locked** to orange `#E0641E`, gold `#CC9900`, black on cream. A
  functional-palette proposal exists at `preview/built-industry-alt.html` and
  `preview/use-cases-alt.html`, awaiting the CEO's call.
- **Built Industry uses full-bleed photo sections**, chosen over cards.
- **The hero rotates three clips**, 7.5s each with a 1.4s crossfade. Only the
  first loads eagerly. See `build/README.md` under Hero clips.
- The architecture layout follows Aiman's deck: Horizon and Pulse flanking Core
  in a white disc, Ray spanning beneath.
- An animated product-visual pilot for the architecture section was **built and
  rejected**. Do not rebuild it unprompted.

## Open items

**Open after launch**
1. Privacy and Terms still describe a commodity, energy and financial market
   intelligence product, with trading disclaimers, watchlists and a "Persistent
   Orchestration" trademark. They are wrong for this company and need replacing.
2. Delete the test row from the leads Google Sheet.

**Content still needed**
5. `fam-pulse.jpg`, Capabilities. The current one is a whiteboard of stock
   placeholder labels; cropping the text out left it nearly blank. Search terms
   are in `preview/incoming/SEARCH.md`.
6. Real headshots for the 20 people on Company. A photographer, not stock. Do
   not generate AI portraits of named real people.
7. Optional: an adaptive-reuse photo for Home's "Enterprise software is
   evolving".

**Offered, never approved**
8. A role and industry selector on Home that routes to pre-filtered Use Cases.
9. A mega menu. Animated counters on true numbers only.
10. Cross-document view transitions and hover prefetch.

## How the user works

- Wants to **see** things. Render and show, don't describe.
- Preview first, publish only on an explicit go-ahead. The preview URL is the
  working surface.
- Says "publish" or "push" when they want production.
- Corrects tersely. "looks crooked", "the shift section is empty". Investigate
  before assuming it is taste, several of those were real bugs.

## Bugs that already bit, do not repeat

- **Deleting a CSS block by cutting between comment markers.** Wiped the
  lifecycle diagram styles. `build.py` now refuses to write a page missing any
  of fifteen required blocks.
- **Pasting CSS into `theme.py` instead of referencing the module.** Editing
  the source then changed nothing. Reveal CSS and eclipse CSS are now pulled
  live.
- **Specificity.** `.rv details.acc` at 0-2-1 outranked `.rv .in` at 0-2-0, so
  elements got the reveal class and stayed invisible. The visible rule is now
  doubled to `.in.in`.
- **`position:relative` on `.hero-glow`** pulled a 620px decorative element
  into flow and doubled the hero height.
- **Headless screenshots misreport mobile.** Use `probe.mjs`, which drives real
  device emulation over CDP.
- **Sizing a decorative circle as a percentage of its column** made it 420px
  against a 215px band and it swallowed the heading.

## Verify before every push

```bash
cd twosuns-live/build && python3 build.py && python3 legal.py
# then, with headless Chrome on port 9333:
node probe.mjs 9333 1440 900 file://…/preview/index.html
node probe.mjs 9333 390 900 file://…/preview/index.html
node sweep.mjs 9333 file://…/preview <scratch dir>
```

Check: div and section balance, no missing assets, no em dashes, no horizontal
overflow at 1440 / 768 / 390, nothing left invisible by the reveals.

## People

Aiman El-Ramly, CEO. Michelle Mollineaux, Marketing Director. Ryan Arian, Chief
Digital Product Officer, owns pilot.twosuns.ai. Kalpesh Bathella advises on IT
and owns mail. DNS changes are coordinated with Ryan and Kalpesh.
