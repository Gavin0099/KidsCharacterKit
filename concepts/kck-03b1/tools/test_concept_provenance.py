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
                          'cat-concept-01', 'cat-concept-02', 'cat-concept-03', 'cat-concept-04',
                          'cat-concept-05', 'cat-concept-06', 'cat-concept-07', 'cat-concept-08',
                          'dinosaur-concept-05', 'dinosaur-concept-06', 'dinosaur-concept-07',
                          'dinosaur-concept-08', 'dinosaur-concept-09', 'dinosaur-concept-10',
                          'dinosaur-concept-11', 'dinosaur-concept-12',
                          'robot-concept-01', 'robot-concept-02'})
        for path in concepts:
            record = json.loads(path.read_text())
            self.validator.validate(record)
            expected_status = 'approved_reference' if record['id'] in {'dinosaur-concept-03', 'cat-concept-01', 'robot-concept-02',
                                                                     'cat-concept-02', 'cat-concept-03', 'cat-concept-05',
                                                                     'cat-concept-06', 'cat-concept-07', 'cat-concept-08',
                                                                     'dinosaur-concept-05', 'dinosaur-concept-06', 'dinosaur-concept-08',
                                                                     'dinosaur-concept-09', 'dinosaur-concept-10', 'dinosaur-concept-12'} else 'candidate'
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

    def test_model_sheet_jobs_match_saved_outputs_and_stop_on_failure(self):
        ledger = json.loads((ROOT / 'concepts/kck-03b2/model-sheet-jobs.json').read_text())
        self.assertEqual(ledger['dinosaur_v2d_budget'], {'used': 2, 'maximum': 2, 'remaining': 0})
        jobs = ledger['jobs']
        self.assertEqual({(x['character'], x['view']) for x in jobs},
                         {(c, v) for c in ('cat', 'dinosaur')
                          for v in ('front', 'three-quarter', 'side', 'back', 'happy', 'confused')})
        self.assertEqual(sum(x['calls'] for x in jobs), 14)
        repairs = [x for x in jobs if x.get('kind') == 'authorized_targeted_correction']
        self.assertEqual({x['character'] for x in repairs}, {'cat', 'dinosaur'})
        self.assertEqual(len(repairs), 2)
        for job in repairs:
            self.assertEqual(job['calls'], 1)
            self.assertTrue((ROOT / job['authorization']).is_file())
            self.assertEqual(hashlib.sha256((ROOT / job['edit_target']).read_bytes()).hexdigest(), job['edit_target_sha256'])
        recorded = set()
        for job in jobs:
            self.assertLessEqual(job['calls'], job['initial_call_limit'])
            self.assertEqual(hashlib.sha256((ROOT / job['reference']).read_bytes()).hexdigest(), job['reference_sha256'])
            self.assertEqual(hashlib.sha256((ROOT / job['instruction']).read_bytes()).hexdigest(), job['instruction_sha256'])
            if job['calls']:
                if job.get('requires_pass'):
                    predecessor = next(x for x in jobs + ledger.get('derivations', []) if x['job_id'] == job['requires_pass'])
                    self.assertEqual(predecessor['agent_hard_gate'], 'PASS')
                    self.assertTrue((ROOT / job['continuation_authorization']).is_file())
                self.assertEqual(job['status'], 'candidate_recorded')
                record = json.loads((ROOT / job['provenance']).read_text())
                self.assertEqual(record['id'], job['concept_id'])
                expected_status = 'approved_reference' if job['job_id'] not in {'cat-side-01', 'dinosaur-side-01', 'dinosaur-side-02'} else 'candidate'
                self.assertEqual(record['status'], expected_status)
                self.assertEqual(hashlib.sha256((ROOT / job['output']).read_bytes()).hexdigest(), job['output_sha256'])
                recorded.add(ROOT / job['provenance'])
            else:
                self.assertEqual(job['status'], 'blocked_after_hard_failure')
                self.assertNotIn('output', job)
        for derivative in ledger.get('derivations', []):
            self.assertEqual(derivative['calls'], 0)
            self.assertEqual(derivative['agent_hard_gate'], 'PASS')
            self.assertTrue((ROOT / derivative['authorization']).is_file())
            self.assertEqual(hashlib.sha256((ROOT / derivative['output']).read_bytes()).hexdigest(), derivative['output_sha256'])
            recorded.add(ROOT / derivative['provenance'])
        self.assertEqual(recorded, set((ROOT / 'concepts/kck-03b2').glob('**/*.provenance.json')))

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
