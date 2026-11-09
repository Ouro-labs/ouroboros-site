#!/usr/bin/env python3
"""Pending-only publication input inventory; does not authorize publication.

Hashes bind bytes, not human review, factual truth, or reviewer identity. The
legacy publication verifier and workflow remain the only production gate.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat

ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT = 'docs-src/pending-publication-snapshot.json'
TREES = ('site', 'docs-src', '.github/workflows')
GENERATED = 'site/docs'
# Python bytecode under the tool and its test directory is not a Pages input.
# Do not ignore caches under content or site: those can be published.
CACHES = ('docs-src/__pycache__', 'docs-src/tests/__pycache__')
SHA = re.compile(r'^[0-9a-f]{64}$')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON key: '+key)
        result[key] = value
    return result


def load_json(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique_pairs)


def safe_relative(value):
    if not isinstance(value, str) or not value or '\\' in value or '\x00' in value:
        raise ValueError('Invalid relative path')
    p = PurePosixPath(value)
    if p.is_absolute() or str(p) != value or any(x in ('', '.', '..') for x in p.parts):
        raise ValueError('Non-canonical path: '+value)
    return p


def require_no_symlink_ancestors(path):
    p = Path(path).absolute()
    for component in (p, *p.parents):
        if component.is_symlink(): raise ValueError('Symlink ancestor rejected')


def regular(root, relative):
    parts = safe_relative(relative).parts
    require_no_symlink_ancestors(root)
    p = root
    if p.is_symlink() or not p.is_dir():
        raise ValueError('Root is not a regular directory')
    for index, part in enumerate(parts):
        p = p / part
        info = p.lstat()
        if stat.S_ISLNK(info.st_mode):
            raise ValueError('Symlink rejected: '+relative)
        if index < len(parts)-1 and not stat.S_ISDIR(info.st_mode):
            raise ValueError('Non-directory ancestor: '+relative)
    if not stat.S_ISREG(p.lstat().st_mode):
        raise ValueError('Non-regular file: '+relative)
    return p


def collect(root):
    require_no_symlink_ancestors(root)
    result = {}
    for tree in TREES:
        start = root / tree
        require_no_symlink_ancestors(start)
        if start.is_symlink() or not start.is_dir():
            raise ValueError('Input tree missing or symlink: '+tree)
        for current, dirs, files in os.walk(start, followlinks=False):
            for name in list(dirs):
                p = Path(current)/name
                rel = p.relative_to(root).as_posix()
                if p.is_symlink(): raise ValueError('Symlink rejected: '+rel)
                if rel == GENERATED or rel in CACHES: dirs.remove(name)
            for name in files:
                p = Path(current)/name
                rel = p.relative_to(root).as_posix()
                if rel == SNAPSHOT: continue
                result[rel] = digest(regular(root, rel).read_bytes())
    return dict(sorted(result.items()))


def check_manifest(root, files):
    rel = 'docs-src/content-manifest.json'
    manifest = load_json(regular(root, rel))
    if manifest.get('semantic_links_reviewed') is not False:
        raise ValueError('Pending snapshot requires closed semantic gate')
    pages = manifest.get('pages')
    if not isinstance(pages, dict) or len(pages) != 63:
        raise ValueError('Expected 63 manifest pages')
    sources = set()
    for name, entry in pages.items():
        safe_relative(name)
        path = 'docs-src/content/'+name
        if path not in files or files[path] != entry.get('page_sha256'):
            raise ValueError('Manifest page mismatch: '+name)
        source = entry.get('source')
        p = safe_relative(source)
        if source in sources: raise ValueError('Duplicate canonical source')
        sources.add(source)
        if not p.parts or p.parts[0] != 'content' or not SHA.fullmatch(str(entry.get('source_sha256',''))):
            raise ValueError('Invalid source metadata: '+name)
    assets = manifest.get('assets')
    if not isinstance(assets, dict) or set(pages) & set(assets): raise ValueError('Invalid or overlapping asset map')
    for name, entry in assets.items():
        safe_relative(name)
        path = 'docs-src/content/'+name
        if path not in files or files[path] != entry.get('sha256'):
            raise ValueError('Manifest asset mismatch: '+name)
    evidence = load_json(regular(root, 'docs-src/link-review-evidence.json'))
    for key in ('outbound_delta_review', 'implementation_review'):
        if evidence.get(key, {}).get('status') != 'pending': raise ValueError('Legacy review must remain pending: '+key)
    static = evidence.get('static_content_sha256')
    if not isinstance(static, dict) or (set(pages) | set(assets)) & set(static):
        raise ValueError('Invalid or overlapping static content map')
    for name, expected in static.items():
        safe_relative(name)
        if not SHA.fullmatch(str(expected)) or 'docs-src/content/'+name not in files:
            raise ValueError('Static content missing or legacy hash malformed: '+name)
    shortcut = load_json(regular(root, 'docs-src/pending-search-shortcut.json'))
    shortcut_files = shortcut.get('files', {})
    shortcut_path = 'docs-src/content/assets/ouro-search-shortcut.js'
    if shortcut.get('status') != 'pending' or not isinstance(shortcut_files, dict) or shortcut_files.get(shortcut_path) != files.get(shortcut_path):
        raise ValueError('Search shortcut input missing or changed')
    if 'assets/ouro-search-shortcut.js' in set(pages) | set(assets) | set(static):
        raise ValueError('Search shortcut content overlaps')
    static = dict(static)
    static['assets/ouro-search-shortcut.js'] = shortcut_files[shortcut_path]
    # This additional asset is pending, never historical publication approval.
    locale_path = root/'docs-src/pending-search-locale.json'
    if locale_path.exists():
        locale = load_json(regular(root, 'docs-src/pending-search-locale.json'))
        if digest(locale_path.read_bytes()) != '810076c353de29b0b88e349d28cbcd46341ccc82b0792f617ccf790245cb4c7e' or locale.get('status') != 'pending':
            raise ValueError('Search locale pending record changed')
        name = 'assets/ouro-search-locale.js'
        current = locale.get('files', {}).get('content/'+name, {}).get('current')
        if not isinstance(current, str) or digest(current.encode()) != files.get('docs-src/content/'+name):
            raise ValueError('Search locale pending asset changed')
        if name in set(pages) | set(assets) | set(static):
            raise ValueError('Search locale content overlaps')
        static[name] = digest(current.encode())
    actual_content = {name.removeprefix('docs-src/content/') for name in files if name.startswith('docs-src/content/')}
    if actual_content != set(pages) | set(assets) | set(static):
        raise ValueError('Content file set differs from manifest and static inputs')
    return digest(regular(root, rel).read_bytes())


def create(root, generator):
    files = collect(root)
    manifest_sha = check_manifest(root, files)
    require_no_symlink_ancestors(generator)
    if generator.is_symlink() or not generator.is_file(): raise ValueError('Generator must be a regular non-symlink file')
    return {'schema': 1, 'status': 'pending', 'manifest_sha256': manifest_sha,
            'generator_sha256': digest(generator.read_bytes()), 'files': files}


def verify(root, snapshot, generator=None):
    if set(snapshot) != {'schema','status','manifest_sha256','generator_sha256','files'} or type(snapshot['schema']) is not int or snapshot['schema'] != 1 or snapshot['status'] != 'pending':
        raise ValueError('Only pending snapshot schema is supported')
    if not SHA.fullmatch(str(snapshot['generator_sha256'])): raise ValueError('Invalid generator hash')
    recorded = snapshot['files']
    if not isinstance(recorded, dict): raise ValueError('Invalid input file map')
    for name, value in recorded.items():
        safe_relative(name)
        if not SHA.fullmatch(str(value)): raise ValueError('Invalid input hash: '+name)
    actual = collect(root)
    if set(actual) != set(recorded): raise ValueError('Input file set differs')
    for name, value in actual.items():
        if value != recorded[name]: raise ValueError('Input file changed: '+name)
    if check_manifest(root, actual) != snapshot['manifest_sha256']: raise ValueError('Manifest hash differs')
    if generator is not None:
        require_no_symlink_ancestors(generator)
        if generator.is_symlink() or not generator.is_file() or digest(generator.read_bytes()) != snapshot['generator_sha256']:
            raise ValueError('Local generator differs')
    return len(actual)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('capture','verify'))
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--generator', type=Path)
    args = parser.parse_args()
    root = args.root.absolute()
    try:
        if args.mode == 'capture':
            if args.generator is None: raise ValueError('Capture requires --generator')
            result = create(root, args.generator)
            path = root/SNAPSHOT
            with path.open('x', encoding='utf-8') as f: json.dump(result, f, ensure_ascii=False, indent=2); f.write('\n')
            print('Pending inventory captured; no review or publication approval granted.')
        else:
            path = regular(root, SNAPSHOT)
            n = verify(root, load_json(path), args.generator)
            print(f'Pending input bytes and set match ({n} files); generator '+('matched locally' if args.generator else 'not checked locally')+'.')
            print('No publication approval, reviewer identity or factual truth is established.')
    except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        raise SystemExit('Pending inventory rejected: '+str(exc)) from exc

if __name__ == '__main__': main()
