# Noah Sjursen Cloud - Infrastructure

This directory contains Terraform configuration for managing GCP infrastructure.

## Prerequisites

1. **GCP Account** with billing enabled
2. **gcloud CLI** installed and authenticated
3. **Terraform** installed (v1.0+)

## Initial Setup

### 1. Install Tools (if needed)

**gcloud CLI:**
```bash
# Windows (PowerShell as Admin)
(New-Object Net.WebClient).DownloadFile("https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe", "$env:Temp\GoogleCloudSDKInstaller.exe")
& $env:Temp\GoogleCloudSDKInstaller.exe
```

**Terraform:**
```bash
# Windows (with Chocolatey)
choco install terraform

# Or download from: https://www.terraform.io/downloads
```

### 2. Create GCP Project

```bash
# Login to GCP
gcloud auth login

# Create a new project (or use existing one)
gcloud projects create noah-sjursen-cloud --name="Noah Sjursen Cloud"

# Set as default project
gcloud config set project noah-sjursen-cloud

# Link billing account (required for Cloud Run)
gcloud billing projects link noah-sjursen-cloud --billing-account=YOUR-BILLING-ACCOUNT-ID
```

To find your billing account ID:
```bash
gcloud billing accounts list
```

### 3. Authenticate Terraform

```bash
# Create application default credentials
gcloud auth application-default login
```

### 4. Configure Terraform Variables

Edit `../environments/dev.tfvars` and set your project ID:
```hcl
project_id = "noah-sjursen-cloud"  # Your actual project ID
```

## Deploy Infrastructure

```bash
# Navigate to core directory
cd dataplatform/iac/terraform/core

# Initialize Terraform
terraform init

# Plan the changes (dry run)
terraform plan -var-file=../environments/dev.tfvars

# Apply the infrastructure
terraform apply -var-file=../environments/dev.tfvars
```

## What This Creates

- ✅ Enables required GCP APIs (Cloud Run, Cloud Build, Artifact Registry)
- ✅ Creates Artifact Registry for container images
- ✅ Sets up basic project configuration

## After Infrastructure is Ready

Deploy your first API:
```bash
cd ../../../projects/FirstApi
bash deploy.sh
```

## Useful Commands

```bash
# View current infrastructure
terraform show

# Destroy all infrastructure (careful!)
terraform destroy -var-file=../environments/dev.tfvars

# Format terraform files
terraform fmt -recursive
```

## Cost Estimate

With this setup on GCP free tier:
- Cloud Run: Free tier covers ~2M requests/month
- Artifact Registry: First 0.5GB free
- Cloud Build: 120 builds/day free

**Estimated monthly cost: $0-5** (depending on usage)

