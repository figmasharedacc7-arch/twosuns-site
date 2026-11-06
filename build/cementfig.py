"""The mixer truck figure on the cement concrete page.

The source is a supplied ProRes 4444 loop of a concrete mixing truck with a
real alpha channel. This ffmpeg cannot write VP9 alpha into WebM, which was
checked against a synthetic alpha clip rather than assumed, and the HEVC route
it can write it cannot read back, so none of it is verifiable from here. The
way out is that the figure does not need alpha: the section it sits in paints
one flat colour, measured off the rendered page at #FFF5DD across 60000 of
60000 sampled pixels, so the truck is composited onto that colour and every
edge of the video is the page's own background.

Two things are done to the frames on the way through.

The hazard stripes were red, and red is banned site wide, so they are turned
orange. The mask is the narrow one: true red is the only thing on this truck
with r-g over 130 that still keeps some blue, while every orange on the body
has effectively no blue at all. A looser mask was tried first and turned the
whole truck yellow, then a second one turned the shadowed drum olive. This one
was checked by rendering the mask itself as an image, where it fires on the
stripes and nothing else, and it takes true red from 1.354 percent of the truck
to 0.002 percent.

The truck is then stood on a ground line, because a vehicle floating on a flat
field reads as a sticker. The line is drawn with its alpha ramped to nothing at
both ends. Drawn flat it ran the full width and stopped dead at the frame edge,
which draws the one thing the flat composite exists to hide, the rectangle.

Run:  python3 build/cementfig.py /path/to/concrete-mixing-truck.mov
"""

import os
import subprocess
import sys

FFMPEG = os.path.expanduser("~/bin/ffmpeg")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.normpath(os.path.join(HERE, "..")), "cement")

W, H = 1110, 612
CROP = "crop=1480:816:228:148"     # the truck, out of the 1920x1080 source
BG = "0xFFF5DD"                    # measured off the rendered section
CRF = "25"

GROUND_Y = 584                     # where the wheels meet
GROUND_A = 0.34
FADE = 320                         # pixels the line takes to reach full strength

# true red is the only thing with r-g>130 that also keeps blue; every orange on
# the truck has b/g near zero, so this fires on the hazard stripes alone
MASK = "gt(r(X,Y)-g(X,Y),130)*gt(b(X,Y)*2,g(X,Y))"
GRADE = ("format=rgba,geq=r='r(X,Y)':g='g(X,Y)+0.37*r(X,Y)*(%s)'"
         ":b='b(X,Y)*(1-0.1*(%s))':a='alpha(X,Y)'" % (MASK, MASK))

# the line, as its own source, with alpha ramped from nothing at each end
LINE = ("color=c=0x2A2520:s=%dx3:r=25,format=rgba,"
        "geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)'"
        ":a='%.3f*min(1,min(X,%d-X)/%d)'" % (W, 255 * GROUND_A, W, FADE))


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__.strip().splitlines()[-1])
    src = sys.argv[1]
    out = os.path.join(OUT, "mixer-truck.mp4")
    fc = ("[0:v]%s,%s,scale=%d:%d,fps=25[t];"
          "[1:v][2:v]overlay=0:%d[bg];"
          "[bg][t]overlay=0:0:shortest=1,format=yuv420p"
          % (CROP, GRADE, W, H, GROUND_Y))
    subprocess.run([FFMPEG, "-v", "error", "-y", "-i", src,
                    "-f", "lavfi", "-i", "color=c=%s:s=%dx%d:r=25" % (BG, W, H),
                    "-f", "lavfi", "-i", LINE,
                    "-filter_complex", fc,
                    "-c:v", "libx264", "-crf", CRF, "-preset", "veryslow",
                    "-an", "-movflags", "+faststart", out], check=True)
    # the poster is the frame the loop opens on, so the still the figure shows
    # before it plays and the still reduced motion keeps are the same picture
    subprocess.run([FFMPEG, "-v", "error", "-y", "-i", out, "-frames:v", "1",
                    "-q:v", "4", os.path.join(OUT, "mixer-truck.jpg")], check=True)
    print("mixer-truck.mp4  %.2f MB" % (os.path.getsize(out) / 1048576.0))


if __name__ == "__main__":
    main()
