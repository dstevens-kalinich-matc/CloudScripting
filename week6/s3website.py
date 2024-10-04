#!/usr/bin/env python3

#Importing modules
import boto3,json,argparse,random,botocore,string

#Creating an s3 client using boto3, creating a variable to act as a name for a bucket
#Client allows for communication with Amazon S3
s3client = boto3.client('s3')
bucketName = 'dstevens-kalinich-week6-web'

#Argument parser to add bucket name when calling script
parser = argparse.ArgumentParser(description="Argument to provide name for s3website.")
parser.add_argument('-s', '--siteName', dest='siteName', default='',type=str, help='Enter unique bucket name for new s3website')
args = parser.parse_args()

#If there is no argument provided, generate a random string and append it to the default bucket name
#Otherwise use the argument as the bucket name
if not args.siteName:
    bucketName += "".join(random.choices(string.ascii_lowercase, k=10))
    print(f"No name was provided, random name will be generated: {bucketName}")
else:
    print(f"You provided bucket name: {args.siteName}")
    bucketName = args.siteName
try:
    #Creating a bucket, and ensuring public access to bucket
    createResponse = s3client.create_bucket(Bucket=bucketName)
    s3client.delete_public_access_block(Bucket=bucketName)

    #Creating a bucket policy using JSON
    bucketPolicy = {
        'Version': '2012-10-17',
        'Statement': [{
            'Sid': 'AddPerm',
            'Effect': 'Allow',
            'Principal': '*',
            'Action': ['s3:GetObject'],
            'Resource': "arn:aws:s3:::%s/*" % bucketName
        }]
    }

    #Turning json object into a string
    bucketPolicyStr = json.dumps(bucketPolicy)

    #Using the S3 client to set the policy for the created bucket and saving Amazon S3's response to a variable
    bucket_policy_response = s3client.put_bucket_policy(
        Bucket=bucketName,
        Policy=bucketPolicyStr
    )

    #Using the S3 client to set the configuration of a website and saving Amazon S3's response to a variable
    #Setting the html files for use with the website
    put_bucket_response = s3client.put_bucket_website(
        Bucket=bucketName, 
        WebsiteConfiguration={
        'ErrorDocument': {'Key': 'error.html'},
        'IndexDocument': {'Suffix': 'index.html'},
        }
    )

    #Opening index.html in read bytes to add the file to the bucket using the S3 client and saving Amazon S3's response to a variable
    indexFile = open('index.html', 'rb')
    indexResponse = s3client.put_object(Body=indexFile, Bucket=bucketName, Key='index.html', ContentType='text/html')
    indexFile.close()
    #print(indexResponse)

    #Opening error.html in read bytes to add the file to the bucket using the S3 client and saving Amazon S3's response to a variable
    errorFile = open('error.html', 'rb')
    errorResponse = s3client.put_object(Body=errorFile, Bucket=bucketName, Key='error.html', ContentType='text/html')
    errorFile.close()
    #print(errorResponse)

    #Using the S3 client grab a list containing all buckets in account
    buckets = s3client.list_buckets()['Buckets']

    #Iterating through each bucket in the list
    for bucket in buckets:
        #Grabbing individual bucket names to list their objects
        bucketName = bucket['Name']
        #Using S3 client to grab bucket object information
        objectsResponse = s3client.list_objects_v2(Bucket=bucketName)
        #If the bucket has objects then:
        if objectsResponse['KeyCount'] > 0:
            print(f"{bucketName}:")
            #Iterating through list of objects
            for bucketObject in objectsResponse['Contents']:
                #print(bucketObject)
                #Saving the object name and printing it
                objectName = (bucketObject['Key'])
                print(objectName)
        #If bucket has no objects, print bucket name and that fact
        else:
            print(f"{objectsResponse['Name']} \nContains no objects")

#Catching service client exception
except s3client.exceptions.BucketAlreadyExists as err:
    print(f"Bucket {bucketName} already exists, try another name or enter nothing to generate random bucket name".format(err.response['Error']['BucketName']))

#Use botocore to catch specific exceptions print statements for them
except botocore.exceptions.ClientError as error:
    if error.response['Error']['Code'] == 'InvalidToken':
        print('Credentials not up to date, please update to continue')
    ##############
    # CATCHES EXCEPTION AS WELL
    ##############    
    # elif error.response['Error']['Code'] == 'BucketAlreadyExists':
    #     print(f"Bucket {bucketName} already exists, try another name or enter nothing to generate random bucket name")
