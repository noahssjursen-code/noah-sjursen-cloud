# Setup OAuth 2.0 for Cloud Control Center
# Paste the OAuth client JSON from Google Console

param(
    [string]$ProjectId = $env:GCP_PROJECT_ID,
    [string]$RedirectUri = "http://localhost:8080/auth/callback",
    [string]$SupportEmail
)

if (-not $ProjectId) {
    Write-Host "Usage: .\setup-oauth.ps1 <project-id>" -ForegroundColor Red
    exit 1
}

if (-not $SupportEmail) {
    $SupportEmail = gcloud config get-value account 2>$null
}

Write-Host "OAuth 2.0 Setup for Cloud Control Center" -ForegroundColor Cyan
Write-Host "Project: $ProjectId" -ForegroundColor Yellow
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Manual Steps in GCP Console" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "1. Open: https://console.cloud.google.com/apis/credentials?project=$ProjectId" -ForegroundColor White
Write-Host ""

Write-Host "2. Configure Consent Screen (if not done):" -ForegroundColor White
Write-Host "   - Click 'Configure Consent Screen'" -ForegroundColor Gray
Write-Host "   - User Type: External" -ForegroundColor Gray
Write-Host "   - App name: Cloud Control Center" -ForegroundColor Gray
Write-Host "   - Support email: $SupportEmail" -ForegroundColor Gray
Write-Host "   - Save and Continue through all steps" -ForegroundColor Gray
Write-Host ""

Write-Host "3. Create OAuth Client:" -ForegroundColor White
Write-Host "   - Click 'Create Credentials' > 'OAuth 2.0 Client ID'" -ForegroundColor Gray
Write-Host "   - Application type: Web application" -ForegroundColor Gray
Write-Host "   - Name: cloud-control-center" -ForegroundColor Gray
Write-Host "   - Authorized redirect URIs: $RedirectUri" -ForegroundColor Gray
Write-Host "   - Click 'Create'" -ForegroundColor Gray
Write-Host "   - Click 'DOWNLOAD JSON' button" -ForegroundColor Gray
Write-Host ""

Write-Host "========================================" -ForegroundColor Green
Write-Host "Paste OAuth Client JSON" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Open the downloaded JSON file and paste the entire contents below:" -ForegroundColor Yellow
Write-Host "Press Enter twice when done" -ForegroundColor Yellow
Write-Host ""

$jsonLines = @()
while ($true) {
    $line = Read-Host
    if ([string]::IsNullOrWhiteSpace($line)) { break }
    $jsonLines += $line
}

$jsonContent = $jsonLines -join "`n"

if ([string]::IsNullOrWhiteSpace($jsonContent)) {
    Write-Host "`nError: No JSON provided" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Enter allowed emails (comma-separated):" -ForegroundColor Yellow
Write-Host "Example: you@gmail.com, friend@gmail.com" -ForegroundColor Gray
Write-Host "Leave blank to allow anyone" -ForegroundColor Gray
$allowedEmails = Read-Host "Allowed emails"

try {
    $oauthData = $jsonContent | ConvertFrom-Json
    
    $clientId = $oauthData.web.client_id
    $clientSecret = $oauthData.web.client_secret
    
    if (-not $clientId -or -not $clientSecret) {
        Write-Host "`nError: Invalid JSON format" -ForegroundColor Red
        exit 1
    }
    
    # Write .env file
    $envPath = Join-Path $PSScriptRoot "../../projects/cloud-control-center/.env"
    $envPath = [System.IO.Path]::GetFullPath($envPath)
    $sessionSecret = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object {[char]$_})
    $envContent = @"
GOOGLE_CLIENT_ID=$clientId
GOOGLE_CLIENT_SECRET=$clientSecret
GOOGLE_REDIRECT_URI=$RedirectUri
SESSION_SECRET=$sessionSecret
GCP_PROJECT_ID=$ProjectId
"@
    
    [System.IO.File]::WriteAllText($envPath, $envContent)
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "OAuth Setup Complete!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Credentials saved to: cloud-control-center/.env" -ForegroundColor Cyan
    Write-Host ""
    
} catch {
    Write-Host "`nError parsing JSON: $_" -ForegroundColor Red
    exit 1
}
