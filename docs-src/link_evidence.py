"""Validate a narrowly scoped, snapshot-bound changed-link review record.

Hashes establish identity, not reviewer independence or factual correctness.
"""
import copy
import hashlib
import json
import re
from pathlib import Path, PurePosixPath
import os

SHA = re.compile(r'^[0-9a-f]{64}$')
EXPECTED_SCOPE = 'changed-link-groups-92-only'
STATIC_CONTENT = {
    'assets/site.css', 'assets/ouro-theme.js', 'assets/ouro-mermaid.js',
    'assets/vendor/mermaid/LICENSE', 'assets/vendor/mermaid/README.txt',
    'assets/vendor/mermaid/mermaid-11.4.1.min.js',
}
PUBLIC_REVIEW_FILES = {'groups-before.md', 'groups-current.md', 'review-a-summary.md', 'review-b-summary.md', 'delta-chain.md', 'outbound-delta.md'}
EVIDENCE_KEYS = {'classification', 'review_a', 'review_b', 'map_delta',
                 'routing_delta', 'first_run_delta', 'english_delta'}


def manifest_digest(manifest):
    """Ignore only the approval flag to avoid a boolean/hash cycle."""
    if not isinstance(manifest.get('semantic_links_reviewed'), bool):
        raise ValueError('Manifest approval flag must be a boolean')
    normalized = dict(manifest)
    normalized['semantic_links_reviewed'] = False
    encoded = json.dumps(normalized, ensure_ascii=False, sort_keys=True,
                         separators=(',', ':')).encode('utf-8')
    return hashlib.sha256(encoded).hexdigest()


def validate(manifest, evidence, *, require_approved=True):
    if evidence.get('schema') != 1 or evidence.get('scope') != EXPECTED_SCOPE:
        raise ValueError('Invalid link review scope or schema')
    if evidence.get('group_count') != 92:
        raise ValueError('Review group count must be 92')
    if evidence.get('manifest_sha256') != manifest_digest(manifest):
        raise ValueError('Manifest does not match link review snapshot')
    if not SHA.fullmatch(str(evidence.get('generator_sha256', ''))):
        raise ValueError('Missing generator digest')
    if not SHA.fullmatch(str(evidence.get('reviewed_generator_sha256', ''))):
        raise ValueError('Missing originally reviewed generator digest')
    chain = evidence.get('delta_reversions')
    names = ('en/troubleshooting.md', 'first-run-detail.md', 'routing-detail.md', 'architecture-map-public.md')
    if not isinstance(chain, list) or tuple(x.get('page') for x in chain if isinstance(x, dict)) != names:
        raise ValueError('Incomplete or unordered reviewed delta chain')
    restored = copy.deepcopy(manifest)
    restored['semantic_links_reviewed'] = False
    for step in chain:
        page = restored.get('pages', {}).get(step['page'])
        if not isinstance(page, dict): raise ValueError('Missing delta page')
        for key in ('source_sha256', 'page_sha256'):
            if page.get(key) != step.get('current_' + key) or not SHA.fullmatch(str(step.get('previous_' + key, ''))):
                raise ValueError('Delta page hash does not match')
            page[key] = step['previous_' + key]
        old_bytes = (json.dumps(restored, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
        if hashlib.sha256(old_bytes).hexdigest() != step.get('previous_manifest_sha256'):
            raise ValueError('Delta manifest chain does not match')
    if chain[-1]['previous_manifest_sha256'] != evidence.get('reviewed_base_manifest_sha256'):
        raise ValueError('Reviewed base manifest does not match delta chain')
    records = evidence.get('evidence_sha256')
    if not isinstance(records, dict) or set(records) != EVIDENCE_KEYS:
        raise ValueError('Incomplete link review evidence digests')
    if any(not SHA.fullmatch(str(value)) for value in records.values()):
        raise ValueError('Invalid link review evidence digest')
    public = evidence.get('public_review_sha256')
    if not isinstance(public, dict) or set(public) != PUBLIC_REVIEW_FILES:
        raise ValueError('Incomplete public link evidence')
    if any(not SHA.fullmatch(str(value)) for value in public.values()):
        raise ValueError('Invalid public link evidence digest')
    outbound = evidence.get('outbound_delta_review')
    if not isinstance(outbound, dict) or outbound.get('status') not in ('pending', 'approved'):
        raise ValueError('Missing outbound delta review status')
    verifiers = evidence.get('verification_sha256')
    if not isinstance(verifiers, dict) or set(verifiers) != {'link_evidence.py', 'verify-content.py', 'workspace-verifier'}:
        raise ValueError('Missing verification code digests')
    if any(not SHA.fullmatch(str(value)) for value in verifiers.values()):
        raise ValueError('Invalid verification code digest')
    deps = evidence.get('site_dependencies')
    if not isinstance(deps, dict) or set(deps) != {'site/assets/learn/ooo-interview.gif'}:
        raise ValueError('Missing reviewed site asset digest')
    if any(not SHA.fullmatch(str(value)) for value in deps.values()):
        raise ValueError('Invalid reviewed site asset digest')
    static = evidence.get('static_content_sha256')
    if not isinstance(static, dict) or set(static) != STATIC_CONTENT:
        raise ValueError('Static content allowlist is incomplete')
    if any(not SHA.fullmatch(str(value)) for value in static.values()):
        raise ValueError('Invalid static content digest')
    review = evidence.get('implementation_review')
    if not isinstance(review, dict) or review.get('status') not in ('pending', 'approved'):
        raise ValueError('Missing independent implementation review status')
    if require_approved:
        if manifest['semantic_links_reviewed'] is not True:
            raise ValueError('Changed-link review gate is closed')
        if (review['status'] != 'approved' or not review.get('reviewer')
                or not review.get('reviewed_at_utc')
                or not SHA.fullmatch(str(review.get('evidence_sha256', '')))):
            raise ValueError('Independent implementation re-review is incomplete')
        if (outbound['status'] != 'approved' or not outbound.get('reviewer')
                or not outbound.get('reviewed_at_utc')
                or not SHA.fullmatch(str(outbound.get('evidence_sha256', '')))):
            raise ValueError('Independent outbound delta review is incomplete')
    elif manifest['semantic_links_reviewed'] is not False:
        raise ValueError('Pending validation requires the gate to remain closed')


def load(root):
    root = Path(root)
    return (json.loads((root/'content-manifest.json').read_text(encoding='utf-8')),
            json.loads((root/'link-review-evidence.json').read_text(encoding='utf-8')))


def verify_content_tree(content_root, manifest, evidence):
    """Reject unlisted files, symlinks, unsafe names and changed content."""
    content_root = Path(content_root)
    if content_root.is_symlink():
        raise ValueError('Content root is a symlink')
    pages = manifest.get('pages', {})
    assets = manifest.get('assets', {})
    static = evidence['static_content_sha256']
    if not isinstance(pages, dict) or not isinstance(assets, dict):
        raise ValueError('Invalid manifest file maps')
    names = list(pages) + list(assets) + list(static)
    if len(names) != len(set(names)):
        raise ValueError('Overlapping content entries')
    for name in names:
        path = PurePosixPath(name)
        if not name or path.is_absolute() or '..' in path.parts or str(path) != name:
            raise ValueError('Unsafe content entry')
    actual = set()
    for directory, dirs, files in os.walk(content_root, followlinks=False):
        for name in dirs + files:
            path = Path(directory) / name
            if path.is_symlink(): raise ValueError('Symlink in content tree')
        for name in files:
            path = Path(directory) / name
            if not path.is_file(): raise ValueError('Non-regular content file')
            actual.add(path.relative_to(content_root).as_posix())
    if actual != set(names):
        raise ValueError('Content tree differs from reviewed allowlist')
    expected = {name: entry['page_sha256'] for name, entry in pages.items()}
    expected.update({name: entry['sha256'] for name, entry in assets.items()})
    expected.update(static)
    for name, value in expected.items():
        if not SHA.fullmatch(str(value)) or hashlib.sha256((content_root/name).read_bytes()).hexdigest() != value:
            raise ValueError('Content hash does not match: ' + name)
