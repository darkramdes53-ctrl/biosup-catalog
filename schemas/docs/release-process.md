# Release process

1. Edit vendor files.
2. Run `python scripts/format_json.py`.
3. Run `python scripts/build_lock.py`.
4. Run `python scripts/validate_catalog.py`.
5. Commit changes.
6. Push to main.
7. Create a GitHub release tag like `catalog-v2.1.0`.
8. Attach generated catalog artifacts.

The GitHub workflow also validates the catalog on push and pull requests.
