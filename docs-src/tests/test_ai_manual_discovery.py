"""Ensure the English AI-index manual links point at the generated manual."""
import json
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
class Lang(HTMLParser):
    def __init__(self):super().__init__();self.lang=None
    def handle_starttag(self,tag,attrs):
        if tag=='html':self.lang=dict(attrs).get('lang')

class ManualDiscoveryTest(unittest.TestCase):
    def test_manual_targets_and_source(self):
        text=(ROOT/'site/llms.txt').read_text()
        for url in ('https://ouroboros.page/docs/en/ai-troubleshooting/','https://ouroboros.page/docs/markdown/en/ai-troubleshooting.md'):
            self.assertEqual(text.count(url),1)
        html=ROOT/'site/docs/en/ai-troubleshooting/index.html';p=Lang();p.feed(html.read_text());self.assertEqual(p.lang,'en')
        exported=ROOT/'site/docs/markdown/en/ai-troubleshooting.md';source=ROOT/'docs-src/content/en/ai-troubleshooting.md'
        self.assertEqual(exported.read_bytes(),source.read_bytes())
        body=source.read_text();self.assertIn('592c667f',body);self.assertIn('Version boundary',body)
        manifest=json.loads((ROOT/'docs-src/content-manifest.json').read_text());self.assertEqual(manifest['pages']['en/ai-troubleshooting.md']['source'],'content/ai-troubleshooting-en.md')
