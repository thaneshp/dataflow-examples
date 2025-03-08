# Process flight delay data from CSV and print results to stdout using DirectRunner

import apache_beam as beam

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
  | beam.CoGroupByKey()
  | beam.Map(print)
)

p1.run()
