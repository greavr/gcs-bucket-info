# Backlog Processor

This cloud function is designed to review the audit logs and capture file uploads from before the current date / time stamp to gather as much information as possible around previous uploads.

# Process
* Check if child process
* If child
   * Pull Audit logs for only child_thread bucket name, from StartDate
   * Get object values:
      * StackDriver Event ID
      * File Name
      * File Path
      * Object Size
      * Date / Time stamp
      * Bucket Name
      * Storage Class (`multi_regional`,`regional`,`nearline`,`coldline`)
      * Add to Pub/Sub Queue
   * If error
      * Save raw data packet into Big Query Error Dataset, along with error message
   * If success
      * Check Time out remaining
      * If > 15 seconds Next
      * If < 15 seconds call another function pass along:
         * Last processed Event Date / Time Stamp + 0.000001ms
* If not child
   * Get list of buckets matching filter (default all)
   * Spawn one function per bucket with parameter of child_thread = thread bucket name, and StartDate


# Parameters Variables
`filtered_gcs_buckets` = Array of buckets to gather info on. If left blank default to all buckets. Used when filtering logs
`start_date` = Sets the start date to review logs newer than this date / time. Default is all history
`child_thread` = Bucket name to search for

# Todo:
* Solve for timeouts (May need to call another cloud Function with a date / time and bucket index to resume updates from that time)
* Use cloud Function to call another cloud function. One cloud function per bucket
* **Work out Trigger and success notifications**

# Notes

`gcloud beta functions deploy backlog_processor \
 — project {PROJECTID} \
 — entry-point main \
 — source . \
 — memory 128 \
 — timeout 540s`
