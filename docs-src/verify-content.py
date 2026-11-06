#!/usr/bin/env python3
"""Check changed-link evidence and generated content before site publication."""
import hashlib
from pathlib import Path
from link_evidence import load, validate, verify_content_tree

root = Path(__file__).resolve().parent
manifest, evidence = load(root)
try:
    validate(manifest, evidence)
except ValueError as exc:
    raise SystemExit(f'Publication blocked: {exc}') from exc
public = root / 'review-evidence'
actual = {p.name for p in public.iterdir() if p.is_file() and not p.is_symlink()}
if actual != set(evidence['public_review_sha256']) or any(p.is_symlink() or not p.is_file() for p in public.iterdir()):
    raise SystemExit('Publication blocked: public review evidence set changed')
for name, expected in evidence['public_review_sha256'].items():
    if hashlib.sha256((public / name).read_bytes()).hexdigest() != expected:
        raise SystemExit(f'Publication blocked: public review evidence changed: {name}')
for name in ('link_evidence.py', 'verify-content.py'):
    if hashlib.sha256((root / name).read_bytes()).hexdigest() != evidence['verification_sha256'][name]:
        raise SystemExit(f'Link verifier changed: {name}')
for name, expected in evidence['site_dependencies'].items():
    if hashlib.sha256((root.parent / name).read_bytes()).hexdigest() != expected:
        raise SystemExit(f'Reviewed site asset changed: {name}')
try:
    verify_content_tree(root / 'content', manifest, evidence)
except (ValueError, OSError, KeyError) as exc:
    raise SystemExit(f'Publication blocked: {exc}') from exc
print(f"Verified changed-link evidence and {len(manifest['pages'])} generated pages.")
