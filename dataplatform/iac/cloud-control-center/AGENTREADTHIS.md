# Cloud Control Center Infrastructure

## Purpose

Setup scripts for Cloud Control Center authentication and permissions.

## Bootstrap

Run all setup in sequence:

```powershell
.\bootstrap.ps1 <project-id> -ServiceAccount
```

Or for OAuth:

```powershell
.\bootstrap.ps1 <project-id> -OAuth
```

## Scripts

### `setup-oauth.ps1`
Configures OAuth 2.0 for user authentication.

**Usage:**
```powershell
.\setup-oauth.ps1 <project-id> [redirect-uri]
```

**What it does:**
- Enables required APIs
- Provides instructions for OAuth consent screen setup
- Guides through OAuth client creation

**Note:** OAuth client creation requires manual steps in GCP Console.

### `setup-service-account.ps1`
Creates service account with read permissions for GCP resources.

**Usage:**
```powershell
.\setup-service-account.ps1 <project-id> [service-account-name]
```

**What it does:**
- Creates service account
- Grants viewer roles (compute, run, storage, logs)
- Generates key file
- Provides .env configuration instructions

**⚠️ Security:** Keep the generated key file secure and add to .gitignore.

## Authentication Methods

### Option A: User OAuth (recommended for personal use)
- User logs in with their Google account
- Uses their own credentials
- Requires OAuth setup

### Option B: Service Account (recommended for team use)
- App uses service account credentials
- User authenticates to dashboard only
- More controlled permissions

## Required APIs

These are enabled automatically:
- `iamcredentials.googleapis.com`
- `cloudresourcemanager.googleapis.com`
- `iam.googleapis.com`

## Environment Variables

After setup, add to `cloud-control-center/.env`:

**For OAuth:**
```bash
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8080/callback
```

**For Service Account:**
```bash
GOOGLE_APPLICATION_CREDENTIALS=../../iac/cloud-control-center/cloud-control-center-sa-key.json
```

## Security Notes

- Never commit `.env` files or service account keys to git
- Add `*-sa-key.json` to `.gitignore`
- Rotate service account keys regularly
- Use minimum required permissions

