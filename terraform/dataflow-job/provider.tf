provider "google" {
  project = var.project_id
  region  = var.region
}

terraform {
  backend "local" {
    path = "./terraform.tfstate"
  }
}
