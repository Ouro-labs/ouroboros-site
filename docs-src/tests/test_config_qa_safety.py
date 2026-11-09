from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]/'content'
class ConfigQASafetyTest(unittest.TestCase):
 def test_boolean_scope_and_backup(self):
  for name in ('config-reference-guide.md','operations-detail.md'):
   with self.subTest(page=name):
    s=(ROOT/name).read_text()
    for x in ('`true` 또는 `false`','기존 설정을 안전하게 보존','같은 설치·설정 환경','`on`이나 오타도 false','Pydantic'):self.assertIn(x,s)
 def test_threshold_scope(self):
  for name in ('qa-detail.md','mcp-reference-guide.md'):
   with self.subTest(page=name):
    s=(ROOT/name).read_text()
    for x in ('유한','0~1','PASS를 신뢰하지 마세요','5f5fca90662861201ff0a26f502edd22b272c4c6'):self.assertIn(x,s)
