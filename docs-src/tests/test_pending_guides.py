import importlib.util
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
spec = importlib.util.spec_from_file_location('pending_guides', ROOT/'verify-pending-guides.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class PendingGuidesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)/'docs-src'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('__pycache__'))
    def rejected(self):
        with self.assertRaises((ValueError, KeyError, OSError)): mod.verify(self.root)
    def test_baseline(self): mod.verify(self.root)
    def test_changed_journey_summary(self):
        (self.root/'pending-journey-review.md').write_text('altered'); self.rejected()
    def test_changed_journey_chain(self):
        p=self.root/'pending-journey.json'; e=json.loads(p.read_text());e['pages']['quickstart.md']['mid']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected()
    def test_changed_summary(self):
        (self.root/'pending-new-guides-review.md').write_text('altered'); self.rejected()
    def test_evidence_input_symlinks(self):
        for name in ('content-manifest.json','link-review-evidence.json','pending-new-guides.json','pending-new-guides-review.md','pending-journey.json','pending-journey-review.md'):
            with self.subTest(name=name):
                path=self.root/name; saved=self.root/(name+'.saved'); path.rename(saved); path.symlink_to(saved)
                try: self.rejected()
                finally: path.unlink(); saved.rename(path)
    def test_changed_prior_evidence(self):
        (self.root/'review-evidence/groups-before.md').write_text('altered'); self.rejected()
    def test_forged_source_hash_in_both_records(self):
        mpath=self.root/'content-manifest.json'; epath=self.root/'pending-new-guides.json'
        manifest=json.loads(mpath.read_text()); evidence=json.loads(epath.read_text())
        name='dashboard-guide.md'; manifest['pages'][name]['source_sha256']='a'*64
        evidence['pages'][name]['source_sha256']='a'*64
        mpath.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
        evidence['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest()
        epath.write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n')
        self.rejected()
    def test_changed_manifest(self):
        with (self.root/'content-manifest.json').open('a') as f: f.write(' ')
        self.rejected()
    def test_extra_file(self):
        (self.root/'content/unlisted.txt').write_text('unreviewed'); self.rejected()
    def test_missing_file(self):
        (self.root/'content/dashboard-guide.md').unlink(); self.rejected()
    def test_changed_page(self):
        (self.root/'content/dashboard-guide.md').write_text('changed'); self.rejected()
    def test_symlink_file(self):
        p=self.root/'content/dashboard-guide.md';p.unlink();p.symlink_to(self.root/'content/megacode-guide.md');self.rejected()
    def test_symlink_root(self):
        p=self.root/'content'; other=self.root/'moved';p.rename(other);p.symlink_to(other,target_is_directory=True);self.rejected()

if __name__ == '__main__': unittest.main()
