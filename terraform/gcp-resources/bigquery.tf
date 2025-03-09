resource "google_bigquery_dataset" "flights_dataset" {
  dataset_id                  = "flights_dataset"
  location                    = var.region
  delete_contents_on_destroy  = true
}

resource "google_bigquery_table" "flights_table" {
  dataset_id = google_bigquery_dataset.flights_dataset.dataset_id
  table_id   = "flights_aggr"
  deletion_protection = false
  
  schema = <<EOF
[
  {
    "name": "airport",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "list_Delayed_num", 
    "type": "INTEGER",
    "mode": "REQUIRED"
  },
  {
    "name": "list_Delayed_time",
    "type": "INTEGER", 
    "mode": "REQUIRED"
  }
]
EOF
}
