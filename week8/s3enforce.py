#!/usr/bin/env python3

import boto3

# Function to create an S3 bucket
def CreateBucket(bucketName):
    s3client = boto3.client('s3')
    response = s3client.create_bucket(Bucket=bucketName)
    return response

# Function to delete an S3 bucket
def DeleteBucket(bucketName):
    s3client = boto3.client('s3')
    response = s3client.delete_bucket(Bucket=bucketName)
    return response

# Function to enforce versioning on an S3 bucket
def EnforceVersioning(bucketName):
    s3client = boto3.client('s3')
    response = s3client.put_bucket_versioning(
        Bucket=bucketName,
        VersioningConfiguration={
            'MFADelete': 'Disabled',
            'Status': 'Enabled',
            }
    )
    return response

# Function to set a bucket policy
def SetBucketPolicy(bucketName, policy):
    s3client = boto3.client('s3')
    response = s3client.put_bucket_policy(Bucket=bucketName,Policy=policy)
    return response

# Main function to create bucket and enforce versioning
def main():
    bucketName = 'dereksk-functiontest'
    nameResponse = CreateBucket(bucketName)
    versioningResponse = EnforceVersioning(bucketName)

if __name__ == '__main__':
    main()