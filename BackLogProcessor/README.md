# Backlog Processor

This cloud function is designed to review the audit logs and capture file uploads from before the current date / time stamp to gather as much information as possible around previous uploads.

# Process
- Get object values:
 - StackDriver Event ID
 - File Name
 - File Path
 - Object Size
 - Date / Time stamp
 - Bucket Name
 - Storage Class (`multi_regional`,`regional`,`nearline`,`coldline`)
 - Check StackDriver Event ID
  - If value not found in Big Query - Insert new row with values
  - If value found in Big Query - Drop
- If error
 - Save raw data packet into Big Query Error Dataset, along with error message
- If success
 - Drop Data
 - Kill Function


# Environmental Variables
gcs_buckets = Array of buckets to gather info on. If left blank default to all buckets. Used when filtering logs
Timeout = Default value is 9 Min
StartDate = Sets the start date to review logs newer than this date / time. Default is all history

# Todo:
* Solve for timeouts (May need to call another cloud Function with a date / time and bucket index to resume updates from that time)
* Use cloud Function to call another cloud function. One cloud function per bucket
* Work out Trigger and success notifications
