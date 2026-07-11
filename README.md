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
