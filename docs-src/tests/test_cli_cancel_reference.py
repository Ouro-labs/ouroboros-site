from pathlib import Path
import unittest

class CLICancelReferenceTest(unittest.TestCase):
    def test_list_and_cancel_scope(self):
        text=(Path(__file__).resolve().parents[1]/'content/cli-reference-guide.md').read_text()
        for value in ('실행 취소: 상태 변경','cancel execution --list','선택·취소 없이','이벤트 저장소 초기화','--all','일시 중지된 세션','취소 요청·실제 취소·실패'):
            with self.subTest(value=value):self.assertIn(value,text)
    def test_session_identifiers_distinguished(self):
        text=(Path(__file__).resolve().parents[1]/'content/mcp-reference-guide.md').read_text()
        for value in ('오케스트레이터 세션 ID 또는 `auto_` 세션 ID','Interview 세션 ID나 job ID와 혼용하지 않음'):
            with self.subTest(value=value):self.assertIn(value,text)
