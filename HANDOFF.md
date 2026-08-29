# TwoSuns website, handoff

Written 2026-08-28. Everything a fresh session needs.

## What exists right now

**twosuns.ai** serves three separate things from one repo, `twosuns-site`:

| URL | What | State |
|---|---|---|
| `twosuns.ai/` | Homepage | **Maintenance page since 2026-08-24.** The real one is saved as `index.live-backup.html` |
| `twosuns.ai/cement/` | Cement campaign microsite, 34 pages | Live, self-contained, deliberately separate |
| `twosuns.ai/preview/` | The new nine-page site | Publicly reachable, `noindex`, not linked from anywhere |

The preview is the work in progress. It is built from the **TwoSuns Website
Master Copy August 22 2026.docx**, which is the source of truth for all copy.

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

**Blocking go-live**
1. Remove `noindex` from all nine pages, or the new site is invisible.
2. Decide the maintenance page. It has been up since 24 August.
3. Privacy and Terms carry over the old market-intelligence positioning and the
   phrase "Persistent Orchestration". They need a legal pass.
4. Delete the test row from the leads Google Sheet.

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
