#!/usr/bin/env python3
import json,boto3,botocore
ec2Client = boto3.client('ec2')
def Stop_EC2():
    response = ec2Client.describe_instances()
    # List to track started instances
    stoppedInstanceList = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instanceId = instance['InstanceId']
        try:
            stopResponse = ec2Client.stop_instances(InstanceIds=[instanceId])
            stoppedInstanceList.append(instance['InstanceId'])
            #print(f"Instance stopped: {instanceId}")
        except botocore.exceptions.ClientError as error:
            stopResponse = f"Instance {instanceId} could not be stopped\nError: {error}"
    return stoppedInstanceList
def lambda_handler(even,context):
    #TODO implement
    # Lambda function handler
    # Call Start_EC2 to start instances and capture the result
    stoppedInstances = Stop_EC2()
    print(stoppedInstances)
    return{
        'statusCode':200,
        'body':json.dumps('Hello from Lambda!')
    }
