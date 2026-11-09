"""Check rendered descriptions, exported Markdown and translated notice placement."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[2]
PAGES={'index.md':'index.html','quickstart.md':'quickstart/index.html','en/quickstart.md':'en/quickstart/index.html','zh/quickstart.md':'zh/quickstart/index.html','ai-troubleshooting.md':'ai-troubleshooting/index.html','existing-project-detail.md':'existing-project-detail/index.html'}
class Metadata(HTMLParser):
    def __init__(self):super().__init__();self.descriptions=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag=='meta' and d.get('name')=='description':self.descriptions.append(d.get('content'))
class DescriptionsTest(unittest.TestCase):
    def test_page_descriptions_and_export(self):
        values=[]
        for name,html_name in PAGES.items():
            with self.subTest(name=name):
                data=(ROOT/'docs-src/content'/name).read_bytes()
                self.assertEqual(data,(ROOT/'site/docs/markdown'/name).read_bytes())
                self.assertRegex(data.decode(),r'\A---\ndescription: .+\n---\n')
                parser=Metadata();parser.feed((ROOT/'site/docs'/html_name).read_text());self.assertEqual(len(parser.descriptions),1);self.assertTrue(parser.descriptions[0]);values.extend(parser.descriptions)
        self.assertEqual(len(set(values)),6)
    def test_translation_notices_follow_h1(self):
        for name,phrase in (('en/quickstart/index.html','Partial translation:'),('zh/quickstart/index.html','部分翻译：')):
            with self.subTest(name=name):
                s=(ROOT/'site/docs'/name).read_text();self.assertLess(s.index('<h1'),s.index(phrase));self.assertLess(s.index(phrase),s.index('<h2',s.index('<h1')))
if __name__=='__main__':unittest.main()
