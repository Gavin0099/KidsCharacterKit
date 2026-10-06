"""Backward compatibility, real file identity and negative concept fixtures."""
import copy
import hashlib
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]


class ConceptProvenance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        schema = json.loads((ROOT / 'provenance/schema/provenance.schema.json').read_text())
        Draft202012Validator.check_schema(schema)
        cls.validator = Draft202012Validator(schema)
        cls.fixture = json.loads((ROOT / 'concepts/kck-03b1/outputs/A3-v2d-attempt-01-highlight-corrected.provenance.json').read_text())

    def test_existing_and_concept_records_remain_valid(self):
        for path in sorted((ROOT / 'provenance').glob('*/*.json')):
            if path.name != 'provenance.schema.json':
                self.validator.validate(json.loads(path.read_text()))
        concepts = sorted((ROOT / 'concepts').glob('**/*.provenance.json'))
        self.assertEqual({json.loads(path.read_text())['id'] for path in concepts},
                         {'dinosaur-concept-02', 'dinosaur-concept-03', 'dinosaur-concept-04',
                          'cat-concept-01', 'robot-concept-01', 'robot-concept-02'})
        for path in concepts:
            record = json.loads(path.read_text())
            self.validator.validate(record)
            expected_status = 'approved_reference' if record['id'] == 'dinosaur-concept-03' else 'candidate'
            self.assertEqual(record['status'], expected_status)
            output = ROOT / record['file']['path']
            self.assertEqual(hashlib.sha256(output.read_bytes()).hexdigest(), record['file']['sha256'])
            self.assertEqual(output.stat().st_size, record['file']['bytes'])
            with Image.open(output) as image:
                self.assertEqual(image.size, (record['file']['width'], record['file']['height']))
                self.assertEqual(image.mode, record['file']['color_type'])
            for source in record['inputs']['requested']:
                self.assertEqual(hashlib.sha256((ROOT / source['name']).read_bytes()).hexdigest(), source['sha256'])
            for evidence in record['evidence']:
                self.assertTrue((ROOT / evidence['path']).is_file())

    def test_missing_rights_or_invalid_hash_rejected(self):
        for mutation in ('rights', 'sha256'):
            bad = copy.deepcopy(self.fixture)
            if mutation == 'rights':
                del bad['rights']
            else:
                bad['file']['sha256'] = 'not-a-file-hash'
            with self.assertRaises(ValidationError):
                self.validator.validate(bad)

    def test_status_evidence_must_be_explicit(self):
        for status in ('approved_reference', 'rejected', 'deferred', 'superseded'):
            bad = copy.deepcopy(self.fixture)
            bad['status'] = status
            del bad['status_evidence']
            with self.assertRaises(ValidationError):
                self.validator.validate(bad)

    def test_unknown_status_or_wrong_concept_id_rejected(self):
        for status in ('selected', 'typo'):
            bad = copy.deepcopy(self.fixture)
            bad['status'] = status
            with self.assertRaises(ValidationError):
                self.validator.validate(bad)
        bad = copy.deepcopy(self.fixture)
        bad['id'] = 'dinosaur-01'
        with self.assertRaises(ValidationError):
            self.validator.validate(bad)


if __name__ == '__main__':
    unittest.main()
