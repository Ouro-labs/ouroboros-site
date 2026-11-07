"""Name heading permalinks using visible heading text at build time."""
from html import escape
from html.parser import HTMLParser
import re

HEADING = re.compile(r'(<h[1-6]\b[^>]*>)(.*?)(</h[1-6]>)', re.DOTALL | re.IGNORECASE)
LINK = re.compile(r'<a\b(?=[^>]*\bclass=["\'][^"\']*\bheaderlink\b)[^>]*>.*?</a>', re.DOTALL | re.IGNORECASE)

class Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
    def handle_data(self, data):
        self.parts.append(data)

def on_page_content(html, page, **kwargs):
    uri = page.file.src_uri
    prefix = 'Link to heading: ' if uri.startswith('en/') else ('标题链接：' if uri.startswith('zh/') else '제목 링크: ')
    def heading(match):
        body = match.group(2)
        links = list(LINK.finditer(body))
        if not links:
            return match.group(0)
        if len(links) != 1:
            raise ValueError('Multiple heading permalinks in '+uri)
        link = links[0]
        parser = Text(); parser.feed(body[:link.start()] + body[link.end():])
        title = ' '.join(''.join(parser.parts).split())
        if not title:
            raise ValueError('Empty heading permalink label in '+uri)
        raw = link.group(0)
        if re.search(r'\baria-label\s*=', raw, re.IGNORECASE):
            raise ValueError('Unexpected existing heading permalink label in '+uri)
        named = raw.replace('<a ', '<a aria-label="'+escape(prefix+title, quote=True)+'" ', 1)
        return match.group(1)+body[:link.start()]+named+body[link.end():]+match.group(3)
    return HEADING.sub(heading, html)
