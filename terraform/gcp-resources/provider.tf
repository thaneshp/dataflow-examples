provider "google" {
  project = var.project_id
  region  = var.region
}

terraform {
  backend "gcs" {
    bucket = "${var.project_id}-tfstate"
    prefix = "terraform/gcp-resources/state"
  }
}
