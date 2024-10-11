#!/usr/bin/env python3

# Description: This script gathers information on EBS volumes in the AWS account.
# It checks if volumes are encrypted and whether they are attached to EC2 instances.
# The script prints the volume details and issues warnings for unencrypted volumes.

import boto3,botocore

ec2client = boto3.client('ec2')

try:
    # Retrieve details of all EBS volumes in the AWS account
    volumes = ec2client.describe_volumes()
    # Iterate through each volume in the list of volumes
    for volume in volumes['Volumes']:
        print(f"Volume ID: {volume['VolumeId']}")
        print(f"    - Volume Size: {volume['Size']}")
        print(f"    - State: {volume['State']}")
        print(f"    - Availability Zone: {volume['AvailabilityZone']}")
        print(f"    - Encrypted: {volume['Encrypted']}")
        # If the volume is not encrypted, print a warning message
        if volume['Encrypted'] == False:
            print(f"WARNING: Volume {volume['VolumeId']} is not encrypted!")
        # If the volume's state is 'in-use', it means the volume is attached to an instance
        if volume['State'] == 'in-use':
            print(f"    - Attachment Information:")
            # Iterate through the list of attachments to provide details about each attachment.
            for data in volume['Attachments']:
                print(f"        - Instance ID: {data['InstanceId']}")
                print(f"        - Device: {data['Device']}")
        print('\n')
except botocore.exceptions.ClientError as error:
    # Handle general ClientError exceptions.
    if error.response['Error']['Code'] == 'UnauthorizedOperation':
        print("You don't have permission to access EC2 volume information.")
    else:
        print(f"Error retrieving volume information: {error}")
except Exception as e:
    # Catch any other exceptions that may occur.
    print(f"An unexpected error occurred: {e}")