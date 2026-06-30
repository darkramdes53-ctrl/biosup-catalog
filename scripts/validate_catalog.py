#!/usr/bin/env python3
import argparse
import json
import pathlib
import re
import sys
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parents[1]
BINARY_EXTENSIONS = {'.zip', '.cap', '.rom', '.bin', '.exe', '.msi', '.7z', '.rar', '.iso', '.ami', '.fd', '.bio'}
FORBIDDEN_HOSTS = {
    'drive.google.com', 'docs.google.com', 'mediafire.com', 'mega.nz', 'dropbox.com',
    'yadi.sk', 'disk.yandex.ru', 'bit.ly', 'goo.gl', 'tinyurl.com', 't.me', 'telegram.me'
}

parser = argparse.ArgumentParser(description='Validate BiosUP catalog safety rules.')
parser.add_argument('--strict', action='store_true', help='Treat recommendations as errors.')
args = parser.parse_args()

errors: list[str] = []
warnings: list[str] = []


def rel(path: pathlib.Path) -> str:
    return str(path.relative_to(ROOT)).replace('\\\\', '/')


def load_json(path: pathlib.Path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc:
        errors.append(f'{rel(path)}: invalid JSON: {exc}')
        return None


def host_matches(host: str, domain: str) -> bool:
    host = host.strip('.').lower()
    domain = domain.strip('.').lower()
    return host == domain or host.endswith('.' + domain)


def check_url(url: str, official_domains: list[str], label: str):
    if not url:
        return
    if '{' in url and '}' in url:
        sample = (url.replace('{slug}', 'SAMPLE-MODEL')
                    .replace('{slugLower}', 'sample-model')
                    .replace('{slugUpper}', 'SAMPLE-MODEL')
                    .replace('{model}', 'SAMPLE MODEL')
                    .replace('{modelEncoded}', 'SAMPLE%20MODEL')
                    .replace('{modelNoSpaces}', 'SAMPLEMODEL')
                    .replace('{query}', 'SAMPLE-MODEL'))
    else:
        sample = url
    parsed = urlparse(sample)
    if parsed.scheme and parsed.scheme != 'https':
        errors.append(f'{label}: URL must use HTTPS: {url}')
        return
    if not parsed.scheme:
        return
    host = parsed.hostname or ''
    if any(host_matches(host, blocked) for blocked in FORBIDDEN_HOSTS):
        errors.append(f'{label}: forbidden host: {url}')
    if official_domains and not any(host_matches(host, domain) for domain in official_domains):
        errors.append(f'{label}: host is not in officialDomains: {url}')


def check_no_binaries():
    for path in ROOT.rglob('*'):
        if path.is_file() and path.suffix.lower() in BINARY_EXTENSIONS:
            errors.append(f'Forbidden binary file in repository: {rel(path)}')


catalog_path = ROOT / 'catalog.json'
if not catalog_path.exists():
    errors.append('catalog.json is missing')
else:
    catalog = load_json(catalog_path)
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
                    check_url(str(template), official_domains, f'{path_value}: genericRules.{key}[{i}]')
            for index, model in enumerate(vendor.get('models') or []):
                label = f'{path_value}: models[{index}] {model.get("model", "")}'
                if not str(model.get('model','')).strip():
                    errors.append(f'{label}: model is empty')
                if 'aliases' in model and not isinstance(model.get('aliases'), list):
                    errors.append(f'{label}: aliases must be an array')
                check_url(str(model.get('supportPageUrl','')), official_domains, f'{label}: supportPageUrl')
                for j, page in enumerate(model.get('revisionPages') or []):
                    check_url(str(page), official_domains, f'{label}: revisionPages[{j}]')
                for field_name in ('latestBios', 'verifiedLatestBios'):
                    bios = model.get(field_name)
                    if isinstance(bios, dict):
                        check_url(str(bios.get('downloadUrl','')), official_domains, f'{label}: {field_name}.downloadUrl')
                        sha = str(bios.get('sha256',''))
                        if sha and not re.match(r'^[A-Fa-f0-9]{64}$', sha):
                            errors.append(f'{label}: {field_name}.sha256 must be 64 hex chars')
                if manufacturer == 'GIGABYTE' and model.get('revisionRequired') is not True:
                    warnings.append(f'{label}: recommended revisionRequired=true')
                if manufacturer == 'GIGABYTE' and model.get('safeWithoutRevision') is not False:
                    warnings.append(f'{label}: recommended safeWithoutRevision=false')
                if not model.get('confidence'):
                    warnings.append(f'{label}: recommended confidence field')
                if not model.get('lastChecked'):
                    warnings.append(f'{label}: recommended lastChecked field')

check_no_binaries()

if args.strict and warnings:
    errors.extend(warnings)

if errors:
    print('Catalog validation failed:')
    for error in errors:
        print(' - ' + error)
    if warnings and not args.strict:
        print('\nRecommendations:')
        for warning in warnings[:50]:
            print(' - ' + warning)
        if len(warnings) > 50:
            print(f' - ... {len(warnings) - 50} more recommendations')
    sys.exit(1)

print('Catalog validation passed.')
if warnings:
    print(f'Recommendations: {len(warnings)}')
    for warning in warnings[:50]:
        print(' - ' + warning)
    if len(warnings) > 50:
        print(f' - ... {len(warnings) - 50} more recommendations')
