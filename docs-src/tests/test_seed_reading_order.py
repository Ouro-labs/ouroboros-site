"""Protect the existing Seed heading destinations and pre-execution warning."""
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
class Headings(HTMLParser):
    def __init__(self):super().__init__();self.headings={};self.current=None;self.skip=False
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if self.current and tag=='a' and 'headerlink' in d.get('class','').split():self.skip=True
        if tag in ('h1','h2','h3','h4','h5','h6') and d.get('id'):self.current=d['id'];self.headings[self.current]=''
    def handle_endtag(self,tag):
        if tag=='a':self.skip=False
        if tag in ('h1','h2','h3','h4','h5','h6'):self.current=None
    def handle_data(self,data):
        if self.current and not self.skip:self.headings[self.current]+=data
class SeedReadingOrderTest(unittest.TestCase):
    def test_existing_heading_meanings(self):
        p=Headings();p.feed((ROOT/'site/docs/seed-guide/index.html').read_text())
        expected={'seed':'Seed: 실행 전에 작업 기준을 검토하기','seed_1':'Seed 만들기','seed_2':'예제 Seed 읽기','_1':'각 부분에서 확인할 것','seed-execution-and-evaluation-evidence':'실행 게이트와 정식 평가의 증거를 구분하기','seed_3':'Seed가 틀렸으면 수정하기','run-reviewed-seed':'언제 실행으로 넘어가나요?','_2':'분기와 문제 해결'}
        for key,title in expected.items():self.assertEqual(p.headings.get(key,'').strip(),title,key)
    def test_release_source_links_are_specific(self):
        source=(ROOT/'docs-src/content/seed-guide.md').read_text()
        release='5f5fca90662861201ff0a26f502edd22b272c4c6'
        main='592c667f076c3dad7ef68d7844e91480d80135d0'
        for label,rev,path in (
            ('기록 조회',release,'src/ouroboros/mcp/tools/evaluation_handlers.py#L739-L760'),
            ('Stage 1 기록 병합',release,'src/ouroboros/evaluation/models.py#L190-L203'),
            ('승인 조건',release,'src/ouroboros/evaluation/models.py#L568-L605'),
            ('release 명령 실행',release,'src/ouroboros/orchestrator/parallel_executor.py#L9787-L9792'),
            ('main 명령 실행',main,'src/ouroboros/orchestrator/parallel_executor.py#L9807-L9812'),
        ):
            self.assertIn(f'[{label}](https://github.com/Q00/ouroboros/blob/{rev}/{path})',source)

    def test_warning_and_reading_order(self):
        s=(ROOT/'docs-src/content/seed-guide.md').read_text()
        marks=['## 예제 Seed 읽기','실제 Seed에 `verify_command`','## Seed가 틀렸으면 수정하기','## 언제 실행으로 넘어가나요?','## 각 부분에서 확인할 것']
        positions=[s.index(m) for m in marks];self.assertEqual(positions,sorted(positions))
        self.assertIn('실행 위치, 셸 동작과 외부 효과를 먼저 확인',s)
if __name__=='__main__':unittest.main()
