import boto3
import os
import logging
from crhelper import CfnResource
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
helper = CfnResource(json_logging=False, log_level='INFO', boto_level='CRITICAL')

try:
    ## Init code goes here
    pass
except Exception as e:
    helper.init_failure(e)

# Triggers on Cloudformation Create Events.
@helper.create
def create(event, context):
    try:
        # Accept a Shared Directory
        ds = boto3.client('ds')
        for directory in ds.describe_directories()['DirectoryDescriptions']:
            if directory['Type'] == 'SharedMicrosoftAD':
                response = ds.accept_shared_directory(
                    SharedDirectoryId=directory['DirectoryId']
                )
                print(response)

    except Exception as e:
        print(e)
    
    # Add Shared DirectoryID to Stack Outputs
    helper.Data.update({"SharedDirectoryId": directory['DirectoryId']})

    return

# Triggers on Cloudformation Update Events.
@helper.update
def update(event, context):
    logger.info("Got Update")


# Triggers on Cloudformation Delete Events.
@helper.delete
def delete(event, context):
    try:
        logger.info("Got Delete")

        # Delete a Shared Directory
        ds = boto3.client('ds')
        for directory in ds.describe_directories()['DirectoryDescriptions']:
            if directory['Type'] == 'SharedMicrosoftAD':
                response = ds.delete_directory(
                    DirectoryId=directory['DirectoryId']
                )
                print(response)

    except Exception as e:
        print(e)

@helper.poll_create
def poll_create(event, context):
    logger.info("Got create poll")
    # Return a resource id or True to indicate that creation is complete. if True is returned an id will be generated
    return True


# Lambda Handler
def lambda_handler(event, context):
    helper(event, context)