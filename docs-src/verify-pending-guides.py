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

def sha(data): return hashlib.sha256(data).hexdigest()
def verify(root=ROOT):
    for name in ('content-manifest.json', 'link-review-evidence.json', 'pending-new-guides.json', 'pending-new-guides-review.md', 'pending-journey.json', 'pending-journey-review.md', 'pending-latest.json', 'pending-latest-review.md', 'pending-install.json', 'pending-install-review.md', 'pending-locale.json', 'pending-locale-review.md'):
        path = root/name
        if path.is_symlink() or not path.is_file():
            raise ValueError('Evidence input is not a regular non-symlink file: '+name)
    manifest, evidence = load(root)
    pending = json.loads((root/'pending-new-guides.json').read_text())
    if manifest.get('semantic_links_reviewed') is not False or pending.get('status') != 'pending':
        raise ValueError('Pending extension requires closed gate')
    locale = json.loads((root/'pending-locale.json').read_text())
    locale_files = {'content/assets/ouro-theme.js','overrides/main.html','overrides/partials/language.html','overrides/partials/nav.html','overrides/partials/nav-item.html','tests/test_locale_ui.py'}
    if locale.get('status') != 'pending' or locale.get('manifest_sha256') != sha((root/'content-manifest.json').read_bytes()):
        raise ValueError('Locale manifest or pending status changed')
    if set(locale.get('files', {})) != locale_files: raise ValueError('Locale file set changed')
    locale_summary = (root/'pending-locale-review.md').read_bytes()
    if sha(locale_summary) != locale['summary_sha256']: raise ValueError('Locale summary changed')
    locale_rows = re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \|',locale_summary.decode('utf-8'),re.MULTILINE)
    if len(locale_rows) != len(locale_files) or dict(locale_rows) != locale['files']:
        raise ValueError('Locale summary file hashes mismatch')
    for name, expected in locale['files'].items():
        path = root/name
        if path.is_symlink() or not path.is_file() or sha(path.read_bytes()) != expected:
            raise ValueError('Locale file changed: '+name)
    if locale['prior_js_sha256'] != evidence['static_content_sha256']['assets/ouro-theme.js']:
        raise ValueError('Locale prior JS does not match old evidence')
    install = json.loads((root/'pending-install.json').read_text())
    if install.get('status') != 'pending' or sha((root/'content-manifest.json').read_bytes()) != install['manifest_sha256']:
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
        if (page['source_sha256'],page['page_sha256']) != (source_hash,page_hash) or manifest['pages'].get(name) != page:
            raise ValueError('Installation current metadata mismatch: '+name)
    install_restored = copy.deepcopy(manifest)
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
        if manifest['pages'].get(name) != pending['pages'][name]:
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
    locale_evidence['static_content_sha256']['assets/ouro-theme.js'] = locale['files']['content/assets/ouro-theme.js']
    verify_content_tree(root/'content', manifest, locale_evidence)
    print('Pending summary, manifest and generated bytes match; canonical source is not checked here. Gate remains closed.')

if __name__ == '__main__': verify()
