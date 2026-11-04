import copy
import importlib.util
import json
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('state_ledger', ROOT / 'scripts/state_ledger_audit.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'examples/state-ledger.json').read_text())
    def errors(self):
        return m.audit(self.data)['errors']
    def test_valid_example(self):
        self.assertEqual(self.errors(), [])
    def test_boundary_seat_drift(self):
        self.data['segments'][1]['entry']['characters']['A']['posture'] = '跪'
        self.assertTrue(self.errors())
    def test_entry_changes_cannot_be_exempted(self):
        self.data['segments'][1]['entry']['characters']['A']['right_hand'] = '空手'
        self.data['segments'][1]['first_action_changes'] = ['characters.A.right_hand']
        self.assertTrue(self.errors())
    def test_missing_character_cannot_pass(self):
        del self.data['segments'][1]['entry']['characters']['B']
        self.assertTrue(self.errors())
    def test_unrecorded_exit_change(self):
        self.data['segments'][0]['exit']['characters']['A']['emotion'] = '失控'
        self.assertTrue(self.errors())
    def test_bad_before_and_unknown_path(self):
        self.data['segments'][0]['shots'][0]['changes'][0]['before'] = '错误'
        self.assertTrue(self.errors())
        self.setUp()
        self.data['segments'][0]['shots'][0]['changes'][0]['path'] = 'characters.MISSING.emotion'
        self.assertTrue(self.errors())
    def test_wrong_hand_holder(self):
        self.data['segments'][0]['entry']['props']['PEN']['holder'] = '不存在'
        self.assertTrue(self.errors())
    def test_time_gap_closure_and_long_shot(self):
        for key, value in [('start', 0.1), ('end', 4.1)]:
            self.setUp()
            self.data['segments'][0]['shots'][0][key] = value
            self.assertTrue(self.errors())
        self.setUp()
        self.data['segments'][0]['duration'] = 7
        self.assertTrue(self.errors())
    def test_invalid_duration_and_missing_state(self):
        for value in [True, -1, 1.5, 16]:
            self.setUp()
            self.data['segments'][0]['duration'] = value
            self.assertTrue(self.errors())
        self.setUp()
        self.data['segments'][0]['entry'] = {}
        self.assertTrue(self.errors())
    def test_malformed_input_does_not_crash(self):
        for data in [None, [], {}, {'schema_version':1,'model_max_seconds':15,'segments':[None]}]:
            self.assertTrue(m.audit(data)['errors'])
    def test_malformed_assets_do_not_crash(self):
        for value in [[], None, False, 'UNKNOWN']:
            self.setUp()
            self.data['segments'][0]['entry']['props']['PEN']['holder'] = value
            self.assertTrue(self.errors())
    def test_knowledge_requires_fact_ids(self):
        self.data['segments'][0]['entry']['characters']['A']['knowledge'] = ['秘密', '秘密']
        self.assertTrue(self.errors())

if __name__ == '__main__':
    unittest.main()
