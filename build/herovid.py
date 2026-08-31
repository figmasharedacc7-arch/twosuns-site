"""Hero rotation clips.

The hero cycles through three golden-hour built-industry clips. hero-build.mp4
came first and is left exactly as approved, so this script only produces the two
that join it. Sources are the Envato originals in ~/Downloads.

Selection rule: the rotation has to read as one continuous mood, not a stock
slideshow, so every clip is golden hour, wide and slow. Candidates were ranked
by measured mean colour against hero-build and only the near matches were kept.

Colour is matched, not eyeballed. Each clip is encoded once without grading, its
mean channel levels are measured, a per-channel gain onto hero-build's levels is
computed, and the final encode applies that gain. Run with VERBOSE=1 to see the
measurements.

Each clip is cut to 10 seconds and closed into a seamless loop by crossfading its
tail onto its head, which leaves 9 seconds. The rotator holds a clip for 7.5s so
it never reaches its own loop point in normal use; the loop is insurance against
timing drift.

Run:  python3 herovid.py
"""

import os
import subprocess
import tempfile

from PIL import Image

FFMPEG = os.path.expanduser("~/bin/ffmpeg")
SRC = os.path.expanduser("~/Downloads")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, ".."))

SEG = 10.0        # seconds cut from the source
XF = 1.0          # loop crossfade, so each clip lands at 9.0s
W, H = 1920, 1080
CRF = "27"
VERBOSE = bool(os.environ.get("VERBOSE"))

# the levels every hero clip is matched to, measured off hero-build.mp4
REFERENCE = "hero-build.mp4"

# hero-build.mp4 was cut from apartment-construction-site-at-golden-sunset, which
# a frame comparison confirmed (mean difference 1.4 per channel against that
# source, 35.4 against any other). That source is therefore off limits here, a
# second window of it would read as the hero stuttering rather than rotating.
PLAN = [
    ("hero-crane",
     "building-construction-crane-sunset-industrial-arch-2026-01-21-05-37-07-utc.mov",
     6.0),
    ("hero-rise",
     "aerial-shot-of-a-new-high-rise-building-under-cons-2025-12-17-13-51-59-utc.mp4",
     1.0),
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


def encode(name, src, start, gain=None):
    """Cut, optionally regrade, close the loop, write the mp4."""
    inp = os.path.join(SRC, src)
    out = os.path.join(OUT, name + ".mp4")
    grade = ""
    if gain:
        grade = "colorchannelmixer=rr=%.4f:gg=%.4f:bb=%.4f," % tuple(gain)
    pre = "scale=%d:%d:flags=lanczos,%sfps=30,format=yuv420p,setsar=1" % (W, H, grade)
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
    target = levels(os.path.join(OUT, REFERENCE))
    if VERBOSE:
        print("reference %-14s R%6.1f G%6.1f B%6.1f" % tuple([REFERENCE] + target))

    for name, src, start in PLAN:
        out = encode(name, src, start)
        raw = levels(out)
        gain = [t / r for t, r in zip(target, raw)]
        # a hero clip that already sits close should not be pushed around
        gain = [min(max(g, 0.70), 1.45) for g in gain]
        if VERBOSE:
            print("  %-12s raw R%6.1f G%6.1f B%6.1f  gain %.3f %.3f %.3f"
                  % tuple([name] + raw + gain))
        encode(name, src, start, gain)

        run([FFMPEG, "-v", "error", "-y", "-ss", "1", "-i", out,
             "-frames:v", "1", "-q:v", "4",
             os.path.join(OUT, name + "-poster.jpg")])
        final = levels(out)
        print("%-16s %5.2f MB   R%6.1f G%6.1f B%6.1f   (target R%6.1f G%6.1f B%6.1f)"
              % (name + ".mp4", os.path.getsize(out) / 1048576.0,
                 final[0], final[1], final[2], target[0], target[1], target[2]))


if __name__ == "__main__":
    main()
