import boto3
import os
import logging

from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

# Shares a Directory with target account.
def create(event):
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

def delete(event):
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

event = {
    "ResourceProperties" : {
        "ShareTargetIds" : ["546837296206","430151054399"],
        "DirectoryId" : "d-90671c4dd3",
        "ShareNotes" : "my Shared Directory"
    }
}
 
# create(event)
# delete(event)