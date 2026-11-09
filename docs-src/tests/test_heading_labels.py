"""Verify generated heading link names without changing destinations."""
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]/'site/docs'
class Parser(HTMLParser):
    def __init__(self):
        super().__init__();self.heading=None;self.depth=0;self.text=[];self.links=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag in ('h1','h2','h3','h4','h5','h6'):self.heading=a.get('id');self.text=[];self.links=[]
        elif self.heading is not None and tag=='a' and 'headerlink' in a.get('class','').split():self.depth+=1;self.links.append(a)
    def handle_data(self,data):
        if self.heading is not None and not self.depth:self.text.append(data)
    def handle_endtag(self,tag):
        if tag=='a' and self.depth:self.depth-=1
        elif tag in ('h1','h2','h3','h4','h5','h6') and self.heading is not None:
            if self.links: self.results.append((self.heading,' '.join(''.join(self.text).split()),self.links))
            self.heading=None
    results=None

class HeadingLabelsTest(unittest.TestCase):
    def test_every_generated_heading_link(self):
        total=0
        for path in ROOT.rglob('*.html'):
            p=Parser();p.results=[];p.feed(path.read_text(encoding='utf-8'))
            rel=path.relative_to(ROOT).as_posix()
            prefix='Link to heading: ' if rel.startswith('en/') else ('标题链接：' if rel.startswith('zh/') else '제목 링크: ')
            for id,title,links in p.results:
                self.assertEqual(len(links),1,rel)
                self.assertEqual(links[0].get('href'),'#'+id,rel)
                self.assertEqual(links[0].get('aria-label'),prefix+title,rel)
                self.assertNotIn('tabindex',links[0],rel)
                total+=1
        self.assertGreater(total,500)
