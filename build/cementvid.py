"""Moving photo bands and heroes for the cement microsite.

The microsite's sector pages carry still photo bands: a photograph under a cream
wash, with the copy in the half the wash covers. A moving band is that same
device with a loop playing where the still sits, so a band that plays and a band
that does not read as one thing. The context hero is the same device again at
hero size. These are the three loops, and the stills that serve as their
posters.

band-dusk is the dusk plant that was briefly the home hero and was reverted,
brought back here where it is not a hero. It is recut from the same source at
the same offset, which a frame comparison confirmed: mean difference 5.8 per
channel against this source at 2.0s, 44.0 against any other clip of the set.
band-works is the works seen from the air at sunrise. context-hero is a drone
orbit of a plant at sunrise, cut to start after its chimney has left frame,
because the page it opens is the one arguing about cost and CO2 per tonne.

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

Every clip here loops forever, so every clip has to close on itself. The
recovered hero-plant.mp4 jumps 3.6 percent of its pixels at its seam, which is
plainly visible once it repeats, and that is what each entry's loop mode is
avoiding.

The bands are cut to 10 seconds and crossfade their own tail onto their head,
which leaves 9. That works because their cameras barely travel.

The context hero does not: its drone orbits far enough in nine seconds that
the dissolve put two towers on screen at once, a plain double exposure rather
than a loop, and measuring the first frame against the last missed it entirely
because a crossfade lands on the opening frame by construction. It is cut to 7
seconds and boomeranged instead, playing forward and then backward to 13.96,
which returns to frame one by retracing its own path and leaves no seam to
measure. The motion reverses, which reads as natural on a slow orbit and would
not on a shot with a clear direction of travel.

This is the same thing bandvid.py does for vid-port on the main site.

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
CRF = "23"            # a wash covers the copy half, the other half is not covered
VERBOSE = bool(os.environ.get("VERBOSE"))

# Output shape, as (width, height, poster width, poster height). A band and a
# hero are cut to different ratios on this site and always have been, so the
# shape belongs to the entry rather than to the module: the still bands are
# 11:6 and the hero stills are a flat 2:1. The hero is 1920 wide because its
# source is, and upscaling a 1080p master to 2560 spends bytes inventing
# detail that is not in the file.
BAND = (2560, 1396, 2200, 1200)
HERO = (1920, 960, 2000, 1000)

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
     2.0, (0.40, 1.00, 0.30), BAND, SEG, "xfade"),
    ("band-works",
     "cement-factory-aerial-view-at-sunrise-2026-10-02-13-08-25-utc.mov",
     0.1, (0.07, 0.67, 0.05), BAND, SEG, "xfade"),
    # The context hero. Supplied for this page: a slow drone orbit of a
    # preheater tower with the sun on the horizon, which is the warmth every
    # other hero on the microsite already has, so it needs no regrade to join
    # them and gets one anyway for the same reason the bands do.
    #
    # It starts at 3.5s, not at 0. The first three seconds carry a stack with
    # a white plume across the clear half of the frame, and a page that sells
    # CO2 per tonne of cement should not open on a smoking chimney. The stack
    # leaves frame between 3.0 and 3.5 and does not come back. 3.5 is also the
    # latest start the source allows: it runs 13.95s and SEG is 10.
    #
    # The window is the full width, which is what the (0, 1) means, cropped
    # down the middle to 2:1 and biased up the frame so the cut keeps the sun,
    # the horizon and the top of the tower rather than more of the yard. The
    # tower already stands at about 0.8 across, which is the strip the wash
    # leaves clear, so unlike the two bands there is nothing to carry outwards.
    ("context-hero",
     "aerial-view-of-cement-factory-at-sunrise-or-sunset-2026-10-01-14-57-45-utc.mov",
     3.5, (0.00, 1.00, 0.35), HERO, 7.0, "boomerang"),
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


def window(crop, shape):
    """The ffmpeg crop for a (left, right, bias) window, at the output ratio."""
    if not crop:
        return ""
    w_out, h_out = shape[0], shape[1]
    lo, hi, bias = crop
    w = "iw*%.4f" % (hi - lo)
    h = "%s*%.6f" % (w, float(h_out) / w_out)
    return "crop=%s:%s:iw*%.4f:(ih-%s)*%.4f," % (w, h, lo, h, bias)


def encode(name, src, start, shape, seg, mode, gain=None, crop=None):
    """Cut, optionally regrade, close the loop, write the mp4.

    Two ways to close it, because one does not suit every shot.

    "xfade" dissolves the clip's tail onto its own head and drops the overlap,
    so seg seconds in gives seg minus XF out. It is the cheaper loop and it is
    right when the camera barely travels, which is the case for both bands.

    "boomerang" plays the cut and then plays it backwards, so the clip returns
    to its first frame by retracing its own path and there is no seam at all.
    It is what the main site's vid-port does. The cost is that the motion
    reverses, which reads as natural on a slow orbit and silly on anything
    with a clear direction of travel, and that the file holds twice the
    frames. The context hero needs it: its drone travels far enough in nine
    seconds that a one second dissolve put two towers on screen at once, a
    plain double exposure rather than a loop."""
    inp = os.path.join(SRC, src)
    have = duration(inp)
    if start + seg > have:
        raise SystemExit("%s wants %s to %.1fs of %s, which runs %.1fs"
                         % (name, start, start + seg, src, have))
    out = os.path.join(OUT, name + ".mp4")
    grade = ""
    if gain:
        grade = "colorchannelmixer=rr=%.4f:gg=%.4f:bb=%.4f," % tuple(gain)
    pre = ("%sscale=%d:%d:flags=lanczos,%sfps=25,format=yuv420p,setsar=1"
           % (window(crop, shape), shape[0], shape[1], grade))
    if mode == "boomerang":
        # trim the reversed copy's first frame, which is the forward copy's
        # last, or the clip holds that frame for two frames at the turn
        fc = ("[0:v]%s,split[a][b];"
              "[b]reverse,trim=start_frame=1,setpts=PTS-STARTPTS[r];"
              "[a][r]concat=n=2:v=1:a=0[v]" % pre)
        ins = ["-ss", "%.3f" % start, "-t", "%.3f" % seg, "-i", inp]
    else:
        fc = ("[0:v]%s[a];[1:v]%s[b];"
              "[a][b]xfade=transition=fade:duration=%.2f:offset=%.2f[v]"
              % (pre, pre, XF, seg - 2 * XF))
        ins = ["-ss", "%.3f" % (start + XF), "-t", "%.3f" % (seg - XF), "-i", inp,
               "-ss", "%.3f" % start, "-t", "%.3f" % XF, "-i", inp]
    run([FFMPEG, "-v", "error", "-y"] + ins +
        ["-filter_complex", fc, "-map", "[v]", "-an",
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

    for name, src, start, crop, shape, seg, mode in PLAN:
        out = encode(name, src, start, shape, seg, mode, crop=crop)
        raw = levels(out)
        gain = [1.0] + [t / (r / raw[0]) for t, r in zip(ratio, raw[1:])]
        # a clip that already sits close should not be pushed around
        gain = [min(max(g, 0.70), 1.45) for g in gain]
        if VERBOSE:
            print("  %-12s raw R%6.1f G%6.1f B%6.1f  gain %.3f %.3f %.3f"
                  % tuple([name] + raw + gain))
        encode(name, src, start, shape, seg, mode, gain, crop)

        # the poster is the band's own first frame, so the still the section
        # opens on and the loop's opening frame are the same picture
        run([FFMPEG, "-v", "error", "-y", "-i", out, "-frames:v", "1",
             "-vf", "scale=%d:%d:flags=lanczos" % (shape[2], shape[3]),
             "-q:v", "4",
             os.path.join(OUT, name + ".jpg")])
        f = levels(out)
        print("%-16s %5.2f MB   R%6.1f G%6.1f B%6.1f   G/R %.3f  B/R %.3f"
              "   (target G/R %.3f  B/R %.3f)"
              % (name + ".mp4", os.path.getsize(out) / 1048576.0,
                 f[0], f[1], f[2], f[1] / f[0], f[2] / f[0], ratio[0], ratio[1]))


if __name__ == "__main__":
    main()
