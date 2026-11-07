from html.parser import HTMLParser
from pathlib import Path
import unittest

class DetailsParser(HTMLParser):
 def __init__(self):super().__init__();self.details=0;self.summaries=[];self.capture=False;self.codes=[];self.code=None;self.links=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='details':self.details+=1
  if tag=='summary' and self.details:self.capture=True
  if tag=='code' and self.details:self.code=[]
  if tag=='a' and self.details:self.links.append(a.get('href'))
 def handle_data(self,data):
  if self.capture:self.summaries.append(data)
  if self.code is not None:self.code.append(data)
 def handle_endtag(self,tag):
  if tag=='summary':self.capture=False
  if tag=='code' and self.code is not None:self.codes.append(''.join(self.code));self.code=None
  if tag=='details':self.details-=1
class ReferenceDetailsTest(unittest.TestCase):
 def test_details_contains_inert_example_and_links(self):
  root=Path(__file__).resolve().parents[2];p=DetailsParser();p.feed((root/'site/docs/todo-reference-example/index.html').read_text())
  self.assertIn('선택형 자동 브라우저 테스트', ''.join(p.summaries));self.assertTrue(any('from playwright.sync_api import Page' in x for x in p.codes));self.assertTrue(p.links);self.assertEqual(p.details,0)
