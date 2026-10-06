"""Real-image regression for the authorized extra-line repair; independent ROIs."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

import correct_dinosaur_side_belly as C

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'outputs/dinosaur-side-02.png'
OUTPUT = ROOT / 'outputs/dinosaur-side-02-belly-corrected.png'


class BellyRepair(unittest.TestCase):
    def test_all_alpha_and_pixels_outside_authorized_interior_preserved(self):
        before, after = np.array(Image.open(SOURCE)), np.array(Image.open(OUTPUT))
        np.testing.assert_array_equal(after[..., 3], before[..., 3])
        allowed = np.zeros(before.shape[:2], dtype=bool)
        allowed[851:864, 466:493] = True  # independently inspected upper-stroke envelope
        np.testing.assert_array_equal(after[~allowed], before[~allowed])
        # Observed contour immediately left of the extra stroke is untouched.
        np.testing.assert_array_equal(after[850:865, 446:466], before[850:865, 446:466])
        self.assertGreater(np.any(after != before, axis=2).sum(), 100)

    def test_extra_ink_removed_and_remaining_two_strokes_exact(self):
        before, after = np.array(Image.open(SOURCE)), np.array(Image.open(OUTPUT))
        def ink(array):
            p = array[853:861, 474:488, :3]
            return int(((p[..., 0] < 180) & (p[..., 1] < 140) & (p[..., 2] < 120)).sum())
        self.assertGreater(ink(before), 60)
        self.assertEqual(ink(after), 0)
        for region in ((slice(912, 947), slice(445, 500)),
                       (slice(977, 1011), slice(450, 508))):
            np.testing.assert_array_equal(after[region], before[region])

    def test_reproducible_pixels_and_wrong_source_rejected(self):
        pixels, _ = C.repair(SOURCE.read_bytes())
        np.testing.assert_array_equal(pixels, np.array(Image.open(OUTPUT)))
        with self.assertRaisesRegex(ValueError, 'Source hash mismatch'):
            C.repair(b'another file')

    def test_source_overwrite_rejected(self):
        raw = SOURCE.read_bytes()
        with tempfile.TemporaryDirectory() as directory:
            record = Path(directory) / 'record.json'
            result = subprocess.run([sys.executable, C.__file__, str(SOURCE), str(SOURCE),
                                     '--record', str(record)], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(record.exists())
        self.assertEqual(raw, SOURCE.read_bytes())


if __name__ == '__main__':
    unittest.main()
