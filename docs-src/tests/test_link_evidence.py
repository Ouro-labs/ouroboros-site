import copy
import importlib.util
import hashlib
import json
from pathlib import Path
import unittest
import tempfile

path = Path(__file__).resolve().parents[1] / 'link_evidence.py'
spec = importlib.util.spec_from_file_location('link_evidence', path)
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

class LinkEvidenceTests(unittest.TestCase):
    def setUp(self):
        names = ('en/troubleshooting.md', 'first-run-detail.md', 'routing-detail.md', 'architecture-map-public.md')
        self.manifest = {'semantic_links_reviewed': False, 'pages': {
            name: {'source_sha256': 'a'*64, 'page_sha256': 'b'*64} for name in names}, 'assets': {}}
        restored=copy.deepcopy(self.manifest); chain=[]
        for name in names:
            step={'page':name, 'current_source_sha256':'a'*64, 'current_page_sha256':'b'*64,
                  'previous_source_sha256':'c'*64, 'previous_page_sha256':'d'*64}
            restored['pages'][name]['source_sha256']='c'*64
            restored['pages'][name]['page_sha256']='d'*64
            step['previous_manifest_sha256']=hashlib.sha256((json.dumps(restored,ensure_ascii=False,indent=2)+'\n').encode()).hexdigest()
            chain.append(step)
        self.evidence = {
            'schema': 1, 'scope': mod.EXPECTED_SCOPE, 'group_count': 92,
            'manifest_sha256': mod.manifest_digest(self.manifest), 'generator_sha256': 'b'*64,
            'reviewed_generator_sha256': 'a'*64, 'delta_reversions': chain,
            'reviewed_base_manifest_sha256': chain[-1]['previous_manifest_sha256'],
            'evidence_sha256': {key: 'c'*64 for key in mod.EVIDENCE_KEYS},
            'public_review_sha256': {key: 'c'*64 for key in mod.PUBLIC_REVIEW_FILES},
            'outbound_delta_review': {'status':'pending'},
            'verification_sha256': {'link_evidence.py':'e'*64, 'verify-content.py':'e'*64, 'workspace-verifier':'e'*64},
            'static_content_sha256': {name:'e'*64 for name in mod.STATIC_CONTENT},
            'site_dependencies': {'site/assets/learn/ooo-interview.gif': 'd'*64},
            'implementation_review': {'status': 'pending', 'reviewer': None, 'reviewed_at_utc': None},
        }
    def test_pending_does_not_open_gate(self):
        mod.validate(self.manifest, self.evidence, require_approved=False)
        with self.assertRaises(ValueError): mod.validate(self.manifest, self.evidence)
    def test_changed_page_or_evidence_is_rejected(self):
        changed=copy.deepcopy(self.manifest); changed['pages']['first-run-detail.md']['page_sha256']='e'*64
        with self.assertRaises(ValueError): mod.validate(changed, self.evidence, require_approved=False)
        changed=copy.deepcopy(self.evidence); del changed['evidence_sha256']['review_a']
        with self.assertRaises(ValueError): mod.validate(self.manifest, changed, require_approved=False)
    def test_unlisted_file_and_symlink_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            page=b'example'; digest=hashlib.sha256(page).hexdigest()
            manifest={'pages':{'index.md':{'page_sha256':digest}},'assets':{}}
            static={name:digest for name in mod.STATIC_CONTENT}
            evidence={'static_content_sha256':static}
            for name in ['index.md', *static]:
                p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(page)
            mod.verify_content_tree(root,manifest,evidence)
            link=root.parent/(root.name + '-link')
            link.symlink_to(root, target_is_directory=True)
            try:
                with self.assertRaises(ValueError): mod.verify_content_tree(link,manifest,evidence)
            finally:
                link.unlink()
            extra=root/'unlisted-probe.txt';extra.write_text('not reviewed')
            with self.assertRaises(ValueError):mod.verify_content_tree(root,manifest,evidence)
            extra.unlink()
            (root/'escape').symlink_to(root/'index.md')
            with self.assertRaises(ValueError):mod.verify_content_tree(root,manifest,evidence)
    def test_delta_chain_tampering_is_rejected(self):
        changed=copy.deepcopy(self.evidence)
        changed['delta_reversions'][0]['previous_source_sha256']='f'*64
        with self.assertRaises(ValueError): mod.validate(self.manifest, changed, require_approved=False)
        changed=copy.deepcopy(self.evidence); changed['delta_reversions'].pop()
        with self.assertRaises(ValueError): mod.validate(self.manifest, changed, require_approved=False)
    def test_true_flag_alone_does_not_approve(self):
        changed=copy.deepcopy(self.manifest); changed['semantic_links_reviewed']=True
        with self.assertRaises(ValueError): mod.validate(changed, self.evidence)
    def test_synthetic_approved_evidence_requires_snapshot(self):
        changed=copy.deepcopy(self.manifest); changed['semantic_links_reviewed']=True
        evidence=copy.deepcopy(self.evidence)
        evidence['implementation_review']={'status':'approved','reviewer':'independent test',
            'reviewed_at_utc':'2026-11-07T00:00:00Z','evidence_sha256':'f'*64}
        with self.assertRaises(ValueError): mod.validate(changed,evidence)
        evidence['outbound_delta_review']={'status':'approved','reviewer':'independent test',
            'reviewed_at_utc':'2026-11-07T00:00:00Z','evidence_sha256':'f'*64}
        mod.validate(changed,evidence)
        changed['pages']['first-run-detail.md']['page_sha256']='e'*64
        with self.assertRaises(ValueError): mod.validate(changed,evidence)

if __name__ == '__main__': unittest.main()
