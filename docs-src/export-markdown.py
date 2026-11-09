#!/usr/bin/env python3
"""Expose the same Markdown used for the HTML build."""
import json
import shutil
from pathlib import Path
root = Path(__file__).resolve().parent
output = root.parent / 'site' / 'docs' / 'markdown'
output.mkdir(parents=True, exist_ok=True)
for name in json.loads((root / 'content-manifest.json').read_text())['pages']:
    target = output / name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(root / 'content' / name, target)
