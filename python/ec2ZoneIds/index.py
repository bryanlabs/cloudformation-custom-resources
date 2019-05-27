import boto3
import os
import logging
from crhelper import CfnResource
from botocore.exceptions import ClientError

# Ensure OS env variables are in place.

logger = logging.getLogger(__name__)
# Initialise the helper, all inputs are optional, this example shows the defaults
helper = CfnResource(json_logging=False, log_level='INFO', boto_level='CRITICAL')

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


@helper.create
def create(event, context):
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


@helper.update
def update(event, context):
    logger.info("Got Update")


@helper.delete
def delete(event, context):
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





@helper.poll_create
def poll_create(event, context):
    logger.info("Got create poll")
    # Return a resource id or True to indicate that creation is complete. if True is returned an id will be generated
    return True


# Lambda Handler
def lambda_handler(event, context):
    print(event)
    helper(event, context)

