# gcs-bucket-info
Get bucket size and information using GCP Audit Trails, saved into Big Query, Presented Via DataStudio

## Application Design
![GCS to StackDriver Export to Pub/Sub to Cloud Function to Big Query](media/GCS%20Bucket%20Path.jpg?raw=true "Data Path")

## Pub / Sub

## Cloud Functions
Two cloud functions (`LogProcessor` and `BackLogProcessor`)

First function is tied to the Pub / Sub queue to save log events to Big Query. It supports a environmental variable to filter selected buckets for storing in BQ.
Second function is setup and triggered to run through the audit history to look for events captured in the past to populate the Big Query Dataset with historic information. It supports more fine grain controls over filtering, along with history of when to back date results too. This second function is also designed to trigger itself in order to spawn tasks running in parallel

## Big Query
Creates a Dataset called `gcs_storage_info` with two table `gcs_storage_info` & `gcs_storage_error`. Where the first table is used to store file information, and the second table is used to capture error logging information.

Service accounts attached to each of the Cloud Functions are used to write to the dataset


### Big Query Table Schema
####GCS_Storage_Info

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

####GCS_Storage_Error
| Column Name | Column Type | Description|
| --- | --- | --- |
| eventid | integer | Used to log either stack driver event id or Pub / Sub Message ID |
| payload | string | Dump of the Event Content or Pub / Sub Message |
| error_msg | string | Error Message caught|


```

## Contribute

Coming soon

## Credits
Your name here!
