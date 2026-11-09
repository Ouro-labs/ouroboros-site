# Pending site accessibility evidence

This retrospective summary records static checks and independent browser/axe observations conveyed in the work conversation, not an original signed report or publication approval. Hashes identify these files only; they do not establish reviewer identity, independence, factual accuracy, full accessibility or real screen reader behavior. Gate and approval remain pending.

| Site-owned file | SHA-256 |
| --- | --- |
| docs-src/content/assets/site.css | adc2a5b37c191960e4b53aa6ce1ccd820fc0ad6528619a77e4e11e08e1cd60fe |
| docs-src/overrides/main.html | 70880cfbaec0ae37136ae2276a60552489e1cedbbb93dc576cd0d37892d99ca3 |
| docs-src/tests/test_accessibility_styles.py | b80084728b0db4e7877978bf636827cfa3890998d5a661ed779f8ec9ad29f520 |

The site-owned CSS adjusts code and inline-code contrast, underlines prose links, adjusts footer contrast, sizes navigation targets and prevents a closed mobile TOC panel intercepting the primary drawer. The site template aligns visible and accessible theme-button names. These files are not produced by canonical Markdown synchronization. Reported independent testing covered five desktop pages in both themes using axe-core 4.14.0/Chromium 155, plus a mobile pointer/TOC sample. Some axe checks remained incomplete; a code-scroll warning had keyboard operation observed in three language samples, and no real screen reader test was performed. This record is not a blanket WCAG conformance claim.
