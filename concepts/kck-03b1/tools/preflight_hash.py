#!/usr/bin/env python3
"""KCK-03B1 pre-flight rev. 5 content-identity helper (docs/kck-03b1-brief.md).
Instruction identity removes empty lines; image gate accepts exactly two pixel hashes.
It does not compute raw-file SHA-256: that is provenance, not a gate.

  python3 preflight_hash.py image <file.png>        -> width, height, pixel SHA-256, gate, route
  python3 preflight_hash.py text  <instruction.txt> -> canonical-content SHA-256
  (text also reads stdin when the path is "-", e.g. the instruction text the generation
   side actually received)

Image identity: decode -> RGBA8 -> row-major, top-to-bottom -> SHA-256 of the raw RGBA
bytes. No color management, no alpha premultiplication, ancillary chunks ignored.
Text identity: UTF-8, leading BOM removed, CRLF/CR -> LF, remove empty lines, then join
remaining lines with LF and append exactly one LF. Empty means zero characters; spaces
and tabs are preserved. Any other difference (including Markdown escapes or changed
characters) changes the hash.
Requires: pillow."""
import hashlib
import sys

IMAGE_SIZE = (1448, 1086)
IMAGE_PIXEL_ROUTES = {
    "5b9b014e0347ec89aab3fe896ae7a94d76202d92adb24aefce404533b71aeab8": "canonical",
    "b9ec2237b6658c2e4c94cf90c2206e416245881544d2700fc8ce1543655dd27d": "premultiply-roundtrip",
}


def image_identity(path):
    from PIL import Image
    with Image.open(path) as im:
        im.load()
        rgba = im.convert("RGBA")
        return rgba.size[0], rgba.size[1], hashlib.sha256(rgba.tobytes()).hexdigest()


def image_route(width, height, pixel_sha256):
    """Return the exact accepted route, or None. Never transform the held pixels."""
    if (width, height) != IMAGE_SIZE:
        return None
    return IMAGE_PIXEL_ROUTES.get(pixel_sha256)


def image_gate(path):
    width, height, pixel_sha256 = image_identity(path)
    route = image_route(width, height, pixel_sha256)
    return {"width": width, "height": height, "pixel_sha256": pixel_sha256,
            "gate": "PASS" if route else "FAIL", "route": route}


def canonical_text(raw):
    t = raw.decode("utf-8")
    if t.startswith("﻿"):
        t = t[1:]
    t = t.replace("\r\n", "\n").replace("\r", "\n")
    return ("\n".join(line for line in t.split("\n") if line != "") + "\n").encode("utf-8")


def text_identity(raw):
    c = canonical_text(raw)
    return len(c), hashlib.sha256(c).hexdigest()


if __name__ == "__main__":
    kind, path = sys.argv[1], sys.argv[2]
    if kind == "image":
        result = image_gate(path)
        print("width={width} height={height} pixel_sha256={pixel_sha256} gate={gate} route={route}".format(**result))
        sys.exit(0 if result["gate"] == "PASS" else 1)
    elif kind == "text":
        raw = sys.stdin.buffer.read() if path == "-" else open(path, "rb").read()
        n, d = text_identity(raw)
        print("canonical_bytes=%d canonical_sha256=%s" % (n, d))
    else:
        sys.exit(__doc__)
