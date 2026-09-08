$ErrorActionPreference = 'Stop'
$root = Resolve-Path (Join-Path $PSScriptRoot '..\..')
Push-Location $root
try {
  node tools/quality/quality-static.mjs
  if ($LASTEXITCODE -ne 0) { throw 'Static quality check failed.' }
  node tools/quality/quality-browser.mjs
  if ($LASTEXITCODE -ne 0) { throw 'Browser quality check failed.' }
  node tools/quality/quality-regressions.mjs
  if ($LASTEXITCODE -ne 0) { throw 'Record/mission regression failed.' }
  node moamoa/validate_puzzles.cjs
  if ($LASTEXITCODE -ne 0) { throw 'Daily puzzle validation failed.' }
  git diff --check -- index.html guide sw.js manifest.webmanifest tools/quality
  if ($LASTEXITCODE -ne 0) { throw 'Whitespace check failed.' }
  Write-Host 'PASS complete local quality baseline'
} finally {
  Pop-Location
}
