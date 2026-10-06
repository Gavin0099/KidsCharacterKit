"""Real-source bounded-mouth preservation and failed-donor regressions."""
import hashlib
import json
import unittest
import numpy as np
from PIL import Image
from pathlib import Path
import correct_robot_mouth as tool
ROOT=Path(__file__).resolve().parents[3]

class MouthRepair(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.src_path=ROOT/'concepts/kck-03b1/outputs/Robot-B1B-attempt-01-highlight-corrected.png'
        cls.donor_path=ROOT/'concepts/kck-03b2/outputs/robot-mouth-01.png'
        cls.src=np.array(Image.open(cls.src_path));cls.out=np.array(Image.open(ROOT/'concepts/kck-03b2/outputs/robot-mouth-01-local-corrected.png'))

    def test_every_alpha_and_every_outside_pixel_preserved(self):
        self.assertTrue(np.array_equal(self.src[:,:,3],self.out[:,:,3]))
        mask=np.ones(self.src.shape[:2],bool);mask[392:520,512:650]=False
        self.assertTrue(np.array_equal(self.src[mask],self.out[mask]))
        changed=np.any(self.src!=self.out,axis=2);self.assertGreater(int(changed.sum()),100)
        self.assertLessEqual(int(changed.sum()),138*128)

    def test_reviewed_tongue_and_hanging_frame_repaired(self):
        # Independent landmarks inspected in the native mouth preview: former
        # lower-right frame is head gray; long tongue-center bar becomes pink.
        gray=self.out[490,630,:3];self.assertTrue(np.all(gray>150))
        pink=self.out[477,572,:3];self.assertGreater(int(pink[0]),180);self.assertGreater(int(pink[1]),80)
        self.assertLess(int(self.src[490,630,1]),100)

    def test_cropped_donor_body_never_copied_and_replay_exact(self):
        donor=np.array(Image.open(self.donor_path));self.assertEqual(int((donor[-1,:,3]>=13).sum()),82)
        self.assertEqual(int((self.out[-1,:,3]>=13).sum()),0)
        self.assertTrue(np.array_equal(self.src[520:],self.out[520:]))
        image,record=tool.repair(self.src_path.read_bytes(),self.donor_path.read_bytes())
        self.assertTrue(np.array_equal(np.array(image),self.out))
        self.assertTrue(record['body_and_boots_equal'])

    def test_wrong_source_and_donor_rejected_and_originals_immutable(self):
        for source,donor in [(b'wrong',self.donor_path.read_bytes()),(self.src_path.read_bytes(),b'wrong')]:
            with self.assertRaisesRegex(ValueError,'hash mismatch'):tool.repair(source,donor)
        self.assertEqual(hashlib.sha256(self.src_path.read_bytes()).hexdigest(),tool.SOURCE_SHA)
        self.assertEqual(hashlib.sha256(self.donor_path.read_bytes()).hexdigest(),tool.DONOR_SHA)
        record=json.loads((ROOT/'concepts/kck-03b2/evidence/robot-mouth-local-correction.json').read_text())
        self.assertEqual(hashlib.sha256((ROOT/record['tool']['path']).read_bytes()).hexdigest(),record['tool']['sha256'])
        self.assertEqual(record['image_generation_calls'],0)

if __name__=='__main__':unittest.main()
