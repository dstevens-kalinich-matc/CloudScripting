#!/usr/bin/env python3

import boto3
#Creating S3 client
s3client = boto3.client('s3')
#Using client to list all buckets in account
response = s3client.list_buckets()
#Iterating through list of buckets, and printing the value for the name
for bucket in response['Buckets']:
    print(f"Bucket name: {bucket['Name']}")