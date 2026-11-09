"""Crawl release entry routes and retain the published URL/anchor contract."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import unittest

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / 'site'


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.anchors, self.lang = [], set(), None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html':
            self.lang = attrs.get('lang')
        if tag == 'a' and attrs.get('href'):
            self.links.append((attrs['href'], attrs.get('lang')))
        if attrs.get('id'):
            self.anchors.add(attrs['id'])
        if tag == 'a' and attrs.get('name'):
            self.anchors.add(attrs['name'])


def parse(path):
    page = Page()
    page.feed(path.read_text(encoding='utf-8'))
    page.close()
    return page


def destination(href, source):
    parts = urlsplit(href)
    if parts.scheme or parts.netloc:
        return None, None
    route = unquote(parts.path)
    target = SITE / route.lstrip('/') if route.startswith('/') else source.parent / route
    if not route or route.endswith('/') or target.is_dir():
        target /= 'index.html'
    return target.resolve(), unquote(parts.fragment)


class ReleaseRoutesTest(unittest.TestCase):
    def test_entry_routes_preserve_contract_and_crawl_destinations(self):
        home = SITE / 'index.html'
        learn_root = SITE / 'learn'
        legacy = sorted(learn_root.glob('**/index.html'))
        self.assertEqual(len(legacy), 43, 'all learn pages, including the Korean overview')
        counts = {'ko': 0, 'en': 0, 'zh': 0}
        for path in legacy:
            locale = 'ko' if path.parent == learn_root else path.parent.name if path.parent.parent == learn_root and path.parent.name in ('en', 'zh') else 'ko' if path.parent.parent == learn_root else path.parent.parent.name
            counts[locale] += 1
        self.assertEqual(counts, {'ko': 16, 'en': 14, 'zh': 13})
        pages = [home, *legacy]
        parsed = {path: parse(path) for path in pages}

        # Stable routes and anchors captured as a repository-independent base contract.
        stable = {
            home: {'href': {'/', '/roadmap/', '/docs/quickstart/', '/docs/en/quickstart/',
                            '/docs/zh/quickstart/', '/docs/en/troubleshooting/',
                            '/docs/zh/troubleshooting/', '/learn/', '/learn/en/',
                            '/learn/zh/', '/learn/en/troubleshooting/'},
                    'anchors': {'content', 'quickstart', 'install', 'docs'}},
        }
        for path, contract in stable.items():
            page = parsed[path]
            hrefs = {href for href, _ in page.links}
            self.assertTrue(contract['href'] <= hrefs, f'published URL removed: {path}')
            self.assertTrue(contract['anchors'] <= page.anchors,
                            f'published anchor removed: {path}')

        # Homepage quickstarts, all localized recovery routes, and AI manuals.
        self.assertTrue({'content', 'quickstart', 'install', 'docs'} <= parsed[home].anchors)
        # Homepage quickstarts, all localized recovery routes, and the EN AI manual.
        home_routes = {(href, lang) for href, lang in parsed[home].links}
        for route, lang in (
            ('/docs/quickstart/', 'ko'), ('/docs/en/quickstart/', 'en'),
            ('/docs/zh/quickstart/', 'zh-Hans'),
            ('/docs/ai-troubleshooting/', 'ko'),
            ('/docs/en/troubleshooting/', 'en'), ('/docs/zh/troubleshooting/', 'zh-Hans'),
            ('/docs/en/ai-troubleshooting/', 'en'),
        ):
            with self.subTest(home_route=route):
                self.assertIn((route, lang), home_routes, f'homepage route missing: {route}')

        for path in legacy:
            locale = 'ko' if path.parent == learn_root else path.parent.name if path.parent.parent == learn_root and path.parent.name in ('en', 'zh') else 'ko' if path.parent.parent == learn_root else path.parent.parent.name
            required = {
                'ko': ('/docs/quickstart/', '/docs/ai-troubleshooting/'),
                'en': ('/docs/en/quickstart/', '/docs/en/troubleshooting/',
                       '/docs/en/ai-troubleshooting/'),
                'zh': ('/docs/zh/quickstart/', '/docs/zh/troubleshooting/',
                       '/docs/en/ai-troubleshooting/'),
            }[locale]
            links = {href for href, _ in parsed[path].links}
            for route in required:
                with self.subTest(page=path.relative_to(ROOT), route=route):
                    self.assertIn(route, links)

        # Crawl every local URL in the selected pages, including fragments.
        missing = {}
        required_crawl_pages = {home, *legacy}
        for source in required_crawl_pages:
            page = parsed[source]
            for href, _ in page.links:
                target, fragment = destination(href, source)
                if target is None:
                    continue
                if not target.is_file():
                    missing.setdefault(href, set()).add(source.relative_to(ROOT).as_posix())
                elif fragment and fragment not in parse(target).anchors:
                    missing.setdefault(href + '#' + fragment, set()).add(source.relative_to(ROOT).as_posix())
        self.assertFalse(missing, f'broken local destinations (route: source pages): {missing}')


if __name__ == '__main__':
    unittest.main()
