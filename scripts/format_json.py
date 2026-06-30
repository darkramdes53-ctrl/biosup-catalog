#!/usr/bin/env python3
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
paths = [ROOT / 'catalog.json'] + sorted((ROOT / 'vendors').glob('*.json'))
for path in paths:
    data = json.loads(path.read_text(encoding='utf-8'))
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'formatted {path.relative_to(ROOT)}')
