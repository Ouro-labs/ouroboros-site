import importlib.util,json,shutil,tempfile,unittest
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
spec=importlib.util.spec_from_file_location('uninstall_pending',ROOT/'verify-pending-guides.py');M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
class UninstallDeltaTest(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)/'docs-src'
  shutil.copytree(ROOT,self.root,ignore=shutil.ignore_patterns('__pycache__'))
  if (self.root/'pending-install-title.json').exists(): M.restore_install_title_fixture(self.root)
  (self.root.parent/'site').mkdir()
  for n in ('index.html','llms.txt'):shutil.copyfile(ROOT.parent/'site'/n,self.root.parent/'site'/n)
 def test_normal(self):M.verify(self.root)
 def test_page_change(self):
  with (self.root/'content/operations-detail.md').open('a')as f:f.write('forged')
  with self.assertRaisesRegex(ValueError,'Uninstall delta current bytes'):M.verify(self.root)
 def test_record_only_change(self):
  p=self.root/'pending-uninstall-warning.json';x=json.loads(p.read_text());x['pages']['operations-detail.md']['current_text']+='forged';p.write_text(json.dumps(x))
  with self.assertRaisesRegex(ValueError,'Uninstall delta evidence changed'):M.verify(self.root)
 def test_page_manifest_record_simultaneous_rebinding_rejected(self):
  import hashlib
  M.verify(self.root) # This exact fixture must pass before simultaneous tampering.
  page=self.root/'content/operations-detail.md'
  changed=page.read_text()+'\nforged simultaneous change\n';page.write_text(changed)
  manifest_path=self.root/'content-manifest.json';manifest=json.loads(manifest_path.read_text())
  manifest['pages']['operations-detail.md']['page_sha256']=hashlib.sha256(page.read_bytes()).hexdigest()
  manifest['pages']['operations-detail.md']['source_sha256']='a'*64
  manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
  record_path=self.root/'pending-uninstall-warning.json';record=json.loads(record_path.read_text())
  record['pages']['operations-detail.md']['current_text']=changed
  record['pages']['operations-detail.md']['current']=manifest['pages']['operations-detail.md']
  record['manifest_sha256']=hashlib.sha256(manifest_path.read_bytes()).hexdigest()
  record_path.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
  self.assertEqual(record['pages']['operations-detail.md']['current']['page_sha256'],hashlib.sha256(page.read_bytes()).hexdigest())
  self.assertEqual(record['manifest_sha256'],hashlib.sha256(manifest_path.read_bytes()).hexdigest())
  with self.assertRaisesRegex(ValueError,'Uninstall delta evidence changed'):M.verify(self.root)
 def test_record_symlink(self):
  p=self.root/'pending-uninstall-warning.json';p.rename(self.root/'saved.json');p.symlink_to(self.root/'saved.json')
  with self.assertRaisesRegex(ValueError,'Uninstall delta unsafe'):M.verify(self.root)
 def test_missing_record(self):
  (self.root/'pending-uninstall-warning.json').unlink()
  with self.assertRaises(ValueError):M.verify(self.root)
 def test_gate_open(self):
  p=self.root/'content-manifest.json';x=json.loads(p.read_text());x['semantic_links_reviewed']=True;p.write_text(json.dumps(x))
  with self.assertRaisesRegex(ValueError,'requires closed gate'):M.verify(self.root)
 def test_old_evidence_tamper(self):
  (self.root/'pending-ai-manual-review.md').write_text('forged')
  with self.assertRaisesRegex(ValueError,'AI manual summary changed'):M.verify(self.root)
if __name__=='__main__':unittest.main()
