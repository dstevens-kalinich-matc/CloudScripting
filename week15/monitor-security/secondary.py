#!/usr/bin/env python3

import boto3

ec2client = boto3.client('ec2')

ec2response = ec2client.describe_instances()

instanceList = []
print("Checking Security Groups for open port 22 in Ingress Rules...")
for reservation in ec2response['Reservations']:
    #print(reservation['Instances'])
    for instances in reservation['Instances']:
        instanceId = instances['InstanceId']
        #print(instanceId)
        for securityGroups in instances['SecurityGroups']:
            SgId = securityGroups['GroupId']
            try:
                response = ec2client.describe_security_group_rules(Filters=[{'Name':'group-id','Values':[SgId]}])
                for SgRule in response['SecurityGroupRules']:
                    print(SgRule['SecurityGroupRuleId'])
            except Exception as e:
                print(e)
#             instanceList.append({'InstanceId':instanceId,'SgId':SgId})
#             SGresponse = ec2client.describe_security_groups(GroupIds=[SgId])          
#             for securityGroup in SGresponse['SecurityGroups']:
#                 for IPpermission in securityGroup['IpPermissions']:
#                     rulePort = IPpermission['FromPort']
#                     if rulePort == 22:
#                         print(f"Port 22 open in Security Group: {SgId}")
#                     #print(IPpermission['IpRanges'])
#                     for CidrRule in IPpermission['IpRanges']:
#                         cidr = CidrRule['CidrIp']
#                         if cidr == '0.0.0.0/0' and rulePort == 22:
#                             print("Rule must be revoked")
#                         else:
#                             print(f"Open to IP: {cidr}")


# def SgRuleId(securityGroup):
#     response = ec2client.describe_security_group_rules(Filters=[{'Name':'group-id','Values':[securityGroup]}])
#     for SgRule in response['SecurityGroupRules']:
#         return SgRule['SecurityGroupRuleId']

