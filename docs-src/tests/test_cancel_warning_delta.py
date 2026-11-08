"""Current cancel warning bytes cannot rebind historical approval evidence."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
spec=importlib.util.spec_from_file_location('cancel_pending',ROOT/'verify-pending-guides.py')
M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
class CancelWarningDelta(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)/'docs-src'
        shutil.copytree(ROOT,self.root,ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copytree(ROOT.parent/'site',self.root.parent/'site',ignore=shutil.ignore_patterns('docs'))
    def test_normal(self): M.verify(self.root)
    def test_changed_page(self):
        with (self.root/'content/cli-reference-detail.md').open('a') as f:f.write('// tamper')
        with self.assertRaisesRegex(ValueError,'Cancel warning current bytes'):M.verify(self.root)
    def test_changed_manifest(self):
        with (self.root/'content-manifest.json').open('a') as f:f.write('tamper')
        with self.assertRaisesRegex(ValueError,'Cancel warning current bytes'):M.verify(self.root)
    def test_rebound_record_and_page(self):
        M.verify(self.root)
        p=self.root/'content/cli-reference-detail.md';p.write_text(p.read_text()+'// tamper')
        r=self.root/'pending-cancel-warning.json';d=json.loads(r.read_text());d['files']['content/cli-reference-detail.md']['current']=p.read_text();r.write_text(json.dumps(d))
        with self.assertRaisesRegex(ValueError,'Cancel warning evidence changed'):M.verify(self.root)
    def test_page_manifest_record_rebinding(self):
        import hashlib
        M.verify(self.root)
        page=self.root/'content/cli-reference-detail.md';page.write_text(page.read_text()+'tamper')
        manifest=self.root/'content-manifest.json';data=json.loads(manifest.read_text())
        data['pages']['cli-reference-detail.md']['page_sha256']=hashlib.sha256(page.read_bytes()).hexdigest()
        manifest.write_text(json.dumps(data))
        record=self.root/'pending-cancel-warning.json';d=json.loads(record.read_text())
        for name in ['content/cli-reference-detail.md','content-manifest.json']:d['files'][name]['current']=(self.root/name).read_text()
        record.write_text(json.dumps(d))
        with self.assertRaisesRegex(ValueError,'Cancel warning evidence changed'):M.verify(self.root)
    def test_record_symlink(self):
        p=self.root/'pending-cancel-warning.json';p.rename(self.root/'other.json');p.symlink_to('other.json')
        with self.assertRaisesRegex(ValueError,'Cancel warning evidence unsafe'):M.verify(self.root)
    def test_missing_record(self):
        (self.root/'pending-cancel-warning.json').unlink()
        with self.assertRaises(ValueError):M.verify(self.root)
