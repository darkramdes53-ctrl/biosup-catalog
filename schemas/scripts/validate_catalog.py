#!/usr/bin/env python3
import json
import pathlib
import re
import sys
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parents[1]
BINARY_EXTENSIONS = {'.zip', '.cap', '.rom', '.bin', '.exe', '.msi', '.7z', '.rar', '.iso'}
FORBIDDEN_HOSTS = {
    'drive.google.com', 'docs.google.com', 'mediafire.com', 'mega.nz', 'dropbox.com',
    'yadi.sk', 'disk.yandex.ru', 'bit.ly', 'goo.gl', 'tinyurl.com', 't.me', 'telegram.me'
}

errors: list[str] = []

def load_json(path: pathlib.Path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc:
        errors.append(f'{path.relative_to(ROOT)}: invalid JSON: {exc}')
        return None

def host_matches(host: str, domain: str) -> bool:
    host = host.strip('.').lower()
    domain = domain.strip('.').lower()
    return host == domain or host.endswith('.' + domain)

def check_url(url: str, official_domains: list[str], label: str):
    if not url:
        return
    parsed = urlparse(url)
    if parsed.scheme != 'https':
        errors.append(f'{label}: URL must use HTTPS: {url}')
        return
    host = parsed.hostname or ''
    if any(host_matches(host, blocked) for blocked in FORBIDDEN_HOSTS):
        errors.append(f'{label}: forbidden host: {url}')
    if official_domains and not any(host_matches(host, domain) for domain in official_domains):
        errors.append(f'{label}: host is not in officialDomains: {url}')

def check_no_binaries():
    for path in ROOT.rglob('*'):
        if path.is_file() and path.suffix.lower() in BINARY_EXTENSIONS:
            errors.append(f'Forbidden binary file in repository: {path.relative_to(ROOT)}')

catalog = load_json(ROOT / 'catalog.json')
if catalog:
    if int(catalog.get('schemaVersion', 0)) < 2:
        errors.append('catalog.json: schemaVersion must be >= 2')
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', str(catalog.get('updatedAt', ''))):
        errors.append('catalog.json: updatedAt must be YYYY-MM-DD')
    vendor_refs = catalog.get('vendors') or []
    if not vendor_refs:
        errors.append('catalog.json: vendors is empty')
    seen_manufacturers = set()
    seen_paths = set()
    for ref in vendor_refs:
        manufacturer = str(ref.get('manufacturer', '')).strip().upper()
        path_value = str(ref.get('path', '')).strip()
        if not manufacturer:
            errors.append('catalog.json: vendor manufacturer is empty')
        if manufacturer in seen_manufacturers:
            errors.append(f'catalog.json: duplicate manufacturer {manufacturer}')
        seen_manufacturers.add(manufacturer)
        if path_value in seen_paths:
            errors.append(f'catalog.json: duplicate vendor path {path_value}')
        seen_paths.add(path_value)
        if not re.match(r'^vendors/[a-z0-9_-]+\.json$', path_value):
            errors.append(f'catalog.json: invalid vendor path {path_value}')
            continue
        vendor_path = ROOT / path_value
        if not vendor_path.exists():
            errors.append(f'catalog.json: missing vendor file {path_value}')
            continue
        vendor = load_json(vendor_path)
        if not vendor:
            continue
        official_domains = vendor.get('officialDomains') or []
        if not official_domains:
            errors.append(f'{path_value}: officialDomains is empty')
        if str(vendor.get('manufacturer','')).strip().upper() != manufacturer:
            errors.append(f'{path_value}: manufacturer mismatch with catalog.json')
        generic = vendor.get('genericRules') or {}
        for key in ('supportPageTemplates', 'revisionPageTemplates', 'searchPageTemplates'):
            for i, template in enumerate(generic.get(key) or []):
                sample = str(template).replace('{slug}', 'SAMPLE-MODEL').replace('{model}', 'SAMPLE-MODEL').replace('{query}', 'SAMPLE-MODEL')
                check_url(sample, official_domains, f'{path_value}: genericRules.{key}[{i}]')
        for index, model in enumerate(vendor.get('models') or []):
            label = f'{path_value}: models[{index}] {model.get("model", "")}'
            if not str(model.get('model','')).strip():
                errors.append(f'{label}: model is empty')
            if not isinstance(model.get('aliases'), list):
                errors.append(f'{label}: aliases must be an array')
            check_url(str(model.get('supportPageUrl','')), official_domains, f'{label}: supportPageUrl')
            for j, page in enumerate(model.get('revisionPages') or []):
                check_url(str(page), official_domains, f'{label}: revisionPages[{j}]')
            latest = model.get('latestBios')
            verified = model.get('verifiedLatestBios')
            for field_name, bios in [('latestBios', latest), ('verifiedLatestBios', verified)]:
                if isinstance(bios, dict):
                    url = str(bios.get('downloadUrl',''))
                    check_url(url, official_domains, f'{label}: {field_name}.downloadUrl')
                    sha = str(bios.get('sha256',''))
                    if sha and not re.match(r'^[A-Fa-f0-9]{64}$', sha):
                        errors.append(f'{label}: {field_name}.sha256 must be 64 hex chars')
            if manufacturer == 'GIGABYTE' and model.get('revisionRequired') is not True:
                errors.append(f'{label}: Gigabyte model must set revisionRequired=true')
            if manufacturer == 'GIGABYTE' and model.get('safeWithoutRevision') is not False:
                errors.append(f'{label}: Gigabyte model must set safeWithoutRevision=false')
            if manufacturer == 'MSI' and model.get('boardId') and not str(model.get('expectedBiosFilePattern','')).upper().startswith('E'):
                errors.append(f'{label}: MSI model with boardId should set expectedBiosFilePattern like E7E28AMS')

check_no_binaries()

if errors:
    print('Catalog validation failed:')
    for error in errors:
        print(' - ' + error)
    sys.exit(1)

print('Catalog validation passed.')
