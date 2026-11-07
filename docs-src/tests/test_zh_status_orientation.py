"""Keep the Chinese status deep link connected to the ID table."""
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
class Page(HTMLParser):
    def __init__(self):super().__init__();self.h={};self.current=None;self.skip=False;self.text=[];self.links=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if self.current and tag=='a' and 'headerlink' in d.get('class','').split():self.skip=True
        if tag in ('h1','h2','h3','h4','h5','h6') and d.get('id'):self.current=d['id'];self.h[self.current]=''
        if tag=='a' and d.get('href'):self.links.append(d['href'])
    def handle_endtag(self,tag):
        if tag=='a':self.skip=False
        if tag in ('h1','h2','h3','h4','h5','h6'):self.current=None
    def handle_data(self,data):
        self.text.append(data)
        if self.current and not self.skip:self.h[self.current]+=data
class ChineseStatusOrientationTest(unittest.TestCase):
    def test_existing_table_heading_and_status_orientation(self):
        p=Page();p.feed((ROOT/'site/docs/zh/troubleshooting/index.html').read_text());s=''.join(p.text)
        self.assertEqual(p.h.get('_2','').strip(),'先保存这些信息')
        self.assertEqual(p.h.get('status','').strip(),'查看当前状态')
        self.assertIn('#_2',p.links)
        start=s.index('查看当前状态',s.index('先保存这些信息'))
        warning=s.index('使用下面的命令前，请先阅读上方',start)
        command=s.index('ouroboros status executions',warning)
        self.assertLess(warning,command)
        self.assertIn('不要把 Interview 返回的',s[warning:command])
if __name__=='__main__':unittest.main()
