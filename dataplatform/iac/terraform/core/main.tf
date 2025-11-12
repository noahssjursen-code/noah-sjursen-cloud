# Noah Sjursen Cloud - Core Infrastructure
# Terraform configuration for GCP

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }

  # Uncomment after first apply to store state in GCS
  # backend "gcs" {
  #   bucket = "noah-sjursen-cloud-terraform-state"
  #   prefix = "terraform/state"
  # }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Enable required GCP APIs
resource "google_project_service" "cloud_run" {
  service            = "run.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "cloud_build" {
  service            = "cloudbuild.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "artifact_registry" {
  service            = "artifactregistry.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "cloud_resource_manager" {
  service            = "cloudresourcemanager.googleapis.com"
  disable_on_destroy = false
}

# Artifact Registry for storing container images
resource "google_artifact_registry_repository" "containers" {
  location      = var.region
  repository_id = "noah-sjursen-cloud"
  description   = "Container images for Noah Sjursen Cloud services"
  format        = "DOCKER"

  depends_on = [google_project_service.artifact_registry]
}

# Cloud Storage bucket for terraform state (create this manually first or uncomment after initial setup)
# resource "google_storage_bucket" "terraform_state" {
#   name     = "${var.project_id}-terraform-state"
#   location = var.region
#   
#   versioning {
#     enabled = true
#   }
#   
#   lifecycle_rule {
#     condition {
#       num_newer_versions = 3
#     }
#     action {
#       type = "Delete"
#     }
#   }
# }

# Output important values
output "project_id" {
  value = var.project_id
}

output "region" {
  value = var.region
}

output "artifact_registry_url" {
  value = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.containers.repository_id}"
}

