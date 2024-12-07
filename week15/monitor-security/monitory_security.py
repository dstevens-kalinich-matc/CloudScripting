#!/usr/bin/env python3
import boto3
from botocore.exceptions import ClientError

# Create an EC2 instance to interact with the AWS 
ec2client = boto3.client('ec2')

# Retrieve a list of EC2 instances and their associated security groups.
def ec2SgList():
    try:
        # Grab information of all instances
        ec2response = ec2client.describe_instances()
    # Incase of trouble getting instance information
    except ClientError as e:
        print(f"Error retrieving EC2 instances: {e}")
        return []
    # List to add istance IDs to
    instanceList = []
    # Parse response to retieve instance IDs and their security groups
    for reservation in ec2response['Reservations']:
        for instances in reservation['Instances']:
            instanceId = instances['InstanceId']
            for securityGroups in instances['SecurityGroups']:
                SgId = securityGroups['GroupId']
                # Add instance ID and security group to list as a dictionary
                instanceList.append({'InstanceId':instanceId,'SgId':SgId})
    return instanceList

# Function to examine a security group and revoke 'SSH from anywhere' rule
# Input variable is SG to check
def checkSG(securityGroup):
    try:
        # Get details of the specified SG
        response = ec2client.describe_security_groups(GroupIds=[securityGroup])
    # Handle errors in retrieval
    except ClientError as e:
        print(f"Error fetching Security Group {securityGroup}: {e}")
        return
    # Iterate over SG details to find ingress rules
    for sg in response['SecurityGroups']:
        if sg['IpPermissions']:
            # Ingress rules
            for IPpermission in sg['IpPermissions']:
                rulePort = IPpermission['FromPort']
                if rulePort == 22:
                    print(f"Port 22 open to everywhere in Security Group: {securityGroup}")
                    # Investigate if the SSH rule allows all, if it does, remoke it
                    for CidrRule in IPpermission['IpRanges']:
                        cidr = CidrRule['CidrIp']
                        if cidr == '0.0.0.0/0' and rulePort == 22:
                            print("Rule must be revoked...")
                            # Removing rule
                            stopResponse = ec2client.revoke_security_group_ingress(
                                GroupId=securityGroup,
                                IpPermissions=[{
                                    'IpProtocol': 'tcp',
                                    'FromPort': 22,
                                    'ToPort': 22,
                                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                                }]
                            )
                            print(f"Ingress rule removed: {stopResponse['Return']}\n")
                        # If there is a port 22 rule but it doesn't allow everything, that is ok
                        elif rulePort == 22 and cidr != '0.0.0.0/0':
                            print(f"Port 22 open to IP: {cidr}\n")
                else:
                    print(f"Ingress rule does not include port 22 in Security Group: {securityGroup}\n")        
        else:
            print(f"No Ingress Rules in Security group: {securityGroup}\n")

def main():
    """
    Main function to identify and address overly permissive ingress rules.
    - Retrieves all EC2 instances and their security groups.
    - Analyzes each security group for port 22 ingress rules.
    """
    print("Checking Security Groups for Ingress rules with port 22 open...")

    # Retrieve a list of all instances and their associated security groups
    instances = ec2SgList()

    # Process each security group associated with the instances
    for instance in instances:
        SgId = instance['SgId']
        SGresponse = checkSG(securityGroup=SgId)
        if SGresponse:
            print(SGresponse)
  
# Script executed only when run directly
if __name__ == '__main__':
    main()