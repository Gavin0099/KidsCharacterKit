"""Contract invariants and actual candidate-file regressions, no scene claim."""
import copy
import json
import unittest
from jsonschema import ValidationError
import validate_animation as tool

class AnimationContract(unittest.TestCase):
    def setUp(self):
        self.pack=json.loads((tool.ROOT/'concepts/kck-03c1/dinosaur-snack-partial-pack.json').read_text())

    def test_actual_partial_pack_and_immutable_frame_replay(self):
        tool.validate_semantics(self.pack)
        result=tool.validate_files(self.pack)
        self.assertEqual(result['status'],'candidate')
        self.assertFalse(result['availability_promoted'])
        self.assertEqual(set(self.pack['actions']),{'idle','run','carry'})
        self.assertEqual(self.pack['actions']['run']['duration_ms'],200)
        self.assertEqual(self.pack['actions']['run']['frames'][0]['anchor'],[512,960])

    def test_cat_candidate_and_anatomical_receiving_hand(self):
        pack=json.loads((tool.ROOT/'concepts/kck-03c1/cat-snack-candidate-pack.json').read_text())
        tool.validate_semantics(pack);tool.validate_files(pack)
        self.assertEqual(pack['actions']['receive']['duration_ms'],350)
        self.assertEqual(pack['actions']['happy']['motion_kind'],'static_hold')
        pack['actions']['receive']['frames'][0]['sockets']['snack']['hand']='anatomical-right'
        with self.assertRaisesRegex(ValueError,'Cat receiving hand'):tool.validate_semantics(pack)

    def test_frame_timing_sum_and_fps(self):
        for change in ['sum','fps','zero']:
            bad=copy.deepcopy(self.pack);run=bad['actions']['run']
            if change=='sum':run['duration_ms']=201
            elif change=='fps':run['fps']=8
            else:run['frames'][0]['duration_ms']=0
            with self.assertRaises((ValueError,ValidationError)):tool.validate_semantics(bad)

    def test_authored_still_is_not_animation(self):
        bad=copy.deepcopy(self.pack);f=bad['actions']['run']['frames'];f[1]['file']=copy.deepcopy(f[0]['file'])
        with self.assertRaisesRegex(ValueError,'distinct poses'):tool.validate_semantics(bad)
        bad=copy.deepcopy(self.pack);bad['actions']['run']['motion_kind']='static_hold'
        with self.assertRaisesRegex(ValueError,'one frame'):tool.validate_semantics(bad)

    def test_missing_or_wrong_hand_socket(self):
        for mutation in ['absent','left']:
            bad=copy.deepcopy(self.pack);socket=bad['actions']['run']['frames'][0]['sockets']
            if mutation=='absent':socket.clear()
            else:socket['snack']['hand']='anatomical-left'
            with self.assertRaises(ValueError):tool.validate_semantics(bad)

    def test_invalid_event_boundaries_order_and_payload(self):
        for events in [[{'type':'action_complete','time_ms':201}],
                       [{'type':'action_complete','time_ms':100},{'type':'action_complete','time_ms':10}],
                       [{'type':'foot_contact','time_ms':0}],
                       [{'type':'prop_attach','time_ms':0}]]:
            bad=copy.deepcopy(self.pack);bad['actions']['run']['events']=events
            with self.assertRaises(ValueError):tool.validate_semantics(bad)

    def test_alias_missing_target_or_cycle(self):
        for target in ['missing','carry','idle']:
            bad=copy.deepcopy(self.pack);bad['actions']['carry']['target']=target
            with self.assertRaises(ValueError):tool.validate_semantics(bad)

    def test_production_and_rights_require_real_evidence(self):
        bad=copy.deepcopy(self.pack);bad['status']='production'
        with self.assertRaisesRegex(ValueError,'consumer-scene'):tool.validate_semantics(bad)
        bad=copy.deepcopy(self.pack);bad['rights']['commercial_use_status']='confirmed'
        with self.assertRaisesRegex(ValueError,'external evidence'):tool.validate_semantics(bad)
        bad=copy.deepcopy(self.pack);bad['status']='production';bad['consumer_scene_evidence']='docs/animation-contract-v1.md'
        # A non-empty evidence path cannot promote actual candidate frames.
        with self.assertRaisesRegex(ValueError,'candidate frame'):tool.validate_files(bad)

    def test_model_views_hash_and_paths(self):
        bad=copy.deepcopy(self.pack);bad['model_sheets'][1]=copy.deepcopy(bad['model_sheets'][0])
        with self.assertRaisesRegex(ValueError,'distinct'):tool.validate_semantics(bad)
        bad=copy.deepcopy(self.pack);bad['source_master']['sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'hash mismatch'):tool.validate_files(bad)
        with self.assertRaisesRegex(ValueError,'escapes'):tool.repo_file(tool.ROOT,'../outside.png')

    def test_frame_character_and_selected_report_are_bound(self):
        bad=copy.deepcopy(self.pack);bad['actions']['run']['frames'][0]['file']['provenance']='provenance/cat/cat-02-soft-handmade-v1-delivery.json'
        with self.assertRaisesRegex(ValueError,'provenance/file'):tool.validate_files(bad)
        record=json.loads((tool.ROOT/self.pack['actions']['run']['frames'][0]['file']['provenance']).read_text())
        record['recipe']['sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'binding mismatch'):tool.validate_motion_frame(record,tool.ROOT)

    def test_scene_fingerprint_changes_with_timing_or_frames(self):
        bad=copy.deepcopy(self.pack);bad['actions']['run']['frames'][0]['duration_ms']=101
        self.assertNotEqual(tool.fingerprint(self.pack),tool.fingerprint(bad))
        self.assertEqual(tool.fingerprint(self.pack),tool.fingerprint(dict(reversed(list(self.pack.items())))))

if __name__=='__main__':unittest.main()
