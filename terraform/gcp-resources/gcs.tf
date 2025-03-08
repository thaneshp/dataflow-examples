resource "google_storage_bucket" "dataflow_bucket" {
  name          = var.project_id
  location      = var.region
  force_destroy = true

  uniform_bucket_level_access = true
}

resource "google_storage_bucket_object" "temp_folder" {
  name          = "temp/"
  content       = " "
  bucket        = google_storage_bucket.dataflow_bucket.name
}

resource "google_storage_bucket_object" "template_folder" {
  name          = "template/"
  content       = " "
  bucket        = google_storage_bucket.dataflow_bucket.name
}

resource "google_storage_bucket_object" "input_folder" {
  name          = "input/"
  content       = " "
  bucket        = google_storage_bucket.dataflow_bucket.name
}

resource "google_storage_bucket_object" "output_folder" {
  name          = "output/"
  content       = " "
  bucket        = google_storage_bucket.dataflow_bucket.name
}
