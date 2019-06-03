import boto3
import os
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

def create(event):
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

def delete(event):
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


event = {
    "ResourceProperties" : {
        "ShareTargetIds" : ["121212121212","212121212121"],
        "DirectoryId" : "d-90671c4dd3",
        "ShareNotes" : "my Shared Directory"
    }
}
 
# create(event)
# delete(event)