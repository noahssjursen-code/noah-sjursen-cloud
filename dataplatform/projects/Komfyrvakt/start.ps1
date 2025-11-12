# Start Komfyrvakt
# Automatically installs dependencies, builds dashboard, and starts the server

Write-Host ""
Write-Host "Starting Komfyrvakt..." -ForegroundColor Green
Write-Host ""

# Check for .env and GEMINI_API_KEY
$envFile = ".env"
$geminiKeySet = $false

if (Test-Path $envFile) {
    $content = Get-Content $envFile -Raw
    if ($content -match 'GEMINI_API_KEY=.+') {
        $geminiKeySet = $true
    }
}

if (-not $geminiKeySet) {
    Write-Host ""
    Write-Host "AI features require a Gemini API key" -ForegroundColor Yellow
    Write-Host "Get free key: https://aistudio.google.com/apikey" -ForegroundColor Cyan
    Write-Host ""
    
    $response = Read-Host "Enter your Gemini API key (or press Enter to skip)"
    
    if ($response -and $response.Trim()) {
        # Append to .env file
        if (-not (Test-Path $envFile)) {
            "# Komfyrvakt Configuration" | Out-File -FilePath $envFile -Encoding UTF8
            "KOMFYRVAKT_API_KEY=" | Out-File -FilePath $envFile -Append -Encoding UTF8
            "" | Out-File -FilePath $envFile -Append -Encoding UTF8
        }
        
        "GEMINI_API_KEY=$response" | Out-File -FilePath $envFile -Append -Encoding UTF8
        Write-Host "Saved to .env file!" -ForegroundColor Green
        Write-Host ""
    } else {
        Write-Host "Skipping AI features (you can add the key to .env later)" -ForegroundColor Yellow
        Write-Host ""
    }
}

# Step 1: Install API dependencies
Write-Host "[1/3] Installing API dependencies..." -ForegroundColor Yellow
cd api
pip install -q -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to install dependencies" -ForegroundColor Red
    exit 1
}
cd ..

# Step 2: Build dashboard
Write-Host "[2/3] Building dashboard..." -ForegroundColor Yellow

$envFile = ".env"
if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        if ($_ -match '^KOMFYRVAKT_API_KEY=(.+)$') {
            $env:VITE_API_KEY = $matches[1]
        }
    }
}

cd dashboard
if (-not (Test-Path "node_modules")) {
    npm install --silent
}
npm run build --silent
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to build dashboard" -ForegroundColor Red
    cd ..
    exit 1
}
cd ..

# Step 3: Start server
Write-Host "[3/3] Starting server..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Ready! Open localhost:8080 in your browser" -ForegroundColor Green
Write-Host ""

cd api
python main.py
