#!/usr/bin/env python3
"""Verify both advertised sitemaps and the generated documentation pages."""
import json
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET
from html.parser import HTMLParser

root = Path(__file__).resolve().parent.parent
site = root / 'site'
ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
origin = 'https://ouroboros.page'
robots = (site / 'robots.txt').read_text().splitlines()
advertised = {line.split(':', 1)[1].strip() for line in robots if line.lower().startswith('sitemap:')}
expected_sitemaps = {origin + '/sitemap.xml', origin + '/docs/sitemap.xml'}
if not expected_sitemaps <= advertised:
    raise SystemExit('Both root and documentation sitemaps must be advertised')

class Page(HTMLParser):
    def __init__(self): super().__init__(); self.canonical = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'link' and 'canonical' in a.get('rel', '').lower().split():
            self.canonical.append(a.get('href'))

def locations(path):
    return [n.text for n in ET.parse(path).findall('.//s:loc', ns)]

root_urls = locations(site / 'sitemap.xml')
doc_urls = locations(site / 'docs/sitemap.xml')
if len(doc_urls) != len(set(doc_urls)): raise SystemExit('Duplicate documentation sitemap URL')
manifest = json.loads((root / 'docs-src/content-manifest.json').read_text())
expected = {origin + '/docs/' + ('' if name == 'index.md' else name.removesuffix('.md') + '/')
            for name in manifest['pages']}
if set(doc_urls) != expected:
    raise SystemExit(f'Documentation sitemap mismatch: missing {sorted(expected-set(doc_urls))}; extra {sorted(set(doc_urls)-expected)}')
for url in root_urls + doc_urls:
    parsed = urlsplit(url)
    if parsed.scheme != 'https' or parsed.netloc != 'ouroboros.page': raise SystemExit(f'Unexpected URL: {url}')
    path = site / parsed.path.lstrip('/')
    path = path / 'index.html' if path.is_dir() else path
    if not path.is_file(): raise SystemExit(f'Missing sitemap page: {url}')
    if url in expected:
        page = Page(); page.feed(path.read_text())
        if page.canonical != [url]: raise SystemExit(f'Canonical mismatch: {url} -> {page.canonical}')
print(f'Both robots entries resolve; {len(root_urls)} existing and {len(doc_urls)} generated sitemap URLs verified.')
