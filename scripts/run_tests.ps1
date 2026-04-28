# Run pytest from repo root; failures show traceback (--tb=short) and non-zero exit code.
$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)
python -m pytest tests @args
exit $LASTEXITCODE
