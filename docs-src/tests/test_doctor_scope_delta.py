import importlib.util,json,shutil,tempfile,unittest,sys,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
spec=importlib.util.spec_from_file_location('doctor_scope_pending',ROOT/'verify-pending-guides.py');M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
class DoctorScopeDelta(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)/'docs-src'
  shutil.copytree(ROOT,self.root,ignore=shutil.ignore_patterns('__pycache__'));shutil.copytree(ROOT.parent/'site',self.root.parent/'site',ignore=shutil.ignore_patterns('docs'))
  if (self.root/'pending-search-results-inert.json').exists(): M.restore_search_results_inert_fixture(self.root)
 def test_normal(self):M.verify(self.root)
 def test_each_page_and_manifest(self):
  for name in ['content/ai-troubleshooting.md', 'content/en/ai-troubleshooting.md', 'content-manifest.json']:
   with self.subTest(name=name):
    p=self.root/name;b=p.read_bytes();p.write_bytes(b+b'tamper')
    try:
     with self.assertRaisesRegex(ValueError,'Doctor scope current bytes'):M.verify(self.root)
    finally:p.write_bytes(b)
 def test_simultaneous_rebinding(self):
  M.verify(self.root)
  page=self.root/'content/en/ai-troubleshooting.md';page.write_text(page.read_text()+'tamper')
  manifest=self.root/'content-manifest.json';d=json.loads(manifest.read_text());d['pages']['en/ai-troubleshooting.md']['page_sha256']=hashlib.sha256(page.read_bytes()).hexdigest();manifest.write_text(json.dumps(d))
  rec=self.root/'pending-doctor-scope.json';d=json.loads(rec.read_text())
  for name in ['content/en/ai-troubleshooting.md','content-manifest.json']:d['files'][name]['current']=(self.root/name).read_text()
  rec.write_text(json.dumps(d))
  with self.assertRaisesRegex(ValueError,'Doctor scope evidence changed'):M.verify(self.root)
 def test_prior_evidence(self):
  M.verify(self.root);(self.root/'pending-search-locale.json').write_text('{}')
  with self.assertRaisesRegex(ValueError,'Search locale evidence changed'):M.verify(self.root)
 def test_gate(self):
  M.verify(self.root);p=self.root/'content-manifest.json';d=json.loads(p.read_text());d['semantic_links_reviewed']=True;p.write_text(json.dumps(d))
  with self.assertRaises(ValueError):M.verify(self.root)
 def test_exact_prior(self):
  d=json.loads((self.root/'pending-doctor-scope.json').read_text());M.restore_doctor_scope_fixture(self.root)
  for name,item in d['files'].items():self.assertEqual((self.root/name).read_bytes(),item['prior'].encode())
  M.verify(self.root)
 def test_symlink(self):
  p=self.root/'pending-doctor-scope.json';p.rename(self.root/'saved');p.symlink_to('saved')
  with self.assertRaisesRegex(ValueError,'Doctor scope evidence unsafe'):M.verify(self.root)
 def test_missing(self):
  (self.root/'pending-doctor-scope.json').unlink()
  with self.assertRaises(ValueError):M.verify(self.root)
