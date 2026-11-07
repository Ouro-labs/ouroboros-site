from pathlib import Path
import unittest

class HomeSourceLabelsTest(unittest.TestCase):
    def test_prior_source_labels_and_current_guides(self):
        text=(Path(__file__).resolve().parents[1]/'content/index.md').read_text()
        for label,target in [('핵심 개념','concepts-detail'),('Seed 형식 참조','seed-format-detail'),('기존 프로젝트','existing-project-detail'),('평가와 진화','evaluation-evolution-detail'),('MCP 도구','mcp-reference-detail'),('설정','config-reference-detail'),('아키텍처','architecture-detail'),('코드 영역 지도','architecture-map-public')]:
            with self.subTest(target=target):self.assertIn(f'[{label} (이전 소스 기준)](/docs/{target}/)',text)
        for label,target in [('빠른 시작','quickstart'),('Interview 안내','interview-guide'),('Seed 안내','seed-guide')]:self.assertIn(f'[{label}](/docs/{target}/)',text)
