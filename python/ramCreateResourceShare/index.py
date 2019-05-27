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


@helper.create
def create(event, context):
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



@helper.update
def update(event, context):
    logger.info("Got Update")
    logger.info(event)
    # If the update resulted in a new resource being created, return an id for the new resource. CloudFormation will send
    # a delete event with the old id when stack update completes


@helper.delete
def delete(event, context):
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




@helper.poll_create
def poll_create(event, context):
    logger.info("Got create poll")
    # Return a resource id or True to indicate that creation is complete. if True is returned an id will be generated
    return True


# Lambda Handler
def lambda_handler(event, context):
    print(event)
    helper(event, context)
