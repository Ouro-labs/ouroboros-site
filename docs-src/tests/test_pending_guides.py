import importlib.util
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
spec = importlib.util.spec_from_file_location('pending_guides', ROOT/'verify-pending-guides.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class PendingGuidesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)/'docs-src'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('__pycache__'))
        (self.root.parent/'site').mkdir();shutil.copy2(ROOT.parent/'site/llms.txt', self.root.parent/'site/llms.txt');shutil.copy2(ROOT.parent/'site/index.html', self.root.parent/'site/index.html')
    def rejected(self, message):
        if self._testMethodName.startswith('test_forged_') or self._testMethodName in ('test_changed_manifest','test_translated_recovery_forged_hash'): message = 'Diagnostics version manifest or pending status changed'
        with self.assertRaisesRegex(ValueError, message): mod.verify(self.root)
    def test_baseline(self): mod.verify(self.root)
    def test_landing_summary_tamper(self):
        (self.root/'pending-landing-review.md').write_text('changed');self.rejected('Landing summary changed')
    def test_landing_prior_tamper(self):
        p=self.root/'pending-landing.json';e=json.loads(p.read_text());e['prior_home_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Landing prior home mismatch')
    def test_landing_evidence_symlink(self):
        p=self.root/'pending-landing.json';p.unlink();p.symlink_to(self.root/'pending-home.json');self.rejected('Evidence input is not a regular non-symlink file')
    def test_diagnostics_version_summary_tamper(self):
        (self.root/'pending-diagnostics-version-review.md').write_text('changed');self.rejected('Diagnostics version summary changed')
    def test_diagnostics_version_prior_tamper(self):
        p=self.root/'pending-diagnostics-version.json';e=json.loads(p.read_text());e['pages']['ai-troubleshooting.md']['prior']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Diagnostics version snapshot chain mismatch')
    def test_diagnostics_version_symlink(self):
        p=self.root/'pending-diagnostics-version.json';p.unlink();p.symlink_to(self.root/'pending-venv-direct.json');self.rejected('Evidence input is not a regular non-symlink file')
    def test_venv_direct_summary_tamper(self):
        (self.root/'pending-venv-direct-review.md').write_text('changed');self.rejected('Venv direct summary changed')
    def test_venv_direct_prior_tamper(self):
        p=self.root/'pending-venv-direct.json';e=json.loads(p.read_text());e['pages']['quickstart.md']['prior']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Venv direct snapshot chain mismatch')
    def test_venv_direct_symlink(self):
        p=self.root/'pending-venv-direct.json';p.unlink();p.symlink_to(self.root/'pending-trace-warning.json');self.rejected('Evidence input is not a regular non-symlink file')
    def test_trace_warning_summary_tamper(self):
        (self.root/'pending-trace-warning-review.md').write_text('changed');self.rejected('Trace warning summary changed')
    def test_trace_warning_prior_tamper(self):
        p=self.root/'pending-trace-warning.json';e=json.loads(p.read_text());e['pages']['harness-traces-guide.md']['prior']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Trace warning snapshot chain mismatch')
    def test_trace_warning_symlink(self):
        p=self.root/'pending-trace-warning.json';p.unlink();p.symlink_to(self.root/'pending-megacode-warning.json');self.rejected('Evidence input is not a regular non-symlink file')
    def test_megacode_warning_summary_tamper(self):
        (self.root/'pending-megacode-warning-review.md').write_text('changed');self.rejected('Megacode warning summary changed')
    def test_megacode_warning_prior_tamper(self):
        p=self.root/'pending-megacode-warning.json';e=json.loads(p.read_text());e['pages']['megacode-guide.md']['prior']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Megacode warning snapshot chain mismatch')
    def test_megacode_warning_symlink(self):
        p=self.root/'pending-megacode-warning.json';p.unlink();p.symlink_to(self.root/'pending-seed-order.json');self.rejected('Evidence input is not a regular non-symlink file')
    def test_seed_order_summary_tamper(self):
        (self.root/'pending-seed-order-review.md').write_text('changed');self.rejected('Seed order summary changed')
    def test_seed_order_prior_tamper(self):
        p=self.root/'pending-seed-order.json';e=json.loads(p.read_text());e['pages']['seed-guide.md']['prior']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Seed order snapshot chain mismatch')
    def test_seed_order_evidence_symlink(self):
        p=self.root/'pending-seed-order.json';p.unlink();p.symlink_to(self.root/'pending-descriptions.json');self.rejected('Evidence input is not a regular non-symlink file')
    def test_seed_order_forged_current_source(self):
        mpath=self.root/'content-manifest.json';ppath=self.root/'pending-seed-order.json';m=json.loads(mpath.read_text());p=json.loads(ppath.read_text());name='seed-guide.md'
        m['pages'][name]['source_sha256']='a'*64;p['pages'][name]['current']['source_sha256']='a'*64;mpath.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');p['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ppath.write_text(json.dumps(p));self.rejected('Diagnostics version manifest or pending status changed')
    def test_descriptions_summary_tamper(self):
        (self.root/'pending-descriptions-review.md').write_text('changed');self.rejected('Descriptions summary changed')
    def test_descriptions_prior_tamper(self):
        p=self.root/'pending-descriptions.json';e=json.loads(p.read_text());e['pages']['index.md']['prior']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Descriptions snapshot chain mismatch')
    def test_descriptions_evidence_symlink(self):
        p=self.root/'pending-descriptions.json';p.unlink();p.symlink_to(self.root/'pending-preflight.json');self.rejected('Evidence input is not a regular non-symlink file')
    def test_worktree_input_forged_current_source(self):
        mpath=self.root/'content-manifest.json';ppath=self.root/'pending-worktree-input.json'
        m=json.loads(mpath.read_text());p=json.loads(ppath.read_text());name='existing-project-detail.md'
        m['pages'][name]['source_sha256']='a'*64;p['pages'][name]['current']['source_sha256']='a'*64
        mpath.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');p['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ppath.write_text(json.dumps(p))
        self.rejected('Diagnostics version manifest or pending status changed')
    def test_worktree_input_summary_tamper(self):
        (self.root/'pending-worktree-input-review.md').write_text('changed');self.rejected('Worktree input summary changed')
    def test_worktree_input_prior_tamper(self):
        p=self.root/'pending-worktree-input.json';e=json.loads(p.read_text());e['pages']['existing-project-detail.md']['prior']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Worktree input snapshot chain mismatch')
    def test_worktree_input_symlink(self):
        p=self.root/'pending-worktree-input.json';p.unlink();p.symlink_to(self.root/'pending-preflight.json');self.rejected('Evidence input is not a regular non-symlink file')
    def test_preflight_summary_tamper(self):
        (self.root/'pending-preflight-review.md').write_text('changed');self.rejected('Preflight summary changed')
    def test_preflight_prior_tamper(self):
        p=self.root/'pending-preflight.json';e=json.loads(p.read_text());e['pages']['index.md']['prior']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Preflight snapshot chain mismatch')
    def test_preflight_evidence_symlink(self):
        p=self.root/'pending-preflight.json';p.unlink();p.symlink_to(self.root/'pending-translated-recovery.json');self.rejected('Evidence input is not a regular non-symlink file')
    def test_changed_worktree_summary(self):
        (self.root/'pending-worktree-review.md').write_text('altered');self.rejected('Worktree summary changed')
    def test_changed_worktree_chain(self):
        p=self.root/'pending-worktree.json';e=json.loads(p.read_text());e['pages']['quickstart.md']['prior']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Worktree snapshot chain mismatch')
    def test_changed_search_summary(self):
        (self.root/'pending-search-review.md').write_text('altered');self.rejected('Search summary changed')
    def test_changed_search_file(self):
        (self.root/'augment-search.py').write_text('altered');self.rejected('Search file changed')
    def test_changed_search_chain(self):
        p=self.root/'pending-search.json';e=json.loads(p.read_text());e['pages']['quickstart.md']['prior']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Search snapshot chain mismatch')
    def test_changed_search_prior_js(self):
        p=self.root/'pending-search.json';e=json.loads(p.read_text());e['prior_js_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Search prior JS mismatch')
    def test_changed_permissions_summary(self):
        (self.root/'pending-permissions-review.md').write_text('altered');self.rejected('Permissions summary changed')
    def test_changed_permissions_chain(self):
        p=self.root/'pending-permissions.json';e=json.loads(p.read_text());e['pages']['quickstart.md']['prior']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Permissions snapshot chain mismatch: prior')
    def test_changed_details_summary(self):
        (self.root/'pending-details-review.md').write_text('altered');self.rejected('Details summary changed')
    def test_changed_details_chain(self):
        p=self.root/'pending-details.json';e=json.loads(p.read_text());e['pages']['quickstart.md']['prior']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Details snapshot chain mismatch')
    def test_missing_details_generator_hash(self):
        p=self.root/'pending-details.json';e=json.loads(p.read_text());e['generator_sha256']='bad';p.write_text(json.dumps(e));self.rejected('Details generator hash missing')
    def test_changed_accessibility_summary(self):
        (self.root/'pending-accessibility-review.md').write_text('altered');self.rejected('Accessibility summary changed')
    def test_search_focus_status_not_approved(self):
        p=self.root/'pending-search-focus.json';e=json.loads(p.read_text());e['status']='approved';p.write_text(json.dumps(e))
        self.rejected('Search focus status changed')

    def test_search_focus_prior_css_mismatch(self):
        p=self.root/'pending-search-focus.json';e=json.loads(p.read_text());e['prior_css_sha256']='0'*64;p.write_text(json.dumps(e))
        self.rejected('Search focus prior CSS mismatch')

    def test_changed_accessibility_css(self):
        (self.root/'content/assets/site.css').write_text('altered');self.rejected('Accessibility file changed')
    def test_accessibility_css_symlink(self):
        p=self.root/'content/assets/site.css';p.unlink();p.symlink_to(self.root/'content/assets/ouro-theme.js');self.rejected('Accessibility file changed')
    def test_changed_accessibility_prior_css(self):
        p=self.root/'pending-accessibility.json';e=json.loads(p.read_text());e['prior_css_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Accessibility prior CSS mismatch')
    def test_changed_evaluation_summary(self):
        (self.root/'pending-evaluation-review.md').write_text('altered');self.rejected('Evaluation summary changed')
    def test_changed_evaluation_chain(self):
        p=self.root/'pending-evaluation.json';e=json.loads(p.read_text());e['pages']['quickstart.md']['prior']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Evaluation snapshot chain mismatch')
    def test_changed_discovery_summary(self):
        (self.root/'pending-discovery-review.md').write_text('altered');self.rejected('Discovery summary changed')
    def test_changed_discovery_main(self):
        (self.root/'overrides/main.html').write_text('altered');self.rejected('Home file changed')
    def test_changed_discovery_llms(self):
        (self.root.parent/'site/llms.txt').write_text('altered');self.rejected('AI manual file changed')
    def test_discovery_llms_symlink(self):
        p=self.root.parent/'site/llms.txt';p.unlink();p.symlink_to(self.root/'overrides/main.html');self.rejected('AI manual file changed')
    def test_changed_discovery_prior_main(self):
        p=self.root/'pending-discovery.json';e=json.loads(p.read_text());e['prior_main_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Discovery prior main mismatch')
    def test_changed_locale_summary(self):
        (self.root/'pending-locale-review.md').write_text('altered');self.rejected('Locale summary changed')
    def test_changed_locale_file(self):
        (self.root/'overrides/partials/language.html').write_text('altered');self.rejected('Locale file changed')
    def test_locale_file_symlink(self):
        p=self.root/'overrides/partials/language.html';p.unlink();p.symlink_to(self.root/'overrides/partials/nav.html');self.rejected('Locale file changed')
    def test_changed_locale_prior_js(self):
        p=self.root/'pending-locale.json';e=json.loads(p.read_text());e['prior_js_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Locale prior JS does not match old evidence')
    def test_changed_install_summary(self):
        (self.root/'pending-install-review.md').write_text('altered');self.rejected('Installation summary changed')
    def test_changed_install_chain(self):
        p=self.root/'pending-install.json';e=json.loads(p.read_text());e['pages']['quickstart.md']['mid']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Installation snapshot chain mismatch: mid')
    def test_forged_install_source_hash(self):
        mpath=self.root/'content-manifest.json';ppath=self.root/'pending-runtime.json'
        m=json.loads(mpath.read_text());p=json.loads(ppath.read_text());m['pages']['quickstart.md']['source_sha256']='a'*64
        mpath.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');p['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ppath.write_text(json.dumps(p));hpath=self.root/'pending-home.json';h=json.loads(hpath.read_text());h['manifest_sha256']=p['manifest_sha256'];hpath.write_text(json.dumps(h))
        spath=self.root/'pending-session.json';q=json.loads(spath.read_text());q['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();spath.write_text(json.dumps(q))
        zpath=self.root/'pending-headings.json';z=json.loads(zpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();zpath.write_text(json.dumps(z))
        xpath=self.root/'pending-example.json';x=json.loads(xpath.read_text());x['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();xpath.write_text(json.dumps(x))
        ypath=self.root/'pending-interview-search.json';y=json.loads(ypath.read_text());y['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ypath.write_text(json.dumps(y))
        wpath=self.root/'pending-worktree-result.json';w=json.loads(wpath.read_text());w['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();wpath.write_text(json.dumps(w))
        vpath=self.root/'pending-seed-verification.json';v=json.loads(vpath.read_text());v['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();vpath.write_text(json.dumps(v))
        bpath=self.root/'pending-browser-example.json';z=json.loads(bpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();bpath.write_text(json.dumps(z))
        ipath=self.root/'pending-initial-commit.json';i=json.loads(ipath.read_text());i['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ipath.write_text(json.dumps(i))
        qpath=self.root/'pending-sidecar.json';q=json.loads(qpath.read_text());q['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();qpath.write_text(json.dumps(q))
        kpath=self.root/'pending-megacode-claim.json';k=json.loads(kpath.read_text());k['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();kpath.write_text(json.dumps(k))
        zpath=self.root/'pending-ko-venv.json';z=json.loads(zpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();zpath.write_text(json.dumps(z))
        tpath=self.root/'pending-translated-recovery.json';t=json.loads(tpath.read_text());t['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();tpath.write_text(json.dumps(t))
        self.rejected('Translated recovery snapshot chain mismatch')

    def test_changed_latest_summary(self):
        (self.root/'pending-latest-review.md').write_text('altered');self.rejected('Latest summary changed')
    def test_forged_latest_source_hash(self):
        mpath=self.root/'content-manifest.json';ppath=self.root/'pending-runtime.json'
        m=json.loads(mpath.read_text());p=json.loads(ppath.read_text());m['pages']['cli-reference-guide.md']['source_sha256']='a'*64
        mpath.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');p['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ppath.write_text(json.dumps(p));hpath=self.root/'pending-home.json';h=json.loads(hpath.read_text());h['manifest_sha256']=p['manifest_sha256'];hpath.write_text(json.dumps(h))
        spath=self.root/'pending-session.json';q=json.loads(spath.read_text());q['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();spath.write_text(json.dumps(q))
        zpath=self.root/'pending-headings.json';z=json.loads(zpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();zpath.write_text(json.dumps(z))
        xpath=self.root/'pending-example.json';x=json.loads(xpath.read_text());x['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();xpath.write_text(json.dumps(x))
        ypath=self.root/'pending-interview-search.json';y=json.loads(ypath.read_text());y['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ypath.write_text(json.dumps(y))
        wpath=self.root/'pending-worktree-result.json';w=json.loads(wpath.read_text());w['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();wpath.write_text(json.dumps(w))
        vpath=self.root/'pending-seed-verification.json';v=json.loads(vpath.read_text());v['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();vpath.write_text(json.dumps(v))
        bpath=self.root/'pending-browser-example.json';z=json.loads(bpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();bpath.write_text(json.dumps(z))
        ipath=self.root/'pending-initial-commit.json';i=json.loads(ipath.read_text());i['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ipath.write_text(json.dumps(i))
        qpath=self.root/'pending-sidecar.json';q=json.loads(qpath.read_text());q['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();qpath.write_text(json.dumps(q))
        kpath=self.root/'pending-megacode-claim.json';k=json.loads(kpath.read_text());k['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();kpath.write_text(json.dumps(k))
        zpath=self.root/'pending-ko-venv.json';z=json.loads(zpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();zpath.write_text(json.dumps(z))
        tpath=self.root/'pending-translated-recovery.json';t=json.loads(tpath.read_text());t['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();tpath.write_text(json.dumps(t))
        self.rejected('Translated recovery snapshot chain mismatch')

    def test_changed_latest_chain(self):
        p=self.root/'pending-latest.json';e=json.loads(p.read_text());e['pages']['cli-reference-guide.md']['mid']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Latest snapshot chain mismatch: mid')
    def test_changed_journey_summary(self):
        (self.root/'pending-journey-review.md').write_text('altered'); self.rejected('Journey summary changed')
    def test_changed_journey_chain(self):
        p=self.root/'pending-journey.json'; e=json.loads(p.read_text());e['pages']['quickstart.md']['mid']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Journey snapshot chain mismatch: mid')
    def test_changed_summary(self):
        (self.root/'pending-new-guides-review.md').write_text('altered'); self.rejected('Summary changed')
    def test_evidence_input_symlinks(self):
        for name in ('content-manifest.json','link-review-evidence.json','pending-new-guides.json','pending-new-guides-review.md','pending-journey.json','pending-journey-review.md','pending-latest.json','pending-latest-review.md','pending-install.json','pending-install-review.md','pending-locale.json','pending-locale-review.md','pending-search.json','pending-search-review.md','pending-worktree.json','pending-worktree-review.md','pending-discovery.json','pending-discovery-review.md','pending-evaluation.json','pending-evaluation-review.md','pending-accessibility.json','pending-accessibility-review.md','pending-details.json','pending-details-review.md','pending-permissions.json','pending-permissions-review.md','pending-job-diagnostic.json','pending-job-diagnostic-review.md','pending-package.json','pending-package-review.md','pending-seed.json','pending-seed-review.md','pending-interview.json','pending-interview-review.md','pending-seed-version.json','pending-seed-version-review.md','pending-runtime.json','pending-runtime-review.md','pending-home.json','pending-home-review.md','pending-session.json','pending-session-review.md','pending-headings.json','pending-headings-review.md','pending-example.json','pending-example-review.md','pending-interview-search.json','pending-interview-search-review.md','pending-worktree-result.json','pending-worktree-review-result.md','pending-seed-verification.json','pending-seed-verification-review.md','pending-browser-example.json','pending-browser-example-review.md','pending-initial-commit.json','pending-initial-commit-review.md','pending-sidecar.json','pending-sidecar-review.md','pending-megacode-claim.json','pending-megacode-claim-review.md','pending-ai-manual.json','pending-ai-manual-review.md','pending-ko-venv.json','pending-ko-venv-review.md'):
            with self.subTest(name=name):
                path=self.root/name; saved=self.root/(name+'.saved'); path.rename(saved); path.symlink_to(saved)
                try: self.rejected('Evidence input is not a regular non-symlink file')
                finally: path.unlink(); saved.rename(path)
    def test_changed_prior_evidence(self):
        (self.root/'review-evidence/groups-before.md').write_text('altered'); self.rejected('Prior public evidence changed')
    def test_forged_source_hash_in_both_records(self):
        mpath=self.root/'content-manifest.json';ppath=self.root/'pending-runtime.json'
        m=json.loads(mpath.read_text());p=json.loads(ppath.read_text());m['pages']['dashboard-guide.md']['source_sha256']='a'*64
        mpath.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');p['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ppath.write_text(json.dumps(p));hpath=self.root/'pending-home.json';h=json.loads(hpath.read_text());h['manifest_sha256']=p['manifest_sha256'];hpath.write_text(json.dumps(h))
        spath=self.root/'pending-session.json';q=json.loads(spath.read_text());q['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();spath.write_text(json.dumps(q))
        zpath=self.root/'pending-headings.json';z=json.loads(zpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();zpath.write_text(json.dumps(z))
        xpath=self.root/'pending-example.json';x=json.loads(xpath.read_text());x['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();xpath.write_text(json.dumps(x))
        ypath=self.root/'pending-interview-search.json';y=json.loads(ypath.read_text());y['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ypath.write_text(json.dumps(y))
        wpath=self.root/'pending-worktree-result.json';w=json.loads(wpath.read_text());w['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();wpath.write_text(json.dumps(w))
        vpath=self.root/'pending-seed-verification.json';v=json.loads(vpath.read_text());v['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();vpath.write_text(json.dumps(v))
        bpath=self.root/'pending-browser-example.json';z=json.loads(bpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();bpath.write_text(json.dumps(z))
        ipath=self.root/'pending-initial-commit.json';i=json.loads(ipath.read_text());i['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ipath.write_text(json.dumps(i))
        qpath=self.root/'pending-sidecar.json';q=json.loads(qpath.read_text());q['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();qpath.write_text(json.dumps(q))
        kpath=self.root/'pending-megacode-claim.json';k=json.loads(kpath.read_text());k['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();kpath.write_text(json.dumps(k))
        zpath=self.root/'pending-ko-venv.json';z=json.loads(zpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();zpath.write_text(json.dumps(z))
        tpath=self.root/'pending-translated-recovery.json';t=json.loads(tpath.read_text());t['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();tpath.write_text(json.dumps(t))
        self.rejected('Translated recovery snapshot chain mismatch')

    def test_changed_diagnostic_summary(self):
        (self.root/'pending-job-diagnostic-review.md').write_text('altered');self.rejected('Diagnostic summary changed')
    def test_changed_diagnostic_chain(self):
        p=self.root/'pending-job-diagnostic.json';e=json.loads(p.read_text());e['pages']['recovery-detail.md']['prior']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Diagnostic snapshot chain mismatch')
    def test_forged_diagnostic_source_hash(self):
        mpath=self.root/'content-manifest.json';ppath=self.root/'pending-job-diagnostic.json'
        m=json.loads(mpath.read_text());p=json.loads(ppath.read_text());name='ai-troubleshooting.md'
        m['pages'][name]['source_sha256']='a'*64;p['pages'][name]['current']['source_sha256']='a'*64
        mpath.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');p['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ppath.write_text(json.dumps(p))
        spath=self.root/'pending-session.json';q=json.loads(spath.read_text());q['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();spath.write_text(json.dumps(q))
        zpath=self.root/'pending-headings.json';z=json.loads(zpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();zpath.write_text(json.dumps(z))
        xpath=self.root/'pending-example.json';x=json.loads(xpath.read_text());x['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();xpath.write_text(json.dumps(x))
        ypath=self.root/'pending-interview-search.json';y=json.loads(ypath.read_text());y['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ypath.write_text(json.dumps(y))
        wpath=self.root/'pending-worktree-result.json';w=json.loads(wpath.read_text());w['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();wpath.write_text(json.dumps(w))
        vpath=self.root/'pending-seed-verification.json';v=json.loads(vpath.read_text());v['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();vpath.write_text(json.dumps(v))
        bpath=self.root/'pending-browser-example.json';z=json.loads(bpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();bpath.write_text(json.dumps(z))
        ipath=self.root/'pending-initial-commit.json';i=json.loads(ipath.read_text());i['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ipath.write_text(json.dumps(i))
        qpath=self.root/'pending-sidecar.json';q=json.loads(qpath.read_text());q['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();qpath.write_text(json.dumps(q))
        kpath=self.root/'pending-megacode-claim.json';k=json.loads(kpath.read_text());k['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();kpath.write_text(json.dumps(k))
        zpath=self.root/'pending-ko-venv.json';z=json.loads(zpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();zpath.write_text(json.dumps(z))
        tpath=self.root/'pending-translated-recovery.json';t=json.loads(tpath.read_text());t['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();tpath.write_text(json.dumps(t))
        self.rejected('Translated recovery snapshot chain mismatch')

    def test_changed_package_summary(self):
        (self.root/'pending-package-review.md').write_text('altered');self.rejected('Package summary changed')
    def test_changed_package_chain(self):
        p=self.root/'pending-package.json';e=json.loads(p.read_text());e['pages']['check-package-detail.md']['prior']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Package snapshot chain mismatch')
    def test_forged_package_source_hash(self):
        mpath=self.root/'content-manifest.json';ppath=self.root/'pending-package.json'
        m=json.loads(mpath.read_text());p=json.loads(ppath.read_text());name='check-package-detail.md'
        m['pages'][name]['source_sha256']='a'*64;p['pages'][name]['current']['source_sha256']='a'*64
        mpath.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');p['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ppath.write_text(json.dumps(p))
        spath=self.root/'pending-session.json';q=json.loads(spath.read_text());q['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();spath.write_text(json.dumps(q))
        zpath=self.root/'pending-headings.json';z=json.loads(zpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();zpath.write_text(json.dumps(z))
        xpath=self.root/'pending-example.json';x=json.loads(xpath.read_text());x['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();xpath.write_text(json.dumps(x))
        ypath=self.root/'pending-interview-search.json';y=json.loads(ypath.read_text());y['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ypath.write_text(json.dumps(y))
        wpath=self.root/'pending-worktree-result.json';w=json.loads(wpath.read_text());w['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();wpath.write_text(json.dumps(w))
        vpath=self.root/'pending-seed-verification.json';v=json.loads(vpath.read_text());v['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();vpath.write_text(json.dumps(v))
        bpath=self.root/'pending-browser-example.json';z=json.loads(bpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();bpath.write_text(json.dumps(z))
        ipath=self.root/'pending-initial-commit.json';i=json.loads(ipath.read_text());i['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ipath.write_text(json.dumps(i))
        qpath=self.root/'pending-sidecar.json';q=json.loads(qpath.read_text());q['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();qpath.write_text(json.dumps(q))
        kpath=self.root/'pending-megacode-claim.json';k=json.loads(kpath.read_text());k['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();kpath.write_text(json.dumps(k))
        zpath=self.root/'pending-ko-venv.json';z=json.loads(zpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();zpath.write_text(json.dumps(z))
        tpath=self.root/'pending-translated-recovery.json';t=json.loads(tpath.read_text());t['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();tpath.write_text(json.dumps(t))
        self.rejected('Translated recovery snapshot chain mismatch')

    def test_changed_seed_summary(self):
        (self.root/'pending-seed-review.md').write_text('altered');self.rejected('Seed summary changed')
    def test_changed_seed_chain(self):
        p=self.root/'pending-seed.json';e=json.loads(p.read_text());e['pages']['seed-guide.md']['prior']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Seed snapshot chain mismatch')
    def test_forged_seed_source_hash(self):
        mpath=self.root/'content-manifest.json';ppath=self.root/'pending-seed.json'
        m=json.loads(mpath.read_text());p=json.loads(ppath.read_text());name='seed-guide.md'
        m['pages'][name]['source_sha256']='a'*64;p['pages'][name]['current']['source_sha256']='a'*64
        mpath.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');p['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ppath.write_text(json.dumps(p))
        spath=self.root/'pending-session.json';q=json.loads(spath.read_text());q['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();spath.write_text(json.dumps(q))
        zpath=self.root/'pending-headings.json';z=json.loads(zpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();zpath.write_text(json.dumps(z))
        xpath=self.root/'pending-example.json';x=json.loads(xpath.read_text());x['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();xpath.write_text(json.dumps(x))
        ypath=self.root/'pending-interview-search.json';y=json.loads(ypath.read_text());y['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ypath.write_text(json.dumps(y))
        wpath=self.root/'pending-worktree-result.json';w=json.loads(wpath.read_text());w['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();wpath.write_text(json.dumps(w))
        vpath=self.root/'pending-seed-verification.json';v=json.loads(vpath.read_text());v['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();vpath.write_text(json.dumps(v))
        bpath=self.root/'pending-browser-example.json';z=json.loads(bpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();bpath.write_text(json.dumps(z))
        ipath=self.root/'pending-initial-commit.json';i=json.loads(ipath.read_text());i['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ipath.write_text(json.dumps(i))
        qpath=self.root/'pending-sidecar.json';q=json.loads(qpath.read_text());q['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();qpath.write_text(json.dumps(q))
        kpath=self.root/'pending-megacode-claim.json';k=json.loads(kpath.read_text());k['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();kpath.write_text(json.dumps(k))
        zpath=self.root/'pending-ko-venv.json';z=json.loads(zpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();zpath.write_text(json.dumps(z))
        tpath=self.root/'pending-translated-recovery.json';t=json.loads(tpath.read_text());t['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();tpath.write_text(json.dumps(t))
        self.rejected('Translated recovery snapshot chain mismatch')

    def test_changed_interview_summary(self):
        (self.root/'pending-interview-review.md').write_text('altered');self.rejected('Interview summary changed')
    def test_changed_interview_chain(self):
        p=self.root/'pending-interview.json';e=json.loads(p.read_text());e['pages']['interview-guide.md']['prior']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Interview snapshot chain mismatch')
    def test_forged_interview_source_hash(self):
        mpath=self.root/'content-manifest.json';ppath=self.root/'pending-interview.json'
        m=json.loads(mpath.read_text());p=json.loads(ppath.read_text());name='interview-guide.md'
        m['pages'][name]['source_sha256']='a'*64;p['pages'][name]['current']['source_sha256']='a'*64
        mpath.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');p['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ppath.write_text(json.dumps(p))
        spath=self.root/'pending-session.json';q=json.loads(spath.read_text());q['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();spath.write_text(json.dumps(q))
        zpath=self.root/'pending-headings.json';z=json.loads(zpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();zpath.write_text(json.dumps(z))
        xpath=self.root/'pending-example.json';x=json.loads(xpath.read_text());x['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();xpath.write_text(json.dumps(x))
        ypath=self.root/'pending-interview-search.json';y=json.loads(ypath.read_text());y['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ypath.write_text(json.dumps(y))
        wpath=self.root/'pending-worktree-result.json';w=json.loads(wpath.read_text());w['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();wpath.write_text(json.dumps(w))
        vpath=self.root/'pending-seed-verification.json';v=json.loads(vpath.read_text());v['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();vpath.write_text(json.dumps(v))
        bpath=self.root/'pending-browser-example.json';z=json.loads(bpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();bpath.write_text(json.dumps(z))
        ipath=self.root/'pending-initial-commit.json';i=json.loads(ipath.read_text());i['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ipath.write_text(json.dumps(i))
        qpath=self.root/'pending-sidecar.json';q=json.loads(qpath.read_text());q['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();qpath.write_text(json.dumps(q))
        kpath=self.root/'pending-megacode-claim.json';k=json.loads(kpath.read_text());k['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();kpath.write_text(json.dumps(k))
        zpath=self.root/'pending-ko-venv.json';z=json.loads(zpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();zpath.write_text(json.dumps(z))
        tpath=self.root/'pending-translated-recovery.json';t=json.loads(tpath.read_text());t['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();tpath.write_text(json.dumps(t))
        self.rejected('Translated recovery snapshot chain mismatch')

    def test_changed_seed_version_summary(self):
        (self.root/'pending-seed-version-review.md').write_text('altered');self.rejected('Seed version summary changed')
    def test_changed_seed_version_chain(self):
        p=self.root/'pending-seed-version.json';e=json.loads(p.read_text());e['pages']['seed-guide.md']['prior']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Seed version snapshot chain mismatch')
    def test_forged_seed_version_source_hash(self):
        mpath=self.root/'content-manifest.json';ppath=self.root/'pending-seed-version.json'
        m=json.loads(mpath.read_text());p=json.loads(ppath.read_text());name='seed-guide.md'
        m['pages'][name]['source_sha256']='a'*64;p['pages'][name]['current']['source_sha256']='a'*64
        mpath.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');p['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ppath.write_text(json.dumps(p))
        spath=self.root/'pending-session.json';q=json.loads(spath.read_text());q['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();spath.write_text(json.dumps(q))
        zpath=self.root/'pending-headings.json';z=json.loads(zpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();zpath.write_text(json.dumps(z))
        xpath=self.root/'pending-example.json';x=json.loads(xpath.read_text());x['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();xpath.write_text(json.dumps(x))
        ypath=self.root/'pending-interview-search.json';y=json.loads(ypath.read_text());y['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ypath.write_text(json.dumps(y))
        wpath=self.root/'pending-worktree-result.json';w=json.loads(wpath.read_text());w['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();wpath.write_text(json.dumps(w))
        vpath=self.root/'pending-seed-verification.json';v=json.loads(vpath.read_text());v['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();vpath.write_text(json.dumps(v))
        bpath=self.root/'pending-browser-example.json';z=json.loads(bpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();bpath.write_text(json.dumps(z))
        ipath=self.root/'pending-initial-commit.json';i=json.loads(ipath.read_text());i['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ipath.write_text(json.dumps(i))
        qpath=self.root/'pending-sidecar.json';q=json.loads(qpath.read_text());q['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();qpath.write_text(json.dumps(q))
        kpath=self.root/'pending-megacode-claim.json';k=json.loads(kpath.read_text());k['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();kpath.write_text(json.dumps(k))
        zpath=self.root/'pending-ko-venv.json';z=json.loads(zpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();zpath.write_text(json.dumps(z))
        tpath=self.root/'pending-translated-recovery.json';t=json.loads(tpath.read_text());t['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();tpath.write_text(json.dumps(t))
        self.rejected('Translated recovery snapshot chain mismatch')

    def test_changed_runtime_summary(self):
        (self.root/'pending-runtime-review.md').write_text('altered');self.rejected('Runtime summary changed')
    def test_changed_runtime_chain(self):
        p=self.root/'pending-runtime.json';e=json.loads(p.read_text());e['pages']['megacode-guide.md']['prior']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Runtime snapshot chain mismatch')
    def test_forged_runtime_source_hash(self):
        mpath=self.root/'content-manifest.json';ppath=self.root/'pending-runtime.json'
        m=json.loads(mpath.read_text());p=json.loads(ppath.read_text());name='megacode-guide.md'
        m['pages'][name]['source_sha256']='a'*64;p['pages'][name]['current']['source_sha256']='a'*64
        mpath.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');p['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ppath.write_text(json.dumps(p));hpath=self.root/'pending-home.json';h=json.loads(hpath.read_text());h['manifest_sha256']=p['manifest_sha256'];hpath.write_text(json.dumps(h))
        spath=self.root/'pending-session.json';q=json.loads(spath.read_text());q['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();spath.write_text(json.dumps(q))
        zpath=self.root/'pending-headings.json';z=json.loads(zpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();zpath.write_text(json.dumps(z))
        xpath=self.root/'pending-example.json';x=json.loads(xpath.read_text());x['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();xpath.write_text(json.dumps(x))
        ypath=self.root/'pending-interview-search.json';y=json.loads(ypath.read_text());y['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ypath.write_text(json.dumps(y))
        wpath=self.root/'pending-worktree-result.json';w=json.loads(wpath.read_text());w['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();wpath.write_text(json.dumps(w))
        vpath=self.root/'pending-seed-verification.json';v=json.loads(vpath.read_text());v['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();vpath.write_text(json.dumps(v))
        bpath=self.root/'pending-browser-example.json';z=json.loads(bpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();bpath.write_text(json.dumps(z))
        ipath=self.root/'pending-initial-commit.json';i=json.loads(ipath.read_text());i['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ipath.write_text(json.dumps(i))
        qpath=self.root/'pending-sidecar.json';q=json.loads(qpath.read_text());q['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();qpath.write_text(json.dumps(q))
        kpath=self.root/'pending-megacode-claim.json';k=json.loads(kpath.read_text());k['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();kpath.write_text(json.dumps(k))
        zpath=self.root/'pending-ko-venv.json';z=json.loads(zpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();zpath.write_text(json.dumps(z))
        tpath=self.root/'pending-translated-recovery.json';t=json.loads(tpath.read_text());t['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();tpath.write_text(json.dumps(t))
        self.rejected('Translated recovery snapshot chain mismatch')

    def test_changed_home_summary(self):
        (self.root/'pending-home-review.md').write_text('altered');self.rejected('Home summary changed')
    def test_changed_home_prior_template(self):
        p=self.root/'pending-home.json';e=json.loads(p.read_text());e['prior_main_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Home prior template mismatch')
    def test_changed_homepage(self):
        (self.root.parent/'site/index.html').write_text('altered');self.rejected('Home file changed')
    def test_homepage_symlink(self):
        p=self.root.parent/'site/index.html';p.unlink();p.symlink_to(self.root/'overrides/main.html');self.rejected('Home file changed')
    def test_changed_home_prior(self):
        p=self.root/'pending-home.json';e=json.loads(p.read_text());e['prior_home_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Home prior homepage changed')
    def test_changed_home_manifest_chain(self):
        p=self.root/'pending-home.json';e=json.loads(p.read_text());e['manifest_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Home manifest chain mismatch')
    def test_home_template_symlink(self):
        p=self.root/'overrides/main.html';p.unlink();p.symlink_to(self.root/'overrides/partials/nav.html');self.rejected('Home file changed')
    def test_changed_session_summary(self):
        (self.root/'pending-session-review.md').write_text('altered');self.rejected('Session summary changed')
    def test_changed_session_chain(self):
        p=self.root/'pending-session.json';e=json.loads(p.read_text());e['pages']['status-guide.md']['prior']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Session snapshot chain mismatch')
    def test_forged_session_source_hash(self):
        mpath=self.root/'content-manifest.json';ppath=self.root/'pending-session.json'
        m=json.loads(mpath.read_text());p=json.loads(ppath.read_text());name='status-guide.md'
        m['pages'][name]['source_sha256']='a'*64;p['pages'][name]['current']['source_sha256']='a'*64
        mpath.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');p['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ppath.write_text(json.dumps(p))
        zpath=self.root/'pending-headings.json';z=json.loads(zpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();zpath.write_text(json.dumps(z))
        xpath=self.root/'pending-example.json';x=json.loads(xpath.read_text());x['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();xpath.write_text(json.dumps(x))
        ypath=self.root/'pending-interview-search.json';y=json.loads(ypath.read_text());y['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ypath.write_text(json.dumps(y))
        wpath=self.root/'pending-worktree-result.json';w=json.loads(wpath.read_text());w['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();wpath.write_text(json.dumps(w))
        vpath=self.root/'pending-seed-verification.json';v=json.loads(vpath.read_text());v['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();vpath.write_text(json.dumps(v))
        bpath=self.root/'pending-browser-example.json';z=json.loads(bpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();bpath.write_text(json.dumps(z))
        ipath=self.root/'pending-initial-commit.json';i=json.loads(ipath.read_text());i['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ipath.write_text(json.dumps(i))
        qpath=self.root/'pending-sidecar.json';q=json.loads(qpath.read_text());q['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();qpath.write_text(json.dumps(q))
        kpath=self.root/'pending-megacode-claim.json';k=json.loads(kpath.read_text());k['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();kpath.write_text(json.dumps(k))
        zpath=self.root/'pending-ko-venv.json';z=json.loads(zpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();zpath.write_text(json.dumps(z))
        tpath=self.root/'pending-translated-recovery.json';t=json.loads(tpath.read_text());t['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();tpath.write_text(json.dumps(t))
        self.rejected('Translated recovery snapshot chain mismatch')

    def test_changed_headings_summary(self):
        (self.root/'pending-headings-review.md').write_text('altered');self.rejected('Headings summary changed')
    def test_changed_headings_chain(self):
        p=self.root/'pending-headings.json';e=json.loads(p.read_text());e['pages']['en/quickstart.md']['prior']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Headings snapshot chain mismatch')
    def test_forged_headings_source_hash(self):
        mpath=self.root/'content-manifest.json';ppath=self.root/'pending-headings.json'
        m=json.loads(mpath.read_text());p=json.loads(ppath.read_text());name='en/quickstart.md'
        m['pages'][name]['source_sha256']='a'*64;p['pages'][name]['current']['source_sha256']='a'*64
        mpath.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');p['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ppath.write_text(json.dumps(p))
        xpath=self.root/'pending-example.json';x=json.loads(xpath.read_text());x['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();xpath.write_text(json.dumps(x))
        ypath=self.root/'pending-interview-search.json';y=json.loads(ypath.read_text());y['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ypath.write_text(json.dumps(y))
        wpath=self.root/'pending-worktree-result.json';w=json.loads(wpath.read_text());w['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();wpath.write_text(json.dumps(w))
        vpath=self.root/'pending-seed-verification.json';v=json.loads(vpath.read_text());v['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();vpath.write_text(json.dumps(v))
        bpath=self.root/'pending-browser-example.json';z=json.loads(bpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();bpath.write_text(json.dumps(z))
        ipath=self.root/'pending-initial-commit.json';i=json.loads(ipath.read_text());i['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ipath.write_text(json.dumps(i))
        qpath=self.root/'pending-sidecar.json';q=json.loads(qpath.read_text());q['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();qpath.write_text(json.dumps(q))
        kpath=self.root/'pending-megacode-claim.json';k=json.loads(kpath.read_text());k['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();kpath.write_text(json.dumps(k))
        zpath=self.root/'pending-ko-venv.json';z=json.loads(zpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();zpath.write_text(json.dumps(z))
        tpath=self.root/'pending-translated-recovery.json';t=json.loads(tpath.read_text());t['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();tpath.write_text(json.dumps(t))
        self.rejected('Translated recovery snapshot chain mismatch')

    def test_changed_headings_hook(self):
        (self.root/'heading_labels.py').write_text('altered');self.rejected('Headings file changed')
    def test_headings_hook_symlink(self):
        p=self.root/'heading_labels.py';p.unlink();p.symlink_to(self.root/'verify-pending-guides.py');self.rejected('Headings file changed')
    def test_changed_example_summary(self):
        (self.root/'pending-example-review.md').write_text('altered');self.rejected('Example summary changed')
    def test_changed_example_chain(self):
        p=self.root/'pending-example.json';e=json.loads(p.read_text());e['pages']['seed-guide.md']['prior']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Example snapshot chain mismatch')
    def test_forged_example_source_hash(self):
        mpath=self.root/'content-manifest.json';ppath=self.root/'pending-example.json'
        m=json.loads(mpath.read_text());p=json.loads(ppath.read_text());name='todo-reference-example.md'
        m['pages'][name]['source_sha256']='a'*64;p['pages'][name]['current']['source_sha256']='a'*64
        mpath.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');p['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ppath.write_text(json.dumps(p))
        ypath=self.root/'pending-interview-search.json';y=json.loads(ypath.read_text());y['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ypath.write_text(json.dumps(y))
        wpath=self.root/'pending-worktree-result.json';w=json.loads(wpath.read_text());w['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();wpath.write_text(json.dumps(w))
        vpath=self.root/'pending-seed-verification.json';v=json.loads(vpath.read_text());v['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();vpath.write_text(json.dumps(v))
        bpath=self.root/'pending-browser-example.json';z=json.loads(bpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();bpath.write_text(json.dumps(z))
        ipath=self.root/'pending-initial-commit.json';i=json.loads(ipath.read_text());i['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ipath.write_text(json.dumps(i))
        qpath=self.root/'pending-sidecar.json';q=json.loads(qpath.read_text());q['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();qpath.write_text(json.dumps(q))
        kpath=self.root/'pending-megacode-claim.json';k=json.loads(kpath.read_text());k['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();kpath.write_text(json.dumps(k))
        zpath=self.root/'pending-ko-venv.json';z=json.loads(zpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();zpath.write_text(json.dumps(z))
        tpath=self.root/'pending-translated-recovery.json';t=json.loads(tpath.read_text());t['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();tpath.write_text(json.dumps(t))
        self.rejected('Translated recovery snapshot chain mismatch')

    def test_changed_example_config(self):
        (self.root/'mkdocs.yml').write_text('altered');self.rejected('Example file changed')
    def test_example_config_symlink(self):
        p=self.root/'mkdocs.yml';p.unlink();p.symlink_to(self.root/'verify-content.py');self.rejected('Example file changed')
    def test_changed_interview_search_summary(self):
        (self.root/'pending-interview-search-review.md').write_text('altered');self.rejected('Interview search summary changed')
    def test_changed_interview_search_chain(self):
        p=self.root/'pending-interview-search.json';e=json.loads(p.read_text());e['pages']['en/ai-troubleshooting.md']['prior']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Interview search snapshot chain mismatch')
    def test_forged_interview_search_source_hash(self):
        mpath=self.root/'content-manifest.json';ppath=self.root/'pending-interview-search.json'
        m=json.loads(mpath.read_text());p=json.loads(ppath.read_text());name='en/ai-troubleshooting.md'
        m['pages'][name]['source_sha256']='a'*64;p['pages'][name]['current']['source_sha256']='a'*64
        mpath.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');p['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ppath.write_text(json.dumps(p))
        wpath=self.root/'pending-worktree-result.json';w=json.loads(wpath.read_text());w['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();wpath.write_text(json.dumps(w))
        vpath=self.root/'pending-seed-verification.json';v=json.loads(vpath.read_text());v['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();vpath.write_text(json.dumps(v))
        bpath=self.root/'pending-browser-example.json';z=json.loads(bpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();bpath.write_text(json.dumps(z))
        ipath=self.root/'pending-initial-commit.json';i=json.loads(ipath.read_text());i['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ipath.write_text(json.dumps(i))
        qpath=self.root/'pending-sidecar.json';q=json.loads(qpath.read_text());q['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();qpath.write_text(json.dumps(q))
        kpath=self.root/'pending-megacode-claim.json';k=json.loads(kpath.read_text());k['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();kpath.write_text(json.dumps(k))
        zpath=self.root/'pending-ko-venv.json';z=json.loads(zpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();zpath.write_text(json.dumps(z))
        tpath=self.root/'pending-translated-recovery.json';t=json.loads(tpath.read_text());t['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();tpath.write_text(json.dumps(t))
        self.rejected('Translated recovery snapshot chain mismatch')

    def test_changed_worktree_result_summary(self):
        (self.root/'pending-worktree-review-result.md').write_text('altered');self.rejected('Worktree result summary changed')
    def test_changed_worktree_result_chain(self):
        p=self.root/'pending-worktree-result.json';e=json.loads(p.read_text());e['pages']['existing-project-detail.md']['prior']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Worktree result snapshot chain mismatch')
    def test_forged_worktree_result_source_hash(self):
        mpath=self.root/'content-manifest.json';ppath=self.root/'pending-worktree-result.json'
        m=json.loads(mpath.read_text());p=json.loads(ppath.read_text());name='existing-project-detail.md'
        m['pages'][name]['source_sha256']='a'*64;p['pages'][name]['current']['source_sha256']='a'*64
        mpath.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');p['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ppath.write_text(json.dumps(p))
        vpath=self.root/'pending-seed-verification.json';v=json.loads(vpath.read_text());v['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();vpath.write_text(json.dumps(v))
        bpath=self.root/'pending-browser-example.json';z=json.loads(bpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();bpath.write_text(json.dumps(z))
        ipath=self.root/'pending-initial-commit.json';i=json.loads(ipath.read_text());i['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ipath.write_text(json.dumps(i))
        qpath=self.root/'pending-sidecar.json';q=json.loads(qpath.read_text());q['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();qpath.write_text(json.dumps(q))
        kpath=self.root/'pending-megacode-claim.json';k=json.loads(kpath.read_text());k['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();kpath.write_text(json.dumps(k))
        zpath=self.root/'pending-ko-venv.json';z=json.loads(zpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();zpath.write_text(json.dumps(z))
        tpath=self.root/'pending-translated-recovery.json';t=json.loads(tpath.read_text());t['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();tpath.write_text(json.dumps(t))
        self.rejected('Translated recovery snapshot chain mismatch')

    def test_changed_seed_verification_summary(self):
        (self.root/'pending-seed-verification-review.md').write_text('altered');self.rejected('Seed verification summary changed')
    def test_changed_seed_verification_chain(self):
        p=self.root/'pending-seed-verification.json';e=json.loads(p.read_text());e['pages']['seed-guide.md']['prior']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Seed verification snapshot chain mismatch')
    def test_forged_seed_verification_source_hash(self):
        mpath=self.root/'content-manifest.json';ppath=self.root/'pending-seed-verification.json'
        m=json.loads(mpath.read_text());p=json.loads(ppath.read_text());name='seed-guide.md'
        m['pages'][name]['source_sha256']='a'*64;p['pages'][name]['current']['source_sha256']='a'*64
        mpath.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');p['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ppath.write_text(json.dumps(p))
        bpath=self.root/'pending-browser-example.json';z=json.loads(bpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();bpath.write_text(json.dumps(z))
        ipath=self.root/'pending-initial-commit.json';i=json.loads(ipath.read_text());i['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ipath.write_text(json.dumps(i))
        qpath=self.root/'pending-sidecar.json';q=json.loads(qpath.read_text());q['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();qpath.write_text(json.dumps(q))
        kpath=self.root/'pending-megacode-claim.json';k=json.loads(kpath.read_text());k['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();kpath.write_text(json.dumps(k))
        zpath=self.root/'pending-ko-venv.json';z=json.loads(zpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();zpath.write_text(json.dumps(z))
        tpath=self.root/'pending-translated-recovery.json';t=json.loads(tpath.read_text());t['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();tpath.write_text(json.dumps(t))
        self.rejected('Translated recovery snapshot chain mismatch')

    def test_changed_browser_example_summary(self):
        (self.root/'pending-browser-example-review.md').write_text('altered');self.rejected('Browser example summary changed')
    def test_changed_browser_example_chain(self):
        p=self.root/'pending-browser-example.json';e=json.loads(p.read_text());e['pages']['seed-guide.md']['prior']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Browser example snapshot chain mismatch')
    def test_forged_browser_example_source_hash(self):
        mpath=self.root/'content-manifest.json';ppath=self.root/'pending-browser-example.json'
        m=json.loads(mpath.read_text());p=json.loads(ppath.read_text());name='todo-reference-example.md'
        m['pages'][name]['source_sha256']='a'*64;p['pages'][name]['current']['source_sha256']='a'*64
        mpath.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');p['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ppath.write_text(json.dumps(p))
        ipath=self.root/'pending-initial-commit.json';i=json.loads(ipath.read_text());i['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ipath.write_text(json.dumps(i))
        qpath=self.root/'pending-sidecar.json';q=json.loads(qpath.read_text());q['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();qpath.write_text(json.dumps(q))
        kpath=self.root/'pending-megacode-claim.json';k=json.loads(kpath.read_text());k['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();kpath.write_text(json.dumps(k))
        zpath=self.root/'pending-ko-venv.json';z=json.loads(zpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();zpath.write_text(json.dumps(z))
        tpath=self.root/'pending-translated-recovery.json';t=json.loads(tpath.read_text());t['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();tpath.write_text(json.dumps(t))
        self.rejected('Translated recovery snapshot chain mismatch')

    def test_changed_initial_commit_summary(self):
        (self.root/'pending-initial-commit-review.md').write_text('altered');self.rejected('Initial commit summary changed')
    def test_changed_initial_commit_chain(self):
        p=self.root/'pending-initial-commit.json';e=json.loads(p.read_text());e['pages']['quickstart.md']['prior']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Initial commit snapshot chain mismatch')
    def test_forged_initial_commit_source_hash(self):
        mpath=self.root/'content-manifest.json';ppath=self.root/'pending-initial-commit.json'
        m=json.loads(mpath.read_text());p=json.loads(ppath.read_text());name='quickstart.md'
        m['pages'][name]['source_sha256']='a'*64;p['pages'][name]['current']['source_sha256']='a'*64
        mpath.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');p['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ppath.write_text(json.dumps(p))
        qpath=self.root/'pending-sidecar.json';q=json.loads(qpath.read_text());q['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();qpath.write_text(json.dumps(q))
        kpath=self.root/'pending-megacode-claim.json';k=json.loads(kpath.read_text());k['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();kpath.write_text(json.dumps(k))
        zpath=self.root/'pending-ko-venv.json';z=json.loads(zpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();zpath.write_text(json.dumps(z))
        tpath=self.root/'pending-translated-recovery.json';t=json.loads(tpath.read_text());t['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();tpath.write_text(json.dumps(t))
        self.rejected('Translated recovery snapshot chain mismatch')

    def test_changed_sidecar_summary(self):
        (self.root/'pending-sidecar-review.md').write_text('altered');self.rejected('Sidecar summary changed')
    def test_changed_sidecar_chain(self):
        p=self.root/'pending-sidecar.json';e=json.loads(p.read_text());e['pages']['status-guide.md']['prior']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Sidecar snapshot chain mismatch')
    def test_forged_sidecar_source_hash(self):
        mpath=self.root/'content-manifest.json';ppath=self.root/'pending-sidecar.json'
        m=json.loads(mpath.read_text());p=json.loads(ppath.read_text());name='status-guide.md'
        m['pages'][name]['source_sha256']='a'*64;p['pages'][name]['current']['source_sha256']='a'*64
        mpath.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');p['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ppath.write_text(json.dumps(p))
        kpath=self.root/'pending-megacode-claim.json';k=json.loads(kpath.read_text());k['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();kpath.write_text(json.dumps(k))
        zpath=self.root/'pending-ko-venv.json';z=json.loads(zpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();zpath.write_text(json.dumps(z))
        tpath=self.root/'pending-translated-recovery.json';t=json.loads(tpath.read_text());t['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();tpath.write_text(json.dumps(t))
        self.rejected('Translated recovery snapshot chain mismatch')

    def test_changed_megacode_claim_summary(self):
        (self.root/'pending-megacode-claim-review.md').write_text('altered');self.rejected('Megacode claim summary changed')
    def test_changed_megacode_claim_chain(self):
        p=self.root/'pending-megacode-claim.json';e=json.loads(p.read_text());e['pages']['megacode-guide.md']['prior']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Megacode claim snapshot chain mismatch')
    def test_forged_megacode_claim_source_hash(self):
        mpath=self.root/'content-manifest.json';ppath=self.root/'pending-megacode-claim.json'
        m=json.loads(mpath.read_text());p=json.loads(ppath.read_text());name='megacode-guide.md'
        m['pages'][name]['source_sha256']='a'*64;p['pages'][name]['current']['source_sha256']='a'*64
        mpath.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');p['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ppath.write_text(json.dumps(p))
        zpath=self.root/'pending-ko-venv.json';z=json.loads(zpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();zpath.write_text(json.dumps(z))
        tpath=self.root/'pending-translated-recovery.json';t=json.loads(tpath.read_text());t['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();tpath.write_text(json.dumps(t))
        self.rejected('Translated recovery snapshot chain mismatch')

    def test_changed_ai_manual_summary(self):
        (self.root/'pending-ai-manual-review.md').write_text('altered');self.rejected('AI manual summary changed')
    def test_changed_ai_manual_prior(self):
        p=self.root/'pending-ai-manual.json';e=json.loads(p.read_text());e['prior_llms_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('AI manual prior index mismatch')
    def test_changed_ai_manual_manifest_chain(self):
        p=self.root/'pending-ai-manual.json';e=json.loads(p.read_text());e['manifest_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('AI manual manifest chain mismatch')
    def test_changed_ai_manual_discovery_test(self):
        (self.root/'tests/test_ai_manual_discovery.py').write_text('altered');self.rejected('AI manual file changed')
    def test_recovery_navigation_summary_changed(self):
        (self.root/'pending-recovery-navigation-review.md').write_text('altered')
        self.rejected('Recovery navigation summary changed')
    def test_recovery_navigation_prior_changed(self):
        p=self.root/'pending-recovery-navigation.json'; e=json.loads(p.read_text()); e['pages']['quickstart.md']['prior']['source_sha256']='a'*64; p.write_text(json.dumps(e))
        self.rejected('Recovery navigation snapshot chain mismatch')
    def test_recovery_navigation_evidence_symlink(self):
        p=self.root/'pending-recovery-navigation.json'; p.unlink(); p.symlink_to(self.root/'pending-ko-venv.json')
        self.rejected('Evidence input is not a regular non-symlink file')
    def test_recovery_navigation_source_changed(self):
        p=self.root/'content/quickstart.md'; p.write_text(p.read_text()+'changed')
        self.rejected('Content hash does not match: quickstart.md')
    def test_changed_ko_venv_summary(self):
        (self.root/'pending-ko-venv-review.md').write_text('altered');self.rejected('Korean venv summary changed')
    def test_changed_ko_venv_chain(self):
        p=self.root/'pending-ko-venv.json';e=json.loads(p.read_text());e['pages']['first-run-detail.md']['prior']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Korean venv snapshot chain mismatch')
    def test_forged_ko_venv_source_hash(self):
        mpath=self.root/'content-manifest.json';ppath=self.root/'pending-ko-venv.json'
        m=json.loads(mpath.read_text());p=json.loads(ppath.read_text());name='first-run-detail.md'
        m['pages'][name]['source_sha256']='a'*64;p['pages'][name]['current']['source_sha256']='a'*64
        mpath.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');p['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ppath.write_text(json.dumps(p))
        tpath=self.root/'pending-translated-recovery.json';t=json.loads(tpath.read_text());t['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();tpath.write_text(json.dumps(t))
        self.rejected('Translated recovery snapshot chain mismatch')

    def test_translated_recovery_summary_changed(self):
        (self.root/'pending-translated-recovery-review.md').write_text('altered');self.rejected('Translated recovery summary changed')
    def test_translated_recovery_prior_changed(self):
        p=self.root/'pending-translated-recovery.json';e=json.loads(p.read_text());e['pages']['en/troubleshooting.md']['prior']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Translated recovery snapshot chain mismatch')
    def test_translated_recovery_evidence_symlink(self):
        p=self.root/'pending-translated-recovery.json';p.unlink();p.symlink_to(self.root/'pending-recovery-navigation.json');self.rejected('Evidence input is not a regular non-symlink file')
    def test_translated_recovery_source_changed(self):
        p=self.root/'content/en/troubleshooting.md';p.write_text(p.read_text()+'changed');self.rejected('Content hash does not match: en/troubleshooting.md')
    def test_translated_recovery_forged_hash(self):
        mpath=self.root/'content-manifest.json';ppath=self.root/'pending-translated-recovery.json'
        m=json.loads(mpath.read_text());p=json.loads(ppath.read_text());name='en/troubleshooting.md'
        m['pages'][name]['source_sha256']='a'*64;p['pages'][name]['current']['source_sha256']='a'*64
        mpath.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');p['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ppath.write_text(json.dumps(p))
        self.rejected('Translated recovery current metadata mismatch')
    def test_changed_manifest(self):
        with (self.root/'content-manifest.json').open('a') as f: f.write(' ')
        self.rejected('Translated recovery manifest or pending status changed')
    def test_extra_file(self):
        (self.root/'content/unlisted.txt').write_text('unreviewed'); self.rejected('Content tree differs')
    def test_missing_file(self):
        (self.root/'content/dashboard-guide.md').unlink(); self.rejected('Content tree differs')
    def test_changed_page(self):
        (self.root/'content/dashboard-guide.md').write_text('changed'); self.rejected('Content hash does not match')
    def test_symlink_file(self):
        p=self.root/'content/dashboard-guide.md';p.unlink();p.symlink_to(self.root/'content/megacode-guide.md');self.rejected('Symlink in content tree')
    def test_symlink_root(self):
        p=self.root/'content'; other=self.root/'moved';p.rename(other);p.symlink_to(other,target_is_directory=True);self.rejected('Content root is a symlink')

class SeedOrderPriorTamperTest(unittest.TestCase):
    def test_forgery_reaches_previous_boundary(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)/'docs-src';shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('__pycache__'))
            (root.parent/'site').mkdir();shutil.copy2(ROOT.parent/'site/llms.txt',root.parent/'site/llms.txt');shutil.copy2(ROOT.parent/'site/index.html',root.parent/'site/index.html')
            mpath=root/'content-manifest.json';m=json.loads(mpath.read_text());diag=json.loads((root/'pending-diagnostics-version.json').read_text())
            for name,entry in diag['pages'].items():m['pages'][name]=entry['prior']
            self.assertEqual(hashlib.sha256((json.dumps(m,ensure_ascii=False,indent=2)+'\n').encode()).hexdigest(),diag['prior_manifest_sha256'])
            outermost=json.loads((root/'pending-venv-direct.json').read_text())
            for name,entry in outermost['pages'].items():m['pages'][name]=entry['prior']
            self.assertEqual(hashlib.sha256((json.dumps(m,ensure_ascii=False,indent=2)+'\n').encode()).hexdigest(),outermost['prior_manifest_sha256'])
            trace=json.loads((root/'pending-trace-warning.json').read_text())
            for name,entry in trace['pages'].items():m['pages'][name]=entry['prior']
            self.assertEqual(hashlib.sha256((json.dumps(m,ensure_ascii=False,indent=2)+'\n').encode()).hexdigest(),trace['prior_manifest_sha256'])
            outer=json.loads((root/'pending-megacode-warning.json').read_text())
            for name,entry in outer['pages'].items():m['pages'][name]=entry['prior']
            raw=(json.dumps(m,ensure_ascii=False,indent=2)+'\n').encode();self.assertEqual(hashlib.sha256(raw).hexdigest(),outer['prior_manifest_sha256']);mpath.write_bytes(raw)
            code=(ROOT/'verify-pending-guides.py').read_text();start=code.index("    diagnostics_version = json.loads(");end=code.index("    seed_order = json.loads(",start);code=code[:start]+code[end:]
            code=code.replace("megacode_warning['prior_manifest_sha256'] != seed_order['manifest_sha256']", "sha((root/'content-manifest.json').read_bytes()) != seed_order['manifest_sha256']")
            namespace={'__file__':str(ROOT/'verify-pending-guides.py'),'__name__':'seed_order_prior_fixture'};exec(compile(code,str(ROOT/'verify-pending-guides.py'),'exec'),namespace)
            ppath=root/'pending-seed-order.json';p=json.loads(ppath.read_text());name='seed-guide.md';m['pages'][name]['source_sha256']='a'*64;p['pages'][name]['current']['source_sha256']='a'*64
            mpath.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');p['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ppath.write_text(json.dumps(p))
            with self.assertRaisesRegex(ValueError,'Seed order current metadata mismatch'):namespace['verify'](root)

class WorktreePriorTamperTest(unittest.TestCase):
    def test_forgery_reaches_previous_boundary(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)/'docs-src';shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('__pycache__'))
            (root.parent/'site').mkdir();shutil.copy2(ROOT.parent/'site/llms.txt',root.parent/'site/llms.txt');shutil.copy2(ROOT.parent/'site/index.html',root.parent/'site/index.html')
            mpath=root/'content-manifest.json';m=json.loads(mpath.read_text());diag=json.loads((root/'pending-diagnostics-version.json').read_text())
            for name,entry in diag['pages'].items():m['pages'][name]=entry['prior']
            self.assertEqual(hashlib.sha256((json.dumps(m,ensure_ascii=False,indent=2)+'\n').encode()).hexdigest(),diag['prior_manifest_sha256'])
            outermost=json.loads((root/'pending-venv-direct.json').read_text())
            for name,entry in outermost['pages'].items():m['pages'][name]=entry['prior']
            self.assertEqual(hashlib.sha256((json.dumps(m,ensure_ascii=False,indent=2)+'\n').encode()).hexdigest(),outermost['prior_manifest_sha256'])
            trace=json.loads((root/'pending-trace-warning.json').read_text())
            for name,entry in trace['pages'].items():m['pages'][name]=entry['prior']
            self.assertEqual(hashlib.sha256((json.dumps(m,ensure_ascii=False,indent=2)+'\n').encode()).hexdigest(),trace['prior_manifest_sha256'])
            outer=json.loads((root/'pending-megacode-warning.json').read_text())
            for name,entry in outer['pages'].items():m['pages'][name]=entry['prior']
            self.assertEqual(hashlib.sha256((json.dumps(m,ensure_ascii=False,indent=2)+'\n').encode()).hexdigest(),outer['prior_manifest_sha256'])
            seed_order=json.loads((root/'pending-seed-order.json').read_text())
            for name,entry in seed_order['pages'].items():m['pages'][name]=entry['prior']
            self.assertEqual(hashlib.sha256((json.dumps(m,ensure_ascii=False,indent=2)+'\n').encode()).hexdigest(),seed_order['prior_manifest_sha256'])
            descriptions=json.loads((root/'pending-descriptions.json').read_text())
            for name,entry in descriptions['pages'].items():m['pages'][name]=entry['prior']
            raw=(json.dumps(m,ensure_ascii=False,indent=2)+'\n').encode();self.assertEqual(hashlib.sha256(raw).hexdigest(),descriptions['prior_manifest_sha256']);mpath.write_bytes(raw)
            code=(ROOT/'verify-pending-guides.py').read_text();start=code.index("    diagnostics_version = json.loads(");end=code.index("    worktree_input = json.loads(",start);code=code[:start]+code[end:]
            code=code.replace("descriptions['prior_manifest_sha256'] != worktree_input['manifest_sha256']", "sha((root/'content-manifest.json').read_bytes()) != worktree_input['manifest_sha256']")
            namespace={'__file__':str(ROOT/'verify-pending-guides.py'),'__name__':'worktree_prior_fixture'};exec(compile(code,str(ROOT/'verify-pending-guides.py'),'exec'),namespace)
            ppath=root/'pending-worktree-input.json';p=json.loads(ppath.read_text());name='existing-project-detail.md';m['pages'][name]['source_sha256']='a'*64;p['pages'][name]['current']['source_sha256']='a'*64
            mpath.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');p['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ppath.write_text(json.dumps(p))
            with self.assertRaisesRegex(ValueError,'Worktree input current metadata mismatch'):namespace['verify'](root)

class TranslatedPriorTamperTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)/'docs-src';shutil.copytree(ROOT,self.root,ignore=shutil.ignore_patterns('__pycache__'))
        (self.root.parent/'site').mkdir();shutil.copy2(ROOT.parent/'site/llms.txt',self.root.parent/'site/llms.txt');shutil.copy2(ROOT.parent/'site/index.html',self.root.parent/'site/index.html')
        manifest=json.loads((self.root/'content-manifest.json').read_text())
        diag=json.loads((self.root/'pending-diagnostics-version.json').read_text())
        for name,entry in diag['pages'].items(): manifest['pages'][name]=entry['prior']
        self.assertEqual(hashlib.sha256((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()).hexdigest(),diag['prior_manifest_sha256'])
        outermost=json.loads((self.root/'pending-venv-direct.json').read_text())
        for name,entry in outermost['pages'].items(): manifest['pages'][name]=entry['prior']
        self.assertEqual(hashlib.sha256((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()).hexdigest(),outermost['prior_manifest_sha256'])
        trace=json.loads((self.root/'pending-trace-warning.json').read_text())
        for name,entry in trace['pages'].items(): manifest['pages'][name]=entry['prior']
        self.assertEqual(hashlib.sha256((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()).hexdigest(),trace['prior_manifest_sha256'])
        outer=json.loads((self.root/'pending-megacode-warning.json').read_text())
        for name,entry in outer['pages'].items(): manifest['pages'][name]=entry['prior']
        self.assertEqual(hashlib.sha256((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()).hexdigest(),outer['prior_manifest_sha256'])
        seed_order=json.loads((self.root/'pending-seed-order.json').read_text())
        for name,entry in seed_order['pages'].items(): manifest['pages'][name]=entry['prior']
        self.assertEqual(hashlib.sha256((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()).hexdigest(),seed_order['prior_manifest_sha256'])
        descriptions=json.loads((self.root/'pending-descriptions.json').read_text())
        for name,entry in descriptions['pages'].items(): manifest['pages'][name]=entry['prior']
        self.assertEqual(hashlib.sha256((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()).hexdigest(),descriptions['prior_manifest_sha256'])
        outer=json.loads((self.root/'pending-worktree-input.json').read_text())
        for name,entry in outer['pages'].items(): manifest['pages'][name]=entry['prior']
        self.assertEqual(hashlib.sha256((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()).hexdigest(),outer['prior_manifest_sha256'])
        preflight=json.loads((self.root/'pending-preflight.json').read_text())
        for name,entry in preflight['pages'].items(): manifest['pages'][name]=entry['prior']
        raw=(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()
        self.assertEqual(hashlib.sha256(raw).hexdigest(),preflight['prior_manifest_sha256'])
        (self.root/'content-manifest.json').write_bytes(raw)
        code=(ROOT/'verify-pending-guides.py').read_text()
        start=code.index("    diagnostics_version = json.loads(")
        end=code.index("    translated = json.loads(",start)
        code=code[:start]+code[end:]
        code=code.replace("preflight['prior_manifest_sha256'] != translated['manifest_sha256']", "sha((root/'content-manifest.json').read_bytes()) != translated['manifest_sha256']")
        namespace={'__file__':str(ROOT/'verify-pending-guides.py'),'__name__':'translated_prior_fixture'}
        exec(compile(code,str(ROOT/'verify-pending-guides.py'),'exec'),namespace)
        self.prior_verify=namespace['verify']
    def test_translated_forgery_prior_boundary(self):
        mpath=self.root/'content-manifest.json';ppath=self.root/'pending-translated-recovery.json'
        m=json.loads(mpath.read_text());p=json.loads(ppath.read_text());name='en/troubleshooting.md'
        m['pages'][name]['source_sha256']='a'*64;p['pages'][name]['current']['source_sha256']='a'*64
        mpath.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');p['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ppath.write_text(json.dumps(p))
        with self.assertRaisesRegex(ValueError,'Translated recovery current metadata mismatch'): self.prior_verify(self.root)

class PriorStageTamperTest(unittest.TestCase):
    """Run the real lower verifier against the reconstructed preceding snapshot.

    The new outer manifest commitment necessarily rejects mutations before they
    reach older checks. The fixture removes only that outer stage from an in-memory
    copy of the verifier, then runs unchanged lower-stage logic against the exact
    previous manifest. Production verification is never bypassed.
    """
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)/'docs-src'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('__pycache__'))
        (self.root.parent/'site').mkdir()
        shutil.copy2(ROOT.parent/'site/llms.txt', self.root.parent/'site/llms.txt')
        shutil.copy2(ROOT.parent/'site/index.html', self.root.parent/'site/index.html')
        nav = json.loads((self.root/'pending-recovery-navigation.json').read_text())
        manifest = json.loads((self.root/'content-manifest.json').read_text())
        diag = json.loads((self.root/'pending-diagnostics-version.json').read_text())
        for name, entry in diag['pages'].items(): manifest['pages'][name] = entry['prior']
        self.assertEqual(hashlib.sha256((json.dumps(manifest, ensure_ascii=False, indent=2)+'\n').encode()).hexdigest(), diag['prior_manifest_sha256'])
        outermost = json.loads((self.root/'pending-venv-direct.json').read_text())
        for name, entry in outermost['pages'].items(): manifest['pages'][name] = entry['prior']
        self.assertEqual(hashlib.sha256((json.dumps(manifest, ensure_ascii=False, indent=2)+'\n').encode()).hexdigest(), outermost['prior_manifest_sha256'])
        trace = json.loads((self.root/'pending-trace-warning.json').read_text())
        for name, entry in trace['pages'].items(): manifest['pages'][name] = entry['prior']
        self.assertEqual(hashlib.sha256((json.dumps(manifest, ensure_ascii=False, indent=2)+'\n').encode()).hexdigest(), trace['prior_manifest_sha256'])
        outer = json.loads((self.root/'pending-megacode-warning.json').read_text())
        for name, entry in outer['pages'].items(): manifest['pages'][name] = entry['prior']
        self.assertEqual(hashlib.sha256((json.dumps(manifest, ensure_ascii=False, indent=2)+'\n').encode()).hexdigest(), outer['prior_manifest_sha256'])
        seed_order = json.loads((self.root/'pending-seed-order.json').read_text())
        for name, entry in seed_order['pages'].items(): manifest['pages'][name] = entry['prior']
        self.assertEqual(hashlib.sha256((json.dumps(manifest, ensure_ascii=False, indent=2)+'\n').encode()).hexdigest(), seed_order['prior_manifest_sha256'])
        descriptions = json.loads((self.root/'pending-descriptions.json').read_text())
        for name, entry in descriptions['pages'].items(): manifest['pages'][name] = entry['prior']
        self.assertEqual(hashlib.sha256((json.dumps(manifest, ensure_ascii=False, indent=2)+'\n').encode()).hexdigest(), descriptions['prior_manifest_sha256'])
        outer = json.loads((self.root/'pending-worktree-input.json').read_text())
        for name, entry in outer['pages'].items(): manifest['pages'][name] = entry['prior']
        self.assertEqual(hashlib.sha256((json.dumps(manifest, ensure_ascii=False, indent=2)+'\n').encode()).hexdigest(), outer['prior_manifest_sha256'])
        preflight = json.loads((self.root/'pending-preflight.json').read_text())
        for name, entry in preflight['pages'].items(): manifest['pages'][name] = entry['prior']
        preflight_raw = (json.dumps(manifest, ensure_ascii=False, indent=2)+'\n').encode()
        self.assertEqual(hashlib.sha256(preflight_raw).hexdigest(), preflight['prior_manifest_sha256'])
        translated = json.loads((self.root/'pending-translated-recovery.json').read_text())
        for name, entry in translated['pages'].items(): manifest['pages'][name] = entry['prior']
        translated_raw = (json.dumps(manifest, ensure_ascii=False, indent=2)+'\n').encode()
        self.assertEqual(hashlib.sha256(translated_raw).hexdigest(), translated['prior_manifest_sha256'])
        for name, entry in nav['pages'].items(): manifest['pages'][name] = entry['prior']
        raw = (json.dumps(manifest, ensure_ascii=False, indent=2)+'\n').encode()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), nav['prior_manifest_sha256'])
        (self.root/'content-manifest.json').write_bytes(raw)
        code = (ROOT/'verify-pending-guides.py').read_text()
        start = code.index('    current_manifest = manifest\n')
        end = code.index("    ko_venv = json.loads(", start)
        code = code[:start] + '    current_manifest = manifest\n' + code[end:]
        old = "navigation['prior_manifest_sha256'] != ko_venv['manifest_sha256']"
        self.assertEqual(code.count(old), 1)
        code = code.replace(old, "sha((root/'content-manifest.json').read_bytes()) != ko_venv['manifest_sha256']")
        namespace = {'__file__': str(ROOT/'verify-pending-guides.py'), '__name__': 'prior_stage_fixture'}
        exec(compile(code, str(ROOT/'verify-pending-guides.py'), 'exec'), namespace)
        self.verify_prior = namespace['verify']
    def rejected(self, _outer_expected):
        expected = ('Korean venv current metadata mismatch' if self._testMethodName == 'test_forged_ko_venv_source_hash'
                    else 'Korean venv manifest or pending status changed' if self._testMethodName == 'test_changed_manifest'
                    else 'Korean venv snapshot chain mismatch')
        with self.assertRaisesRegex(ValueError, expected): self.verify_prior(self.root)

# Repeat every original forged-manifest case at the old lower boundary, while
# retaining its current end-to-end outer rejection test in PendingGuidesTest.
for _name in dir(PendingGuidesTest):
    if _name.startswith('test_forged_') or _name == 'test_changed_manifest':
        setattr(PriorStageTamperTest, _name, getattr(PendingGuidesTest, _name))

if __name__ == '__main__': unittest.main()
