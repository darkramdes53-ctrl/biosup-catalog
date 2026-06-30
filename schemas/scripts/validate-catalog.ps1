$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
python "$root/scripts/validate_catalog.py"
python "$root/scripts/build_lock.py"
Write-Host "Catalog validation and lock generation completed."
