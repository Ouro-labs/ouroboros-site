from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
class Links(HTMLParser):
    def __init__(self): super().__init__(); self.links=[]
    def handle_starttag(self,tag,attrs):
        if tag=='a': self.links.append(dict(attrs))

class LandingQuickstartsTest(unittest.TestCase):
    def test_three_languages_and_historical_links(self):
        p=Links();p.feed((ROOT/'site/index.html').read_text()); links=p.links
        for path,lang in (('/docs/quickstart/','ko'),('/docs/en/quickstart/','en'),('/docs/zh/quickstart/','zh-Hans')):
            self.assertTrue(any(a.get('href')==path and a.get('lang')==lang for a in links),path)
            self.assertTrue((ROOT/'site'/path.lstrip('/')/'index.html').is_file(),path)
        for path in ('/learn/','/learn/en/','/learn/zh/'):
            self.assertTrue(any(a.get('href')==path for a in links),path)
    def test_example_separates_seed_and_execution(self):
        s=(ROOT/'site/index.html').read_text();section=s.split('<h2 id="quickstart">',1)[1].split('</ol>',1)[0]
        self.assertIn('to-do web app',section);self.assertIn('marks them complete',section)
        self.assertLess(section.index('ooo interview'),section.index('ooo seed'))
        self.assertLess(section.index('ooo seed'),section.index('ooo run'))
        self.assertIn('review the Seed YAML',section)
        self.assertNotIn('Build a task management CLI',section)
if __name__=='__main__':unittest.main()
