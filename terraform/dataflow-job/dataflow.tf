resource "google_dataflow_job" "dataflow_job" {
  depends_on = [
    google_service_account.dataflow_service_account,
    google_project_iam_member.dataflow_worker,
    google_project_iam_member.storage_viewer
  ]
  
  name                    = var.job_name
  template_gcs_path       = "gs://my-bucket/templates/template_file"
  temp_gcs_location      = "gs://my-bucket/tmp_dir"
  service_account_email  = google_service_account.dataflow_service_account.email
}
