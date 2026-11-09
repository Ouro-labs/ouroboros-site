import importlib.util
from pathlib import Path
import unittest
import shutil
import tempfile

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('scope_pending',ROOT/'verify-pending-guides.py')
M=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)

class ScopeDeltaTest(unittest.TestCase):
 def setUp(self):self.current=(ROOT.parent/'site/llms.txt').read_bytes()
 def test_exact_prior_hash_is_still_required(self):
  import json
  prior=M.restore_public_index_prior(self.current)
  expected=json.loads((ROOT/'pending-ai-manual.json').read_text())['files']['site/llms.txt']
  self.assertEqual(M.sha(prior),expected)
 def test_missing_delta_rejected(self):
  with self.assertRaises(ValueError):M.restore_public_index_prior(self.current.replace(M.PUBLIC_INDEX_SCOPE_ADDITION,b''))
 def test_duplicate_delta_rejected(self):
  with self.assertRaises(ValueError):M.restore_public_index_prior(self.current+M.PUBLIC_INDEX_SCOPE_ADDITION)
 def test_changed_delta_rejected(self):
  with self.assertRaises(ValueError):M.restore_public_index_prior(self.current.replace(b'That historical scope',b'Altered historical scope'))
 def test_unrelated_change_does_not_rebind_prior(self):
  import json
  prior=M.restore_public_index_prior(self.current.replace(b'# Ouroboros',b'# Forged',1))
  expected=json.loads((ROOT/'pending-ai-manual.json').read_text())['files']['site/llms.txt']
  self.assertNotEqual(M.sha(prior),expected)
 def test_moved_delta_rejected(self):
  moved=self.current.replace(M.PUBLIC_INDEX_SCOPE_ADDITION,b'')+M.PUBLIC_INDEX_SCOPE_ADDITION
  with self.assertRaisesRegex(ValueError,'pending scope delta'):M.restore_public_index_prior(moved)
 def test_changed_preceding_context_rejected(self):
  changed=self.current.replace(M.PUBLIC_INDEX_SCOPE_BEFORE,b'Altered context\n\n')
  with self.assertRaisesRegex(ValueError,'pending scope delta'):M.restore_public_index_prior(changed)
 def test_changed_following_context_rejected(self):
  changed=self.current.replace(M.PUBLIC_INDEX_SCOPE_AFTER,b'- Altered next link\n')
  with self.assertRaisesRegex(ValueError,'pending scope delta'):M.restore_public_index_prior(changed)
 def test_verify_root_accepts_current_then_rejects_moved_delta(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp)/'docs-src'
   shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('__pycache__'))
   # Nested pending restorers need the complete site fixture, not only the two
   # files asserted directly by this suite.
   shutil.copytree(ROOT.parent/'site',root.parent/'site',ignore=shutil.ignore_patterns('docs'))
   M.verify(root) # Ensure mutation reaches the real current verifier boundary.
   path=root.parent/'site/llms.txt'
   path.write_bytes(self.current.replace(M.PUBLIC_INDEX_SCOPE_ADDITION,b'')+M.PUBLIC_INDEX_SCOPE_ADDITION)
   with self.assertRaisesRegex(ValueError,'AI manual file changed: site/llms.txt .*pending scope delta'):
    M.verify(root)

if __name__=='__main__':unittest.main()
