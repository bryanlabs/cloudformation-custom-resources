import boto3
import os
import time
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


def create(event):
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

def delete(event):
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



event = {
    "ResourceProperties" : {
        "DestinationCidrBlock" : "myDirectory",
        "TransitGatewayId" : "myDirectory",
        "RouteTableId" : "string"
    }
}
 
# create(event)
# delete(event)
