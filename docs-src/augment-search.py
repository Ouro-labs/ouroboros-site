#!/usr/bin/env python3
"""Add CJK search tokens to generated Chinese pages without changing page text."""
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import hashlib

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / 'site/docs/search/search_index.json'
HAN = re.compile(r'[\u3400-\u4dbf\u4e00-\u9fff]+')
# The wording is a natural task query; this section describes interrupted work.
ALIASES = {'zh/troubleshooting/#recovery': ['任务中断']}

# Explicit reviewed output paths; unknown future pages receive no language label.
# Keep this list in sync with the manifest only after language review.
LANGUAGE_PAGES = {
    'ko': ['ac-recovery-detail.md', 'ai-troubleshooting.md', 'architecture-detail.md', 'architecture-map-public.md', 'artifacts-detail.md', 'auto-detail.md', 'check-package-detail.md', 'cleanup-detail.md', 'cli-reference-detail.md', 'cli-reference-guide.md', 'concepts-detail.md', 'config-reference-detail.md', 'config-reference-guide.md', 'dashboard-guide.md', 'diagnostics-detail.md', 'drift-detail.md', 'evaluation-evolution-detail.md', 'event-contract-detail.md', 'example-detail.md', 'existing-project-detail.md', 'fanout-detail.md', 'first-run-detail.md', 'harness-traces-guide.md', 'index.md', 'integration-detail.md', 'interview-detail.md', 'interview-guide.md', 'lifecycle-detail.md', 'mcp-reference-detail.md', 'mcp-reference-guide.md', 'mcp-schema-snapshot-detail.md', 'megacode-guide.md', 'model-routing-guide.md', 'opencode-bridge-detail.md', 'operations-detail.md', 'plugins-detail.md', 'progress-detail.md', 'python-api-detail.md', 'python-api-inventory-detail.md', 'qa-detail.md', 'query-projections-detail.md', 'quickstart.md', 'recovery-detail.md', 'routing-detail.md', 'runtime-support-detail.md', 'seed-format-detail.md', 'seed-guide.md', 'settings-gui-guide.md', 'setup-host-detail.md', 'status-guide.md', 'synapse-detail.md', 'update-detail.md', 'version-guide.md', 'windows-wsl-detail.md', 'workflow-ir-detail.md', 'workflows-detail.md'],
    'en': ['en/ai-troubleshooting.md', 'en/quickstart.md', 'en/settings-gui-guide.md', 'en/troubleshooting.md'],
    'zh-Hans': ['zh/quickstart.md', 'zh/troubleshooting.md'],
}

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

manifest = json.loads((ROOT / 'docs-src/content-manifest.json').read_text(encoding='utf-8'))
listed = [name for names in LANGUAGE_PAGES.values() for name in names]
if len(listed) != len(set(listed)) or not set(listed).issubset(manifest['pages']):
    raise SystemExit('Reviewed search-language pages no longer match the manifest')
routes = {}
for language, names in LANGUAGE_PAGES.items():
    for name in names:
        path = '/docs/' if name == 'index.md' else '/docs/' + name.removesuffix('.md') + '/'
        routes[path] = language
(ROOT / 'site/docs/search/languages.json').write_text(
    json.dumps(routes, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n', encoding='utf-8')
print('Wrote explicit search result language map.')

# Stable partition only already-matched page groups, before Material truncates
# the first rendered chunk. No score changes, filtering or query aliases here.
patch = '''
;(()=>{const send=self.postMessage.bind(self);
const locale=new URL(self.location.href).searchParams.get('ouro_locale');
const routes=ROUTES;
self.postMessage=function(message,...rest){
 if(message && message.type===3 && message.data && Array.isArray(message.data.items) && ['ko','en','zh-Hans'].includes(locale)){
  const items=message.data.items;
  const same=group=>Array.isArray(group)&&group.some(item=>{
   if(!item || typeof item.location!=='string')return false;
   const path='/docs/'+item.location.split('#')[0];
   return routes[path]===locale;
  });
  message={...message,data:{...message.data,items:items.filter(same).concat(items.filter(group=>!same(group)))}};
 }
 return send(message,...rest);
};})();
'''.replace('ROUTES',json.dumps(routes,ensure_ascii=False))
workers=list((ROOT/'site/docs/assets/javascripts/workers').glob('search.*.min.js'))
if len(workers)!=1: raise SystemExit('Expected one pinned Material search worker')
worker=workers[0]
marker='\n/* ouro-locale-order-v1 */\n'
original_bytes=worker.read_bytes().split(marker.encode())[0]
original=original_bytes.decode('utf-8')
# Exact upstream bytes pin both matching and the 0/1 init, 2/3 query protocol.
# An upgrade must be explicitly reviewed; never publish an unrecognized patch.
if worker.name != 'search.2c215733.min.js' or hashlib.sha256(original_bytes).hexdigest() != 'cfb35333fafd6d2eb148eba21452849fb7fbde32fdfbf986836573f963106188':
    raise SystemExit('Unsupported Material search worker bytes/protocol; build blocked')
worker.write_text(original+marker+patch,encoding='utf-8')
