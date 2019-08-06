# gcs-bucket-info
Get bucket size and information using GCP Audit Trails, saved into Big Query, Presented Via DataStudio

# Application Design
![GCS to StackDriver Export to Pub/Sub to Cloud Function to Big Query](media/GCS%20Bucket%20Path.jpg?raw=true "Data Path")

# Getting Started

## Things To Consider

## Google Cloud Storage (GCS)
This is the bucket which holds the files. We will be using [GCS Audit](https://cloud.google.com/storage/docs/audit-logs) feature, along with [GCS Triggers](https://cloud.google.com/functions/docs/calling/storage) in order to build this data.

## StackDriver Logging / Sync
[Data Audit logs](https://cloud.google.com/logging/docs/audit/#data-access) events (add, delete, modify) are saved in StackDriver Audit Logs. We will create a sync (another name for export) for these events to a Pub / Sub Queue system that holds a queue of GCS Audit events to be logged.

## Pub / Sub
Message Queue system, used to ensure single queue for processing data into Big Query. Pub/Sub guarantees [At Least Once Delivery](https://cloud.google.com/pubsub/docs/subscriber#at-least-once-delivery) so the code needs to validate that the same value is not recorded twice. Pub/Sub can be configured to use Cloud Functions as a Subscriber to the queue, and we will limit the maximum parallel processing to *20* calls. This way we do not max out the Big Query Connection.

## Cloud Functions
Two cloud functions (`LogProcessor` and `BackLogProcessor`)

First function is tied to the Pub / Sub queue to save log events to Big Query. It supports a environmental variable to filter selected buckets for storing in BQ.
Second function is setup and triggered to run through the audit history to look for events captured in the past to populate the Big Query Dataset with historic information. It supports more fine grain controls over filtering, along with history of when to back date results too. This second function is also designed to trigger itself in order to spawn tasks running in parallel

## Big Query
Creates a Dataset called `gcs_storage_info` with two table `gcs_storage_info` & `gcs_storage_error`. Where the first table is used to store file information, and the second table is used to capture error logging information.

Service accounts attached to each of the Cloud Functions are used to write to the dataset


## Big Query Table Schema
### GCS_Storage_Info

| Column Name | Column Type | Description|
| --- | --- | --- |
| eventid | integer | Used to log either stack driver event id or Pub / Sub Message ID |
| project_id | integer | Project ID |
| project_name | string | Project User Friend Name |
| bucket_name | string | GCS Bucket Name |
| file_name | string | Name of the file |
| file_path | string | Path of the file |
| file_size | int | Size in bytes of the file |
| file_class | string | Storage class of the file |
| date | date | Date of event |
| time | timestamp | Time of the event |

### GCS_Storage_Error

| Column Name | Column Type | Description|
| --- | --- | --- |
| eventid | integer | Used to log either stack driver event id or Pub / Sub Message ID |
| payload | string | Dump of the Event Content or Pub / Sub Message |
| error_msg | string | Error Message caught|
| date_time | datestamp | Date & Time of event|

### Notes:
`gsutil notification create -e OBJECT_FINALIZE -f none gs://{BUCKET}`

`bq mk gcs_storage_info`

`bq mk —-schema \
eventid:integer,\
project_id:integer,\
project_name:string,\
bucket_name:string,\
file_name:string, \
file_path:string, \
file_size:integer,\
file_class:string,\
date:date,\
time:timestamp,\
-t gcs_storage_info.gcs_storage_info`

`bq mk —-schema \
eventid:integer,\
payload:string,\
error_msg:string,\
time:timestamp,\
-t gcs_storage_info.gcs_storage_error`


## Contribute

Coming soon

## Credits
Your name here!
