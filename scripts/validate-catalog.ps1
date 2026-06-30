$ErrorActionPreference = "Stop"
python scripts/validate_catalog.py
python scripts/build_lock.py
Write-Host "Catalog validation complete."
