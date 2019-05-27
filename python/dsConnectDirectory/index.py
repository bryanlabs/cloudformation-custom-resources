import boto3
import os
import logging
import time
from crhelper import CfnResource
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
helper = CfnResource(json_logging=False, log_level='INFO', boto_level='CRITICAL')

try:
    ## Init code goes here
    pass
except Exception as e:
    helper.init_failure(e)

# Get the Status of a directory
def get_directory_stage(client, directoryId):
    for directory in client.describe_directories()['DirectoryDescriptions']:
        if directory['Type'] == "ADConnector" and directory['DirectoryId'] == directoryId:
            return directory['Stage']

# Triggers on Cloudformation Create Events.
@helper.create
def create(event, context):
    logger.info("Got Create")
    
    try:
        # Create AD Connector
        ds = boto3.client('ds')
        response = ds.connect_directory(
            Name=event['ResourceProperties']['Name'],
            ShortName=event['ResourceProperties']['ShortName'],
            Password=event['ResourceProperties']['Password'],
            Description=event['ResourceProperties']['Description'],
            Size=event['ResourceProperties']['Size'],
            ConnectSettings={
                'VpcId': event['ResourceProperties']['VpcId'],
                'SubnetIds': [
                    event['ResourceProperties']['Subnet1'],
                    event['ResourceProperties']['Subnet2'],
                ],
                'CustomerDnsIps': [
                    event['ResourceProperties']['DNS1'],
                    event['ResourceProperties']['DNS2'],
                ],
                'CustomerUserName': event['ResourceProperties']['CustomerUserName'],
            },
            Tags=[
                {
                    'Key': 'Name',
                    'Value': event['ResourceProperties']['Name'],
                },
            ]
        )
    
    except Exception as e:
        print(e)
    
    # Add DirectoryId to Stack Outputs
        helper.Data.update({"DirectoryId": response['DirectoryId']})
    
    return

# Triggers on Cloudformation UpdateEvents.
@helper.update
def update(event, context):
    logger.info("Got Update")

# Triggers on Cloudformation Delete Events.
@helper.delete
def delete(event, context):
    logger.info("Got Delete")
    
    # Delete AD Connector
    try:
        ds = boto3.client('ds')
        for directory in ds.describe_directories()['DirectoryDescriptions']:
            if directory['Type'] == "ADConnector":
                
                # Delete the Directory
                status = ds.delete_directory(
                    DirectoryId=directory['DirectoryId']
                )
                print(status)

                # Wait for Directory to delete.
                while get_directory_stage(ds,directory['DirectoryId']) != None:
                    print(directory['DirectoryId'] + ': ' + get_directory_stage(ds,directory['DirectoryId']))
                    time.sleep(30)
                
                # Deleted associated network interfaces
                try:
                    ec2 = boto3.client('ec2')
                    for int in ec2.describe_network_interfaces()['NetworkInterfaces']:
                        if directory['DirectoryId'] in int['Description']:
                            status = ec2.delete_network_interface(
                                NetworkInterfaceId=int['NetworkInterfaceId']
                            )
                            print(status)
                except Exception as e:
                    print(e)
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