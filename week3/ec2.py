#!/usr/bin/env python3

import boto3
#Creating a variable for dry run use
DRYRUN = False

#Function with a single arument to find images with selected features using an EC2 client, 
#then returning the image ID of the image at the top of the list
def Get_Image(ec2client):
    #Use of the EC2 client argument
    imagesResponse = ec2client.describe_images(
        Filters=[
            {
                'Name': 'description',
                'Values': ['Amazon Linux 2 AMI*']
            },
            {
                'Name': 'architecture',
                'Values': ['x86_64']
            },
            {
                'Name': 'owner-alias',
                'Values': ['amazon']
            }
        ]
    )
    return imagesResponse['Images'][0]['ImageId']

#Function to create an instance with specifications using an EC2 client and image ID as arguments,
#then returning the instance ID
def Create_EC2(AMI,ec2client):
    #Use of EC2 client argument
    response = ec2client.run_instances(
        #Use of image ID argument in creating instance
        ImageId=AMI,
        InstanceType='t2.micro',
        MaxCount=1,
        MinCount=1,
        DryRun=DRYRUN
    )
    return response['Instances'][0]['InstanceId']

#Main function to test other created functions and print information
def main():
    #Creating an EC2 client for use in functions and interacting with AWS
    client = boto3.client('ec2')
    #Running the previously creating function and saving the returned image ID for use in creating an instance
    AMI = Get_Image(client)
    
    #Running the previously created function and printing the created EC2's instance ID
    instanceId = Create_EC2(AMI, client)
    print(f"Instance ID: {instanceId}")
    #Creating an EC2 resource to interact with AWS at a higher level
    ec2 = boto3.resource('ec2')
    instance = ec2.Instance(instanceId)

    print(f"Before wait for instance to run status: {instance.state['Name']}")
    instance.wait_until_running()
    instance.load()
    print(f"Instance after wait status: {instance.state['Name']}")
    print(f"Instance Public IP Address: {instance.public_ip_address}")
    #Creating tag
    instance.create_tags(
        Tags=[
            {
                'Key': 'Name',
                'Value': 'Derek'
            },
        ]
    )
    print(f"Instance Tags: {instance.tags}")
    instance.terminate()
    print(f"Instance waiting to terminate status: {instance.state['Name']}")
    instance.wait_until_terminated()
    instance.load()
    print(f"Instance after terminating status: {instance.state['Name']}")

#Ensures the main function runs only when this script is run directly
if __name__ == '__main__':
    main()