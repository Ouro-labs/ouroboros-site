"""Check homepage entry points and Korean header labels on built pages."""
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.current=None; self.text=[]; self.canonical=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='a': self.current=a.get('href'); self.text=[]
        if tag=='link' and a.get('rel')=='canonical': self.canonical.append(a.get('href'))
    def handle_data(self, data):
        if self.current is not None: self.text.append(data)
    def handle_endtag(self, tag):
        if tag=='a' and self.current is not None:
            self.links.append((self.current, ' '.join(''.join(self.text).split()))); self.current=None

def parse(path):
    p=Links();p.feed(path.read_text(encoding='utf-8'));return p

class HomeDiscoveryTest(unittest.TestCase):
    def test_home_targets_and_labels(self):
        p=parse(ROOT/'site/index.html');links=dict(p.links)
        for path in ('/docs/en/quickstart/','/docs/en/troubleshooting/','/learn/en/','/learn/en/troubleshooting/'):
            self.assertTrue((ROOT/'site'/path.lstrip('/')/'index.html').is_file(),path)
            self.assertIn(path,links)
        self.assertIn('draft',links['/docs/en/quickstart/'].lower())
        self.assertIn('partial',links['/docs/en/troubleshooting/'].lower())
        self.assertIn('0.51.5',links['/learn/en/'])
        self.assertIn('0.51.5',links['/learn/en/troubleshooting/'])
        self.assertEqual(p.canonical,['https://ouroboros.page/'])
    def test_small_home_header_wraps_without_hiding_links(self):
        home=(ROOT/'site/index.html').read_text(encoding='utf-8')
        self.assertIn('@media(max-width:800px)',home)
        self.assertIn('.top nav{width:100%;margin-left:0;flex-wrap:wrap;',home)
        self.assertIn('.top nav a[data-aux]{display:inline}',home)
    def test_small_header_wraps_without_hiding_links(self):
        template=(ROOT/'docs-src/overrides/main.html').read_text(encoding='utf-8')
        self.assertIn('@media (max-width: 800px)',template)
        self.assertIn('flex-wrap: wrap',template)
        self.assertIn('.ouro-nav a:nth-child(2), .ouro-nav a:nth-child(3) { display: inline; }',template)
    def test_korean_header(self):
        p=parse(ROOT/'site/docs/quickstart/index.html'); links=dict(p.links)
        self.assertEqual(links['/docs/quickstart/'],'빠른 시작 (592 초안)')
        self.assertEqual(links['/learn/install/'],'설치 기초 (0.51.5)')
        self.assertTrue((ROOT/'site/learn/install/index.html').is_file())
