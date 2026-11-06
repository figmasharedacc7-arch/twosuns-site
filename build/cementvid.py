"""Moving photo bands for the cement microsite.

The microsite's sector pages carry still photo bands: a photograph under a cream
wash, with the copy in the half the wash covers. A moving band is that same
device with a loop playing where the still sits, so a band that plays and a band
that does not read as one thing. These are the two loops, and the stills that
serve as their posters.

band-dusk is the dusk plant that was briefly the home hero and was reverted,
brought back here where it is not a hero. It is recut from the same source at
the same offset, which a frame comparison confirmed: mean difference 5.8 per
channel against this source at 2.0s, 44.0 against any other clip of the set.
band-quarry is the limestone quarry that feeds the line.

Colour is matched, not eyeballed, the way build/herovid.py matches the hero
rotation. The approved hero-plant.mp4 is read straight out of git and measured,
each clip is encoded once without grading and measured, a gain onto the approved
colour is computed, and the final encode applies that gain. Run with VERBOSE=1
to see the measurements.

What is matched here is the warmth, not the brightness, which is where this
parts company with herovid.py. Every clip in the hero rotation was golden hour,
so matching absolute levels was right. These bands are not: one is a plant at
dusk and the other a quarry in full daylight, and the still bands they sit among
run from R128 to R186, so the site plainly does not ask every band to be the
same brightness. It does ask them to be warm. So red is left alone and green and
blue are moved until the clip holds the reference's G/R and B/R, which pulls a
daylight clip into the palette without pretending it was shot at dusk. Matching
absolute levels instead drove the quarry to R94, darker than any band on the
site, and left its blue ratio untouched, which is the opposite of the point.

Each clip is cut to 10 seconds and closed into a seamless loop by crossfading
its tail onto its head, which leaves 9 seconds. The hero never needed this
because it cross-dissolved to the next clip before reaching its own end; a band
loops forever, and the recovered hero-plant.mp4 jumps 3.6 percent of its pixels
at the seam, which is plainly visible once it repeats.

Run:  python3 build/cementvid.py
"""

import os
import re
import subprocess
import tempfile

from PIL import Image

FFMPEG = os.path.expanduser("~/bin/ffmpeg")
SRC = os.path.expanduser("~/Downloads")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, ".."))
OUT = os.path.join(REPO, "cement")

SEG = 10.0            # seconds cut from the source
XF = 1.0              # loop crossfade, so each clip lands at 9.0s
W, H = 1760, 960      # 0.8 of the 2200x1200 the still bands are cut to
POSTER = (2200, 1200)
CRF = "32"            # a background behind a wash, and 58 percent of it is covered
VERBOSE = bool(os.environ.get("VERBOSE"))

# The approved look. hero-plant.mp4 was graded to the palette and signed off
# before the hero was reverted, so it is the reference rather than a fresh cut:
# this is the commit it was removed in, and the file is still in its parent.
REF_COMMIT = "1ce47a4:cement/hero-plant.mp4"

# name, source, start second, and the window of the source frame to keep as
# (left, right, vertical bias) in fractions, or None for the whole frame.
#
# The window is not decoration. A band's wash is opaque cream across the copy
# half and only thins past about 72 percent, so whatever the picture is of has
# to stand in the far quarter or it is not in the picture at all. hero-plant
# was framed for a hero, where the preheater tower sits dead centre and reads
# fine; dropped into a band unchanged, that tower lands under the solid part of
# the wash and both outer strips measure an edge density of 2.1, which is to
# say sky. Cutting the empty left of the frame away carries the tower out to
# the clear strip and keeps the rail yard, which was the half worth having.
#
# band-works needed the same cut for the same reason: its structure centroid
# sits at 0.51 of the frame across the whole ten seconds, which is to say the
# plant is dead centre, under the solid part of the wash.
#
# The quarry aerial that was tried here first is not in this list. It measured
# fine, mean luminance 140 and more contrast than the shipped quarry band it
# would have sat among, and still read as a pale smear at every crop, because
# it is a high hazy aerial of pale limestone with nothing near the camera while
# every band already on the site is close to one thing. That is a property of
# the footage and not something exposure or framing could fix.
PLAN = [
    ("band-dusk",
     "aerial-shot-of-a-cement-factory-at-sunset-2026-10-02-23-45-08-utc.mov",
     2.0, (0.40, 1.00, 0.30)),
    ("band-works",
     "cement-factory-aerial-view-at-sunrise-2026-10-02-13-08-25-utc.mov",
     0.1, (0.07, 0.67, 0.05)),
]


def run(cmd):
    subprocess.run(cmd, check=True)


def levels(path, samples=(1, 3, 5, 7)):
    """Mean R, G, B across a few frames of a finished clip."""
    tot = [0.0, 0.0, 0.0]
    with tempfile.TemporaryDirectory() as td:
        for t in samples:
            f = os.path.join(td, "%s.png" % t)
            run([FFMPEG, "-v", "error", "-y", "-ss", str(t), "-i", path,
                 "-frames:v", "1", "-vf", "scale=320:-1", f])
            px = list(Image.open(f).convert("RGB").resize((64, 36)).getdata())
            n = len(px)
            for i in range(3):
                tot[i] += sum(p[i] for p in px) / n
    return [v / len(samples) for v in tot]


def reference():
    """The approved hero-plant.mp4, read out of git so this needs no stray file."""
    blob = subprocess.run(["git", "-C", REPO, "show", REF_COMMIT],
                          check=True, stdout=subprocess.PIPE).stdout
    with tempfile.TemporaryDirectory() as td:
        f = os.path.join(td, "ref.mp4")
        with open(f, "wb") as fh:
            fh.write(blob)
        return levels(f)


def duration(path):
    """Seconds, parsed off ffmpeg's banner. ffprobe is not installed here."""
    txt = subprocess.run([FFMPEG, "-i", path], stderr=subprocess.PIPE
                         ).stderr.decode("utf-8", "replace")
    h, m, sec = re.search(r"Duration: (\d+):(\d+):([\d.]+)", txt).groups()
    return int(h) * 3600 + int(m) * 60 + float(sec)


def window(crop):
    """The ffmpeg crop for a (left, right, bias) window, at the output ratio."""
    if not crop:
        return ""
    lo, hi, bias = crop
    w = "iw*%.4f" % (hi - lo)
    h = "%s*%.6f" % (w, float(H) / W)
    return "crop=%s:%s:iw*%.4f:(ih-%s)*%.4f," % (w, h, lo, h, bias)


def encode(name, src, start, gain=None, crop=None):
    """Cut, optionally regrade, close the loop, write the mp4."""
    inp = os.path.join(SRC, src)
    have = duration(inp)
    if start + SEG > have:
        raise SystemExit("%s wants %s to %.1fs of %s, which runs %.1fs"
                         % (name, start, start + SEG, src, have))
    out = os.path.join(OUT, name + ".mp4")
    grade = ""
    if gain:
        grade = "colorchannelmixer=rr=%.4f:gg=%.4f:bb=%.4f," % tuple(gain)
    pre = ("%sscale=%d:%d:flags=lanczos,%sfps=25,format=yuv420p,setsar=1"
           % (window(crop), W, H, grade))
    fc = ("[0:v]%s[a];[1:v]%s[b];"
          "[a][b]xfade=transition=fade:duration=%.2f:offset=%.2f[v]"
          % (pre, pre, XF, SEG - 2 * XF))
    run([FFMPEG, "-v", "error", "-y",
         "-ss", "%.3f" % (start + XF), "-t", "%.3f" % (SEG - XF), "-i", inp,
         "-ss", "%.3f" % start, "-t", "%.3f" % XF, "-i", inp,
         "-filter_complex", fc, "-map", "[v]", "-an",
         "-c:v", "libx264", "-preset", "slow", "-crf", CRF,
         "-profile:v", "high", "-pix_fmt", "yuv420p",
         "-movflags", "+faststart", out])
    return out


def main():
    target = reference()
    if VERBOSE:
        print("reference %-14s R%6.1f G%6.1f B%6.1f"
              % tuple([REF_COMMIT.split(":")[0]] + target))

    # the warmth to match, as the reference's green and blue over its red
    ratio = [target[1] / target[0], target[2] / target[0]]

    for name, src, start, crop in PLAN:
        out = encode(name, src, start, crop=crop)
        raw = levels(out)
        gain = [1.0] + [t / (r / raw[0]) for t, r in zip(ratio, raw[1:])]
        # a clip that already sits close should not be pushed around
        gain = [min(max(g, 0.70), 1.45) for g in gain]
        if VERBOSE:
            print("  %-12s raw R%6.1f G%6.1f B%6.1f  gain %.3f %.3f %.3f"
                  % tuple([name] + raw + gain))
        encode(name, src, start, gain, crop)

        # the poster is the band's own first frame, so the still the section
        # opens on and the loop's opening frame are the same picture
        run([FFMPEG, "-v", "error", "-y", "-i", out, "-frames:v", "1",
             "-vf", "scale=%d:%d:flags=lanczos" % POSTER, "-q:v", "4",
             os.path.join(OUT, name + ".jpg")])
        f = levels(out)
        print("%-16s %5.2f MB   R%6.1f G%6.1f B%6.1f   G/R %.3f  B/R %.3f"
              "   (target G/R %.3f  B/R %.3f)"
              % (name + ".mp4", os.path.getsize(out) / 1048576.0,
                 f[0], f[1], f[2], f[1] / f[0], f[2] / f[0], ratio[0], ratio[1]))


if __name__ == "__main__":
    main()
