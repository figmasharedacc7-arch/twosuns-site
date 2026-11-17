# -*- coding: utf-8 -*-
"""The three motion bands on the main site.

vid-work, vid-aerial and vid-port were never built by a script. They went into
the repo as low resolution downscales, 1600x900, 1152x648 and 1280x720, at
1.4, 0.57 and 0.64 Mbps, while every one of them is stretched across the full
width of the viewport under object-fit:cover. On a 1440px window at 2x that is
a two and a half times upscale for vid-aerial, which is why the bands read soft
against everything around them.

Each clip was traced back to its master by comparing frames, and the in point
and the speed were recovered the same way, so what this writes is the cut that
is already on the site, at the resolution its master can actually carry.

  vid-work    561Z_11_hand_upload.mov, 3840x2160 ProRes, a straight cut from
              0.0. Frames at 1.00s and 11.92s land at master 1.00 and 11.88.
  vid-aerial  aerial-view-of-a-large-cement-plant..., 3840x2160, from 1.0.
  vid-port    hong-kong-container-port..., 1920x1080 and only 7.12s long, so
              the 14.25s on the site cannot be a straight cut. Frames at 1.00s
              and at 13.25s both land at master 1.00s, which makes it the clip
              run forward and then backward, a boomerang rather than a loop.
              The reversed half drops its first frame, or the turn would hold
              the same picture for two frames and read as a stutter.

Resolution is never invented. vid-port stays at 1920x1080 because that is what
its master is; the other two go to 2560x1440 from 4K. Frame rate is the
master's own, which is also a fix: the files on the site were converted to 24
and 25 fps off 29.97 masters, and that conversion is visible as judder on a
slow aerial pan.

Run:  python3 build/bandvid.py
"""

import os
import subprocess

FFMPEG = os.path.expanduser("~/bin/ffmpeg")
SRC = os.path.expanduser("~/Downloads")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, ".."))

# CRF 28 with a ceiling, picked off a measured sweep rather than by eye. At
# CRF 23 vid-aerial came out at 15.6 Mbps and 26 MB for fourteen seconds: the
# footage is a drone over a whole cement plant, so every part of every frame is
# fine detail and there is nothing cheap in it to spend less on. 28 brings it
# to 6.8 Mbps, and the ceiling holds the peaks under 3.5, which is still five
# times the bitrate any of these files carried before.
CRF = "28"
MAXRATE, BUFSIZE = "3500k", "7000k"

# name, source, start, seconds, output size, fps, boomerang
PLAN = [
    ("vid-work",
     "561Z_11_hand_upload.mov",
     0.0, 12.92, (2560, 1440), 30, False),
    ("vid-aerial",
     "aerial-view-of-a-large-cement-plant-and-industrial-2026-06-03-21-58-33-utc.mp4",
     1.0, 14.00, (2560, 1440), 30, False),
    ("vid-port",
     "hong-kong-container-port-terminal-and-logistics-ce-2025-12-17-09-27-13-utc.mov",
     0.0, 7.12, (1920, 1080), 25, True),
]


def run(cmd):
    subprocess.run(cmd, check=True)


def encode(name, src, start, dur, size, fps, boomerang):
    w, h = size
    out = os.path.join(OUT, name + ".mp4")
    pre = ("scale=%d:%d:flags=lanczos,fps=%d,format=yuv420p,setsar=1"
           % (w, h, fps))
    cmd = [FFMPEG, "-v", "error", "-y",
           "-ss", "%.3f" % start, "-t", "%.3f" % dur,
           "-i", os.path.join(SRC, src)]
    if boomerang:
        cmd += ["-filter_complex",
                "[0:v]%s,split[a][b];"
                "[b]reverse,trim=start_frame=1,setpts=PTS-STARTPTS[r];"
                "[a][r]concat=n=2:v=1:a=0[v]" % pre,
                "-map", "[v]"]
    else:
        cmd += ["-vf", pre]
    cmd += ["-an", "-c:v", "libx264", "-preset", "slow", "-crf", CRF,
            "-maxrate", MAXRATE, "-bufsize", BUFSIZE,
            "-profile:v", "high", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", out]
    run(cmd)

    # the poster is the frame the band opens on, so the still a reader sees
    # before it plays and the still reduced motion keeps are the same picture
    run([FFMPEG, "-v", "error", "-y", "-i", out, "-frames:v", "1",
         "-q:v", "4", os.path.join(OUT, name + "-poster.jpg")])
    return out


def main():
    for name, src, start, dur, size, fps, boom in PLAN:
        out = encode(name, src, start, dur, size, fps, boom)
        print("%-16s %5.2f MB   %dx%d @ %dfps%s"
              % (name + ".mp4", os.path.getsize(out) / 1048576.0,
                 size[0], size[1], fps, "   boomerang" if boom else ""))


if __name__ == "__main__":
    main()
