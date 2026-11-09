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


def btn(label, href=None, ghost=False):
    cls = "btn-ghost" if ghost else "btn-cta"
    return '<a class="%s" href="%s">%s</a>' % (cls, href or ask(label), e(label))


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
  .cmhero.sh-capabilities{--cmshot:url('/cap-hero.jpg');}
  /* the Sectors hub takes the supplied plant aerial, flipped, so its tower
     stands in the half the wash leaves clear */
  .cmhero.sh-aerial{--cmshot:url('/cement/plant-aerial.jpg');}
  .cmhero.sh-construction{--cmshot:url('/cons-hero.jpg');}
  .cmhero.sh-concrete{--cmshot:url('/bm-concrete.jpg');}
  .cmhero.sh-distribution{--cmshot:url('/bm-distribution.jpg');}
  .cmhero.sh-usecases{--cmshot:url('/uc-hero.jpg');}
  .cmhero.sh-company{--cmshot:url('/company-hero.jpg');}
  .cmhero.sh-events{--cmshot:url('/events-hero.jpg');}
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
<style>{theme.CSS}{theme.REVEAL_CSS}{arch.CSS}{process.CSS}{CEM_CSS}{RTL_CSS}{extra_css}</style>
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
    var host = v.closest('.cncmix') || v.closest('.imgsec');
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


def hero(d, eyebrow, h1, sub, acts, shot=""):
    """shot names the hero photograph, as the sh- class defined in CEM_CSS.
    Empty means the cement banner the home page carries."""
    return """<section class="cmhero%s">
  <div class="hero-glow"></div>
  <div class="container">
    <div class="hero-eyebrow"><span class="dot"></span>%s</div>
    <h1>%s</h1>
    <p class="hero-sub">%s</p>
    <div class="hero-actions">%s</div>
  </div>
</section>
<div class="sun-divider"></div>
""" % (" sh-" + shot if shot else "", e(eyebrow), e(h1), e(sub), acts)


def cta_band(heading, para, acts):
    return """<section class="cta-band">
  <div class="container">
    <h2>%s</h2>
    <p>%s</p>
    <div class="cta-actions">%s</div>
  </div>
</section>
""" % (e(heading), e(para), acts)


def rows(items, two=False):
    cells = "".join('<div class="r"><b>%s</b>%s</div>' % (e(k), e(v)) for k, v in items)
    return '<div class="cmrows%s">%s</div>' % (" two" if two else "", cells)


def chips(items):
    return '<ul class="cmchips">%s</ul>' % "".join("<li>%s</li>" % e(i) for i in items)


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
    s += sec(rows(d["cfg_rows"], two=True), tag=d["cfg_tag"], h=d["cfg_h"],
             p=d["cfg_p"], **band("cfg_kiln"))

    s += cta_band(d["home_close_h"], d["home_close_p"],
                  btn(d["home_close_cta1"]) + " " + btn(d["home_close_cta2"], ghost=True))
    return s + footer(d) + tail(d)


# ================================================== PLATFORM CAPABILITY MAP
def capmap(d):
    """The platform capability map: administration and inputs, the three module
    columns either side of Core, and the shared facilities. This is the diagram the
    business plan carries as slide 5, as real bilingual markup rather than a raster,
    so the Arabic page gets Arabic and a phone gets a reflow."""
    def mod(cls, h, dd, cnt, items):
        c = '<div class="d">%s%s</div>' % (e(dd), (" · " + e(cnt)) if cnt else "")
        return ('<div class="cmmod %s"><h3>%s</h3>%s<ul>%s</ul></div>'
                % (cls, e(h), c, "".join("<li>%s</li>" % e(i) for i in items)))

    out = """<section class="band-alt">
  <div class="container">
    <div class="section-tag">%s</div>
    <h2 class="section-heading">%s</h2>
    <p class="section-sub">%s</p>

    <div class="cmtier">
      <div class="cmtier-h"><span class="cmtier-n">%s</span>
        <span class="cmtier-k">%s</span><span class="cmtier-a">%s</span></div>
      <div class="cmtier-who">%s</div>
      %s
      <p class="cmnote">%s</p>
    </div>

    <div class="cmtier">
      <div class="cmtier-h"><span class="cmtier-n">%s</span>
        <span class="cmtier-k">%s</span><span class="cmtier-a">%s</span></div>
      <div class="cmmods">%s%s%s</div>
    </div>

    <div class="cmtier">
      <div class="cmtier-h"><span class="cmtier-n">%s</span>
        <span class="cmtier-k">%s</span><span class="cmtier-a">%s</span></div>
      <div class="cmray">%s</div>
      %s
      <p class="cmnote">%s</p>
    </div>

    <div class="cmunits">%s</div>
  </div>
</section>
""" % (e(d["arch_tag"]), e(d["arch_h"]), e(d["arch_p"]),
       e(d["arch_t1_n"]), e(d["arch_t1_k"]), e(d["arch_t1_a"]), e(d["arch_t1_who"]),
       chips(d["arch_t1"]), e(d["arch_t1_note"]),
       e(d["arch_t2_n"]), e(d["arch_t2_k"]), e(d["arch_t2_a"]),
       mod("", d["arch_hz_h"], d["arch_hz_d"], d["arch_hz_c"], d["arch_hz"]),
       mod("core", d["arch_core_h"], d["arch_core_d"], "", d["arch_core"]),
       mod("", d["arch_pl_h"], d["arch_pl_d"], d["arch_pl_c"], d["arch_pl"]),
       e(d["arch_t3_n"]), e(d["arch_t3_k"]), e(d["arch_t3_a"]),
       e(d["arch_ray"]), chips(d["arch_t3"]), e(d["arch_t3_note"]),
       e(d["arch_units"]))
    return out


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
""" % (e(d["ev_up_tag"]), e(d["ev_up_h"]), e(d["ev_up_p"]),
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

    pd = "".join('<div class="p"><div class="k">%s</div><div class="v">%s</div></div>'
                 % (e(k), e(v)) for k, v in d["pd_rows"])

    if AGENDA_PUBLIC:
        programme = ("""<h3 class="sub-heading" style="margin-top:38px;font-size:22px;">%s</h3>
    <div class="cmag">%s</div>
    <p class="cmnote">%s</p>

    <h3 class="sub-heading" style="margin-top:38px;font-size:22px;">%s</h3>
    <div class="cmag">%s</div>
    <p class="cmnote">%s</p>
"""
                     % (e(d["eve_h"]), eve, e(d["eve_note"]),
                        e(d["ag_h"]), ag, e(d["ag_note"])))
    else:
        # .callout is the gold panel the home page already uses, so holding the
        # programme back needs no styling of its own.
        programme = ('<div class="callout"><h3>%s</h3><p>%s</p></div>\n'
                     % (e(d["ev_soon_h"]), e(d["ev_soon_p"])))

    s += """<section class="band-alt">
  <div class="container">
    <div class="cmev feat">
      <div class="cmbadge">%s</div>
      <h3>%s</h3>
      <p style="font-weight:700;color:var(--navy);">%s</p>
      <p style="margin-bottom:12px;">%s</p>
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
""" % (e(d["ev2_badge"]), e(d["ev2_h"]), e(d["ev2_kicker"]), e(d["ev2_line"]),
       e(d["ev2_when"]), e(d["ev2_time"]), e(d["ev2_place"]), e(d["ev2_dress"]),
       e(d["ev2_p"]), btn(d["ev2_cta1"]), btn(d["ev2_cta2"], ghost=True), e(d["ev2_note"]),
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
def sec(body, band="", tag="", h="", p="", lede=False, shot="", side="r", clip=""):
    """One section. band is "", "band-alt" or "band-warm"; p renders as the section
    sub, or as a lede paragraph when the copy is long enough to want the wider type.

    shot lays the section over a photograph the way the main site's industry pages
    do, and takes the image's path from the site root. side is the half of the
    frame the photograph keeps, "r" or "l"; the wash covers the other half and the
    copy sits there, so consecutive bands on a page alternate. A photograph
    replaces the band colour, so the two are never combined.

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
    return '<section%s>\n  <div class="container">\n%s    %s\n  </div>\n</section>\n' % (
        ' class="%s"' % band if band else "", top, body)


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
              shot="context")
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
              shot="capabilities")
    s += capmap(d)
    s += sec(stations("hz", d["cap_hz_groups"], d["cap_hz_run"], d["cap_hz_stops"]),
             "", d["cap_hz_tag"], d["cap_hz_h"], d["cap_hz_p"])
    s += sec(stations("pl", d["cap_pl_groups"], d["cap_pl_run"], d["cap_pl_stops"]),
             "band-alt", d["cap_pl_tag"], d["cap_pl_h"], d["cap_pl_p"])
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
