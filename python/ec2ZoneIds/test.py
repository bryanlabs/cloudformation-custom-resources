import boto3
import os
import time
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

# Returns AZ Zone Name from ZoneId.
def get_zonename_from_zoneid(mappings,fzoneid):
    for item in mappings['AvailabilityZones']:
        if item['ZoneId'] == fzoneid:
            return item['ZoneName']

# Creates ZoneIdMapping SSM Parameter.
def create_zonename_param(ssm,zoneid,mappings):    
    zonename = get_zonename_from_zoneid(mappings,zoneid)
    return ssm.put_parameter(
        Name='/azinfo/' + zoneid,
        Description=zonename,
        Value=zonename,
        Type='String',
        Overwrite=True,
        Tier='Standard'
    )

# Deletes ZoneIdMapping SSM Parameter.
def delete_zonename_param(ssm,zoneid):
    return ssm.delete_parameter(
        Name='/azinfo/' + zoneid
    )

def create(event):
    logger.info("Got Create")
    
    try:
        ec2 = boto3.client('ec2')
        ssm = boto3.client('ssm')
        mappings = ec2.describe_availability_zones()
        for item in mappings['AvailabilityZones']:
            create_zonename_param(ssm,(item['ZoneId']),mappings)
    
    except Exception as e:
        print(e)
    
    return

def delete(event):
    logger.info("Got Delete")

    # Delete an EC2 Route.
    try:
        ec2 = boto3.client('ec2')
        ssm = boto3.client('ssm')
        mappings = ec2.describe_availability_zones()
        for item in mappings['AvailabilityZones']:
            delete_zonename_param(ssm,(item['ZoneId']))

    except Exception as e:
        print(e)



event = {}
 
# create(event)
# delete(event)
