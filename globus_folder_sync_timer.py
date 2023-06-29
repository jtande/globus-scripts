#!/usr/bin/python3.8

#############################################################################
##!/usr/bin/env python
#
#"""Sync a directory between two Globus endpoints. Defaults:
#
# Authorization only needs to happen once, afterwards tokens are saved to disk
# (MUST BE STORED IN A SECURE LOCATION). Store data is already checked for
# previous transfers, so if this script is run twice in quick succession,
# the second run won't queue a duplicate transfer."""
#
# You can specify how long and often to execute the transfer task
#
#     cc Jacob Fosso Tande, Ph.D 2023-06-23
#############################################################################

import json
import sys
import os
import six
import argparse
import globus_sdk
from fair_research_login import NativeClient

from globus_sdk.scopes import (
    GCSCollectionScopeBuilder,
    MutableScope,
    TimerScopes,
    TransferScopes
)

##############################################
#
#       Define Default Parameters
#
#############################################


### begin setting for timer task
from datetime import datetime, timedelta
# Globus Azure VM endpoint
SOURCE_ENDPOINT = '2a32604c-fe5e-11ed-ba4c-09d6a6f08166'
# Globus PSI Research Storage
DESTINATION_ENDPOINT = '23438250-7ba0-47be-b165-85f1ebf18b51'
# Copy data off of the endpoint share
SOURCE_PATH = '/data/rdata'

# Destination Path -- The directory will be created if it doesn't exist
DESTINATION_PATH = '/sandhills/test' #rs1/shares/cals-research-station/sandhills/raw/'

TRANSFER_LABEL = 'NCSU PSI Sweet-APPS Data Transfer'
# You will need to register a *Native App* at https://developers.globus.org/
# Your app should include the following:
#     - The scopes should match the SCOPES variable below
#     - Your app's clientid should match the CLIENT_ID var below
#     - "Native App" should be checked
# For more information:
# https://docs.globus.org/api/auth/developer-guide/#register-app
NATIVE_CLIENT_ID = 'b9e2108b-2f93-40d7-a88b-607ed636ef16'

# Unique globus endpoint for globus timer
TIMER_CLIENT_ID = "524230d7-ea86-4a52-8312-86065a9e0417" #'69b33ab6-6a4d-4952-b197-7e59c0b67a9d'
DATA_FILE = 'transfer-data.json'
REDIRECT_URI = 'https://auth.globus.org/v2/web/auth-code'
SCOPES = ('openid email profile '
          'urn:globus:auth:scope:transfer.api.globus.org:all')

APP_NAME = 'NCSU PSI Data Transfer App'

# Parse input arguments                                                         
def parse_args():
    parser = argparse.ArgumentParser(description='''                            
        Source Endpoint ID.''')
    parser.add_argument('--srcendpt',
        type=str,
        default=SOURCE_ENDPOINT,
        help=f'Starting endpoint ID. [default: 2a32604c-fe5e-11ed-ba4c-09d6a6f08166 ]')
    parser.add_argument('--destendpt',
        type=str,
        default=DESTINATION_ENDPOINT,
        help=f'Destination endpoint ID. [default: 23438250-7ba0-47be-b165-85f1ebf18b51 ]')
    parser.add_argument('--sourcepath',
        type=str,
        default=SOURCE_PATH,
        help=f'Source Path. [default: /data/rdata ]')
    parser.add_argument('--destpath',
        type=str,
        default=DESTINATION_PATH,
        help=f'Source Path. [default: /data/rdata ]')
    parser.add_argument('--transflabel',
        type=str,
        default=TRANSFER_LABEL,
        help='Human readable transfer label. [default: "NCSU PSI Sweet-APPS Data Transfer"]')
    parser.set_defaults(verbose=True)

    return parser.parse_args()

# timer client
def setup_timer_client():

    timer_scope = TimerScopes.make_mutable("timer")
    transfer_scope = TransferScopes.make_mutable("all")
    transfer_action_provider_scope_string = ("https://auth.globus.org/scopes/actions.globus.org/transfer/transfer")
    transfer_action_provider_scope = MutableScope(transfer_action_provider_scope_string)
    transfer_action_provider_scope.add_dependency(transfer_scope)
    timer_scope.add_dependency(transfer_action_provider_scope)
    print(f"Requesting scopes: {timer_scope}")

    # Initialize your native app auth client
    native_client = globus_sdk.NativeAppAuthClient(NATIVE_CLIENT_ID)

    # Get access tokens to use for both Transfer and Timer
    native_client.oauth2_start_flow(requested_scopes=timer_scope)
    authorize_url = native_client.oauth2_get_authorize_url()
    print(f"Please go to this URL and login:\n\n{authorize_url}\n")
    auth_code = input("Enter the auth code here: ").strip()
    
    token_response = native_client.oauth2_exchange_code_for_tokens(auth_code)
    timer_token = token_response.by_resource_server[TIMER_CLIENT_ID]["access_token"]

    # Create a `TransferData` object
    data = globus_sdk.TransferData(source_endpoint=SOURCE_ENDPOINT,
                                    destination_endpoint=DESTINATION_ENDPOINT,
                                    label=TRANSFER_LABEL,
                                    sync_level="checksum")
    data.add_item(SOURCE_PATH, DESTINATION_PATH, recursive=True)
    
    # Set up the Timer client
    timer_authorizer = globus_sdk.AccessTokenAuthorizer(timer_token)
    timer_client = globus_sdk.TimerClient(authorizer=timer_authorizer)
    
    # Create a Timer job, set to start at midnight every day 
    start = datetime(2023, 6, 27, hour=4, minute=0, second=0, microsecond=0) #datetime.utcnow()
    interval = timedelta(days=1)
    name =TRANSFER_LABEL
    job = globus_sdk.TimerJob.from_transfer_data(
        data,
        start,
        interval,
        stop_after_n=999999999,
        name=name,
        scope=transfer_action_provider_scope_string,
    )
    response = timer_client.create_job(job)
    assert response.http_status == 201
    job_id = response["job_id"]
    print(f"Timer job ID: {job_id}")
    
    all_jobs = timer_client.list_jobs()
    assert job_id in {job["job_id"] for job in timer_client.list_jobs()["jobs"]}

    get_job_response = timer_client.get_job(job_id)
    assert get_job_response.http_status == 200
    assert get_job_response["name"] == name
    
    return 

# Compress data before transfer. This script should be run on the source endpoint
def compress_dir():
    ''' compress the directory to transfer'''
    return os.system("tar --zstd -cf /data/rdata/05212023_w.tar.zstd /data/rdata/05212023_w")

get_input = getattr(__builtins__, 'raw_input', input)


# Define the driver function
def main():
    tokens = None
    # get input parameters
    args = parse_args()
    TRANSFER_LABEL=args.transflabel
    DESTINATION_PATH=args.destpath
    SOURCE_PATH=args.sourcepath
    DESTINATION_ENDPOINT=args.destendpt
    SOURCE_ENDPOINT=args.srcendpt

    # compress file before transfer
    compress_dir()

    # Set up the Timer client
    setup_timer_client()
  
    print('Transfer has been started from\n  {}:{}\nto\n  {}:{}'.format(
        SOURCE_ENDPOINT,
        SOURCE_PATH,
        DESTINATION_ENDPOINT,
        DESTINATION_PATH
    ))

# Start driver function

if __name__ == '__main__':
    main()
