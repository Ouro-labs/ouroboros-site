from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]/'content/en/ai-troubleshooting.md'
class ManualTableTest(unittest.TestCase):
 def test_source_navigation_and_ids(self):
  s=ROOT.read_text()
  for x in ('[MCP connection](#mcp-connection-or-authentication-fails)','[Status and recovery](#recovery)','| What you have | Standalone CLI command | Next step |','chained_evaluate_job_id','chained_ralph_job_id'):self.assertIn(x,s)
