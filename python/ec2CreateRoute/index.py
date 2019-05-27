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
    
    try:
        # Create an EC2 Route.
        ec2 = boto3.client('ec2')

        ec2.create_route(
            DestinationCidrBlock=event['ResourceProperties']['DestinationCidrBlock'],
            TransitGatewayId=event['ResourceProperties']['TransitGatewayId'],
            RouteTableId=event['ResourceProperties']['RouteTableId'],
        )
    
    except Exception as e:
        print(e)
    
    return


@helper.update
def update(event, context):
    logger.info("Got Update")
    
    try:
        # Replace an EC2 Route.
        ec2 = boto3.client('ec2')

        ec2.replace_route(
            DestinationCidrBlock=event['ResourceProperties']['DestinationCidrBlock'],
            TransitGatewayId=event['ResourceProperties']['TransitGatewayId'],
            RouteTableId=event['ResourceProperties']['RouteTableId'],
        )
    
    except Exception as e:
        print(e)
    
    return


@helper.delete
def delete(event, context):
    logger.info("Got Delete")

    # Delete an EC2 Route.
    try:
        ec2 = boto3.client('ec2')

        ec2.delete_route(
            DestinationCidrBlock=event['ResourceProperties']['DestinationCidrBlock'],
            RouteTableId=event['ResourceProperties']['RouteTableId'],
        )
    except Exception as e:
        print(e)



@helper.poll_create
def poll_create(event, context):
    logger.info("Got create poll")
    return True


# Lambda Handler
def lambda_handler(event, context):
    helper(event, context)