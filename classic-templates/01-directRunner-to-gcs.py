# Process flight delay data from CSV and write to GCS using DirectRunner

from dotenv import load_dotenv
import apache_beam as beam
import os

load_dotenv()

serviceAccount = os.getenv('SERVICE_ACCOUNT_CREDENTIALS')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= serviceAccount
project_id = os.getenv('PROJECT_ID')

p1 = beam.Pipeline()

class Filter(beam.DoFn):
  def process(self,record):
    if int(record[8]) > 0:
      return [record]

Delayed_time = (
p1
  | "Import Data time" >> beam.io.ReadFromText("flights_sample.csv", skip_header_lines = 1)
  | "Split by comma time" >> beam.Map(lambda record: record.split(','))
  | "Filter Delays time" >> beam.ParDo(Filter())
  | "Create a key-value time" >> beam.Map(lambda record: (record[4],int(record[8])))
  | "Sum by key time" >> beam.CombinePerKey(sum)
)

Delayed_num = (
    p1
    | "Import Data" >> beam.io.ReadFromText("flights_sample.csv", skip_header_lines = 1)
    | "Split by comma" >> beam.Map(lambda record: record.split(','))
    | "Filter Delays" >> beam.ParDo(Filter())
    | "Create a key-value" >> beam.Map(lambda record: (record[4],int(record[8])))
    | "Count by key" >> beam.combiners.Count.PerKey()
)

Delay_table = (
    {'Delayed_num':Delayed_num,'Delayed_time':Delayed_time} 
    | "Group By" >> beam.CoGroupByKey()
    | "Save to GCS" >> beam.io.WriteToText(f'gs://{project_id}/flights_output.csv')
)

p1.run()
