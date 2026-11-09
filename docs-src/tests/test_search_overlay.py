"""The closed overlay must stop receiving pointer events immediately."""
from pathlib import Path
import unittest

CSS = Path(__file__).resolve().parents[1] / 'content/assets/site.css'
RULE = '[data-md-toggle="search"]:not(:checked) ~ .md-header .md-search__overlay { pointer-events: none; }'
DESKTOP_SEARCH_SLOT_RULE = '''@media screen and (min-width: 60em) {
  .ouro-top-inner > .md-search {
    flex: 0 0 11.7rem;
    width: 11.7rem;
    min-width: 0;
  }
}'''
COMPACT_DESKTOP_HEADER_RULE = '''@media screen and (min-width: 60em) and (max-width: 76.234375em) {
  .ouro-top-inner {
    height: auto;
    min-height: 64px;
    padding-block: 8px;
    gap: 12px;
  }
  .ouro-top-inner > .ouro-brand {
    flex-shrink: 0;
  }
  .ouro-top-inner > .ouro-nav {
    flex: 1 1 0;
    min-width: 0;
    margin-inline: 0;
    flex-wrap: wrap;
    gap: 8px 12px;
  }
}'''

class SearchOverlayTest(unittest.TestCase):
    def test_closed_only_rule_is_present_once(self):
        self.assertEqual(CSS.read_text().count(RULE), 1)

    def test_desktop_search_uses_fixed_header_slot_once(self):
        self.assertEqual(CSS.read_text().count(DESKTOP_SEARCH_SLOT_RULE), 1)

    def test_compact_desktop_header_rule_is_present_once(self):
        self.assertEqual(CSS.read_text().count(COMPACT_DESKTOP_HEADER_RULE), 1)
