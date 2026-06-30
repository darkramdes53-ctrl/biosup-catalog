#!/usr/bin/env python3
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
for path in [ROOT / 'catalog.json', *sorted((ROOT / 'vendors').glob('*.json')), *sorted((ROOT / 'schemas').glob('*.json'))]:
    data = json.loads(path.read_text(encoding='utf-8'))
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'formatted {path.relative_to(ROOT)}')
