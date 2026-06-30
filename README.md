# BiosUP Catalog

BiosUP Catalog stores only official BIOS lookup rules and official support-page templates.

It does not store BIOS files, firmware binaries, cracks, mirrors, third-party downloads or proxy lists.

The application uses this catalog to find the correct official support page for a detected motherboard. The final BIOS package must still pass domain, preflight, archive and file verification inside BiosUP before it is treated as safe.

## What is stored

- Vendor names and aliases.
- Official vendor domains.
- Support-page URL templates.
- Model aliases.
- Board IDs when known.
- Revision rules when required.
- Expected BIOS file patterns when known.
- Optional verified latest BIOS metadata when a file has been checked.

## What is not stored

- BIOS ZIP files.
- CAP, ROM, BIN, EXE, MSI, ISO or archive files.
- Mirrors.
- Unofficial downloads.
- Proxy lists.
- Private logs.
- User hardware data.

## Safety rules

- Official domains only.
- HTTPS only.
- Free proxies are never allowed for BIOS downloads.
- Gigabyte boards require revision checks.
- MSI boards should use board-id checks when available.
- SAFE is only valid after file verification inside BiosUP.

## Local validation

Run:

```bash
python scripts/format_json.py
python scripts/build_lock.py
python scripts/validate_catalog.py
```

On Windows PowerShell:

```powershell
./scripts/validate-catalog.ps1
```

## Repository layout

```text
catalog.json
catalog.lock.json
vendors/*.json
schemas/*.json
scripts/*.py
scripts/*.ps1
docs/*.md
.github/workflows/*.yml
```
