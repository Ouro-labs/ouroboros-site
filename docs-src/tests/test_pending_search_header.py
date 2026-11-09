"""Focused tamper tests for pending search header evidence binding."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

DOCS = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(DOCS))
spec = importlib.util.spec_from_file_location('pending_guides_header', DOCS/'verify-pending-guides.py')
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


class PendingSearchHeaderTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)/'docs-src'
        shutil.copytree(DOCS, self.root, ignore=shutil.ignore_patterns('__pycache__'))
        for relative in ('content/assets/site.css', 'tests/test_search_overlay.py'):
            source=DOCS/relative
            target=self.root.parent/'docs-src'/relative
            target.write_bytes(source.read_bytes())

    def record(self):
        return json.loads((self.root/'pending-search-header.json').read_text())

    def verify(self):
        overlay=json.loads((self.root/'pending-search-overlay.json').read_text())
        summary=(self.root/'pending-search-overlay-review.md').read_bytes()
        return verifier.verify_search_header(self.root,overlay)

    def rebind_css_evidence(self):
        css_path=self.root.parent/'docs-src/content/assets/site.css'
        header_path=self.root/'pending-search-header.json'
        summary_path=self.root/'pending-search-header-review.md'
        header=json.loads(header_path.read_text())
        old=header['files']['docs-src/content/assets/site.css']
        new=hashlib.sha256(css_path.read_bytes()).hexdigest()
        header['files']['docs-src/content/assets/site.css']=new
        summary=summary_path.read_bytes().replace(old.encode(),new.encode())
        header['summary_sha256']=hashlib.sha256(summary).hexdigest()
        summary_path.write_bytes(summary)
        header_path.write_text(json.dumps(header,ensure_ascii=False,indent=2)+'\n')

    def rebind_test_evidence(self, test_bytes):
        test_path=self.root.parent/'docs-src/tests/test_search_overlay.py'
        header_path=self.root/'pending-search-header.json'
        summary_path=self.root/'pending-search-header-review.md'
        header=json.loads(header_path.read_text())
        old=header['files']['docs-src/tests/test_search_overlay.py']
        new=hashlib.sha256(test_bytes).hexdigest()
        header['files']['docs-src/tests/test_search_overlay.py']=new
        summary=summary_path.read_bytes().replace(old.encode(),new.encode())
        header['summary_sha256']=hashlib.sha256(summary).hexdigest()
        test_path.write_bytes(test_bytes)
        summary_path.write_bytes(summary)
        header_path.write_text(json.dumps(header,ensure_ascii=False,indent=2)+'\n')

    def reject(self, message):
        with self.assertRaisesRegex(ValueError,message): self.verify()

    def test_valid_pending_header_restores_overlay_hashes(self):
        _,css,test=self.verify()
        overlay=json.loads((self.root/'pending-search-overlay.json').read_text())
        self.assertEqual(hashlib.sha256(css).hexdigest(),'28051bf0e816ef42a2da210a9b6387c247abecae686d9d8a6a9228a4b299661c')
        self.assertEqual(hashlib.sha256(test).hexdigest(),overlay['files']['docs-src/tests/test_search_overlay.py'])

    def test_missing_header_record_rejected(self):
        (self.root/'pending-search-header.json').unlink()
        self.reject('Evidence input is not a regular non-symlink file: pending-search-header.json')

    def test_missing_header_summary_rejected(self):
        (self.root/'pending-search-header-review.md').unlink()
        self.reject('Evidence input is not a regular non-symlink file: pending-search-header-review.md')

    def test_duplicate_css_block_rejected(self):
        p=self.root.parent/'docs-src/content/assets/site.css'
        p.write_bytes(p.read_bytes()+verifier.SEARCH_HEADER_CSS_BLOCK)
        self.rebind_css_evidence()
        self.reject('Search header CSS block missing, duplicated, or moved')

    def test_moved_css_block_rejected(self):
        p=self.root.parent/'docs-src/content/assets/site.css'; data=p.read_bytes()
        block=verifier.SEARCH_HEADER_CSS_BLOCK
        p.write_bytes(data.replace(block,b'',1)+block)
        self.rebind_css_evidence()
        self.reject('Search header CSS block missing, duplicated, or moved')

    def test_missing_css_block_rejected(self):
        p=self.root.parent/'docs-src/content/assets/site.css'; data=p.read_bytes()
        p.write_bytes(data.replace(verifier.SEARCH_HEADER_CSS_BLOCK,b'',1))
        self.rebind_css_evidence()
        self.reject('Search header CSS block missing, duplicated, or moved')

    def test_test_file_tamper_rejected(self):
        p=self.root.parent/'docs-src/tests/test_search_overlay.py'
        p.write_bytes(p.read_bytes()+b'# tampered\n')
        self.reject('Search header test changed')

    def test_test_methods_moved_outside_class_rejected_after_rebinding(self):
        p=self.root.parent/'docs-src/tests/test_search_overlay.py'; data=p.read_bytes()
        block=verifier.SEARCH_HEADER_TEST_METHODS
        self.assertEqual(data.count(block),1)
        moved=data.replace(block,b'',1)
        class_at=moved.index(b'class SearchOverlayTest(unittest.TestCase):')
        moved=moved[:class_at]+block+b'\n'+moved[class_at:]
        self.rebind_test_evidence(moved)
        self.reject('Search header test methods moved')

    def test_search_header_input_parent_symlink_rejected(self):
        original=self.root.parent/'docs-src'
        redirected=self.root.parent/'redirected-docs-src'
        original.rename(redirected)
        original.symlink_to(redirected, target_is_directory=True)
        self.reject('Search header path has symlink ancestor')

    def test_header_status_cannot_open_approval(self):
        p=self.root/'pending-search-header.json'; data=self.record(); data['status']='approved'
        p.write_text(json.dumps(data))
        self.reject('Search header status changed')

    def test_publication_gate_must_remain_closed(self):
        with self.assertRaisesRegex(ValueError,'Pending extension requires closed gate'):
            verifier.verify_pending_gate({'semantic_links_reviewed':True},{'status':'pending'})
        with self.assertRaisesRegex(ValueError,'Pending extension requires closed gate'):
            verifier.verify_pending_gate({'semantic_links_reviewed':False},{'status':'approved'})

    def test_drawer_modification_rejected_by_restore_helper(self):
        data=(DOCS/'content/assets/ouro-theme.js').read_bytes()
        modified=data.replace(b'button.focus();', b'button.blur();', 1)
        self.assertNotEqual(data, modified)
        with self.assertRaisesRegex(ValueError, 'Search drawer block changed or moved'):
            verifier.restore_search_javascript(modified, 'unused')

    def test_overlay_record_change_rejected(self):
        p=self.root/'pending-search-overlay.json'; p.write_bytes(p.read_bytes()+b' ')
        self.reject('Search header overlay record changed')

    def test_summary_change_rejected(self):
        p=self.root/'pending-search-header-review.md'; p.write_bytes(p.read_bytes()+b'changed')
        self.reject('Search header summary changed')


if __name__ == '__main__': unittest.main()
