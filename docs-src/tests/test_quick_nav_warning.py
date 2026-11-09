"""The first-task shortcuts must land before the visible worktree warning."""
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.events = []
        self.details = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'details':
            self.details += 1
        self.events.append((tag, attrs, self.details))

    def handle_endtag(self, tag):
        if tag == 'details':
            self.details -= 1


class QuickNavigationWarningTest(unittest.TestCase):
    def test_shortcuts_land_before_visible_warning_and_all_task_paths(self):
        for path in ('quickstart', 'en/quickstart', 'zh/quickstart'):
            with self.subTest(path=path):
                page = Page()
                page.feed((ROOT / 'site/docs' / path / 'index.html').read_text())
                events = page.events
                links = [a for tag, a, _ in events if tag == 'a' and a.get('href') == '#worktree-first-task']
                self.assertEqual(len(links), 3)
                anchors = [i for i, (_, a, _) in enumerate(events) if a.get('id') == 'worktree-first-task']
                self.assertEqual(len(anchors), 1)
                start = anchors[0]
                warning = next(i for i in range(start + 1, len(events)) if events[i][0] == 'div' and {'admonition', 'warning'} <= set(events[i][1].get('class', '').split()))
                self.assertEqual(events[warning][2], 0, 'warning must not be collapsed in details')
                for target in ('plugin-first-task', 'codex-first-task', 'cli-first-task'):
                    ids = [i for i, (_, a, _) in enumerate(events) if a.get('id') == target]
                    self.assertEqual(len(ids), 1)
                    self.assertLess(warning, ids[0])


if __name__ == '__main__':
    unittest.main()
