import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('prompt_audit', ROOT / 'scripts/prompt_audit.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class PromptContractTests(unittest.TestCase):
    def setUp(self):
        self.text = (ROOT / 'examples/full-prompt.txt').read_text()

    def errors(self, text, expected=None, **kwargs):
        return m.audit(text, expected, 'full', **kwargs)['errors']

    def test_published_example(self):
        self.assertEqual(self.errors(self.text, ['你再说一遍。']), [])

    def test_repeated_source_dialogue_is_valid(self):
        text = self.text.replace('{你再说一遍。}', '{你再说一遍。}{你再说一遍。}')
        self.assertEqual(self.errors(text, ['你再说一遍。', '你再说一遍。']), [])

    def test_unexpected_repetition_and_order_fail(self):
        self.assertTrue(self.errors(self.text.replace('{你再说一遍。}', '{你再说一遍。}{你再说一遍。}'), ['你再说一遍。']))
        self.assertTrue(self.errors(self.text.replace('{你再说一遍。}', '{再说你一遍。}'), ['你再说一遍。']))

    def test_contiguous_speech_fragments_across_shots(self):
        text = self.text.replace('{你再说一遍。}', '{你再说}')
        text = text.replace('只有右手与手机入画', '人物甲O.S.：{一遍。} 只有右手与手机入画')
        self.assertEqual(self.errors(text, ['你再说一遍。']), [])

    def test_expected_silence_rejects_dialogue(self):
        self.assertTrue(self.errors(self.text, []))

    def test_missing_or_extra_fragment_fails(self):
        self.assertTrue(self.errors(self.text.replace('{你再说一遍。}', '{你再说}'), ['你再说一遍。']))

    def test_dialogue_outside_timeline_fails(self):
        text = self.text.replace('[本段任务]', '[本段任务]\n{你再说一遍。}')
        self.assertTrue(self.errors(text, ['你再说一遍。']))

    def test_timing_gap_and_noninteger_duration_fail(self):
        self.assertTrue(self.errors(self.text.replace('3.0—6.0', '3.1—6.0')))
        self.assertTrue(self.errors(self.text.replace('｜12秒', '｜12.5秒')))
        self.assertTrue(self.errors(self.text.replace('0.0—3.0', '0.1—3.0')))
        self.assertTrue(self.errors(self.text.replace('9.0—12.0', '9.0—11.0')))

    def test_missing_timecode_fails(self):
        self.assertTrue(self.errors(self.text.replace('0.0—3.0秒', '开场')))

    def test_long_take_requires_explicit_override(self):
        text = self.text.replace('0.0—3.0', '0.0—6.0').replace('3.0—6.0', '6.0—7.0').replace('6.0—9.0', '7.0—9.0')
        self.assertTrue(self.errors(text))
        self.assertEqual(self.errors(text, max_shot_seconds=6), [])

    def test_mapping_reference_policy(self):
        text = self.text.replace('未提供参考素材；按剧本与文字设定执行。', '@[图片1] = 人物甲')
        self.assertEqual(self.errors(text), [])
        self.assertTrue(self.errors(text.replace('只有人物甲入画', '只有@[图片1]人物甲入画')))
        self.assertEqual(self.errors(text.replace('只有人物甲入画', '只有@[图片1]人物甲入画'), reference_policy='shot'), [])

if __name__ == '__main__':
    unittest.main()
