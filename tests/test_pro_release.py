from pathlib import Path
import copy
import importlib.util
import json
import unittest
ROOT=Path(__file__).resolve().parents[1]
def module(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/'scripts'/f'{name}.py')
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result);return result
PROMPT=module('prompt_audit');CONT=module('continuity_audit');TIMING=module('segment_timing_audit')
class ProReleaseChecks(unittest.TestCase):
    def setUp(self):
        self.prompt=(ROOT/'examples/full-prompt.txt').read_text()
        self.states=json.loads((ROOT/'examples/continuity.json').read_text())['segments']
    def test_full_example(self):
        self.assertEqual(PROMPT.audit(self.prompt,['你再说一遍。'],'full')['errors'],[])
    def test_visible_character_requires_shot_binding(self):
        text=self.prompt.replace('甲@[图片1]单人入画','甲单人入画')
        self.assertTrue(any('VISIBLE_CHARACTER_REFERENCE_MISSING' in x for x in PROMPT.audit(text,[],'full')['errors']))
    def test_visible_prop_requires_shot_binding(self):
        text=self.prompt.replace('手机@[图片3]由右手','手机由右手')
        self.assertTrue(any('CONTINUITY_PROP_REFERENCE_MISSING' in x for x in PROMPT.audit(text,[],'full')['errors']))
    def test_wrong_dialogue_rejected(self):
        self.assertTrue(PROMPT.audit(self.prompt,['你说错了。'],'full')['errors'])
    def test_prop_relation_drift_rejected(self):
        self.states[1]['entry']['props']['PHONE_A']['relation_mode']='worn'
        self.assertTrue(CONT.audit(self.states)['errors'])
    def test_active_prop_cannot_disappear(self):
        del self.states[1]['entry']['props']['PHONE_A']
        self.assertTrue(any('CONTINUITY_PROP_REFERENCE_DROPPED' in x for x in CONT.audit(self.states)['errors']))
    def test_voice_identity_drift_rejected(self):
        self.states[1]['entry']['voices']['A']['voice_identity']='OTHER'
        self.assertTrue(CONT.audit(self.states)['errors'])
    def test_extended_requires_mode(self):
        data=json.loads((ROOT/'examples/segments-extended.json').read_text())
        data['segments'][0]['segment_mode']='standard'
        self.assertTrue(TIMING.audit(data)['errors'])
if __name__=='__main__':unittest.main()
