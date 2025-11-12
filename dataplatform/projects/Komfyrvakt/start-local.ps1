# Start Komfyrvakt locally (API + Dashboard)
# Alternative to Docker Compose for local development

Write-Host "🔥 Starting Komfyrvakt..." -ForegroundColor Green

# Start API in background
Write-Host "`nStarting API on port 8080..." -ForegroundColor Yellow
$apiJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    cd api
    python main.py
}

# Wait a moment for API to start
Start-Sleep -Seconds 3

# Start Dashboard
Write-Host "Starting Dashboard on port 3000..." -ForegroundColor Yellow
cd dashboard
npm run dev

# Cleanup on exit
Stop-Job $apiJob
Remove-Job $apiJob

