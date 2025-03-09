# Google Cloud Dataflow Examples

This repository contains example implementations of Google Cloud Dataflow pipelines. The examples demonstrate how to process data using Apache Beam and Dataflow, including reading from CSV files and writing results to both Google Cloud Storage (GCS) and BigQuery.

## Prerequisites

Before you begin, ensure you have the following:

- [Python](https://www.python.org/downloads/) installed on your local machine.
- [Terraform](https://www.terraform.io/downloads.html) installed on your local machine.
- A Google Cloud Platform account.

## Setup

Before running the examples, you'll need to set up the required Google Cloud Platform resources. This repository includes Terraform configurations to automatically provision:

- A service account with necessary permissions for Dataflow
- Cloud Storage buckets for input/output data
- BigQuery dataset and tables
- Required IAM roles and permissions

Follow the steps below to set up the infrastructure:

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
     terraform plan -var-file="../common.tfvars"
     ```

5. **Apply the configuration**:

     ```bash
     terraform apply -var-file="../common.tfvars" -auto-approve
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

3. **Run the sample scripts**:

   Navigate to the `classic-templates` directory and run any of the scripts.

   The scripts perform the following:
   
   * `00-directRunner-to-stdout.py`: Processes flight delays locally, prints to stdout
   * `01-directRunner-to-gcs.py`: Processes flight delays locally, writes to GCS
   * `02-dataflow-to-gcs.py`: Processes flight delays on Dataflow, writes to GCS
   * `03-dataflow-to-bq.py`: Processes flight delays on Dataflow, writes to BigQuery

4. **Apply the Dataflow configuration**:

   ```bash
   cd dataflow-examples/terraform/dataflow-job
   terraform init
   terraform plan --var-file="../common.tfvars"
   terraform apply --var-file="../common.tfvars" -auto-approve
   ```

5. **View the Dataflow jobs**:

   Navigate to the [Dataflow Jobs page](https://console.cloud.google.com/dataflow/jobs) in the Google Cloud Console to monitor your running jobs. You should see two jobs:
   
   * `df-to-gcs-job`: Processing flight delays and writing to Cloud Storage
   * `df-to-bq-job`: Processing flight delays and writing to BigQuery

## Notes

- Ensure your `.env` file is not committed to version control as it contains sensitive information.
- Adjust the resource configurations in the module files as needed to fit your specific requirements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Thanesh Pannirselvam - [@thaneshp333](https://x.com/thaneshp333)
