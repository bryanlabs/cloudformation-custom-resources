import boto3
import os
import time
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

def create(event):
    logger.info("Got Create")
    
    # Create a resource share.
    try:
        ram = boto3.client('ram')
        ram.create_resource_share(
            name=event['ResourceProperties']['Name'],
            resourceArns=event['ResourceProperties']['ResourceArns'],
            principals=event['ResourceProperties']['Principals'],
            tags=[
                {
                    'key': 'Name',
                    'value': 'Share'
                },
            ]
        )
    
    except Exception as e:
        print(e)
    
    return

def delete(event):
    logger.info("Got Delete")

    # Delete a resource share.
    try:
        ram = boto3.client('ram')

        resource_shares = ram.get_resource_shares(
            name='Share',
            resourceOwner='SELF'
        )

        
        for share in resource_shares['resourceShares']:
            arn = share['resourceShareArn']
            ram.delete_resource_share(
                    resourceShareArn=arn
            )

    except Exception as e:
        print(e)



event = {
    "ResourceProperties" : {
        "Name" : "Name",
        "ResourceArns" : ["d-90671c4dd3"],
        "Principals" : ["my Shared Directory"]
    }
}

# create(event)
# delete(event)
