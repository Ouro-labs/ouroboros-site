"""Protect the Megacode CLI warning and detailed boundary destination."""
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
class Page(HTMLParser):
    def __init__(self):super().__init__();self.ids=set();self.links=[];self.text=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if d.get('id'):self.ids.add(d['id'])
        if tag=='a' and d.get('href'):self.links.append(d['href'])
    def handle_data(self,data):self.text.append(data)
class MegacodeWarningTest(unittest.TestCase):
    def test_warning_precedes_both_examples(self):
        p=Page();p.feed((ROOT/'site/docs/megacode-guide/index.html').read_text());s=''.join(p.text)
        warn=s.index('CLI 실행 전에 별도 격리 경계를 확인하세요')
        first=s.index('ouroboros run workflow seed.yaml --runtime megacode')
        second=s.index('OUROBOROS_LLM_BACKEND=megacode ouroboros run workflow seed.yaml --runtime megacode')
        self.assertLess(warn,first);self.assertLess(warn,second)
        self.assertIn('megacode-cli-sandbox-boundary',p.ids);self.assertIn('#megacode-cli-sandbox-boundary',p.links)
        self.assertIn('harness -p --sandbox off',s)
if __name__=='__main__':unittest.main()
