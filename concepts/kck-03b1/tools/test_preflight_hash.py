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
RAW_EXPECTED = {
    "A2": ("12c67216741b4bf308d61cdf4390bb773080e9eb5fb5398e9627e49df9a47e1e", 2342),
    "A3": ("c93b136768f35baf12e9c55da09571cd6a86ab307221abbe875ff511555c9884", 2371),
    "A4": ("d667795522e258351cb0686230fba66d829698057404c86738ba32d5fba4bf34", 2396),
}
EXPECTED = {
    "A2": ("b1b54564a7b6b5e4a8ee0420a9d52c7053eb2edf7d108561493a913a51a668d1", 2335),
    "A3": ("53e34cde5ec972a98347dd8e808f49a4ac3fb831621ddd3f1acf33c85eeaff09", 2364),
    "A4": ("99679d30a86d32be6555e1071babecf50aa25233feff69ab3db9c0b923c522ee", 2389),
}


def load(v):
    with open(os.path.join(INSTR, "%s_instruction_v2d.txt" % v), "rb") as f:
        return f.read()


class InstructionHashes(unittest.TestCase):
    def test_committed_files_match_brief(self):
        for v, (raw_sha, raw_size) in RAW_EXPECTED.items():
            raw = load(v)
            self.assertEqual(len(raw), raw_size, v)
            self.assertEqual(hashlib.sha256(raw).hexdigest(), raw_sha, v)
            sha, size = EXPECTED[v]
            self.assertEqual(P.text_identity(raw), (size, sha), v)

    def test_transport_differences_do_not_change_hash(self):
        raw = load("A3")
        want = EXPECTED["A3"][0]
        for name, variant in {
            "crlf": raw.replace(b"\n", b"\r\n"),
            "bom": b"\xef\xbb\xbf" + raw,
            "no trailing newline": raw.rstrip(b"\n"),
            "extra trailing newline": raw + b"\n",
            "cr": raw.replace(b"\n", b"\r"),
            "empty lines removed": b"\n".join(line for line in raw.split(b"\n") if line) + b"\n",
            "empty lines inserted": b"\n\n" + raw.replace(b"\n", b"\n\n\n"),
            "combined transport": b"\xef\xbb\xbf\r\n" + raw.replace(b"\n", b"\r\n\r\n"),
        }.items():
            self.assertEqual(P.text_identity(variant)[1], want, name)

    def test_content_changes_do_change_hash(self):
        raw = load("A3")
        want = EXPECTED["A3"][0]
        self.assertNotEqual(P.text_identity(raw.replace("–".encode(), b"-"))[1], want)
        self.assertNotEqual(P.text_identity(raw.replace(b"x=30", b"x\\=30"))[1], want)
        self.assertNotEqual(P.text_identity(raw.replace(b"x=30", b"x=31"))[1], want)
        self.assertNotEqual(P.text_identity(raw.replace(b"\n\n", b"\n \n", 1))[1], want)
        self.assertNotEqual(P.text_identity(raw.replace(b"\n\n", b"\n\t\n", 1))[1], want)
        self.assertNotEqual(P.text_identity(raw.replace(b"\nGoal:", b" Goal:", 1))[1], want)

    def test_canonicalization_is_idempotent(self):
        for v in EXPECTED:
            c = P.canonical_text(load(v))
            self.assertEqual(P.canonical_text(c), c, v)
            self.assertNotIn(b"\n\n", c, v)
            self.assertTrue(c.endswith(b"\n"), v)


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
