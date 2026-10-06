#!/usr/bin/env python3
"""KCK-03B1 eye-highlight gate (Round 2c method). Usage: python3 eye_highlight_gate.py <image.png|webp>
Requires: pillow, numpy, scipy.
Eye = filled connected dark-brown region (its bounding box is the 0-1 frame).
Highlights = near-white blobs inside the eye; center = centroid.
Gate per eye: large x in [0.30,0.40], y in [0.20,0.35]; small x > large.x and y > large.y."""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

a = np.array(Image.open(sys.argv[1]).convert("RGBA"))
rgb = a[..., :3].astype(int)
al = a[..., 3]
dark = (rgb[..., 0] < 110) & (rgb[..., 1] < 70) & (rgb[..., 2] < 60) & (al > 200)
lab, _ = ndimage.label(dark)
H, W = al.shape
eyes = []
for i, o in enumerate(ndimage.find_objects(lab), 1):
    h = o[0].stop - o[0].start
    w = o[1].stop - o[1].start
    # eye-sized blobs only (scaled to canvas): 6%-16% of canvas width, plausible aspect ratio
    if 0.06 * W < w < 0.16 * W and 0.06 * W < h < 0.16 * W and (lab[o] == i).sum() > 0.004 * W * H:
        eyes.append((i, o, w, h))
ok_all = len(eyes) == 2
print("eyes found:", len(eyes), "(expected 2)")
for i, o, w, h in sorted(eyes, key=lambda e: e[1][1].start):
    y0, x0 = o[0].start, o[1].start
    eye = ndimage.binary_fill_holes(lab[o] == i)
    sub = a[o]
    white = (sub[..., 0] > 235) & (sub[..., 1] > 235) & (sub[..., 2] > 235) & (sub[..., 3] > 200) & eye
    l2, n2 = ndimage.label(white)
    blobs = []
    for j in range(1, n2 + 1):
        ys, xs = np.where(l2 == j)
        if len(ys) >= 30:
            blobs.append((len(ys), xs.mean() / w, ys.mean() / h))
    blobs.sort(reverse=True)
    if len(blobs) < 2:
        print("eye at x=%d: fewer than 2 highlights found -> FAIL" % x0); ok_all = False; continue
    (_, lx, ly), (_, sx, sy) = blobs[0], blobs[1]
    g = 0.30 <= lx <= 0.40 and 0.20 <= ly <= 0.35 and sx > lx and sy > ly
    ok_all &= g
    print("eye at x=%d  large=(%.3f, %.3f)  small=(%.3f, %.3f)  -> %s" % (x0, lx, ly, sx, sy, "PASS" if g else "FAIL"))
print("GATE:", "PASS" if ok_all else "FAIL")
