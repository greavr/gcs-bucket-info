# Log Processor

This cloud function is designed to respond to a Pub/Sub queue to handle a log event for specific events:
* New Object: `google.storage.object.finalize`
* Delete Object: `google.storage.object.delete`

# Process
- Get object values:
 - Project ID
 - Project Name
 - File Name
 - File Path
 - Object Size
 - Date / Time stamp
 - Bucket Name
 - Storage Class (`multi_regional`,`regional`,`nearline`,`coldline`)
- Check Pub/Sub MSG ID
 - If value not found in Big Query - Insert new row with values
 - If value found in Big Query - Drop
- If error
 - Save raw data packet into Big Query Error Dataset, along with error message
- Drop Data
- Kill Function

# Environmental Variables
`gcs_buckets` = Array of buckets to gather info on. If left blank default to all buckets. Used when filtering logs


# Notes
* [Google Cloud Storage Triggers](https://cloud.google.com/functions/docs/calling/storage)
