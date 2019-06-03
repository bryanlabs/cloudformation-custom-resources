# ec2ZoneIds



**ec2ZoneIds** - Creates a Mapping of Zone Names to Zone Ids in SSM. This Allows you to specify the ZoneId instead of Zone Name in your templates.

Example:  

````
AvailabilityZone1:
    ConstraintDescription: Must be a valid zone
    Description: The first zone in the region
    Type : 'AWS::SSM::Parameter::Value<AWS::EC2::AvailabilityZone::Name>'
    Default: /azinfo/use1-az2
````