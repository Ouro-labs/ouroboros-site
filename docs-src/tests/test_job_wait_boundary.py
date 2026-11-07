from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]/'content'
class JobWaitBoundaryTest(unittest.TestCase):
 def test_zero_and_positive_timeout(self):
  s=(ROOT/'mcp-reference-detail.md').read_text()
  for x in ('timeout_seconds=0','snapshot·DB 조회 응답시간의 상한이 아닙니다','guard를 적용하지 않으므로','wait_timed_out: true','작업의 종료나 취소가 아닙니다','5f5fca90662861201ff0a26f502edd22b272c4c6'):self.assertIn(x,s)
  s=(ROOT/'status-guide.md').read_text();self.assertIn('snapshot·DB 응답시간을 제한하지 않습니다',s);self.assertIn('같은 job ID·서버·소유자',s)
