#!/usr/bin/env python3
import hashlib
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / 'catalog.json').read_text(encoding='utf-8'))
vendors = []
for ref in catalog.get('vendors', []):
    path = ROOT / ref['path']
    data = json.loads(path.read_text(encoding='utf-8'))
    raw = path.read_bytes()
    vendors.append({
        'manufacturer': ref['manufacturer'],
        'path': ref['path'],
        'sha256': hashlib.sha256(raw).hexdigest(),
        'models': len(data.get('models') or []),
        'officialDomains': len(data.get('officialDomains') or [])
    })
lock = {
    'schemaVersion': catalog.get('schemaVersion', 2),
    'catalogVersion': catalog.get('catalogVersion', ''),
    'generatedAt': (catalog.get('updatedAt') or '1970-01-01') + 'T00:00:00Z',
    'catalogSha256': hashlib.sha256((ROOT / 'catalog.json').read_bytes()).hexdigest(),
    'vendorCount': len(vendors),
    'modelCount': sum(v['models'] for v in vendors),
    'vendors': vendors
}
(ROOT / 'catalog.lock.json').write_text(json.dumps(lock, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('catalog.lock.json generated.')
