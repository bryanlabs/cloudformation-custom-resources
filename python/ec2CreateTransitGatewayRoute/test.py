import boto3
import os
import time
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


def create(event):
    logger.info("Got Create")
    
    try:
        # Get TransitgatewayID.
        ec2 = boto3.client('ec2')
        response = ec2.describe_transit_gateways(
            TransitGatewayIds=[
                event['ResourceProperties']['TransitGatewayId'],
            ]
        )
        
        # Create the route.
        ec2.create_transit_gateway_route(
            DestinationCidrBlock=event['ResourceProperties']['DestinationCidrBlock'],
            TransitGatewayRouteTableId=response['TransitGateways'][0]['Options']['AssociationDefaultRouteTableId'],
            TransitGatewayAttachmentId=event['ResourceProperties']['TransitGatewayAttachmentId'],
            Blackhole=False
        )
    
    except Exception as e:
        print(e)
    
    return

def delete(event):
    logger.info("Got Delete")

    # Delete an EC2 Route to TransitGateway.
    try:
        ec2 = boto3.client('ec2')
        response = ec2.describe_transit_gateways(
            TransitGatewayIds=[
                event['ResourceProperties']['TransitGatewayId'],
            ]
        )

        # Create the route.
        ec2.delete_transit_gateway_route(
            DestinationCidrBlock=event['ResourceProperties']['DestinationCidrBlock'],
            TransitGatewayRouteTableId=response['TransitGateways'][0]['Options']['AssociationDefaultRouteTableId']
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
