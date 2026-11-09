import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class WorktreeHeadingAnchorsTest(unittest.TestCase):
    def test_existing_headings_and_new_explicit_ids(self):
        source = (ROOT / 'content/existing-project-detail.md').read_text()
        headings = re.findall(r'^#{1,6} (.+)$', source, re.MULTILINE)
        expected = [
            '기존 프로젝트에서 시작하기', '현재 상황', '입력',
            '호스트 플러그인에서 시작', '독립 CLI에서 시작',
            'Seed 경로가 거부되거나 예상과 다를 때', '예상', '확인',
            '별도 작업 결과를 원래 프로젝트에 반영하기', '하위 프로젝트의 실행 위치 구분', '다음 행동',
        ]
        old = [re.sub(r' \{#[^}]+\}$', '', h) for h in headings
               if not h.endswith('{#worktree-preflight}') and not h.endswith('{#worktree-inputs}')]
        self.assertEqual(old, expected)
        self.assertEqual(headings.count('실행 전 저장소 기준을 기록하세요 {#worktree-preflight}'), 1)
        self.assertEqual(headings.count('작업 worktree의 기존 변경과 검증 설정 확인 {#worktree-inputs}'), 1)
        self.assertEqual(headings.count('하위 프로젝트의 실행 위치 구분 {#subproject-result}'), 1)

if __name__ == '__main__':
    unittest.main()
