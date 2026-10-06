#!/usr/bin/env python3
"""Read-only PNG transport diagnostics; never used to pass the image gate.

Usage: python3 diagnose_png_transport.py canonical.png held.png > report.json
Requires Pillow and numpy. Coordinates are zero-based, bounding boxes inclusive.
"""
import argparse
import hashlib
import json
import struct
from collections import Counter
from pathlib import Path

import numpy as np
import PIL
from PIL import Image


def inspect(path):
    raw = path.read_bytes()
    if raw[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("Not a PNG: %s" % path)
    chunks = []
    pos = 8
    while pos < len(raw):
        length = struct.unpack_from(">I", raw, pos)[0]
        if pos + length + 12 > len(raw):
            raise ValueError("Truncated PNG chunk")
        chunks.append({"type": raw[pos + 4:pos + 8].decode("ascii"), "bytes": length})
        pos += length + 12
    with Image.open(path) as image:
        rgba = np.asarray(image.convert("RGBA")).copy()
    alpha = rgba[:, :, 3]
    y, x = np.nonzero(alpha > 10)
    mask = alpha > 200
    report = {
        "file": path.name,
        "raw_bytes": len(raw),
        "raw_sha256": hashlib.sha256(raw).hexdigest(),
        "pixel_sha256": hashlib.sha256(rgba.tobytes()).hexdigest(),
        "dimensions": [rgba.shape[1], rgba.shape[0]],
        "alpha_counts": {
            "zero": int((alpha == 0).sum()),
            "partial": int(((alpha > 0) & (alpha < 255)).sum()),
            "opaque": int((alpha == 255).sum()),
        },
        "alpha_top_four": [{"value": int(value), "count": int(count)}
                           for value, count in Counter(alpha.ravel()).most_common(4)],
        "alpha_gt_10_bbox_inclusive": [int(x.min()), int(y.min()), int(x.max()), int(y.max())]
        if x.size else None,
        "alpha_gt_200_count": int(mask.sum()),
        "alpha_gt_200_mean_rgb": rgba[:, :, :3][mask].mean(axis=0).tolist()
        if mask.any() else None,
        "png_chunks": chunks,
        "ihdr_bit_depth": raw[24],
        "ihdr_color_type": raw[25],
    }
    return report, rgba


def compare(source, held):
    if source.shape != held.shape:
        return {"same_dimensions": False}
    delta = held.astype(np.int16) - source.astype(np.int16)
    # Diagnostic model: nearest integer, ties upward, for each 8-bit channel.
    wide = source.astype(np.uint32)
    alpha = wide[:, :, 3:4]
    premultiplied = (wide[:, :, :3] * alpha + 127) // 255
    restored = (premultiplied * 255 + alpha // 2) // np.maximum(alpha, 1)
    modeled = np.concatenate([restored, alpha], axis=2).astype(np.uint8)
    positive = source[:, :, 3] > 0
    return {
        "same_dimensions": True,
        "alpha_identical": bool(np.array_equal(source[:, :, 3], held[:, :, 3])),
        "changed_pixels": int((delta != 0).any(axis=2).sum()),
        "changed_pixels_per_rgba_channel": (delta != 0).sum(axis=(0, 1)).tolist(),
        "max_absolute_rgba_difference": np.abs(delta).max(axis=(0, 1)).tolist(),
        "max_absolute_rgba_difference_alpha_gt_0": np.abs(delta)[positive].max(axis=0).tolist()
        if positive.any() else None,
        "mean_absolute_rgba_difference": np.abs(delta).mean(axis=(0, 1)).tolist(),
        "changed_pixels_alpha_zero": int(((delta != 0).any(axis=2) & ~positive).sum()),
        "roundtrip_formula": {
            "premultiply": "p = floor((c * a + 127) / 255)",
            "unpremultiply": "c2 = floor((p * 255 + floor(a / 2)) / a) if a > 0 else 0",
            "alpha": "unchanged",
        },
        "roundtrip_pixel_sha256": hashlib.sha256(modeled.tobytes()).hexdigest(),
        "roundtrip_matches_held_exactly": bool(np.array_equal(modeled, held)),
        "interpretation": "An exact match establishes a reproducible transform, not which platform component ran it. Gate checking separately requires exact dimensions and one explicitly accepted pixel hash; this diagnostic does not change held pixels.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("canonical", type=Path)
    parser.add_argument("held", type=Path)
    args = parser.parse_args()
    canonical, source = inspect(args.canonical)
    held, received = inspect(args.held)
    print(json.dumps({
        "measurement_actor": "Codex, local independent measurement, 2026-10-06 Asia/Taipei",
        "tool_versions": {"pillow": PIL.__version__, "numpy": np.__version__},
        "coordinate_convention": "zero-based; bounding boxes inclusive; RGBA8 row-major top-to-bottom; no color management",
        "canonical": canonical,
        "held_attachment_copy": held,
        "comparison": compare(source, received),
    }, indent=2))
