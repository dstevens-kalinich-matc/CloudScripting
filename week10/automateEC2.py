#!/usr/bin/env python3
import boto3,botocore

ec2Client = boto3.client('ec2')

def Stop_EC2():
    # Describe EC2 instances filtered by 'dev' tag
    response = ec2Client.describe_instances(
        Filters=[
            {
                'Name':'tag:env',
                'Values':['dev']
            }
        ]
    )
    instanceList = []
    # Capturing individual instance IDs
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instanceList.append(instance['InstanceId'])
            instanceId = instance['InstanceId']
        try:
            # Attempt to stop the specified EC2 instance
            stopResponse = ec2Client.stop_instances(InstanceIds=[instanceId])
            print(f"Instance stopped: {instanceId}")
        # Handle error if stopping fails
        except botocore.exceptions.ClientError as error:
            stopResponse = f"Instance {instanceId} could not be stopped\nError: {error}"
    return stopResponse

def Start_EC2():
    # Describe EC2 instances filtered by 'dev' tag
    response = ec2Client.describe_instances(
        Filters=[
            {
                'Name':'tag:env',
                'Values':['dev']
            }
        ]
    )
    instanceList = []
    # Capturing individual instance IDs
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instanceList.append(instance['InstanceId'])
            instanceId = instance['InstanceId']
        try:
            # Attempt to start the specified EC2 instance
            startResponse = ec2Client.start_instances(InstanceIds=[instanceId])
            print(f"Instance started: {instanceId}")
        # Handle error if stopping fails
        except botocore.exceptions.ClientError as error:
            startResponse = f"Instance {instanceId} could not be started\nError: {error}"
    return startResponse

# Execute the main function when the script is run directly
def main():
    #stopIdList = Stop_EC2()
    #print(stopIdList)
    startIdList = Start_EC2()
    #print(startIdList)

if __name__ == '__main__':
    main()