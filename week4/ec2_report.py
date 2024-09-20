#!/usr/bin/env python3

import boto3, csv

#Function to retrieve EC2 instance info based on provided key (Name), and value (Value) filters
def Get_Instances(Name,Value):
    #Empty list to capture response information
    response = []
    ec2Client = boto3.client('ec2')
    paginator = ec2Client.get_paginator('describe_instances')
    
    #Filter instances based on provided arguments, and create a PageIterator object
    pageList = paginator.paginate(
        Filters=[
            {
                'Name': Name,
                'Values': [
                    Value,
                ]
            },
        ],
    )
    #Turning PageIterator object into a dictionary 
    for page in pageList:
        #Iterating through instances and appending them to the response list
        for reservation in page['Reservations']:
            response.append(reservation)

    return response

#Funtion to write instance details to CSV file
def CSV_Writer(header,content):
    with open('export.csv','w') as csvFile:
        #Use DictWriter to format dictionaries into CSV format
        writer = csv.DictWriter(csvFile,fieldnames=header)
        writer.writeheader()
        for line in content:
            writer.writerow(line)

def main():

    #Run function to capture list of instance info
    instancesList = Get_Instances('instance-type', 't2.micro')

    #Setting header for CSV
    header = ['InstanceId', 'InstanceType', 'State', 'PublicIpAddress', 'MonitoringState', 'InstanceName']
    #List of information to be converted into CSV format
    content = []

    #Iterate through instances list to extract relevant info to append to content list
    for instance in instancesList:
        for ec2 in instance['Instances']:
            #Capturing instance name from tags if it or tags exists
            if 'Tags' in ec2:
                for tag in ec2['Tags']:
                    if tag['Key'] == 'Name':
                        instanceName = tag['Value']
            else:
                instanceName = 'N/A'
            #Appending relevant information to content list
            content.append(
                {
                    "InstanceId": ec2['InstanceId'],
                    "InstanceType": ec2['InstanceType'],
                    "State": ec2['State']['Name'],
                    "PublicIpAddress": ec2.get('PublicIpAddress','N/A'),
                    "MonitoringState": ec2['Monitoring']['State'],
                    "InstanceName": instanceName
                }
            )
            print(f"Instance Name: {instanceName}\nMonitoring State: {ec2['Monitoring']['State']}\n")

    CSV_Writer(header,content)
    
#Ensures the main function runs only when script is run directly
if __name__ == '__main__':
    main()
