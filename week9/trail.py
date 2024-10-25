#!/usr/bin/env python3

import boto3,s3enforce,json

# Function to create a CloudTrail or start logging if the trail already exists
def CreateTrail(trailName,bucketName):
    trailClient = boto3.client('cloudtrail')
    # Try to create a new CloudTrail linked to the specified S3 bucket
    try:
        trailResponse = trailClient.create_trail(S3BucketName=bucketName,Name=trailName)
        return trailResponse
    # If the trail already exists, start logging for the existing trail
    except trailClient.exceptions.TrailAlreadyExistsException as error:
        response = trailClient.start_logging(Name=trailName)
        return response

# Function to start logging on trail
def StartLogging(trailName):
    trailClient = boto3.client('cloudtrail')
    startResponse = trailClient.start_logging(Name=trailName)
    return startResponse

# Function to stop logging on trail
def StopLogging(trailName):
    trailClient = boto3.client('cloudtrail')
    stopResponse = trailClient.stop_logging(Name=trailName)
    return stopResponse

# Function to get status of trail
def GetTrailStatus(trailName):
    trailClient = boto3.client('cloudtrail')
    # If the function runs correctly, return the status of logging
    try:
        statusResponse = trailClient.get_trail_status(Name=trailName)
        return statusResponse['IsLogging']
    # If trying to get status of non-existing trail give clear message why function does not work
    except trailClient.exceptions.TrailNotFoundException as error:
        print("That trail name does not exist.")
        raise NameError("That Cloudtrail Trail was not found")
    # If any other error occurs print
    except:
        print("Some other error occured.")

def main():
    bucketName = 'dereksk-ctv1'
    trailName = 'dereksk-trailName-v1'
    
    # Retrieve account ID of IAM user making call
    stsClient = boto3.client('sts')
    accountId = stsClient.get_caller_identity()['Account']

    # Define the S3 bucket policy to allow CloudTrail to write logs and check bucket ACLs
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AWSCloudTrailAclCheck20150319",
                "Effect": "Allow",
                "Principal": {"Service": "cloudtrail.amazonaws.com"},
                "Action": "s3:GetBucketAcl",
                "Resource": f"arn:aws:s3:::{bucketName}"
            },
            {
                "Sid": "AWSCloudTrailWrite20150319",
                "Effect": "Allow",
                "Principal": {"Service": "cloudtrail.amazonaws.com"},
                "Action": "s3:PutObject",
                "Resource": f"arn:aws:s3:::{bucketName}/AWSLogs/{accountId}/*",
                "Condition": {"StringEquals": {"s3:x-amz-acl": "bucket-owner-full-control"}}
            }
        ]
    }
    # Create the S3 bucket for CloudTrail logs
    createBucketResponse = s3enforce.CreateBucket(bucketName)

    # Convert the bucket policy to JSON and apply it to the bucket
    policyStr = json.dumps(policy)
    bucketPolicyResponse = s3enforce.SetBucketPolicy(bucketName,policyStr)

    # Create the CloudTrail or start logging if it already exists
    createTrailResponse = CreateTrail(trailName,bucketName)
    #stopResponse = StopLogging(trailName)

    # Call status function
    statusResponse = GetTrailStatus(trailName)

    # If status is true display message
    if statusResponse:
        print(f"Logging for {trailName} is already enabled.")
    # If false, start logging and display message
    else:
        StartLogging(trailName)
        print(f"Initializing logging for trail: {trailName}")

if __name__ == '__main__':
    main()