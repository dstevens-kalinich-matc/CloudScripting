#!/usr/bin/env python3

import boto3
import ec2,sns

DRYRUN = False

# Retrieve account id of IAM user making call
stsClient = boto3.client('sts')
accountId = stsClient.get_caller_identity()['Account']

# Generating an EC2 instance via using functions from ec2.py
ec2Client = boto3.client('ec2')
ImageId = ec2.Get_Image(ec2Client)
InstanceId = ec2.Create_EC2(ImageId,ec2Client)

# Variables for SNS topic and email subscription
topic = 'DerekStevens-KalinichTopic'
SubEmail = 'dstevens-kalinich@madisoncollege.edu'

# Create SNS topic and subscribe email
topicARN = sns.CreateSNSTopic(topic)
subscription = sns.SubscribeEmail(topicARN,SubEmail)

# Set up CloudWatch client for alarm creation
CWclient = boto3.client('cloudwatch')

# Create a CloudWatch alarm for high CPU utilization to trigger EC2 reboot
alarmResponse = CWclient.put_metric_alarm(
    AlarmName='Web_Server_Reboot',
    ComparisonOperator='GreaterThanOrEqualToThreshold',
    EvaluationPeriods=2,
    MetricName='CPUUtilization',
    Namespace='AWS/EC2',
    Period=300,
    Statistic='Average',
    Threshold=70.0,
    ActionsEnabled=True,
    AlarmActions=[
        f'arn:aws:swf:us-east-1:{accountId}:action/actions/AWS_EC2.InstanceId.Reboot/1.0',
        f'arn:aws:sns:us-east-1:{accountId}:{topic}'
    ],
    AlarmDescription='Alarm when server CPU is higher than 70 percent reboot',
    Dimensions=[{'Name': 'InstanceId','Value': InstanceId}]
)
