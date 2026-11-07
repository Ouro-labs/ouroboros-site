from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]/'content'
class WorktreeIdPreflightTest(unittest.TestCase):
 def test_new_id_unknown_and_resume_distinct(self):
  items={'quickstart.md':['정확한 새 경로를 미리 알 수 없습니다','재개는 실제 세션 ID','동시 변경에 따른 위험','[기존 프로젝트 안내]'], 'en/quickstart.md':['exact new path is not known beforehand','For a resume','Concurrent changes can still create risk','[the existing-project guide (Korean)]'], 'zh/quickstart.md':['无法事先知道精确的新路径','恢复时','检查后仍可能发生并发变化','[现有项目指南（韩文）]'], 'existing-project-detail.md':['정확한 새 경로를 미리 알 수 없습니다','재개라면 실제 세션 ID','동시 변경에 따른 위험']}
  for name,phrases in items.items():
   with self.subTest(page=name):
    s=(ROOT/name).read_text()
    for phrase in phrases:self.assertIn(phrase,s)
    self.assertIn('git worktree list --porcelain',s)
