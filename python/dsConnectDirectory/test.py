import boto3
import os
import time
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

# Get the Status of a directory
def get_directory_stage(client, directoryId):
    for directory in client.describe_directories()['DirectoryDescriptions']:
        if directory['Type'] == "ADConnector" and directory['DirectoryId'] == directoryId:
            return directory['Stage']

def create(event):
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
    
    # Sim Output
    print({"DirectoryId": response['DirectoryId']})
    return

def delete(event):
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



event = {
    "ResourceProperties" : {
        "Name" : "myDirectory",
        "ShortName" : "myDirectory",
        "Password" : "string",
        "Description" : "string",
        "Size" : "small",
        "VpcId" : "string",
        "Subnet1" : "string",
        "Subnet2" : "string",
        "DNS1" : "string",
        "DNS2" : "string",
        "CustomerUserName" : "Admin"
    }
}
 
# create(event)
# delete(event)
