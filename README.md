# Google Cloud Dataflow Examples

This repository contains example implementations of Google Cloud Dataflow pipelines. The examples demonstrate how to process data using Apache Beam and Dataflow, including reading from CSV files and writing results to both Google Cloud Storage (GCS) and BigQuery.

## Prerequisites

Before you begin, ensure you have the following:

- [Python](https://www.python.org/downloads/) installed on your local machine.
- [Terraform](https://www.terraform.io/downloads.html) installed on your local machine.
- A Google Cloud Platform account.

## Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/thaneshp/dataflow-examples.git
   cd dataflow-examples/terraform/gcp-resources
   ```
2. **Update environment variables**:

   ```bash
   project_id = "your-project-id"    # Your GCP project ID
   job_name   = "your-job-name"      # Name for your Dataflow job
   region     = "your-region"        # GCP region (e.g., australia-southeast1)
   ```

2. **Authenticate with Google Cloud**:

    ```
    gcloud auth login
    ```

3. **Initialize Terraform**:

     ```bash
     terraform init
     ```

4. **Plan the infrastructure**:

     ```bash
     terraform plan -var-file="env.tfvars"
     ```

5. **Apply the configuration**:

     ```bash
     terraform apply -var-file="env.tfvars" -auto-approve
     ```

## Usage

1. **Get service account key**:

   ``` 
   # Download key file
   gcloud iam service-accounts keys create service-account-key.json \
     --iam-account=dataflow-sa@your-project-id.iam.gserviceaccount.com
   ```

2. **Update the environment variables**:

   Create a `.env` file in the `classic-templates` directory with:
   
   ```bash
   SERVICE_ACCOUNT_CREDENTIALS=/path/to/your-service-account-key.json
   PROJECT_ID=your-gcp-project-id  
   REGION=your-gcp-region
   ```

2. **Run the sample scripts**:

   Navigate to the `classic-templates` directory and run any of the following scripts:

   ```bash
   # Test locally with DirectRunner printing to stdout
   python directRunner-to-stdout.py

   # Test locally with DirectRunner writing to GCS
   python directRunner-to-gcs.py 

   # Create Dataflow template and run job
   python dataflow-to-gcs.py
   ```

3. **Update the Dataflow job configuration**:

   After creating the template, update `dataflow.tf` with:

   ```hcl
   resource "google_dataflow_job" "batch_job" {
     name              = var.job_name
     template_gcs_path = "gs://${var.project_id}/template/batch_job_df_gcs_flights"
     temp_gcs_location = "gs://${var.project_id}/temp"
     project           = var.project_id
     region           = var.region
   }
   ```

   Then run:
   ```bash
   terraform apply -var-file="env.tfvars" -auto-approve
   ```

## Notes

- Ensure your `.env` file is not committed to version control as it contains sensitive information.
- Adjust the resource configurations in the module files as needed to fit your specific requirements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

