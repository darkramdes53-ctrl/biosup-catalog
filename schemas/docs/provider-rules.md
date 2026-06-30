# Provider rules

## ASUS

- Prefer `supportonly/{slug}/helpdesk_bios/` pages.
- Do not parse chipset names like B650, B850, X670 as BIOS versions.
- Prefer version numbers from BIOS package file names.
- ZIP packages should contain CAP files.

## MSI

- Use board-id when available.
- Expected pattern should look like `E7E28AMS`.
- Never create MSI.ROM without board-id confirmation.

## Gigabyte

- Revision matters.
- Set `revisionRequired` to true.
- Set `safeWithoutRevision` to false.
- When revision is unknown, BiosUP should prepare separate revision folders or stop for user review.

## ASRock

- Prefer BIOS table parsing over loose page links.
- Check ROM/CAP/BIN payloads after extraction.

## OEM vendors

Dell, HP, Lenovo, Acer and Fujitsu may provide EXE packages.
BiosUP should not blindly treat OEM EXE files as flash-ready motherboard BIOS files.

## GIGABYTE stable/beta rule

GIGABYTE BIOS versions commonly look like `F67` for stable releases and `F68a`, `F67b`, `F67d`, `F67g` for beta/pre-release branches. Application parsers must not treat checksum fields such as `Checksum: F531` as a BIOS version.

When `AllowBeta=false`, the application must choose the highest stable version if one exists. If a beta version is newer than the latest stable version, it may be shown as informational only and must not be prepared automatically unless beta mode is explicitly enabled.

After extraction, the selected version must match the BIOS payload filename/extension. Example: selected `F67` must extract a payload such as `B450MS2H.F67`; selected `F67b` must extract `*.F67b`.
