from pathlib import Path
import hashlib
import json
import unittest
ROOT=Path(__file__).resolve().parents[1]

class OriginalProPackageIntegrity(unittest.TestCase):
    def test_every_original_reference_script_and_asset_is_included(self):
        manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
        rows=manifest['files']
        self.assertEqual(len(rows),23)
        self.assertEqual(len([x for x in rows if x['path'].startswith('references/')]),16)
        self.assertEqual(len([x for x in rows if x['path'].startswith('scripts/')]),4)
        for item in rows:
            path=ROOT/item['path']
            self.assertTrue(path.is_file(),item['path'])
            if item['policy']=='byte_identical':
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),item['source_sha256'],item['path'])

    def test_skill_instructions_only_have_branding_changes(self):
        manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
        expected=next(x['source_sha256'] for x in manifest['files'] if x['path']=='SKILL.md')
        original=(ROOT/'SKILL.md').read_text().replace('name: chuangmeng-director-pro','name: direct-episode-to-seedance-prompts-pro-v1-6',1).replace('# 创梦 导演skills Pro V1.6','# Seedance电影导演 Pro V1.6',1)
        self.assertEqual(hashlib.sha256(original.encode()).hexdigest(),expected)

if __name__=='__main__':unittest.main()
