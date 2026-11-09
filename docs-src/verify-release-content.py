#!/usr/bin/env python3
"""Verify a separately reviewed current release; never approve or mutate inputs.

Legacy pending records remain pending. Review authenticity is established by
repository review and the user's deployment decision, not by these hashes.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

import pending_publication_snapshot as inventory

ROOT = Path(__file__).resolve().parent.parent
BASELINE = '5c15731dd3c8a7cb7c4f6bf851b50494641185db45443bba884376ce2276c660'
REPORTS = {'semantic': 'semantic-review.md', 'outbound': 'outbound-review.md',
           'mac_codex': 'mac-codex.md', 'validation': 'validation.md'}
CHECKS = {
    'semantic': {'instructions_versions', 'cross_artifact_consumers', 'historical_review_gaps', 'current_delta_coverage'},
    'outbound': {'historical_92_groups', 'historical_outbound_delta', 'current_link_contexts', 'routes_anchors_languages'},
    'mac_codex': {'installation', 'manual_discovery_read', 'product_first_task', 'result_verification',
                  'mcp_failure_diagnosis', 'interrupted_task_diagnosis', 'version_difference_diagnosis', 'actual_model_use'},
    'validation': {'full_tests', 'strict_build', 'search_export_sitemaps', 'canonical_sync',
                   'desktop_mobile_keyboard_impact', 'public_information_review'},
}
SHA = re.compile(r'[0-9a-f]{64}')
UTC = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def exact(value, keys, code):
    if not isinstance(value, dict) or set(value) != set(keys):
        raise ValueError(code)


def digest(value, code):
    if not isinstance(value, str) or SHA.fullmatch(value) is None:
        raise ValueError(code)


def load(root, name):
    raw = inventory.regular(root, name).read_bytes()
    return json.loads(raw.decode('utf-8'), object_pairs_hook=inventory.unique_pairs), raw


def run_pending(root):
    # No shell, arbitrary command, model, install or external service is used.
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    try:
        subprocess.run([sys.executable, str(root/'docs-src/verify-pending-guides.py')],
                       cwd=root, env=env, stdin=subprocess.DEVNULL,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                       check=True, timeout=180)
    except (OSError, subprocess.SubprocessError) as exc:
        raise ValueError('Historical pending verification failed') from exc


def verify(root=ROOT):
    root = Path(root)
    try:
        record, record_raw = load(root, 'release-evidence.json')
    except FileNotFoundError as exc:
        raise ValueError('Current release approval missing: release-evidence.json') from exc
    exact(record, {'schema', 'scope', 'status', 'baseline_snapshot_sha256',
                   'snapshot_sha256', 'generator_sha256', 'reviews', 'other_hosts'}, 'Invalid release record keys')
    if type(record['schema']) is not int or record['schema'] != 1 or record['scope'] != 'documentation-release-current-snapshot':
        raise ValueError('Invalid release schema or scope')
    if record['status'] != 'approved':
        raise ValueError('Current release approval is incomplete')
    if record['baseline_snapshot_sha256'] != BASELINE:
        raise ValueError('Release baseline snapshot changed')
    digest(record['snapshot_sha256'], 'Invalid release snapshot digest')
    digest(record['generator_sha256'], 'Invalid release generator digest')
    snapshot, snapshot_raw = load(root, inventory.SNAPSHOT)
    if sha(snapshot_raw) != record['snapshot_sha256']:
        raise ValueError('Release approval snapshot mismatch')
    if record['generator_sha256'] != snapshot.get('generator_sha256'):
        raise ValueError('Release generator mismatch')
    inventory.verify(root, snapshot)
    exact(record['reviews'], REPORTS, 'Incomplete release reviews')
    directory = root/'release-review'
    inventory.require_no_symlink_ancestors(directory)
    if not directory.is_dir() or {p.name for p in directory.iterdir()} != set(REPORTS.values()):
        raise ValueError('Release review file set differs')
    report_bytes = {}
    for role, filename in REPORTS.items():
        review = record['reviews'][role]
        exact(review, {'status', 'reviewer', 'reviewed_at_utc', 'snapshot_sha256', 'report_sha256', 'checks'},
              'Invalid release review keys: '+role)
        if review['status'] != 'approved' or not isinstance(review['reviewer'], str) or not review['reviewer'].strip():
            raise ValueError('Release review incomplete: '+role)
        stamp = review['reviewed_at_utc']
        if not isinstance(stamp, str) or UTC.fullmatch(stamp) is None:
            raise ValueError('Invalid release review timestamp: '+role)
        # strptime rejects impossible dates in otherwise well-formed UTC text.
        from datetime import datetime
        try:
            datetime.strptime(stamp, '%Y-%m-%dT%H:%M:%SZ')
        except ValueError as exc:
            raise ValueError('Invalid release review timestamp: '+role) from exc
        if review['snapshot_sha256'] != record['snapshot_sha256']:
            raise ValueError('Release review snapshot mismatch: '+role)
        digest(review['report_sha256'], 'Invalid release report digest: '+role)
        exact(review['checks'], CHECKS[role], 'Incomplete release checks: '+role)
        if any(value != 'pass' for value in review['checks'].values()):
            raise ValueError('Required release check not passed: '+role)
        path = 'release-review/'+filename
        raw = inventory.regular(root, path).read_bytes()
        if sha(raw) != review['report_sha256']:
            raise ValueError('Release report changed: '+role)
        if not raw.decode('utf-8').strip():
            raise ValueError('Empty release report: '+role)
        report_bytes[path] = raw
    others = record['other_hosts']
    if not isinstance(others, list) or not others:
        raise ValueError('Other host followup inventory missing')
    names = set()
    for host in others:
        exact(host, {'host', 'status', 'reason'}, 'Invalid host followup')
        if (not isinstance(host['host'], str) or not host['host'].strip()
                or host['host'] in names or host['status'] != 'followup'
                or not isinstance(host['reason'], str) or not host['reason'].strip()):
            raise ValueError('Invalid host followup')
        names.add(host['host'])
    run_pending(root)
    # Reject changes observed during the child check; this is not an OS lock.
    inventory.verify(root, snapshot)
    if inventory.regular(root, inventory.SNAPSHOT).read_bytes() != snapshot_raw:
        raise ValueError('Snapshot changed during verification')
    if inventory.regular(root, 'release-evidence.json').read_bytes() != record_raw:
        raise ValueError('Release record changed during verification')
    if {p.name for p in directory.iterdir()} != set(REPORTS.values()):
        raise ValueError('Release review file set differs')
    for path, raw in report_bytes.items():
        if inventory.regular(root, path).read_bytes() != raw:
            raise ValueError('Release report changed during verification')
    return len(snapshot['files'])


def main():
    try:
        count = verify()
    except (ValueError, OSError, KeyError, TypeError, UnicodeError) as exc:
        raise SystemExit('Publication blocked: '+str(exc)) from exc
    print(f'Current release evidence and {count} pending inputs verified; historical records remain pending.')
    print('Technical review evidence does not replace the user\'s final merge/deploy approval.')


if __name__ == '__main__':
    main()
