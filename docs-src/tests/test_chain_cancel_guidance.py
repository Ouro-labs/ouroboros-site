from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]/'content'
class ChainCancelTest(unittest.TestCase):
 def test_chain_ids_and_user_decision(self):
  for name in ('status-guide.md','recovery-detail.md','ai-troubleshooting.md','en/ai-troubleshooting.md'):
   s=(ROOT/name).read_text()
   for x in ('chained_evaluate_job_id','chained_ralph_job_id','ouroboros_cancel_job'):
    with self.subTest(page=name,value=x):self.assertIn(x,s)
