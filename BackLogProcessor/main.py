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
# -selected_gcs_buckets
#######################

import os
from google.cloud import pubsub_v1      # Pub/Sub
from google.cloud import storage        # GCS
from google.cloud import monitoring_v3  # Used for StackDriver Audit
import requests                         # Used to curl
import json                             # Used to send & receive data
import datetime                         # Used for time filtering
import time                             # Used to measure lifespan


# Used to measure timespan of function execution
function_lifespan = os.environ(FUNCTION_TIMEOUT_SEC)
function_startTime = time.time()

def Master():
    # List all buckets within scope:
    storage_client = storage.Client()
    buckets = storage_client.list_buckets() ##Array of all buckets

    #List of found Buckets
    FoundBuckets = []
    # Call Functions
    for bucket in buckets:
        # Only call if bucket name matches
        if bucket.name in os.environ(selected_gcs_buckets):
            # Build Curl request
            CallChild(bucket.name)
            # Add to found bucket list
            FoundBuckets.append(bucket.name)

    # Log buckets not Found
    RequestedBuckets = os.environ(selected_gcs_buckets).split(',')

    print ("Following buckets not found: ")

def CallChild(BucketName, AuditStartTime = datetime.datetime.now()):
    # Function used to may a curl request to trigger a copy of this function
    # TODO : Solve for Parallel

    # Build Clound Function URL Path
    function_url = "https://" + os.environ(FUNCTION_REGION) + "." + os.environ(GCP_PROJECT) + ".cloudfunctions.net/" + os.environ(FUNCTION_NAME)
    # Add Headers
    headers = { 'Content-Type' : 'application/json' }
    # Add Relative parameters
    data = {'child_thread' : BucketName, 'start_date' : AuditStartTime }
    # Make Call
    res = requests.post(function_url, json=data, headers=headers)


def Child(BucketName, AuditStartTime):
    # Child process searched StackDriver Audit for a specific bucket and publishes to pub/sub
    AuditResults = query_auditlogs(BucketName, AuditStartTime)

    # Itterate over events and push to pub/sub queue
    for aEvent in AuditResults:
        add_to_pubsub(aEvent)
        # Check time stamp to see if need to pass to Child to continue before function time out
        timeremaining = (time.time() - global function_startTime) - function_lifespan
        if timeremaining > 15:
            CallChild(BucketName, aEvent.time) # TODO: Fix this

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
