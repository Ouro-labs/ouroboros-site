from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]/'content'
class CalibrationReceiptTest(unittest.TestCase):
 def test_korean_receipt_and_calibration(self):
  for n in ('ai-troubleshooting.md','mcp-reference-guide.md'):
   s=(ROOT/n).read_text()
   for x in ('calibration_input','interview_calibration','handler까지 전달된 경우','재개 분기','답변 분기','detached_job_acceptance_pending','job_handle_not_found','is_terminal: true','중복 실행하지 말고'):
    with self.subTest(page=n,value=x):self.assertIn(x,s)
 def test_status_and_english_limits(self):
  s=(ROOT/'status-guide.md').read_text();self.assertIn('job_wait',s);self.assertIn('worker가 이미 있을 수',s)
  s=(ROOT/'en/ai-troubleshooting.md').read_text()
  for x in ('calibration_input','interview_calibration','unsupported argument nevertheless reaches the handler','selects an answer','otherwise a resume','job_handle_not_found','do not start a duplicate'):self.assertIn(x,s)
