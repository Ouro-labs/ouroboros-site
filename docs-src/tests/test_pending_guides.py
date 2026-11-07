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
        with self.assertRaisesRegex(ValueError, message): mod.verify(self.root)
    def test_baseline(self): mod.verify(self.root)
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
        (self.root.parent/'site/llms.txt').write_text('altered');self.rejected('Discovery file changed')
    def test_discovery_llms_symlink(self):
        p=self.root.parent/'site/llms.txt';p.unlink();p.symlink_to(self.root/'overrides/main.html');self.rejected('Discovery file changed')
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
        self.rejected('Example current metadata mismatch')

    def test_changed_latest_summary(self):
        (self.root/'pending-latest-review.md').write_text('altered');self.rejected('Latest summary changed')
    def test_forged_latest_source_hash(self):
        mpath=self.root/'content-manifest.json';ppath=self.root/'pending-runtime.json'
        m=json.loads(mpath.read_text());p=json.loads(ppath.read_text());m['pages']['cli-reference-guide.md']['source_sha256']='a'*64
        mpath.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');p['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();ppath.write_text(json.dumps(p));hpath=self.root/'pending-home.json';h=json.loads(hpath.read_text());h['manifest_sha256']=p['manifest_sha256'];hpath.write_text(json.dumps(h))
        spath=self.root/'pending-session.json';q=json.loads(spath.read_text());q['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();spath.write_text(json.dumps(q))
        zpath=self.root/'pending-headings.json';z=json.loads(zpath.read_text());z['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();zpath.write_text(json.dumps(z))
        xpath=self.root/'pending-example.json';x=json.loads(xpath.read_text());x['manifest_sha256']=hashlib.sha256(mpath.read_bytes()).hexdigest();xpath.write_text(json.dumps(x))
        self.rejected('Example snapshot chain mismatch')

    def test_changed_latest_chain(self):
        p=self.root/'pending-latest.json';e=json.loads(p.read_text());e['pages']['cli-reference-guide.md']['mid']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Latest snapshot chain mismatch: mid')
    def test_changed_journey_summary(self):
        (self.root/'pending-journey-review.md').write_text('altered'); self.rejected('Journey summary changed')
    def test_changed_journey_chain(self):
        p=self.root/'pending-journey.json'; e=json.loads(p.read_text());e['pages']['quickstart.md']['mid']['source_sha256']='a'*64;p.write_text(json.dumps(e));self.rejected('Journey snapshot chain mismatch: mid')
    def test_changed_summary(self):
        (self.root/'pending-new-guides-review.md').write_text('altered'); self.rejected('Summary changed')
    def test_evidence_input_symlinks(self):
        for name in ('content-manifest.json','link-review-evidence.json','pending-new-guides.json','pending-new-guides-review.md','pending-journey.json','pending-journey-review.md','pending-latest.json','pending-latest-review.md','pending-install.json','pending-install-review.md','pending-locale.json','pending-locale-review.md','pending-search.json','pending-search-review.md','pending-worktree.json','pending-worktree-review.md','pending-discovery.json','pending-discovery-review.md','pending-evaluation.json','pending-evaluation-review.md','pending-accessibility.json','pending-accessibility-review.md','pending-details.json','pending-details-review.md','pending-permissions.json','pending-permissions-review.md','pending-job-diagnostic.json','pending-job-diagnostic-review.md','pending-package.json','pending-package-review.md','pending-seed.json','pending-seed-review.md','pending-interview.json','pending-interview-review.md','pending-seed-version.json','pending-seed-version-review.md','pending-runtime.json','pending-runtime-review.md','pending-home.json','pending-home-review.md','pending-session.json','pending-session-review.md','pending-headings.json','pending-headings-review.md','pending-example.json','pending-example-review.md'):
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
        self.rejected('Example snapshot chain mismatch')

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
        self.rejected('Example snapshot chain mismatch')

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
        self.rejected('Example snapshot chain mismatch')

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
        self.rejected('Example current metadata mismatch')

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
        self.rejected('Example snapshot chain mismatch')

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
        self.rejected('Example current metadata mismatch')

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
        self.rejected('Example snapshot chain mismatch')

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
        self.rejected('Example snapshot chain mismatch')

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
        self.rejected('Example snapshot chain mismatch')

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
        self.rejected('Example current metadata mismatch')
    def test_changed_example_config(self):
        (self.root/'mkdocs.yml').write_text('altered');self.rejected('Example file changed')
    def test_example_config_symlink(self):
        p=self.root/'mkdocs.yml';p.unlink();p.symlink_to(self.root/'verify-content.py');self.rejected('Example file changed')
    def test_changed_manifest(self):
        with (self.root/'content-manifest.json').open('a') as f: f.write(' ')
        self.rejected('Example manifest or pending status changed')
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

if __name__ == '__main__': unittest.main()
