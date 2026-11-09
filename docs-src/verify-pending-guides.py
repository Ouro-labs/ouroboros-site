#!/usr/bin/env python3
"""Validate a pending extension without opening the publication gate."""
import copy
import hashlib
import json
import re
from pathlib import Path
from link_evidence import load, validate, verify_content_tree

ROOT = Path(__file__).resolve().parent
NAMES = {'megacode-guide.md', 'settings-gui-guide.md', 'en/settings-gui-guide.md',
         'model-routing-guide.md', 'harness-traces-guide.md', 'dashboard-guide.md'}
BASE = 'ce90835b5bc460c172c1b85c1101ec037a0471763cfb8aeeea5fc48a7a56adf2'

PUBLIC_INDEX_SCOPE_ADDITION = b"That historical scope applies to the original `/learn/` guides, not to every page under `/docs/`. The first-task quickstarts and AI troubleshooting manual identify their own product-source and release boundaries, including main `592c667f` and release `0.59.9`. Follow the source revision stated on the page you read; do not apply historical `722172ef` detail-page behavior to a current-source instruction without comparison. The canonical repository's legacy `content/llms.txt` uses a different set of relative paths and is not this public index.\n\n"

PUBLIC_INDEX_SCOPE_BEFORE = b'The English and Korean guides identify Ouroboros 0.51.5 and upstream d103058fe as their reference. Installed CLI packages, host plugins, and MCP servers can have different versions. Check the installed version and the product repository\'s current installation and command documentation before applying instructions.\n\n'
PUBLIC_INDEX_SCOPE_AFTER = b'- Getting started and installation: https://github.com/Q00/ouroboros/blob/main/docs/getting-started.md\n'

def restore_public_index_prior(data):
    # Pending-only exact additive delta; historical evidence remains unchanged.
    bound=PUBLIC_INDEX_SCOPE_BEFORE+PUBLIC_INDEX_SCOPE_ADDITION+PUBLIC_INDEX_SCOPE_AFTER
    if data.count(PUBLIC_INDEX_SCOPE_ADDITION) != 1 or data.count(bound) != 1:
        raise ValueError("AI manual file changed: site/llms.txt (pending scope delta)")
    return data.replace(bound,PUBLIC_INDEX_SCOPE_BEFORE+PUBLIC_INDEX_SCOPE_AFTER,1)

def sha(data): return hashlib.sha256(data).hexdigest()
def verify_pending_gate(manifest, pending):
    if manifest.get('semantic_links_reviewed') is not False or pending.get('status') != 'pending':
        raise ValueError('Pending extension requires closed gate')

SEARCH_HEADER_CSS_BLOCK = b'''\n/* Keep Material's desktop search overlay anchored to the header's search slot. */
@media screen and (min-width: 60em) {
  .ouro-top-inner > .md-search {
    flex: 0 0 11.7rem;
    width: 11.7rem;
    min-width: 0;
  }
}

@media screen and (min-width: 60em) and (max-width: 76.234375em) {
  .ouro-top-inner {
    height: auto;
    min-height: 64px;
    padding-block: 8px;
    gap: 12px;
  }
  .ouro-top-inner > .ouro-brand {
    flex-shrink: 0;
  }
  .ouro-top-inner > .ouro-nav {
    flex: 1 1 0;
    min-width: 0;
    margin-inline: 0;
    flex-wrap: wrap;
    gap: 8px 12px;
  }
}
'''
SEARCH_HEADER_TEST_CONSTANTS = b'''\nDESKTOP_SEARCH_SLOT_RULE = \'''@media screen and (min-width: 60em) {
  .ouro-top-inner > .md-search {
    flex: 0 0 11.7rem;
    width: 11.7rem;
    min-width: 0;
  }
}\'''
COMPACT_DESKTOP_HEADER_RULE = \'''@media screen and (min-width: 60em) and (max-width: 76.234375em) {
  .ouro-top-inner {
    height: auto;
    min-height: 64px;
    padding-block: 8px;
    gap: 12px;
  }
  .ouro-top-inner > .ouro-brand {
    flex-shrink: 0;
  }
  .ouro-top-inner > .ouro-nav {
    flex: 1 1 0;
    min-width: 0;
    margin-inline: 0;
    flex-wrap: wrap;
    gap: 8px 12px;
  }
}\'''\n'''
SEARCH_HEADER_TEST_METHODS = b'''\n    def test_desktop_search_uses_fixed_header_slot_once(self):
        self.assertEqual(CSS.read_text().count(DESKTOP_SEARCH_SLOT_RULE), 1)

    def test_compact_desktop_header_rule_is_present_once(self):
        self.assertEqual(CSS.read_text().count(COMPACT_DESKTOP_HEADER_RULE), 1)
'''
SEARCH_HEADER_TEST_ANCHOR = b"RULE = '[data-md-toggle=\"search\"]:not(:checked) ~ .md-header .md-search__overlay { pointer-events: none; }'\n"
SEARCH_HEADER_BASE_METHOD = b"    def test_closed_only_rule_is_present_once(self):\n        self.assertEqual(CSS.read_text().count(RULE), 1)\n"

SEARCH_DRAWER_CURRENT = b'''(function(){
  var toggle=document.getElementById('__drawer');
  var button=document.querySelector('.ouro-drawer');
  var sidebar=document.querySelector('.md-sidebar--primary');
  var searchToggle=document.getElementById('__search');
  var search=document.querySelector('[data-md-component="search"]');
  if(!toggle || !button || !sidebar) return;
  sidebar.id='ouro-navigation';
  var mobile=window.matchMedia('(max-width: 76.2344em)');
  function syncDrawer(){
    var open=toggle.checked && mobile.matches;
    sidebar.inert=mobile.matches && !open;
    button.setAttribute('aria-expanded',String(open));
    button.setAttribute('aria-label',open ? button.dataset.labelClose : button.dataset.labelOpen);
  }
  button.addEventListener('click',function(){toggle.click();syncDrawer();});
  toggle.addEventListener('change',syncDrawer);
  mobile.addEventListener('change',syncDrawer);
  document.addEventListener('keydown',function(event){
    if(event.key==='Escape' && !event.defaultPrevented && !event.isComposing && event.keyCode!==229 && toggle.checked && mobile.matches){
      if(search && search.contains(event.target)) return;
      toggle.click();syncDrawer();button.focus();
    }
  });
  syncDrawer();
})();'''
SEARCH_DRAWER_PRIOR = b'''(function(){
  var toggle=document.getElementById('__drawer');
  var button=document.querySelector('.ouro-drawer');
  var sidebar=document.querySelector('.md-sidebar--primary');
  if(!toggle || !button || !sidebar) return;
  sidebar.id='ouro-navigation';
  var mobile=window.matchMedia('(max-width: 76.2344em)');
  function syncDrawer(){
    var open=toggle.checked && mobile.matches;
    sidebar.inert=mobile.matches && !open;
    button.setAttribute('aria-expanded',String(open));
    button.setAttribute('aria-label',open ? button.dataset.labelClose : button.dataset.labelOpen);
  }
  button.addEventListener('click',function(){toggle.click();syncDrawer();});
  toggle.addEventListener('change',syncDrawer);
  mobile.addEventListener('change',syncDrawer);
  document.addEventListener('keydown',function(event){
    if(event.key==='Escape' && toggle.checked && mobile.matches){
      toggle.click();syncDrawer();button.focus();
    }
  });
  syncDrawer();
})();'''

def verify_search_header(root, overlay):
    def reject_symlink_ancestors(path, boundary):
        path=Path(path).absolute(); boundary=Path(boundary).absolute()
        try: relative=path.relative_to(boundary)
        except ValueError: raise ValueError('Search header path escaped allowed root')
        current=boundary
        if current.is_symlink(): raise ValueError('Search header path has symlink ancestor: '+str(current))
        for part in relative.parts:
            current=current/part
            if current.is_symlink(): raise ValueError('Search header path has symlink ancestor: '+str(current))
    for name in ('pending-search-header.json','pending-search-header-review.md',
                 'pending-search-overlay.json','pending-search-overlay-review.md'):
        path=root/name
        reject_symlink_ancestors(path,root)
        if path.is_symlink() or not path.is_file():
            raise ValueError('Evidence input is not a regular non-symlink file: '+name)
    header = json.loads((root/'pending-search-header.json').read_text())
    if header.get('status') != 'pending': raise ValueError('Search header status changed')
    current_names={'docs-src/content/assets/site.css','docs-src/tests/test_search_overlay.py'}
    if set(header.get('files',{})) != current_names: raise ValueError('Search header file set changed')
    overlay_json=(root/'pending-search-overlay.json').read_bytes()
    overlay_summary_path=(root/'pending-search-overlay-review.md').read_bytes()
    if sha(overlay_json)!=header.get('overlay_record_sha256'): raise ValueError('Search header overlay record changed')
    if sha(overlay_summary_path)!=header.get('overlay_summary_sha256'): raise ValueError('Search header overlay summary changed')
    summary=(root/'pending-search-header-review.md').read_bytes()
    if sha(summary)!=header.get('summary_sha256'): raise ValueError('Search header summary changed')
    decoded=summary.decode('utf-8')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \|$',decoded,re.MULTILINE)
    expected={**header['files'],
              'docs-src/pending-search-overlay.json':header['overlay_record_sha256'],
              'docs-src/pending-search-overlay-review.md':header['overlay_summary_sha256']}
    if len(rows)!=len(expected) or dict(rows)!=expected: raise ValueError('Search header summary rows mismatch')
    if 'does not approve semantic review or publication' not in decoded:
        raise ValueError('Search header summary approval boundary missing')

    css_path=root.parent/'docs-src/content/assets/site.css'
    test_path=root.parent/'docs-src/tests/test_search_overlay.py'
    reject_symlink_ancestors(css_path,root.parent)
    reject_symlink_ancestors(test_path,root.parent)
    if css_path.is_symlink() or not css_path.is_file(): raise ValueError('Search header CSS is not a regular file')
    if test_path.is_symlink() or not test_path.is_file(): raise ValueError('Search header test is not a regular file')
    css=css_path.read_bytes(); test=test_path.read_bytes()
    if sha(css)!=header['files']['docs-src/content/assets/site.css']:
        raise ValueError('Search header CSS changed')
    if sha(test)!=header['files']['docs-src/tests/test_search_overlay.py']:
        raise ValueError('Search header test changed')

    anchor=b'[data-ouro-result-language]{display:inline-block;margin-inline-start:.5em;padding:.1em .4em;border:1px solid currentColor;border-radius:.4em;font-size:.7em;font-weight:600;vertical-align:middle}\n'
    if css.count(SEARCH_HEADER_CSS_BLOCK)!=1 or css.count(anchor)!=1 or css.index(SEARCH_HEADER_CSS_BLOCK)!=css.index(anchor)+len(anchor):
        raise ValueError('Search header CSS block missing, duplicated, or moved')
    prior_css=css.replace(SEARCH_HEADER_CSS_BLOCK,b'',1)
    css_name='docs-src/content/assets/site.css'
    if sha(prior_css)!=overlay['files'][css_name]: raise ValueError('Search overlay prior CSS bytes changed')

    if test.count(SEARCH_HEADER_TEST_CONSTANTS)!=1 or test.count(SEARCH_HEADER_TEST_METHODS)!=1:
        raise ValueError('Search header test additions missing, duplicated, or moved')
    if test.count(SEARCH_HEADER_TEST_ANCHOR)!=1 or test.count(SEARCH_HEADER_BASE_METHOD)!=1:
        raise ValueError('Search header test insertion anchor missing or duplicated')
    if test.index(SEARCH_HEADER_TEST_CONSTANTS)!=test.index(SEARCH_HEADER_TEST_ANCHOR)+len(SEARCH_HEADER_TEST_ANCHOR)-1:
        raise ValueError('Search header test constants moved')
    if test.index(SEARCH_HEADER_TEST_METHODS)!=test.index(SEARCH_HEADER_BASE_METHOD)+len(SEARCH_HEADER_BASE_METHOD):
        raise ValueError('Search header test methods moved')
    prior_test=test.replace(SEARCH_HEADER_TEST_CONSTANTS,b'\n',1).replace(SEARCH_HEADER_TEST_METHODS,b'',1)
    reinserted=prior_test.replace(SEARCH_HEADER_TEST_ANCHOR,SEARCH_HEADER_TEST_ANCHOR[:-1]+SEARCH_HEADER_TEST_CONSTANTS,1)
    reinserted=reinserted.replace(SEARCH_HEADER_BASE_METHOD,SEARCH_HEADER_BASE_METHOD+SEARCH_HEADER_TEST_METHODS,1)
    if reinserted!=test:
        raise ValueError('Search header test round trip changed')
    test_name='docs-src/tests/test_search_overlay.py'
    if sha(prior_test)!=overlay['files'][test_name]: raise ValueError('Search overlay prior test bytes changed')
    return header, prior_css, prior_test

def restore_search_javascript(data, expected_prior_hash):
    marker=b"(function(){\n  var toggle=document.getElementById('__drawer');"
    starts=[m.start() for m in re.finditer(re.escape(marker),data)]
    if len(starts)!=1: raise ValueError('Search drawer block missing or duplicated')
    start=starts[0]; end=data.find(b"\n\n// Material's search listens",start)
    if end<0: raise ValueError('Search drawer block boundary missing')
    current=data[start:end]
    if current != SEARCH_DRAWER_CURRENT:
        raise ValueError('Search drawer block changed or moved')
    restored=data[:start]+SEARCH_DRAWER_PRIOR+data[end:]
    starts=[m.start() for m in re.finditer(re.escape(b'// Search keyboard operation and Escape focus restoration.'),restored)]
    if len(starts)!=1: raise ValueError('Search Escape block missing or duplicated')
    s=starts[0]; e=restored.find(b'// Annotate only reviewed result URLs.',s)
    if e<0: raise ValueError('Search Escape block boundary missing')
    old_search=b"// The Material search opener is a label; make it operable from the keyboard.\n(function(){\n  var opener=document.querySelector('[data-ouro-search-open]');\n  if(!opener) return;\n  opener.addEventListener('keydown',function(event){\n    if(event.key==='Enter' || event.key===' '){event.preventDefault();opener.click();}\n  });\n})();\n\n"
    restored=restored[:s]+old_search+restored[e:]
    if sha(restored)!=expected_prior_hash: raise ValueError('Search file changed: content/assets/ouro-theme.js')
    return restored

def restore_doctor_scope_fixture(root):
    path=root/'pending-doctor-scope.json'
    if path.is_symlink() or not path.is_file(): raise ValueError('Doctor scope evidence unsafe')
    if sha(path.read_bytes())!='aa6fa3bb66218c1402ecf19096ef61438c942903a0f25232efa2f3033d4471ec': raise ValueError('Doctor scope evidence changed')
    delta=json.loads(path.read_text())
    expected={'content/ai-troubleshooting.md', 'content-manifest.json', 'content/en/ai-troubleshooting.md'}
    if delta.get('status')!='pending' or set(delta.get('files',{}))!=expected: raise ValueError('Doctor scope shape')
    for name,item in delta['files'].items():
        target=root/name
        if target.is_symlink() or any(p.is_symlink() for p in target.parents): raise ValueError('Doctor scope path unsafe')
        if not target.is_file() or target.read_bytes()!=item['current'].encode(): raise ValueError('Doctor scope current bytes')
    if json.loads((root/'content-manifest.json').read_text()).get('semantic_links_reviewed') is not False:
        raise ValueError('Doctor scope requires closed gate')
    for name,item in delta['files'].items(): (root/name).write_text(item['prior'])
    path.unlink()

def restore_quickstart_target_fixture(root):
    if (root/'pending-doctor-scope.json').exists(): restore_doctor_scope_fixture(root)
    path=root/'pending-quickstart-target.json'
    if path.is_symlink() or not path.is_file(): raise ValueError('Quickstart target evidence unsafe')
    if sha(path.read_bytes())!='1ac9833d90b09192a9e824755b8b911eebd0f0c8cba60e5c802d7df1fe99561a': raise ValueError('Quickstart target evidence changed')
    delta=json.loads(path.read_text())
    expected={'content/zh/quickstart.md', 'content-manifest.json', 'content/en/quickstart.md', 'content/quickstart.md'}
    if delta.get('status')!='pending' or set(delta.get('files',{}))!=expected: raise ValueError('Quickstart target shape')
    for name,item in delta['files'].items():
        target=root/name
        if target.is_symlink() or any(p.is_symlink() for p in target.parents): raise ValueError('Quickstart target path unsafe')
        if not target.is_file() or target.read_bytes()!=item['current'].encode(): raise ValueError('Quickstart target current bytes')
    if json.loads((root/'content-manifest.json').read_text()).get('semantic_links_reviewed') is not False:
        raise ValueError('Quickstart target requires closed gate')
    for name,item in delta['files'].items(): (root/name).write_text(item['prior'])
    path.unlink()

def restore_recovery_translation_fixture(root):
    if (root/'pending-quickstart-target.json').exists(): restore_quickstart_target_fixture(root)
    path=root/'pending-recovery-translation.json'
    if path.is_symlink() or not path.is_file(): raise ValueError('Recovery translation evidence unsafe')
    if sha(path.read_bytes())!='8f7bbebd3f9fbf5520e30679b5f5407d881e7a4b81e1aa8be8dead4c325f7c3d': raise ValueError('Recovery translation evidence changed')
    delta=json.loads(path.read_text())
    expected={'content/en/troubleshooting.md','content/zh/troubleshooting.md','content-manifest.json'}
    if delta.get('status')!='pending' or set(delta.get('files',{}))!=expected: raise ValueError('Recovery translation shape')
    for name,item in delta['files'].items():
        target=root/name
        if target.is_symlink() or any(p.is_symlink() for p in target.parents): raise ValueError('Recovery translation path unsafe')
        if not target.is_file() or target.read_bytes()!=item['current'].encode(): raise ValueError('Recovery translation current bytes')
    if json.loads((root/'content-manifest.json').read_text()).get('semantic_links_reviewed') is not False:
        raise ValueError('Recovery translation requires closed gate')
    for name,item in delta['files'].items(): (root/name).write_text(item['prior'])
    path.unlink()

def restore_interface_entry_fixture(root):
    if (root/'pending-recovery-translation.json').exists(): restore_recovery_translation_fixture(root)
    path=root/'pending-interface-entry.json'
    if path.is_symlink() or not path.is_file(): raise ValueError('Interface entry evidence unsafe')
    if sha(path.read_bytes())!='ec21c761e3fe1c905d17f31d62a3b9ea819a3f99a6618893f2283baf21eb0804': raise ValueError('Interface entry evidence changed')
    delta=json.loads(path.read_text())
    expected={'content/cli-reference-detail.md','content/mcp-reference-detail.md','content/config-reference-guide.md','content-manifest.json'}
    if delta.get('status')!='pending' or set(delta.get('files',{}))!=expected: raise ValueError('Interface entry shape')
    for name,item in delta['files'].items():
        target=root/name
        if target.is_symlink() or any(p.is_symlink() for p in target.parents): raise ValueError('Interface entry path unsafe')
        if not target.is_file() or target.read_bytes()!=item['current'].encode(): raise ValueError('Interface entry current bytes')
    if json.loads((root/'content-manifest.json').read_text()).get('semantic_links_reviewed') is not False:
        raise ValueError('Interface entry requires closed gate')
    for name,item in delta['files'].items(): (root/name).write_text(item['prior'])
    path.unlink()

def restore_todo_language_fixture(root):
    if (root/'pending-interface-entry.json').exists(): restore_interface_entry_fixture(root)
    path=root/'pending-todo-language.json'
    if path.is_symlink() or not path.is_file(): raise ValueError('Todo language evidence unsafe')
    if sha(path.read_bytes())!='0227e7f2a5d1e3280f718a95d23e05df8ae78fad23a3546607edf8e64bfd5288': raise ValueError('Todo language evidence changed')
    delta=json.loads(path.read_text())
    if delta.get('status')!='pending' or set(delta.get('files',{}))!={'augment-search.py'}:
        raise ValueError('Todo language pending shape')
    target=root/'augment-search.py';item=delta['files']['augment-search.py']
    if target.is_symlink() or any(p.is_symlink() for p in target.parents): raise ValueError('Todo language path unsafe')
    if not target.is_file() or target.read_bytes()!=item['current'].encode(): raise ValueError('Todo language current bytes')
    if json.loads((root/'content-manifest.json').read_text()).get('semantic_links_reviewed') is not False:
        raise ValueError('Todo language requires closed gate')
    target.write_text(item['prior'])
    path.unlink()

def restore_auto_status_fixture(root):
    if (root/'pending-todo-language.json').exists(): restore_todo_language_fixture(root)
    path=root/'pending-auto-status.json'
    if path.is_symlink() or not path.is_file(): raise ValueError('Auto status evidence unsafe')
    if sha(path.read_bytes())!='b55c3a440236ac77a470cdb178a1731e16df2bab7c73c6fcb287df5dd6b3411d': raise ValueError('Auto status evidence changed')
    delta=json.loads(path.read_text())
    if delta.get('status')!='pending' or set(delta.get('files',{}))!={'content/auto-detail.md','content-manifest.json'}:
        raise ValueError('Auto status pending shape')
    for name,item in delta['files'].items():
        target=root/name
        if target.is_symlink() or any(p.is_symlink() for p in target.parents): raise ValueError('Auto status path unsafe')
        if not target.is_file() or target.read_bytes()!=item['current'].encode(): raise ValueError('Auto status current bytes')
    manifest=json.loads((root/'content-manifest.json').read_text())
    if manifest.get('semantic_links_reviewed') is not False: raise ValueError('Auto status requires closed gate')
    for name,item in delta['files'].items(): (root/name).write_text(item['prior'])
    path.unlink()

def restore_cancel_warning_fixture(root):
    if (root/'pending-auto-status.json').exists(): restore_auto_status_fixture(root)
    path=root/'pending-cancel-warning.json'
    if path.is_symlink() or not path.is_file(): raise ValueError('Cancel warning evidence unsafe')
    if sha(path.read_bytes())!='8dbedf717696405d051cebd74a7d8278c2dd9c3692140e7f23a9e3325f6d532a': raise ValueError('Cancel warning evidence changed')
    delta=json.loads(path.read_text())
    if delta.get('status')!='pending' or set(delta.get('files',{}))!={'content/cli-reference-detail.md','content-manifest.json'}:
        raise ValueError('Cancel warning pending shape')
    for name,item in delta['files'].items():
        target=root/name
        if target.is_symlink() or any(p.is_symlink() for p in target.parents): raise ValueError('Cancel warning path unsafe')
        if not target.is_file() or target.read_bytes()!=item['current'].encode(): raise ValueError('Cancel warning current bytes')
    manifest=json.loads((root/'content-manifest.json').read_text())
    if manifest.get('semantic_links_reviewed') is not False: raise ValueError('Cancel warning requires closed gate')
    for name,item in delta['files'].items(): (root/name).write_text(item['prior'])
    path.unlink()

def restore_install_title_fixture(root):
    if (root/'pending-cancel-warning.json').exists(): restore_cancel_warning_fixture(root)
    path=root/'pending-install-title.json'
    if path.is_symlink() or not path.is_file(): raise ValueError('Install title evidence unsafe')
    if sha(path.read_bytes())!='9668ba6a72610e46edc9b16f8f91c09856da35c64634b66ff392ff081c5b91a9': raise ValueError('Install title evidence changed')
    delta=json.loads(path.read_text())
    if delta.get('status')!='pending' or set(delta.get('files',{}))!={'content/quickstart.md','content-manifest.json'}:
        raise ValueError('Install title pending shape')
    for name,item in delta['files'].items():
        target=root/name
        if target.is_symlink() or any(p.is_symlink() for p in target.parents): raise ValueError('Install title path unsafe')
        if not target.is_file() or target.read_bytes()!=item['current'].encode(): raise ValueError('Install title current bytes')
    manifest=json.loads((root/'content-manifest.json').read_text())
    if manifest.get('semantic_links_reviewed') is not False: raise ValueError('Install title requires closed gate')
    for name,item in delta['files'].items(): (root/name).write_text(item['prior'])
    path.unlink()

def restore_search_locale_fixture(root):
    if (root/'pending-install-title.json').exists(): restore_install_title_fixture(root)
    record_path=root/'pending-search-locale.json'
    if record_path.is_symlink() or not record_path.is_file(): raise ValueError('Search locale evidence unsafe')
    if sha(record_path.read_bytes())!='810076c353de29b0b88e349d28cbcd46341ccc82b0792f617ccf790245cb4c7e': raise ValueError('Search locale evidence changed')
    record=json.loads(record_path.read_text())
    if record.get('status')!='pending': raise ValueError('Search locale status')
    for name,item in record['files'].items():
        path=root/name
        if path.is_symlink() or any(p.is_symlink() for p in path.parents if p!=root.parent):
            raise ValueError('Search locale path unsafe')
        if not path.is_file() or path.read_bytes()!=item['current'].encode(): raise ValueError('Search locale current bytes')
    for name,item in record['files'].items():
        path=root/name
        if item['prior'] is None: path.unlink()
        else: path.write_text(item['prior'])
    record_path.unlink()

def verify_uninstall_delta(root):
    import tempfile, shutil
    for entry in (root,root/'content',root/'content-manifest.json'):
        if entry.is_symlink(): raise ValueError('Uninstall delta unsafe ancestor')
    path=root/'pending-uninstall-warning.json'
    if path.is_symlink() or not path.is_file(): raise ValueError('Uninstall delta unsafe')
    if sha(path.read_bytes()) != 'ff5578fd1f662369d4934fca00626999aa72fbfa13b3dbf9819359864dee0640': raise ValueError('Uninstall delta evidence changed')
    delta=json.loads(path.read_text())
    manifest=json.loads((root/'content-manifest.json').read_text())
    if delta.get('status')!='pending' or manifest.get('semantic_links_reviewed') is not False:
        raise ValueError('Pending extension requires closed gate')
    if set(delta.get('pages',{}))!={'operations-detail.md','cli-reference-detail.md'}:
        raise ValueError('Uninstall delta page set')
    if sha((root/'content-manifest.json').read_bytes())!=delta['manifest_sha256']:
        return False # Historical tamper fixtures still run their unchanged boundaries.
    prior=copy.deepcopy(manifest)
    for name,item in delta['pages'].items():
        page=root/'content'/name
        if page.is_symlink() or not page.is_file() or page.read_bytes()!=item['current_text'].encode():
            raise ValueError('Uninstall delta current bytes')
        if manifest['pages'][name]!=item['current'] or sha(page.read_bytes())!=item['current']['page_sha256']:
            raise ValueError('Uninstall delta current metadata')
        if sha(item['prior_text'].encode())!=item['prior']['page_sha256']:
            raise ValueError('Uninstall delta prior bytes')
        prior['pages'][name]=item['prior']
    prior_bytes=(json.dumps(prior,ensure_ascii=False,indent=2)+'\n').encode()
    if sha(prior_bytes)!=delta['prior_manifest_sha256'] or delta['prior_manifest_sha256']!='258487737d17401dea71952f2ed4a1da13612becf922b5fa50db0f4c4b16cddb':
        raise ValueError('Uninstall delta prior chain')
    with tempfile.TemporaryDirectory() as tmp:
        restored=Path(tmp)/'docs-src'
        shutil.copytree(root,restored,symlinks=True,ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copytree(root.parent/'site',restored.parent/'site',symlinks=True,ignore=shutil.ignore_patterns('docs'))
        (restored/'content-manifest.json').write_bytes(prior_bytes)
        for name,item in delta['pages'].items(): (restored/'content'/name).write_text(item['prior_text'])
        verify(restored,_uninstall=False)
    return True

def verify(root=ROOT, _uninstall=True):
    if (root/'pending-doctor-scope.json').exists():
        import tempfile, shutil
        with tempfile.TemporaryDirectory() as tmp:
            prior=Path(tmp)/'docs-src'
            shutil.copytree(root,prior,symlinks=True,ignore=shutil.ignore_patterns('__pycache__'))
            shutil.copytree(root.parent/'site',prior.parent/'site',symlinks=True,ignore=shutil.ignore_patterns('docs'))
            restore_doctor_scope_fixture(prior)
            verify(prior,_uninstall=_uninstall)
        return
    if (root/'pending-quickstart-target.json').exists():
        import tempfile, shutil
        with tempfile.TemporaryDirectory() as tmp:
            prior=Path(tmp)/'docs-src'
            shutil.copytree(root,prior,symlinks=True,ignore=shutil.ignore_patterns('__pycache__'))
            shutil.copytree(root.parent/'site',prior.parent/'site',symlinks=True,ignore=shutil.ignore_patterns('docs'))
            restore_quickstart_target_fixture(prior)
            verify(prior,_uninstall=_uninstall)
        return
    if (root/'pending-recovery-translation.json').exists():
        import tempfile, shutil
        with tempfile.TemporaryDirectory() as tmp:
            prior=Path(tmp)/'docs-src'
            shutil.copytree(root,prior,symlinks=True,ignore=shutil.ignore_patterns('__pycache__'))
            shutil.copytree(root.parent/'site',prior.parent/'site',symlinks=True,ignore=shutil.ignore_patterns('docs'))
            restore_recovery_translation_fixture(prior)
            verify(prior,_uninstall=_uninstall)
        return
    if (root/'pending-interface-entry.json').exists():
        import tempfile, shutil
        with tempfile.TemporaryDirectory() as tmp:
            prior=Path(tmp)/'docs-src'
            shutil.copytree(root,prior,symlinks=True,ignore=shutil.ignore_patterns('__pycache__'))
            shutil.copytree(root.parent/'site',prior.parent/'site',symlinks=True,ignore=shutil.ignore_patterns('docs'))
            restore_interface_entry_fixture(prior)
            verify(prior,_uninstall=_uninstall)
        return
    if (root/'pending-todo-language.json').exists():
        import tempfile, shutil
        with tempfile.TemporaryDirectory() as tmp:
            prior=Path(tmp)/'docs-src'
            shutil.copytree(root,prior,symlinks=True,ignore=shutil.ignore_patterns('__pycache__'))
            shutil.copytree(root.parent/'site',prior.parent/'site',symlinks=True,ignore=shutil.ignore_patterns('docs'))
            restore_todo_language_fixture(prior)
            verify(prior,_uninstall=_uninstall)
        return
    if (root/'pending-auto-status.json').exists():
        import tempfile, shutil
        with tempfile.TemporaryDirectory() as tmp:
            prior=Path(tmp)/'docs-src'
            shutil.copytree(root,prior,symlinks=True,ignore=shutil.ignore_patterns('__pycache__'))
            shutil.copytree(root.parent/'site',prior.parent/'site',symlinks=True,ignore=shutil.ignore_patterns('docs'))
            restore_auto_status_fixture(prior)
            verify(prior,_uninstall=_uninstall)
        return
    if (root/'pending-cancel-warning.json').exists():
        import tempfile, shutil
        with tempfile.TemporaryDirectory() as tmp:
            prior=Path(tmp)/'docs-src'
            shutil.copytree(root,prior,symlinks=True,ignore=shutil.ignore_patterns('__pycache__'))
            shutil.copytree(root.parent/'site',prior.parent/'site',symlinks=True,ignore=shutil.ignore_patterns('docs'))
            restore_cancel_warning_fixture(prior)
            verify(prior,_uninstall=_uninstall)
        return
    if (root/'pending-install-title.json').exists():
        import tempfile, shutil
        with tempfile.TemporaryDirectory() as tmp:
            prior=Path(tmp)/'docs-src'
            shutil.copytree(root,prior,symlinks=True,ignore=shutil.ignore_patterns('__pycache__'))
            shutil.copytree(root.parent/'site',prior.parent/'site',symlinks=True,ignore=shutil.ignore_patterns('docs'))
            restore_install_title_fixture(prior)
            verify(prior,_uninstall=_uninstall)
        return
    if (root/'pending-search-locale.json').exists():
        import tempfile, shutil
        with tempfile.TemporaryDirectory() as tmp:
            prior=Path(tmp)/'docs-src'
            shutil.copytree(root,prior,symlinks=True,ignore=shutil.ignore_patterns('__pycache__'))
            shutil.copytree(root.parent/'site',prior.parent/'site',symlinks=True,ignore=shutil.ignore_patterns('docs'))
            restore_search_locale_fixture(prior)
            verify(prior,_uninstall=_uninstall)
        return
    if _uninstall and (root/'pending-uninstall-warning.json').is_file() and verify_uninstall_delta(root): return
    for name in ('content-manifest.json', 'link-review-evidence.json', 'pending-new-guides.json', 'pending-new-guides-review.md', 'pending-journey.json', 'pending-journey-review.md', 'pending-latest.json', 'pending-latest-review.md', 'pending-install.json', 'pending-install-review.md', 'pending-locale.json', 'pending-locale-review.md', 'pending-search.json', 'pending-search-review.md', 'pending-worktree.json', 'pending-worktree-review.md', 'pending-discovery.json', 'pending-discovery-review.md', 'pending-evaluation.json', 'pending-evaluation-review.md', 'pending-accessibility.json', 'pending-accessibility-review.md', 'pending-details.json', 'pending-details-review.md', 'pending-permissions.json', 'pending-permissions-review.md', 'pending-job-diagnostic.json', 'pending-job-diagnostic-review.md', 'pending-package.json', 'pending-package-review.md', 'pending-seed.json', 'pending-seed-review.md', 'pending-interview.json', 'pending-interview-review.md', 'pending-seed-version.json', 'pending-seed-version-review.md', 'pending-runtime.json', 'pending-runtime-review.md', 'pending-home.json', 'pending-home-review.md', 'pending-session.json', 'pending-session-review.md', 'pending-headings.json', 'pending-headings-review.md', 'pending-example.json', 'pending-example-review.md', 'pending-interview-search.json', 'pending-interview-search-review.md', 'pending-worktree-result.json', 'pending-worktree-review-result.md', 'pending-seed-verification.json', 'pending-seed-verification-review.md', 'pending-browser-example.json', 'pending-browser-example-review.md', 'pending-initial-commit.json', 'pending-initial-commit-review.md', 'pending-sidecar.json', 'pending-sidecar-review.md', 'pending-megacode-claim.json', 'pending-megacode-claim-review.md', 'pending-ai-manual.json', 'pending-ai-manual-review.md', 'pending-ko-venv.json', 'pending-ko-venv-review.md', 'pending-recovery-navigation.json', 'pending-recovery-navigation-review.md', 'pending-translated-recovery.json', 'pending-translated-recovery-review.md', 'pending-search-focus.json', 'pending-search-focus-review.md', 'pending-preflight.json', 'pending-preflight-review.md', 'pending-worktree-input.json', 'pending-worktree-input-review.md', 'pending-landing.json', 'pending-landing-review.md', 'pending-descriptions.json', 'pending-descriptions-review.md', 'pending-seed-order.json', 'pending-seed-order-review.md', 'pending-megacode-warning.json', 'pending-megacode-warning-review.md', 'pending-trace-warning.json', 'pending-trace-warning-review.md', 'pending-venv-direct.json', 'pending-venv-direct-review.md', 'pending-diagnostics-version.json', 'pending-diagnostics-version-review.md', 'pending-diagnostics-auto-id.json', 'pending-diagnostics-auto-id-review.md', 'pending-seed-source.json', 'pending-seed-source-review.md', 'pending-zh-status.json', 'pending-zh-status-review.md', 'pending-home-readability.json', 'pending-home-readability-review.md', 'pending-setup-split.json', 'pending-setup-split-review.md', 'pending-seed-flow.json', 'pending-seed-flow-review.md', 'pending-home-source-labels.json', 'pending-home-source-labels-review.md', 'pending-windows-codex.json', 'pending-windows-codex-review.md', 'pending-worktree-warning.json', 'pending-worktree-warning-review.md', 'pending-mcp-query.json', 'pending-mcp-query-review.md', 'pending-worktree-id.json', 'pending-worktree-id-review.md', 'pending-windows-codex-cli.json', 'pending-windows-codex-cli-review.md', 'pending-check-package-result.json', 'pending-check-package-result-review.md', 'pending-concepts-detail.json', 'pending-concepts-detail-review.md', 'pending-codex-plugin.json', 'pending-codex-plugin-review.md', 'pending-codex-plugin-zh.json', 'pending-codex-plugin-zh-review.md', 'pending-en-chain-summary.json', 'pending-en-chain-summary-review.md', 'pending-ko-navigation.json', 'pending-ko-navigation-review.md', 'pending-seed-example.json', 'pending-seed-example-review.md', 'pending-host-setup.json', 'pending-host-setup-review.md', 'pending-config-qa.json', 'pending-config-qa-review.md', 'pending-cal-receipt.json', 'pending-cal-receipt-review.md', 'pending-job-wait.json', 'pending-job-wait-review.md', 'pending-chain-cancel.json', 'pending-chain-cancel-review.md', 'pending-manual-table.json', 'pending-manual-table-review.md', 'pending-quick-nav.json', 'pending-quick-nav-review.md', 'pending-quick-sequence.json', 'pending-quick-sequence-review.md', 'pending-run-preflight.json', 'pending-run-preflight-review.md', 'pending-cli-readability.json', 'pending-cli-readability-review.md', 'pending-search-shortcut.json', 'pending-search-shortcut-review.md', 'pending-ai-entry.json', 'pending-ai-entry-review.md', 'pending-event-display.json', 'pending-event-display-review.md', 'pending-search-overlay.json', 'pending-search-overlay-review.md', 'pending-search-header.json', 'pending-search-header-review.md', 'pending-quickstart-eval.json', 'pending-quickstart-eval-review.md', 'pending-job-wait-clarification.json', 'pending-job-wait-clarification-review.md', 'pending-worktree-scope.json', 'pending-worktree-scope-review.md', 'pending-mcp-visibility.json', 'pending-mcp-visibility-review.md', 'pending-en-manual-update.json', 'pending-en-manual-update-review.md', 'pending-search-escape.json', 'pending-search-escape-review.md', 'pending-codex-tui.json', 'pending-codex-tui-review.md'):
        path = root/name
        if path.is_symlink() or not path.is_file():
            raise ValueError('Evidence input is not a regular non-symlink file: '+name)
    manifest, evidence = load(root)
    pending = json.loads((root/'pending-new-guides.json').read_text())
    verify_pending_gate(manifest,pending)
    # Restore the three newly synchronized quickstarts to the exact site HEAD
    # manifest before the established pending chain is evaluated.
    codex_tui = json.loads((root/'pending-codex-tui.json').read_text())
    if codex_tui.get('status') != 'pending': raise ValueError('Codex TUI status changed')
    verify_pending_gate(manifest, codex_tui)
    tui_names = {'quickstart.md', 'en/quickstart.md', 'zh/quickstart.md'}
    if set(codex_tui.get('pages', {})) != tui_names: raise ValueError('Codex TUI page set changed')
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()) != codex_tui.get('manifest_sha256'):
        raise ValueError('Codex TUI manifest or pending status changed')
    tui_summary = (root/'pending-codex-tui-review.md').read_bytes()
    if sha(tui_summary) != codex_tui.get('summary_sha256'): raise ValueError('Codex TUI summary changed')
    tui_text = tui_summary.decode('utf-8')
    if 'does not approve semantic review or publication' not in tui_text:
        raise ValueError('Codex TUI summary approval boundary missing')
    tui_rows = re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|$', tui_text, re.MULTILINE)
    if len(tui_rows) != len(tui_names) or {row[0] for row in tui_rows} != tui_names:
        raise ValueError('Codex TUI summary rows incomplete or duplicated')
    current_manifest = copy.deepcopy(manifest)
    tui_restored = copy.deepcopy(manifest)
    for name, entry in codex_tui['pages'].items():
        if set(entry) != {'prior', 'current'} or set(entry['prior']) != {'source', 'source_sha256', 'page_sha256'} or set(entry['current']) != {'source', 'source_sha256', 'page_sha256'}:
            raise ValueError('Codex TUI page metadata shape changed: '+name)
        if tui_restored['pages'].get(name) != entry['current']:
            raise ValueError('Codex TUI current metadata mismatch: '+name)
        tui_restored['pages'][name] = entry['prior']
    for name, prior_source, prior_page, current_source, current_page in tui_rows:
        entry = codex_tui['pages'][name]
        if (prior_source, prior_page) != (entry['prior']['source_sha256'], entry['prior']['page_sha256']) or (current_source, current_page) != (entry['current']['source_sha256'], entry['current']['page_sha256']):
            raise ValueError('Codex TUI summary hash mismatch: '+name)
    if sha((json.dumps(tui_restored,ensure_ascii=False,indent=2)+'\n').encode()) != codex_tui.get('prior_manifest_sha256'):
        raise ValueError('Codex TUI snapshot chain mismatch')
    manifest = tui_restored

    # Bind the newest concepts detail page, then restore the prior manifest
    # so check-package and every older stage retain their existing checks.
    escape = json.loads((root/'pending-search-escape.json').read_text())
    if escape.get('status') != 'pending': raise ValueError('Search Escape status changed')
    names={'docs-src/content/assets/ouro-theme.js','docs-src/tests/test_search_escape.cjs'}
    if set(escape.get('files',{})) != names: raise ValueError('Search Escape file set changed')
    summary=(root/'pending-search-escape-review.md').read_bytes()
    if sha(summary)!=escape['summary_sha256']: raise ValueError('Search Escape summary changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \|$',summary.decode(),re.MULTILINE)
    if len(rows)!=len(names) or dict(rows)!=escape['files']: raise ValueError('Search Escape summary rows mismatch')
    check_package=json.loads((root/'pending-check-package-result.json').read_text())
    ko_navigation=json.loads((root/'pending-ko-navigation.json').read_text())
    if ko_navigation.get('status') != 'pending' or sha((json.dumps(tui_restored,ensure_ascii=False,indent=2)+'\n').encode()) != ko_navigation['manifest_sha256']:
        raise ValueError('KO navigation manifest or pending status changed')
    ko_navigation_summary=(root/'pending-ko-navigation-review.md').read_bytes()
    if sha(ko_navigation_summary)!=ko_navigation['summary_sha256']: raise ValueError('KO navigation summary changed')
    ko_navigation_names={'quickstart.md','existing-project-detail.md'}
    if set(ko_navigation.get('pages',{})) != ko_navigation_names: raise ValueError('KO navigation page set changed')
    ko_navigation_rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|$',ko_navigation_summary.decode('utf-8'),re.MULTILINE)
    if len(ko_navigation_rows)!=len(ko_navigation_names) or {x[0] for x in ko_navigation_rows}!=ko_navigation_names: raise ValueError('KO navigation summary rows mismatch')
    for name, prior_source, prior_page, current_source, current_page in ko_navigation_rows:
        entry=ko_navigation['pages'][name]['current']; prior=ko_navigation['pages'][name]['prior']
        if (prior_source,prior_page)!=(prior['source_sha256'],prior['page_sha256']): raise ValueError('KO navigation summary prior hash mismatch: '+name)
        if (current_source,current_page)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('KO navigation current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in ko_navigation['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=ko_navigation['prior_manifest_sha256']:
        raise ValueError('KO navigation snapshot chain mismatch')
    en_chain_summary=json.loads((root/'pending-en-chain-summary.json').read_text())
    if en_chain_summary.get('status') != 'pending' or sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()) != en_chain_summary['manifest_sha256']:
        raise ValueError('EN chain summary manifest or pending status changed')
    en_chain_summary_summary=(root/'pending-en-chain-summary-review.md').read_bytes()
    if sha(en_chain_summary_summary)!=en_chain_summary['summary_sha256']: raise ValueError('EN chain summary summary changed')
    en_chain_summary_names={'en/ai-troubleshooting.md'}
    if set(en_chain_summary.get('pages',{})) != en_chain_summary_names: raise ValueError('EN chain summary page set changed')
    en_chain_summary_rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|$',en_chain_summary_summary.decode('utf-8'),re.MULTILINE)
    if len(en_chain_summary_rows)!=len(en_chain_summary_names) or {x[0] for x in en_chain_summary_rows}!=en_chain_summary_names: raise ValueError('EN chain summary summary rows mismatch')
    for name, prior_source, prior_page, current_source, current_page in en_chain_summary_rows:
        entry=en_chain_summary['pages'][name]['current']; prior=en_chain_summary['pages'][name]['prior']
        if (prior_source,prior_page)!=(prior['source_sha256'],prior['page_sha256']): raise ValueError('EN chain summary summary prior hash mismatch: '+name)
        if (current_source,current_page)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('EN chain summary current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in en_chain_summary['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=en_chain_summary['prior_manifest_sha256']:
        raise ValueError('EN chain summary snapshot chain mismatch')
    codex_plugin_zh=json.loads((root/'pending-codex-plugin-zh.json').read_text())
    if codex_plugin_zh.get('status') != 'pending' or sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()) != codex_plugin_zh['manifest_sha256']:
        raise ValueError('Codex plugin ZH manifest or pending status changed')
    codex_plugin_zh_summary=(root/'pending-codex-plugin-zh-review.md').read_bytes()
    if sha(codex_plugin_zh_summary)!=codex_plugin_zh['summary_sha256']: raise ValueError('Codex plugin ZH summary changed')
    codex_plugin_zh_names={'zh/troubleshooting.md'}
    if set(codex_plugin_zh.get('pages',{})) != codex_plugin_zh_names: raise ValueError('Codex plugin ZH page set changed')
    codex_plugin_zh_rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|$',codex_plugin_zh_summary.decode('utf-8'),re.MULTILINE)
    if len(codex_plugin_zh_rows)!=len(codex_plugin_zh_names) or {x[0] for x in codex_plugin_zh_rows}!=codex_plugin_zh_names: raise ValueError('Codex plugin ZH summary rows mismatch')
    for name, prior_source, prior_page, current_source, current_page in codex_plugin_zh_rows:
        entry=codex_plugin_zh['pages'][name]['current']; prior=codex_plugin_zh['pages'][name]['prior']
        if (prior_source,prior_page)!=(prior['source_sha256'],prior['page_sha256']): raise ValueError('Codex plugin ZH summary prior hash mismatch: '+name)
        if (current_source,current_page)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('Codex plugin ZH current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in codex_plugin_zh['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=codex_plugin_zh['prior_manifest_sha256']:
        raise ValueError('Codex plugin ZH snapshot chain mismatch')
    codex_plugin=json.loads((root/'pending-codex-plugin.json').read_text())
    if codex_plugin.get('status') != 'pending' or sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()) != codex_plugin['manifest_sha256']:
        raise ValueError('Codex plugin manifest or pending status changed')
    codex_plugin_summary=(root/'pending-codex-plugin-review.md').read_bytes()
    if sha(codex_plugin_summary)!=codex_plugin['summary_sha256']: raise ValueError('Codex plugin summary changed')
    codex_plugin_names={'ai-troubleshooting.md','en/ai-troubleshooting.md','setup-host-detail.md'}
    if set(codex_plugin.get('pages',{})) != codex_plugin_names: raise ValueError('Codex plugin page set changed')
    codex_plugin_rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|$',codex_plugin_summary.decode('utf-8'),re.MULTILINE)
    if len(codex_plugin_rows)!=len(codex_plugin_names) or {x[0] for x in codex_plugin_rows}!=codex_plugin_names: raise ValueError('Codex plugin summary rows mismatch')
    for name, prior_source, prior_page, current_source, current_page in codex_plugin_rows:
        entry=codex_plugin['pages'][name]['current']; prior=codex_plugin['pages'][name]['prior']
        if (prior_source,prior_page)!=(prior['source_sha256'],prior['page_sha256']): raise ValueError('Codex plugin summary prior hash mismatch: '+name)
        if (current_source,current_page)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('Codex plugin current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in codex_plugin['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=codex_plugin['prior_manifest_sha256']:
        raise ValueError('Codex plugin snapshot chain mismatch')
    concepts=json.loads((root/'pending-concepts-detail.json').read_text())
    if concepts.get('status') != 'pending' or sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()) != concepts['manifest_sha256']:
        raise ValueError('Concepts detail manifest or pending status changed')
    concepts_summary=(root/'pending-concepts-detail-review.md').read_bytes()
    if sha(concepts_summary)!=concepts['summary_sha256']: raise ValueError('Concepts detail summary changed')
    concepts_names={'concepts-detail.md'}
    if set(concepts.get('pages',{})) != concepts_names: raise ValueError('Concepts detail page set changed')
    concepts_rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|$',concepts_summary.decode('utf-8'),re.MULTILINE)
    if len(concepts_rows)!=len(concepts_names) or {x[0] for x in concepts_rows}!=concepts_names: raise ValueError('Concepts detail summary rows mismatch')
    for name, prior_source, prior_page, current_source, current_page in concepts_rows:
        entry=concepts['pages'][name]['current']; prior=concepts['pages'][name]['prior']
        if (prior_source,prior_page)!=(prior['source_sha256'],prior['page_sha256']): raise ValueError('Concepts detail summary prior hash mismatch: '+name)
        if (current_source,current_page)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('Concepts detail current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in concepts['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=concepts['prior_manifest_sha256']:
        raise ValueError('Concepts detail snapshot chain mismatch')
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=check_package['manifest_sha256']:
        raise ValueError('Concepts detail does not restore check-package manifest')
    if check_package.get('status') != 'pending' or sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()) != check_package['manifest_sha256']:
        raise ValueError('Check-package result manifest or pending status changed')
    check_summary=(root/'pending-check-package-result-review.md').read_bytes()
    if sha(check_summary)!=check_package['summary_sha256']: raise ValueError('Check-package result summary changed')
    check_names={'check-package-detail.md'}
    if set(check_package.get('pages',{})) != check_names: raise ValueError('Check-package result page set changed')
    check_rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|$',check_summary.decode('utf-8'),re.MULTILINE)
    if len(check_rows)!=len(check_names) or {x[0] for x in check_rows}!=check_names: raise ValueError('Check-package result summary rows mismatch')
    for name, prior_source, prior_page, current_source, current_page in check_rows:
        entry=check_package['pages'][name]['current']; prior=check_package['pages'][name]['prior']
        if (prior_source,prior_page)!=(prior['source_sha256'],prior['page_sha256']): raise ValueError('Check-package result summary prior hash mismatch: '+name)
        if (current_source,current_page)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('Check-package result current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in check_package['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=check_package['prior_manifest_sha256']:
        raise ValueError('Check-package result snapshot chain mismatch')
    if check_package['prior_manifest_sha256'] != '3391d9fa7b7f12b397b11e313eea963e46d10c5fa9c74bffe0dfe9811b22f797':
        raise ValueError('Check-package result prior chain anchor changed')
    # Continue through the preceding scope chain after restoring its manifest.
    windows_codex_cli=json.loads((root/'pending-windows-codex-cli.json').read_text())
    if windows_codex_cli.get('status') != 'pending' or sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()) != windows_codex_cli['manifest_sha256']:
        raise ValueError('Windows Codex CLI manifest or pending status changed')
    windows_summary=(root/'pending-windows-codex-cli-review.md').read_bytes()
    if sha(windows_summary)!=windows_codex_cli['summary_sha256']: raise ValueError('Windows Codex CLI summary changed')
    windows_names={'quickstart.md','en/quickstart.md','zh/quickstart.md'}
    if set(windows_codex_cli.get('pages',{})) != windows_names: raise ValueError('Windows Codex CLI page set changed')
    windows_rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|$',windows_summary.decode('utf-8'),re.MULTILINE)
    if len(windows_rows)!=len(windows_names) or {x[0] for x in windows_rows}!=windows_names: raise ValueError('Windows Codex CLI summary rows mismatch')
    for name, prior_source, prior_page, current_source, current_page in windows_rows:
        entry=windows_codex_cli['pages'][name]['current']; prior=windows_codex_cli['pages'][name]['prior']
        if (prior_source,prior_page)!=(prior['source_sha256'],prior['page_sha256']): raise ValueError('Windows Codex CLI summary prior hash mismatch: '+name)
        if (current_source,current_page)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('Windows Codex CLI current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in windows_codex_cli['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=windows_codex_cli['prior_manifest_sha256']:
        raise ValueError('Windows Codex CLI snapshot chain mismatch')
    en_manual_update=json.loads((root/'pending-en-manual-update.json').read_text())
    if en_manual_update.get('status') != 'pending' or sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()) != en_manual_update['manifest_sha256']:
        raise ValueError('EN manual update manifest or pending status changed')
    mcp_summary=(root/'pending-en-manual-update-review.md').read_bytes()
    if sha(mcp_summary)!=en_manual_update['summary_sha256']: raise ValueError('EN manual update summary changed')
    mcp_names={'en/ai-troubleshooting.md'}
    if set(en_manual_update.get('pages',{})) != mcp_names: raise ValueError('EN manual update page set changed')
    mcp_rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|$',mcp_summary.decode('utf-8'),re.MULTILINE)
    if len(mcp_rows)!=len(mcp_names) or {x[0] for x in mcp_rows}!=mcp_names: raise ValueError('EN manual update summary rows mismatch')
    for name, prior_source, prior_page, current_source, current_page in mcp_rows:
        entry=en_manual_update['pages'][name]['current']; prior=en_manual_update['pages'][name]['prior']
        if (prior_source,prior_page)!=(prior['source_sha256'],prior['page_sha256']): raise ValueError('EN manual update summary prior hash mismatch: '+name)
        if (current_source,current_page)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('EN manual update current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in en_manual_update['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=en_manual_update['prior_manifest_sha256']:
        raise ValueError('EN manual update snapshot chain mismatch')
    mcp_visibility=json.loads((root/'pending-mcp-visibility.json').read_text())
    if mcp_visibility.get('status') != 'pending' or sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()) != mcp_visibility['manifest_sha256']:
        raise ValueError('MCP visibility manifest or pending status changed')
    mcp_summary=(root/'pending-mcp-visibility-review.md').read_bytes()
    if sha(mcp_summary)!=mcp_visibility['summary_sha256']: raise ValueError('MCP visibility summary changed')
    mcp_names={'quickstart.md','en/quickstart.md','zh/quickstart.md'}
    if set(mcp_visibility.get('pages',{})) != mcp_names: raise ValueError('MCP visibility page set changed')
    mcp_rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|$',mcp_summary.decode('utf-8'),re.MULTILINE)
    if len(mcp_rows)!=len(mcp_names) or {x[0] for x in mcp_rows}!=mcp_names: raise ValueError('MCP visibility summary rows mismatch')
    for name, prior_source, prior_page, current_source, current_page in mcp_rows:
        entry=mcp_visibility['pages'][name]['current']; prior=mcp_visibility['pages'][name]['prior']
        if (prior_source,prior_page)!=(prior['source_sha256'],prior['page_sha256']): raise ValueError('MCP visibility summary prior hash mismatch: '+name)
        if (current_source,current_page)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('MCP visibility current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in mcp_visibility['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=mcp_visibility['prior_manifest_sha256']:
        raise ValueError('MCP visibility snapshot chain mismatch')
    worktree_scope = json.loads((root/'pending-worktree-scope.json').read_text())
    if worktree_scope.get('status') != 'pending' or sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()) != worktree_scope['manifest_sha256']:
        raise ValueError('Worktree scope manifest or pending status changed')
    scope_summary=(root/'pending-worktree-scope-review.md').read_bytes()
    if sha(scope_summary)!=worktree_scope['summary_sha256']: raise ValueError('Worktree scope summary changed')
    scope_names={'quickstart.md','en/quickstart.md','zh/quickstart.md'}
    if set(worktree_scope['pages']) != scope_names: raise ValueError('Worktree scope page set changed')
    scope_rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|$',scope_summary.decode('utf-8'),re.MULTILINE)
    if len(scope_rows)!=len(scope_names) or {x[0] for x in scope_rows}!=scope_names: raise ValueError('Worktree scope summary rows mismatch')
    for name, prior_source_hash, prior_page_hash, source_hash, page_hash in scope_rows:
        entry=worktree_scope['pages'][name]['current']; prior=worktree_scope['pages'][name]['prior']
        if (prior_source_hash,prior_page_hash)!=(prior['source_sha256'],prior['page_sha256']): raise ValueError('Worktree scope summary prior hash mismatch: '+name)
        if (source_hash,page_hash)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('Worktree scope current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in worktree_scope['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=worktree_scope['prior_manifest_sha256']:
        raise ValueError('Worktree scope snapshot chain mismatch')
    wait_clarification = json.loads((root/'pending-job-wait-clarification.json').read_text())
    if wait_clarification.get('status') != 'pending' or sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()) != wait_clarification['manifest_sha256']:
        raise ValueError('Job wait clarification manifest or pending status changed')
    wait_summary=(root/'pending-job-wait-clarification-review.md').read_bytes()
    if sha(wait_summary)!=wait_clarification['summary_sha256']: raise ValueError('Job wait clarification summary changed')
    wait_names={'zh/troubleshooting.md','en/troubleshooting.md','recovery-detail.md'}
    if set(wait_clarification['pages']) != wait_names: raise ValueError('Job wait clarification page set changed')
    wait_rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|$',wait_summary.decode('utf-8'),re.MULTILINE)
    if len(wait_rows)!=len(wait_names) or {x[0] for x in wait_rows}!=wait_names: raise ValueError('Job wait clarification summary rows mismatch')
    for name, prior_source_hash, prior_page_hash, source_hash, page_hash in wait_rows:
        entry=wait_clarification['pages'][name]['current']
        prior=wait_clarification['pages'][name]['prior']
        if (prior_source_hash,prior_page_hash)!=(prior['source_sha256'],prior['page_sha256']): raise ValueError('Job wait clarification summary prior hash mismatch: '+name)
        if (source_hash,page_hash)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('Job wait clarification current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in wait_clarification['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=wait_clarification['prior_manifest_sha256']:
        raise ValueError('Job wait clarification snapshot chain mismatch')
    landing = json.loads((root/'pending-landing.json').read_text())
    if landing.get('status') != 'pending': raise ValueError('Landing pending status changed')
    landing_files={'site/index.html','docs-src/tests/test_landing_quickstarts.py'}
    if set(landing.get('files',{})) != landing_files: raise ValueError('Landing file set changed')
    summary=(root/'pending-landing-review.md').read_bytes()
    if sha(summary)!=landing['summary_sha256']: raise ValueError('Landing summary changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \|$',summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(landing_files) or dict(rows)!=landing['files']: raise ValueError('Landing summary rows mismatch')
    for name, expected in landing['files'].items():
        path=root.parent/name
        if path.is_symlink() or not path.is_file() or sha(path.read_bytes())!=expected: raise ValueError('Home file changed: '+name)
    home = json.loads((root/'pending-home.json').read_text())
    if home.get('status') != 'pending':
        raise ValueError('Home manifest or pending status changed')
    home_files={'site/index.html','docs-src/overrides/main.html','docs-src/tests/test_home_discovery.py'}
    if set(home.get('files', {})) != home_files: raise ValueError('Home file set changed')
    home_summary=(root/'pending-home-review.md').read_bytes()
    if sha(home_summary)!=home['summary_sha256']: raise ValueError('Home summary changed')
    home_rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \|$',home_summary.decode('utf-8'),re.MULTILINE)
    if len(home_rows)!=len(home_files) or dict(home_rows)!=home['files']: raise ValueError('Home summary rows mismatch')
    for name, expected in home['files'].items():
        path=root.parent/name
        if name == 'site/index.html':
            if expected != landing['prior_home_sha256']: raise ValueError('Landing prior home mismatch')
        elif path.is_symlink() or not path.is_file() or sha(path.read_bytes())!=expected: raise ValueError('Home file changed: '+name)
    if home['prior_home_sha256'] != '3f53646153e3023e81d452e751b5a65649e98e33ce9e69f7c5b89c611dbbff99': raise ValueError('Home prior homepage changed')
    manual = json.loads((root/'pending-ai-manual.json').read_text())
    if manual.get('status') != 'pending': raise ValueError('AI manual pending status changed')
    manual_files={'site/llms.txt','docs-src/tests/test_ai_manual_discovery.py'}
    if set(manual.get('files', {})) != manual_files: raise ValueError('AI manual file set changed')
    manual_summary=(root/'pending-ai-manual-review.md').read_bytes()
    if sha(manual_summary)!=manual['summary_sha256']: raise ValueError('AI manual summary changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \|$',manual_summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(manual_files) or dict(rows)!=manual['files']: raise ValueError('AI manual rows mismatch')
    for name, expected in manual['files'].items():
        path=root.parent/name
        if path.is_symlink() or not path.is_file(): raise ValueError('AI manual file changed: '+name)
        data=path.read_bytes()
        if name == 'site/llms.txt': data=restore_public_index_prior(data)
        if sha(data)!=expected: raise ValueError('AI manual file changed: '+name)
    overlay = json.loads((root/'pending-search-overlay.json').read_text())
    if overlay.get('status') != 'pending': raise ValueError('Search overlay status changed')
    names={'docs-src/content/assets/site.css','docs-src/tests/test_search_overlay.py'}
    if set(overlay.get('files',{})) != names: raise ValueError('Search overlay file set changed')
    summary=(root/'pending-search-overlay-review.md').read_bytes()
    if sha(summary)!=overlay['summary_sha256']: raise ValueError('Search overlay summary changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \|$',summary.decode(),re.MULTILINE)
    if len(rows)!=len(names) or dict(rows)!=overlay['files']: raise ValueError('Search overlay summary rows mismatch')
    header, overlay_css, overlay_test = verify_search_header(root, overlay)
    focus = json.loads((root/'pending-search-focus.json').read_text())
    if focus.get('status') != 'pending': raise ValueError('Search focus status changed')
    focus_files={'docs-src/content/assets/site.css','docs-src/tests/test_search_focus.py'}
    if set(focus.get('files', {})) != focus_files: raise ValueError('Search focus file set changed')
    focus_summary=(root/'pending-search-focus-review.md').read_bytes()
    if sha(focus_summary)!=focus['summary_sha256']: raise ValueError('Search focus summary changed')
    focus_rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \|$',focus_summary.decode('utf-8'),re.MULTILINE)
    if len(focus_rows)!=len(focus_files) or dict(focus_rows)!=focus['files']: raise ValueError('Search focus summary rows mismatch')
    for name, expected in focus['files'].items():
        path=root.parent/name
        if name == 'docs-src/content/assets/site.css':
            rule=b'\n/* A closed search overlay must not intercept clicks during its fade-out. */\n[data-md-toggle="search"]:not(:checked) ~ .md-header .md-search__overlay { pointer-events: none; }\n'
            if overlay_css.count(rule)!=1 or overlay['prior_css_sha256']!=expected or sha(overlay_css.replace(rule,b''))!=expected: raise ValueError('Accessibility file changed: '+name)
        elif path.is_symlink() or not path.is_file() or sha(path.read_bytes())!=expected: raise ValueError('Accessibility file changed: '+name)
    if sha(overlay_css)!=overlay['files']['docs-src/content/assets/site.css'] or sha(overlay_test)!=overlay['files']['docs-src/tests/test_search_overlay.py']:
        raise ValueError('Search overlay historical bytes changed')
    shortcut = json.loads((root/'pending-search-shortcut.json').read_text())
    if shortcut.get('status') != 'pending': raise ValueError('Search shortcut not pending')
    expected={'docs-src/mkdocs.yml','docs-src/content/assets/ouro-search-shortcut.js','docs-src/tests/test_search_shortcut.cjs'}
    if set(shortcut.get('files',{})) != expected: raise ValueError('Search shortcut file set changed')
    summary=(root/'pending-search-shortcut-review.md').read_bytes()
    if sha(summary)!=shortcut['summary_sha256']: raise ValueError('Search shortcut summary changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \|$',summary.decode(),re.MULTILINE)
    if len(rows)!=len(expected) or dict(rows)!=shortcut['files']: raise ValueError('Search shortcut summary rows mismatch')
    # Preserve the newest manifest for final page/content verification.
    quick_eval = json.loads((root/'pending-quickstart-eval.json').read_text())
    if quick_eval.get('status') != 'pending' or sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()) != quick_eval['manifest_sha256']:
        raise ValueError('Quickstart evaluation manifest or pending status changed')
    summary=(root/'pending-quickstart-eval-review.md').read_bytes()
    if sha(summary)!=quick_eval['summary_sha256']: raise ValueError('Quickstart evaluation summary changed')
    quick_names={'quickstart.md','en/quickstart.md','zh/quickstart.md'}
    if set(quick_eval['pages']) != quick_names: raise ValueError('Quickstart evaluation page set changed')
    manifest=copy.deepcopy(manifest)
    for name,entry in quick_eval['pages'].items():
        if manifest['pages'].get(name)!=entry['current']: raise ValueError('Quickstart evaluation current metadata mismatch: '+name)
        manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=quick_eval['prior_manifest_sha256']:
        raise ValueError('Quickstart evaluation snapshot chain mismatch')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|$',summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(quick_names) or {x[0] for x in rows}!=quick_names: raise ValueError('Quickstart evaluation summary rows mismatch')
    for name, prior_source, prior_page, current_source, current_page in rows:
        entry=quick_eval['pages'][name]
        if (prior_source,prior_page)!=(entry['prior']['source_sha256'],entry['prior']['page_sha256']) or (current_source,current_page)!=(entry['current']['source_sha256'],entry['current']['page_sha256']):
            raise ValueError('Quickstart evaluation summary hash mismatch: '+name)
    event_display = json.loads((root/'pending-event-display.json').read_text())
    if event_display.get('status') != 'pending' or sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()) != event_display['manifest_sha256']:
        raise ValueError('Event display manifest or pending status changed')
    summary=(root/'pending-event-display-review.md').read_bytes()
    if sha(summary)!=event_display['summary_sha256']: raise ValueError('Event display summary changed')
    names={'query-projections-detail.md'}
    if set(event_display['pages']) != names: raise ValueError('Event display page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(names) or {x[0] for x in rows}!=names: raise ValueError('Event display summary rows mismatch')
    for name, source_hash, page_hash in rows:
        entry=event_display['pages'][name]['current']
        if (source_hash,page_hash)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('Event display current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in event_display['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=event_display['prior_manifest_sha256']: raise ValueError('Event display snapshot chain mismatch')
    ai_entry = json.loads((root/'pending-ai-entry.json').read_text())
    if ai_entry.get('status') != 'pending' or sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()) != ai_entry['manifest_sha256']:
        raise ValueError('AI entry manifest or pending status changed')
    summary=(root/'pending-ai-entry-review.md').read_bytes()
    if sha(summary)!=ai_entry['summary_sha256']: raise ValueError('AI entry summary changed')
    names={'index.md','quickstart.md','en/quickstart.md','zh/quickstart.md'}
    if set(ai_entry['pages']) != names: raise ValueError('AI entry page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(names) or {x[0] for x in rows}!=names: raise ValueError('AI entry summary rows mismatch')
    for name, source_hash, page_hash in rows:
        entry=ai_entry['pages'][name]['current']
        if (source_hash,page_hash)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('AI entry current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in ai_entry['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=ai_entry['prior_manifest_sha256']: raise ValueError('AI entry snapshot chain mismatch')
    cli_readability = json.loads((root/'pending-cli-readability.json').read_text())
    if cli_readability.get('status') != 'pending' or sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()) != cli_readability['manifest_sha256']:
        raise ValueError('CLI readability manifest or pending status changed')
    summary=(root/'pending-cli-readability-review.md').read_bytes()
    if sha(summary)!=cli_readability['summary_sha256']: raise ValueError('CLI readability summary changed')
    names={'quickstart.md','en/quickstart.md','zh/quickstart.md'}
    if set(cli_readability['pages']) != names: raise ValueError('CLI readability page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(names) or {x[0] for x in rows}!=names: raise ValueError('CLI readability summary rows mismatch')
    for name, source_hash, page_hash in rows:
        entry=cli_readability['pages'][name]['current']
        if (source_hash,page_hash)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('CLI readability current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in cli_readability['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=cli_readability['prior_manifest_sha256']: raise ValueError('CLI readability snapshot chain mismatch')
    run_preflight = json.loads((root/'pending-run-preflight.json').read_text())
    if run_preflight.get('status') != 'pending' or sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()) != run_preflight['manifest_sha256']:
        raise ValueError('Run preflight manifest or pending status changed')
    summary=(root/'pending-run-preflight-review.md').read_bytes()
    if sha(summary)!=run_preflight['summary_sha256']: raise ValueError('Run preflight summary changed')
    names={'en/quickstart.md','zh/quickstart.md'}
    if set(run_preflight['pages']) != names: raise ValueError('Run preflight page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(names) or {x[0] for x in rows}!=names: raise ValueError('Run preflight summary rows mismatch')
    for name, source_hash, page_hash in rows:
        entry=run_preflight['pages'][name]['current']
        if (source_hash,page_hash)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('Run preflight current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in run_preflight['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=run_preflight['prior_manifest_sha256']: raise ValueError('Run preflight snapshot chain mismatch')
    sequence = json.loads((root/'pending-quick-sequence.json').read_text())
    if sequence.get('status') != 'pending' or sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()) != sequence['manifest_sha256']:
        raise ValueError('Quick sequence manifest or pending status changed')
    summary=(root/'pending-quick-sequence-review.md').read_bytes()
    if sha(summary)!=sequence['summary_sha256']: raise ValueError('Quick sequence summary changed')
    names={'quickstart.md','en/quickstart.md','zh/quickstart.md'}
    if set(sequence['pages']) != names: raise ValueError('Quick sequence page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(names) or {x[0] for x in rows}!=names: raise ValueError('Quick sequence summary rows mismatch')
    for name, source_hash, page_hash in rows:
        entry=sequence['pages'][name]['current']
        if (source_hash,page_hash)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('Quick sequence current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in sequence['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=sequence['prior_manifest_sha256']: raise ValueError('Quick sequence snapshot chain mismatch')
    quick_nav = json.loads((root/'pending-quick-nav.json').read_text())
    if quick_nav.get('status') != 'pending' or sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()) != quick_nav['manifest_sha256']:
        raise ValueError('Quick nav manifest or pending status changed')
    summary=(root/'pending-quick-nav-review.md').read_bytes()
    if sha(summary)!=quick_nav['summary_sha256']: raise ValueError('Quick nav summary changed')
    names={'quickstart.md','en/quickstart.md','zh/quickstart.md'}
    if set(quick_nav['pages']) != names: raise ValueError('Quick nav page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(names) or {x[0] for x in rows}!=names: raise ValueError('Quick nav summary rows mismatch')
    for name, source_hash, page_hash in rows:
        entry=quick_nav['pages'][name]['current']
        if (source_hash,page_hash)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('Quick nav current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in quick_nav['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=quick_nav['prior_manifest_sha256']: raise ValueError('Quick nav snapshot chain mismatch')
    manual_table = json.loads((root/'pending-manual-table.json').read_text())
    if manual_table.get('status') != 'pending' or quick_nav['prior_manifest_sha256'] != manual_table['manifest_sha256']:
        raise ValueError('Manual table manifest or pending status changed')
    summary=(root/'pending-manual-table-review.md').read_bytes()
    if sha(summary)!=manual_table['summary_sha256']: raise ValueError('Manual table summary changed')
    names={'en/ai-troubleshooting.md'}
    if set(manual_table['pages']) != names: raise ValueError('Manual table page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(names) or {x[0] for x in rows}!=names: raise ValueError('Manual table summary rows mismatch')
    for name, source_hash, page_hash in rows:
        entry=manual_table['pages'][name]['current']
        if (source_hash,page_hash)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('Manual table current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in manual_table['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=manual_table['prior_manifest_sha256']: raise ValueError('Manual table snapshot chain mismatch')
    chain_cancel = json.loads((root/'pending-chain-cancel.json').read_text())
    if chain_cancel.get('status') != 'pending' or manual_table['prior_manifest_sha256'] != chain_cancel['manifest_sha256']:
        raise ValueError('Chain cancel manifest or pending status changed')
    summary=(root/'pending-chain-cancel-review.md').read_bytes()
    if sha(summary)!=chain_cancel['summary_sha256']: raise ValueError('Chain cancel summary changed')
    names={'ai-troubleshooting.md','en/ai-troubleshooting.md','recovery-detail.md','status-guide.md'}
    if set(chain_cancel['pages']) != names: raise ValueError('Chain cancel page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(names) or {x[0] for x in rows}!=names: raise ValueError('Chain cancel summary rows mismatch')
    for name, source_hash, page_hash in rows:
        entry=chain_cancel['pages'][name]['current']
        if (source_hash,page_hash)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('Chain cancel current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in chain_cancel['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=chain_cancel['prior_manifest_sha256']: raise ValueError('Chain cancel snapshot chain mismatch')
    job_wait = json.loads((root/'pending-job-wait.json').read_text())
    if job_wait.get('status') != 'pending' or chain_cancel['prior_manifest_sha256'] != job_wait['manifest_sha256']:
        raise ValueError('Job wait manifest or pending status changed')
    summary=(root/'pending-job-wait-review.md').read_bytes()
    if sha(summary)!=job_wait['summary_sha256']: raise ValueError('Job wait summary changed')
    names={'mcp-reference-detail.md','status-guide.md'}
    if set(job_wait['pages']) != names: raise ValueError('Job wait page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(names) or {x[0] for x in rows}!=names: raise ValueError('Job wait summary rows mismatch')
    for name, source_hash, page_hash in rows:
        entry=job_wait['pages'][name]['current']
        if (source_hash,page_hash)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('Job wait current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in job_wait['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=job_wait['prior_manifest_sha256']: raise ValueError('Job wait snapshot chain mismatch')
    cal_receipt = json.loads((root/'pending-cal-receipt.json').read_text())
    if cal_receipt.get('status') != 'pending' or job_wait['prior_manifest_sha256'] != cal_receipt['manifest_sha256']:
        raise ValueError('Calibration receipt manifest or pending status changed')
    summary=(root/'pending-cal-receipt-review.md').read_bytes()
    if sha(summary)!=cal_receipt['summary_sha256']: raise ValueError('Calibration receipt summary changed')
    names={'ai-troubleshooting.md','en/ai-troubleshooting.md','mcp-reference-guide.md','status-guide.md'}
    if set(cal_receipt['pages']) != names: raise ValueError('Calibration receipt page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(names) or {x[0] for x in rows}!=names: raise ValueError('Calibration receipt summary rows mismatch')
    for name, source_hash, page_hash in rows:
        entry=cal_receipt['pages'][name]['current']
        if (source_hash,page_hash)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('Calibration receipt current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in cal_receipt['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=cal_receipt['prior_manifest_sha256']: raise ValueError('Calibration receipt snapshot chain mismatch')
    config_qa = json.loads((root/'pending-config-qa.json').read_text())
    if config_qa.get('status') != 'pending' or cal_receipt['prior_manifest_sha256'] != config_qa['manifest_sha256']:
        raise ValueError('Config QA manifest or pending status changed')
    summary=(root/'pending-config-qa-review.md').read_bytes()
    if sha(summary)!=config_qa['summary_sha256']: raise ValueError('Config QA summary changed')
    names={'config-reference-guide.md','operations-detail.md','qa-detail.md','mcp-reference-guide.md'}
    if set(config_qa['pages']) != names: raise ValueError('Config QA page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(names) or {x[0] for x in rows}!=names: raise ValueError('Config QA summary rows mismatch')
    for name, source_hash, page_hash in rows:
        entry=config_qa['pages'][name]['current']
        if (source_hash,page_hash)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('Config QA current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in config_qa['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=config_qa['prior_manifest_sha256']: raise ValueError('Config QA snapshot chain mismatch')
    host_setup = json.loads((root/'pending-host-setup.json').read_text())
    if host_setup.get('status') != 'pending' or config_qa['prior_manifest_sha256'] != host_setup['manifest_sha256']:
        raise ValueError('Host setup manifest or pending status changed')
    summary=(root/'pending-host-setup-review.md').read_bytes()
    if sha(summary)!=host_setup['summary_sha256']: raise ValueError('Host setup summary changed')
    names={'quickstart.md','en/quickstart.md','zh/quickstart.md'}
    if set(host_setup['pages']) != names: raise ValueError('Host setup page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(names) or {x[0] for x in rows}!=names: raise ValueError('Host setup summary rows mismatch')
    for name, source_hash, page_hash in rows:
        entry=host_setup['pages'][name]['current']
        if (source_hash,page_hash)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('Host setup current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in host_setup['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=host_setup['prior_manifest_sha256']: raise ValueError('Host setup snapshot chain mismatch')
    seed_example = json.loads((root/'pending-seed-example.json').read_text())
    if seed_example.get('status') != 'pending' or host_setup['prior_manifest_sha256'] != seed_example['manifest_sha256']:
        raise ValueError('Seed example manifest or pending status changed')
    summary=(root/'pending-seed-example-review.md').read_bytes()
    if sha(summary)!=seed_example['summary_sha256']: raise ValueError('Seed example summary changed')
    names={'quickstart.md','en/quickstart.md','zh/quickstart.md'}
    if set(seed_example['pages']) != names: raise ValueError('Seed example page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(names) or {x[0] for x in rows}!=names: raise ValueError('Seed example summary rows mismatch')
    for name, source_hash, page_hash in rows:
        entry=seed_example['pages'][name]['current']
        if (source_hash,page_hash)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('Seed example current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in seed_example['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=seed_example['prior_manifest_sha256']: raise ValueError('Seed example snapshot chain mismatch')
    worktree_id = json.loads((root/'pending-worktree-id.json').read_text())
    if worktree_id.get('status') != 'pending' or seed_example['prior_manifest_sha256'] != worktree_id['manifest_sha256']:
        raise ValueError('Worktree ID manifest or pending status changed')
    summary=(root/'pending-worktree-id-review.md').read_bytes()
    if sha(summary)!=worktree_id['summary_sha256']: raise ValueError('Worktree ID summary changed')
    names={'quickstart.md','en/quickstart.md','zh/quickstart.md','existing-project-detail.md','todo-reference-example.md'}
    if set(worktree_id['pages']) != names: raise ValueError('Worktree ID page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(names) or {x[0] for x in rows}!=names: raise ValueError('Worktree ID summary rows mismatch')
    for name, source_hash, page_hash in rows:
        entry=worktree_id['pages'][name]['current']
        if (source_hash,page_hash)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('Worktree ID current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in worktree_id['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=worktree_id['prior_manifest_sha256']: raise ValueError('Worktree ID snapshot chain mismatch')
    mcp_query = json.loads((root/'pending-mcp-query.json').read_text())
    if mcp_query.get('status') != 'pending' or worktree_id['prior_manifest_sha256'] != mcp_query['manifest_sha256']:
        raise ValueError('MCP query manifest or pending status changed')
    summary=(root/'pending-mcp-query-review.md').read_bytes()
    if sha(summary)!=mcp_query['summary_sha256']: raise ValueError('MCP query summary changed')
    names={'mcp-reference-guide.md','cli-reference-guide.md'}
    if set(mcp_query['pages']) != names: raise ValueError('MCP query page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(names) or {x[0] for x in rows}!=names: raise ValueError('MCP query summary rows mismatch')
    for name, source_hash, page_hash in rows:
        entry=mcp_query['pages'][name]['current']
        if (source_hash,page_hash)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('MCP query current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in mcp_query['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=mcp_query['prior_manifest_sha256']: raise ValueError('MCP query snapshot chain mismatch')
    worktree_warning = json.loads((root/'pending-worktree-warning.json').read_text())
    if worktree_warning.get('status') != 'pending' or mcp_query['prior_manifest_sha256'] != worktree_warning['manifest_sha256']:
        raise ValueError('Worktree warning manifest or pending status changed')
    summary=(root/'pending-worktree-warning-review.md').read_bytes()
    if sha(summary)!=worktree_warning['summary_sha256']: raise ValueError('Worktree warning summary changed')
    names={'quickstart.md','en/quickstart.md','zh/quickstart.md','existing-project-detail.md'}
    if set(worktree_warning['pages']) != names: raise ValueError('Worktree warning page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(names) or {x[0] for x in rows}!=names: raise ValueError('Worktree warning summary rows mismatch')
    for name, source_hash, page_hash in rows:
        entry=worktree_warning['pages'][name]['current']
        if (source_hash,page_hash)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('Worktree warning current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in worktree_warning['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=worktree_warning['prior_manifest_sha256']: raise ValueError('Worktree warning snapshot chain mismatch')
    windows_codex = json.loads((root/'pending-windows-codex.json').read_text())
    if windows_codex.get('status') != 'pending' or worktree_warning['prior_manifest_sha256'] != windows_codex['manifest_sha256']:
        raise ValueError('Windows Codex manifest or pending status changed')
    summary=(root/'pending-windows-codex-review.md').read_bytes()
    if sha(summary)!=windows_codex['summary_sha256']: raise ValueError('Windows Codex summary changed')
    names={'quickstart.md','en/quickstart.md','zh/quickstart.md'}
    if set(windows_codex['pages']) != names: raise ValueError('Windows Codex page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(names) or {x[0] for x in rows}!=names: raise ValueError('Windows Codex summary rows mismatch')
    for name, source_hash, page_hash in rows:
        entry=windows_codex['pages'][name]['current']
        if (source_hash,page_hash)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('Windows Codex current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in windows_codex['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=windows_codex['prior_manifest_sha256']: raise ValueError('Windows Codex snapshot chain mismatch')
    home_source_labels = json.loads((root/'pending-home-source-labels.json').read_text())
    if home_source_labels.get('status') != 'pending' or windows_codex['prior_manifest_sha256'] != home_source_labels['manifest_sha256']:
        raise ValueError('Home source labels manifest or pending status changed')
    summary=(root/'pending-home-source-labels-review.md').read_bytes()
    if sha(summary)!=home_source_labels['summary_sha256']: raise ValueError('Home source labels summary changed')
    names={'index.md'}
    if set(home_source_labels['pages']) != names: raise ValueError('Home source labels page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(names) or {x[0] for x in rows}!=names: raise ValueError('Home source labels summary rows mismatch')
    for name, source_hash, page_hash in rows:
        entry=home_source_labels['pages'][name]['current']
        if (source_hash,page_hash)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('Home source labels current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in home_source_labels['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=home_source_labels['prior_manifest_sha256']: raise ValueError('Home source labels snapshot chain mismatch')
    seed_flow = json.loads((root/'pending-seed-flow.json').read_text())
    if seed_flow.get('status') != 'pending' or home_source_labels['prior_manifest_sha256'] != seed_flow['manifest_sha256']:
        raise ValueError('Seed flow manifest or pending status changed')
    summary=(root/'pending-seed-flow-review.md').read_bytes()
    if sha(summary)!=seed_flow['summary_sha256']: raise ValueError('Seed flow summary changed')
    names={'quickstart.md','en/quickstart.md','zh/quickstart.md'}
    if set(seed_flow['pages']) != names: raise ValueError('Seed flow page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(names) or {x[0] for x in rows}!=names: raise ValueError('Seed flow summary rows mismatch')
    for name, source_hash, page_hash in rows:
        entry=seed_flow['pages'][name]['current']
        if (source_hash,page_hash)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('Seed flow current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in seed_flow['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=seed_flow['prior_manifest_sha256']: raise ValueError('Seed flow snapshot chain mismatch')
    setup_split = json.loads((root/'pending-setup-split.json').read_text())
    if setup_split.get('status') != 'pending' or seed_flow['prior_manifest_sha256'] != setup_split['manifest_sha256']:
        raise ValueError('Setup split manifest or pending status changed')
    summary=(root/'pending-setup-split-review.md').read_bytes()
    if sha(summary)!=setup_split['summary_sha256']: raise ValueError('Setup split summary changed')
    names={'quickstart.md','en/quickstart.md','zh/quickstart.md'}
    if set(setup_split['pages']) != names: raise ValueError('Setup split page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(names) or {x[0] for x in rows}!=names: raise ValueError('Setup split summary rows mismatch')
    for name, source_hash, page_hash in rows:
        entry=setup_split['pages'][name]['current']
        if (source_hash,page_hash)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('Setup split current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in setup_split['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=setup_split['prior_manifest_sha256']: raise ValueError('Setup split snapshot chain mismatch')
    home_readability = json.loads((root/'pending-home-readability.json').read_text())
    if home_readability.get('status') != 'pending' or setup_split['prior_manifest_sha256'] != home_readability['manifest_sha256']:
        raise ValueError('Home readability manifest or pending status changed')
    summary=(root/'pending-home-readability-review.md').read_bytes()
    if sha(summary)!=home_readability['summary_sha256']: raise ValueError('Home readability summary changed')
    names={'index.md'}
    if set(home_readability['pages']) != names: raise ValueError('Home readability page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(names) or {x[0] for x in rows}!=names: raise ValueError('Home readability summary rows mismatch')
    for name, source_hash, page_hash in rows:
        entry=home_readability['pages'][name]['current']
        if (source_hash,page_hash)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('Home readability current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in home_readability['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=home_readability['prior_manifest_sha256']: raise ValueError('Home readability snapshot chain mismatch')
    zh_status = json.loads((root/'pending-zh-status.json').read_text())
    if zh_status.get('status') != 'pending' or home_readability['prior_manifest_sha256'] != zh_status['manifest_sha256']:
        raise ValueError('Chinese status manifest or pending status changed')
    summary=(root/'pending-zh-status-review.md').read_bytes()
    if sha(summary)!=zh_status['summary_sha256']: raise ValueError('Chinese status summary changed')
    names={'zh/troubleshooting.md'}
    if set(zh_status['pages']) != names: raise ValueError('Chinese status page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(names) or {x[0] for x in rows}!=names: raise ValueError('Chinese status summary rows mismatch')
    for name, source_hash, page_hash in rows:
        entry=zh_status['pages'][name]['current']
        if (source_hash,page_hash)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('Chinese status current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in zh_status['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=zh_status['prior_manifest_sha256']: raise ValueError('Chinese status snapshot chain mismatch')
    seed_source = json.loads((root/'pending-seed-source.json').read_text())
    if seed_source.get('status') != 'pending' or zh_status['prior_manifest_sha256'] != seed_source['manifest_sha256']:
        raise ValueError('Seed source manifest or pending status changed')
    summary=(root/'pending-seed-source-review.md').read_bytes()
    if sha(summary)!=seed_source['summary_sha256']: raise ValueError('Seed source summary changed')
    names={'seed-guide.md'}
    if set(seed_source['pages']) != names: raise ValueError('Seed source page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(names) or {x[0] for x in rows}!=names: raise ValueError('Seed source summary rows mismatch')
    for name, source_hash, page_hash in rows:
        entry=seed_source['pages'][name]['current']
        if (source_hash,page_hash)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('Seed source current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in seed_source['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=seed_source['prior_manifest_sha256']: raise ValueError('Seed source snapshot chain mismatch')
    diagnostics_auto_id = json.loads((root/'pending-diagnostics-auto-id.json').read_text())
    if diagnostics_auto_id.get('status') != 'pending' or seed_source['prior_manifest_sha256'] != diagnostics_auto_id['manifest_sha256']:
        raise ValueError('Diagnostics auto ID manifest or pending status changed')
    summary=(root/'pending-diagnostics-auto-id-review.md').read_bytes()
    if sha(summary)!=diagnostics_auto_id['summary_sha256']: raise ValueError('Diagnostics auto ID summary changed')
    names={'ai-troubleshooting.md','en/ai-troubleshooting.md'}
    if set(diagnostics_auto_id['pages']) != names: raise ValueError('Diagnostics auto ID page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(names) or {x[0] for x in rows}!=names: raise ValueError('Diagnostics auto ID summary rows mismatch')
    for name, source_hash, page_hash in rows:
        entry=diagnostics_auto_id['pages'][name]['current']
        if (source_hash,page_hash)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('Diagnostics auto ID current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in diagnostics_auto_id['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=diagnostics_auto_id['prior_manifest_sha256']: raise ValueError('Diagnostics auto ID snapshot chain mismatch')
    diagnostics_version = json.loads((root/'pending-diagnostics-version.json').read_text())
    if diagnostics_version.get('status') != 'pending' or diagnostics_auto_id['prior_manifest_sha256'] != diagnostics_version['manifest_sha256']:
        raise ValueError('Diagnostics version manifest or pending status changed')
    summary=(root/'pending-diagnostics-version-review.md').read_bytes()
    if sha(summary)!=diagnostics_version['summary_sha256']: raise ValueError('Diagnostics version summary changed')
    names={'ai-troubleshooting.md','en/ai-troubleshooting.md'}
    if set(diagnostics_version['pages']) != names: raise ValueError('Diagnostics version page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(names) or {x[0] for x in rows}!=names: raise ValueError('Diagnostics version summary rows mismatch')
    for name, source_hash, page_hash in rows:
        entry=diagnostics_version['pages'][name]['current']
        if (source_hash,page_hash)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('Diagnostics version current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in diagnostics_version['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=diagnostics_version['prior_manifest_sha256']: raise ValueError('Diagnostics version snapshot chain mismatch')
    venv_direct = json.loads((root/'pending-venv-direct.json').read_text())
    if venv_direct.get('status') != 'pending' or diagnostics_version['prior_manifest_sha256'] != venv_direct['manifest_sha256']:
        raise ValueError('Venv direct manifest or pending status changed')
    summary=(root/'pending-venv-direct-review.md').read_bytes()
    if sha(summary)!=venv_direct['summary_sha256']: raise ValueError('Venv direct summary changed')
    names={'quickstart.md','en/quickstart.md','zh/quickstart.md'}
    if set(venv_direct['pages']) != names: raise ValueError('Venv direct page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(names) or {x[0] for x in rows}!=names: raise ValueError('Venv direct summary rows mismatch')
    for name, source_hash, page_hash in rows:
        entry=venv_direct['pages'][name]['current']
        if (source_hash,page_hash)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('Venv direct current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in venv_direct['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=venv_direct['prior_manifest_sha256']: raise ValueError('Venv direct snapshot chain mismatch')
    trace_warning = json.loads((root/'pending-trace-warning.json').read_text())
    if trace_warning.get('status') != 'pending' or venv_direct['prior_manifest_sha256'] != trace_warning['manifest_sha256']:
        raise ValueError('Trace warning manifest or pending status changed')
    summary=(root/'pending-trace-warning-review.md').read_bytes()
    if sha(summary)!=trace_warning['summary_sha256']: raise ValueError('Trace warning summary changed')
    names={'harness-traces-guide.md'}
    if set(trace_warning['pages']) != names: raise ValueError('Trace warning page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(names) or {x[0] for x in rows}!=names: raise ValueError('Trace warning summary rows mismatch')
    for name, source_hash, page_hash in rows:
        entry=trace_warning['pages'][name]['current']
        if (source_hash,page_hash)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('Trace warning current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in trace_warning['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=trace_warning['prior_manifest_sha256']: raise ValueError('Trace warning snapshot chain mismatch')
    megacode_warning = json.loads((root/'pending-megacode-warning.json').read_text())
    if megacode_warning.get('status') != 'pending' or trace_warning['prior_manifest_sha256'] != megacode_warning['manifest_sha256']:
        raise ValueError('Megacode warning manifest or pending status changed')
    summary=(root/'pending-megacode-warning-review.md').read_bytes()
    if sha(summary)!=megacode_warning['summary_sha256']: raise ValueError('Megacode warning summary changed')
    names={'megacode-guide.md'}
    if set(megacode_warning['pages']) != names: raise ValueError('Megacode warning page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(names) or {x[0] for x in rows}!=names: raise ValueError('Megacode warning summary rows mismatch')
    for name, source_hash, page_hash in rows:
        entry=megacode_warning['pages'][name]['current']
        if (source_hash,page_hash)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('Megacode warning current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in megacode_warning['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=megacode_warning['prior_manifest_sha256']: raise ValueError('Megacode warning snapshot chain mismatch')
    seed_order = json.loads((root/'pending-seed-order.json').read_text())
    if seed_order.get('status') != 'pending' or megacode_warning['prior_manifest_sha256'] != seed_order['manifest_sha256']:
        raise ValueError('Seed order manifest or pending status changed')
    summary=(root/'pending-seed-order-review.md').read_bytes()
    if sha(summary)!=seed_order['summary_sha256']: raise ValueError('Seed order summary changed')
    names={'seed-guide.md'}
    if set(seed_order['pages']) != names: raise ValueError('Seed order page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(names) or {x[0] for x in rows}!=names: raise ValueError('Seed order summary rows mismatch')
    for name, source_hash, page_hash in rows:
        entry=seed_order['pages'][name]['current']
        if (source_hash,page_hash)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('Seed order current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in seed_order['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=seed_order['prior_manifest_sha256']: raise ValueError('Seed order snapshot chain mismatch')
    descriptions = json.loads((root/'pending-descriptions.json').read_text())
    if descriptions.get('status') != 'pending' or seed_order['prior_manifest_sha256'] != descriptions['manifest_sha256']:
        raise ValueError('Descriptions manifest or pending status changed')
    summary=(root/'pending-descriptions-review.md').read_bytes()
    if sha(summary)!=descriptions['summary_sha256']: raise ValueError('Descriptions summary changed')
    names={'index.md','quickstart.md','en/quickstart.md','zh/quickstart.md','ai-troubleshooting.md','existing-project-detail.md'}
    if set(descriptions['pages']) != names: raise ValueError('Descriptions page set changed')
    if not re.fullmatch(r'[0-9a-f]{64}',str(descriptions.get('generator_sha256',''))): raise ValueError('Descriptions generator hash missing')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(names) or {x[0] for x in rows}!=names: raise ValueError('Descriptions summary rows mismatch')
    for name, source_hash, page_hash in rows:
        entry=descriptions['pages'][name]['current']
        if (source_hash,page_hash)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('Descriptions current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in descriptions['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=descriptions['prior_manifest_sha256']: raise ValueError('Descriptions snapshot chain mismatch')
    worktree_input = json.loads((root/'pending-worktree-input.json').read_text())
    if worktree_input.get('status') != 'pending' or descriptions['prior_manifest_sha256'] != worktree_input['manifest_sha256']:
        raise ValueError('Worktree input manifest or pending status changed')
    summary=(root/'pending-worktree-input-review.md').read_bytes()
    if sha(summary)!=worktree_input['summary_sha256']: raise ValueError('Worktree input summary changed')
    names={'existing-project-detail.md'}
    if set(worktree_input['pages']) != names: raise ValueError('Worktree input page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(names) or {x[0] for x in rows}!=names: raise ValueError('Worktree input summary rows mismatch')
    for name, source_hash, page_hash in rows:
        entry=worktree_input['pages'][name]['current']
        if (source_hash,page_hash)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('Worktree input current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in worktree_input['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=worktree_input['prior_manifest_sha256']: raise ValueError('Worktree input snapshot chain mismatch')
    preflight = json.loads((root/'pending-preflight.json').read_text())
    if preflight.get('status') != 'pending' or worktree_input['prior_manifest_sha256'] != preflight['manifest_sha256']:
        raise ValueError('Preflight manifest or pending status changed')
    summary=(root/'pending-preflight-review.md').read_bytes()
    if sha(summary)!=preflight['summary_sha256']: raise ValueError('Preflight summary changed')
    names={'index.md','quickstart.md'}
    if set(preflight['pages']) != names: raise ValueError('Preflight page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(names) or {x[0] for x in rows}!=names: raise ValueError('Preflight summary rows mismatch')
    for name, source_hash, page_hash in rows:
        entry=preflight['pages'][name]['current']
        if (source_hash,page_hash)!=(entry['source_sha256'],entry['page_sha256']) or manifest['pages'].get(name)!=entry: raise ValueError('Preflight current metadata mismatch: '+name)
    manifest=copy.deepcopy(manifest)
    for name,entry in preflight['pages'].items(): manifest['pages'][name]=entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())!=preflight['prior_manifest_sha256']: raise ValueError('Preflight snapshot chain mismatch')
    translated = json.loads((root/'pending-translated-recovery.json').read_text())
    if translated.get('status') != 'pending' or preflight['prior_manifest_sha256'] != translated['manifest_sha256']:
        raise ValueError('Translated recovery manifest or pending status changed')
    if translated['prior_manifest_sha256'] != 'd60122332a9ee475ebd2ede76c76704e3d32e79ed70d275d8d19047604b986b9': raise ValueError('Translated recovery prior manifest changed')
    summary = (root/'pending-translated-recovery-review.md').read_bytes()
    if sha(summary) != translated['summary_sha256']: raise ValueError('Translated recovery summary changed')
    if not re.fullmatch(r'[0-9a-f]{64}', str(translated.get('generator_sha256',''))): raise ValueError('Translated recovery generator hash missing')
    if set(translated['pages']) != {'en/troubleshooting.md', 'zh/troubleshooting.md'}: raise ValueError('Translated recovery page set changed')
    rows = re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|', summary.decode('utf-8'), re.MULTILINE)
    if len(rows) != len(translated['pages']) or {row[0] for row in rows} != set(translated['pages']): raise ValueError('Translated recovery summary rows mismatch')
    for name, source_hash, page_hash in rows:
        entry = translated['pages'][name]['current']
        if (entry['source_sha256'], entry['page_sha256']) != (source_hash, page_hash) or manifest['pages'].get(name) != entry: raise ValueError('Translated recovery current metadata mismatch: '+name)
    manifest = copy.deepcopy(manifest)
    for name, entry in translated['pages'].items(): manifest['pages'][name] = entry['prior']
    if sha((json.dumps(manifest, ensure_ascii=False, indent=2)+'\n').encode()) != translated['prior_manifest_sha256']: raise ValueError('Translated recovery snapshot chain mismatch')
    navigation = json.loads((root/'pending-recovery-navigation.json').read_text())
    if navigation.get('status') != 'pending' or translated['prior_manifest_sha256'] != navigation['manifest_sha256']:
        raise ValueError('Recovery navigation manifest or pending status changed')
    if navigation['prior_manifest_sha256'] != '5a7d9f2833de983d8dd2d9e1c3711657634127ae8ce02bbdd0432c3c8d4545a6':
        raise ValueError('Recovery navigation prior manifest changed')
    summary = (root/'pending-recovery-navigation-review.md').read_bytes()
    if sha(summary) != navigation['summary_sha256']: raise ValueError('Recovery navigation summary changed')
    if set(navigation['pages']) != {'quickstart.md', 'first-run-detail.md'}: raise ValueError('Recovery navigation page set changed')
    rows = re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|', summary.decode('utf-8'), re.MULTILINE)
    if len(rows) != len(navigation['pages']) or {row[0] for row in rows} != set(navigation['pages']):
        raise ValueError('Recovery navigation summary rows mismatch')
    for name, source_hash, page_hash in rows:
        entry = navigation['pages'][name]['current']
        if (entry['source_sha256'], entry['page_sha256']) != (source_hash, page_hash) or manifest['pages'].get(name) != entry:
            raise ValueError('Recovery navigation current metadata mismatch: '+name)
    manifest = copy.deepcopy(manifest)
    for name, entry in navigation['pages'].items(): manifest['pages'][name] = entry['prior']
    if sha((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()) != navigation['prior_manifest_sha256']:
        raise ValueError('Recovery navigation snapshot chain mismatch')
    ko_venv = json.loads((root/'pending-ko-venv.json').read_text())
    if ko_venv.get('status') != 'pending' or navigation['prior_manifest_sha256'] != ko_venv['manifest_sha256']:
        raise ValueError('Korean venv manifest or pending status changed')
    if ko_venv['prior_manifest_sha256'] != '263d4ecf1f03cc86d3feccb53ee56a3e75885cce329f41c12d622b6650093da0': raise ValueError('Korean venv prior manifest changed')
    ko_venv_summary=(root/'pending-ko-venv-review.md').read_bytes()
    if sha(ko_venv_summary) != ko_venv['summary_sha256']: raise ValueError('Korean venv summary changed')
    ko_venv_names={'first-run-detail.md'}
    if set(ko_venv['pages']) != ko_venv_names: raise ValueError('Korean venv page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',ko_venv_summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(ko_venv_names) or {x[0] for x in rows}!=ko_venv_names: raise ValueError('Korean venv summary rows mismatch')
    for name, source_hash, page_hash in rows:
        page=ko_venv['pages'][name]['current']
        if (page['source_sha256'],page['page_sha256']) != (source_hash,page_hash) or manifest['pages'].get(name)!=page:
            raise ValueError('Korean venv current metadata mismatch: '+name)
    ko_venv_restored=copy.deepcopy(manifest)
    for name in ko_venv_names:
        prior=ko_venv['pages'][name]['prior']
        if prior is None: del ko_venv_restored['pages'][name]
        else: ko_venv_restored['pages'][name]=prior
    if sha((json.dumps(ko_venv_restored,ensure_ascii=False,indent=2)+'\n').encode())!=ko_venv['prior_manifest_sha256']:
        raise ValueError('Korean venv snapshot chain mismatch')
    megacode_claim = json.loads((root/'pending-megacode-claim.json').read_text())
    if manual.get('manifest_sha256') != ko_venv.get('prior_manifest_sha256') or manual.get('manifest_sha256') != megacode_claim.get('manifest_sha256'): raise ValueError('AI manual manifest chain mismatch')
    if megacode_claim.get('status') != 'pending' or ko_venv['prior_manifest_sha256'] != megacode_claim['manifest_sha256']:
        raise ValueError('Megacode claim manifest or pending status changed')
    if megacode_claim['prior_manifest_sha256'] != '079bf2deb6f23de29c939d49785aacb812a1fa8f4af4282412832caeed281af5': raise ValueError('Megacode claim prior manifest changed')
    megacode_claim_summary=(root/'pending-megacode-claim-review.md').read_bytes()
    if sha(megacode_claim_summary) != megacode_claim['summary_sha256']: raise ValueError('Megacode claim summary changed')
    megacode_claim_names={'megacode-guide.md'}
    if set(megacode_claim['pages']) != megacode_claim_names: raise ValueError('Megacode claim page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',megacode_claim_summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(megacode_claim_names) or {x[0] for x in rows}!=megacode_claim_names: raise ValueError('Megacode claim summary rows mismatch')
    for name, source_hash, page_hash in rows:
        page=megacode_claim['pages'][name]['current']
        if (page['source_sha256'],page['page_sha256']) != (source_hash,page_hash) or ko_venv_restored['pages'].get(name)!=page:
            raise ValueError('Megacode claim current metadata mismatch: '+name)
    megacode_claim_restored=copy.deepcopy(ko_venv_restored)
    for name in megacode_claim_names:
        prior=megacode_claim['pages'][name]['prior']
        if prior is None: del megacode_claim_restored['pages'][name]
        else: megacode_claim_restored['pages'][name]=prior
    if sha((json.dumps(megacode_claim_restored,ensure_ascii=False,indent=2)+'\n').encode())!=megacode_claim['prior_manifest_sha256']:
        raise ValueError('Megacode claim snapshot chain mismatch')
    sidecar = json.loads((root/'pending-sidecar.json').read_text())
    if sidecar.get('status') != 'pending' or megacode_claim['prior_manifest_sha256'] != sidecar['manifest_sha256']:
        raise ValueError('Sidecar manifest or pending status changed')
    if sidecar['prior_manifest_sha256'] != 'ec55fb966abb8da9d404100ad5f9252c0278e9c1dd06d5a9cfad26a18ab0e9e1': raise ValueError('Sidecar prior manifest changed')
    sidecar_summary=(root/'pending-sidecar-review.md').read_bytes()
    if sha(sidecar_summary) != sidecar['summary_sha256']: raise ValueError('Sidecar summary changed')
    sidecar_names={'status-guide.md'}
    if set(sidecar['pages']) != sidecar_names: raise ValueError('Sidecar page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',sidecar_summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(sidecar_names) or {x[0] for x in rows}!=sidecar_names: raise ValueError('Sidecar summary rows mismatch')
    for name, source_hash, page_hash in rows:
        page=sidecar['pages'][name]['current']
        if (page['source_sha256'],page['page_sha256']) != (source_hash,page_hash) or megacode_claim_restored['pages'].get(name)!=page:
            raise ValueError('Sidecar current metadata mismatch: '+name)
    sidecar_restored=copy.deepcopy(megacode_claim_restored)
    for name in sidecar_names:
        prior=sidecar['pages'][name]['prior']
        if prior is None: del sidecar_restored['pages'][name]
        else: sidecar_restored['pages'][name]=prior
    if sha((json.dumps(sidecar_restored,ensure_ascii=False,indent=2)+'\n').encode())!=sidecar['prior_manifest_sha256']:
        raise ValueError('Sidecar snapshot chain mismatch')
    initial_commit = json.loads((root/'pending-initial-commit.json').read_text())
    if initial_commit.get('status') != 'pending' or sidecar['prior_manifest_sha256'] != initial_commit['manifest_sha256']:
        raise ValueError('Initial commit manifest or pending status changed')
    if initial_commit['prior_manifest_sha256'] != 'f299710b8495c8378e6a3a719fb54a1774e89a30eba41ddb758ffae12bd1b8a4': raise ValueError('Initial commit prior manifest changed')
    initial_commit_summary=(root/'pending-initial-commit-review.md').read_bytes()
    if sha(initial_commit_summary) != initial_commit['summary_sha256']: raise ValueError('Initial commit summary changed')
    initial_commit_names={'quickstart.md','en/quickstart.md','zh/quickstart.md','recovery-detail.md'}
    if set(initial_commit['pages']) != initial_commit_names: raise ValueError('Initial commit page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',initial_commit_summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(initial_commit_names) or {x[0] for x in rows}!=initial_commit_names: raise ValueError('Initial commit summary rows mismatch')
    for name, source_hash, page_hash in rows:
        page=initial_commit['pages'][name]['current']
        if (page['source_sha256'],page['page_sha256']) != (source_hash,page_hash) or sidecar_restored['pages'].get(name)!=page:
            raise ValueError('Initial commit current metadata mismatch: '+name)
    initial_commit_restored=copy.deepcopy(sidecar_restored)
    for name in initial_commit_names:
        prior=initial_commit['pages'][name]['prior']
        if prior is None: del initial_commit_restored['pages'][name]
        else: initial_commit_restored['pages'][name]=prior
    if sha((json.dumps(initial_commit_restored,ensure_ascii=False,indent=2)+'\n').encode())!=initial_commit['prior_manifest_sha256']:
        raise ValueError('Initial commit snapshot chain mismatch')
    browser_example = json.loads((root/'pending-browser-example.json').read_text())
    if browser_example.get('status') != 'pending' or initial_commit['prior_manifest_sha256'] != browser_example['manifest_sha256']:
        raise ValueError('Browser example manifest or pending status changed')
    if browser_example['prior_manifest_sha256'] != 'ef700511346707327ec93499a86e7082180ec751ce037b364d82241ed80b6139': raise ValueError('Browser example prior manifest changed')
    browser_example_summary=(root/'pending-browser-example-review.md').read_bytes()
    if sha(browser_example_summary) != browser_example['summary_sha256']: raise ValueError('Browser example summary changed')
    browser_example_names={'todo-reference-example.md','seed-guide.md'}
    if set(browser_example['pages']) != browser_example_names: raise ValueError('Browser example page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',browser_example_summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(browser_example_names) or {x[0] for x in rows}!=browser_example_names: raise ValueError('Browser example summary rows mismatch')
    for name, source_hash, page_hash in rows:
        page=browser_example['pages'][name]['current']
        if (page['source_sha256'],page['page_sha256']) != (source_hash,page_hash) or initial_commit_restored['pages'].get(name)!=page:
            raise ValueError('Browser example current metadata mismatch: '+name)
    browser_example_restored=copy.deepcopy(initial_commit_restored)
    for name in browser_example_names:
        prior=browser_example['pages'][name]['prior']
        if prior is None: del browser_example_restored['pages'][name]
        else: browser_example_restored['pages'][name]=prior
    if sha((json.dumps(browser_example_restored,ensure_ascii=False,indent=2)+'\n').encode())!=browser_example['prior_manifest_sha256']:
        raise ValueError('Browser example snapshot chain mismatch')
    if not re.fullmatch(r'[0-9a-f]{64}', str(browser_example.get('generator_sha256',''))): raise ValueError('Browser example generator hash missing')
    seed_verification = json.loads((root/'pending-seed-verification.json').read_text())
    if seed_verification.get('status') != 'pending' or browser_example['prior_manifest_sha256'] != seed_verification['manifest_sha256']:
        raise ValueError('Seed verification manifest or pending status changed')
    if seed_verification['prior_manifest_sha256'] != 'b90f234ae57313065d61381506accd991d096d06fa832bbd78adef52bf9ecda0': raise ValueError('Seed verification prior manifest changed')
    seed_verification_summary=(root/'pending-seed-verification-review.md').read_bytes()
    if sha(seed_verification_summary) != seed_verification['summary_sha256']: raise ValueError('Seed verification summary changed')
    seed_verification_names={'seed-guide.md'}
    if set(seed_verification['pages']) != seed_verification_names: raise ValueError('Seed verification page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',seed_verification_summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(seed_verification_names) or {x[0] for x in rows}!=seed_verification_names: raise ValueError('Seed verification summary rows mismatch')
    for name, source_hash, page_hash in rows:
        page=seed_verification['pages'][name]['current']
        if (page['source_sha256'],page['page_sha256']) != (source_hash,page_hash) or browser_example_restored['pages'].get(name)!=page:
            raise ValueError('Seed verification current metadata mismatch: '+name)
    seed_verification_restored=copy.deepcopy(browser_example_restored)
    for name in seed_verification_names:
        prior=seed_verification['pages'][name]['prior']
        if prior is None: del seed_verification_restored['pages'][name]
        else: seed_verification_restored['pages'][name]=prior
    if sha((json.dumps(seed_verification_restored,ensure_ascii=False,indent=2)+'\n').encode())!=seed_verification['prior_manifest_sha256']:
        raise ValueError('Seed verification snapshot chain mismatch')
    worktree_result = json.loads((root/'pending-worktree-result.json').read_text())
    if worktree_result.get('status') != 'pending' or seed_verification['prior_manifest_sha256'] != worktree_result['manifest_sha256']:
        raise ValueError('Worktree result manifest or pending status changed')
    if worktree_result['prior_manifest_sha256'] != 'ca1caefda3ed1fdbda773f10b511444af4d58c05e79b06fce0481a17fabcb101': raise ValueError('Worktree result prior manifest changed')
    worktree_result_summary=(root/'pending-worktree-review-result.md').read_bytes()
    if sha(worktree_result_summary) != worktree_result['summary_sha256']: raise ValueError('Worktree result summary changed')
    worktree_result_names={'existing-project-detail.md'}
    if set(worktree_result['pages']) != worktree_result_names: raise ValueError('Worktree result page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',worktree_result_summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(worktree_result_names) or {x[0] for x in rows}!=worktree_result_names: raise ValueError('Worktree result summary rows mismatch')
    for name, source_hash, page_hash in rows:
        page=worktree_result['pages'][name]['current']
        if (page['source_sha256'],page['page_sha256']) != (source_hash,page_hash) or seed_verification_restored['pages'].get(name)!=page:
            raise ValueError('Worktree result current metadata mismatch: '+name)
    worktree_result_restored=copy.deepcopy(seed_verification_restored)
    for name in worktree_result_names:
        prior=worktree_result['pages'][name]['prior']
        if prior is None: del worktree_result_restored['pages'][name]
        else: worktree_result_restored['pages'][name]=prior
    if sha((json.dumps(worktree_result_restored,ensure_ascii=False,indent=2)+'\n').encode())!=worktree_result['prior_manifest_sha256']:
        raise ValueError('Worktree result snapshot chain mismatch')
    interview_search = json.loads((root/'pending-interview-search.json').read_text())
    if interview_search.get('status') != 'pending' or worktree_result['prior_manifest_sha256'] != interview_search['manifest_sha256']:
        raise ValueError('Interview search manifest or pending status changed')
    if interview_search['prior_manifest_sha256'] != '4dde250ec244f87fa7ae1fdb4f7dcaabd90ed55afe9ef494000c24503cf8a4c0': raise ValueError('Interview search prior manifest changed')
    interview_search_summary=(root/'pending-interview-search-review.md').read_bytes()
    if sha(interview_search_summary) != interview_search['summary_sha256']: raise ValueError('Interview search summary changed')
    interview_search_names={'en/ai-troubleshooting.md'}
    if set(interview_search['pages']) != interview_search_names: raise ValueError('Interview search page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',interview_search_summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(interview_search_names) or {x[0] for x in rows}!=interview_search_names: raise ValueError('Interview search summary rows mismatch')
    for name, source_hash, page_hash in rows:
        page=interview_search['pages'][name]['current']
        if (page['source_sha256'],page['page_sha256']) != (source_hash,page_hash) or worktree_result_restored['pages'].get(name)!=page:
            raise ValueError('Interview search current metadata mismatch: '+name)
    interview_search_restored=copy.deepcopy(worktree_result_restored)
    for name in interview_search_names:
        prior=interview_search['pages'][name]['prior']
        if prior is None: del interview_search_restored['pages'][name]
        else: interview_search_restored['pages'][name]=prior
    if sha((json.dumps(interview_search_restored,ensure_ascii=False,indent=2)+'\n').encode())!=interview_search['prior_manifest_sha256']:
        raise ValueError('Interview search snapshot chain mismatch')
    example = json.loads((root/'pending-example.json').read_text())
    if example.get('status') != 'pending' or interview_search['prior_manifest_sha256'] != example['manifest_sha256']:
        raise ValueError('Example manifest or pending status changed')
    if example['prior_manifest_sha256'] != '127beeeb9185648456340df79a40485d2e2dcc7388f944072d905a15c395132c': raise ValueError('Example prior manifest changed')
    example_summary=(root/'pending-example-review.md').read_bytes()
    if sha(example_summary) != example['summary_sha256']: raise ValueError('Example summary changed')
    example_names={'quickstart.md','seed-guide.md','en/troubleshooting.md','todo-reference-example.md'}
    if set(example['pages']) != example_names: raise ValueError('Example page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',example_summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(example_names) or {x[0] for x in rows}!=example_names: raise ValueError('Example summary rows mismatch')
    for name, source_hash, page_hash in rows:
        page=example['pages'][name]['current']
        if (page['source_sha256'],page['page_sha256']) != (source_hash,page_hash) or interview_search_restored['pages'].get(name)!=page:
            raise ValueError('Example current metadata mismatch: '+name)
    example_restored=copy.deepcopy(interview_search_restored)
    for name in example_names:
        prior=example['pages'][name]['prior']
        if prior is None: del example_restored['pages'][name]
        else: example_restored['pages'][name]=prior
    if sha((json.dumps(example_restored,ensure_ascii=False,indent=2)+'\n').encode())!=example['prior_manifest_sha256']:
        raise ValueError('Example snapshot chain mismatch')
    if not re.fullmatch(r'[0-9a-f]{64}', str(example.get('generator_sha256',''))): raise ValueError('Example generator hash missing')
    example_files={'docs-src/mkdocs.yml'}
    if set(example.get('files', {})) != example_files: raise ValueError('Example file set changed')
    file_rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \|$',example_summary.decode('utf-8'),re.MULTILINE)
    if len(file_rows)!=1 or dict(file_rows)!=example['files']: raise ValueError('Example file rows mismatch')
    for name, expected in example['files'].items():
        path=root.parent/name
        if path.is_symlink() or not path.is_file() or shortcut['prior_mkdocs_sha256'] != expected or sha(path.read_bytes().replace(b'  - assets/ouro-search-shortcut.js\n',b'')) != expected: raise ValueError('Example file changed: '+name)
    for name,digest in shortcut['files'].items():
        path=root.parent/name
        if path.is_symlink() or not path.is_file() or sha(path.read_bytes())!=digest: raise ValueError('Search shortcut file changed: '+name)
    headings = json.loads((root/'pending-headings.json').read_text())
    if headings.get('status') != 'pending' or example['prior_manifest_sha256'] != headings['manifest_sha256']:
        raise ValueError('Headings manifest or pending status changed')
    if headings['prior_manifest_sha256'] != '3297ffe6a21e153264a25aecdeff2e9692f67cd067bcbdd6f42cfb3d59fafe0b': raise ValueError('Headings prior manifest changed')
    headings_summary=(root/'pending-headings-review.md').read_bytes()
    if sha(headings_summary) != headings['summary_sha256']: raise ValueError('Headings summary changed')
    headings_names={'en/quickstart.md','zh/quickstart.md'}
    if set(headings['pages']) != headings_names: raise ValueError('Headings page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',headings_summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(headings_names) or {x[0] for x in rows}!=headings_names: raise ValueError('Headings summary rows mismatch')
    for name, source_hash, page_hash in rows:
        page=headings['pages'][name]['current']
        if (page['source_sha256'],page['page_sha256']) != (source_hash,page_hash) or example_restored['pages'].get(name)!=page:
            raise ValueError('Headings current metadata mismatch: '+name)
    headings_restored=copy.deepcopy(example_restored)
    for name in headings_names: headings_restored['pages'][name]=headings['pages'][name]['prior']
    if sha((json.dumps(headings_restored,ensure_ascii=False,indent=2)+'\n').encode())!=headings['prior_manifest_sha256']:
        raise ValueError('Headings snapshot chain mismatch')
    heading_files={'docs-src/mkdocs.yml','docs-src/heading_labels.py','docs-src/tests/test_heading_labels.py'}
    if set(headings.get('files', {})) != heading_files: raise ValueError('Headings file set changed')
    file_rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \|$',headings_summary.decode('utf-8'),re.MULTILINE)
    if len(file_rows)!=len(heading_files) or dict(file_rows)!=headings['files']: raise ValueError('Headings file rows mismatch')
    for name, expected in headings['files'].items():
        path=root.parent/name
        if name == 'docs-src/mkdocs.yml':
            if expected != example['prior_mkdocs_sha256']: raise ValueError('Example prior config mismatch')
        elif path.is_symlink() or not path.is_file() or sha(path.read_bytes()) != expected: raise ValueError('Headings file changed: '+name)
    session = json.loads((root/'pending-session.json').read_text())
    if session.get('status') != 'pending' or headings['prior_manifest_sha256'] != session['manifest_sha256']:
        raise ValueError('Session manifest or pending status changed')
    if session['prior_manifest_sha256'] != 'ea59b6a439e9af819e1915035f6bd14fcac6581e37ab211d1aed8f006506a69f': raise ValueError('Session prior manifest changed')
    session_summary=(root/'pending-session-review.md').read_bytes()
    if sha(session_summary) != session['summary_sha256']: raise ValueError('Session summary changed')
    session_names={'index.md','progress-detail.md','recovery-detail.md','status-guide.md','ai-troubleshooting.md','en/ai-troubleshooting.md'}
    if set(session['pages']) != session_names: raise ValueError('Session page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',session_summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(session_names) or {x[0] for x in rows}!=session_names: raise ValueError('Session summary rows mismatch')
    for name, source_hash, page_hash in rows:
        page=session['pages'][name]['current']
        if (page['source_sha256'],page['page_sha256']) != (source_hash,page_hash) or headings_restored['pages'].get(name)!=page:
            raise ValueError('Session current metadata mismatch: '+name)
    session_restored=copy.deepcopy(headings_restored)
    for name in session_names: session_restored['pages'][name]=session['pages'][name]['prior']
    if sha((json.dumps(session_restored,ensure_ascii=False,indent=2)+'\n').encode())!=session['prior_manifest_sha256']:
        raise ValueError('Session snapshot chain mismatch')
    runtime = json.loads((root/'pending-runtime.json').read_text())
    if home.get('manifest_sha256') != session.get('prior_manifest_sha256') or home.get('manifest_sha256') != runtime.get('manifest_sha256'): raise ValueError('Home manifest chain mismatch')
    if runtime.get('status') != 'pending' or session['prior_manifest_sha256'] != runtime['manifest_sha256']:
        raise ValueError('Runtime manifest or pending status changed')
    if runtime['prior_manifest_sha256'] != 'cba82169c5fffef75de469b8e3722016ece8551b0067c4906d6154efa9642bb8': raise ValueError('Runtime prior manifest changed')
    runtime_summary=(root/'pending-runtime-review.md').read_bytes()
    if sha(runtime_summary) != runtime['summary_sha256']: raise ValueError('Runtime summary changed')
    runtime_names={'megacode-guide.md','runtime-support-detail.md'}
    if set(runtime['pages']) != runtime_names: raise ValueError('Runtime page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',runtime_summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(runtime_names) or {x[0] for x in rows}!=runtime_names: raise ValueError('Runtime summary rows mismatch')
    for name, source_hash, page_hash in rows:
        page=runtime['pages'][name]['current']
        if (page['source_sha256'],page['page_sha256']) != (source_hash,page_hash) or session_restored['pages'].get(name)!=page:
            raise ValueError('Runtime current metadata mismatch: '+name)
    runtime_restored=copy.deepcopy(session_restored)
    for name in runtime_names: runtime_restored['pages'][name]=runtime['pages'][name]['prior']
    if sha((json.dumps(runtime_restored,ensure_ascii=False,indent=2)+'\n').encode())!=runtime['prior_manifest_sha256']:
        raise ValueError('Runtime snapshot chain mismatch')
    seed_version = json.loads((root/'pending-seed-version.json').read_text())
    if seed_version.get('status') != 'pending' or runtime['prior_manifest_sha256'] != seed_version['manifest_sha256']:
        raise ValueError('Seed version manifest or pending status changed')
    if seed_version['prior_manifest_sha256'] != '25c8aa5b5a2adbea5ed1abcc278b142dacf2681b3deb30953744c12b3c9053f3': raise ValueError('Seed version prior manifest changed')
    seed_version_summary=(root/'pending-seed-version-review.md').read_bytes()
    if sha(seed_version_summary) != seed_version['summary_sha256']: raise ValueError('Seed version summary changed')
    seed_version_names={'seed-guide.md'}
    if set(seed_version['pages']) != seed_version_names: raise ValueError('Seed version page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',seed_version_summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(seed_version_names) or {x[0] for x in rows}!=seed_version_names: raise ValueError('Seed version summary rows mismatch')
    for name, source_hash, page_hash in rows:
        page=seed_version['pages'][name]['current']
        if (page['source_sha256'],page['page_sha256']) != (source_hash,page_hash) or runtime_restored['pages'].get(name)!=page:
            raise ValueError('Seed version current metadata mismatch: '+name)
    seed_version_restored=copy.deepcopy(runtime_restored)
    for name in seed_version_names: seed_version_restored['pages'][name]=seed_version['pages'][name]['prior']
    if sha((json.dumps(seed_version_restored,ensure_ascii=False,indent=2)+'\n').encode())!=seed_version['prior_manifest_sha256']:
        raise ValueError('Seed version snapshot chain mismatch')
    interview = json.loads((root/'pending-interview.json').read_text())
    if interview.get('status') != 'pending' or seed_version['prior_manifest_sha256'] != interview['manifest_sha256']:
        raise ValueError('Interview manifest or pending status changed')
    if interview['prior_manifest_sha256'] != '6ed8a45fc1f5080d6be9158b945e2f834a1cc010caa5a5b6fa74e9d161eec286': raise ValueError('Interview prior manifest changed')
    interview_summary=(root/'pending-interview-review.md').read_bytes()
    if sha(interview_summary) != interview['summary_sha256']: raise ValueError('Interview summary changed')
    interview_names={'interview-guide.md'}
    if set(interview['pages']) != interview_names: raise ValueError('Interview page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',interview_summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(interview_names) or {x[0] for x in rows}!=interview_names: raise ValueError('Interview summary rows mismatch')
    for name, source_hash, page_hash in rows:
        page=interview['pages'][name]['current']
        if (page['source_sha256'],page['page_sha256']) != (source_hash,page_hash) or seed_version_restored['pages'].get(name)!=page:
            raise ValueError('Interview current metadata mismatch: '+name)
    interview_restored=copy.deepcopy(seed_version_restored)
    for name in interview_names: interview_restored['pages'][name]=interview['pages'][name]['prior']
    if sha((json.dumps(interview_restored,ensure_ascii=False,indent=2)+'\n').encode())!=interview['prior_manifest_sha256']:
        raise ValueError('Interview snapshot chain mismatch')
    seed = json.loads((root/'pending-seed.json').read_text())
    if seed.get('status') != 'pending' or interview['prior_manifest_sha256'] != seed['manifest_sha256']:
        raise ValueError('Seed manifest or pending status changed')
    if seed['prior_manifest_sha256'] != 'b095ccfea3e380c3a330ebc46bda00703f61cd8ab591acfd2979f8465a908164': raise ValueError('Seed prior manifest changed')
    seed_summary=(root/'pending-seed-review.md').read_bytes()
    if sha(seed_summary) != seed['summary_sha256']: raise ValueError('Seed summary changed')
    seed_names={'quickstart.md','en/quickstart.md','zh/quickstart.md','seed-guide.md'}
    if set(seed['pages']) != seed_names: raise ValueError('Seed page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',seed_summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(seed_names) or {x[0] for x in rows}!=seed_names: raise ValueError('Seed summary rows mismatch')
    for name, source_hash, page_hash in rows:
        page=seed['pages'][name]['current']
        if (page['source_sha256'],page['page_sha256']) != (source_hash,page_hash) or interview_restored['pages'].get(name)!=page:
            raise ValueError('Seed current metadata mismatch: '+name)
    seed_restored=copy.deepcopy(interview_restored)
    for name in seed_names: seed_restored['pages'][name]=seed['pages'][name]['prior']
    if sha((json.dumps(seed_restored,ensure_ascii=False,indent=2)+'\n').encode())!=seed['prior_manifest_sha256']:
        raise ValueError('Seed snapshot chain mismatch')
    package = json.loads((root/'pending-package.json').read_text())
    if package.get('status') != 'pending' or seed['prior_manifest_sha256'] != package['manifest_sha256']:
        raise ValueError('Package manifest or pending status changed')
    if package['prior_manifest_sha256'] != '0c103b41bad9c41bafd7e0d6713520d49386a225c300ecfc31e35d8f347bf5a6': raise ValueError('Package prior manifest changed')
    package_summary=(root/'pending-package-review.md').read_bytes()
    if sha(package_summary) != package['summary_sha256']: raise ValueError('Package summary changed')
    package_names={'check-package-detail.md','cli-reference-detail.md'}
    if set(package['pages']) != package_names: raise ValueError('Package page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',package_summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(package_names) or {x[0] for x in rows}!=package_names: raise ValueError('Package summary rows mismatch')
    for name, source_hash, page_hash in rows:
        page=package['pages'][name]['current']
        if (page['source_sha256'],page['page_sha256']) != (source_hash,page_hash) or seed_restored['pages'].get(name)!=page:
            raise ValueError('Package current metadata mismatch: '+name)
    package_restored=copy.deepcopy(seed_restored)
    for name in package_names: package_restored['pages'][name]=package['pages'][name]['prior']
    if sha((json.dumps(package_restored,ensure_ascii=False,indent=2)+'\n').encode())!=package['prior_manifest_sha256']:
        raise ValueError('Package snapshot chain mismatch')
    diagnostic = json.loads((root/'pending-job-diagnostic.json').read_text())
    if diagnostic.get('status') != 'pending' or package['prior_manifest_sha256'] != diagnostic['manifest_sha256']:
        raise ValueError('Diagnostic manifest or pending status changed')
    if diagnostic['prior_manifest_sha256'] != 'b62efecbb144f3f7a1f6af1df1e82dccece51a8e427ecb59bce2171b32c2eee3': raise ValueError('Diagnostic prior manifest changed')
    diagnostic_summary=(root/'pending-job-diagnostic-review.md').read_bytes()
    if sha(diagnostic_summary) != diagnostic['summary_sha256']: raise ValueError('Diagnostic summary changed')
    diagnostic_names={'recovery-detail.md','ai-troubleshooting.md','en/ai-troubleshooting.md'}
    if set(diagnostic['pages']) != diagnostic_names: raise ValueError('Diagnostic page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',diagnostic_summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(diagnostic_names) or {x[0] for x in rows}!=diagnostic_names: raise ValueError('Diagnostic summary rows mismatch')
    for name, source_hash, page_hash in rows:
        page=diagnostic['pages'][name]['current']
        if (page['source_sha256'],page['page_sha256']) != (source_hash,page_hash) or package_restored['pages'].get(name)!=page:
            raise ValueError('Diagnostic current metadata mismatch: '+name)
    diagnostic_restored=copy.deepcopy(package_restored)
    for name in diagnostic_names: diagnostic_restored['pages'][name]=diagnostic['pages'][name]['prior']
    if sha((json.dumps(diagnostic_restored,ensure_ascii=False,indent=2)+'\n').encode())!=diagnostic['prior_manifest_sha256']:
        raise ValueError('Diagnostic snapshot chain mismatch')
    permissions = json.loads((root/'pending-permissions.json').read_text())
    if permissions.get('status') != 'pending' or diagnostic['prior_manifest_sha256'] != permissions['manifest_sha256']:
        raise ValueError('Permissions manifest or pending status changed')
    if permissions['prior_manifest_sha256'] != '3aa371fb502fd0debf74365b9168a792a1b2e1290c346d6e625bb51f05976b3e': raise ValueError('Permissions prior manifest changed')
    permissions_summary=(root/'pending-permissions-review.md').read_bytes()
    if sha(permissions_summary) != permissions['summary_sha256']: raise ValueError('Permissions summary changed')
    permissions_names={'quickstart.md','en/quickstart.md','zh/quickstart.md','ai-troubleshooting.md','en/ai-troubleshooting.md'}
    if set(permissions['pages']) != permissions_names: raise ValueError('Permissions page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',permissions_summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(permissions_names) or {x[0] for x in rows}!=permissions_names: raise ValueError('Permissions summary rows mismatch')
    for name, source_hash, page_hash in rows:
        page=permissions['pages'][name]['current']
        if (page['source_sha256'],page['page_sha256']) != (source_hash,page_hash) or diagnostic_restored['pages'].get(name)!=page:
            raise ValueError('Permissions current metadata mismatch: '+name)
    if permissions.get('mid_manifest_sha256') != '6afa1dc4983a9407a24df1ca3d2c5f0589a307891d664d62d2df196e3f1dd4f2': raise ValueError('Permissions intermediate snapshot changed')
    permissions_restored=copy.deepcopy(diagnostic_restored)
    for level, expected in (('mid',permissions['mid_manifest_sha256']),('prior',permissions['prior_manifest_sha256'])):
        for name in permissions_names: permissions_restored['pages'][name]=permissions['pages'][name][level]
        if sha((json.dumps(permissions_restored,ensure_ascii=False,indent=2)+'\n').encode())!=expected:
            raise ValueError('Permissions snapshot chain mismatch: '+level)
    details = json.loads((root/'pending-details.json').read_text())
    if details.get('status') != 'pending' or permissions['prior_manifest_sha256'] != details['manifest_sha256']:
        raise ValueError('Details manifest or pending status changed')
    if details['prior_manifest_sha256'] != '723c433f14ddf86540074b9ecaf4dfb4fbaac8773e396bf8409e1569719cc7ce': raise ValueError('Details prior manifest changed')
    if not re.fullmatch(r'[0-9a-f]{64}',str(details.get('generator_sha256',''))): raise ValueError('Details generator hash missing')
    details_summary=(root/'pending-details-review.md').read_bytes()
    if sha(details_summary) != details['summary_sha256']: raise ValueError('Details summary changed')
    details_names={'quickstart.md','en/quickstart.md','zh/quickstart.md','recovery-detail.md'}
    if set(details['pages']) != details_names: raise ValueError('Details page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',details_summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(details_names) or {x[0] for x in rows}!=details_names: raise ValueError('Details summary rows mismatch')
    for name, source_hash, page_hash in rows:
        page=details['pages'][name]['current']
        if (page['source_sha256'],page['page_sha256']) != (source_hash,page_hash) or permissions_restored['pages'].get(name)!=page:
            raise ValueError('Details current metadata mismatch: '+name)
    details_restored=copy.deepcopy(permissions_restored)
    for name in details_names: details_restored['pages'][name]=details['pages'][name]['prior']
    if sha((json.dumps(details_restored,ensure_ascii=False,indent=2)+'\n').encode())!=details['prior_manifest_sha256']:
        raise ValueError('Details snapshot chain mismatch')
    access = json.loads((root/'pending-accessibility.json').read_text())
    if access.get('status') != 'pending' or details['prior_manifest_sha256'] != access['manifest_sha256']:
        raise ValueError('Accessibility manifest or pending status changed')
    access_files={'docs-src/content/assets/site.css','docs-src/overrides/main.html','docs-src/tests/test_accessibility_styles.py'}
    if set(access.get('files', {})) != access_files: raise ValueError('Accessibility file set changed')
    access_summary=(root/'pending-accessibility-review.md').read_bytes()
    if sha(access_summary) != access['summary_sha256']: raise ValueError('Accessibility summary changed')
    access_rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \|$',access_summary.decode('utf-8'),re.MULTILINE)
    if len(access_rows)!=len(access_files) or dict(access_rows)!=access['files']: raise ValueError('Accessibility summary rows mismatch')
    for name, expected in access['files'].items():
        path=root.parent/name
        if name == 'docs-src/overrides/main.html':
            if expected != home['prior_main_sha256']: raise ValueError('Home prior template mismatch')
        elif name == 'docs-src/content/assets/site.css':
            if expected != focus['prior_css_sha256']: raise ValueError('Search focus prior CSS mismatch')
        elif path.is_symlink() or not path.is_file() or sha(path.read_bytes())!=expected: raise ValueError('Accessibility file changed: '+name)
    evaluation = json.loads((root/'pending-evaluation.json').read_text())
    if evaluation.get('status') != 'pending' or details['prior_manifest_sha256'] != evaluation['manifest_sha256']:
        raise ValueError('Evaluation manifest or pending status changed')
    if evaluation['prior_manifest_sha256'] != '8d5f3f543953f78406099e1ec0b70e3d783e4c53860ec4a14f5cb791db76f50e': raise ValueError('Evaluation prior manifest changed')
    evaluation_summary=(root/'pending-evaluation-review.md').read_bytes()
    if sha(evaluation_summary) != evaluation['summary_sha256']: raise ValueError('Evaluation summary changed')
    evaluation_names={'quickstart.md','en/quickstart.md','zh/quickstart.md'}
    if set(evaluation['pages']) != evaluation_names: raise ValueError('Evaluation page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',evaluation_summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(evaluation_names) or {x[0] for x in rows}!=evaluation_names: raise ValueError('Evaluation summary rows mismatch')
    for name, source_hash, page_hash in rows:
        page=evaluation['pages'][name]['current']
        if (page['source_sha256'],page['page_sha256']) != (source_hash,page_hash) or details_restored['pages'].get(name)!=page:
            raise ValueError('Evaluation current metadata mismatch: '+name)
    evaluation_restored=copy.deepcopy(details_restored)
    for name in evaluation_names: evaluation_restored['pages'][name]=evaluation['pages'][name]['prior']
    if sha((json.dumps(evaluation_restored,ensure_ascii=False,indent=2)+'\n').encode())!=evaluation['prior_manifest_sha256']:
        raise ValueError('Evaluation snapshot chain mismatch')
    discovery = json.loads((root/'pending-discovery.json').read_text())
    if discovery.get('status') != 'pending' or evaluation['prior_manifest_sha256'] != discovery['manifest_sha256']:
        raise ValueError('Discovery manifest or pending status changed')
    if discovery['prior_llms_sha256'] != '2632632c91c2ffc253ac44c88e99039f24c0bcd7f39c80733414f4594b36bac0':
        raise ValueError('Discovery prior AI index changed')
    discovery_files={'docs-src/overrides/main.html','site/llms.txt','docs-src/tests/test_discovery.py'}
    if set(discovery.get('files', {})) != discovery_files: raise ValueError('Discovery file set changed')
    discovery_summary=(root/'pending-discovery-review.md').read_bytes()
    if sha(discovery_summary) != discovery['summary_sha256']: raise ValueError('Discovery summary changed')
    discovery_rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \|$',discovery_summary.decode('utf-8'),re.MULTILINE)
    if len(discovery_rows)!=len(discovery_files) or dict(discovery_rows)!=discovery['files']: raise ValueError('Discovery summary rows mismatch')
    for name, expected in discovery['files'].items():
        path=root.parent/name
        if name == 'docs-src/overrides/main.html':
            if expected != access['prior_main_sha256']: raise ValueError('Accessibility prior main mismatch')
        elif name == 'site/llms.txt':
            if expected != manual['prior_llms_sha256']: raise ValueError('AI manual prior index mismatch')
        elif path.is_symlink() or not path.is_file() or sha(path.read_bytes())!=expected: raise ValueError('Discovery file changed: '+name)
    worktree = json.loads((root/'pending-worktree.json').read_text())
    if worktree.get('status') != 'pending' or evaluation['prior_manifest_sha256'] != worktree['manifest_sha256']:
        raise ValueError('Worktree manifest or pending status changed')
    if worktree['prior_manifest_sha256'] != '69796799c107e5a995469e2c1a5c6e7e249f67237df0ddc9d1b2ce447241c2d6': raise ValueError('Worktree prior manifest changed')
    worktree_summary=(root/'pending-worktree-review.md').read_bytes()
    if sha(worktree_summary) != worktree['summary_sha256']: raise ValueError('Worktree summary changed')
    worktree_names={'quickstart.md','en/quickstart.md','zh/quickstart.md','ai-troubleshooting.md','en/ai-troubleshooting.md'}
    if set(worktree['pages']) != worktree_names: raise ValueError('Worktree page set changed')
    rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',worktree_summary.decode('utf-8'),re.MULTILINE)
    if len(rows)!=len(worktree_names) or {x[0] for x in rows}!=worktree_names: raise ValueError('Worktree summary rows mismatch')
    for name, source_hash, page_hash in rows:
        page=worktree['pages'][name]['current']
        if (page['source_sha256'],page['page_sha256']) != (source_hash,page_hash) or evaluation_restored['pages'].get(name)!=page:
            raise ValueError('Worktree current metadata mismatch: '+name)
    worktree_restored=copy.deepcopy(evaluation_restored)
    for name in worktree_names: worktree_restored['pages'][name]=worktree['pages'][name]['prior']
    if sha((json.dumps(worktree_restored,ensure_ascii=False,indent=2)+'\n').encode())!=worktree['prior_manifest_sha256']:
        raise ValueError('Worktree snapshot chain mismatch')
    search = json.loads((root/'pending-search.json').read_text())
    if search.get('status') != 'pending' or worktree['prior_manifest_sha256'] != search['manifest_sha256']:
        raise ValueError('Search manifest or pending status changed')
    if search['prior_manifest_sha256'] != '51ee6cf67ffed9fba8ab8b593b4728b7169452076b9f741730d833b94e82d56c': raise ValueError('Search prior manifest changed')
    search_summary=(root/'pending-search-review.md').read_bytes()
    if sha(search_summary) != search['summary_sha256']: raise ValueError('Search summary changed')
    search_names={'quickstart.md','en/quickstart.md','zh/quickstart.md'}
    search_files={'augment-search.py','content/assets/ouro-theme.js','content/assets/site.css','tests/test_search_languages.cjs'}
    if set(search['pages']) != search_names or set(search['files']) != search_files: raise ValueError('Search page or file set changed')
    page_rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',search_summary.decode('utf-8'),re.MULTILINE)
    file_rows=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \|$',search_summary.decode('utf-8'),re.MULTILINE)
    if len(page_rows)!=len(search_names) or {x[0] for x in page_rows}!=search_names or len(file_rows)!=len(search_files) or dict(file_rows)!=search['files']:
        raise ValueError('Search summary rows mismatch')
    for name, source_hash, page_hash in page_rows:
        page=search['pages'][name]['current']
        if (page['source_sha256'],page['page_sha256']) != (source_hash,page_hash) or worktree_restored['pages'].get(name)!=page:
            raise ValueError('Search current metadata mismatch: '+name)
    for name, expected in search['files'].items():
        path=root/name
        if name == 'content/assets/site.css':
            if expected != access['prior_css_sha256']: raise ValueError('Accessibility prior CSS mismatch')
        elif name == 'content/assets/ouro-theme.js':
            if path.is_symlink() or not path.is_file(): raise ValueError('Search file changed: '+name)
            if escape['prior_js_sha256']!=expected: raise ValueError('Search file changed: '+name)
            restore_search_javascript(path.read_bytes(),expected)
        elif path.is_symlink() or not path.is_file() or sha(path.read_bytes())!=expected: raise ValueError('Search file changed: '+name)
    for name, expected in escape['files'].items():
        path=root.parent/name
        if path.is_symlink() or not path.is_file() or sha(path.read_bytes())!=expected: raise ValueError('Search Escape file changed: '+name)
    search_restored=copy.deepcopy(worktree_restored)
    for name in search_names: search_restored['pages'][name]=search['pages'][name]['prior']
    if sha((json.dumps(search_restored,ensure_ascii=False,indent=2)+'\n').encode())!=search['prior_manifest_sha256']:
        raise ValueError('Search snapshot chain mismatch')
    locale = json.loads((root/'pending-locale.json').read_text())
    locale_files = {'content/assets/ouro-theme.js','overrides/main.html','overrides/partials/language.html','overrides/partials/nav.html','overrides/partials/nav-item.html','tests/test_locale_ui.py'}
    if locale.get('status') != 'pending' or locale.get('manifest_sha256') != search['prior_manifest_sha256']:
        raise ValueError('Locale manifest or pending status changed')
    if set(locale.get('files', {})) != locale_files: raise ValueError('Locale file set changed')
    locale_summary = (root/'pending-locale-review.md').read_bytes()
    if sha(locale_summary) != locale['summary_sha256']: raise ValueError('Locale summary changed')
    locale_rows = re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \|',locale_summary.decode('utf-8'),re.MULTILINE)
    if len(locale_rows) != len(locale_files) or dict(locale_rows) != locale['files']:
        raise ValueError('Locale summary file hashes mismatch')
    for name, expected in locale['files'].items():
        path = root/name
        if name == 'content/assets/ouro-theme.js':
            if expected != search['prior_js_sha256']: raise ValueError('Search prior JS mismatch')
        elif name == 'overrides/main.html':
            if expected != discovery['prior_main_sha256']: raise ValueError('Discovery prior main mismatch')
        elif path.is_symlink() or not path.is_file() or sha(path.read_bytes()) != expected:
            raise ValueError('Locale file changed: '+name)
    if locale['prior_js_sha256'] != evidence['static_content_sha256']['assets/ouro-theme.js']:
        raise ValueError('Locale prior JS does not match old evidence')
    if search['prior_css_sha256'] != evidence['static_content_sha256']['assets/site.css']: raise ValueError('Search prior CSS mismatch')
    install = json.loads((root/'pending-install.json').read_text())
    if install.get('status') != 'pending' or search['prior_manifest_sha256'] != install['manifest_sha256']:
        raise ValueError('Installation manifest or pending status changed')
    anchors = {'mid_manifest_sha256':'8d2bd20b236120b5ade616e56b030902870c7bf2744a925ea23cf4b514a055a0','interim_manifest_sha256':'cdff69ea47481b6658506269938a15c57b886544df6007df07552799cf7c8ca1','prior_manifest_sha256':'c82fbdfb3593de50e72fc13d67c53fd8a22444050893b5cd2ea18f6ee947727a'}
    if any(install.get(k) != v for k,v in anchors.items()): raise ValueError('Installation chain anchor changed')
    install_summary = (root/'pending-install-review.md').read_bytes()
    if sha(install_summary) != install['summary_sha256']: raise ValueError('Installation summary changed')
    install_names = {'quickstart.md','en/quickstart.md','zh/quickstart.md','first-run-detail.md'}
    if set(install['pages']) != install_names: raise ValueError('Installation page set changed')
    install_rows = re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',install_summary.decode('utf-8'),re.MULTILINE)
    if len(install_rows) != len(install_names) or {x[0] for x in install_rows} != install_names: raise ValueError('Installation summary rows incomplete or duplicated')
    for name, source_hash, page_hash in install_rows:
        page = install['pages'][name]['current']
        if (page['source_sha256'],page['page_sha256']) != (source_hash,page_hash) or search_restored['pages'].get(name) != page:
            raise ValueError('Installation current metadata mismatch: '+name)
    install_restored = copy.deepcopy(search_restored)
    for level, expected in (('mid',install['mid_manifest_sha256']),('interim',install['interim_manifest_sha256']),('prior',install['prior_manifest_sha256'])):
        for name in install_names: install_restored['pages'][name] = install['pages'][name][level]
        raw = (json.dumps(install_restored,ensure_ascii=False,indent=2)+'\n').encode()
        if sha(raw) != expected: raise ValueError('Installation snapshot chain mismatch: '+level)
    latest = json.loads((root/'pending-latest.json').read_text())
    if latest.get('status') != 'pending' or install['prior_manifest_sha256'] != latest['manifest_sha256']:
        raise ValueError('Latest manifest or pending status changed')
    if latest['mid_manifest_sha256'] != '19b0d170589066675f7dcbbd4dfc7e291fcbe0b6e539feee1c839a2a0b2f4af1' or latest['prior_manifest_sha256'] != 'a488794807be63edc6fbbd65cb474fdafb82b74eb32e62c16362cc66acbe303d':
        raise ValueError('Latest chain anchor changed')
    latest_summary = (root/'pending-latest-review.md').read_bytes()
    if sha(latest_summary) != latest['summary_sha256']: raise ValueError('Latest summary changed')
    latest_names = {'ai-troubleshooting.md','en/ai-troubleshooting.md','cli-reference-guide.md'}
    if set(latest['pages']) != latest_names: raise ValueError('Latest page set changed')
    latest_rows = re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|',latest_summary.decode('utf-8'),re.MULTILINE)
    if len(latest_rows) != len(latest_names) or {x[0] for x in latest_rows} != latest_names: raise ValueError('Latest summary rows incomplete or duplicated')
    for name, source_hash, page_hash in latest_rows:
        page = latest['pages'][name]['current']
        if (page['source_sha256'],page['page_sha256']) != (source_hash,page_hash) or install_restored['pages'].get(name) != page:
            raise ValueError('Latest current metadata mismatch: '+name)
    latest_restored = copy.deepcopy(install_restored)
    for level, expected in (('mid',latest['mid_manifest_sha256']),('prior',latest['prior_manifest_sha256'])):
        for name in latest_names: latest_restored['pages'][name] = latest['pages'][name][level]
        raw = (json.dumps(latest_restored,ensure_ascii=False,indent=2)+'\n').encode()
        if sha(raw) != expected: raise ValueError('Latest snapshot chain mismatch: '+level)
    journey = json.loads((root/'pending-journey.json').read_text())
    if journey.get('mid_manifest_sha256') != '008a851dce898884dbf91ec55385936e901dea46a8e045969b37e1e006ad2d8b':
        raise ValueError('Journey intermediate snapshot changed')
    if journey.get('status') != 'pending' or latest['prior_manifest_sha256'] != journey['manifest_sha256']:
        raise ValueError('Journey manifest or pending status changed')
    summary_journey = (root/'pending-journey-review.md').read_bytes()
    if sha(summary_journey) != journey['summary_sha256']:
        raise ValueError('Journey summary changed')
    journey_names = {'progress-detail.md','recovery-detail.md','evaluation-evolution-detail.md','quickstart.md','en/quickstart.md','zh/quickstart.md'}
    if set(journey['pages']) != journey_names:
        raise ValueError('Journey page set changed')
    journey_rows = re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|', summary_journey.decode('utf-8'), re.MULTILINE)
    if len(journey_rows) != len(journey_names) or {x[0] for x in journey_rows} != journey_names:
        raise ValueError('Journey summary rows incomplete or duplicated')
    for name, source_hash, page_hash in journey_rows:
        page = journey['pages'][name]['current']
        if (page['source_sha256'],page['page_sha256']) != (source_hash,page_hash) or latest_restored['pages'].get(name) != page:
            raise ValueError('Journey current metadata mismatch: '+name)
    journey_restored = copy.deepcopy(latest_restored)
    for level, expected in (('mid',journey['mid_manifest_sha256']), ('prior',journey['prior_manifest_sha256'])):
        for name in journey_names: journey_restored['pages'][name] = journey['pages'][name][level]
        raw = (json.dumps(journey_restored,ensure_ascii=False,indent=2)+'\n').encode()
        if sha(raw) != expected: raise ValueError('Journey snapshot chain mismatch: '+level)
    if journey['prior_manifest_sha256'] != pending['manifest_sha256']:
        raise ValueError('Journey does not match prior pending snapshot')
    if sha((root/'pending-new-guides-review.md').read_bytes()) != pending['summary_sha256']:
        raise ValueError('Summary changed')
    if set(pending['pages']) != NAMES:
        raise ValueError('New page list changed')
    summary = (root/'pending-new-guides-review.md').read_text(encoding='utf-8')
    rows = re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \| ([0-9a-f]{64}) \|', summary, re.MULTILINE)
    if len(rows) != len(NAMES) or {row[0] for row in rows} != NAMES:
        raise ValueError('Summary page rows incomplete or duplicated')
    for name, source_hash, page_hash in rows:
        item = pending['pages'][name]
        if (item.get('source_sha256'), item.get('page_sha256')) != (source_hash, page_hash):
            raise ValueError('Summary hash mismatch: '+name)
    for name in NAMES:
        if journey_restored['pages'].get(name) != pending['pages'][name]:
            raise ValueError('New page metadata changed: '+name)
    restored = journey_restored
    for name in NAMES: del restored['pages'][name]
    original = (json.dumps(restored,ensure_ascii=False,indent=2)+'\n').encode()
    if sha(original) != BASE or pending['prior_manifest_sha256'] != BASE:
        raise ValueError('Prior manifest cannot be reconstructed')
    validate(restored, evidence, require_approved=False)
    public = root/'review-evidence'
    if public.is_symlink() or {p.name for p in public.iterdir()} != set(evidence['public_review_sha256']):
        raise ValueError('Prior public evidence set changed')
    for name, expected in evidence['public_review_sha256'].items():
        item = public/name
        if item.is_symlink() or not item.is_file() or sha(item.read_bytes()) != expected:
            raise ValueError('Prior public evidence changed: '+name)
    for name in ('link_evidence.py', 'verify-content.py'):
        if sha((root/name).read_bytes()) != evidence['verification_sha256'][name]:
            raise ValueError('Prior verifier changed: '+name)
    locale_evidence = copy.deepcopy(evidence)
    locale_evidence['static_content_sha256']['assets/ouro-theme.js'] = escape['files']['docs-src/content/assets/ouro-theme.js']
    locale_evidence['static_content_sha256']['assets/site.css'] = header['files']['docs-src/content/assets/site.css']
    locale_evidence['static_content_sha256']['assets/ouro-search-shortcut.js'] = shortcut['files']['docs-src/content/assets/ouro-search-shortcut.js']
    verify_content_tree(root/'content', current_manifest, locale_evidence)
    print('Pending summary, manifest and generated bytes match; canonical source is not checked here. Gate remains closed.')

if __name__ == '__main__': verify()
