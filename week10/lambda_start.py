#!/usr/bin/env python3
import boto3

IAMclient = boto3.client('iam')
lambdaClient = boto3.client('lambda')

def Create_Lambda(functionName):
    roleResponse = IAMclient.get_role(RoleName='LabRole')

    with open('lambda_start_function.zip','rb') as handler:
        codeZipped = handler.read()
    
    functionResponse = lambdaClient.create_function(
        FunctionName=functionName,
        Role=roleResponse['Role']['Arn'],
        Publish=True,
        PackageType='Zip',
        Runtime='python3.9',
        Code={
            'ZipFile':codeZipped
        },
        Handler='lambda_start_function.lambda_handler'
    )

def main():
    functionName = 'startEC2'
    try:
        existingFunction = lambdaClient.get_function(FunctionName=functionName)
        print("Function already exists.")
    except:
        print("Creating function.")
        functionResponse = Create_Lambda(functionName)


if __name__ in '__main__':
    main()