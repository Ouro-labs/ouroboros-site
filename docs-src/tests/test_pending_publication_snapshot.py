"""Pending-only inventory defenses; fixtures never approve publication."""
import copy
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('snapshot', ROOT/'pending_publication_snapshot.py')
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

class SnapshotTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)/'fixture';self.root.mkdir()
        for d in ('site','docs-src/content','docs-src/overrides','.github/workflows'):(self.root/d).mkdir(parents=True)
        self.generator=self.root/'generator.py';self.generator.write_text('generator')
        pages={}
        for i in range(63):
            name=f'p{i}.md'; data=f'page {i}'.encode();(self.root/'docs-src/content'/name).write_bytes(data)
            pages[name]={'source':'content/'+name,'source_sha256':mod.digest(data),'page_sha256':mod.digest(data)}
        asset=b'asset';(self.root/'docs-src/content/asset.bin').write_bytes(asset)
        manifest={'format':1,'semantic_links_reviewed':False,'pages':pages,'assets':{'asset.bin':{'sha256':mod.digest(asset)}}}
        (self.root/'docs-src/content-manifest.json').write_text(json.dumps(manifest))
        evidence={'outbound_delta_review':{'status':'pending'},'implementation_review':{'status':'pending'},'static_content_sha256':{}}
        (self.root/'docs-src/link-review-evidence.json').write_text(json.dumps(evidence))
        for name in ('site/llms.txt','site/index.html','docs-src/overrides/main.html','docs-src/mkdocs.yml','.github/workflows/pages.yml'):
            (self.root/name).write_text(name)
        shortcut=self.root/'docs-src/content/assets/ouro-search-shortcut.js'
        shortcut.parent.mkdir(parents=True);shortcut.write_text('synthetic shortcut')
        (self.root/'docs-src/pending-search-shortcut.json').write_text(json.dumps({'status':'pending','files':{'docs-src/content/assets/ouro-search-shortcut.js':mod.digest(shortcut.read_bytes())}}))
        self.snapshot=mod.create(self.root,self.generator)
    def rejected(self, text):
        with self.assertRaisesRegex((ValueError,OSError),text):mod.verify(self.root,self.snapshot,self.generator)
    def test_baseline(self):self.assertGreater(mod.verify(self.root,self.snapshot,self.generator),63)
    def test_each_input_mutation(self):
        for name in ('site/llms.txt','site/index.html','docs-src/content/p0.md','docs-src/content/asset.bin','docs-src/overrides/main.html','docs-src/mkdocs.yml','.github/workflows/pages.yml'):
            with self.subTest(name=name):
                p=self.root/name;old=p.read_bytes();p.write_bytes(old+b'x')
                try:self.rejected('Input file changed')
                finally:p.write_bytes(old)
    def test_llms_change_with_unchanged_manifest_rejected(self):
        before=(self.root/'docs-src/content-manifest.json').read_bytes();(self.root/'site/llms.txt').write_text('altered')
        self.assertEqual(before,(self.root/'docs-src/content-manifest.json').read_bytes());self.rejected('Input file changed')
    def test_only_tool_test_bytecode_is_excluded(self):
        for name in ('docs-src/__pycache__','docs-src/tests/__pycache__'):
            p=self.root/name;p.mkdir(parents=True,exist_ok=True);(p/'local.pyc').write_bytes(b'bytecode')
        self.assertGreater(mod.verify(self.root,self.snapshot,self.generator),63)
        for name in ('site/__pycache__','docs-src/content/__pycache__'):
            p=self.root/name;p.mkdir();(p/'local.pyc').write_bytes(b'bytecode')
            try:self.rejected('Input file set differs')
            finally:(p/'local.pyc').unlink();p.rmdir()
    def test_test_cache_directory_symlink_rejected(self):
        p=self.root/'docs-src/tests/__pycache__';p.parent.mkdir();p.symlink_to(self.root/'site',target_is_directory=True);self.rejected('Symlink rejected')
    def test_extra_and_missing_files(self):
        extra=self.root/'site/new.txt';extra.write_text('new');self.rejected('Input file set differs');extra.unlink()
        (self.root/'docs-src/content/p0.md').unlink();self.rejected('Input file set differs')
    def test_record_removed_and_bad_hash(self):
        del self.snapshot['files']['site/llms.txt'];self.rejected('Input file set differs')
    def test_bad_hash(self):
        self.snapshot['files']['site/llms.txt']='bad';self.rejected('Invalid input hash')
    def test_noncanonical_paths(self):
        for path in ('/site/x','site/../x','site/./x','site//x','site\\x'):
            with self.subTest(path=path):
                bad=copy.deepcopy(self.snapshot);bad['files'][path]='a'*64
                with self.assertRaises(ValueError):mod.verify(self.root,bad,self.generator)
    def test_duplicate_json_key(self):
        p=self.root/'dup.json';p.write_text('{"status":"pending","status":"approved"}')
        with self.assertRaisesRegex(ValueError,'Duplicate JSON key'):mod.load_json(p)
    def test_fake_approval_and_boolean_schema_rejected(self):
        for field,value in (('status','approved'),('schema',True),('approved',True)):
            with self.subTest(field=field):
                bad=copy.deepcopy(self.snapshot);bad[field]=value
                with self.assertRaisesRegex(ValueError,'Only pending'):mod.verify(self.root,bad,self.generator)
    def test_changed_manifest_even_with_rehashed_inventory(self):
        p=self.root/'docs-src/content-manifest.json';m=json.loads(p.read_text());m['semantic_links_reviewed']=True;p.write_text(json.dumps(m));self.snapshot['files']['docs-src/content-manifest.json']=mod.digest(p.read_bytes());self.snapshot['manifest_sha256']=mod.digest(p.read_bytes());self.rejected('closed semantic gate')
    def test_legacy_approval_is_not_accepted(self):
        p=self.root/'docs-src/link-review-evidence.json';e=json.loads(p.read_text());e['outbound_delta_review']['status']='approved';p.write_text(json.dumps(e));self.snapshot['files']['docs-src/link-review-evidence.json']=mod.digest(p.read_bytes());self.rejected('Legacy review must remain pending')
    def test_manifest_page_overlap_rejected(self):
        p=self.root/'docs-src/content-manifest.json';m=json.loads(p.read_text());m['assets']['p0.md']={'sha256':m['pages']['p0.md']['page_sha256']};p.write_text(json.dumps(m));self.snapshot['files']['docs-src/content-manifest.json']=mod.digest(p.read_bytes());self.snapshot['manifest_sha256']=mod.digest(p.read_bytes());self.rejected('overlapping')
    def test_symlink_file_directory_and_root(self):
        p=self.root/'site/llms.txt';p.unlink();p.symlink_to(self.root/'site/index.html');self.rejected('Symlink rejected');p.unlink();p.write_text('site/llms.txt')
        q=self.root/'docs-src/overrides';q.rename(self.root/'docs-src/moved');q.symlink_to(self.root/'docs-src/moved',target_is_directory=True);self.rejected('Symlink rejected')
        link=Path(self.tmp.name)/'root-link';link.symlink_to(self.root,target_is_directory=True)
        with self.assertRaisesRegex(ValueError,'Symlink ancestor'):mod.verify(link,self.snapshot,self.generator)
    @unittest.skipUnless(hasattr(os,'mkfifo'),'FIFO unavailable')
    def test_fifo_rejected_before_read(self):
        os.mkfifo(self.root/'site/fifo');self.rejected('Non-regular file')
    def test_recapture_cannot_prove_review_or_identity(self):
        # A coordinated edit and recapture can agree on bytes; this is not approval.
        (self.root/'site/llms.txt').write_text('fabricated but captured')
        fabricated=mod.create(self.root,self.generator)
        self.assertGreater(mod.verify(self.root,fabricated,self.generator),63)
        self.assertEqual(fabricated['status'],'pending')
    def test_unlisted_content_rejected_even_if_inventory_is_recaptured(self):
        (self.root/'docs-src/content/unlisted.md').write_text('unreviewed')
        with self.assertRaisesRegex(ValueError,'Content file set differs'):
            mod.create(self.root,self.generator)
    def test_source_duplicate_rejected(self):
        p=self.root/'docs-src/content-manifest.json';m=json.loads(p.read_text());m['pages']['p1.md']['source']=m['pages']['p0.md']['source'];p.write_text(json.dumps(m))
        with self.assertRaisesRegex(ValueError,'Duplicate canonical source'):mod.create(self.root,self.generator)
    def test_generator_change(self):
        self.generator.write_text('changed');self.rejected('Local generator differs')

class ProductionGateTest(unittest.TestCase):
    def test_existing_publication_gate_still_blocks(self):
        env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
        result=subprocess.run([sys.executable,str(ROOT/'verify-content.py')],capture_output=True,text=True,env=env)
        self.assertNotEqual(result.returncode,0)
        self.assertIn('Manifest does not match link review snapshot',result.stdout+result.stderr)

if __name__=='__main__':unittest.main()
