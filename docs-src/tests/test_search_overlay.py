"""The closed overlay must stop receiving pointer events immediately."""
from pathlib import Path
import unittest

CSS = Path(__file__).resolve().parents[1] / 'content/assets/site.css'
RULE = '[data-md-toggle="search"]:not(:checked) ~ .md-header .md-search__overlay { pointer-events: none; }'

class SearchOverlayTest(unittest.TestCase):
    def test_closed_only_rule_is_present_once(self):
        self.assertEqual(CSS.read_text().count(RULE), 1)
