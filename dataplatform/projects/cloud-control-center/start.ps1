# Start Cloud Control Center locally
# Installs dependencies, builds dashboard, runs server

Write-Host "🎛️  Cloud Control Center - Starting..." -ForegroundColor Cyan

# Install Python dependencies
Write-Host "`nInstalling Python dependencies..." -ForegroundColor Yellow
pip install -r api/requirements.txt

# Install dashboard dependencies
Write-Host "`nInstalling dashboard dependencies..." -ForegroundColor Yellow
cd dashboard
npm install

# Build dashboard
Write-Host "`nBuilding dashboard..." -ForegroundColor Yellow
npm run build

# Return to root
cd ..

# Start server
Write-Host "`n========================================" -ForegroundColor Green
Write-Host "Starting server on http://localhost:8080" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green

python api/main.py

