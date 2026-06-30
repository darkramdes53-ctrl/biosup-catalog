$ErrorActionPreference = "Stop"
$forbidden = @("*.zip","*.7z","*.rar","*.iso","*.exe","*.msi","*.cap","*.rom","*.bin","*.ami","*.fd","*.bio")
foreach ($pattern in $forbidden) {
  $files = Get-ChildItem -Path . -Recurse -File -Filter $pattern -ErrorAction SilentlyContinue
  if ($files.Count -gt 0) {
    $files | ForEach-Object { Write-Error "Forbidden binary file: $($_.FullName)" }
  }
}
Write-Host "No forbidden binary files found."
