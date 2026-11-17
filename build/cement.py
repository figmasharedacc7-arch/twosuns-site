# -*- coding: utf-8 -*-
"""Render the TwoSuns cement microsite, English and Arabic.

Three pages per language, generated from cement_copy.py in the twosuns.ai
theme. English at /cement/, Arabic at /cement/ar/. Assets are referenced
from the site root so both depths resolve.
"""
import os, sys, html, json, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import arch
import process
import theme
import reveal
import teamgrid
import content2
from cement_copy import LANGS

OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "cement"))
SITE = "https://twosuns.ai"
BASE = "/cement/"
DISCUSS = "https://twosuns.ai/discuss.html"
# registration for the evening, exactly as the printed invitation gives it
EVENTBRITE = ("https://www.eventbrite.com/e/"
              "ai-cement-presentation-reception-tickets-2004099361138"
              "?aff=oddtdtcreator")


def e(s):
    return html.escape(s, quote=False)


# Arabic CTA labels resolve back to their English counterpart, because
# discuss.html is English and renders ?ask= verbatim as a chip. Values that
# are the same in both languages are excluded, so the lookup cannot misfire.
_EN_VALUES = set(v for v in LANGS["en"].values() if isinstance(v, str))
AR_TO_EN = dict((v, LANGS["en"][k]) for k, v in LANGS["ar"].items()
                if isinstance(v, str) and isinstance(LANGS["en"].get(k), str)
                and v != LANGS["en"][k] and v not in _EN_VALUES)


def ask(label):
    """CTA target. An Arabic label sends its English equivalent so the English
    form shows a chip it can render, plus a marker recording the Arabic origin."""
    en = AR_TO_EN.get(label)
    if en is None:
        return DISCUSS + "?ask=" + urllib.parse.quote_plus(label)
    return DISCUSS + "?ask=" + urllib.parse.quote_plus(en) + "&amp;lang=ar"


def btn(label, href=None, ghost=False, new_tab=False):
    cls = "btn-ghost" if ghost else "btn-cta"
    out = ' target="_blank" rel="noopener"' if new_tab else ""
    return ('<a class="%s" href="%s"%s>%s</a>'
            % (cls, href or ask(label), out, e(label)))


# --------------------------------------------------------------- microsite CSS
CEM_CSS = r"""
  /* ---- microsite chrome ---- */
  .cmnav{position:sticky;top:0;z-index:100;background:rgba(255,248,236,.95);
    backdrop-filter:blur(16px);border-bottom:1px solid rgba(224,100,30,.15);
    box-shadow:0 1px 20px rgba(224,100,30,.08);}
  .cmnav-in{max-width:1240px;margin:0 auto;padding:0 32px;display:flex;align-items:center;
    height:70px;gap:26px;}
  .cmnav-in a.brand img{height:46px;width:auto;display:block;}
  .cmlinks{display:flex;align-items:center;gap:24px;margin-inline-start:auto;}
  .cmlinks a{font-size:14px;font-weight:600;color:var(--ink);white-space:nowrap;transition:color .2s;}
  .cmlinks a:hover,.cmlinks a.active{color:var(--sun-deep);}
  .cmlang{display:inline-flex;align-items:center;gap:9px;font-size:13px;font-weight:700;
    padding-inline:14px;border-inline:1px solid rgba(140,101,0,.22);}
  .cmlang .on{color:var(--sun-deep);}
  .cmlang a{color:var(--text-muted);}
  .cmtoggle{display:none;margin-inline-start:auto;background:none;border:0;font-size:24px;
    color:var(--navy);cursor:pointer;line-height:1;}
  .cmskip{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);
    white-space:nowrap;inset-inline-start:12px;top:10px;}
  .cmskip:focus{width:auto;height:auto;overflow:visible;clip-path:none;z-index:200;
    background:#fff;padding:8px 14px;border-radius:8px;border:2px solid var(--sun);}

  /* ---- hero with the washed plant photo ---- */
  /* Hero. The photograph and the wash over it are two custom properties, so a
     page only swaps the image and the right to left flip is written once:
     redefining --cmwash under html[dir="rtl"] re-angles every hero together.
     The wash is the main site's, opaque cream under the words and clear over
     the photograph, so a cement page reads as the same site. Paths are rooted
     because the microsite sits one level down and the Arabic two. */
  .cmhero{position:relative;overflow:hidden;padding:104px 0 90px;
    --cmshot:url('/cement/cement-banner.jpg');
    --cmwash:linear-gradient(100deg,#FFF6E2 0%,#FFF6E2 40%,rgba(255,246,226,.94) 48%,
      rgba(255,246,226,.74) 56%,rgba(255,245,222,.44) 64%,rgba(255,244,218,.16) 72%,
      rgba(255,243,216,0) 80%);
    background-image:var(--cmwash),var(--cmshot);
    background-size:cover,cover;background-repeat:no-repeat;
    background-position:center,center 30%;}
  html[dir="rtl"] .cmhero{--cmwash:linear-gradient(260deg,#FFF6E2 0%,#FFF6E2 40%,rgba(255,246,226,.94) 48%,
      rgba(255,246,226,.74) 56%,rgba(255,245,222,.44) 64%,rgba(255,244,218,.16) 72%,
      rgba(255,243,216,0) 80%);}
  /* Supplied for this page: a works in desert, which suits a page about Egypt
     better than the flat band it replaces. Cropped, and its sky graded warm,
     in the file rather than here: every other hero is cream and gold, and a
     deep blue band across the top read as a different site. */
  .cmhero.sh-context{--cmshot:url('/cement/context-hero.jpg');}
  .cmhero.sh-capabilities{--cmshot:url('/cement/cap-hero.jpg');}
  /* the Sectors hub takes the supplied plant aerial, flipped, so its tower
     stands in the half the wash leaves clear */
  .cmhero.sh-aerial{--cmshot:url('/cement/plant-aerial.jpg');}
  .cmhero.sh-construction{--cmshot:url('/cons-hero.jpg');}
  .cmhero.sh-concrete{--cmshot:url('/bm-concrete.jpg');}
  .cmhero.sh-distribution{--cmshot:url('/bm-distribution.jpg');}
  .cmhero.sh-usecases{--cmshot:url('/uc-hero.jpg');}
  .cmhero.sh-company{--cmshot:url('/company-hero.jpg');}
  .cmhero.sh-events{--cmshot:url('/events-hero.jpg');}
  /* ---- a hero that plays ----
     The photograph stays the section's background and the clip sits in a
     layer over it, with the wash lifted on top of both. The wash is a
     background layer on .cmhero itself, so a video child would otherwise
     paint over the very gradient that keeps the copy readable. The overlay
     takes var(--cmwash) rather than restating the gradient, so the right to
     left flip, which redefines that one property, re-angles this along with
     every other hero on the site.
     The poster and the clip's first frame are the same picture, and the
     object-position here is the background-position above, so nothing shifts
     when the loop attaches. */
  .cmhero.has-v>.cmhero-v{position:absolute;inset:0;z-index:0;}
  .cmhero.has-v>.cmhero-v video{display:block;width:100%;height:100%;
    object-fit:cover;object-position:center 30%;}
  .cmhero.has-v>.cmhero-v::after{content:"";position:absolute;inset:0;
    background:var(--cmwash);}
  /* The wash covers the start half and clears by 80 percent, so whatever the
     picture is of has to stand in the far strip. The still heroes solve that
     by flipping the file, which is what sh-aerial does and says so; one clip
     cannot ship twice, so the Arabic page mirrors it here instead and its
     tower stands in the half that wash leaves clear. */
  html[dir="rtl"] .cmhero.has-v>.cmhero-v video{transform:scaleX(-1);}
  .cmhero h1{font-size:clamp(32px,4.4vw,54px);font-weight:900;line-height:1.1;color:var(--navy);
    margin-bottom:20px;max-width:19ch;}
  .cmhero p.hero-sub{max-width:620px;}

  /* ---- Cement Context: the regional pressure card ---- */
  /* Three stacked blocks in one card: what the pressure is, how it reaches the
     plant, and the scenario it becomes. The scenario block is tinted and pushed
     to the bottom with margin-top:auto, so the three cards line their scenarios
     up however unevenly the middle block fills. */
  .cmpr{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:32px;
    align-items:stretch;}
  .cmpr>*{min-width:0;}
  .cmpr .p{background:#fff;border:1px solid var(--border);border-radius:16px;
    box-shadow:var(--shadow);overflow:hidden;display:flex;flex-direction:column;}
  .cmpr .p-top{padding:24px 24px 18px;}
  .cmpr .n{width:40px;height:40px;border-radius:50%;background:var(--sun);color:#fff;
    font-weight:900;font-size:14px;display:inline-flex;align-items:center;
    justify-content:center;margin-bottom:14px;}
  .cmpr .p-top h3{font-size:19px;font-weight:900;color:var(--navy);line-height:1.3;}
  .cmpr .p-top p{font-size:14.5px;color:var(--text-muted);line-height:1.6;margin-top:9px;}
  .cmpr .p-mid{padding:18px 24px;border-top:1px solid var(--border-soft);}
  .cmpr .k{display:block;font-size:11.5px;font-weight:800;letter-spacing:1.3px;
    text-transform:uppercase;color:#8C6500;}
  /* The pairs are spaced with margins rather than a grid gap. A gap applies
     between dt and dd as well as between pairs, which puts more air inside a
     pair than around it and reads as though each description belongs to the
     label below it. */
  .cmpr dl{margin-top:11px;}
  .cmpr dt{font-size:14px;font-weight:800;color:var(--navy);margin-top:13px;}
  .cmpr dt:first-child{margin-top:0;}
  .cmpr dd{font-size:14px;color:var(--text-muted);line-height:1.6;margin-top:2px;}
  .cmpr .p-end{padding:18px 24px 20px;margin-top:auto;background:var(--bg2);
    border-top:1px solid var(--border);}
  .cmpr .p-end .k{color:var(--sun-deep);}
  .cmpr .p-end p{font-size:14.5px;line-height:1.6;color:var(--navy);font-weight:600;
    margin-top:8px;}
  .cmpr .mods{display:flex;flex-wrap:wrap;gap:4px 12px;margin-top:12px;}
  .cmpr .mods span{font-size:13px;font-weight:700;color:var(--sun-deep);}
  html[dir="rtl"] .cmpr .k{letter-spacing:0;}

  /* ---- Cement Context: the workflow group ---- */
  /* A labelled group of numbered workflows, two to a row. The label sits on a
     rule that runs to the end of the row, which is why the heading is a flex
     with a growing pseudo element rather than a border on the group. */
  .cmfl{margin-top:30px;}
  .cmfl+.cmfl{margin-top:34px;}
  /* the label is a pill on a rule that runs to the end of the row, so the two
     groups read as two bands rather than as one long list */
  .cmfl>h3{display:flex;align-items:center;gap:14px;font-size:11.5px;font-weight:800;
    letter-spacing:1.6px;text-transform:uppercase;color:var(--sun-deep);margin-bottom:6px;}
  .cmfl>h3 b{font-weight:800;border:1px solid var(--border);border-radius:999px;
    padding:6px 14px;background:var(--bg2);}
  .cmfl>h3::after{content:"";flex:1;height:1px;background:var(--border);}
  html[dir="rtl"] .cmfl>h3{letter-spacing:0;}
  html[dir="rtl"] .cmrail .run,html[dir="rtl"] .cmrail .l{letter-spacing:0;}
  .cmfl .g{display:grid;grid-template-columns:repeat(2,1fr);gap:0 34px;}
  .cmfl .g>*{min-width:0;}
  .cmfl .w{display:grid;grid-template-columns:auto 1fr;gap:0 14px;align-items:start;
    padding:18px 0;border-bottom:1px solid var(--border-soft);}
  .cmfl .n{width:26px;height:26px;border-radius:50%;border:1px solid var(--sun);
    color:var(--sun-deep);font-size:12px;font-weight:800;display:inline-flex;
    align-items:center;justify-content:center;margin-top:1px;}
  .cmfl .w h4{font-size:16px;font-weight:900;color:var(--navy);line-height:1.35;}
  .cmfl .w p{font-size:14px;color:var(--text-muted);line-height:1.6;margin-top:7px;}
  .cmfl .mods{display:flex;flex-wrap:wrap;gap:3px 12px;margin-top:9px;}
  .cmfl .mods span{font-size:13px;font-weight:700;color:var(--sun-deep);}

  /* ---- platform family cards ---- */
  .cmfam{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:30px;}
  .cmfam>*{min-width:0;}
  .cmfam .f{background:#fff;border:1px solid var(--border);border-radius:16px;padding:24px 22px;
    box-shadow:var(--shadow);border-top:4px solid var(--sun);transition:all .3s;}
  .cmfam .f:nth-child(2){border-top-color:var(--gold);}
  .cmfam .f:nth-child(3){border-top-color:var(--sun-deep);}
  .cmfam .f:nth-child(4){border-top-color:var(--a4);}
  .cmfam .f:hover{transform:translateY(-5px);box-shadow:0 12px 40px rgba(224,100,30,.14);}
  .cmfam h3{font-size:19px;font-weight:800;color:var(--navy);margin-bottom:8px;}
  .cmfam .d{font-size:14.5px;color:var(--text-muted);line-height:1.65;margin-bottom:10px;}
  .cmfam .x{font-size:13px;color:#8C6500;line-height:1.6;font-weight:600;
    border-top:1px solid var(--border-soft);padding-top:10px;}

  /* ---- labelled rows: configuration, governance ---- */
  .cmrows{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:28px;}
  .cmrows>*{min-width:0;}
  .cmrows .r{background:#fff;border:1px solid var(--border-soft);border-radius:14px;
    padding:20px 22px;box-shadow:var(--shadow);font-size:14.5px;color:var(--text-muted);
    line-height:1.68;}
  .cmrows .r b{display:block;color:var(--navy);font-weight:800;margin-bottom:5px;font-size:15px;}
  .cmrows.two{grid-template-columns:repeat(2,1fr);}

  /* ---- architecture tiers ---- */
  .cmtier{background:#fff;border:1px solid var(--border);border-radius:20px;padding:26px 28px;
    box-shadow:var(--shadow);margin-top:18px;}
  .cmtier-h{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;margin-bottom:6px;}
  .cmtier-n{font-size:12px;font-weight:900;color:var(--sun-deep);letter-spacing:2px;}
  .cmtier-k{font-size:11.5px;font-weight:800;letter-spacing:2px;text-transform:uppercase;
    color:var(--navy);}
  .cmtier-a{font-size:11.5px;font-weight:700;color:#8C6500;margin-inline-start:auto;
    background:var(--gold-soft);border-radius:20px;padding:3px 12px;}
  .cmtier-who{font-size:13.5px;color:var(--text-muted);margin-bottom:14px;line-height:1.6;}
  .cmchips{display:flex;flex-wrap:wrap;gap:9px;}
  .cmchips li{list-style:none;background:var(--bg2);border:1px solid var(--border-soft);
    border-radius:9px;padding:9px 14px;font-size:13.5px;font-weight:700;color:var(--navy);}
  /* The nine shared facilities wrap to eight and one on a desktop row, and the
     one left behind reads as an accident. Three equal columns divide nine
     exactly and line up with the three module columns above it. Under 820px the
     pills wrap again, where they sit two and three to a row and none is
     stranded. */
  @media(min-width:820px){
    .cmchips.g{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));}
    .cmchips.g li{display:flex;align-items:center;justify-content:center;
      text-align:center;}
  }
  .cmnote{font-size:13px;color:var(--text-muted);margin-top:14px;line-height:1.65;font-style:italic;}

  /* THE CUSTOMER'S MIXER, in the empty column beside the panel on the concrete
     page. The clip is composited onto the flat cream this section paints, so it
     carries no card and no border: what shows is the truck standing on the page.
     It is a figure with a caption, not a mascot, because the copy on this page
     says tanker seven times and never says mixer: the caption is what makes the
     difference between the producer's vehicle and the customer's legible. */
  .cncgap{display:grid;grid-template-columns:minmax(0,760px) minmax(0,1fr);
    gap:30px;align-items:center;}
  .cncmix{margin:22px 0 0;}
  .cncmix video,.cncmix img{display:block;width:100%;height:auto;}
  /* the clip faces left, into the panel. In Arabic the panel is on the other
     side, so the truck turns with it, the same mirror .prc svg takes. */
  html[dir="rtl"] .cncmix video,html[dir="rtl"] .cncmix img{transform:scaleX(-1);}
  .cncmix figcaption{margin-top:8px;font-size:13.5px;line-height:1.55;font-weight:600;
    color:var(--text-muted);max-width:40ch;}
  /* the still is the same frame the loop opens on, so a reader who has asked
     for no motion gets the same truck, parked, and loses nothing */
  .cncmix img{display:none;}
  @media(prefers-reduced-motion:reduce){
    .cncmix video{display:none;}
    .cncmix img{display:block;}
  }
  /* The gutter never gets wider than this. .container caps at 1240 box and
     1176 inside it, so with a 760 panel and a 30 gap the figure column is
     pinned at 386px from 1240 up, and below 1240 it only shrinks: 346 at 1200,
     266 at 1120, 227 at 1081. The first version broke at 1080, which put the
     truck at its smallest in the 1081 to 1200 band and made crossing the
     breakpoint upward shrink it from 520 to 227. Breaking where the column
     stops being full size instead means the step is 520 to 386 and the
     starved band does not exist. */
  @media(max-width:1239px){
    .cncgap{grid-template-columns:minmax(0,1fr);gap:0;}
    .cncmix{max-width:520px;}
    .cmfig{max-width:520px;margin-top:26px;}
  }
  /* ---- a photograph beside the copy, where a band cannot go ---- */
  /* The home page's about section runs the four card family grid under its
     ledes, and .cmfam has no narrowed form inside .imgsec, so a photo band
     would squeeze those cards into a quarter of the 682px copy column. The
     picture takes the gutter .cncgap already leaves beside a 760 column
     instead, and the grid keeps the full measure below it.
     This borrows the mixer truck's layout and deliberately not its figure
     class: .cncmix hides its <img> until reduced motion, because there the
     still is only the loop's stand-in, and mirrors it for Arabic, because a
     composited vehicle should face into the copy. Both are wrong for a
     photograph, which always shows and is never mirrored on this site.
     The box is .cmst .ph: same 3:2, same radius, same warm veil, so a picture
     beside type reads the same here as it does on the capabilities rows. */
  .cmfig{position:relative;overflow:hidden;border-radius:16px;aspect-ratio:3/2;
    margin:0;background:var(--gold-soft);box-shadow:var(--shadow);}
  .cmfig img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
    display:block;}
  .cmfig::after{content:"";position:absolute;inset:0;
    background:linear-gradient(180deg,rgba(224,100,30,.06),rgba(255,246,226,.16));}
  .cmmods{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;margin-top:4px;}
  .cmmods>*{min-width:0;}
  .cmmod{border:1px solid var(--border-soft);border-radius:14px;padding:18px 18px 20px;
    background:linear-gradient(170deg,#FFFBF0,#FFF6E4);}
  .cmmod.core{background:linear-gradient(170deg,#FEF6DA,#FBE9BE);border-color:rgba(204,153,0,.3);}
  .cmmod h3{font-size:17px;font-weight:900;color:var(--navy);margin-bottom:2px;}
  .cmmod .d{font-size:12.5px;color:#8C6500;font-weight:700;margin-bottom:12px;}
  .cmmod ul{list-style:none;}
  .cmmod li{font-size:13.5px;color:var(--text-muted);line-height:1.5;padding:6px 0;
    border-top:1px solid rgba(140,101,0,.12);}
  .cmmod li:first-child{border-top:0;}
  .cmray{display:flex;align-items:center;gap:12px;background:linear-gradient(135deg,var(--sun),var(--sun-deep));
    color:#fff;border-radius:12px;padding:13px 20px;font-weight:800;font-size:15px;margin-bottom:14px;}
  .cmunits{margin-top:22px;background:var(--gold-soft);border:1px solid rgba(140,101,0,.25);
    border-radius:12px;padding:16px 20px;font-size:13.5px;color:#7A5A08;line-height:1.7;}

  /* ---- inputs table ---- */
  .cmtblw{margin-top:26px;overflow-x:auto;border:1px solid var(--border);border-radius:16px;
    box-shadow:var(--shadow);background:#fff;}
  .cmtblw:focus-visible{outline:3px solid var(--sun);outline-offset:2px;}
  .cmtbl{width:100%;border-collapse:collapse;min-width:720px;}
  .cmtbl th{text-align:start;font-size:11px;font-weight:800;letter-spacing:1.6px;
    text-transform:uppercase;color:#8C6500;background:var(--gold-soft);padding:13px 18px;
    border-bottom:1px solid rgba(140,101,0,.22);}
  .cmtbl td{text-align:start;font-size:14px;color:var(--text-muted);padding:14px 18px;
    border-bottom:1px solid var(--border-soft);line-height:1.6;vertical-align:top;}
  .cmtbl tr:last-child td{border-bottom:0;}
  .cmtbl td:first-child{font-weight:700;color:var(--navy);}
  .cmtbl tr:hover td{background:rgba(255,246,226,.7);}

  /* ---- events ---- */
  .cmev{background:#fff;border:1px solid var(--border);border-radius:20px;padding:28px 30px;
    box-shadow:var(--shadow);margin-top:20px;}
  .cmev-when{font-size:13px;font-weight:800;color:#8C6500;letter-spacing:.4px;margin-bottom:8px;}
  .cmev h3{font-size:clamp(19px,2.2vw,25px);font-weight:800;color:var(--navy);line-height:1.25;
    margin-bottom:10px;}
  .cmev p{font-size:15px;color:var(--text-muted);line-height:1.72;}
  .cmev .acts{display:flex;flex-wrap:wrap;gap:12px;margin-top:20px;}
  .cmev.feat{border:1px solid rgba(224,100,30,.4);
    background:linear-gradient(165deg,#FFFBF0 0%,#FEF3DA 100%);}
  .cmbadge{display:inline-block;background:var(--navy);color:#FFD9A8;font-size:10.5px;
    font-weight:800;letter-spacing:1.6px;text-transform:uppercase;padding:5px 14px;
    border-radius:20px;margin-bottom:14px;}
  .cmses{display:grid;grid-template-columns:96px 1fr;gap:0;background:#fff;
    border:1px solid var(--border-soft);border-radius:18px;overflow:hidden;
    box-shadow:var(--shadow);margin-top:18px;}
  .cmses-d{background:linear-gradient(150deg,var(--sun),var(--sun-deep));color:#fff;
    display:flex;flex-direction:column;align-items:center;justify-content:center;padding:20px 8px;}
  .cmses-d .dd{font-size:32px;font-weight:900;line-height:1;}
  .cmses-d .mm{font-size:12px;font-weight:800;letter-spacing:2px;text-transform:uppercase;margin-top:4px;}
  .cmses-b{padding:22px 26px;}
  .cmmeta{display:flex;flex-wrap:wrap;gap:8px 18px;margin-top:14px;font-size:13.5px;
    color:var(--text-muted);font-weight:600;}
  .cmmeta span{display:inline-flex;align-items:center;gap:7px;}
  .cmmeta span::before{content:'';width:6px;height:6px;border-radius:50%;background:var(--sun);flex-shrink:0;}

  /* ---- agenda ---- */
  .cmag{margin-top:22px;border:1px solid var(--border);border-radius:18px;overflow:hidden;
    background:#fff;box-shadow:var(--shadow);}
  .cmag-r{display:grid;grid-template-columns:148px 1fr;gap:0;
    border-bottom:1px solid var(--border-soft);}
  .cmag-r:last-child{border-bottom:0;}
  .cmag-t{padding:16px 18px;font-size:13.5px;font-weight:800;color:#8C6500;
    background:rgba(255,246,226,.75);border-inline-end:1px solid var(--border-soft);}
  .cmag-b{padding:16px 22px;}
  .cmag-b h3{font-size:15.5px;font-weight:800;color:var(--navy);margin-bottom:3px;
    display:flex;align-items:center;gap:10px;flex-wrap:wrap;}
  .split2-panel h3{font-size:11px;font-weight:800;letter-spacing:2px;text-transform:uppercase;
    color:#8C6500;margin-bottom:14px;}
  html[dir="rtl"] .split2-panel h3{letter-spacing:0;}
  .cmag-k{font-size:9.5px;font-weight:800;letter-spacing:1.4px;text-transform:uppercase;
    color:var(--sun-deep);border:1px solid rgba(224,100,30,.4);border-radius:20px;padding:2px 9px;}
  .cmag-b p{font-size:13.5px;color:var(--text-muted);line-height:1.6;}
  .cmag-b ul{list-style:none;margin-top:7px;}
  .cmag-b li{font-size:13px;color:var(--text-muted);padding-inline-start:14px;position:relative;
    line-height:1.6;}
  .cmag-b li::before{content:'';position:absolute;inset-inline-start:0;top:9px;width:5px;height:5px;
    border-radius:50%;background:var(--gold);}

  /* ---- practical details ---- */
  .cmpd{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:26px;}
  .cmpd>*{min-width:0;}
  .cmpd .p{background:#fff;border:1px solid var(--border-soft);border-radius:14px;padding:18px 20px;
    box-shadow:var(--shadow);}
  .cmpd .k{font-size:10.5px;font-weight:800;letter-spacing:1.6px;text-transform:uppercase;
    color:#8C6500;margin-bottom:6px;}
  .cmpd .v{font-size:14px;color:var(--navy);font-weight:700;line-height:1.55;}

  /* ---- past events ---- */
  .cmpast{list-style:none;margin-top:24px;display:grid;gap:12px;}
  .cmpast li{background:rgba(255,255,255,.72);border:1px solid var(--border-soft);
    border-radius:12px;padding:15px 20px;font-size:14.5px;color:var(--text-muted);}
  .cmpast b{color:var(--navy);font-weight:800;}

  /* ---- microsite footer ---- */
  .cmfoot{background:var(--bg);border-top:3px solid var(--sun);padding:48px 0 28px;
    position:relative;z-index:2;}
  .cmfoot-top{display:flex;flex-wrap:wrap;gap:26px;align-items:flex-start;justify-content:space-between;}
  .cmfoot-brand img{height:42px;margin-bottom:10px;display:block;}
  .cmfoot-brand .by{font-size:12.5px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;
    color:#8C6500;}
  .cmfoot-brand .cn{font-size:13.5px;color:var(--text-muted);margin-top:8px;line-height:1.7;}
  .cmfoot-links{display:flex;flex-wrap:wrap;gap:8px 20px;align-items:center;}
  .cmfoot-links a{font-size:14px;font-weight:600;color:var(--text-muted);}
  .cmfoot-links a:hover{color:var(--sun-deep);}
  .cmfoot-bot{margin-top:28px;padding-top:18px;border-top:1px solid var(--border-soft);
    display:flex;flex-wrap:wrap;gap:10px 20px;justify-content:space-between;font-size:13px;
    color:var(--text-muted);}

  /* sector cards and workflow cards. Two grids added for the pages that mirror
     the main site. They reuse the card tokens above so a new page cannot drift
     from the shipped ones. */

  /* ---- Capabilities: the family run rail and its stations ---- */
  /* The six groups in a family are positions in a run, not six interchangeable
     boxes, so each family opens on a dark rail naming the run and its six stops
     and the groups below are wide rows. Twelve identical cards in two grids was
     the page, and it was the page the owner called box after box.
     A row carries a photograph only where one exists that shows that work. Most
     do not yet, and a frame filled because a slot wanted filling is worse than
     no frame, so a row without a picture is simply full width. */
  .cmrail{margin-top:26px;border-radius:18px;padding:26px 30px 30px;color:#F6EEDE;
    background:linear-gradient(140deg,#2A2520,#171310);}
  .cmrail .run{font-size:16.5px;font-weight:800;line-height:1.35;color:#fff;
    letter-spacing:.04em;text-transform:uppercase;}
  .cmrail .track{position:relative;display:grid;grid-template-columns:repeat(6,minmax(0,1fr));
    margin-top:22px;}
  /* the thread behind the stops, inset so it begins and ends inside the first
     and last number rather than running off the ends of the rail */
  .cmrail .track::before{content:"";position:absolute;inset-inline:8%;top:14px;
    height:1px;background:rgba(224,178,80,.45);}
  .cmrail a{position:relative;text-align:center;text-decoration:none;}
  .cmrail .n{width:30px;height:30px;margin:0 auto;border-radius:50%;background:#2A2520;
    border:1px solid rgba(224,178,80,.55);color:var(--gold);font-size:11.5px;
    font-weight:800;display:flex;align-items:center;justify-content:center;
    transition:background .25s,border-color .25s,color .25s;}
  .cmrail .l{margin-top:9px;font-size:11.5px;font-weight:800;line-height:1.25;
    color:#F6EEDE;letter-spacing:.1em;text-transform:uppercase;transition:color .25s;}
  /* the glyph darkens rather than turning white: white on --sun is 3.49:1 at
     11.5px, and the hovered or focused stop is the one being read */
  .cmrail a:hover .n,.cmrail a:focus-visible .n{background:var(--sun);
    border-color:var(--sun);color:#2A2520;}
  .cmrail a:hover .l,.cmrail a:focus-visible .l{color:var(--gold);}

  .cmsts{margin-top:30px;}
  /* without a picture the row runs the full measure, title and descriptor in a
     rail at the start so a reader scanning names has one column to run down */
  .cmst{display:grid;grid-template-columns:340px 1fr;gap:14px 36px;padding:30px 0;
    border-top:1px solid rgba(204,153,0,.30);scroll-margin-top:90px;}
  .cmst:first-child{border-top:0;padding-top:8px;}
  .cmst:focus{outline:none;}
  .cmst>*{min-width:0;}
  .cmst.shot{grid-template-columns:5fr 7fr;gap:36px;align-items:center;}
  .cmst .ph{position:relative;overflow:hidden;border-radius:16px;aspect-ratio:3/2;
    background:var(--gold-soft);box-shadow:var(--shadow);}
  .cmst .ph img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;}
  /* the warm veil the hero wash already puts over a photograph, so a picture
     joins the page rather than sitting on top of it */
  .cmst .ph::after{content:"";position:absolute;inset:0;
    background:linear-gradient(180deg,rgba(224,100,30,.06),rgba(255,246,226,.16));}
  .cmst .n{width:38px;height:38px;border-radius:50%;color:#fff;font-size:14px;
    font-weight:900;display:flex;align-items:center;justify-content:center;flex:none;
    background:linear-gradient(135deg,var(--sun),var(--sun-deep));}
  /* on a picture row the ordinal sits on the picture, otherwise it leads the name */
  .cmst.shot .n{position:absolute;z-index:2;top:14px;inset-inline-start:14px;
    box-shadow:0 4px 14px rgba(60,50,30,.35);}
  .cmst h3{font-size:19px;font-weight:900;color:var(--navy);line-height:1.3;}
  .cmst.shot h3{font-size:21px;line-height:1.25;}
  .cmst .d{font-size:13.5px;font-weight:700;color:var(--sun-deep);line-height:1.55;
    margin-top:9px;}
  /* the ordinal leads the name on a plain row, on the same line, because it
     numbers that name and because stacking it cost a phone 50px a row */
  .cmst .hd{display:flex;align-items:center;gap:12px;}
  .cmst .hd .n{width:30px;height:30px;font-size:12px;}
  .cmst .tick{columns:2;column-gap:32px;}
  .cmst.shot .tick{margin-top:16px;column-gap:28px;}
  .cmst .tick li{break-inside:avoid;margin-bottom:9px;}
  /* a picture sits at the start of an odd row and at the end of an even one, so
     the side follows the station's number in the family, not the order of the
     pictures: two pictures on 01 and 03 both sit at the start. grid order does
     the flip, so the DOM keeps picture before text for a screen reader, and
     Arabic mirrors the whole rhythm without a rule of its own. */
  .cmst.shot:nth-child(even){grid-template-columns:7fr 5fr;}
  .cmst.shot:nth-child(even) .ph{order:2;}
  .cmst.shot:nth-child(even) .bd{order:1;}

  .cmsx{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:28px;}
  .cmsx>*{min-width:0;}
  .cmsx .s{background:#fff;border:1px solid var(--border-soft);border-radius:14px;
    padding:22px 22px 18px;box-shadow:var(--shadow);display:flex;flex-direction:column;}
  .cmsx .s h3{font-size:17px;font-weight:900;color:var(--navy);margin-bottom:8px;}
  .cmsx .s p{font-size:14px;color:var(--text-muted);line-height:1.65;margin-bottom:12px;}
  .cmsx .s ul{list-style:none;margin-bottom:16px;}
  .cmsx .s li{font-size:13.5px;color:var(--text-muted);line-height:1.5;padding:6px 0;
    border-top:1px solid rgba(140,101,0,.12);}
  .cmsx .s li:first-child{border-top:0;}
  .cmsx .s .go{margin-top:auto;font-size:13.5px;font-weight:800;color:var(--sun-deep);
    text-decoration:none;}
  .cmsx .s .go:hover{text-decoration:underline;}

  .cmwf{display:grid;grid-template-columns:repeat(2,1fr);gap:16px;margin-top:26px;}
  .cmwf>*{min-width:0;}
  .cmwf .w{background:#fff;border:1px solid var(--border-soft);border-radius:14px;
    padding:20px 22px;box-shadow:var(--shadow);}
  .cmwf .w h3{font-size:16px;font-weight:900;color:var(--navy);margin-bottom:12px;}
  .cmwf .w dl{display:grid;grid-template-columns:auto 1fr;gap:6px 12px;}
  .cmwf .w dt{font-size:11.5px;font-weight:800;color:#8C6500;text-transform:uppercase;
    letter-spacing:.6px;padding-top:2px;}
  .cmwf .w dd{font-size:13.5px;color:var(--text-muted);line-height:1.55;}
  html[dir="rtl"] .cmwf .w dt{letter-spacing:0;}

  /* ---- photo band, the main site's .imgsec laid over a whole section ---- */
  /* theme.CSS gives .imgsec its wash and its 58% copy column but names each
     photograph in a class whose url is relative, so from /cement/ it resolves to
     a file that is not there. The section carries its own rooted url in --cmband
     instead, which needs no class per picture and works from /cement/ar/ too. */
  .imgsec::before{background-image:var(--cmband);}
  /* A band whose photograph moves. The loop sits at the same depth as the still,
     under the same wash, so a band that plays and a band that does not read as
     the same device. ::before keeps the photograph, which makes it the poster:
     it is what shows while the file loads, if the browser refuses to autoplay,
     and for a reader who has asked for no motion. The loop is decoration behind
     the copy, so it is aria-hidden and out of the tab order, exactly as a CSS
     background photograph already is.
     Tree order does the layering: ::before and .cmband-v are both at -2, so the
     pseudo paints first and the loop lands on top of it, and ::after at -1 puts
     the wash over both. */
  .imgsec>.cmband-v{position:absolute;inset:0;z-index:-2;overflow:hidden;}
  .imgsec>.cmband-v video{width:100%;height:100%;display:block;object-fit:cover;}
  /* the loop keeps the half of the frame its still kept. A photograph is never
     mirrored for Arabic, it is repositioned, the same thing ::before does. */
  .imgsec-r>.cmband-v video{object-position:right center;}
  .imgsec-l>.cmband-v video{object-position:left center;}
  html[dir="rtl"] .imgsec-r>.cmband-v video{object-position:left center;}
  html[dir="rtl"] .imgsec-l>.cmband-v video{object-position:right center;}
  /* belt and braces: the script never attaches a loop under reduced motion, so
     there is normally nothing here to hide. This covers the loop already
     playing when a reader changes the setting mid-visit. */
  @media(prefers-reduced-motion:reduce){.imgsec>.cmband-v{display:none;}}

  /* Every loop on this microsite starts by itself, runs longer than five
     seconds and sits beside the copy, which is the case WCAG 2.2.2 asks to be
     pausable. The control is small and quiet because the motion it governs is
     too. It is written by script rather than into the markup, because without
     script nothing moves and there would be nothing for it to pause. */
  .cmpause{position:absolute;right:14px;bottom:14px;z-index:2;width:30px;height:30px;
    border-radius:50%;border:1px solid rgba(42,37,32,.18);cursor:pointer;padding:0;
    background:rgba(255,246,226,.82);display:grid;place-items:center;
    -webkit-backdrop-filter:blur(3px);backdrop-filter:blur(3px);}
  .cmpause:hover{background:#FFF6E2;border-color:rgba(42,37,32,.34);}
  .cmpause:focus-visible{outline:2px solid var(--sun-deep);outline-offset:2px;}
  html[dir="rtl"] .cmpause{right:auto;left:14px;}
  /* two bars for pause, one triangle for play, drawn in borders so they keep
     their weight beside the type rather than riding on a font */
  .cmpause-i{width:9px;height:10px;box-sizing:border-box;
    border-left:3px solid var(--navy);border-right:3px solid var(--navy);}
  .cmpause.is-off .cmpause-i{width:0;height:0;border:0;
    border-left:9px solid var(--navy);
    border-top:5px solid transparent;border-bottom:5px solid transparent;}
  /* on the truck the control would land on the caption, so it takes the empty
     cream above the cab instead */
  .cncmix{position:relative;}
  .cncmix .cmpause{bottom:auto;top:10px;}
  /* the copy column is a little over half the width, so the grids inside a band
     drop a column earlier than they do in a full width section */
  .imgsec .cmsx,.imgsec .cmrows.two{grid-template-columns:1fr;}
  @media(min-width:1180px){.imgsec .cmrows.two{grid-template-columns:repeat(2,1fr);}}
  @media(min-width:1200px){.cmst:not(.shot) .tick{columns:3;column-gap:30px;}}
  /* between the chip breakpoint and about 705 the longest stop, MAINTENANCE,
     is wider than a sixth of the rail and pushes its neighbours off the beat */
  @media(max-width:760px){.cmrail .l{font-size:10.5px;letter-spacing:.04em;}}

  @media(max-width:1000px){
    .cmhero,html[dir="rtl"] .cmhero{background-position:center,center;
      --cmwash:linear-gradient(175deg,rgba(255,246,226,.95) 0%,rgba(255,246,226,.89) 55%,
        rgba(255,244,220,.58) 80%,rgba(255,242,214,.24) 100%);}
    /* the wash is vertical here and symmetric, so there is no clear half to
       carry the tower into and the mirror would only disagree with the still */
    .cmhero.has-v>.cmhero-v video,
    html[dir="rtl"] .cmhero.has-v>.cmhero-v video{object-position:center;
      transform:none;}
    .cmfam,.cmrows,.cmrows.two,.cmmods,.cmpr{grid-template-columns:repeat(2,1fr);}
    .cmpd{grid-template-columns:repeat(2,1fr);}
    .cmsx{grid-template-columns:1fr;}
  }
  @media(max-width:820px){
    .cmtoggle{display:block;}
    .cmlinks{display:none;position:absolute;top:70px;inset-inline:0;background:rgba(255,250,240,.99);
      flex-direction:column;align-items:stretch;gap:0;padding:10px 24px 18px;
      border-bottom:1px solid var(--border);box-shadow:0 14px 30px rgba(60,50,30,.14);}
    .cmlinks.open{display:flex;}
    .cmlinks a{padding:11px 0;}
    .cmlang{border-inline:0;padding-inline:0;border-top:1px solid var(--border-soft);
      padding-top:10px;margin-top:4px;}
  }
  @media(max-width:620px){
    .cmfam,.cmrows,.cmrows.two,.cmmods,.cmpd{grid-template-columns:1fr;}
    .cmwf,.cmpr,.cmfl .g{grid-template-columns:1fr;}
    /* a station stacks, picture above its text, and the stops wrap */
    .cmst,.cmst.shot,.cmst.shot:nth-child(even){grid-template-columns:1fr;gap:18px;}
    .cmst.shot:nth-child(even) .ph{order:0;}
    .cmst.shot:nth-child(even) .bd{order:0;}
    .cmst .tick{columns:1;}
    .cmst{padding:24px 0;}
    /* stops as inline chips: a number over a label twice over costs 270px of a
       phone screen, and the rail is a jump index, not a diagram */
    .cmrail{padding:20px 20px 22px;}
    .cmrail .track{display:flex;flex-wrap:wrap;gap:18px 10px;margin-top:16px;}
    .cmrail a{display:flex;align-items:center;gap:7px;text-align:start;}
    .cmrail .n{width:24px;height:24px;font-size:10.5px;margin:0;}
    .cmrail .l{margin-top:0;font-size:11px;letter-spacing:.06em;}
    .cmrail .track::before{display:none;}
    .cmwf .w dl{grid-template-columns:1fr;gap:2px;}
    .cmwf .w dd{margin-bottom:8px;}
    .cmag-r,.cmses{grid-template-columns:1fr;}
    .cmag-t{border-inline-end:0;border-bottom:1px solid var(--border-soft);}
    .cmses-d{flex-direction:row;gap:10px;padding:12px;}
    .cmhero{padding:72px 0 62px;}
  }

  /* ---- vertical rhythm between sections ---- */
  /* Measured on the rendered home page at 1340, the empty band between the end
     of one section and the start of the next ran 184px where two plain sections
     meet, 168 and 170 where a plain section meets a photograph band, and 152
     between the two bands. That is theme.py's 92px of section padding counted
     twice, plus area-sec's 76 twice. It reads as a pause between pages rather
     than a join between sections. These take the same four gaps to 132, 122,
     122 and 112, which is still an unambiguous break and about 190px off the
     home page.
     Scope. This sits in CEM_CSS, so it reaches the twenty microsite pages and
     nothing else. build/theme.py keeps 92 for the main site, which was not part
     of the request, and theme.py cannot be edited from here anyway without
     running build.py over the live root pages.
     The media query is not optional. theme.py drops section to 64px under
     760px, and it does so EARLIER in the cascade than this file, so the base
     rule below would otherwise override it and make the phone looser than it
     is today rather than tighter. */
  section{padding:66px 0;}
  .area-sec{padding:56px 0;}
  @media(max-width:760px){
    section{padding:48px 0;}
    .area-sec{padding:44px 0;}
  }
"""

# The capability map. Adapted from the workshop deck's architecture diagram,
# which laid the three tiers against one numbered spine instead of stacking
# three separate cards, and made every module expand in place.
#
# Two things in it were changed rather than copied.
#
# Colour. The deck put the input tiles and the shared facilities on a slate
# blue, #2F5D8A on #FBFCFD with #123A63 text. That is a fourth hue and the site
# is locked to the logo's orange, gold and black on cream, so those surfaces
# are rebuilt here as white cards on the deck hairline, which is also what the
# variant above does to every other card field on the microsite. The two module
# columns keep their tint: it is not decoration there, it is the one thing the
# diagram exists to say, which of the two operating domains a module belongs
# to, and the gold and the orange carrying it are the brand's own.
#
# Contrast. Three colours came off the deck below AA and are corrected here.
# The Horizon heading was #CC9900 on white, 2.6:1 against the 3:1 that 26px
# bold needs, and is --dk-gold #8C6500 at 5.3:1; Pulse follows it to --dk-acc
# #C45213 at 4.6:1 rather than stay bright on its own, which left the pair
# looking mismatched. The gold expander badge was #8C6500 on #F3E3A6 at 4.1:1
# and is --dk-gold-deep #7A5A08 at 5.0:1. The tier numerals were #B9B2A6 at
# 2.1:1 and are #9A8F7E at 3.2:1. The bright gold and orange stay, on the 4px
# module rails and the two connector lines, where nothing is read off them.
#
# Class names are all cma-. The deck's own names collide with this site: .mods
# is already the module tag row on the pressures and the workflows, .core is
# the middle card of the old three, and .n, .k, .d and .go are each used by
# several unrelated blocks. A prefix is cheaper than scoping every one.
CMA_CSS = r"""
  .cma{background:#fff;border:1px solid var(--border);border-radius:22px;
    box-shadow:var(--shadow-lg);padding:34px;margin-top:36px;text-align:start;
    display:grid;gap:30px;}
  .cma-row{display:grid;grid-template-columns:170px minmax(0,1fr);gap:24px;
    align-items:start;}
  .cma-row>*{min-width:0;}
  .cma-lab .cma-n{display:block;font-size:34px;font-weight:300;color:#9A8F7E;
    line-height:1;}
  .cma-lab b{display:block;font-size:13px;font-weight:800;letter-spacing:1.2px;
    text-transform:uppercase;color:var(--navy);margin-top:8px;line-height:1.35;}
  .cma-lab small{display:block;font-size:12.5px;color:var(--text-muted);
    margin-top:4px;line-height:1.5;}
  .cma-cap{font-size:13.5px;color:var(--text-muted);line-height:1.6;}

  /* ---- every module opens in place ---- */
  /* <details>, so this needs no script, survives a page print, and opens when
     the browser's own find-in-page lands inside one. The name is in the
     summary, so the closed diagram is still a complete list to a reader, a
     crawler and a screen reader, and the description is in the DOM either way. */
  .cma summary{list-style:none;cursor:pointer;}
  .cma summary::-webkit-details-marker{display:none;}
  .cma details>summary::after{content:"+";flex:0 0 auto;width:20px;height:20px;
    border-radius:50%;display:inline-flex;align-items:center;
    justify-content:center;font-size:15px;font-weight:700;line-height:1;
    transition:transform .2s;}
  .cma details[open]>summary::after{transform:rotate(45deg);}

  /* ---- 01 administration and inputs ---- */
  .cma-admin{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;
    margin-block:12px;align-items:stretch;}
  /* The five tiles are one row of equal weight, so they take one height
     between them rather than each sizing to its own name. "DCS Historian and
     Customer Data" runs to three lines and left the other four looking
     clipped. */
  .cma-tile{background:#fff;border:1px solid var(--dk-acc-line);
    border-radius:10px;min-width:0;display:flex;flex-direction:column;}
  .cma-tile>summary{display:flex;flex:1;align-items:center;
    justify-content:center;gap:8px;padding:11px 12px;text-align:center;
    font-size:14px;color:var(--navy);font-weight:600;line-height:1.35;}
  .cma-tile>summary::after{background:var(--dk-gold-pale);
    color:var(--dk-gold-deep);font-size:13px;width:18px;height:18px;}
  .cma-tile>p{padding:0 14px 12px;font-size:12.5px;line-height:1.55;
    color:var(--text-muted);text-align:center;}
  .cma-tile[open]{background:#FBF3E4;}

  /* ---- 02 the two module columns either side of Core ---- */
  /* The connectors are drawn outwards from the middle of the grid, half the
     Core's own width plus the gap, so each one meets the dark panel exactly.
     Logical properties, so the Arabic page draws them from the other side
     without a second rule. */
  .cma-grid{display:grid;grid-template-columns:minmax(0,1fr) 230px minmax(0,1fr);
    gap:30px;align-items:stretch;position:relative;}
  .cma-grid::before,.cma-grid::after{content:"";position:absolute;top:50%;
    height:2px;width:30px;}
  .cma-grid::before{background:var(--gold);inset-inline-start:calc(50% - 145px);}
  .cma-grid::after{background:var(--sun);inset-inline-start:calc(50% + 115px);}
  .cma-colh{display:flex;justify-content:space-between;align-items:flex-end;
    gap:10px;margin-bottom:12px;}
  .cma-colh h3{font-size:26px;font-weight:900;letter-spacing:.5px;line-height:1;}
  .cma-colh span{display:block;font-size:13.5px;color:var(--text-muted);
    margin-top:5px;line-height:1.4;}
  .cma-colh em{font-style:normal;font-size:12.5px;color:var(--text-muted);
    white-space:nowrap;}
  .cma-hz .cma-colh h3{color:var(--dk-gold);}
  .cma-pl .cma-colh h3{color:var(--dk-acc);}
  .cma-list{display:grid;gap:8px;}
  .cma-mi{border-radius:8px;font-size:15px;color:var(--navy);
    transition:box-shadow .15s;}
  .cma-mi>summary{display:flex;align-items:center;justify-content:space-between;
    gap:10px;padding:10px 14px;line-height:1.4;}
  .cma-mi>p{padding:0 14px 12px;font-size:13.5px;line-height:1.55;
    color:var(--text-muted);}
  .cma-mi[open]{box-shadow:0 8px 20px rgba(60,50,30,.10);}
  .cma-hz .cma-mi{background:#FFFBEF;border:1px solid #F3E3A6;
    border-inline-start:4px solid var(--gold);}
  .cma-hz .cma-mi>summary::after{background:#F3E3A6;color:var(--dk-gold-deep);}
  .cma-hz .cma-mi[open]{background:var(--dk-gold-pale);}
  .cma-pl .cma-mi{background:#FFF8F2;border:1px solid #F8D9C2;
    border-inline-start:4px solid var(--sun);}
  .cma-pl .cma-mi>summary::after{background:#F8D9C2;color:var(--dk-acc-deep);}
  .cma-pl .cma-mi[open]{background:var(--dk-acc-pale);}
  .cma-go{display:inline-flex;align-items:center;gap:7px;margin-top:13px;
    font-size:13px;font-weight:800;color:var(--dk-acc-deep);}
  .cma-go:hover{color:var(--dk-acc);}
  .cma-go:focus-visible{outline:2px solid var(--dk-acc-deep);outline-offset:4px;
    border-radius:4px;}
  .cma-arrow{font-size:14px;line-height:1;transition:transform .18s ease;}
  .cma-go:hover .cma-arrow{transform:translateY(2px);}

    /* Core runs the full height of the taller column rather than sitting at its
     own size, because it is the one thing both columns attach to and a short
     panel floating between them reads as a third, smaller module. Its content
     is centred inside that height, where the two connectors meet it. */
  .cma-core{background:var(--dk-navy);color:#fff;border-radius:16px;
    padding:26px 18px;display:flex;flex-direction:column;align-items:center;
    justify-content:center;text-align:center;
    box-shadow:0 18px 44px rgba(30,26,20,.25);position:relative;min-width:0;}
  .cma-core h3{font-size:30px;font-weight:900;letter-spacing:1px;color:#fff;}
  .cma-core .cma-k{color:#E3B21C;font-size:15px;margin-top:4px;
    padding-bottom:16px;border-bottom:1px solid rgba(255,255,255,.18);
    width:100%;line-height:1.35;}
  .cma-core ul{list-style:none;margin-top:14px;display:grid;gap:9px;width:100%;}
  .cma-ci>summary{display:flex;align-items:center;justify-content:center;gap:8px;
    color:#fff;font-size:15.5px;line-height:1.35;}
  .cma-ci>summary::after{background:rgba(255,255,255,.12);color:#E3B21C;
    font-size:13px;width:18px;height:18px;}
  .cma-ci>p{margin-top:6px;font-size:12.5px;line-height:1.5;color:#CFC6B6;
    padding:0 4px;}
  .cma-ci[open]>summary{color:#E3B21C;}

  /* ---- 03 shared facilities ---- */
  .cma-ray{display:flex;align-items:center;gap:12px;
    background:linear-gradient(135deg,var(--sun),var(--sun-deep));color:#fff;
    border-radius:12px;padding:13px 20px;font-weight:800;font-size:15px;
    margin-bottom:14px;}
  .cma-shared{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;
    align-items:start;}
  .cma-sf{background:#fff;border:1px solid var(--dk-acc-line);border-radius:12px;
    min-width:0;}
  .cma-sf>summary{display:flex;align-items:center;justify-content:space-between;
    gap:10px;padding:13px 16px;font-size:15px;font-weight:700;color:var(--navy);
    line-height:1.3;}
  .cma-sf>summary::after{background:var(--dk-gold-pale);
    color:var(--dk-gold-deep);}
  .cma-sf>span{display:block;padding:0 16px 13px;font-size:13px;
    color:var(--text-muted);line-height:1.45;}
  .cma-sf[open]{background:#FBF3E4;box-shadow:0 8px 20px rgba(60,50,30,.08);}

  .cma-foot{border-top:1px solid var(--border);padding-top:16px;font-size:13.5px;
    color:var(--text-muted);line-height:1.7;}

  /* Arabic sets no letter-spacing: it separates the joined letterforms. */
  html[lang="ar"] .cma-lab b{letter-spacing:0;font-size:14px;}
  html[lang="ar"] .cma-core h3,html[lang="ar"] .cma-colh h3{letter-spacing:0;}

  /* The spine folds above its row, the three columns stack with Core still in
     the middle, and the connectors go: stacked, they would be drawing a
     relationship the layout no longer shows. */
  @media(max-width:980px){
    .cma{padding:22px;}
    .cma-row{grid-template-columns:1fr;gap:14px;}
    .cma-lab{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;}
    .cma-lab .cma-n{font-size:22px;}
    .cma-lab b{margin-top:0;}
    .cma-lab small{margin-inline-start:auto;margin-top:0;}
    .cma-grid{grid-template-columns:1fr;gap:18px;}
    .cma-grid::before,.cma-grid::after{display:none;}
    .cma-admin{grid-template-columns:repeat(2,minmax(0,1fr));}
    .cma-shared{grid-template-columns:repeat(2,minmax(0,1fr));}
  }
  @media(max-width:620px){
    .cma-admin,.cma-shared{grid-template-columns:1fr;}
    .cma-colh{flex-wrap:wrap;align-items:baseline;}
    .cma-foot{font-size:12.5px;}
  }
  @media(prefers-reduced-motion:reduce){
    .cma details>summary::after,.cma-arrow{transition:none;}
    .cma-go:hover .cma-arrow{transform:none;}
  }
"""

# the theme stylesheet is authored left to right, so mirror what it hard-codes
RTL_CSS = r"""
  html[dir="rtl"] .tick li{padding-left:0;padding-right:22px;}
  html[dir="rtl"] .tick li::before{left:auto;right:0;}
  html[dir="rtl"] .step{padding:20px 68px 20px 22px;}
  html[dir="rtl"] .step::before{left:auto;right:22px;}
  html[dir="rtl"] .split2-panel::after{right:auto;left:-50px;}
  html[dir="rtl"] .hero-glow{right:auto;left:-90px;}
  html[dir="rtl"] .btn-cta,html[dir="rtl"] .btn-ghost{letter-spacing:0;}
  html[dir="rtl"] .section-tag,html[dir="rtl"] .hero-eyebrow,
  html[dir="rtl"] .cmtier-k,html[dir="rtl"] .cmpd .k,html[dir="rtl"] .cmtbl th,
  html[dir="rtl"] .cmbadge,html[dir="rtl"] .cmag-k,html[dir="rtl"] .cmfoot-brand .by,
  html[dir="rtl"] .cmses-d .mm,html[dir="rtl"] .cmtier-n{letter-spacing:0;}
  html[dir="rtl"] body{font-family:'Segoe UI','Noto Sans Arabic','Geeza Pro',Tahoma,
    system-ui,-apple-system,sans-serif;}
  /* .imgsec is authored left to right: the photograph keeps one half of the
     frame and the wash covers the other, where the copy sits. Mirror the pair,
     or the Arabic copy lands on the photograph. The narrow screen wash has to be
     restated because these selectors outrank the theme's own media query. */
  html[dir="rtl"] .imgsec-r::before{background-position:left center;}
  html[dir="rtl"] .imgsec-l::before{background-position:right center;}
  html[dir="rtl"] .imgsec-r::after{background:linear-gradient(260deg,#FFF6E2 0%,#FFF6E2 44%,rgba(255,246,226,.97) 53%,rgba(255,246,226,.86) 62%,
    rgba(255,245,222,.58) 72%,rgba(255,244,218,.26) 85%,rgba(255,243,216,.05) 100%);}
  html[dir="rtl"] .imgsec-l::after{background:linear-gradient(100deg,#FFF6E2 0%,#FFF6E2 44%,rgba(255,246,226,.97) 53%,rgba(255,246,226,.86) 62%,
    rgba(255,245,222,.58) 72%,rgba(255,244,218,.26) 85%,rgba(255,243,216,.05) 100%);}
  html[dir="rtl"] .imgsec-l .sec-split{margin-left:0;margin-right:auto;}

  /* A band composed for one side cannot be mirrored for Arabic. The still
     bands can be: their subject sits near the middle of the frame, so moving
     the photograph across is enough, which is what the rules above do. A band
     whose crop deliberately carried its subject out into the clear quarter has
     nothing in the other half to show, and those rules would swing the picture
     onto the empty side and leave an Arabic reader a band of sky. The tower on
     the context page did exactly that. So a band with a loop keeps the side it
     was composed for and the copy column moves instead, which for Arabic puts
     the copy at the reading start anyway. */
  html[dir="rtl"] .imgsec-keep.imgsec-r::before{background-position:right center;}
  html[dir="rtl"] .imgsec-keep.imgsec-l::before{background-position:left center;}
  html[dir="rtl"] .imgsec-keep.imgsec-r>.cmband-v video{object-position:right center;}
  html[dir="rtl"] .imgsec-keep.imgsec-l>.cmband-v video{object-position:left center;}
  html[dir="rtl"] .imgsec-keep.imgsec-r::after{background:linear-gradient(100deg,#FFF6E2 0%,#FFF6E2 44%,rgba(255,246,226,.97) 53%,rgba(255,246,226,.86) 62%,rgba(255,245,222,.58) 72%,rgba(255,244,218,.26) 85%,rgba(255,243,216,.05) 100%);}
  html[dir="rtl"] .imgsec-keep.imgsec-l::after{background:linear-gradient(260deg,#FFF6E2 0%,#FFF6E2 44%,rgba(255,246,226,.97) 53%,rgba(255,246,226,.86) 62%,rgba(255,245,222,.58) 72%,rgba(255,244,218,.26) 85%,rgba(255,243,216,.05) 100%);}
  html[dir="rtl"] .imgsec-keep.imgsec-r .sec-split{margin-left:0;margin-right:auto;}
  html[dir="rtl"] .imgsec-keep.imgsec-l .sec-split{margin-left:auto;margin-right:0;}
  @media(max-width:1000px){
    html[dir="rtl"] .imgsec-r::after,html[dir="rtl"] .imgsec-l::after{
      background:linear-gradient(175deg,rgba(255,246,226,.96) 0%,rgba(255,246,226,.90) 55%,
        rgba(255,244,220,.60) 100%);}
    html[dir="rtl"] .imgsec-l .sec-split{margin-right:0;}
  }
  html[dir="rtl"] .cmhero h1{max-width:24ch;line-height:1.3;}
  html[dir="rtl"] .hero h1{line-height:1.3;}
  html[dir="rtl"] .section-heading{line-height:1.35;}
  html[dir="rtl"] .cta-band h2{line-height:1.4;}
  html[dir="rtl"] .cmev h3{line-height:1.4;}
"""

# =========================================================== VARIANT A, WARM
# The Yanbu TwoSuns September 22 deck, brought onto the cement microsite as a
# set of habits rather than as a palette. The first cut carried the deck's own
# blue family around #2766E8 as well, and the owner's verdict on seeing it was
# that the blue was not looking good, so the blue is gone from the whole site.
#
# What survives is everything the deck actually teaches, which has nothing to do
# with hue: colour marks one thing out of many instead of decorating all of
# them, a sequence changes colour at its last step, the line worth remembering
# goes on a dark full width bar, a thin gold hairline sits under a title, and
# status colour is spent about twenty times in seventeen slides rather than
# once per card.
#
# So the roles stay and the hues move onto the two the logo already owns. Deck
# accent1, the structural accent on cards, numerals, rails, rules and labels,
# becomes the site orange: #C45213, with #9A3E0C beneath it wherever the colour
# has to carry type. Deck accent2, which ended a sequence and tinted the second
# card, becomes the site gold: #8C6500, with #7A5A08 for type. Orange and gold
# separate at a glance and both belong here, which is the job the blue and the
# orange were doing between them before.
#
# THE GROUND is unchanged, and was never the deck's to change: cream, the hero
# washes and the warm photograph bands all stay exactly as they are. Only ONE
# section on the home page is painted by --bg at all, so repointing it would
# recolour that single band and leave the warm ones untouched beside it. The
# colour arrives on the furniture instead, which is also where the deck puts it.
#
# Loaded after CEM_CSS and RTL_CSS, so on equal specificity these rules win.
VAR_A_CSS = r"""
  :root{
    /* the deck, measured, then re-pitched. A name beginning dk is a deck role. */
    --dk-acc:#C45213;         /* accent1, the structural accent, the site orange */
    --dk-acc-deep:#9A3E0C;    /* accent1 darkened, 6.8:1 on white, 5.8 on the tint */
    --dk-acc-lit:#E89A5C;     /* accent6, for type and hairlines on the dark bar */
    --dk-acc-pale:#FFEAD6;    /* the tint that singles one card out */
    --dk-acc-line:#EEDFC9;    /* the deck card hairline */
    --dk-gold:#8C6500;        /* accent2, the second mark and the end of a run */
    --dk-gold-deep:#7A5A08;   /* accent2 for type, 6.4:1 on white */
    --dk-gold-pale:#F7EDC8;   /* the second tint on deck slide 4 */
    --dk-navy:#241A12;        /* the full width takeaway bar */
    --dk-navy-2:#1B130D;      /* dk2, the rail */
    --dk-grey-line:#EDE4D4;

    /* the site tokens the deck repoints. Both hues the deck and the site
       already share, the orange and the gold, are left alone. */
    --navy:#241A12; --ink:#2A231B;
    --text:#3A3A3A; --text-muted:#5A554C;
    --border:#EEDFC9; --border-soft:#F0E7D8;
    --shadow:0 4px 24px rgba(60,50,30,0.08),0 1px 4px rgba(0,0,0,0.06);
    --shadow-lg:0 18px 48px rgba(60,50,30,0.14);
  }

  /* ---- 1. a neutral card field with one card singled out by a tint ---- */
  /* Deck slide 4 runs six cards, four white, one pale orange, one pale green.
     Slides 8, 10 and 14 run a grey field with exactly one tinted card. Colour
     marks one thing out of many, it does not decorate all of them. Two card
     fields on the microsite take it: the six configuration rows and the eight
     practical detail cards, each with exactly one tinted, and the reason is in
     the copy at both. Those rules are below.
     The platform family grid used to be the third. It ran Core on a pale
     orange and Ray on a pale gold, with Horizon and Pulse white, because Core
     is the layer the other three attach to and Ray is the only one that is not
     a domain at all. It is a grid of four and the cycle below is a cycle of
     four, so it is the one place on the microsite where the two devices land
     exactly on top of each other, and two tinted cards beside two white ones
     read as uneven next to it. The grid goes to deck slide 13 instead: four
     white cards, each on its own bar. What the tint was saying, the copy on
     the cards already says in words. */
  .cmfam .f{background:#fff;border:1px solid var(--dk-acc-line);
    border-top:4px solid var(--dk-acc-line);}
  .cmfam .f:hover{box-shadow:0 12px 40px rgba(60,50,30,.15);}
  .cmfam .x{border-top-color:rgba(36,26,18,.12);}

  /* The small uppercase labels. There are eleven of these on the microsite in
     #8C6500, and the two cards above are tinted, one pale orange and one pale
     gold, so a gold eyebrow inside the gold card is a label the tint swallows.
     They all move to #9A3E0C, which is 5.9:1 on the orange tint, 5.3 on the
     gold one and 6.8 on white, clear of AA at their 10.5px to 13px sizes.
     Not in this list, on purpose: .cmtier-a and theme's .section-tag, which are
     pills with their own warm background rather than labels on a card, and
     .cmpr .p-end .k, the scenario label, which is set below at 0,3,0 and wins
     against the 0,2,0 .cmpr .k here whatever order the two sit in. */
  .cmmod .d,.cmpd .k,.cmpr .k,.cmev-when,.split2-panel h3,
  .cmfoot-brand .by{color:var(--dk-acc-deep);}

  /* The six configuration rows on the home page, the deck's quiet field with
     one tint in it. Inputs is the one tinted, and the reason is in the
     copy: the other five rows describe the plant, and this one names the
     historian, the laboratory, the ERP, the weighbridge and how often each
     arrives. Nothing configured in the five above it stays true without it. */
  .cmrows .r{background:#FBF3E4;border-color:var(--dk-grey-line);}
  .cmrows .r.tint{background:var(--dk-acc-pale);border-color:rgba(196,82,19,.28);}

  /* The eight practical detail cards on the events page, same field, same rule.
     Entry is the tinted one: seven of the eight tell a guest what the evening
     is, and that one tells them whether they can come through the door. */
  .cmpd .p{background:#FBF3E4;border-color:var(--dk-grey-line);}
  .cmpd .p.tint{background:var(--dk-acc-pale);border-color:rgba(196,82,19,.28);}

  /* The capability map's three module columns already ran one tinted card, in
     gold. The content reason was right and only the hue changes: Core is the
     shared layer either side of which Horizon and Pulse sit. */
  .cmmod{background:#fff;border-color:var(--dk-grey-line);}
  .cmmod.core{background:var(--dk-acc-pale);border-color:rgba(196,82,19,.28);}
  .cmmod li{border-top-color:var(--dk-acc-line);}

  /* ---- 2. a sequence whose last step changes colour ---- */
  /* Deck slides 12 and 17 number 01, 02, 03 in accent1 and 04 in accent2. The
     microsite has four real sequences and each one gets it: the eight context
     workflows in two groups of four, the six stops on a capability run, the six
     stations under that run, and the numbered steps on two sector pages. The
     run is orange and the arrival is gold, which is the pair the logo runs and
     the one place a reader is meant to notice a change of colour at all. */
  .cmfl .n{background:var(--dk-acc-pale);border-color:var(--dk-acc);
    color:var(--dk-acc-deep);}
  .cmfl .g .w:last-child .n{background:var(--dk-gold-pale);border-color:var(--dk-gold);
    color:var(--dk-gold-deep);}
  .cmfl>h3{color:var(--dk-acc-deep);}
  .cmfl>h3 b{background:#fff;}
  .cmfl .mods span{color:var(--dk-acc-deep);}

  .cmrail{background:linear-gradient(140deg,#2C2016,#1B130D);}
  .cmrail .n{background:var(--dk-navy-2);border-color:rgba(232,154,92,.55);color:#FFCBA3;}
  .cmrail .track a:last-child .n{border-color:var(--dk-gold);color:#F3D08A;}
  .cmrail .track::before{background:rgba(232,154,92,.42);}
  .cmrail a:hover .n,.cmrail a:focus-visible .n{background:#FFCBA3;
    border-color:#FFCBA3;color:#1B130D;}
  .cmrail a:hover .l,.cmrail a:focus-visible .l{color:#FFCBA3;}

  /* These markers carry a 900 weight numeral in white, so both ends of a
     gradient have to clear 4.5 against white, and the site orange does not:
     white on #E0641E measures 3.49 and on the deck's own #FF7600 2.68, under
     even the 3:1 floor. The run therefore darkens to #C45213 at 4.55 into
     #9A3E0C at 6.84, and the gold arrival to #8C6500 at 5.28 into #7A5A08 at
     6.38. .cmfl keeps the pale fill with a dark numeral instead, which is the
     other way to end a sequence and measures 5.4. */
  .cmst .n{background:linear-gradient(135deg,var(--dk-acc),var(--dk-acc-deep));}
  .cmsts .cmst:last-child .n{background:linear-gradient(135deg,#8C6500,#7A5A08);}
  .cmst .d{color:var(--dk-acc-deep);}
  .cmst{border-top-color:rgba(204,153,0,.30);}

  .step::before{background:linear-gradient(135deg,var(--dk-acc),var(--dk-acc-deep));}
  .steps .step:last-child::before{background:linear-gradient(135deg,#8C6500,#7A5A08);}

  /* three numbered pressure cards on the context page, same rule */
  .cmpr .n{background:var(--dk-acc);}
  .cmpr .p:last-child .n{background:#8C6500;}
  .cmpr .mods span{color:var(--dk-acc-deep);}
  .cmpr .p-top p,.cmpr dd{color:var(--text-muted);}

  /* ---- 3. the dark bar that carries the takeaway ---- */
  /* The deck drops a near black bar across the full width of a slide and puts
     the one line it wants remembered on it. Two things on this microsite are
     exactly that: the closing call on every page, and the callout that states
     what the whole decision flow comes down to. Both were pale gold panels,
     which is how a takeaway looks when it is the same weight as the body
     around it. The bar is #241A12, the warm near black the site already runs
     as --navy rather than a cool one, and the gold hairline on the top edge is
     the deck's own rule, here marking the bar rather than a title. */
  .cta-band{background:var(--dk-navy);border-top:2px solid var(--gold);
    border-bottom:1px solid rgba(36,26,18,.5);}
  .cta-band h2{color:#fff;}
  .cta-band p{color:#EEDFC9;}
  .cta-band .btn-ghost{background:transparent;color:#fff;
    border-color:rgba(255,255,255,.55);}
  .cta-band .btn-ghost:hover{background:#fff;color:var(--dk-navy);}

  .callout{background:var(--dk-navy-2);border:1px solid rgba(232,154,92,.32);
    border-top:2px solid var(--gold);}
  .callout h3{color:#fff;}
  .callout p{color:#EEDFC9;}
  /* A callout whose heading is the whole message, the events programme panel,
     keeps the 10px the theme leaves under a heading that has a paragraph to
     separate itself from, which reads as an empty half of the box. */
  .callout h3:only-child{margin-bottom:0;}

  /* ---- 4. the thin gold hairline under a title ---- */
  /* Deck pattern, unchanged in hue: #E0B321 is the site gold. A block pseudo
     element sits at the inline start on its own, so Arabic needs no rule. */
  .cmhero h1::after,.section-heading::after{content:"";display:block;width:74px;
    height:2px;margin-top:16px;background:var(--gold);}
  .cta-band h2::after,.callout h3::after{content:none;}

  /* ---- 5. the two places that carried status colour ---- */
  /* The deck spends a green sixteen times and a red three times across
     seventeen slides, both as status, and the first cut of this variant spent
     each of them once: green on the outcome field of a workflow, red on the
     scenario block at the foot of a pressure card. The red was the larger of
     the two by a long way. Three pale pink panels run the full width of the
     three pressure cards and sit under half the context page, which made them
     the biggest block of colour on it and the one thing the warm repaint had
     not reached. Both colours are out, and the two jobs they were doing are
     done inside the palette instead.
     The scenario block goes back to the cream field and the rule the design
     gives it, which already separates it from the white card above; only its
     label is held at #9A3E0C, because the #C45213 the base file sets reads
     4.05 on that cream and the label is 11.5px uppercase.
     The outcome field is the fourth of four labels in a workflow and the one
     that says what changes once the work runs, so it takes the gold this
     variant already spends on the end of a run. 6.4:1 on white, against the
     #9A3E0C its three siblings carry. */
  .cmwf .w dt:nth-of-type(4){color:var(--dk-gold-deep);}
  .cmpr .p-end .k{color:var(--dk-acc-deep);}

  /* ---- 6. the rest of the furniture, so the accent is the system and not a
     stripe on two components ---- */
  .cmnav{border-bottom-color:rgba(196,82,19,.18);box-shadow:0 1px 20px rgba(60,50,30,.07);}
  .cmlinks a:hover,.cmlinks a.active{color:var(--dk-acc-deep);}
  .cmlang{border-inline-color:rgba(196,82,19,.22);}
  .cmlang .on{color:var(--dk-acc-deep);}
  .cmfoot{border-top-color:var(--dk-acc);}
  .cmfoot-links a:hover{color:var(--dk-acc-deep);}
  .cmtier-n{color:var(--dk-acc-deep);}
  .cmchips li{background:#fff;border-color:var(--dk-acc-line);}
  .cmsx .s .go{color:var(--dk-acc-deep);}
  .cmsx .s li,.cmmod li{border-top-color:var(--dk-acc-line);}
  .cmwf .w dt{color:var(--dk-acc-deep);}
  /* .cmtbl is not here. Its CSS exists at the top of this file but nothing in
     the generator emits the class, so a rule for it would paint nothing. The
     three .cmag rules below DO stay: that block is emitted, just gated behind
     AGENDA_PUBLIC, so it has to be right for the day that flag flips. */
  .cmag-t{background:rgba(255,234,214,.72);color:var(--dk-acc-deep);}
  .cmag-k{color:var(--dk-acc-deep);border-color:rgba(196,82,19,.40);}
  .cmag-b li::before{background:var(--dk-acc);}
  .cmmeta span::before{background:var(--dk-acc);}
  /* The tick marker is the only list bullet on the microsite and it ran an
     #E0641E to #CC9900 gradient, two hues on a 7px square sitting about 20px
     under a station line, 72 times on the capabilities page alone. One flat
     accent instead. */
  .tick li::before{background:var(--dk-acc);}
  /* The two remaining gold-soft panels on the capabilities page. The note bar
     is 1172px wide and would outweigh the single tinted Core card if it took
     the same tint, so it takes the neutral field the row cards already use.
     The tier pill is 170px and reads as a status beside a number this variant
     paints with the accent, so that one does take the tint. */
  .cmunits{background:#FBF3E4;border-color:var(--dk-grey-line);color:var(--text-muted);}
  .cmtier-a{background:var(--dk-acc-pale);color:var(--dk-acc-deep);}

  /* ---- 7. the framed pictures ---- */
  /* The eight station pictures and the home page works figure. They carry a 2px
     frame whose gradient runs #C45213 into #9A3E0C. One hue, so the eye reads a
     frame rather than a second accent arguing with the ordinal sitting on top
     of it, and with the pictures back in their own colours the frame is the
     only thing joining them to the page.
     The border is transparent and the colour arrives as a background, because
     border-image ignores border-radius and these boxes are 16px rounded. The
     padding box keeps var(--gold-soft), which is what shows while the picture
     loads, so nothing changes before the image arrives. The img is positioned
     against the padding box, so the border sits outside it and the picture is
     not covered. */
  .cmst .ph,.cmfig{border:2px solid transparent;
    background:linear-gradient(var(--gold-soft),var(--gold-soft)) padding-box,
               linear-gradient(135deg,#C45213,#9A3E0C) border-box;}
  /* No veil on these nine. They were re-cut from the files the owner supplied,
     without the colorchannelmixer grade the first cut baked in, so what the
     page shows is the photograph as it was taken: blue sky, green scrub, an
     orange excavator, high visibility vests. A wash of any colour over that
     would be the grade coming back by another route, which is the thing being
     undone. The gradient frame stays and now does the whole job of joining the
     picture to the page. */
  .cmst .ph::after,.cmfig::after{background:none;}
  /* ---- 8. the two event cards ---- */
  /* The page has to answer "is this one for me" from across the room. The
     conference card is the open one, so it stays light and gains an accent top
     edge and a lift. The evening is the closed one and the one being sold, so
     it goes to the apricot wash with a solid badge on it. One pale card, one
     warm card, and the answer arrives before any of the words do. */
  .cmev{position:relative;}
  .cmev:not(.feat),.cmses{box-shadow:0 10px 30px rgba(60,50,30,.09);
    transition:transform .2s ease,box-shadow .2s ease;}
  .cmev:not(.feat):hover,.cmses:hover{transform:translateY(-3px);
    box-shadow:0 16px 38px rgba(60,50,30,.15);}
  .cmev::before{content:"";position:absolute;inset:-1px -1px auto;height:4px;
    border-radius:20px 20px 0 0;}
  .cmev:not(.feat)::before{background:linear-gradient(90deg,var(--dk-acc),var(--dk-acc-lit));}

  /* The evening card is the warm one. The band behind it is cream at
     #FFEFCE, so a pale gold card would sink into it and a white one would
     be the conference card again. Apricot is the one light tone that is
     still clearly a different block against that cream, and it keeps the
     page inside the orange and gold the rest of the site runs on. */
  .cmev.feat{border:1px solid rgba(154,62,12,.26);padding:34px 36px;
    background:linear-gradient(150deg,#FFE7D3 0%,#FFD9BC 52%,#FFCBA3 100%);
    box-shadow:0 18px 44px rgba(154,62,12,.20);}
  .cmev.feat::before{background:linear-gradient(90deg,#9A3E0C,#F97316);}
  .cmev.feat h3{color:var(--dk-navy);font-size:clamp(22px,2.7vw,31px);}
  /* .k is the kicker, .l the one line claim under it. #9A3E0C rather than
     the #C45213 used elsewhere: measured against #FFCBA3, the darkest point
     of the wash, #C45213 reads 3.14 to 1 and #9A3E0C reads 5.16. */
  .cmev.feat .k{color:#9A3E0C;font-weight:800;margin-bottom:4px;}
  .cmev.feat .l{color:rgba(36,26,18,.76);margin-bottom:12px;}
  .cmev.feat p{color:rgba(36,26,18,.84);}
  .cmev.feat .cmmeta{color:rgba(36,26,18,.80);}
  .cmev.feat .cmmeta span::before{background:#9A3E0C;}
  .cmev.feat .cmnote{color:rgba(36,26,18,.74);}
  .cmev.feat .cmbadge{background:#9A3E0C;color:#fff;}
  .cmev.feat .btn-ghost{background:transparent;color:var(--dk-navy);
    border-color:rgba(36,26,18,.40);}
  .cmev.feat .btn-ghost:hover{background:var(--dk-navy);color:#fff;
    border-color:var(--dk-navy);}
  @media(max-width:760px){.cmev.feat{padding:26px 22px;}}
  /* The programme panel sits directly under the evening card. White keeps
     the apricot card the one coloured block in the section rather than
     making a second one of the panel. */
  .callout.cmsoon{background:#fff;border:1px solid var(--dk-grey-line);
    border-top:2px solid var(--gold);padding:19px 26px;}
  .callout.cmsoon h3{color:var(--dk-navy);}
  /* The invitation is printed, so the anchor it carries has to clear the
     sticky nav when a reader arrives on it rather than land under it. */
  .cmanch{scroll-margin-top:96px;}
  .cmanch:focus{outline:none;}
  .cmpd-l{display:block;margin-top:7px;font-size:13px;font-weight:800;
    color:var(--dk-acc);text-decoration:none;
    border-bottom:1px solid rgba(196,82,19,.35);width:fit-content;}
  .cmpd-l:hover{color:var(--dk-acc-deep);border-bottom-color:currentColor;}
  .cmbadge{background:var(--dk-navy);color:#FFCBA3;}
  /* Filled near black for the closed door, outlined for the open one. The pair
     has to separate at a glance and from across the page, so the
     difference is weight rather than hue. */
  .cmbadge.open{background:var(--dk-acc-pale);color:var(--dk-acc-deep);
    box-shadow:inset 0 0 0 1px rgba(196,82,19,.34);}
  .cmses-d{background:linear-gradient(150deg,var(--dk-acc),var(--dk-acc-deep));}
  .cmpast li{background:#fff;border-color:var(--dk-grey-line);}
  /* the panel's corner glow was a gold and orange bloom. Kept at the same
     weight it had, pitched onto the one accent, because two hues in a glow
     behind a panel whose hairline is a single warm line read as a leftover. */
  .split2-panel::after{background:radial-gradient(ellipse,rgba(196,82,19,.10) 0%,
    rgba(196,82,19,.04) 45%,transparent 70%);}

  /* ---- 9. three more devices off the deck ---- */

  /* THE EDGE RULE. Deck slides 4 and 13 mark an item with a coloured rule at
     its inline start rather than with a border all the way round or a badge on
     top: slide 13 runs four cards on a 6px bar, slide 4 six items on a 3px one,
     and in both the rule is the only thing that says where an item begins. The
     microsite has four card families that carry no mark at all, a white or
     cream box with a hairline and a label, and between them they run about
     forty cards over seven pages: the configuration and governance rows, the
     workflow cards on use cases, the practical detail cards on the events page
     and the sector cards. They all take the rule.
     One hue, not the deck's four. The deck cycles blue, orange, gold and green
     down a column of six, which reads as four categories, and these cards are
     not four categories of anything. The rule here is structure, the same
     decision the top borders on the family grid already took.
     border-inline-start, so Arabic mirrors it with no second rule. */
  .cmrows .r,.cmwf .w,.cmpd .p,.cmsx .s{border-inline-start:4px solid var(--dk-acc);}
  /* the tinted card in a field sets border-color on all four edges at 0,3,0,
     which would take the rule back to the hairline, so it is restated */
  .cmrows .r.tint,.cmpd .p.tint{border-inline-start-color:var(--dk-acc);}

  /* THE PILL CHIP. Slide 3 ends with a row of capabilities that cut across the
     chain it has just drawn, and sets them as fully rounded outlined pills in
     the accent rather than as filled tags. The microsite's chips are the same
     content in the same position, the facilities shared across the modules
     above them, so they take the same shape: white, a 999px radius, and the
     outline and the label both in the accent. #9A3E0C on white is 6.8:1. */
  .cmchips li{border-radius:999px;border-color:rgba(196,82,19,.42);
    color:var(--dk-acc-deep);}

  /* THE CLOSING LINE. Slides 3 and 13 both end on a qualifier, centred, bold
     and in the accent, with air above it: the deck gives the line that says
     what the figure does not claim as much weight as the figure. Two notes on
     the microsite are exactly that, one under the workflow cards and one under
     the measurement list, and both were a small grey italic line at the left
     margin. The notes that sit inside a card, on the architecture tiers and on
     the two event cards, are captions on the thing beside them rather than the
     close of a section, so they keep what they had. */
  .cmnote{text-align:center;font-style:normal;font-weight:700;font-size:14px;
    color:var(--dk-acc-deep);margin-top:24px;}
  .cmtier .cmnote,.cmev .cmnote{text-align:start;font-style:italic;font-weight:400;
    font-size:13px;color:var(--text-muted);margin-top:14px;}

  /* ---- 10. the deck's four accents, cycling across the items in a group ---- */
  /* The deck does not mark a group in one colour. Slide 4 sets six items in six,
     slide 13 four cards in four, slide 3 numbers its chain in three and outlines
     its cross-cutting pills in four. Blue, orange, gold and green, with a red
     kept for the money and spent three times in seventeen slides.
     What the deck never does is let any of them become the system. Its pages are
     a pale field, its titles are near black, and an accent only ever lands on
     the mark beside an item. That is the whole difference from the first cut of
     this variant, where the blue was the nav, every lede, every badge, every
     bullet and both rails, and the owner's verdict on it was that the blue was
     not looking good. Here the four land on item marks and on nothing else:
     the chrome, the headings, the buttons, the rails, the dark closing bars and
     the photograph frames all stay on the logo's orange, gold and ink.
     --m is the item's mark and --m-t the same colour darkened for type.
     Measured, two of the deck's four cannot be a mark on white. A mark that
     carries meaning has a 3 to 1 floor, and the deck's #FF7600 reads 2.68 on
     white and its #E0B321 reads 1.97: on the deck they sit on a pale field, on
     a white card they are a line you have to look for. The blue and the green
     hold at 5.06 and 3.56 and stay exactly as the deck sets them. The orange
     moves to the site's own sun #E0641E at 3.49 and the gold to #A67C00 at
     3.82, both still plainly the same hue.
     Every darkened value clears 4.5 as type, on white and on the cream the
     scenario block uses: 7.09 and 6.24 for the blue, 5.27 and 4.64 for the
     orange, 5.28 and 4.65 for the gold, 5.37 and 4.73 for the green. */
  .cmrows .r,.cmwf .w,.cmpd .p,.cmsx .s,.cmpr .p{
    --m:#2766E8;--m-t:#1B4FC4;}
  .cmrows .r:nth-child(4n+2),.cmwf .w:nth-child(4n+2),.cmpd .p:nth-child(4n+2),.cmsx .s:nth-child(4n+2),.cmpr .p:nth-child(4n+2){
    --m:#E0641E;--m-t:#B24E00;}
  .cmrows .r:nth-child(4n+3),.cmwf .w:nth-child(4n+3),.cmpd .p:nth-child(4n+3),.cmsx .s:nth-child(4n+3),.cmpr .p:nth-child(4n+3){
    --m:#A67C00;--m-t:#8C6500;}
  .cmrows .r:nth-child(4n),.cmwf .w:nth-child(4n),.cmpd .p:nth-child(4n),.cmsx .s:nth-child(4n),.cmpr .p:nth-child(4n){
    --m:#169B62;--m-t:#0F7A4D;}
  /* A tinted card is the deck's other device, the one thing singled out of
     many, and it steps out of the cycle rather than fighting it: the tint is
     pale orange, so the mark on it is the orange. */
  .cmrows .r.tint,.cmpd .p.tint{--m:#E0641E;--m-t:#B24E00;}

  /* the mark itself: an edge rule on four families, the numbered badge on the
     fifth, since that is the mark those cards already carry */
  .cmrows .r,.cmwf .w,.cmpd .p,.cmsx .s{border-inline-start-color:var(--m);}
  .cmrows .r.tint,.cmpd .p.tint{border-inline-start-color:var(--m);}
  /* the badge is the one mark that carries type: a 14px 900 numeral in white,
     which needs 4.5 and not 3, so it is filled with the darkened value. White
     reads 7.09, 5.27, 5.28 and 5.37 on the four. */
  .cmpr .n{background:var(--m-t);}
  .cmpr .p:last-child .n{background:var(--m-t);}

  /* and the type that belongs to the mark. On the deck a card's kicker is the
     colour of its own rule, never of its neighbour's. */
  .cmpd .p .k{color:var(--m-t);}
  .cmpr .p .k{color:var(--m-t);}
  .cmpr .p .mods span{color:var(--m-t);}
  .cmsx .s .go{color:var(--m-t);}
  .cmwf .w dt,.cmwf .w dt:nth-of-type(4){color:var(--m-t);}
  /* the outcome field was the one label held apart in gold, which cannot stay
     a hue now that gold is one of the four marks. The emphasis moves off the
     label and onto the answer, where slide 13 also puts it. */
  .cmwf .w dd:nth-of-type(4){color:var(--navy);font-weight:600;}

  /* The platform family grid is four cards and the cycle is four marks, so it
     takes one each and nothing repeats: Core blue, Ray orange, Horizon gold,
     Pulse green. The mark is the top bar the grid already carried, and the
     line of capabilities at the foot of each card takes that card's colour. */
  /* the colour is set on the same rule that paints the bar, because the base
     file reaches these four cards through :nth-child too and a plain
     .cmfam .f would lose to it on specificity for cards two, three and four */
  .cmfam .f:nth-child(1){--m:#2766E8;--m-t:#1B4FC4;border-top-color:var(--m);}
  .cmfam .f:nth-child(2){--m:#E0641E;--m-t:#B24E00;border-top-color:var(--m);}
  .cmfam .f:nth-child(3){--m:#A67C00;--m-t:#8C6500;border-top-color:var(--m);}
  .cmfam .f:nth-child(4){--m:#169B62;--m-t:#0F7A4D;border-top-color:var(--m);}
  .cmfam .x{color:var(--m-t);}

  /* NOT cycled, on purpose. The four sequences already say something with
     colour, that the run is orange and the arrival is gold, and a cycle of four
     would overwrite it. The chips run five and nine to a group, where a cycle of
     four repeats visibly. */

  /* ---- 11. tier 02's two domain cards open the sections that detail them ---- */
  /* The capabilities page already carries a Horizon section and a Pulse section,
     each with its six capability groups and its stage rail, a screen and a half
     below the tier that names them. The tier was giving a reader the names and
     leaving them to go and find the rest. The card keeps every line it had, and
     the whole of it becomes the way in. Core is not a link: there is no Core
     section on this page, and a card that looks clickable and goes nowhere is
     worse than a card that never offered. */
  .cmmod-a{display:flex;flex-direction:column;height:100%;
    text-decoration:none;color:inherit;}
  .cmmod-a ul{flex:1;}
  .cmmod.go{transition:transform .2s ease,box-shadow .2s ease,border-color .2s ease;}
  .cmmod.go:hover,.cmmod.go:focus-within{transform:translateY(-3px);
    border-color:var(--dk-acc);box-shadow:0 14px 34px rgba(60,50,30,.15);}
  .cmmod-a:focus-visible{outline:2px solid var(--dk-acc-deep);outline-offset:4px;
    border-radius:10px;}
  .cmmod .go-l{display:flex;align-items:center;gap:8px;margin-top:13px;
    padding-top:12px;border-top:1px solid var(--dk-acc-line);
    font-size:12.5px;font-weight:800;color:var(--dk-acc-deep);line-height:1.4;}
  .cmmod .go-l .ar{font-size:14px;line-height:1;transition:transform .18s ease;}
  .cmmod.go:hover .go-l .ar{transform:translateY(2px);}
  @media(prefers-reduced-motion:reduce){
    .cmmod.go:hover,.cmmod.go:focus-within{transform:none;}
    .cmmod.go:hover .go-l .ar{transform:none;}
  }
"""


def head(d, title, desc, page, extra_css=""):
    """Page head. Arabic sits one level deeper, so canonical and alternates differ.
    extra_css carries styling only one page needs, so the other nine stay lean."""
    sub = "ar/" if d["lang"] == "ar" else ""
    canon = SITE + BASE + sub + ("" if page == "index.html" else page)
    en_url = SITE + BASE + ("" if page == "index.html" else page)
    ar_url = SITE + BASE + "ar/" + ("" if page == "index.html" else page)
    esc_t, esc_d = title.replace('"', "&quot;"), desc.replace('"', "&quot;")
    return f"""<!DOCTYPE html>
<html lang="{d['lang']}" dir="{d['dir']}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="ar" href="{ar_url}">
<link rel="alternate" hreflang="x-default" href="{en_url}">
<meta name="theme-color" content="#FFF5DD">
<meta property="og:type" content="website">
<meta property="og:site_name" content="TwoSuns">
<meta property="og:locale" content="{'ar_EG' if d['lang'] == 'ar' else 'en_CA'}">
<meta property="og:title" content="{esc_t}">
<meta property="og:description" content="{esc_d}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}/og-twosuns.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc_t}">
<meta name="twitter:description" content="{esc_d}">
<meta name="twitter:image" content="{SITE}/og-twosuns.jpg">
<link rel="icon" type="image/svg+xml" href="/logo-mini.svg">
<style>{theme.CSS}{theme.REVEAL_CSS}{arch.CSS}{process.CSS}{CEM_CSS}{CMA_CSS}{RTL_CSS}{VAR_A_CSS}{extra_css}</style>
{theme.REVEAL_HEAD}
{theme.LEADLANDER}
</head>
<body>
<a class="cmskip" href="#main">{e(d['skip'])}</a>
<canvas id="sun-canvas" aria-hidden="true"></canvas>
"""


# Pages the nav and the footer do not show, while the pages themselves stay
# built and reachable by their own URL. Hiding here rather than cutting the
# entries out of cement_copy means the Arabic labels survive the hiatus and
# putting an item back is one line, and it keeps the two copy dicts at the same
# number of keys. The three sector pages come with sectors.html: they are only ever
# reached from that hub, so hiding it alone would leave them orphaned.
# Requested 2026-11-05 as a temporary measure while capabilities is reworked.
HIDDEN = {"sectors.html", "use-cases.html"}

# The evening blocks and the detailed running order, held back while the speaker
# list is unconfirmed. The events page shows a short note in their place. Both
# agendas stay in the copy dicts untouched, so publishing them again is this one
# flag and nothing else. Requested 2026-11-09.
AGENDA_PUBLIC = False


def shown(pairs):
    """The nav or footer pairs that are not currently hidden."""
    return [(n, u) for n, u in pairs if u.split("#")[0] not in HIDDEN]


def nav(d, active, page=None):
    """Microsite nav. active is the nav item to light up, page is the file this
    really is. They differ on the three sector pages, which light up Sectors,
    and the language toggle has to follow page or it drops the visitor on the
    hub instead of the same page in the other language. An active page that is
    in HIDDEN simply marks nothing, which is what the sector pages now do."""
    pre = "../" if d["lang"] == "ar" else "ar/"
    def mark(u):
        here = u.split("#")[0] == active and (active != "index.html" or "#" not in u)
        return ' class="active" aria-current="page"' if here else ""
    links = "".join('<a href="%s"%s>%s</a>' % (u, mark(u), e(n))
                    for n, u in shown(d["nav"]))
    page = page or active
    other = pre + ("" if page == "index.html" else page)
    lang = ('<span class="cmlang"><span class="on">%s</span>'
            '<a href="%s" lang="%s" hreflang="%s">%s</a></span>'
            % (e(d["self_label"]), other, d["other"], d["other"], e(d["other_label"])))
    return """<nav class="cmnav">
  <div class="cmnav-in">
    <a class="brand" href="./"><img src="/logo-color.svg" alt="TwoSuns"></a>
    <button class="cmtoggle" aria-label="%s" aria-controls="cml" aria-expanded="false"
      onclick="var l=document.getElementById('cml');l.classList.toggle('open');
        this.setAttribute('aria-expanded',l.classList.contains('open'));">&#9776;</button>
    <div class="cmlinks" id="cml">%s%s
      <a class="btn-cta" href="%s">%s</a>
    </div>
  </div>
</nav>
<main id="main" tabindex="-1">
""" % (e(d["menu_label"]), links, lang, ask(d["nav_cta"]), e(d["nav_cta"]))


def footer(d):
    links = "".join('<a href="%s">%s</a>' % (u, e(n)) for n, u in shown(d["foot_links"]))
    return """</main>
<footer class="cmfoot">
  <div class="container">
    <div class="cmfoot-top">
      <div class="cmfoot-brand">
        <img src="/logo-color.svg" alt="TwoSuns">
        <div class="by">%s</div>
        <div class="cn"><a href="mailto:info@twosuns.ai">%s</a><br>%s</div>
      </div>
      <div class="cmfoot-links">%s</div>
    </div>
    <div class="cmfoot-bot">
      <div>%s</div>
      <div><a href="%s/privacy.html">%s</a> &nbsp;|&nbsp; <a href="%s/terms.html">%s</a>
        &nbsp;|&nbsp; <a href="%s/">%s</a></div>
    </div>
  </div>
</footer>
""" % (e(d["by"]), e(d["foot_email"]), e(d["foot_wa"]), links, e(d["foot_rights"]),
       SITE, e(d["foot_privacy"]), SITE, e(d["foot_terms"]), SITE, e(d["main_site"]))


# The loops on this microsite, attached late and only when they will be seen.
#
# A <video> carrying autoplay and a src fetches the whole file as soon as the
# page parses, wherever on the page it sits and whatever the reader has asked
# for. preload="metadata" does not hold that back; autoplay overrides it. On the
# concrete page that meant half a megabyte pulled down three viewports before
# the truck was reached, and pulled down in full for a reader with reduced
# motion who is then shown the still instead. So the markup carries data-src and
# no autoplay, and this attaches the real src when the element comes near the
# viewport, and never at all under prefers-reduced-motion.
#
# It also gives each loop the pause control WCAG 2.2.2 asks for. The button is
# built here rather than written into the markup because with no script nothing
# moves, and a pause button over a still picture is a lie.
MOTION_JS = """<script>
(function(){
  var vs = [].slice.call(document.querySelectorAll('video[data-src]'));
  if(!vs.length) return;
  if(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  var PAUSE = %s, PLAY = %s;

  function control(v){
    // the band's video sits in a layer behind the copy, so the button cannot
    // live beside it; both kinds hang it on the positioned box one level up
    var host = v.closest('.cncmix') || v.closest('.imgsec') || v.closest('.cmhero');
    if(!host) return;
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'cmpause';
    b.setAttribute('aria-label', PAUSE);
    b.innerHTML = '<span class="cmpause-i"></span>';
    b.addEventListener('click', function(){
      if(v.paused){ v.play(); b.classList.remove('is-off'); b.setAttribute('aria-label', PAUSE); }
      else { v.pause(); b.classList.add('is-off'); b.setAttribute('aria-label', PLAY); }
    });
    host.appendChild(b);
  }

  function start(v){
    if(v.getAttribute('src')) return;
    v.setAttribute('src', v.getAttribute('data-src'));
    var p = v.play();
    if(p && p.catch) p.catch(function(){});
    control(v);
  }

  if(!('IntersectionObserver' in window)){ vs.forEach(start); return; }
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(en){
      if(!en.isIntersecting) return;
      io.unobserve(en.target);
      start(en.target);
    });
  }, {rootMargin: '300px 0px'});
  vs.forEach(function(v){ io.observe(v); });
})();
</script>"""


def tail(d):
    """The scripts every page ends on, with this page's language in them."""
    import json
    return (theme.PARTICLES + reveal.body_script()
            + MOTION_JS % (json.dumps(d["motion_pause"]), json.dumps(d["motion_play"]))
            + "\n</body>\n</html>\n")


def hero(d, eyebrow, h1, sub, acts, shot="", vid=""):
    """shot names the hero photograph, as the sh- class defined in CEM_CSS.
    Empty means the cement banner the home page carries.

    vid names a loop to play in place of that photograph, without its suffix:
    the clip is vid.mp4 and the still is vid.jpg, which is the pair
    build/cementvid.py writes, so the poster and the loop's first frame are the
    same picture and there is nothing to see at the handover. The still stays
    the section's CSS background underneath, so a browser that will not play
    the clip, or a reader who has asked for less motion, gets the photograph
    the page had before rather than an empty box. The src is withheld until
    MOTION_JS attaches it, which is also what gives the loop its pause
    control."""
    v = ""
    if vid:
        if not os.path.exists(os.path.join(OUT, vid + ".mp4")):
            raise SystemExit("the %s hero needs cement/%s.mp4" % (shot, vid))
        v = ('<div class="cmhero-v">'
             '<video data-src="%s%s.mp4" poster="%s%s.jpg"'
             ' muted loop playsinline aria-hidden="true" tabindex="-1"></video>'
             '</div>' % (BASE, vid, BASE, vid))
    return """<section class="cmhero%s%s">
  %s<div class="hero-glow"></div>
  <div class="container">
    <div class="hero-eyebrow"><span class="dot"></span>%s</div>
    <h1>%s</h1>
    <p class="hero-sub">%s</p>
    <div class="hero-actions">%s</div>
  </div>
</section>
<div class="sun-divider"></div>
""" % (" sh-" + shot if shot else "", " has-v" if vid else "", v,
       e(eyebrow), e(h1), e(sub), acts)


def cta_band(heading, para, acts):
    return """<section class="cta-band">
  <div class="container">
    <h2>%s</h2>
    <p>%s</p>
    <div class="cta-actions">%s</div>
  </div>
</section>
""" % (e(heading), e(para), acts)


def rows(items, two=False, tint=()):
    """tint names the 1 based positions that carry the deck's pale blue, the one
    card singled out of a neutral field. Colour only, the copy is untouched."""
    cells = "".join('<div class="r%s"><b>%s</b>%s</div>'
                    % (" tint" if i in tint else "", e(k), e(v))
                    for i, (k, v) in enumerate(items, 1))
    return '<div class="cmrows%s">%s</div>' % (" two" if two else "", cells)


def chips(items, grid=False):
    """A row of capability pills. grid=True lays them out in equal columns
    instead of letting them wrap, which is what the nine shared facilities need:
    the natural wrap puts eight on the first row and strands the ninth."""
    return ('<ul class="cmchips%s">%s</ul>'
            % (" g" if grid else "",
               "".join("<li>%s</li>" % e(i) for i in items)))


def ticks(items):
    return '<ul class="tick">%s</ul>' % "".join("<li>%s</li>" % e(i) for i in items)


def steps(items):
    return '<div class="steps">%s</div>' % "".join(
        '<div class="step"><b>%s</b> %s</div>' % (e(a), e(b)) for a, b in items)


# ================================================================ HOME
def build_home(d):
    s = head(d, d["home_title"], d["home_desc"], "index.html") + nav(d, "index.html")
    s += hero(d, d["home_eyebrow"], d["home_h1"], d["home_sub"],
              btn(d["home_cta1"]) + " " + btn(d["home_cta2"], "capabilities.html", ghost=True))

    fams = "".join('<div class="f"><h3>%s</h3><div class="d">%s</div><div class="x">%s</div></div>'
                   % (e(n), e(a), e(b)) for n, a, b in d["fams"])
    # the heading and the two ledes take the 760 column and the works takes the
    # gutter beside them; the family grid stays at the full measure underneath,
    # which is the whole reason this is a figure and not a photo band
    s += """<section id="about">
  <div class="container">
    <div class="cncgap">
      <div>
        <div class="section-tag">%s</div>
        <h2 class="section-heading">%s</h2>
        <p class="lede">%s</p>
        <p class="lede">%s</p>
      </div>
      <figure class="cmfig"><img src="/cement/about-works.jpg" alt="%s"
        width="840" height="560" loading="lazy" decoding="async"></figure>
    </div>
    <h3 class="sub-heading" style="margin-top:34px;font-size:22px;">%s</h3>
    <div class="cmfam">%s</div>
  </div>
</section>
""" % (e(d["about_tag"]), e(d["about_h"]), e(d["about_p1"]), e(d["about_p2"]),
       e(d["about_fig_alt"]), e(d["about_fam_h"]), fams)

    # the platform architecture figure, the same one the main site home carries,
    # in this page's own language
    s += arch.section(e(d["arx_h"]), e(d["arx_p"]),
                      btn(d["arx_cta"], "capabilities.html", ghost=True),
                      tag=e(d["arx_tag"]), band="band-warm", variant="explain",
                      foot=e(d["arx_foot"]),
                      labels=dict((k, e(v)) for k, v in d["arx_labels"].items()))

    # The decision problem, over the dusk works. The side by side split this
    # section used to run cannot survive a band: the copy column and the
    # conditions panel measure 590 and 534 and would have to share 682, and
    # nothing in the CSS narrows .split2 or .callout inside .imgsec. Stacked
    # into the band's one column they are both WIDER than they were, which is
    # the trade this makes, and the section grows by roughly 350px for it.
    # The plate is the one already on context.html, which this section is the
    # precis of, and it is the only graded loop whose crop was cut to empty the
    # half the copy needs. sec() gives it imgsec-keep because it carries a clip,
    # so Arabic repositions nothing and the tower cannot jump into that half.
    ctx_body = ('<p class="section-sub" style="margin-top:16px;">%s</p>\n'
                '    %s\n'
                '    <div class="callout"><h3>%s</h3><p>%s</p></div>'
                % (e(d["ctx_p2"]), panel(d["ctx_cond_h"], d["ctx_cond"]),
                   e(d["ctx_flow_h"]), e(d["ctx_flow_p"])))
    s += sec(ctx_body, tag=d["ctx_tag"], h=d["ctx_h"], p=d["ctx_p1"],
             **band("cx_wf"))

    # Configuration, over the kiln shell its first row names. two=True is not
    # optional: .imgsec .cmrows.two is the only rows form the CSS narrows inside
    # a band, so plain rows() would be stranded at three columns of 207px in a
    # 682px column. This is the pairing the four industry pages already run.
    s += sec(rows(d["cfg_rows"], two=True, tint=(6,)), tag=d["cfg_tag"], h=d["cfg_h"],
             p=d["cfg_p"], **band("cfg_kiln"))

    s += cta_band(d["home_close_h"], d["home_close_p"],
                  btn(d["home_close_cta1"]) + " " + btn(d["home_close_cta2"], ghost=True))
    return s + footer(d) + tail(d)


# ================================================== PLATFORM CAPABILITY MAP
def capmap(d):
    """The platform capability map: administration and inputs, the three module
    columns either side of Core, and the shared facilities. This is the diagram the
    business plan carries as slide 5, as real bilingual markup rather than a raster,
    so the Arabic page gets Arabic and a phone gets a reflow.

    One card with a numbered spine down the start edge, rather than the three
    separate cards this was before. The three tiers are one structure, and three
    boxes stacked with a gap between them read as three unrelated diagrams.

    Every module is a <details>. The names alone were a list of nouns a reader
    outside the industry could not price, and the page had no room to spend a
    paragraph on each of the thirty two. Closed, the diagram is the same quick
    read it was; opened, a module explains itself in place. The summary carries
    the name, so a closed <details> is still a complete capability list for a
    screen reader and for a crawler, and the description is in the DOM either
    way. No JavaScript: <details> opens on its own, and it opens when the page
    is printed or when the browser searches text inside it."""
    def det(cls, name, desc, tag="p"):
        return ('<details class="%s"><summary><span>%s</span></summary>'
                '<%s>%s</%s></details>' % (cls, e(name), tag, e(desc), tag))

    def column(side, h, sub, cnt, names, descs, go, go_l):
        items = "".join(det("cma-mi", n, dd) for n, dd in zip(names, descs))
        return ('<div class="cma-%s">'
                '<div class="cma-colh"><div><h3>%s</h3><span>%s</span></div>'
                '<em>%s</em></div>'
                '<div class="cma-list">%s</div>'
                '<a class="cma-go" href="#%s">%s'
                '<span class="cma-arrow" aria-hidden="true">&#8595;</span></a>'
                '</div>'
                % (side, e(h), e(sub), e(cnt), items, go, e(go_l)))

    assert len(d["arch_t1"]) == len(d["arch_t1_dd"]), "every input tile needs its line"
    assert len(d["arch_hz"]) == len(d["arch_hz_dd"]), "every Horizon module needs its line"
    assert len(d["arch_core"]) == len(d["arch_core_dd"]), "every Core element needs its line"
    assert len(d["arch_pl"]) == len(d["arch_pl_dd"]), "every Pulse module needs its line"
    assert len(d["arch_t3"]) == len(d["arch_t3_dd"]), "every shared facility needs its line"

    admin = "".join(det("cma-tile", n, dd)
                    for n, dd in zip(d["arch_t1"], d["arch_t1_dd"]))
    core = "".join('<li>%s</li>' % det("cma-ci", n, dd)
                   for n, dd in zip(d["arch_core"], d["arch_core_dd"]))
    shared = "".join(det("cma-sf", n, dd, tag="span")
                     for n, dd in zip(d["arch_t3"], d["arch_t3_dd"]))

    return """<section class="band-alt">
  <div class="container">
    <div class="section-tag">%s</div>
    <h2 class="section-heading">%s</h2>
    <p class="section-sub">%s</p>

    <div class="cma">

      <div class="cma-row">
        <div class="cma-lab"><span class="cma-n">%s</span><b>%s</b><small>%s</small></div>
        <div>
          <p class="cma-cap">%s</p>
          <div class="cma-admin">%s</div>
          <p class="cma-cap">%s</p>
        </div>
      </div>

      <div class="cma-row">
        <div class="cma-lab"><span class="cma-n">%s</span><b>%s</b><small>%s</small></div>
        <div class="cma-grid">
          %s
          <div class="cma-core">
            <h3>%s</h3>
            <div class="cma-k">%s</div>
            <ul>%s</ul>
          </div>
          %s
        </div>
      </div>

      <div class="cma-row">
        <div class="cma-lab"><span class="cma-n">%s</span><b>%s</b><small>%s</small></div>
        <div>
          <div class="cma-ray">%s</div>
          <div class="cma-shared">%s</div>
          <p class="cma-cap">%s</p>
        </div>
      </div>

      <div class="cma-foot">%s</div>
    </div>
  </div>
</section>
""" % (e(d["arch_tag"]), e(d["arch_h"]), e(d["arch_p"]),
       e(d["arch_t1_n"]), e(d["arch_t1_k"]), e(d["arch_t1_a"]),
       e(d["arch_t1_who"]), admin, e(d["arch_t1_note"]),
       e(d["arch_t2_n"]), e(d["arch_t2_k"]), e(d["arch_t2_a"]),
       column("hz", d["arch_hz_h"], d["arch_hz_d"], d["arch_hz_c"],
              d["arch_hz"], d["arch_hz_dd"], "horizon",
              d["arch_go"] % d["arch_hz_h"]),
       e(d["arch_core_h"]), e(d["arch_core_d"]), core,
       column("pl", d["arch_pl_h"], d["arch_pl_d"], d["arch_pl_c"],
              d["arch_pl"], d["arch_pl_dd"], "pulse",
              d["arch_go"] % d["arch_pl_h"]),
       e(d["arch_t3_n"]), e(d["arch_t3_k"]), e(d["arch_t3_a"]),
       e(d["arch_ray"]), shared, e(d["arch_t3_note"]),
       e(d["arch_units"]))



# ================================================================ EVENTS
def events_jsonld(d):
    """Event structured data for the three dated items on the events page.
    Times are Africa/Cairo, which is UTC+2 in November. The invitation-only
    items carry no offers, because there is no ticket to price."""
    sub = "ar/" if d["lang"] == "ar" else ""
    page = SITE + BASE + sub + "events.html"
    cairo = {"@type": "PostalAddress", "addressLocality": "Cairo",
             "addressCountry": "EG"}
    base = {"eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
            "eventStatus": "https://schema.org/EventScheduled",
            "inLanguage": d["lang"], "url": page}
    conf_id = page + "#aicce29"
    conf = dict(base, **{
        "@type": "Event", "@id": conf_id,
        "name": d["ev1_h"], "description": d["ev1_p"],
        "startDate": "2026-11-23", "endDate": "2026-11-25",
        "location": {"@type": "Place", "name": d["ev1_where"], "address": cairo},
        "organizer": {"@type": "Organization",
                      "name": "Arab Union for Cement and Building Materials",
                      "alternateName": "AUCBM"},
    })
    session = dict(base, **{
        "@type": "Event", "@id": page + "#session-10-7",
        "name": d["ses_h"], "description": d["ses_p"],
        "identifier": d["ses_code"],
        "startDate": "2026-11-24T13:30:00+02:00",
        "endDate": "2026-11-24T13:45:00+02:00",
        "superEvent": {"@id": conf_id},
        "location": {"@type": "Place", "name": d["ses_place"], "address": cairo},
        "performer": {"@type": "Person", "name": "Aiman El-Ramly",
                      "jobTitle": "Chief Executive Officer",
                      "worksFor": {"@type": "Organization", "name": "TwoSuns"}},
    })
    reception = dict(base, **{
        "@type": "Event", "@id": page + "#future-of-cement",
        "name": d["ev2_h"], "description": d["ev2_p"],
        "startDate": "2026-11-25T16:00:00+02:00",
        "endDate": "2026-11-25T23:00:00+02:00",
        "location": {"@type": "Place", "name": d["ev2_place"], "address": cairo},
        "organizer": [{"@type": "Organization", "name": "TwoSuns"},
                      {"@type": "Organization", "name": "Korayem Group"}],
    })
    graph = {"@context": "https://schema.org",
             "@graph": [conf, session, reception]}
    blob = json.dumps(graph, ensure_ascii=False, separators=(",", ":"))
    return ('<script type="application/ld+json">%s</script>\n'
            % blob.replace("<", "\\u003c"))


def build_events(d):
    s = head(d, d["ev_title"], d["ev_desc"], "events.html") + nav(d, "events.html")
    s += hero(d, d["ev_eyebrow"], d["ev_h1"], d["ev_sub"],
              btn(d["ev_cta1"]) + " " + btn(d["ev_cta2"], ghost=True),
              shot="events")

    s += """<section>
  <div class="container">
    <div class="section-tag">%s</div>
    <h2 class="section-heading">%s</h2>
    <p class="section-sub">%s</p>

    <div class="cmev">
      <div class="cmbadge open">%s</div>
      <div class="cmev-when">%s &middot; %s</div>
      <h3>%s</h3>
      <p>%s</p>
      <div class="acts">%s</div>
    </div>

    <div class="cmses">
      <div class="cmses-d"><span class="dd">%s</span><span class="mm">%s</span></div>
      <div class="cmses-b">
        <div class="cmev-when">%s &middot; %s</div>
        <h3 style="font-size:20px;">%s</h3>
        <p style="font-weight:700;color:var(--navy);margin-bottom:6px;">%s</p>
        <p>%s</p>
        <div class="cmmeta"><span>%s</span><span>%s</span><span>%s</span></div>
      </div>
    </div>
  </div>
</section>
""" % (e(d["ev_up_tag"]), e(d["ev_up_h"]), e(d["ev_up_p"]), e(d["ev1_badge"]),
       e(d["ev1_when"]), e(d["ev1_where"]), e(d["ev1_h"]), e(d["ev1_p"]),
       btn(d["ev1_cta"]),
       e(d["ses_day"]), e(d["ses_mon"]), e(d["ses_tag"]), e(d["ses_code"]),
       e(d["ses_h"]), e(d["ses_who"]), e(d["ses_p"]),
       e(d["ses_when"]), e(d["ses_time"]), e(d["ses_place"]))

    def agenda(rows):
        """A time column beside a block of detail. The invitation's three blocks
        and the detailed running order are the same shape, so they share this."""
        out = ""
        for t, h, kind, p, who in rows:
            k = '<span class="cmag-k">%s</span>' % e(kind) if kind else ""
            body = "<h3>%s%s</h3>" % (e(h), k)
            if p:
                body += "<p>%s</p>" % e(p)
            if who:
                body += "<ul>%s</ul>" % "".join("<li>%s</li>" % e(w) for w in who)
            out += ('<div class="cmag-r"><div class="cmag-t">%s</div>'
                    '<div class="cmag-b">%s</div></div>' % (e(t), body))
        return out

    eve = agenda(d["eve_rows"])
    ag = agenda(d["ag_rows"])

    # position 5 is Entry, the one of the eight that governs whether a guest
    # gets through the door, so it is the card the deck's tint singles out.
    def pd_val(v):
        """A value is a sentence, or a sentence with a link under it. The
        invitation prints a map link for the venue, and Getting there is the
        cell a reader is in when they want it."""
        if isinstance(v, tuple):
            text, label, href = v
            return ('%s<a class="cmpd-l" href="%s" target="_blank" '
                    'rel="noopener">%s</a>' % (e(text), href, e(label)))
        return e(v)

    pd = "".join('<div class="p%s"><div class="k">%s</div><div class="v">%s</div></div>'
                 % (" tint" if i == 5 else "", e(k), pd_val(v))
                 for i, (k, v) in enumerate(d["pd_rows"], 1))

    # The printed invitation sends readers to events.html#agenda, so the three
    # blocks it carries are on the page whatever AGENDA_PUBLIC says, and the
    # anchor lands on them. Only the detailed running order is held back.
    programme = ("""<h3 class="sub-heading cmanch" id="agenda" tabindex="-1"
        style="margin-top:38px;font-size:22px;">%s</h3>
    <div class="cmag">%s</div>
""" % (e(d["eve_h"]), eve))

    if AGENDA_PUBLIC:
        programme += ("""    <p class="cmnote">%s</p>

    <h3 class="sub-heading" style="margin-top:38px;font-size:22px;">%s</h3>
    <div class="cmag">%s</div>
    <p class="cmnote">%s</p>
"""
                      % (e(d["eve_note"]), e(d["ag_h"]), ag, e(d["ag_note"])))
    else:
        # .callout is the gold panel the home page already uses, so holding the
        # running order back needs no styling of its own. The line is the whole
        # message, there is nothing to say about a detail that does not exist
        # yet, so the panel carries the heading alone.
        programme += ('    <div class="callout cmsoon"><h3>%s</h3></div>\n'
                      % e(d["ev_soon_h"]))

    # The evening is a different kind of event from the conference, so it gets
    # its own section head rather than sitting as one more card under the
    # conference. The band change alone was not saying it.
    s += """<section class="band-alt">
  <div class="container">
    <div class="section-tag">%s</div>
    <h2 class="section-heading">%s</h2>
    <p class="section-sub">%s</p>

    <div class="cmev feat">
      <div class="cmbadge">%s</div>
      <h3>%s</h3>
      <p class="k">%s</p>
      <p class="l">%s</p>
      <div class="cmmeta"><span>%s</span><span>%s</span><span>%s</span><span>%s</span></div>
      <p style="margin-top:16px;">%s</p>
      <div class="acts">%s %s</div>
      <p class="cmnote">%s</p>
      <p class="cmnote">%s</p>
    </div>

    %s
    <h3 class="sub-heading" style="margin-top:38px;font-size:22px;">%s</h3>
    <div class="cmpd">%s</div>
  </div>
</section>
""" % (e(d["ev_inv_tag"]), e(d["ev_inv_h"]), e(d["ev_inv_p"]),
       e(d["ev2_badge"]), e(d["ev2_h"]), e(d["ev2_kicker"]), e(d["ev2_line"]),
       e(d["ev2_when"]), e(d["ev2_time"]), e(d["ev2_place"]), e(d["ev2_dress"]),
       e(d["ev2_p"]), btn(d["ev2_cta1"], href=EVENTBRITE, new_tab=True),
       btn(d["ev2_cta2"], ghost=True), e(d["ev2_note"]),
       e(d["ev2_cred"]),
       programme, e(d["pd_tag"]), pd)

    past = "".join("<li><b>%s</b> &middot; %s &middot; %s</li>" % (e(a), e(b), e(c))
                   for a, b, c in d["past_rows"])
    s += """<section>
  <div class="container">
    <div class="section-tag">%s</div>
    <h2 class="section-heading">%s</h2>
    <p class="section-sub">%s</p>
    <ul class="cmpast">%s</ul>
  </div>
</section>
""" % (e(d["past_tag"]), e(d["past_h"]), e(d["past_p"]), past)

    s += cta_band(d["ev_close_h"], d["ev_close_p"],
                  btn(d["ev_cta2"]) + " " + btn(d["ev_cta1"], ghost=True))
    return s + events_jsonld(d) + footer(d) + tail(d)


# ================================================================ CHECKS
# ========================================================== SHARED PAGE PIECES
def sec(body, band="", tag="", h="", p="", lede=False, shot="", side="r", clip="",
        sid=""):
    """One section. band is "", "band-alt" or "band-warm"; p renders as the section
    sub, or as a lede paragraph when the copy is long enough to want the wider type.

    shot lays the section over a photograph the way the main site's industry pages
    do, and takes the image's path from the site root. side is the half of the
    frame the photograph keeps, "r" or "l"; the wash covers the other half and the
    copy sits there, so consecutive bands on a page alternate. A photograph
    replaces the band colour, so the two are never combined.

    sid gives the section an id to be linked to from elsewhere on the page, and
    the scroll margin that stops a reader landing underneath the sticky nav.

    clip names a loop that plays where that photograph sits, as the basename of
    a pair under cement/: <clip>.mp4 is the loop and the shot stays its poster,
    so the section looks the same the moment the page opens and only then starts
    moving. It needs a shot to be its poster, and the builder refuses to generate
    a page whose loop is not in the repository."""
    top = ""
    if tag:
        top += '    <div class="section-tag">%s</div>\n' % e(tag)
    if h:
        top += '    <h2 class="section-heading">%s</h2>\n' % e(h)
    if p:
        top += '    <p class="%s">%s</p>\n' % ("lede" if lede else "section-sub", e(p))
    if shot:
        assert side in ("r", "l"), side
        vd = ""
        if clip:
            if not os.path.exists(os.path.join(OUT, clip + ".mp4")):
                raise SystemExit("the band loop %s.mp4 is not in cement/" % clip)
            vd = ('  <div class="cmband-v"><video data-src="/cement/%s.mp4" muted'
                  ' loop playsinline aria-hidden="true"'
                  ' tabindex="-1"></video></div>\n' % clip)
        keep = " imgsec-keep" if clip else ""
        return ('<section class="imgsec imgsec-%s%s area-sec" style="--cmband:url(\'%s\');">\n'
                '%s  <div class="container">\n   <div class="sec-split">\n%s    %s\n'
                '   </div>\n  </div>\n</section>\n') % (side, keep, shot, vd, top, body)
    assert not clip, "a loop needs a shot to be its poster"
    cls = " ".join(x for x in (band, "cmanch" if sid else "") if x)
    return '<section%s%s>\n  <div class="container">\n%s    %s\n  </div>\n</section>\n' % (
        ' id="%s"' % sid if sid else "", ' class="%s"' % cls if cls else "", top, body)


def panel(h, items):
    return '<div class="split2-panel" style="margin-top:22px;max-width:760px;">' \
           '<h3>%s</h3>%s</div>' % (e(h), ticks(items))


def mixer(d):
    """The supplied mixer truck loop, as a captioned figure.

    The clip is composited onto the exact cream this section paints, measured
    off the rendered page, so it needs no alpha and no card: every edge is the
    page's own background. The poster is the frame the loop opens on, which is
    both what shows while the file loads and what a reader who has asked for no
    motion sees instead, so nothing is lost either way.

    Muted, inline and looping, so no browser refuses to start it and nothing
    plays sound. The still carries the description and the caption carries the
    point, which is whose truck this is.

    The src is withheld until MOTION_JS attaches it, so the file is fetched
    when the figure is nearly in view and not at all under reduced motion. The
    poster is what the element shows until then, which is also what it shows
    if there is no script at all. role="img" is not a role <video> is allowed
    to take, so the description lives on the <img> that reduced motion reveals
    and the video is left to the caption.
    """
    for f in ("mixer-truck.mp4", "mixer-truck.jpg"):
        if not os.path.exists(os.path.join(OUT, f)):
            raise SystemExit("the mixer figure needs cement/%s" % f)
    return ('<figure class="cncmix">'
            '<video data-src="/cement/mixer-truck.mp4" poster="/cement/mixer-truck.jpg"'
            ' muted loop playsinline aria-hidden="true" tabindex="-1"></video>'
            '<img src="/cement/mixer-truck.jpg" alt="%s">'
            '<figcaption>%s</figcaption></figure>'
            % (e(d["cnc_gap_fig_alt"]), e(d["cnc_gap_fig_cap"])))


def mods(names):
    """The modules a pressure or a workflow reaches. The microsite has no module
    reference page, so these name the module rather than linking to it. Every name
    comes from arch_hz and arch_pl, so one module reads one way across the site."""
    return '<div class="mods">%s</div>' % "".join("<span>%s</span>" % e(n) for n in names)


def pressures(d):
    out = []
    for i, ((title, intro, scen), rows_, tags) in enumerate(
            zip(d["cx_rp_cards"], d["cx_rp_rows"], d["cx_rp_tags"]), 1):
        pairs = "".join("<dt>%s</dt><dd>%s</dd>" % (e(k), e(v)) for k, v in rows_)
        out.append(
            '<div class="p">'
            '<div class="p-top"><div class="n">%02d</div><h3>%s</h3><p>%s</p></div>'
            '<div class="p-mid"><span class="k">%s</span><dl>%s</dl></div>'
            '<div class="p-end"><span class="k">%s</span><p>%s</p>%s</div>'
            '</div>'
            % (i, e(title), e(intro), e(d["cx_rp_effect"]), pairs,
               e(d["cx_rp_scen"]), e(scen), mods(tags)))
    return '<div class="cmpr">%s</div>' % "".join(out)


def flows(d):
    """The eight workflows in two labelled groups, the plant four then the
    commercial four. The split is positional because the copy lists them in that
    order in both languages, and asserting it here means a reordered list fails the
    build rather than quietly filing a Horizon workflow under Pulse."""
    items, tags = d["cx_wf_items"], d["cx_wf_tags"]
    assert len(items) == 8 and len(tags) == 8, "the context page expects eight workflows"
    out = []
    for label, lo in ((d["cx_wf_pulse"], 0), (d["cx_wf_horizon"], 4)):
        ws = []
        for n in range(lo, lo + 4):
            title, desc = items[n]
            ws.append('<div class="w"><div class="n">%d</div><div><h4>%s</h4>'
                      '<p>%s</p>%s</div></div>'
                      % (n + 1, e(title), e(desc), mods(tags[n])))
        out.append('<div class="cmfl"><h3><b>%s</b></h3><div class="g">%s</div></div>'
                   % (e(label), "".join(ws)))
    return "".join(out)


# ======================================================= CEMENT CONTEXT
def build_context(d):
    """The cement context the microsite opens on: the pressures an Egyptian producer
    is working through, and the workflows configured against them. It was a section
    of the home page until it became its own page, which is why the home section it
    left behind is now called the decision problem instead."""
    s = head(d, d["cx_title"], d["cx_desc"], "context.html") + nav(d, "context.html")
    s += hero(d, d["cx_eyebrow"], d["cx_h1"], d["cx_sub"],
              btn(d["cx_cta1"]) + " " + btn(d["cx_cta2"], "capabilities.html", ghost=True),
              shot="context", vid="context-hero")
    s += sec(pressures(d), "band-alt", d["cx_rp_tag"], d["cx_rp_h"], d["cx_rp_p"])
    s += sec(flows(d), "", d["cx_wf_tag"], d["cx_wf_h"], d["cx_wf_p"],
             **band("cx_wf"))
    # the production line the page has been describing in words, drawn
    s += sec(process.figure(dict((k, e(v)) for k, v in d["prc_labels"].items())),
             "band-warm", d["prc_tag"], d["prc_h"], d["prc_p"])
    s += cta_band(d["cx_close_h"], d["cx_close_p"],
                  btn(d["cx_close_cta1"]) + " "
                  + btn(d["cx_close_cta2"], "capabilities.html", ghost=True))
    return s + footer(d) + tail(d)


# The photograph a capability station carries, by station id. A station appears
# here only when a picture exists that really shows that work. The page was first
# drawn with twelve, and eleven of them were an office, a conference stage, an air
# handling unit or a batching plant, chosen because the layout had a slot. The
# owner's instruction was that the pictures be relevant, so a station with no
# entry renders as a plain wide row and adding its picture is one line here.
# Files are named cap-<station>.jpg so a commissioned picture drops into the slot
# it was briefed for. cap-pl-1.jpg is a stopgap, not a commissioned one: it is
# bm-extraction.jpg cropped below the ridge and onto the working bench, with the
# grey pulled out of the spoil face, which is the best the repository can do for
# this station until the real one arrives.
STATION_SHOTS = {
    "hz-1": "/cement/cap-hz-1.jpg",
    "hz-2": "/cement/cap-hz-2.jpg",
    "pl-1": "/cement/cap-pl-1.jpg",
    "pl-2": "/cement/cap-pl-2.jpg",
    "pl-3": "/cement/cap-pl-3.jpg",
    "pl-4": "/cement/cap-pl-4.jpg",
    "pl-5": "/cement/cap-pl-5.jpg",
    "pl-6": "/cement/cap-pl-6.jpg",
}


def stations(fam, groups, run, stops):
    """One capability family as a run: a dark rail naming the run and its six
    stops, then the six groups as wide rows beneath it.

    A row with a picture splits, picture against name, descriptor and items. A
    row without one puts the name and descriptor in a rail at the start and the
    items beside it, so both kinds read as wide rows and the page does not
    change shape as pictures arrive.

    fam prefixes the row ids so the rail's stops reach them, "hz" or "pl"."""
    assert len(groups) == len(stops) == 6, (
        "the rail is drawn for six stops, got %d groups and %d labels"
        % (len(groups), len(stops)))
    track = "".join(
        '<a href="#%s-%d"><div class="n">%02d</div><div class="l">%s</div></a>'
        % (fam, i, i, e(lab)) for i, lab in enumerate(stops, 1))
    out = ['<div class="cmrail"><div class="run">%s</div><div class="track">%s</div></div>'
           % (e(run), track), '<div class="cmsts">']
    for i, (name, desc, items) in enumerate(groups, 1):
        sid = "%s-%d" % (fam, i)
        shot = STATION_SHOTS.get(sid)
        if shot and not os.path.exists(os.path.join(OUT, "..", shot.lstrip("/"))):
            raise SystemExit("STATION_SHOTS[%r] names %s, which is not in the "
                             "repository" % (sid, shot))
        num = '<div class="n" aria-hidden="true">%02d</div>' % i
        if shot:
            head = '<h3>%s</h3><div class="d">%s</div>' % (e(name), e(desc))
            # alt is empty on purpose: the row's own heading names the work, and
            # a caption repeating it is noise in a screen reader. The ordinal
            # rides on the picture, so the name starts the text half.
            body = ('<div class="ph">%s<img src="%s" alt="" width="1000" height="667"'
                    ' loading="lazy" decoding="async"></div>'
                    '<div class="bd">%s%s</div>' % (num, shot, head, ticks(items)))
        else:
            # .nm is the name rail, .it the items beside it. .bd is the picture
            # row's text half only, so a class means one thing in both branches.
            body = ('<div class="nm"><div class="hd">%s<h3>%s</h3></div>'
                    '<div class="d">%s</div></div><div class="it">%s</div>'
                    % (num, e(name), e(desc), ticks(items)))
        out.append('<div class="cmst%s" id="%s" tabindex="-1">%s</div>'
                   % (" shot" if shot else "", sid, body))
    out.append("</div>")
    unseen = set(STATION_SHOTS) - {"%s-%d" % (fam, i) for i in range(1, 7)}
    assert unseen <= {"%s-%d" % (f, i) for f in ("hz", "pl") for i in range(1, 7)}, (
        "STATION_SHOTS has keys no station will ever ask for: %s" % sorted(unseen))
    return "".join(out)


# ========================================================== CAPABILITIES
def build_capabilities(d):
    s = head(d, d["cap_title"], d["cap_desc"], "capabilities.html") + nav(d, "capabilities.html")
    s += hero(d, d["cap_eyebrow"], d["cap_h1"], d["cap_sub"],
              btn(d["cap_cta1"]),
              shot="capabilities", vid="cap-hero")
    s += capmap(d)
    s += sec(stations("hz", d["cap_hz_groups"], d["cap_hz_run"], d["cap_hz_stops"]),
             "", d["cap_hz_tag"], d["cap_hz_h"], d["cap_hz_p"], sid="horizon")
    s += sec(stations("pl", d["cap_pl_groups"], d["cap_pl_run"], d["cap_pl_stops"]),
             "band-alt", d["cap_pl_tag"], d["cap_pl_h"], d["cap_pl_p"], sid="pulse")
    s += sec("", "", d["cap_adapt_tag"], d["cap_adapt_h"], d["cap_adapt_p"],
             lede=True, **band("cap_adapt"))
    s += cta_band(d["cap_close_h"], d["cap_close_p"], btn(d["cap_cta1"]))
    return s + footer(d) + tail(d)


# ========================================================== INDUSTRIES HUB
# The sector pages in display order. The hrefs live here and not in the copy dict
# because a filename is not translatable, and the Arabic dict must mirror the
# English one entry for entry.
SECTORS = ["construction.html", "concrete.html", "distribution.html"]

# The photograph each Sectors section is laid over, and the half of the frame
# it keeps. The bands on a page alternate sides, the way the main site's industry
# pages do. Paths are rooted because the microsite sits one level down and the
# Arabic two, and band() checks each file is really there, because a wrong name
# costs nothing at build time and shows as an empty wash on the live page.
# Do not reach for mfg-supply.jpg: the photograph is flipped, so its aisle
# numerals read backwards. The main site uses it on manufacturing.html.
# plant-aerial.jpg is not in this table: it was supplied for the Sectors
# hero and is set as sh-aerial above. It was flipped horizontally on request,
# which stands the preheater tower in the half the hero wash leaves clear.
# A third entry names a loop that plays where that band's photograph sits, as
# the basename of a pair built by build/cementvid.py. The still stays the
# poster, so a band that moves and a band that does not open identically.
BANDS = {
    "ind_sectors": ("/bm-operations.jpg",    "l"),
    "ind_areas":   ("/bm-extraction.jpg",    "r"),
    "con_who":     ("/cons-owners.jpg",      "l"),
    "con_ts":      ("/plat-deploy.jpg",      "r"),
    "cnc_who":     ("/area-materials.jpg",   "l"),
    "cnc_qual":    ("/bm-process.jpg",       "r"),
    "dst_who":     ("/area-distribution.jpg", "r"),
    "dst_vis":     ("/cons-logistics.jpg",   "l"),
    # the two moving bands. cx_wf is the dusk plant that was briefly the home
    # hero and was pulled from it, back on the page about the cement context
    # rather than over a headline. cap_adapt is a works at sunrise, a plant of
    # the size a first deployment actually lands in. It was cut for the platform
    # page's deployment section and moved here when that page was retired.
    # the side each one takes is where its subject actually is. The wash is
    # solid cream to 44 percent and only thins past about 72, so the far
    # quarter is the only part of a band that is really seen, which is what
    # the crops in build/cementvid.py put there.
    "cx_wf":       ("/cement/band-dusk.jpg",   "l", "band-dusk"),
    "cap_adapt":   ("/cement/band-works.jpg",  "r", "band-works"),
    # the kiln shell on the home page's configuration section, the only picture
    # on this microsite that is not an exterior of a works. It is a still and
    # not a loop because the source is a tracking shot: its head and tail are
    # 50.7 mean levels apart with 84 percent of pixels moved, against 2.1 and
    # 0.8 percent for band-dusk, so no crossfade closes it, and at 8.90s the
    # source is shorter than the 10.0s SEG cementvid.py cuts. It takes no
    # imgsec-keep: both outer quarters measure an edge density of 22.0 and
    # 19.0, so neither half is empty and the Arabic reposition shows the far
    # end of the same kiln rather than sky.
    "cfg_kiln":    ("/cement/band-kiln.jpg",   "r"),
}


def band(key):
    """The shot, side and clip keyword arguments sec() takes, from BANDS."""
    shot, side = BANDS[key][0], BANDS[key][1]
    clip = BANDS[key][2] if len(BANDS[key]) > 2 else ""
    path = os.path.join(OUT, "..", shot.lstrip("/"))
    if not os.path.exists(path):
        raise SystemExit("BANDS[%r] names %s, which is not in the repository" % (key, shot))
    return {"shot": shot, "side": side, "clip": clip}


def build_sectors(d):
    s = head(d, d["ind_title"], d["ind_desc"], "sectors.html") + nav(d, "sectors.html")
    s += hero(d, d["ind_eyebrow"], d["ind_h1"], d["ind_sub"],
              btn(d["ind_cta1"]) + " " + btn(d["ind_cta2"], "capabilities.html", ghost=True),
              shot="aerial")

    cells = []
    for (name, desc, bullets), href in zip(d["ind_sectors"], SECTORS):
        cells.append('<div class="s"><h3>%s</h3><p>%s</p><ul>%s</ul>'
                     '<a class="go" href="%s">%s</a></div>'
                     % (e(name), e(desc), "".join("<li>%s</li>" % e(b) for b in bullets),
                        href, e(d["ind_sec_link"])))
    s += sec('<div class="cmsx">%s</div>' % "".join(cells),
             "", d["ind_sec_tag"], d["ind_sec_h"], d["ind_sec_p"],
             **band("ind_sectors"))

    s += sec(rows(d["ind_behind_items"], two=True)
             + '<div style="margin-top:26px;">%s</div>'
               % btn(d["ind_behind_cta"], "capabilities.html", ghost=True),
             "", d["ind_behind_tag"], d["ind_behind_h"], d["ind_behind_p"],
             **band("ind_areas"))

    s += cta_band(d["ind_close_h"], d["ind_close_p"],
                  btn(d["ind_cta1"]) + " " + btn(d["ind_cta2"], "capabilities.html", ghost=True))
    return s + footer(d) + tail(d)


# ========================================================== SECTOR: CONSTRUCTION
def build_construction(d):
    s = head(d, d["con_title"], d["con_desc"], "construction.html") + nav(d, "sectors.html", "construction.html")
    s += hero(d, d["con_eyebrow"], d["con_h1"], d["con_sub"],
              btn(d["con_cta1"]) + " " + btn(d["con_cta2"], "sectors.html", ghost=True),
              shot="construction")
    s += sec(rows(d["con_who_rows"], two=True), "", d["con_who_tag"], d["con_who_h"],
             d["con_who_p"], lede=True, **band("con_who"))
    s += sec(rows(d["con_dem_rows"], two=True), "band-alt", d["con_dem_tag"], d["con_dem_h"],
             d["con_dem_p"])
    s += sec(ticks(d["con_gap_items"]), "", d["con_gap_tag"], d["con_gap_h"], d["con_gap_p"])
    s += sec(rows(d["con_ts_rows"], two=True) + panel(d["con_prac_h"], d["con_prac"]),
             "", d["con_ts_tag"], d["con_ts_h"], d["con_ts_p"], lede=True,
             **band("con_ts"))
    s += cta_band(d["con_close_h"], d["con_close_p"],
                  btn(d["con_cta1"]) + " " + btn(d["con_cta2"], "sectors.html", ghost=True))
    return s + footer(d) + tail(d)


# ========================================================== SECTOR: CONCRETE
def build_concrete(d):
    s = head(d, d["cnc_title"], d["cnc_desc"], "concrete.html") + nav(d, "sectors.html", "concrete.html")
    s += hero(d, d["cnc_eyebrow"], d["cnc_h1"], d["cnc_sub"],
              btn(d["cnc_cta1"]) + " " + btn(d["cnc_cta2"], "sectors.html", ghost=True),
              shot="concrete")
    s += sec(rows(d["cnc_who_rows"], two=True), "", d["cnc_who_tag"], d["cnc_who_h"],
             d["cnc_who_p"], lede=True, **band("cnc_who"))
    s += sec(rows(d["cnc_dem_rows"], two=True), "band-alt", d["cnc_dem_tag"], d["cnc_dem_h"],
             d["cnc_dem_p"])
    # the panel keeps the reading order; the truck sits in the column beside it
    s += sec('<div class="cncgap">'
             + panel(d["cnc_gap_panel_h"], d["cnc_gap_items"]) + mixer(d) + '</div>'
             + '<div class="callout" style="margin-top:22px;"><h3>%s</h3><p>%s</p></div>'
               % (e(d["cnc_gap_call_h"]), e(d["cnc_gap_call_p"])),
             "", d["cnc_gap_tag"], d["cnc_gap_h"], d["cnc_gap_p"], lede=True)
    s += sec(rows(d["cnc_tws_dom_rows"], two=True) + rows(d["cnc_tws_rows"], two=True),
             "band-warm", d["cnc_tws_tag"], d["cnc_tws_h"], d["cnc_tws_p"], lede=True)
    s += sec(steps(d["cnc_qual_steps"]) + panel(d["cnc_qual_carry_h"], d["cnc_qual_carry"])
             + '<p class="cmnote">%s</p>' % e(d["cnc_qual_note"]),
             "", d["cnc_qual_tag"], d["cnc_qual_h"], d["cnc_qual_p"],
             **band("cnc_qual"))
    s += cta_band(d["cnc_close_h"], d["cnc_close_p"],
                  btn(d["cnc_cta1"]) + " " + btn(d["cnc_cta2"], "sectors.html", ghost=True))
    return s + footer(d) + tail(d)


# ========================================================== SECTOR: DISTRIBUTION
def build_distribution(d):
    s = head(d, d["dst_title"], d["dst_desc"], "distribution.html") + nav(d, "sectors.html", "distribution.html")
    s += hero(d, d["dst_eyebrow"], d["dst_h1"], d["dst_sub"],
              btn(d["dst_cta1"]) + " " + btn(d["dst_cta2"], "sectors.html", ghost=True),
              shot="distribution")
    s += sec(rows(d["dst_who_rows"], two=True), "", d["dst_who_tag"], d["dst_who_h"],
             d["dst_who_p"], lede=True, **band("dst_who"))
    s += sec('<p class="lede">%s</p>' % e(d["dst_req_p2"])
             + panel(d["dst_req_panel_h"], d["dst_req_items"]),
             "band-alt", d["dst_req_tag"], d["dst_req_h"], d["dst_req_p1"], lede=True)
    s += sec(rows(d["dst_gap_rows"], two=True), "", d["dst_gap_tag"], d["dst_gap_h"],
             d["dst_gap_p"])
    s += sec(steps(d["dst_plat_steps"])
             + '<div class="split2" style="margin-top:26px;align-items:start;">'
               '<div class="split2-panel"><h3>%s</h3><p>%s</p></div>'
               '<div class="split2-panel"><h3>%s</h3><p>%s</p></div></div>'
               % (e(d["dst_plat_hz_h"]), e(d["dst_exp_p"]),
                  e(d["dst_plat_pl_h"]), e(d["dst_exp_h"])),
             "band-warm", d["dst_plat_tag"], d["dst_plat_h"], d["dst_plat_p"], lede=True)
    s += sec('<p class="lede">%s</p>' % e(d["dst_vis_p2"])
             + panel(d["dst_vis_panel_h"], d["dst_vis_items"]),
             "", d["dst_vis_tag"], d["dst_vis_h"], d["dst_vis_p1"], lede=True,
             **band("dst_vis"))
    s += sec('<p class="lede">%s</p>' % e(d["dst_cred_p2"])
             + rows(d["dst_cred_rows"], two=True),
             "band-alt", d["dst_cred_tag"], d["dst_cred_h"], d["dst_cred_p1"], lede=True)
    s += cta_band(d["dst_close_h"], d["dst_close_p"],
                  btn(d["dst_cta1"]) + " " + btn(d["dst_cta2"], "sectors.html", ghost=True))
    return s + footer(d) + tail(d)


# ========================================================== USE CASES
def build_usecases(d):
    s = head(d, d["uc_title"], d["uc_desc"], "use-cases.html") + nav(d, "use-cases.html")
    s += hero(d, d["uc_eyebrow"], d["uc_h1"], d["uc_sub"],
              btn(d["uc_cta1"]) + " " + btn(d["uc_cta2"], "capabilities.html", ghost=True),
              shot="usecases")
    s += sec(chips(d["uc_chain"]), "", d["uc_chain_tag"], d["uc_chain_h"], d["uc_chain_p"])

    labels = (d["uc_f_owner"], d["uc_f_surfaces"], d["uc_f_work"], d["uc_f_change"])
    wf = []
    for name, owner, surfaces, work, change in d["uc_items"]:
        pairs = "".join("<dt>%s</dt><dd>%s</dd>" % (e(k), e(v))
                        for k, v in zip(labels, (owner, surfaces, work, change)))
        wf.append('<div class="w"><h3>%s</h3><dl>%s</dl></div>' % (e(name), pairs))
    s += sec('<div class="cmwf">%s</div>' % "".join(wf)
             + '<p class="cmnote">%s</p>' % e(d["uc_wf_note"]),
             "band-alt", d["uc_wf_tag"], d["uc_wf_h"], d["uc_wf_p"])

    s += sec("".join('<p class="lede">%s</p>' % e(p) for p in d["uc_bring_p"]),
             "band-warm", d["uc_bring_tag"], d["uc_bring_h"], "")
    s += cta_band(d["uc_close_h"], d["uc_close_p"],
                  btn(d["uc_close_cta1"]) + " " + btn(d["uc_close_cta2"], ghost=True))
    return s + footer(d) + tail(d)


# ========================================================== COMPANY
def build_company(d):
    """The roster is not in the copy dict. A person's name and photo are the same in
    both languages, so they are read straight from the main site's content2.COMPANY
    and paired by position with the translated role and bio."""
    s = head(d, d["co_title"], d["co_desc"], "company.html",
             extra_css=teamgrid.CSS) + nav(d, "company.html")
    s += hero(d, d["co_eyebrow"], d["co_h1"], d["co_sub"],
              btn(d["co_cta1"]) + " " + btn(d["co_cta2"], "capabilities.html", ghost=True),
              shot="company")

    s += sec("".join('<p class="lede">%s</p>' % e(p)
                     for p in (d["co_purpose_p1"], d["co_purpose_p2"], d["co_purpose_p3"]))
             + '<div class="callout" style="margin-top:22px;"><p>%s</p></div>' % e(d["co_ab_p"]),
             "", d["co_purpose_tag"], d["co_purpose_h"], "")

    groups = content2.COMPANY["groups"]
    spec = (("co_lead_tag", "co_lead_h", "co_lead", True, "band-alt"),
            ("co_pae_tag", "co_pae_h", "co_pae", False, ""),
            ("co_ge_tag", "co_ge_h", "co_ge", False, "band-alt"))
    for (tagk, hk, rowk, is_lead, band), group in zip(spec, groups):
        people = group[-1]
        if len(people) != len(d[rowk]):
            raise SystemExit("cement.py: %s has %d rows but content2 group %r has %d people"
                             % (rowk, len(d[rowk]), group[0], len(people)))
        merged = []
        for src, (role, bio) in zip(people, d[rowk]):
            name, photo = src[0], (src[2] if len(src) == 4 else "")
            # content2 stores the portrait bare, which resolves against the main
            # site's root. The microsite sits a level down and the Arabic two, so
            # the path has to be rooted or every portrait 404s.
            if photo:
                photo = "/" + photo.lstrip("/")
            merged.append((name, role, photo, bio) if photo else (name, role, bio))
        s += ('<section%s>\n  <div class="container" style="%s">\n'
              '    <div class="section-tag">%s</div>\n'
              '    <h2 class="section-heading">%s</h2>\n    %s\n  </div>\n</section>\n'
              % (' class="%s"' % band if band else "", teamgrid.vars_for("warm"),
                 e(d[tagk]), e(d[hk]), teamgrid.grid(merged, lead=is_lead, e=e)))

    s += sec("", "band-warm", d["co_aepg_tag"], d["co_aepg_h"], d["co_aepg_p"], lede=True)
    s += sec('<div style="margin-top:26px;">%s</div>'
             % btn(d["co_ev_cta"], "events.html", ghost=True),
             "", d["co_ev_tag"], d["co_ev_h"], d["co_ev_p"])
    s += cta_band(d["co_close_h"], d["co_close_p"],
                  btn(d["co_cta1"]) + " " + btn(d["co_cta2"], "capabilities.html", ghost=True))
    return s + footer(d) + tail(d)


BANNED = ["—", "–", "revolutionary", "cutting-edge", "seamless", "leverage",
          "unlock", "empower", "AI-powered", "robust", "game-chang", "best-in-class",
          "transform the", "supercharge", "effortless", "turnkey solution"]


def check(body, name):
    low = body.lower()
    for b in BANNED:
        if b.lower() in low:
            raise SystemExit("cement.py: %s contains banned token %r" % (name, b))
    for tag in ("div", "section", "ul", "table"):
        o = body.count("<%s" % tag)
        c = body.count("</%s>" % tag)
        if o != c:
            raise SystemExit("cement.py: %s unbalanced <%s>: %d open, %d close"
                             % (name, tag, o, c))
    if body.count("<html") != 1 or body.count("</html>") != 1:
        raise SystemExit("cement.py: %s bad html wrapper" % name)
    # the reveal CSS hides content until the body script runs. Ship both or neither.
    if "classList.add('rv')" in body and "IntersectionObserver(function" not in body:
        raise SystemExit("cement.py: %s loads the reveal CSS without the reveal "
                         "body script, so revealed sections would stay invisible" % name)


def check_copy():
    """The two languages must describe the same page, so they must carry the same
    keys holding the same shapes. A key added to one and forgotten in the other is
    the easiest mistake to make here, and it would only surface as a KeyError on
    whichever page happened to use it."""
    en, ar = LANGS["en"], LANGS["ar"]
    missing = sorted(set(en) - set(ar))
    extra = sorted(set(ar) - set(en))
    if missing or extra:
        raise SystemExit("cement.py: copy keys differ. Missing from ar: %s. "
                         "Not in en: %s" % (missing or "none", extra or "none"))
    for k in sorted(en):
        if type(en[k]) is not type(ar[k]):
            raise SystemExit("cement.py: %s is %s in en but %s in ar"
                             % (k, type(en[k]).__name__, type(ar[k]).__name__))
        if isinstance(en[k], (list, dict)) and len(en[k]) != len(ar[k]):
            raise SystemExit("cement.py: %s has %d entries in en but %d in ar"
                             % (k, len(en[k]), len(ar[k])))
        if isinstance(en[k], dict) and set(en[k]) != set(ar[k]):
            raise SystemExit("cement.py: %s has different sub-keys in en and ar" % k)
    print("copy       %d keys, en and ar in step" % len(en))


if __name__ == "__main__":
    check_copy()
    total = 0
    for code, d in LANGS.items():
        out = OUT if code == "en" else os.path.join(OUT, "ar")
        os.makedirs(out, exist_ok=True)
        pages = {"index.html": build_home(d),
                 "context.html": build_context(d),
                 "capabilities.html": build_capabilities(d),
                 "sectors.html": build_sectors(d),
                 "construction.html": build_construction(d),
                 "concrete.html": build_concrete(d),
                 "distribution.html": build_distribution(d),
                 "use-cases.html": build_usecases(d),
                 "company.html": build_company(d),
                 "events.html": build_events(d)}
        for n, b in pages.items():
            check(b, "%s/%s" % (code, n))
            with open(os.path.join(out, n), "w") as f:
                f.write(b)
            total += len(b)
            print("%-8s %-14s %7d bytes" % (code, n, len(b)))
    print("total %d bytes" % total)
