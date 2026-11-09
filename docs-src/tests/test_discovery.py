"""Check generated quickstart alternates and local AI-index links."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import re
import unittest

SITE = Path(__file__).resolve().parents[2]/'site'
EXPECTED = {
    'ko': 'https://ouroboros.page/docs/quickstart/',
    'en': 'https://ouroboros.page/docs/en/quickstart/',
    'zh-Hans': 'https://ouroboros.page/docs/zh/quickstart/',
}
class Metadata(HTMLParser):
    def __init__(self): super().__init__(); self.canonicals=[]; self.alternates=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='link' and a.get('rel')=='canonical': self.canonicals.append(a.get('href'))
        if tag=='link' and a.get('rel')=='alternate' and a.get('hreflang'): self.alternates.append((a['hreflang'],a.get('href')))
class DiscoveryTest(unittest.TestCase):
    def test_quickstart_reciprocal_and_canonical(self):
        for url in EXPECTED.values():
            with self.subTest(url=url):
                file=SITE/urlsplit(url).path.lstrip('/')/'index.html'
                self.assertTrue(file.is_file()); meta=Metadata();meta.feed(file.read_text())
                self.assertEqual(meta.canonicals,[url]);self.assertCountEqual(meta.alternates,EXPECTED.items())
    def test_ai_index_local_docs_exist(self):
        links=re.findall(r'https://ouroboros\.page/docs/[^\s]+',(SITE/'llms.txt').read_text())
        self.assertTrue(links)
        for url in links:
            with self.subTest(url=url):
                file=SITE/urlsplit(url).path.lstrip('/')
                if file.is_dir():file=file/'index.html'
                self.assertTrue(file.is_file())
    def test_no_unverified_troubleshooting_alternates(self):
        for name in ('en/troubleshooting','zh/troubleshooting'):
            meta=Metadata();meta.feed((SITE/'docs'/name/'index.html').read_text())
            self.assertEqual(meta.alternates,[])
if __name__=='__main__': unittest.main()
