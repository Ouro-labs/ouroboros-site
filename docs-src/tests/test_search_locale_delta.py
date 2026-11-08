"""Current locale bytes cannot rebind historical approval evidence."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('locale_pending',ROOT/'verify-pending-guides.py')
M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
class LocaleDelta(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)/'docs-src'
        shutil.copytree(ROOT,self.root,ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copytree(ROOT.parent/'site',self.root.parent/'site',ignore=shutil.ignore_patterns('docs'))
    def test_normal(self): M.verify(self.root)
    def test_changed_script(self):
        with (self.root/'content/assets/ouro-search-locale.js').open('a') as f:f.write('// tamper')
        with self.assertRaisesRegex(ValueError,'Search locale current bytes'):M.verify(self.root)
    def test_changed_template(self):
        with (self.root/'overrides/main.html').open('a') as f:f.write('tamper')
        with self.assertRaisesRegex(ValueError,'Search locale current bytes'):M.verify(self.root)
    def test_rebound_record_and_script(self):
        M.verify(self.root)
        p=self.root/'content/assets/ouro-search-locale.js';p.write_text(p.read_text()+'// tamper')
        r=self.root/'pending-search-locale.json';d=json.loads(r.read_text());d['files']['content/assets/ouro-search-locale.js']['current']=p.read_text();r.write_text(json.dumps(d))
        with self.assertRaisesRegex(ValueError,'Search locale evidence changed'):M.verify(self.root)
    def test_record_symlink(self):
        p=self.root/'pending-search-locale.json';p.rename(self.root/'other.json');p.symlink_to('other.json')
        with self.assertRaisesRegex(ValueError,'Search locale evidence unsafe'):M.verify(self.root)
    def test_missing_record(self):
        (self.root/'pending-search-locale.json').unlink()
        with self.assertRaises(ValueError):M.verify(self.root)
