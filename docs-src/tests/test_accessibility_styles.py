"""Static checks for code palette and localized theme labels; browser audit remains separate."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT.parent/'site/docs'

def luminance(value):
    components=[int(value[i:i+2],16)/255 for i in (1,3,5)]
    linear=[c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4 for c in components]
    return sum(x*y for x,y in zip(linear,(0.2126,0.7152,0.0722)))

def contrast(a,b):
    values=sorted((luminance(a),luminance(b)))
    return (values[1]+0.05)/(values[0]+0.05)

class ThemeButton(HTMLParser):
    def __init__(self):super().__init__();self.button=None;self.inside=False
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag=='button' and 'data-ouro-theme' in d:self.button={'label':d.get('aria-label',''),'text':''};self.inside=True
    def handle_data(self,data):
        if self.inside:self.button['text']+=data
    def handle_endtag(self,tag):
        if tag=='button':self.inside=False

class AccessibilityStylesTest(unittest.TestCase):
    def test_code_palette_contrast_and_prose_underline(self):
        css=(ROOT/'content/assets/site.css').read_text(); block=css.split('.md-typeset pre > code {',1)[1].split('}',1)[0]
        colors=re.findall(r'--md-code-(?:fg|hl-[a-z-]+)-color:\s*(#[0-9a-fA-F]{6})',block)
        self.assertEqual(len(colors),13)
        for color in colors:
            with self.subTest(color=color):self.assertGreaterEqual(contrast(color,'#102019'),4.5)
        self.assertRegex(css,r'(?s)\.md-typeset :is\(p, li, td, th, blockquote\) a:not\(\.headerlink\)\s*\{[^}]*text-decoration:\s*underline')
    def test_dark_inline_link_and_footer_contrast(self):
        css=(ROOT/'content/assets/site.css').read_text()
        self.assertIn('html[data-theme=dark] .md-typeset a code { background-color: #17251e; color: #7fbea1; }',css)
        self.assertIn('html[data-theme=dark] .md-footer-meta.md-typeset a { color: #b4c8bd !important; }',css)
        self.assertIn('html[data-theme=dark] .md-footer-meta .md-copyright__highlight { color: #b4c8bd; }',css)
        self.assertGreaterEqual(contrast('#7fbea1','#17251e'),4.5)
        self.assertGreaterEqual(contrast('#b4c8bd','#010101'),4.5)
    def test_navigation_target_and_sticky_rule(self):
        css=(ROOT/'content/assets/site.css').read_text()
        self.assertRegex(css,r'(?s)\.md-nav--primary \.md-nav__link\[href\].*?min-height:\s*24px')
        self.assertRegex(css,r'(?s)\.md-nav--primary \.md-nav__title\s*\{[^}]*position:\s*static')
    def test_mobile_toc_panel_follows_toggle(self):
        css=(ROOT/'content/assets/site.css').read_text()
        self.assertRegex(css,r'(?s)#__toc:not\(:checked\) ~ \.md-nav--secondary\s*\{[^}]*visibility:\s*hidden;[^}]*pointer-events:\s*none')
        self.assertRegex(css,r'(?s)#__toc:checked ~ \.md-nav--secondary\s*\{[^}]*visibility:\s*visible;[^}]*pointer-events:\s*auto')
    def test_theme_visible_label_in_accessible_name(self):
        for page in ('quickstart','en/quickstart','zh/quickstart'):
            with self.subTest(page=page):
                parsed=ThemeButton();parsed.feed((SITE/page/'index.html').read_text())
                self.assertIsNotNone(parsed.button);self.assertIn(parsed.button['text'].strip(),parsed.button['label'])
if __name__=='__main__':unittest.main()
