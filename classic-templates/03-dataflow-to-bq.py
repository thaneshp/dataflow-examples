# Process flight delay data from CSV and write statistics to BigQuery using Dataflow

from dotenv import load_dotenv
import apache_beam as beam
import os
from apache_beam.options.pipeline_options import PipelineOptions

load_dotenv()

project_id = os.getenv('PROJECT_ID')
region = os.getenv('REGION')
serviceAccount = os.getenv('SERVICE_ACCOUNT_CREDENTIALS')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= serviceAccount

pipeline_options = {
  'project': project_id ,
  'runner': 'DataflowRunner',
  'region': region,
  'staging_location': f'gs://{project_id}/temp',
  'temp_location': f'gs://{project_id}/temp',
  'template_location': f'gs://{project_id}/template/batch_job_df_bq_flights',
  'save_main_session': True 
}

pipeline_options = PipelineOptions.from_dictionary(pipeline_options)
p1 = beam.Pipeline(options=pipeline_options)

class split_lines(beam.DoFn):
  def process(self,record):
    return [record.split(',')]

class Filter(beam.DoFn):
  def process(self,record):
    if int(record[8]) > 0:
      return [record]

def dict_level1(record):
    dict_ = {} 
    dict_['airport'] = record[0]
    dict_['list'] = record[1]
    return(dict_)

def unnest_dict(record):
    def expand(key, value):
        if isinstance(value, dict):
            return [ (key + '_' + k, v) for k, v in unnest_dict(value).items() ]
        else:
            return [ (key, value) ]
    items = [ item for k, v in record.items() for item in expand(k, v) ]
    return dict(items)

def dict_level0(record):
    dict_ = {} 
    dict_['airport'] = record['airport']
    dict_['list_Delayed_num'] = record['list_Delayed_num'][0]
    dict_['list_Delayed_time'] = record['list_Delayed_time'][0]
    return(dict_)

table_schema = 'airport:STRING, list_Delayed_num:INTEGER, list_Delayed_time:INTEGER'
table = f'{project_id}:flights_dataflow.flights_aggr'

Delayed_time = (
  p1
  | "Import Data time" >> beam.io.ReadFromText(f'gs://{project_id}/input/flights_sample.csv', skip_header_lines = 1)
  | "Split by comma time" >> beam.ParDo(split_lines())
  | "Filter Delays time" >> beam.ParDo(Filter())
  | "Create a key-value time" >> beam.Map(lambda record: (record[4],int(record[8])))
  | "Sum by key time" >> beam.CombinePerKey(sum)
)

Delayed_num = (
  p1
  |"Import Data" >> beam.io.ReadFromText(f'gs://{project_id}/input/flights_sample.csv', skip_header_lines = 1)
  | "Split by comma" >> beam.ParDo(split_lines())
  | "Filter Delays" >> beam.ParDo(Filter())
  | "Create a key-value" >> beam.Map(lambda record: (record[4],int(record[8])))
  | "Count by key" >> beam.combiners.Count.PerKey()
)

Delay_table = (
    {'Delayed_num':Delayed_num,'Delayed_time':Delayed_time} 
    | "Group By" >> beam.CoGroupByKey()
    | "Unnest 1" >> beam.Map(lambda record: dict_level1(record))
    | "Unnest 2" >> beam.Map(lambda record: unnest_dict(record))
    | "Unnest 3" >> beam.Map(lambda record: dict_level0(record)) 
    | "Write to BQ" >> beam.io.WriteToBigQuery(
                              table,
                              schema=table_schema,
                              write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                              create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                              custom_gcs_temp_location = f'gs://{project_id}/temp' )
)

p1.run()