#!/usr/bin/env python3
import json,boto3,botocore
ec2Client = boto3.client('ec2')
def Start_EC2():
    response = ec2Client.describe_instances()
    # List to track started instances
    startedInstanceList = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instanceId = instance['InstanceId']
        try:
            startResponse = ec2Client.start_instances(InstanceIds=[instanceId])
            startedInstanceList.append(instance['InstanceId'])
            #print(f"Instance started: {instanceId}")
        except botocore.exceptions.ClientError as error:
            startesponse = f"Instance {instanceId} could not be started\nError: {error}"
    return startedInstanceList
def lambda_handler(even,context):
    #TODO implement
    # Lambda function handler
    # Call Start_EC2 to start instances and capture the result
    startedInstances = Start_EC2()
    print(startedInstances)
    return{
        'statusCode':200,
        'body':json.dumps('Hello from Lambda!')
    }
