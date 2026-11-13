# -*- coding: utf-8 -*-
"""The cement production line, drawn flat and animated.

Seven stages from the quarry face to the loaded truck: quarry, crushing, raw
mill, preheater and kiln, cooler, cement mill, silo and dispatch. The belts
carry material, the mills and the kiln turn, the preheater smokes and the
flame breathes, so the figure reads as a plant running rather than a diagram
of one.

What joins two stages is drawn as what joins them on a real line, which is
also what fits: a sloped conveyor where there is room for one, a bucket
elevator where the lift is vertical, and nothing at all between the kiln and
the cooler, because the kiln nose discharges straight into it.

Drawn in the site's own three colours on cream, in the flat register of the
supplied mixer truck animation. The art is SVG and every label is positioned
HTML, the same split arch.py uses, so the words stay selectable text that
scales with the container and the Arabic page gets its own without a second
copy of the drawing.

Arabic mirrors for free: the labels sit on inset-inline-start, so they lay
themselves out from the other edge, and the drawing takes a scaleX(-1). The
numerals are drawn as HTML too, so the flip never reverses a digit.

Everything moves through CSS animation on a class, so one reduced-motion rule
stops all of it and leaves the figure legible and still.
"""

# The view starts just above the tallest thing drawn, the silo cap, so the
# figure does not open with a band of empty cream. Nothing is drawn below
# GROUND either: what follows it is the band the labels sit in, which the view
# reserves rather than letting them spill past the figure's own height.
VB_W = 2000
VB_Y, VB_H = 104, 596
GROUND = 480

GOLD, ORANGE, DEEP = "#E0B33A", "#F97316", "#C45213"
INK, SAND, CREAM = "#2A2520", "#EBD9B4", "#FFF6E2"
# SAND is a hair off the cream these sections are banded in, so anything
# structural drawn in it disappears. STONE is the same warmth a few steps
# down, dark enough to hold an edge; SAND stays for the small bright marks
# that sit on ink, the roller centres and the wheel hubs, and for the smoke.
STONE = "#D3B983"

# The seven stage centres: a 112 margin at each end, then an even pitch. Every
# machine is drawn inside roughly 80 either side of its centre, which leaves
# about 90 between neighbours for whatever carries material between them.
XS = [239, 493, 746, 1000, 1254, 1507, 1761]

LABELS = {
    "svg_aria": "The cement production line as one run: the quarry face, crushing, "
                "the raw mill, the preheater and kiln, the cooler, the cement mill, "
                "and the silo the truck loads from.",
    # The drawing is of the machines. The labels are the words the Pulse module
    # list uses, so the reader meets one vocabulary across the two figures. Two
    # of those modules cover two drawn stages each, and the name is split over
    # the pair: crushing and raw mix, pyro process and cooling.
    "s1": "Quarry",
    "s2": "Crushing",
    "s3": "Raw Mix",
    "s4": "Pyro Process",
    "s5": "Cooling",
    "s6": "Grinding and Product",
    "s7": "Packing and Dispatch",
    "s1_d": "Limestone won at the face",
    "s2_d": "Sized for the mill",
    "s3_d": "Ground and blended",
    "s4_d": "Raw meal burned to clinker",
    "s5_d": "Cooled, heat recovered",
    "s6_d": "Clinker ground to cement",
    "s7_d": "Held, loaded and released",
}

CSS = r"""
  /* CEMENT PRODUCTION LINE */
  .prc{position:relative;width:100%;max-width:1240px;margin:26px auto 0;
    aspect-ratio:2000/596;container-type:inline-size;}
  .prc svg{position:absolute;inset:0;width:100%;height:100%;}
  html[dir="rtl"] .prc svg{transform:scaleX(-1);}
  .prc-lab{position:absolute;transform:translateX(-50%);width:12%;text-align:center;}
  html[dir="rtl"] .prc-lab{transform:translateX(50%);}
  .prc-n{font-size:1.02cqw;font-weight:900;letter-spacing:.14em;color:var(--sun-deep);}
  .prc-t{font-size:1.30cqw;font-weight:900;line-height:1.2;color:var(--navy);
    margin-top:.2cqw;min-height:2.4em;}
  .prc-d{font-size:1.00cqw;font-weight:600;line-height:1.38;color:var(--text-muted);
    margin-top:.35cqw;}

  /* the belts, the drums, the kiln and the elevators all move by walking a dash
     pattern along their own path, which costs one property and never reflows */
  @keyframes prc-belt{to{stroke-dashoffset:-72;}}
  @keyframes prc-drum{to{stroke-dashoffset:-90;}}
  @keyframes prc-kiln{to{stroke-dashoffset:-120;}}
  @keyframes prc-lift{to{stroke-dashoffset:-64;}}
  @keyframes prc-fall{0%{opacity:0;transform:translateY(-12px);}
    20%{opacity:1;}80%{opacity:1;}100%{opacity:0;transform:translateY(24px);}}
  @keyframes prc-smoke{0%{opacity:0;transform:translateY(0) scale(.6);}
    30%{opacity:.42;}100%{opacity:0;transform:translateY(-82px) scale(1.8);}}
  @keyframes prc-flame{0%,100%{transform:scale(1,1);}50%{transform:scale(1.18,.84);}}
  @keyframes prc-glow{0%,100%{opacity:.5;}50%{opacity:1;}}
  .prc-belt{stroke-dasharray:13 15;animation:prc-belt 1.3s linear infinite;}
  .prc-spin{stroke-dasharray:16 20;animation:prc-drum 1.9s linear infinite;}
  .prc-band{stroke-dasharray:14 34;animation:prc-kiln 2.6s linear infinite;}
  .prc-lift{stroke-dasharray:12 20;animation:prc-lift 1.5s linear infinite;}
  .prc-fall circle{animation:prc-fall 1.5s linear infinite;}
  .prc-smoke circle{transform-box:fill-box;transform-origin:center;
    animation:prc-smoke 4.4s ease-out infinite;}
  .prc-flame{transform-box:fill-box;transform-origin:right center;
    animation:prc-flame 1.1s ease-in-out infinite;}
  .prc-hot{animation:prc-glow 2.2s ease-in-out infinite;}

  /* a reader who has asked for no motion gets the same plant, standing still */
  @media(prefers-reduced-motion:reduce){
    .prc-belt,.prc-spin,.prc-band,.prc-lift,.prc-fall circle,.prc-smoke circle,
    .prc-flame,.prc-hot{animation:none;}
  }
  /* the run is too wide to read on a narrow screen, so it scrolls as one piece
     rather than shrinking the labels past legibility. The width is held well
     above the viewport on purpose: the label sizes are container units, so a
     figure narrow enough to nearly fit would take the words down with it. */
  @media(max-width:900px){
    .prc-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch;
      scrollbar-width:thin;padding-bottom:10px;}
    .prc{width:1120px;max-width:none;}
  }
"""


def _conveyor(x1, y1, x2, y2):
    """A sloped belt between two stages: frame, material, head and tail rollers,
    and the A-frame it stands on."""
    mx, my = (x1 + x2) // 2, (y1 + y2) // 2
    out = ['<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="18"'
           ' stroke-linecap="round"/>' % (x1, y1, x2, y2, STONE),
           '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="9"'
           ' class="prc-belt"/>' % (x1, y1, x2, y2, DEEP)]
    for lx in (mx - 22, mx + 22):
        out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="6"'
                   ' opacity=".40"/>' % (mx, my + 8, lx, GROUND, INK))
    for cx, cy in ((x1, y1), (x2, y2)):
        out.append('<circle cx="%d" cy="%d" r="14" fill="%s"/>'
                   '<circle cx="%d" cy="%d" r="5" fill="%s"/>'
                   % (cx, cy, INK, cx, cy, SAND))
    return "".join(out)


def _elevator(x, top):
    """A bucket elevator: a closed shaft with the buckets climbing inside it.
    Drawn where the lift is vertical and no sloped belt would fit."""
    return ('<rect x="%d" y="%d" width="36" height="%d" rx="8" fill="%s"/>'
            '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="13"'
            ' class="prc-lift"/>'
            '<rect x="%d" y="%d" width="48" height="18" rx="5" fill="%s"/>'
            % (x - 18, top, GROUND - top, STONE,
               x, GROUND - 16, x, top + 16, DEEP,
               x - 24, top - 14, INK))


def _fall(x, y, n, fill, spread=13, r=5):
    """Material dropping through air, used wherever one stage feeds the next."""
    return ('<g class="prc-fall">'
            + "".join('<circle cx="%d" cy="%d" r="%d" fill="%s"'
                      ' style="animation-delay:%.2fs"/>'
                      % (x + (i - (n - 1) / 2) * spread, y, r, fill, i * 0.33)
                      for i in range(n))
            + "</g>")


def _hopper(x, y, w, h, fill):
    return ('<path d="M%d %d H%d L%d %d H%d Z" fill="%s"/>'
            % (x - w // 2, y, x + w // 2, x + w // 4, y + h, x - w // 4, fill))


def _quarry(x):
    """Three benches stepping up to the right, a shovel working the top one."""
    b = GROUND
    face = ('<path d="M%d %d V%d H%d V%d H%d V%d H%d V%d Z" fill="%s"/>'
            % (x - 78, b, b - 38, x - 36, b - 76, x + 6, b - 114, x + 78, b, STONE))
    treads = ('<path d="M%d %d H%d M%d %d H%d M%d %d H%d" stroke="%s" stroke-width="4"'
              ' opacity=".26" fill="none"/>'
              % (x - 78, b - 38, x - 36, x - 36, b - 76, x + 6,
                 x + 6, b - 114, x + 78, INK))
    shovel = ('<rect x="%d" y="%d" width="34" height="20" rx="5" fill="%s"/>'
              '<path d="M%d %d L%d %d" stroke="%s" stroke-width="7"'
              ' stroke-linecap="round"/>'
              '<circle cx="%d" cy="%d" r="8" fill="%s"/>'
              % (x + 26, b - 134, GOLD, x + 34, b - 128, x + 2, b - 104, GOLD,
                 x + 2, b - 104, DEEP))
    rubble = "".join('<circle cx="%d" cy="%d" r="%d" fill="%s" opacity=".9"/>'
                     % (x - 70 + i * 15, b - 7 - (i % 3) * 5, 5 + (i % 3), DEEP)
                     for i in range(5))
    return face + treads + shovel + _fall(x + 2, b - 92, 2, DEEP, 11, 4) + rubble


def _crusher(x):
    """A feed hopper over a jaw, the teeth biting inside it."""
    b = GROUND
    return "".join([
        _fall(x, b - 168, 3, DEEP),
        _hopper(x, b - 152, 112, 66, GOLD),
        '<rect x="%d" y="%d" width="108" height="84" rx="9" fill="%s"/>'
        % (x - 54, b - 84, INK),
        '<path d="M%d %d l12 17 l12 -17 l12 17 l12 -17 l12 17 l12 -17" fill="none"'
        ' stroke="%s" stroke-width="5" stroke-linecap="round"/>' % (x - 36, b - 55, ORANGE),
    ])


def _drum(x, tone):
    """A horizontal mill: a rounded tube with its shell turning on two piers."""
    b = GROUND
    y = b - 104
    return "".join([
        '<rect x="%d" y="%d" width="116" height="26" rx="6" fill="%s"/>'
        % (x - 58, b - 26, INK),
        '<rect x="%d" y="%d" width="136" height="70" rx="35" fill="%s"/>'
        % (x - 68, y, tone),
        '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="54"'
        ' class="prc-spin" opacity=".38"/>' % (x - 54, y + 35, x + 54, y + 35, INK),
        '<rect x="%d" y="%d" width="14" height="90" rx="5" fill="%s"/>'
        '<rect x="%d" y="%d" width="14" height="90" rx="5" fill="%s"/>'
        % (x - 80, y - 10, INK, x + 66, y - 10, INK),
    ])


def _kiln(x):
    """The elevator, the preheater tower it fills, and the tilted kiln below,
    burning back from the nose that discharges into the cooler."""
    b = GROUND
    tx = x - 72
    out = [_elevator(tx - 46, b - 266)]
    # the piers the kiln rides on, the right one shorter because it runs downhill
    out.append('<rect x="%d" y="%d" width="34" height="78" rx="5" fill="%s"/>'
               % (x + 24, b - 78, INK))
    out.append('<rect x="%d" y="%d" width="34" height="66" rx="5" fill="%s"/>'
               % (x + 144, b - 66, INK))
    # the kiln: one long tube on a six degree fall from the tower to the cooler.
    # Its upper end runs back under the tower, which is drawn over it, so the two
    # meet instead of standing a gap apart.
    out.append('<g transform="rotate(6 %d %d)">' % (x + 40, b - 100))
    out.append('<rect x="%d" y="%d" width="292" height="56" rx="28" fill="%s"/>'
               % (x - 70, b - 128, DEEP))
    out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="44"'
               ' class="prc-band" opacity=".45"/>' % (x - 6, b - 100, x + 202, b - 100, ORANGE))
    for rx in (x + 28, x + 148):
        out.append('<rect x="%d" y="%d" width="15" height="64" rx="4" fill="%s"'
                   ' opacity=".85"/>' % (rx, b - 132, INK))
    out.append('<ellipse cx="%d" cy="%d" rx="12" ry="24" fill="%s" class="prc-hot"/>'
               % (x + 222, b - 100, ORANGE))
    out.append('<path d="M%d %d c-22 -13 -46 -13 -64 0 c18 13 42 13 64 0 Z" fill="%s"'
               ' class="prc-flame"/>' % (x + 224, b - 100, GOLD))
    out.append("</g>")
    # the tower: a column of four cyclone cones, smoking at the top
    out.append('<rect x="%d" y="%d" width="54" height="238" rx="8" fill="%s"/>'
               % (tx - 27, b - 258, STONE))
    for i in range(4):
        cy = b - 240 + i * 56
        out.append('<path d="M%d %d H%d L%d %d H%d Z" fill="%s"/>'
                   % (tx - 33, cy, tx + 33, tx + 13, cy + 38, tx - 13, GOLD))
    out.append('<rect x="%d" y="%d" width="22" height="34" rx="4" fill="%s"/>'
               % (tx - 11, b - 290, INK))
    out.append('<g class="prc-smoke">'
               + "".join('<circle cx="%d" cy="%d" r="%d" fill="%s"'
                         ' style="animation-delay:%.1fs"/>'
                         % (tx + (i % 2) * 11 - 5, b - 298, 13 + i * 3, SAND, i * 1.1)
                         for i in range(4))
               + "</g>")
    return "".join(out)


def _cooler(x):
    """A stepped grate in a box under the kiln nose, the clinker cooling down it."""
    b = GROUND
    out = [_fall(x - 58, b - 122, 3, ORANGE, 15)]
    for i in range(4):
        sx, sy = x - 76 + i * 40, b - 102 + i * 16
        out.append('<rect x="%d" y="%d" width="36" height="17" fill="%s"/>'
                   % (sx, sy, STONE))
        out.append('<rect x="%d" y="%d" width="36" height="6" fill="%s" opacity="%.2f"'
                   ' class="prc-hot" style="animation-delay:%.1fs"/>'
                   % (sx, sy - 6, ORANGE, 1 - i * 0.18, i * 0.4))
    out.append('<rect x="%d" y="%d" width="12" height="56" rx="3" fill="%s"/>'
               '<rect x="%d" y="%d" width="12" height="56" rx="3" fill="%s"/>'
               % (x - 86, b - 104, INK, x + 74, b - 104, INK))
    out.append('<rect x="%d" y="%d" width="172" height="52" rx="8" fill="%s"/>'
               % (x - 86, b - 52, INK))
    return "".join(out)


def _silo(x):
    """The silo on its legs, and the truck loading under the chute, drum turning."""
    b = GROUND
    out = [_elevator(x - 96, b - 318)]
    out.append('<rect x="%d" y="%d" width="104" height="170" rx="10" fill="%s"/>'
               % (x - 72, b - 340, STONE))
    out.append('<rect x="%d" y="%d" width="112" height="16" rx="6" fill="%s"/>'
               % (x - 76, b - 354, INK))
    for i in range(3):
        out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="3"'
                   ' opacity=".24"/>' % (x - 72, b - 298 + i * 42, x + 32, b - 298 + i * 42, INK))
    out.append('<path d="M%d %d H%d L%d %d H%d Z" fill="%s"/>'
               % (x - 72, b - 170, x + 32, x - 10, b - 128, x - 30, GOLD))
    for lx in (x - 68, x + 18):
        out.append('<rect x="%d" y="%d" width="14" height="170" fill="%s" opacity=".9"/>'
                   % (lx, b - 170, INK))
    out.append('<rect x="%d" y="%d" width="24" height="16" rx="3" fill="%s"/>'
               % (x - 32, b - 128, INK))
    out.append(_fall(x - 20, b - 112, 2, SAND, 12, 4))
    # the mixer truck, drawn in the register of the supplied animation, facing out
    tx = x + 4
    out.append('<rect x="%d" y="%d" width="124" height="22" rx="6" fill="%s"/>'
               % (tx - 62, b - 44, INK))
    out.append('<g transform="rotate(-14 %d %d)">'
               '<rect x="%d" y="%d" width="92" height="56" rx="27" fill="%s"/>'
               '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="42"'
               ' class="prc-spin" opacity=".38"/></g>'
               % (tx - 16, b - 70, tx - 62, b - 96, GOLD,
                  tx - 46, b - 68, tx + 14, b - 68, DEEP))
    out.append('<rect x="%d" y="%d" width="42" height="42" rx="7" fill="%s"/>'
               '<rect x="%d" y="%d" width="24" height="17" rx="3" fill="%s"/>'
               % (tx + 22, b - 86, GOLD, tx + 32, b - 80, INK))
    for wx in (tx - 44, tx + 6, tx + 38):
        out.append('<circle cx="%d" cy="%d" r="14" fill="%s"/>'
                   '<circle cx="%d" cy="%d" r="5" fill="%s"/>'
                   % (wx, b - 16, INK, wx, b - 16, SAND))
    return "".join(out)


STAGES = [_quarry, _crusher, lambda x: _drum(x, GOLD), _kiln, _cooler,
          lambda x: _drum(x, DEEP), _silo]

# What joins one stage to the next, where a sloped belt is what joins them. The
# rest are drawn inside their own stage: the two bucket elevators stand against
# the tower and the silo they fill, and the kiln nose discharges straight into
# the cooler, so there is nothing between four and five to draw.
BELTS = [(317, GROUND - 116, 437, GROUND - 152),
         (547, GROUND - 90, 666, GROUND - 120),
         (1340, GROUND - 70, 1427, GROUND - 114)]


def figure(labels=None):
    """The drawing plus its seven HTML labels, as one block."""
    L = dict(LABELS, **(labels or {}))
    s = ['<div class="prc-wrap"><div class="prc">',
         '<svg viewBox="0 %d %d %d" role="img" aria-label="%s">'
         % (VB_Y, VB_W, VB_H, L["svg_aria"])]
    s.append('<line x1="40" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="4"'
             ' opacity=".34"/>' % (GROUND, VB_W - 40, GROUND, INK))
    for b in BELTS:
        s.append(_conveyor(*b))
    for draw, x in zip(STAGES, XS):
        s.append(draw(x))
    s.append("</svg>")
    for i, x in enumerate(XS, 1):
        s.append('<div class="prc-lab" style="inset-inline-start:%.2f%%;top:%.1f%%">'
                 '<div class="prc-n">%02d</div><div class="prc-t">%s</div>'
                 '<div class="prc-d">%s</div></div>'
                 % (x / VB_W * 100, (GROUND + 46 - VB_Y) / VB_H * 100, i,
                    L["s%d" % i], L["s%d_d" % i]))
    s.append("</div></div>")
    return "".join(s)
