"""Real-image invariants for Owner-authorized A3 repair (Pillow + numpy)."""
import hashlib
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

import correct_a3_highlights as C
import measure_output as M

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'outputs/A3-v2d-attempt-01.png'
OUTPUT = ROOT / 'outputs/A3-v2d-attempt-01-highlight-corrected.png'
REFERENCE = ROOT / 'inputs/dinosaur-01_DinosaurResearcher.png'


class RealA3Repair(unittest.TestCase):
    def test_original_and_all_unrelated_pixels_preserved(self):
        self.assertEqual(hashlib.sha256(SOURCE.read_bytes()).hexdigest(), C.SOURCE_SHA)
        source = np.array(Image.open(SOURCE))
        output = np.array(Image.open(OUTPUT))
        self.assertEqual(output.shape, source.shape)
        np.testing.assert_array_equal(output[..., 3], source[..., 3])
        # Independently bounded regions include source/destination large blobs only.
        allowed = np.zeros(source.shape[:2], dtype=bool)
        allowed[514:570, 465:557] = True
        allowed[405:461, 816:901] = True
        np.testing.assert_array_equal(output[~allowed], source[~allowed])
        for x0,y0,x1,y1 in [(524,583,548,608),(871,476,896,500)]:
            np.testing.assert_array_equal(output[y0:y1,x0:x1],source[y0:y1,x0:x1])
        # Color swaps, not synthesized eye color: the eye histograms remain exact.
        for x0,y0,x1,y1 in [(445,497,582,647),(796,390,929,542)]:
            for channel in range(3):
                np.testing.assert_array_equal(np.bincount(output[y0:y1,x0:x1,channel].ravel(),minlength=256),
                                              np.bincount(source[y0:y1,x0:x1,channel].ravel(),minlength=256))

    def test_identity_and_highlights_satisfy_unchanged_contract(self):
        out, ref = M.measure(OUTPUT), M.measure(REFERENCE)
        self.assertEqual(M.compare(out,ref)['gate'],'PASS')
        self.assertEqual(len(out['eyes']),2)
        for eye in out['eyes']:
            self.assertEqual(eye['style_gate'],'PASS')
            x,y=eye['highlights'][0]['normalized_centroid']
            self.assertGreaterEqual(x,.30)
            self.assertLessEqual(x,.40)
            self.assertGreaterEqual(y,.20)
            self.assertLessEqual(y,.35)

    def test_repeat_run_matches_delivered_pixels(self):
        repaired, _ = C.repair(SOURCE.read_bytes())
        np.testing.assert_array_equal(repaired,np.array(Image.open(OUTPUT)))

    def test_wrong_source_is_rejected_before_decode(self):
        with self.assertRaisesRegex(ValueError,'Source hash mismatch'):
            C.repair(b'not the approved A3')


if __name__ == '__main__':
    unittest.main()
