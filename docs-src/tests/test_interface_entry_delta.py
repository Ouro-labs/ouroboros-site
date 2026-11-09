import importlib.util,json,shutil,tempfile,unittest,sys,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
spec=importlib.util.spec_from_file_location('entry_pending',ROOT/'verify-pending-guides.py');M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
class InterfaceEntryDelta(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)/'docs-src'
  shutil.copytree(ROOT,self.root,ignore=shutil.ignore_patterns('__pycache__'));shutil.copytree(ROOT.parent/'site',self.root.parent/'site',ignore=shutil.ignore_patterns('docs'))
  if (self.root/'pending-recovery-translation.json').exists(): M.restore_recovery_translation_fixture(self.root)
 def test_normal(self):M.verify(self.root)
 def test_each_page_and_manifest(self):
  for name in ['content/cli-reference-detail.md','content/mcp-reference-detail.md','content/config-reference-guide.md','content-manifest.json']:
   with self.subTest(name=name):
    p=self.root/name;b=p.read_bytes();p.write_bytes(b+b'tamper')
    try:
     with self.assertRaisesRegex(ValueError,'Interface entry current bytes'):M.verify(self.root)
    finally:p.write_bytes(b)
 def test_simultaneous_rebinding(self):
  M.verify(self.root)
  page=self.root/'content/cli-reference-detail.md';page.write_text(page.read_text()+'tamper')
  manifest=self.root/'content-manifest.json';d=json.loads(manifest.read_text());d['pages']['cli-reference-detail.md']['page_sha256']=hashlib.sha256(page.read_bytes()).hexdigest();manifest.write_text(json.dumps(d))
  rec=self.root/'pending-interface-entry.json';d=json.loads(rec.read_text())
  for name in ['content/cli-reference-detail.md','content-manifest.json']:d['files'][name]['current']=(self.root/name).read_text()
  rec.write_text(json.dumps(d))
  with self.assertRaisesRegex(ValueError,'Interface entry evidence changed'):M.verify(self.root)
 def test_prior_evidence(self):
  M.verify(self.root);(self.root/'pending-search-locale.json').write_text('{}')
  with self.assertRaisesRegex(ValueError,'Search locale evidence changed'):M.verify(self.root)
 def test_gate(self):
  M.verify(self.root);p=self.root/'content-manifest.json';d=json.loads(p.read_text());d['semantic_links_reviewed']=True;p.write_text(json.dumps(d))
  with self.assertRaises(ValueError):M.verify(self.root)
 def test_exact_prior(self):
  d=json.loads((self.root/'pending-interface-entry.json').read_text());M.restore_interface_entry_fixture(self.root)
  for name,item in d['files'].items():self.assertEqual((self.root/name).read_bytes(),item['prior'].encode())
  M.verify(self.root)
 def test_symlink(self):
  p=self.root/'pending-interface-entry.json';p.rename(self.root/'saved');p.symlink_to('saved')
  with self.assertRaisesRegex(ValueError,'Interface entry evidence unsafe'):M.verify(self.root)
 def test_missing(self):
  (self.root/'pending-interface-entry.json').unlink()
  with self.assertRaises(ValueError):M.verify(self.root)
