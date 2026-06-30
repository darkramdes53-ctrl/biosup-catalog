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
