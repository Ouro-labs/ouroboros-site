# ouroboros.page

Public website for [Ouroboros](https://github.com/Q00/ouroboros), the specification-first Agent OS.

This repository is intentionally a presentation layer. Product behavior, installation instructions, runtime support, and technical documentation remain canonical in `Q00/ouroboros`.

## Local preview

```bash
python3 -m http.server --directory site 8000
```

Then open <http://localhost:8000>.

## Deployment

GitHub Actions deploys `site/` to GitHub Pages on every push to `main`. The custom domain is `ouroboros.page`.

## Korean documentation preview

The selected Markdown pages under `docs-src/content/` are generated from the
Ouroboros documentation source. `docs-src/content-manifest.json` records source
and generated SHA-256 values. To check the copied pages and build locally:

```bash
python -m pip install -r docs-src/requirements.txt
python docs-src/verify-content.py
python -m mkdocs build --strict --config-file docs-src/mkdocs.yml
python docs-src/augment-search.py
python docs-src/check-sitemaps.py
python docs-src/export-markdown.py
python -m http.server --directory site 8000
```

Open `/docs/`. The Pages workflow runs the same build before publishing. To
refresh the snapshot, use `integration/site/sync-public-pages.py` in the
separate documentation source repository. From that repository, run:

```bash
python3 integration/site/sync-public-pages.py --site /path/to/ouroboros-site
python3 integration/site/sync-public-pages.py --site /path/to/ouroboros-site --check
```

The second command compares source and generated page hashes. Review the resulting diff and publication
scope before using it. The site build alone cannot check an unavailable source
repository; it checks generated pages against the committed manifest.

The TUI demo GIF is from Q00/ouroboros commit `722172ef096767583679d04aef5e847458fee6b2`, `docs/images/ooo-tui-monitor.gif`, and is covered by the repository's MIT license and copyright notice in `LICENSE`. Its SHA-256 and source are recorded in the generated manifest.

The changed-link gate is deliberately closed. `docs-src/link-review-evidence.json`
contains only review scope and SHA-256 identities, with independent implementation
review still pending. It covers the 92 changed-link groups only; it does not
certify unchanged links, external availability, all product facts, privacy,
translations, accessibility, or host execution. The private review reports are
not included here. In the documentation workspace, run
`python3 integration/site/verify-link-evidence.py` to compare those report hashes,
the generator, source pages, generated pages, and the recorded delta chain. The
public build can check the generated snapshot and verifier hashes, but cannot
independently access private reports or prove reviewer independence. An independent
implementation review must be recorded before this link-specific gate is opened;
opening it is not permission to publish or merge.
