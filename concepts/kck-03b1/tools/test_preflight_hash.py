"""Regression cases for preflight_hash.py (a hard-gate helper). Run:
    python3 concepts/kck-03b1/tools/test_preflight_hash.py
Needs pillow only for the image case. Checks the committed instruction files against the
hashes in docs/kck-03b1-brief.md and that transport differences do not change the hash."""
import hashlib
import os
import unittest

import preflight_hash as P

HERE = os.path.dirname(os.path.abspath(__file__))
INSTR = os.path.join(HERE, "..", "instructions")
EXPECTED = {
    "A2": ("12c67216741b4bf308d61cdf4390bb773080e9eb5fb5398e9627e49df9a47e1e", 2342),
    "A3": ("c93b136768f35baf12e9c55da09571cd6a86ab307221abbe875ff511555c9884", 2371),
    "A4": ("d667795522e258351cb0686230fba66d829698057404c86738ba32d5fba4bf34", 2396),
}


def load(v):
    with open(os.path.join(INSTR, "%s_instruction_v2d.txt" % v), "rb") as f:
        return f.read()


class InstructionHashes(unittest.TestCase):
    def test_committed_files_match_brief(self):
        for v, (sha, size) in EXPECTED.items():
            raw = load(v)
            self.assertEqual(len(raw), size, v)
            self.assertEqual(hashlib.sha256(raw).hexdigest(), sha, v)
            self.assertEqual(P.text_identity(raw), (size, sha), v)

    def test_transport_differences_do_not_change_hash(self):
        raw = load("A3")
        want = EXPECTED["A3"][0]
        for name, variant in {
            "crlf": raw.replace(b"\n", b"\r\n"),
            "bom": b"\xef\xbb\xbf" + raw,
            "no trailing newline": raw.rstrip(b"\n"),
            "extra trailing newline": raw + b"\n",
        }.items():
            self.assertEqual(P.text_identity(variant)[1], want, name)

    def test_content_changes_do_change_hash(self):
        raw = load("A3")
        want = EXPECTED["A3"][0]
        self.assertNotEqual(P.text_identity(raw.replace("–".encode(), b"-"))[1], want)
        self.assertNotEqual(P.text_identity(raw.replace(b"x=30", b"x\\=30"))[1], want)
        self.assertNotEqual(P.text_identity(raw.replace(b"x=30", b"x=31"))[1], want)


class ImageIdentity(unittest.TestCase):
    def test_pixels_not_container(self):
        from PIL import Image
        import io
        im = Image.new("RGBA", (3, 2), (10, 20, 30, 255))
        b1, b2 = io.BytesIO(), io.BytesIO()
        im.save(b1, "PNG", compress_level=0)
        im.save(b2, "PNG", compress_level=9)
        self.assertNotEqual(b1.getvalue(), b2.getvalue())
        self.assertEqual(P.image_identity(io.BytesIO(b1.getvalue())), P.image_identity(io.BytesIO(b2.getvalue())))
        im2 = im.copy()
        im2.putpixel((0, 0), (11, 20, 30, 255))
        b3 = io.BytesIO()
        im2.save(b3, "PNG")
        self.assertNotEqual(P.image_identity(io.BytesIO(b3.getvalue())), P.image_identity(io.BytesIO(b1.getvalue())))


if __name__ == "__main__":
    unittest.main()
