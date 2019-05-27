import boto3
import os
import logging
from crhelper import CfnResource
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
# Initialise the helper, all inputs are optional, this example shows the defaults
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
        logger.info("Got Create")

        # Shares a Directory with target account.
        ds = boto3.client('ds')
        accounts = event['ResourceProperties']['ShareTargetIds']
        for account in accounts:
            ds.share_directory(
                DirectoryId=event['ResourceProperties']['DirectoryId'],
                ShareNotes=event['ResourceProperties']['ShareNotes'],
                ShareTarget={
                    'Id': account,
                    'Type': 'ACCOUNT'
                },
                ShareMethod='HANDSHAKE'
            )

        return

    except Exception as e:
        print(e)


# Triggers on Cloudformation Update Events.
@helper.update
def update(event, context):
    logger.info("Got Update")


# Triggers on Cloudformation Delete Events.
@helper.delete
def delete(event, context):
# Unshares a Directory with target account.
    try:
        logger.info("Got Delete")

        # Unshares a Directory with target account.
        client = boto3.client('ds')    
        accounts = event['ResourceProperties']['ShareTargetIds']
        for account in accounts:
            client.unshare_directory(
                DirectoryId=event['ResourceProperties']['DirectoryId'],
                UnshareTarget={
                    'Id': account,
                    'Type': 'ACCOUNT'
                }
            )

    except Exception as e:
        print(e)



@helper.poll_create
def poll_create(event, context):
    logger.info("Got create poll")
    # Return a resource id or True to indicate that creation is complete. if True is returned an id will be generated
    return True


# Lambda Handler
def lambda_handler(event, context):
    # print(event)
    helper(event, context)

# lambda_handler('foo','bar')