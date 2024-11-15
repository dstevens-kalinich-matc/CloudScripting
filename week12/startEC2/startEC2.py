import boto3
import json
# Define the AWS region where the resources are located
region = 'us-east-1'
# Create an EC2 client using Boto3 for interacting with the EC2 service
ec2 = boto3.client('ec2', region_name=region)
# Define the Lambda function handler
def lambda_handler(event, context):
    # Describe EC2 instances with a filter to list only running instances
    response = ec2.describe_instances(

        Filters=[
        {
            'Name': 'instance-state-name',
            'Values': [
            'stopped',
            ]
        },
    ],
    )

    listofinstanceids = []
    # Iterate through the response to extract instance details
    for reservation in response["Reservations"]:
        instances = reservation["Instances"]
        for instance in instances:
            print(instance["InstanceId"])
            listofinstanceids.append(instance["InstanceId"])

    start_response = "Nothing needed to be started"

    if len(listofinstanceids) != 0:
        start_response = ec2.start_instances(InstanceIds=listofinstanceids,DryRun=False)
        print(start_response)
        # Return a success response with the API call details
        return {
            'statusCode': 200,
            'body': json.dumps(start_response)
        }