# Variables for Noah Sjursen Cloud Infrastructure

variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "Default GCP region"
  type        = string
  default     = "us-central1"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "billing_account" {
  description = "GCP Billing Account ID (optional, only needed if creating new project)"
  type        = string
  default     = ""
}

