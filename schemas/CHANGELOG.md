# Changelog

## v2.2.0 - 2026-06-30

- Added GitHub Actions validation and release workflows.
- Added JSON schemas, validation scripts, docs and issue templates.
- Added `catalog.lock.json` generation.
- Added safety policy: no BIOS/firmware binaries, no mirrors, official vendor domains only.
- Added future-proof guidance for GIGABYTE stable/beta handling: stable BIOS must be preferred when application `AllowBeta=false`; beta versions use suffix letters such as `F68a`.
- Added GIGABYTE parser safety requirement: checksum values must never be treated as BIOS versions.

## v2.1.0 - 2026-06-30

- Added catalog validation structure.
- Added provider rules and release docs.

## v2.0.0 - 2026-06-30

- Initial public BiosUP catalog format with vendor files.
