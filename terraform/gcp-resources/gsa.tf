resource "google_service_account" "dataflow_service_account" {
  account_id   = "dataflow-sa"
  display_name = "Service Account for Dataflow Jobs"
  description  = "Service account used to run Dataflow jobs"
}

resource "google_project_iam_member" "dataflow_worker" {
  project = var.project_id
  role    = "roles/dataflow.worker"
  member  = "serviceAccount:${google_service_account.dataflow_service_account.email}"
}

resource "google_project_iam_member" "storage_viewer" {
  project = var.project_id
  role    = "roles/storage.objectViewer"
  member  = "serviceAccount:${google_service_account.dataflow_service_account.email}"
}
