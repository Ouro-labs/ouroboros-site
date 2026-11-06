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
    def rejected(self, message):
        with self.assertRaisesRegex(ValueError, message): mod.verify(self.root)
    def test_baseline(self): mod.verify(self.root)
    def test_changed_locale_summary(self):
        (self.root/'pending-locale-review.md').write_text('altered');self.rejected('Locale summary changed')
    def test_changed_locale_file(self):
        (self.root/'overrides/main.html').write_text('altered');self.rejected('Locale file changed')
    def test_locale_file_symlink(self):
        p=self.root/'overrides/main.html';p.unlink();p.symlink_to(self.root/'overrides/partials/nav.html');self.rejected('Locale file changed')
    def test_changed_locale_prior_js(self):
        p=self.root/'pending-locale.json';e=json.loads(p.read_text());e['prior_js_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Locale prior JS does not match old evidence')
    def test_changed_install_summary(self):
        (self.root/'pending-install-review.md').write_text('altered');self.rejected('Installation summary changed')
    def test_changed_install_chain(self):
        p=self.root/'pending-install.json';e=json.loads(p.read_text());e['pages']['quickstart.md']['mid']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Installation snapshot chain mismatch: mid')
    def test_forged_install_source_hash(self):
        mpath=self.root/'content-manifest.json';epath=self.root/'pending-install.json'
        m=json.loads(mpath.read_text());e=json.loads(epath.read_text());name='quickstart.md'
        m['pages'][name]['source_sha256']='a'*64;e['pages'][name]['current']['source_sha256']='a'*64
        mpath.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');e['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();epath.write_text(json.dumps(e));lpath=self.root/'pending-locale.json';l=json.loads(lpath.read_text());l['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();lpath.write_text(json.dumps(l));self.rejected('Installation current metadata mismatch')
    def test_changed_latest_summary(self):
        (self.root/'pending-latest-review.md').write_text('altered');self.rejected('Latest summary changed')
    def test_forged_latest_source_hash(self):
        mpath=self.root/'content-manifest.json';epath=self.root/'pending-latest.json'
        m=json.loads(mpath.read_text());e=json.loads(epath.read_text());name='cli-reference-guide.md'
        m['pages'][name]['source_sha256']='a'*64;e['pages'][name]['current']['source_sha256']='a'*64
        mpath.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');e['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();epath.write_text(json.dumps(e))
        ipath=self.root/'pending-install.json';i=json.loads(ipath.read_text());i['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ipath.write_text(json.dumps(i));lpath=self.root/'pending-locale.json';l=json.loads(lpath.read_text());l['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();lpath.write_text(json.dumps(l));self.rejected('Installation snapshot chain mismatch: mid')
    def test_changed_latest_chain(self):
        p=self.root/'pending-latest.json';e=json.loads(p.read_text());e['pages']['cli-reference-guide.md']['mid']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Latest snapshot chain mismatch: mid')
    def test_changed_journey_summary(self):
        (self.root/'pending-journey-review.md').write_text('altered'); self.rejected('Journey summary changed')
    def test_changed_journey_chain(self):
        p=self.root/'pending-journey.json'; e=json.loads(p.read_text());e['pages']['quickstart.md']['mid']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Journey snapshot chain mismatch: mid')
    def test_changed_summary(self):
        (self.root/'pending-new-guides-review.md').write_text('altered'); self.rejected('Summary changed')
    def test_evidence_input_symlinks(self):
        for name in ('content-manifest.json','link-review-evidence.json','pending-new-guides.json','pending-new-guides-review.md','pending-journey.json','pending-journey-review.md','pending-latest.json','pending-latest-review.md','pending-install.json','pending-install-review.md','pending-locale.json','pending-locale-review.md'):
            with self.subTest(name=name):
                path=self.root/name; saved=self.root/(name+'.saved'); path.rename(saved); path.symlink_to(saved)
                try: self.rejected('Evidence input is not a regular non-symlink file')
                finally: path.unlink(); saved.rename(path)
    def test_changed_prior_evidence(self):
        (self.root/'review-evidence/groups-before.md').write_text('altered'); self.rejected('Prior public evidence changed')
    def test_forged_source_hash_in_both_records(self):
        mpath=self.root/'content-manifest.json'; epath=self.root/'pending-new-guides.json'
        manifest=json.loads(mpath.read_text()); evidence=json.loads(epath.read_text())
        name='dashboard-guide.md'; manifest['pages'][name]['source_sha256']='a'*64
        evidence['pages'][name]['source_sha256']='a'*64
        mpath.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
        epath.write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n')
        latest_path=self.root/'pending-latest.json';latest=json.loads(latest_path.read_text())
        latest['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();latest_path.write_text(json.dumps(latest,ensure_ascii=False,indent=2)+'\n')
        ipath=self.root/'pending-install.json';i=json.loads(ipath.read_text());i['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ipath.write_text(json.dumps(i))
        lpath=self.root/'pending-locale.json';l=json.loads(lpath.read_text());l['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();lpath.write_text(json.dumps(l))
        self.rejected('Installation snapshot chain mismatch: mid')
    def test_changed_manifest(self):
        with (self.root/'content-manifest.json').open('a') as f: f.write(' ')
        self.rejected('Locale manifest or pending status changed')
    def test_extra_file(self):
        (self.root/'content/unlisted.txt').write_text('unreviewed'); self.rejected('Content tree differs')
    def test_missing_file(self):
        (self.root/'content/dashboard-guide.md').unlink(); self.rejected('Content tree differs')
    def test_changed_page(self):
        (self.root/'content/dashboard-guide.md').write_text('changed'); self.rejected('Content hash does not match')
    def test_symlink_file(self):
        p=self.root/'content/dashboard-guide.md';p.unlink();p.symlink_to(self.root/'content/megacode-guide.md');self.rejected('Symlink in content tree')
    def test_symlink_root(self):
        p=self.root/'content'; other=self.root/'moved';p.rename(other);p.symlink_to(other,target_is_directory=True);self.rejected('Content root is a symlink')

if __name__ == '__main__': unittest.main()
