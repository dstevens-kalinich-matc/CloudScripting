#!/usr/bin/env python3

import boto3, datetime

# Creating an IAM client
IAMclient = boto3.client('iam')

# Saving the list of roles to a variable
roles = IAMclient.list_roles()['Roles']

# Creating a variable to act as the 90 cutoff date
cutOffDate = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=90)

# Iterating through the list of roles
for role in roles:

    # Checking each role to see if it was created in the last 90 days
    if role['CreateDate'] > cutOffDate:
        print(f"Role: {role['RoleName']} -- Created: {role['CreateDate']}")
        # Handle potential exceptions while retrieving policies
        try:
            # Using list_role_policies to capture a list of unmanaged policies
            unmanagedPolicies = IAMclient.list_role_policies(RoleName=role['RoleName'])
            # Printing each unmanaged policy associated to the role
            for policyName in unmanagedPolicies['PolicyNames']:
                print(f"    - Unmanaged Policy Name: {policyName}")

            # Using list_attached_role_policies to capture a list of managed policies
            managedPolicies = IAMclient.list_attached_role_policies(RoleName=role['RoleName'])
            # Printing each managed policy associated to the role
            for policyName in managedPolicies['AttachedPolicies']:
                print(f"    - Managed Policy Name: {policyName['PolicyName']}")
        # Handle cases where no policy found for role
        except IAMclient.exceptions.NoSuchEntityException:
            print(f"      No policies found for {role['RoleName']}")
        # Handle access denial errors
        except IAMclient.exceptions.ClientError as error:
            if error.response['Error']['Code'] == 'AccessDenied':
                print(f"      Access denied when trying to retrieve policies for {role['RoleName']}")
            # Handle any other client errors that occur
            else:
                print(f"      An error occured: {error.response['Error']['Code']}")
