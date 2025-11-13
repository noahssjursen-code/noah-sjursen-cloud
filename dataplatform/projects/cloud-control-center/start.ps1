# Start Cloud Control Center
# Quick start: assumes dashboard is already built

Write-Host "Cloud Control Center - Starting..." -ForegroundColor Cyan

# Check if dashboard build exists
if (-not (Test-Path "dashboard/build")) {
    Write-Host "`nError: Dashboard not built. Run .\startNbuild.ps1 first." -ForegroundColor Red
    exit 1
}

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "Starting server on http://localhost:8080" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green

python api/main.py

