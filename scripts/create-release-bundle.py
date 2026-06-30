#!/usr/bin/env python3
import hashlib
import pathlib
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'
OUT.mkdir(exist_ok=True)
zip_path = OUT / 'biosup-catalog-release.zip'
include_dirs = ['vendors', 'schemas', 'docs']
include_files = ['catalog.json', 'catalog.lock.json', 'README.md', 'CHANGELOG.md', 'SECURITY.md', 'CONTRIBUTING.md']
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    for name in include_files:
        path = ROOT / name
        if path.exists():
            zf.write(path, name)
    for dirname in include_dirs:
        base = ROOT / dirname
        if base.exists():
            for path in sorted(base.rglob('*')):
                if path.is_file():
                    zf.write(path, str(path.relative_to(ROOT)))
sha = hashlib.sha256(zip_path.read_bytes()).hexdigest()
(OUT / 'SHA256SUMS.txt').write_text(f'{sha}  {zip_path.name}\n', encoding='utf-8')
print(zip_path)
print(sha)
