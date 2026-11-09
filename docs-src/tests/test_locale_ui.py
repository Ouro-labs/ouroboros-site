"""Check locally built locale UI and destination links (build before running)."""
from html.parser import HTMLParser
from pathlib import Path
import unittest

SITE = Path(__file__).resolve().parents[2] / 'site'

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.lang = None; self.attrs = []; self.links = []; self.text = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'html': self.lang = a.get('lang')
        if tag == 'a' and a.get('href'): self.links.append(a['href'])
        self.attrs += [v for k, v in attrs if v and k in ('aria-label', 'placeholder', 'data-label-open', 'data-label-close')]
    def handle_data(self, data): self.text.append(data)

class LocaleUITest(unittest.TestCase):
    def test_all_translated_pages(self):
        locales = {
            'en': ('en', 'Search', 'Open documentation navigation', '/learn/en/', '(Korean)'),
            'zh': ('zh-Hans', '搜索', '打开文档目录', '/learn/zh/', '（韩文）'),
        }
        for locale, (lang, search, nav, prefix, notice) in locales.items():
            files = list((SITE/'docs'/locale).rglob('index.html'))
            self.assertTrue(files, locale)
            for f in files:
                with self.subTest(page=str(f)):
                    page = Page(); page.feed(f.read_text())
                    self.assertEqual(page.lang, lang)
                    self.assertIn(search, page.attrs); self.assertIn(nav, page.attrs)
                    for suffix in ('', 'install/', 'glossary/'):
                        href = prefix + suffix
                        self.assertIn(href, page.links)
                        self.assertTrue((SITE/href.lstrip('/')/'index.html').is_file())
                    self.assertTrue(any(notice in item for item in page.text))
                    self.assertTrue(any('Ouroboros Docs (Korean)' in item if locale == 'en' else 'Ouroboros 文档（韩文）' in item for item in page.attrs))
                    if locale == 'zh': self.assertTrue(any('跳到正文' in item for item in page.text))
                    self.assertNotIn('검색 열기', page.attrs)
                    self.assertNotIn('문서 목차 열기', page.attrs)

if __name__ == '__main__': unittest.main()
