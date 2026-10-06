"""Actual Robot regression fixtures; independent spatial/pixel invariants."""
import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

import correct_robot_highlights as C
from measure_output import label4

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'outputs/Robot-B1B-attempt-01.png'
OUTPUT = ROOT / 'outputs/Robot-B1B-attempt-01-highlight-corrected.png'
# Independently bounded pre-repair eye crops; these fixtures don't invoke the
# production component detector or copy its computed mask/centroid.
EYES = [(432, 261, 508, 339), (659, 275, 733, 352)]


class RobotRepair(unittest.TestCase):
    def test_original_alpha_rims_and_all_unrelated_pixels_preserved(self):
        self.assertEqual(hashlib.sha256(SOURCE.read_bytes()).hexdigest(), C.SOURCE_SHA)
        source = np.array(Image.open(SOURCE))
        output = np.array(Image.open(OUTPUT))
        np.testing.assert_array_equal(output[..., 3], source[..., 3])
        allowed = np.zeros(source.shape[:2], dtype=bool)
        allowed[270:294, 446:494] = True
        allowed[285:308, 673:719] = True
        np.testing.assert_array_equal(output[~allowed], source[~allowed])
        for x0, y0, x1, y1 in EYES:
            before, after = source[y0:y1, x0:x1], output[y0:y1, x0:x1]
            for channel in range(3):
                np.testing.assert_array_equal(np.bincount(before[..., channel].ravel(), minlength=256),
                                              np.bincount(after[..., channel].ravel(), minlength=256))
            np.testing.assert_array_equal(before[:3], after[:3])
            np.testing.assert_array_equal(before[-3:], after[-3:])
            np.testing.assert_array_equal(before[:, :3], after[:, :3])
            np.testing.assert_array_equal(before[:, -3:], after[:, -3:])

    def test_upper_left_direction_and_original_white_core_counts_preserved(self):
        source = np.array(Image.open(SOURCE))
        output = np.array(Image.open(OUTPUT))
        for (x0, y0, x1, y1), original_core_count in zip(EYES, (295, 284)):
            centroids = []
            for array in (source, output):
                eye = array[y0:y1, x0:x1]
                white = np.all(eye[..., :3] > 235, axis=2) & (eye[..., 3] > 200)
                # The rectangular fixture includes a few exterior paper pixels.
                # Measure the largest connected white core, not all white pixels.
                labels, _ = label4(white)
                counts = np.bincount(labels.ravel())
                counts[0] = 0
                yy, xx = np.where(labels == counts.argmax())
                self.assertEqual(len(xx), original_core_count)
                centroids.append((float(xx.mean()) / (x1-x0), float(yy.mean()) / (y1-y0)))
            before, after = centroids
            self.assertGreater(before[0], .5)
            self.assertLess(after[0], .5)  # Upper left means left/top halves, not Dino ranges.
            self.assertLess(after[1], .5)
            self.assertEqual(before[1], after[1])

    def test_repeat_run_matches_delivered_pixels_and_wrong_source_rejected(self):
        expected = np.array(Image.open(OUTPUT))
        repaired, _ = C.repair(SOURCE.read_bytes())
        np.testing.assert_array_equal(repaired, expected)
        with self.assertRaisesRegex(ValueError, 'Source hash mismatch'):
            C.repair(b'another asset')

    def test_overwrite_rejected_without_changing_source(self):
        before = SOURCE.read_bytes()
        with tempfile.TemporaryDirectory() as temporary:
            record = Path(temporary) / 'record.json'
            result = subprocess.run([sys.executable, str(Path(C.__file__)), str(SOURCE), str(SOURCE),
                                     '--record', str(record)], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(record.exists())
        self.assertEqual(SOURCE.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
