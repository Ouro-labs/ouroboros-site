import re
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
class SetupInterviewSplitTest(unittest.TestCase):
    def test_host_setup_is_scoped_and_interview_separate(self):
        phrases={'quickstart.md':('Claude Code 플러그인','Codex 플러그인','다음 메시지로 Interview'), 'en/quickstart.md':('Claude Code plugin','Codex plugin','next message in the host conversation'), 'zh/quickstart.md':('Claude Code 插件','Codex 插件','下一条消息中发送 Interview')}
        for name,(claude,codex,bridge) in phrases.items():
            with self.subTest(page=name):
                text=(ROOT/'content'/name).read_text();a=text.index(claude);b=text.index('```text\nooo setup\n```',a);c=text.index(codex,b);d=text.index(bridge,c);e=text.index('```text\nooo interview ',d);self.assertTrue(a<b<c<d<e);self.assertIn('MCP',text[c:d])
