import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class SetupInterviewSplitTest(unittest.TestCase):
    def test_separate_conversation_messages(self):
        phrases = {'quickstart.md': '설정 질문에 답해 설정을 마친 다음, 다음 메시지로 Interview를 요청합니다.', 'en/quickstart.md': 'Answer the setup questions and finish setup, then send the Interview request as the next message.', 'zh/quickstart.md': '回答设置问题并完成设置，然后在下一条消息中发送 Interview 请求。'}
        for name, phrase in phrases.items():
            with self.subTest(page=name):
                text=(ROOT/'content'/name).read_text()
                pattern=r'```text\nooo setup\n```\n\n'+re.escape(phrase)+r'\n\n```text\nooo interview "[^\n]+"\n```'
                self.assertRegex(text,pattern)
