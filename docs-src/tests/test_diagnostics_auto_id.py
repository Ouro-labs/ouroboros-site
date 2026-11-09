"""Protect the distinction between CLI and MCP session ID scope."""
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
class Text(HTMLParser):
    def __init__(self):super().__init__();self.parts=[]
    def handle_data(self,text):self.parts.append(text)
class DiagnosticsAutoIdTest(unittest.TestCase):
    def test_cli_and_mcp_scope_is_visible(self):
        for path,cli,mcp in (
            ('ai-troubleshooting','오케스트레이터 세션 ID만 받습니다','auto 세션 상태'),
            ('en/ai-troubleshooting','accepts orchestrator session IDs only','auto-session status'),
        ):
            with self.subTest(path=path):
                p=Text();p.feed((ROOT/'site/docs'/path/'index.html').read_text());s=''.join(p.parts)
                self.assertIn(cli,s);self.assertIn(mcp,s);self.assertIn('ouroboros_session_status',s);self.assertIn('auto_<id>',s)
if __name__=='__main__':unittest.main()
