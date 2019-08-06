# gcs-bucket-info
Get bucket size and information using GCP Audit Trails

## Application Design
![GCS to StackDriver Export to Pub/Sub to Cloud Function to Big Query](media/GCS%20Bucket%20Path.jpg?raw=true "Data Path")

## Big Query Table Schema
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


```

## Contribute

Coming soon

## Credits
Your name here!
