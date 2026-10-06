#!/usr/bin/env python3
"""KCK-03B1 pre-flight rev. 3 content-identity helper (docs/kck-03b1-brief.md, "v2d pre-flight
gate, rev. 3"; items 2-3, the pixel and canonical-text hashes, are unchanged since rev. 2).
It does not compute raw-file SHA-256: that is provenance, not a gate.

  python3 preflight_hash.py image <file.png>        -> width, height, pixel SHA-256
  python3 preflight_hash.py text  <instruction.txt> -> canonical-content SHA-256
  (text also reads stdin when the path is "-", e.g. the instruction text the generation
   side actually received)

Image identity: decode -> RGBA8 -> row-major, top-to-bottom -> SHA-256 of the raw RGBA
bytes. No color management, no alpha premultiplication, ancillary chunks ignored.
Text identity: UTF-8, leading BOM removed, CRLF/CR -> LF, then exactly one trailing LF;
any other difference (including Markdown escapes or changed characters) changes the hash.
Requires: pillow."""
import hashlib
import sys


def image_identity(path):
    from PIL import Image
    im = Image.open(path)
    im.load()
    rgba = im.convert("RGBA")
    return rgba.size[0], rgba.size[1], hashlib.sha256(rgba.tobytes()).hexdigest()


def canonical_text(raw):
    t = raw.decode("utf-8")
    if t.startswith("﻿"):
        t = t[1:]
    t = t.replace("\r\n", "\n").replace("\r", "\n")
    return (t.rstrip("\n") + "\n").encode("utf-8")


def text_identity(raw):
    c = canonical_text(raw)
    return len(c), hashlib.sha256(c).hexdigest()


if __name__ == "__main__":
    kind, path = sys.argv[1], sys.argv[2]
    if kind == "image":
        w, h, d = image_identity(path)
        print("width=%d height=%d pixel_sha256=%s" % (w, h, d))
    elif kind == "text":
        raw = sys.stdin.buffer.read() if path == "-" else open(path, "rb").read()
        n, d = text_identity(raw)
        print("canonical_bytes=%d canonical_sha256=%s" % (n, d))
    else:
        sys.exit(__doc__)
