"""Owner conditional lifecycle and real failure retention across new jobs."""
import copy
import hashlib
import json
import unittest
import validate_raster as tool

class Lifecycle(unittest.TestCase):
    def test_actual_promotion_and_robot_mouth_restoration(self):
        result=tool.validate()
        self.assertEqual([(x['asset_id'],x['status'],x['available']) for x in result['records']],
                         [('cat-02','production',True),('dinosaur-01','production',True),('robot-01','production',True)])

    def test_robot_cannot_be_enabled_by_manifest_alone(self):
        index=json.loads((tool.ROOT/'concepts/kck-03b/raster-candidate-set.json').read_text())
        index['records']=[index['retired_records'][0] if x['asset_id']=='robot-01' else x for x in index['records']]
        with self.assertRaisesRegex(ValueError,'availability/lifecycle'):tool.validate(index=index)

    def test_job_sources_calls_and_failure_retention(self):
        jobs=[]
        for name in ['robot-model-sheet-jobs','robot-mouth-jobs','snack-motion-jobs']:
            ledger=json.loads((tool.ROOT/f'concepts/kck-03b2/{name}.json').read_text());jobs+=ledger['jobs']
        self.assertEqual(sum(j['calls'] for j in jobs),7)
        gates={j['job_id']:j.get('agent_hard_gate') for j in jobs}
        self.assertEqual(gates['robot-side-01'],'FAIL');self.assertEqual(gates['robot-mouth-01'],'FAIL')
        self.assertEqual(gates['dinosaur-stumble-01'],'FAIL');self.assertEqual(gates['cat-receive-01'],'PASS')
        qualifier=json.loads((tool.ROOT/'concepts/kck-03c1/evidence/cat-receive-art-conformance.json').read_text())
        self.assertEqual(hashlib.sha256((tool.ROOT/qualifier['source']).read_bytes()).hexdigest(),qualifier['sha256'])
        self.assertEqual(len(qualifier['actual_glints']),4)
        for j in jobs:
            self.assertLessEqual(j['calls'],j['initial_call_limit'])
            for source,hashkey in [('reference','reference_sha256'),('instruction','instruction_sha256')]:
                self.assertEqual(hashlib.sha256((tool.ROOT/j[source]).read_bytes()).hexdigest(),j[hashkey])
            if j['calls']:
                self.assertEqual(hashlib.sha256((tool.ROOT/j['output']).read_bytes()).hexdigest(),j['output_sha256'])
                record=json.loads((tool.ROOT/j['provenance']).read_text());self.assertEqual(record['status'],'candidate')
            else:
                self.assertEqual(j['status'],'blocked_after_hard_failure');self.assertNotIn('output',j)
        manifest=json.loads((tool.ROOT/'manifests/characters.json').read_text())
        self.assertTrue(all(not x['representations']['animation_2d']['available'] for x in manifest['characters'].values()))

    def test_failed_mouth_crop_remains_diagnosable(self):
        from PIL import Image
        with Image.open(tool.ROOT/'concepts/kck-03b2/outputs/robot-mouth-01.png') as image:
            alpha=image.getchannel('A');self.assertEqual(sum(alpha.crop((0,1447,1086,1448)).histogram()[13:]),82)
        authority=json.loads((tool.ROOT/'concepts/kck-03b/evidence/2026-10-06-owner-robot-tongue-feedback.json').read_text())
        self.assertEqual(authority['quote'],'機器人舌頭有點怪')

    def test_bounded_retry_authority_and_failure_stops_unspent_robot_jobs(self):
        root=tool.ROOT
        ledger=json.loads((root/'concepts/kck-03c1/bounded-retry-jobs.json').read_text())
        authority=json.loads((root/ledger['authorization']).read_text())
        self.assertEqual(authority['exact_reply'],'好 幫我嘗試')
        p=authority['proposal'];self.assertEqual(hashlib.sha256((root/p['path']).read_bytes()).hexdigest(),p['sha256'])
        self.assertEqual(ledger['calls'],2);self.assertEqual(ledger['maximum_calls'],7)
        self.assertEqual(ledger['old_budget_unchanged'],{'dinosaur_v2d_used':2,'dinosaur_v2d_maximum':2,'remaining':0})
        self.assertEqual([j.get('agent_hard_gate') for j in ledger['jobs'][:2]],['PASS','FAIL'])
        for j in ledger['jobs']:
            self.assertLessEqual(j['calls'],j['max_calls'])
            for key in ['instruction','reference']:
                entry=j[key];self.assertEqual(hashlib.sha256((root/entry['path']).read_bytes()).hexdigest(),entry['sha256'])
            if j['calls']:
                self.assertEqual(j['status'],'candidate_recorded')
                self.assertEqual(hashlib.sha256((root/j['output']).read_bytes()).hexdigest(),j['output_sha256'])
                self.assertEqual(json.loads((root/j['provenance']).read_text())['status'],'candidate')
            else:
                self.assertEqual(j['status'],'blocked_after_hard_failure')
                self.assertEqual(j['blocked_by'],'robot-side-02');self.assertNotIn('output',j)
                self.assertFalse((root/j['concept_output']).exists())

if __name__=='__main__':unittest.main()
