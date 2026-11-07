from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]/'content'
class WorktreeWarningPlacementTest(unittest.TestCase):
    def test_warning_before_execution_paths(self):
        for name, warning, stop in [('quickstart.md','실행 전 관리 worktree 경로 확인','확인할 수 없다면 실행을 보류'),('en/quickstart.md','Check the managed worktree path before execution','If you cannot verify them, defer execution'),('zh/quickstart.md','运行前检查受管理 worktree 路径','如果无法确认，请暂缓执行')]:
            with self.subTest(page=name):
                text=(ROOT/name).read_text();i=text.index(warning);self.assertLess(i,text.index('ooo interview'));self.assertLess(i,text.index('ouroboros init start'));self.assertLess(i,text.index(stop));self.assertIn('durable_id',text[i:text.index('ooo interview')])
        text=(ROOT/'existing-project-detail.md').read_text();i=text.index('작업 worktree 준비 경로의 기존 파일을 먼저 확인하세요');self.assertLess(i,text.index('### 호스트 플러그인에서 시작'));self.assertLess(i,text.index('ouroboros run /path/to/seed.yaml'));self.assertIn('확인할 수 없다면 실행을 보류',text[i:text.index('### 호스트 플러그인에서 시작')])
