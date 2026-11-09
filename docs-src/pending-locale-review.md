# Pending localized documentation UI evidence

This retrospective summary describes static review and limited browser checks communicated in the work conversation, not original signed review records or publication approval. Its hash identifies the summary only; it cannot prove reviewer identity, independence, factual accuracy, full accessibility or real host behavior. Gate and approval remain pending.

| Site-specific file | SHA-256 |
| --- | --- |
| content/assets/ouro-theme.js | 2442b9b72e5a225ddfaf4c2959074880c337b6929138e21c7969380241f4059c |
| overrides/main.html | fbaa5b7642b2eb1c354a5f37ce83725600c0b319140229f25cb39435d91d680f |
| overrides/partials/language.html | 104e838bcc7e3acd19eebe9170e25051cc1b4c1e9c2afd602556c6a2bc80a9bf |
| overrides/partials/nav.html | 8a0f57603fa893b93e2952b6bb7a38b8bfe3d0ce108c5bc8fefefb5e765d3e76 |
| overrides/partials/nav-item.html | fa891f61e114bc0a4dd194ac3f12ea6dc837fca4a593ba7f5d3e92ccf835c8c5 |
| tests/test_locale_ui.py | ed071ce983106bfdcde097470d28a371227f0a8ec934ee90249fa9ef9aa430a0 |

English and Chinese Material labels and custom header/drawer/search controls were localized. Korean-only destinations are labeled; locale guide/install/glossary targets are existing pages. Sidebar logo destination is marked Korean and Chinese skip text clarified. The original upstream typeset-title rendering is preserved. An independent static review reported the original localization P2 addressed; limited browser checks reported English mobile drawer open/Escape close and Chinese header labels. These checks do not establish comprehensive search, keyboard, screen reader, translation, privacy or production behavior.

These files are site-specific and owned by the site repository, not regenerated from the separate canonical Markdown source repository. The two navigation overrides are based on the MkDocs Material 9.7.1 templates and should be rechecked on theme upgrades. To reproduce, use this site snapshot and its `docs-src/requirements.txt`, run the strict MkDocs build, search augmentation, sitemap check and Markdown export. Canonical source sync verifies Markdown but does not recreate these site-owned overrides or JavaScript. Publication gate remains false.
