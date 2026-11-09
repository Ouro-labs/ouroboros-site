from pathlib import Path
import unittest

class MCPQueryReferenceTest(unittest.TestCase):
    def test_query_contract_and_limits_are_explained(self):
        text=(Path(__file__).resolve().parents[1]/'content/mcp-reference-guide.md').read_text()
        for value in ('{#query-events}','ouroboros_query_events','session_id','event_type','limit','offset','`50`','`0`','두 필터가 모두 생략되거나 빈 문자열이면 모든 세션의 모든 유형','100자','이번 응답에 들어온 개수','읽기 전용 연결을 지정하지 않고','디렉터리·DB·스키마','722172ef','5f5fca90662861201ff0a26f502edd22b272c4c6'):
            with self.subTest(value=value):self.assertIn(value,text)
