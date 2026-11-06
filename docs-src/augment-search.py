#!/usr/bin/env python3
"""Add CJK search tokens to generated Chinese pages without changing page text."""
from html.parser import HTMLParser
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / 'site/docs/search/search_index.json'
HAN = re.compile(r'[\u3400-\u4dbf\u4e00-\u9fff]+')
# The wording is a natural task query; this section describes interrupted work.
ALIASES = {'zh/troubleshooting/#recovery': ['任务中断']}

class Text(HTMLParser):
    def __init__(self): super().__init__(); self.parts = []
    def handle_data(self, data): self.parts.append(data)

def tokens(text):
    result = set()
    for run in HAN.findall(text):
        for size in (1, 2, 3):
            result.update(run[i:i+size] for i in range(len(run)-size+1))
    return result

data = json.loads(INDEX.read_text(encoding='utf-8'))
seen = set()
for doc in data['docs']:
    location = doc['location']
    if not location.startswith('zh/'):
        continue
    parser = Text(); parser.feed(doc.get('text', ''))
    words = tokens(doc.get('title', '') + ' '.join(parser.parts))
    for alias in ALIASES.get(location, []):
        words |= tokens(alias)
        words.add(alias)
        seen.add(location)
    # A separate indexed field is not rendered as user-visible tags.
    doc['search_tokens'] = sorted(words)
if set(ALIASES) != seen:
    raise SystemExit('Chinese search alias section missing; review changed anchors')
# Material indexes declared fields, but its result template renders only
# title, text, and genuine tags. Leave the normal tags field untouched.
data['config']['fields']['search_tokens'] = {'boost': 1.0}
INDEX.write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':'))+'\n', encoding='utf-8')
print('Added Chinese search metadata; rendered page text is unchanged.')
