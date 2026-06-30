# Contributing

Before opening a pull request:

1. Do not add BIOS files.
2. Add only official vendor links.
3. Keep vendor JSON formatted with two-space indentation.
4. Run validation scripts.
5. Explain which official support page you used.
6. For Gigabyte, include revision notes.
7. For MSI, include board-id when known.

Validation:

```bash
python scripts/format_json.py
python scripts/build_lock.py
python scripts/validate_catalog.py
```
