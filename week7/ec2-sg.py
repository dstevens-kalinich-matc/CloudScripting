#!/usr/bin/env python3

import boto3,botocore,argparse

ec2client = boto3.client('ec2')

# Set up argument parsing to accept a security group name from the user
parser = argparse.ArgumentParser(description='Argument to supply security group.')
parser.add_argument('-s', '--security-group', dest='argSG', default='',type=str, help='Enter known security group')
args = parser.parse_args()

# Capture the information for all security groups
allSG = ec2client.describe_security_groups()

# Check if the user provided 'default' as the security group name
if args.argSG == 'default':
    print('Default group configured to allow all traffic')
# If a specific security group name is provided
elif args.argSG:
    try:
        # Capture information on specified security group using its name
        argGroup = ec2client.describe_security_groups(GroupNames=[args.argSG])
        # Iterate through the details of the specified security group
        for configList in argGroup['SecurityGroups']:
            print(f"Security Group: {configList['GroupName']}")
            # Retrieving the group ID for specific security group
            groupID = configList['GroupId']
            # Retrieve detailed rules for the security group using its GroupId
            response = ec2client.describe_security_group_rules(Filters=[{'Name': 'group-id', 'Values': [groupID]}])
            # Loop through each rule in the security group
            for rules in response['SecurityGroupRules']:
                # Check if the rule is for inbound traffic then print inbout traffic information
                if rules['IsEgress'] == False:
                    print(f"    - IP Range: {rules['CidrIpv4']}")
                    print(f"    - From Port: {rules['FromPort']}")
                    print(f"    - To Port: {rules['ToPort']}")
                    if rules['CidrIpv4'] == '0.0.0.0/0':
                        print('WARNING: Open to the public internet!')
    # Handle the exception if the specified security group does not exist
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'InvalidGroup.NotFound':
            print(f"Error: The security group '{args.argSG}' does not exist.")
        else:
            print(f"Unexpected client error occurred: {error}")
# If no specific security group is provided, list all security groups
else:
    for secGroup in allSG['SecurityGroups']:
        print(f"Security Group: {secGroup['GroupName']}")
        
        # Iterate through each inbound rule for the security group
        for config in secGroup['IpPermissions']:
            for range in config['IpRanges']:
                SgIpRange = range['CidrIp']
                fromPort = config['FromPort']
                toPort = config['ToPort']
                print(f"   - IP Range: {SgIpRange}\n   - From Port: {fromPort}\n   - To Port: {toPort}")

