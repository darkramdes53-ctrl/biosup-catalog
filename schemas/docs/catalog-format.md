# Catalog format

## catalog.json

`catalog.json` is the index file. It lists vendor files and global safety policy.

Required fields:

- `schemaVersion`
- `catalogVersion`
- `updatedAt`
- `vendors`

Each vendor entry has:

- `manufacturer`
- `path`

## vendors/*.json

Each vendor file stores official lookup rules.

Required fields:

- `manufacturer`
- `aliases`
- `officialDomains`
- `genericRules`
- `models`

## Model fields

Each model entry should include:

- `model`
- `aliases`
- `supportSlug`
- `supportPageUrl`
- `boardId`
- `revision`
- `expectedBiosFilePattern`
- `revisionPages`
- `latestBios`
- `verifiedLatestBios`
- `confidence`
- `lastChecked`
- `source`
- `safeForDirectDownload`
- `revisionRequired`
- `safeWithoutRevision`
- `notes`

## Confidence values

Use these values:

- `template`: generated from vendor URL rules.
- `manual`: support page was added by hand.
- `verified_page`: support page was opened and matched.
- `verified_file`: BIOS file was checked and hash/size metadata is known.

BiosUP must not treat `template`, `manual` or `verified_page` as final SAFE.

## latestBios and verifiedLatestBios

`latestBios` should stay null unless you intentionally want a direct catalog BIOS candidate.

Prefer `verifiedLatestBios` for checked files. It should contain:

- `version`
- `releaseDate`
- `downloadUrl`
- `fileName`
- `sha256`
- `fileSize`
- `archiveType`
- `biosFileName`
- `checkedAt`
- `sourcePageUrl`

Do not add direct download metadata without verification.
