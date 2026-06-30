# Release process

1. Validate the catalog.
2. Build `catalog.lock.json`.
3. Commit changes.
4. Create a tag like `catalog-v2.1.0`.
5. Push the tag.
6. GitHub Actions will build a release bundle and SHA-256 file.

The release bundle should contain metadata and lookup rules only. It must not contain BIOS files.
