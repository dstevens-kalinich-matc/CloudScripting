#!/usr/bin/env python3

import boto3

def CreateSNSTopic(topicName):
    snsClient = boto3.client('sns')
    snsResponse = snsClient.create_topic(Name=topicName)
    return snsResponse['TopicArn']

def SubscribeEmail(topicARN,email):
    snsClient = boto3.client('sns')
    snsResponse = snsClient.subscribe(TopicArn=topicARN,Protocol='email',Endpoint=email)
    return snsResponse['SubscriptionArn']