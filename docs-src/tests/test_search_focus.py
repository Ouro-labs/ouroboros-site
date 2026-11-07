import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

class SearchFocusTest(unittest.TestCase):
    def test_keyboard_focus_has_inset_light_and_dark_outline(self):
        css = (ROOT / 'content/assets/site.css').read_text()
        self.assertIn('.md-search-result__link:focus-visible { outline: 3px solid #145d57; outline-offset: -3px; }', css)
        self.assertIn('html[data-theme="dark"] .md-search-result__link:focus-visible { outline-color: #a9f2cb; }', css)

if __name__ == '__main__':
    unittest.main()
