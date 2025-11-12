# Build SvelteKit dashboard for production
# Creates static files that the API will serve

Write-Host "Building Komfyrvakt Dashboard..." -ForegroundColor Green

# Load API key from root .env and pass to Vite
$envFile = ".env"
if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        if ($_ -match '^KOMFYRVAKT_API_KEY=(.+)$') {
            $env:VITE_API_KEY = $matches[1]
        }
    }
}

cd dashboard

# Install dependencies if needed
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    npm install
}

# Build the app (VITE_API_KEY is passed from parent env)
Write-Host "Building dashboard..." -ForegroundColor Yellow
npm run build

Write-Host ""
Write-Host "Dashboard built successfully!" -ForegroundColor Green
Write-Host "Run: cd api; python main.py" -ForegroundColor Cyan
