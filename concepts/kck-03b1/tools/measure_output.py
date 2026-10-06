#!/usr/bin/env python3
"""Read-only v2d output measurements; visual gates and Owner acceptance stay separate.

Usage: python measure_output.py candidate.png reference.png
Uses the eye/component method recorded in the A2 evidence, with JSON output.
Bounding boxes are [min x, min y, max x exclusive, max y exclusive].
Requires Pillow and numpy. Does not edit or re-encode either input.
"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import PIL
from PIL import Image


def label4(mask):
    """Four-neighbor connected components, using overlapping horizontal runs."""
    labels = np.zeros(mask.shape, dtype=np.int32)
    parents = [0]
    runs = []
    previous = []

    def root(i):
        while parents[i] != i:
            parents[i] = parents[parents[i]]
            i = parents[i]
        return i

    for y, row in enumerate(mask):
        changes = np.diff(np.r_[False, row, False].astype(np.int8))
        current = []
        for x0, x1 in zip(np.where(changes == 1)[0], np.where(changes == -1)[0]):
            i = len(parents)
            parents.append(i)
            for px0, px1, pi in previous:
                if px0 < x1 and px1 > x0:
                    a, b = root(i), root(pi)
                    parents[max(a, b)] = min(a, b)
            labels[y, x0:x1] = i
            current.append((int(x0), int(x1), i))
            runs.append((y, int(x0), int(x1), i))
        previous = current
    roots = [root(i) for i in range(len(parents))]
    compact = {r: j for j, r in enumerate(sorted(set(roots)))}
    mapping = np.array([compact[r] for r in roots], dtype=np.int32)
    boxes = [None] * (len(compact) - 1)
    for y, x0, x1, i in runs:
        j = mapping[i] - 1
        old = boxes[j]
        boxes[j] = [x0, y, x1, y+1] if old is None else [min(x0, old[0]), min(y, old[1]), max(x1, old[2]), max(y+1, old[3])]
    return mapping[labels], [(slice(y0, y1), slice(x0, x1)) for x0, y0, x1, y1 in boxes]


def fill_holes(mask):
    background, _ = label4(~mask)
    outside = np.unique(np.r_[background[0], background[-1], background[:, 0], background[:, -1]])
    return mask | ~np.isin(background, outside)


def measure(path):
    data = Path(path).read_bytes()
    with Image.open(path) as im:
        fmt, mode = im.format, im.mode
        a = np.array(im.convert("RGBA"))
    alpha = a[..., 3]
    rgb = a[..., :3].astype(int)
    height, width = alpha.shape
    ys, xs = np.where(alpha > 10)
    if not len(xs):
        raise ValueError("No visible foreground")
    x0, y0 = int(xs.min()), int(ys.min())
    vw, vh = int(xs.max()) + 1 - x0, int(ys.max()) + 1 - y0
    dark = (rgb[..., 0] < 110) & (rgb[..., 1] < 70) & (rgb[..., 2] < 60) & (alpha > 200)
    labels, boxes = label4(dark)
    eyes = []
    for i, box in enumerate(boxes, 1):
        h, w = box[0].stop - box[0].start, box[1].stop - box[1].start
        mask = labels[box] == i
        if not (0.06 * width < w < 0.16 * width and 0.06 * width < h < 0.16 * width
                and mask.sum() > 0.004 * width * height):
            continue
        ex, ey = box[1].start, box[0].start
        eye = fill_holes(mask)
        sub = a[box]
        white = np.all(sub[..., :3] > 235, axis=2) & (sub[..., 3] > 200) & eye
        blobs, blob_boxes = label4(white)
        highlights = []
        for j in range(1, len(blob_boxes) + 1):
            by, bx = np.where(blobs == j)
            if len(bx) >= 30:
                highlights.append({"pixels": len(bx), "normalized_centroid": [float(bx.mean()/w), float(by.mean()/h)],
                                   "bbox": [int(bx.min())+ex, int(by.min())+ey, int(bx.max())+ex+1, int(by.max())+ey+1]})
        highlights.sort(key=lambda b: b["pixels"], reverse=True)
        style = "INCONCLUSIVE"
        if len(highlights) >= 2:
            lx, ly = highlights[0]["normalized_centroid"]
            sx, sy = highlights[1]["normalized_centroid"]
            style = "PASS" if 0.30 <= lx <= 0.40 and 0.20 <= ly <= 0.35 and sx > lx and sy > ly else "FAIL"
        eyes.append({"bbox": [ex, ey, ex+w, ey+h], "width": w/vw, "height": h/vw,
                     "cx": (ex+w/2-x0)/vw, "cy": (ey+h/2-y0)/vh,
                     "dark_rgb_mean": rgb[box][mask].mean(axis=0).tolist(), "highlights": highlights, "style_gate": style})
    eyes.sort(key=lambda e: e["cx"])
    components, _ = label4(alpha > 10)
    sizes = np.bincount(components.ravel())[1:]
    return {"file": Path(path).name, "format": fmt, "mode": mode, "bytes": len(data),
            "raw_sha256": hashlib.sha256(data).hexdigest(),
            "rgba8_sha256": hashlib.sha256(a.tobytes()).hexdigest(), "dimensions": [width, height],
            "visible_bbox": [x0, y0, x0+vw, y0+vh], "corner_alpha_TL_TR_BL_BR": [int(alpha[0,0]), int(alpha[0,-1]), int(alpha[-1,0]), int(alpha[-1,-1])],
            "alpha_zero": int((alpha == 0).sum()), "alpha_partial": int(((alpha > 0) & (alpha < 255)).sum()),
            "alpha_opaque": int((alpha == 255).sum()), "foreground_components_over_10_pixels": int((sizes > 10).sum()),
            "square_canvas": width == height, "eyes": eyes}


def compare(candidate, reference):
    if len(candidate["eyes"]) != 2 or len(reference["eyes"]) != 2:
        return {"gate": "INCONCLUSIVE", "reason": "Expected exactly two detected eye regions in both files"}
    deltas = []
    worst = {"size": 0.0, "center": 0.0, "rgb": 0.0}
    for eye, base in zip(candidate["eyes"], reference["eyes"]):
        d = {k: eye[k] - base[k] for k in ("width", "height", "cx", "cy")}
        d["rgb"] = (np.array(eye["dark_rgb_mean"]) - base["dark_rgb_mean"]).tolist()
        worst["size"] = max(worst["size"], abs(d["width"]), abs(d["height"]))
        worst["center"] = max(worst["center"], abs(d["cx"]), abs(d["cy"]))
        worst["rgb"] = max(worst["rgb"], max(abs(v) for v in d["rgb"]))
        deltas.append(d)
    worst["spacing"] = abs((candidate["eyes"][1]["cx"] - candidate["eyes"][0]["cx"]) -
                           (reference["eyes"][1]["cx"] - reference["eyes"][0]["cx"]))
    limits = {"size": 0.015, "center": 0.02, "spacing": 0.02, "rgb": 15}
    return {"gate": "PASS" if all(worst[k] <= limits[k] for k in limits) else "FAIL",
            "maximum_absolute_deviations": worst, "tolerances": limits, "per_eye_deltas_left_to_right": deltas}


if __name__ == "__main__":
    c, r = measure(sys.argv[1]), measure(sys.argv[2])
    style = "INCONCLUSIVE" if len(c["eyes"]) != 2 else (
        "FAIL" if any(e["style_gate"] == "FAIL" for e in c["eyes"]) else
        "PASS" if all(e["style_gate"] == "PASS" for e in c["eyes"]) else "INCONCLUSIVE")
    print(json.dumps({"libraries": {"python": sys.version.split()[0], "Pillow": PIL.__version__, "numpy": np.__version__},
                      "method": {"bbox": "maximum coordinates exclusive", "connectivity": "4-neighbor, overlapping horizontal runs (equivalent to the prior scipy default)",
                                 "visible": "alpha>10", "dark_eye": "R<110,G<70,B<60,alpha>200; width and height each 6%-16% of canvas width; dark area>0.4% canvas area",
                                 "highlight": "filled dark eye; R,G,B>235,alpha>200; connected blobs >=30 pixels; two largest; centroid/bbox width or height",
                                 "identity": "eye width/height/center x normalized to visible width; center y to visible height; color from dark mask excluding highlights"},
                      "candidate": c, "reference": r, "eye_identity": compare(c, r), "eye_style": style,
                      "visual_gates": "one-character/no-text, matte absence, eye shape and overall identity require separate visual review; corners alone do not prove no matte",
                      "owner_texture_acceptance": "pending"}, indent=2))
