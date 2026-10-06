#!/usr/bin/env python3
"""KCK-03B1 A2 measurement: gates 1-3 (one character, true alpha, eye identity).
Usage: python3 a2_measure.py <candidate.png|webp> <dinosaur-01 base.png>
Requires: pillow, numpy, scipy. Gate 4 is eye_highlight_gate.py (same folder).
Conventions (docs/kck-03b1-brief.md): visible bounds = alpha > 10; eye = filled connected
dark-brown region; eye width/height and center x are fractions of the visible-bounds WIDTH,
center y a fraction of the visible-bounds HEIGHT; highlights are inside the filled eye."""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage


def load(p):
    return np.array(Image.open(p).convert("RGBA"))


def eyes(a):
    al = a[..., 3]
    rgb = a[..., :3].astype(int)
    ys, xs = np.where(al > 10)
    x0, y0 = xs.min(), ys.min()
    W, H = xs.max() + 1 - x0, ys.max() + 1 - y0
    CH, CW = al.shape
    dark = (rgb[..., 0] < 110) & (rgb[..., 1] < 70) & (rgb[..., 2] < 60) & (al > 200)
    lab, _ = ndimage.label(dark)
    out = []
    for i, o in enumerate(ndimage.find_objects(lab), 1):
        h, w = o[0].stop - o[0].start, o[1].stop - o[1].start
        if 0.06 * CW < w < 0.16 * CW and 0.06 * CW < h < 0.16 * CW and (lab[o] == i).sum() > 0.004 * CW * CH:
            col = rgb[o][lab[o] == i].mean(0)
            out.append(dict(w=w / W, h=h / W, cx=(o[1].start + w / 2 - x0) / W,
                            cy=(o[0].start + h / 2 - y0) / H, rgb=col))
    out.sort(key=lambda e: e["cx"])
    return out, (int(W), int(H))


cand, base = load(sys.argv[1]), load(sys.argv[2])
al = cand[..., 3]
comp, n = ndimage.label(al > 10)
sizes = ndimage.sum(np.ones_like(al), comp, range(1, n + 1))
print("gate1 connected foreground components (alpha>10, >10 px): %d" % (sizes > 10).sum())
print("gate2 corner alpha TL,TR,BL,BR:", al[0, 0], al[0, -1], al[-1, 0], al[-1, -1],
      " alpha==0 fraction: %.4f" % (al == 0).mean())
ce, cb = eyes(cand), eyes(base)
(e, (cw, chh)), (b, (bw, bh)) = ce, cb
print("visible bounds: candidate %dx%d, base %dx%d" % (cw, chh, bw, bh))
assert len(e) == 2 and len(b) == 2
worst = {"size": 0, "center": 0, "rgb": 0}
for n_, x, y in zip("LR", e, b):
    d = {k: x[k] - y[k] for k in ("w", "h", "cx", "cy")}
    dc = np.abs(x["rgb"] - y["rgb"]).max()
    print("%s  w %.3f/%.3f (%+.3f)  h %.3f/%.3f (%+.3f)  cx %.3f/%.3f (%+.3f)  cy %.3f/%.3f (%+.3f)  rgb %s/%s (max %.1f)" % (
        n_, x["w"], y["w"], d["w"], x["h"], y["h"], d["h"], x["cx"], y["cx"], d["cx"], x["cy"], y["cy"], d["cy"],
        x["rgb"].round(1), y["rgb"].round(1), dc))
    worst["size"] = max(worst["size"], abs(d["w"]), abs(d["h"]))
    worst["center"] = max(worst["center"], abs(d["cx"]), abs(d["cy"]))
    worst["rgb"] = max(worst["rgb"], dc)
sp = (e[1]["cx"] - e[0]["cx"]) - (b[1]["cx"] - b[0]["cx"])
print("spacing x %.3f/%.3f (%+.3f)" % (e[1]["cx"] - e[0]["cx"], b[1]["cx"] - b[0]["cx"], sp))
ok = worst["size"] <= 0.015 and worst["center"] <= 0.02 and abs(sp) <= 0.02 and worst["rgb"] <= 15
print("gate3 max deviation size %.3f center %.3f spacing %.3f rgb %.1f -> %s" % (
    worst["size"], worst["center"], abs(sp), worst["rgb"], "PASS" if ok else "FAIL"))
