#######################
# Custom function designed to operate in master OR child mode
# Master mode: Get list of GCS Buckets and spawn child process per GCS Bucket
# Child mode: Query StackDriver Audit logs for insert / delete events on target GCS bucket and publish events to pubsub queue
# Maintainer: Rgreaves@google.com
# Latest update: Augst 6th 2019
# Accepted Parameters:
# - child_thread
# - start_date
# Envionmental Variables:
# -filtered_gcs_buckets
#######################

import os
from google.cloud import pubsub_v1      # Pub/Sub
from google.cloud import storage        # GCS
import requests                         # Used to curl
from google.cloud import monitoring_v3  # Used for StackDriver Audit
import json                             # Used to send & receive data


# Build Clound Function Path
function_url = "https://" + os.environ(FUNCTION_REGION) + "." + os.environ(GCP_PROJECT) + ".cloudfunctions.net/" + os.environ(FUNCTION_NAME)

def Master():
    # List all buckets within scope:
    storage_client = storage.Client()
    buckets = storage_client.list_buckets() ##Array of all buckets

    # Call Functions
    for bucket in buckets:
        # Build Curl request
        # TODO: Solve for parralization
        headers = {(}'Content-Type':'application/json'}
        data = {"child_thread":bucket.name}
        res = requests.post(function_url, json=data, headers=headers)

def Child(BucketName, AuditStartTime):
    # Child process searched StackDriver Audit for a specific bucket and publishes to pub/sub
    AuditResults = query_auditlogs(BucketName, AuditStartTime)

    # Itterate over events and push to pub/sub queue
    for aEvent in AuditResults:
        add_to_pubsub(aEvent)
    return True

def add_to_pubsub(EventDetails):
    return True

def query_auditlogs(BucketName, AuditStartTime):
    return True



def main(request):
    # Check if child process or master process
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'child_thread' in request_json:
        Child(request_json['child_thread'], request_json['start_date'])
    elif request_args and 'child_thread' in request_args:
        Child(request_args['child_thread'], request_args['start_date'])
    else:
        Master() # Child_thread not set run as master
