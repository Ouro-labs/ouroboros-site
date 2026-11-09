"""Synthetic approvals exist only in temporary fixtures, never the real tree."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'docs-src'))
spec = importlib.util.spec_from_file_location('release_verifier', ROOT/'docs-src/verify-release-content.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class ReleaseEvidenceTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)/'site-repo'
        self.root.mkdir()
        for tree in mod.inventory.TREES:
            ignore = shutil.ignore_patterns('__pycache__', 'docs') if tree == 'site' else shutil.ignore_patterns('__pycache__')
            shutil.copytree(ROOT/tree, self.root/tree, symlinks=True, ignore=ignore)
        # Only metadata identity is needed here; canonical sync has its own checks.
        generator = Path(self.temp.name)/'synthetic-generator.py'
        generator.write_text('# synthetic generator identity, not executed\n')
        snapshot = mod.inventory.create(self.root, generator)
        self.snapshot_path = self.root/mod.inventory.SNAPSHOT
        self.write(self.snapshot_path, snapshot)
        self.record = {
            'schema': 1, 'scope': 'documentation-release-current-snapshot', 'status': 'approved',
            'baseline_snapshot_sha256': mod.BASELINE,
            'snapshot_sha256': mod.sha(self.snapshot_path.read_bytes()),
            'generator_sha256': snapshot['generator_sha256'], 'reviews': {},
            'other_hosts': [{'host': 'non-Mac hosts (synthetic fixture)', 'status': 'followup', 'reason': 'test only'}],
        }
        directory = self.root/'release-review'
        directory.mkdir()
        for role, name in mod.REPORTS.items():
            raw = ('SYNTHETIC UNITTEST ONLY: '+role+'\n').encode()
            (directory/name).write_bytes(raw)
            self.record['reviews'][role] = {
                'status': 'approved', 'reviewer': 'synthetic unittest only', 'reviewed_at_utc': '2026-11-10T00:00:00Z',
                'snapshot_sha256': self.record['snapshot_sha256'], 'report_sha256': mod.sha(raw),
                'checks': {name: 'pass' for name in mod.CHECKS[role]},
            }
        self.save()

    def write(self, path, value):
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')

    def save(self):
        self.write(self.root/'release-evidence.json', self.record)

    def baseline(self):
        self.assertGreaterEqual(mod.verify(self.root), 413)

    def rejected(self, text):
        with self.assertRaisesRegex((ValueError, OSError), text):
            mod.verify(self.root)

    def test_real_child_and_cli_baseline(self):
        self.baseline()
        result = subprocess.run([sys.executable, str(self.root/'docs-src/verify-release-content.py')],
                                capture_output=True, text=True, timeout=180)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('historical records remain pending', result.stdout)

    def test_missing_approval_blocks_cli(self):
        (self.root/'release-evidence.json').unlink()
        result = subprocess.run([sys.executable, str(self.root/'docs-src/verify-release-content.py')],
                                capture_output=True, text=True, timeout=180)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Current release approval missing', result.stderr)

    def test_missing_mac_report_and_workflow_gate(self):
        workflow = (self.root/'.github/workflows/pages.yml').read_text()
        gate = 'python docs-src/verify-release-content.py'
        self.assertEqual(workflow.count(gate), 1)
        self.assertLess(workflow.index(gate), workflow.index('python -m mkdocs build --strict'))
        self.assertLess(workflow.index(gate), workflow.index('actions/upload-pages-artifact@'))
        (self.root/'release-review/mac-codex.md').unlink()
        self.rejected('Release review file set differs')

    def test_pending_and_missing_roles(self):
        for role in mod.REPORTS:
            with self.subTest(role=role):
                original = self.record['reviews'].pop(role)
                self.save(); self.rejected('Incomplete release reviews')
                self.record['reviews'][role] = original
        self.record['status'] = 'pending'; self.save()
        self.rejected('Current release approval is incomplete')

    def test_required_mac_checks_not_followup(self):
        for check in mod.CHECKS['mac_codex']:
            with self.subTest(check=check):
                self.record['reviews']['mac_codex']['checks'][check] = 'followup'
                self.save(); self.rejected('Required release check not passed: mac_codex')
                self.record['reviews']['mac_codex']['checks'][check] = 'pass'

    def test_report_and_review_target(self):
        self.baseline()
        p = self.root/'release-review/semantic-review.md'
        raw = p.read_bytes(); p.write_bytes(raw+b'changed')
        self.rejected('Release report changed: semantic')
        p.write_bytes(raw)
        self.record['reviews']['semantic']['snapshot_sha256'] = '0'*64
        self.save(); self.rejected('Release review snapshot mismatch: semantic')

    def test_exact_report_set_and_symlinks(self):
        p = self.root/'release-review/extra.md'; p.write_text('extra')
        self.rejected('Release review file set differs'); p.unlink()
        p = self.root/'release-review/outbound-review.md'
        target = self.root/'outside.md'; target.write_bytes(p.read_bytes())
        p.unlink(); p.symlink_to(target)
        self.rejected('Symlink')

    def test_review_directory_symlink(self):
        p = self.root/'release-review'; target = self.root/'reports'
        p.rename(target); p.symlink_to(target, target_is_directory=True)
        self.rejected('Symlink ancestor')

    def test_record_symlink(self):
        p = self.root/'release-evidence.json'; target = self.root/'other.json'
        p.rename(target); p.symlink_to(target)
        self.rejected('Symlink')

    def test_schema_duplicates_dates_and_types(self):
        original = copy.deepcopy(self.record)
        for key, value, message in [('schema', True, 'schema'), ('unexpected', 1, 'record keys')]:
            self.record = copy.deepcopy(original); self.record[key] = value
            self.save(); self.rejected(message)
        self.record = copy.deepcopy(original)
        self.record['reviews']['semantic']['reviewed_at_utc'] = '2026-02-31T00:00:00Z'
        self.save(); self.rejected('timestamp')
        self.save()
        p = self.root/'release-evidence.json'
        p.write_text(p.read_text().replace('"schema": 1,', '"schema": 1, "schema": 1,'))
        self.rejected('Duplicate JSON key')

    def test_current_inputs_changed_deleted_added_moved(self):
        self.baseline()
        p = self.root/'site/index.html'; raw = p.read_bytes()
        p.write_bytes(raw+b'changed'); self.rejected('Input file changed: site/index.html')
        p.write_bytes(raw); moved = p.with_name('moved.html'); p.rename(moved)
        self.rejected('Input file set differs'); moved.rename(p)
        added = self.root/'docs-src/extra.txt'; added.write_text('added')
        self.rejected('Input file set differs'); added.unlink()
        p.unlink(); self.rejected('Input file set differs')

    def test_page_manifest_and_snapshot_rebinding_cannot_reuse_approval(self):
        self.baseline()
        p = self.root/'docs-src/content/ai-troubleshooting.md'
        p.write_bytes(p.read_bytes()+b'\nchanged\n')
        manifest_path = self.root/'docs-src/content-manifest.json'
        manifest = json.loads(manifest_path.read_text())
        manifest['pages']['ai-troubleshooting.md']['page_sha256'] = mod.sha(p.read_bytes())
        self.write(manifest_path, manifest)
        snapshot = json.loads(self.snapshot_path.read_text())
        snapshot['files'] = mod.inventory.collect(self.root)
        snapshot['manifest_sha256'] = snapshot['files']['docs-src/content-manifest.json']
        self.write(self.snapshot_path, snapshot)
        self.rejected('Release approval snapshot mismatch')
        # Even rebinding synthetic approval cannot bypass the old hard-bound delta.
        self.record['snapshot_sha256'] = mod.sha(self.snapshot_path.read_bytes())
        for review in self.record['reviews'].values():
            review['snapshot_sha256'] = self.record['snapshot_sha256']
        self.save(); self.rejected('Historical pending verification failed')

    def test_old_flag_and_legacy_approval_rejected_after_recapture(self):
        for field in ('flag', 'legacy_review'):
            with self.subTest(field=field):
                path = self.root/('docs-src/content-manifest.json' if field == 'flag' else 'docs-src/link-review-evidence.json')
                raw = path.read_bytes(); data = json.loads(raw)
                if field == 'flag': data['semantic_links_reviewed'] = True
                else: data['implementation_review']['status'] = 'approved'
                self.write(path, data)
                snapshot = json.loads(self.snapshot_path.read_text())
                snapshot['files'] = mod.inventory.collect(self.root)
                self.write(self.snapshot_path, snapshot)
                self.record['snapshot_sha256'] = mod.sha(self.snapshot_path.read_bytes()); self.save()
                self.rejected('closed semantic gate' if field == 'flag' else 'Legacy review must remain pending')
                path.write_bytes(raw)

    def test_child_nonzero_timeout_oserror_fail_closed(self):
        for error in (subprocess.CalledProcessError(7, ['test']), subprocess.TimeoutExpired(['test'], 180), OSError('test')):
            with self.subTest(error=type(error).__name__):
                with patch.object(mod.subprocess, 'run', side_effect=error):
                    self.rejected('Historical pending verification failed')

    def test_no_success_if_input_changes_during_child(self):
        def change(root):
            p = root/'site/index.html'; p.write_bytes(p.read_bytes()+b'changed')
        with patch.object(mod, 'run_pending', side_effect=change):
            self.rejected('Input file changed: site/index.html')

    def test_baseline_generator_and_checks(self):
        self.record['baseline_snapshot_sha256'] = '0'*64
        self.save(); self.rejected('baseline snapshot changed')
        self.record['baseline_snapshot_sha256'] = mod.BASELINE
        self.record['generator_sha256'] = '0'*64
        self.save(); self.rejected('Release generator mismatch')


if __name__ == '__main__':
    unittest.main()
