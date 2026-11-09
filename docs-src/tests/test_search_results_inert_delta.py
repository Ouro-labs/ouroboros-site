import importlib.util,json,shutil,tempfile,unittest,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
spec=importlib.util.spec_from_file_location('focus_pending',ROOT/'verify-pending-guides.py');M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
class SearchResultsInertDelta(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)/'docs-src'
  shutil.copytree(ROOT,self.root,ignore=shutil.ignore_patterns('__pycache__'));shutil.copytree(ROOT.parent/'site',self.root.parent/'site',ignore=shutil.ignore_patterns('docs'))
 def test_normal(self):M.verify(self.root)
 def test_script_tamper(self):
  p=self.root/'content/assets/ouro-theme.js';p.write_text(p.read_text()+'tamper')
  with self.assertRaisesRegex(ValueError,'Search results inert current bytes'):M.verify(self.root)
 def test_record_script_rebinding(self):
  M.verify(self.root)
  p=self.root/'content/assets/ouro-theme.js';p.write_text(p.read_text()+'tamper')
  r=self.root/'pending-search-results-inert.json';d=json.loads(r.read_text());d['files']['content/assets/ouro-theme.js']['current']=p.read_text();r.write_text(json.dumps(d))
  with self.assertRaisesRegex(ValueError,'Search results inert evidence changed'):M.verify(self.root)
 def test_old_locale_record_tamper(self):
  M.verify(self.root)
  (self.root/'pending-search-locale.json').write_text('{}')
  with self.assertRaisesRegex(ValueError,'Search locale evidence changed'):M.verify(self.root)
 def test_open_gate(self):
  M.verify(self.root)
  p=self.root/'content-manifest.json';d=json.loads(p.read_text());d['semantic_links_reviewed']=True;p.write_text(json.dumps(d))
  with self.assertRaisesRegex(ValueError,'Search results inert requires closed gate'):M.verify(self.root)
 def test_missing(self):
  (self.root/'pending-search-results-inert.json').unlink()
  with self.assertRaises(ValueError):M.verify(self.root)
 def test_symlink(self):
  p=self.root/'pending-search-results-inert.json';p.rename(self.root/'saved.json');p.symlink_to('saved.json')
  with self.assertRaisesRegex(ValueError,'Search results inert evidence unsafe'):M.verify(self.root)
 def test_exact_prior(self):
  d=json.loads((self.root/'pending-search-results-inert.json').read_text());M.restore_search_results_inert_fixture(self.root)
  self.assertEqual((self.root/'content/assets/ouro-theme.js').read_bytes(),d['files']['content/assets/ouro-theme.js']['prior'].encode())
  self.assertEqual((self.root/'tests/test_search_escape.cjs').read_bytes(),d['files']['tests/test_search_escape.cjs']['prior'].encode())
  M.verify(self.root)
