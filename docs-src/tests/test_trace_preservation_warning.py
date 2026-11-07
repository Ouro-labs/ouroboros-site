"""Protect trace preservation warning placement and distinct destinations."""
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
class Page(HTMLParser):
    def __init__(self):super().__init__();self.ids=[];self.links=[];self.text=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if d.get('id'):self.ids.append(d['id'])
        if tag=='a' and d.get('href'):self.links.append(d['href'])
    def handle_data(self,data):self.text.append(data)
class TracePreservationTest(unittest.TestCase):
    def test_warning_precedes_three_commands_and_target_is_unique(self):
        p=Page();p.feed((ROOT/'site/docs/harness-traces-guide/index.html').read_text());s=''.join(p.text)
        warn=s.index('를 실행하기 전에 trace 보존 여부를 확인하세요')
        for command in ('ouroboros harness show','ouroboros harness trace','ouroboros harness diff'):
            self.assertLess(warn,s.index(command),command)
        self.assertEqual(p.ids.count('trace-projection-file-effects'),1)
        self.assertIn('#trace-projection-file-effects',p.links)
        self.assertEqual(p.ids.count('export-db'),1)
if __name__=='__main__':unittest.main()
