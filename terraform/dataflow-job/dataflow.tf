resource "google_project_service" "dataflow_api" {
  service = "dataflow.googleapis.com"
  disable_on_destroy = true
}

resource "google_dataflow_job" "df_to_gcs_job" {
  depends_on = [
    google_project_service.dataflow_api
  ]

  name                    = "df-to-gcs-job"
  template_gcs_path       = "gs://${var.project_id}/template/batch_job_df_gcs_flights"
  temp_gcs_location      = "gs://${var.project_id}/temp"
  service_account_email  = "dataflow-sa@${var.project_id}.iam.gserviceaccount.com"
}

resource "google_dataflow_job" "df_to_bq_job" {
  depends_on = [
    google_project_service.dataflow_api
  ]

  name                    = "df-to-bq-job"
  template_gcs_path       = "gs://${var.project_id}/template/batch_job_df_bq_flights"
  temp_gcs_location      = "gs://${var.project_id}/temp"
  service_account_email  = "dataflow-sa@${var.project_id}.iam.gserviceaccount.com"
}
