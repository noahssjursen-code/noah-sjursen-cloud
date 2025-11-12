# Post sample logs to Komfyrvakt for testing
# Generates realistic time-series data

$apiKey = (Get-Content .env | Select-String "KOMFYRVAKT_API_KEY=").Line -replace "KOMFYRVAKT_API_KEY=", ""
$baseUrl = "http://localhost:8080/api"

Write-Host "Posting sample logs to Komfyrvakt..." -ForegroundColor Green
Write-Host ""

# Generate 60 logs over last 2 HOURS with varying temperature
$logs = @()
$now = Get-Date
for ($i = 120; $i -ge 0; $i -= 2) {  # Every 2 minutes for 2 hours = 60 logs
    $time = $now.AddMinutes(-$i)
    
    # Simulate realistic temperature trend over time
    # Early hours: normal (4-5°C)
    # Mid period: gradual rise
    # Recent: spike then recovery
    if ($i -lt 15) {
        # Recent: cooling down
        $temp = 6.5 + (Get-Random -Minimum -10 -Maximum 5) / 10.0
        $level = if ($temp -gt 7.0) { "warning" } else { "info" }
    } elseif ($i -lt 30) {
        # Temperature spike!
        $temp = 8.0 + (Get-Random -Minimum 0 -Maximum 40) / 10.0
        $level = if ($temp -gt 10.0) { "error" } elseif ($temp -gt 7.0) { "warning" } else { "info" }
    } elseif ($i -lt 60) {
        # Gradual rise
        $temp = 5.0 + (Get-Random -Minimum 0 -Maximum 20) / 10.0
        $level = if ($temp -gt 6.5) { "warning" } else { "info" }
    } else {
        # Early: normal range
        $temp = 4.0 + (Get-Random -Minimum 0 -Maximum 15) / 10.0
        $level = "info"
    }
    
    $log = @{
        message = "Temperature reading"
        level = $level
        group = "datacenter:server-rack-1"
        tags = @("temperature", "monitoring")
        source = "sensor-temp-rack1"
        timestamp = $time.ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
        data = @{
            temperature = [math]::Round($temp, 2)
            threshold = 6.0
            humidity = [math]::Round(45 + (Get-Random -Minimum -5 -Maximum 5), 1)
            cpu_usage = [math]::Round(30 + (Get-Random -Minimum 0 -Maximum 40), 1)
        }
    }
    
    $logs += $log
}

# Post batch
$body = $logs | ConvertTo-Json -Depth 10
$headers = @{
    "Authorization" = "Bearer $apiKey"
    "Content-Type" = "application/json"
}

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/logs/batch" -Method POST -Body $body -Headers $headers
    Write-Host "✅ Posted $($response.ingested) logs successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "View at: http://localhost:8080" -ForegroundColor Cyan
    Write-Host "Group: datacenter:server-rack-1" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Failed to post logs: $_" -ForegroundColor Red
}

