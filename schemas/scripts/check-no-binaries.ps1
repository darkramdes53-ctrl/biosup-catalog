$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$forbiddenExtensions = @(".zip", ".cap", ".rom", ".bin", ".exe", ".msi", ".7z", ".rar", ".iso")
$files = Get-ChildItem -Path $root -Recurse -File | Where-Object { $forbiddenExtensions -contains $_.Extension.ToLowerInvariant() }
if ($files.Count -gt 0) {
  $list = $files | ForEach-Object { $_.FullName }
  throw "Forbidden binary files found:`n$($list -join "`n")"
}
Write-Host "No forbidden binary files found."
