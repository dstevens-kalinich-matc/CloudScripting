/* Configure the Terraform cloud settings*/
terraform {
    cloud {
        organization = "dstevens-kalinich-scripting"
        workspaces {
            name = "Derek-Workspace"
        }
    }
    required_providers {
        aws = {
            source = "hashicorp/aws"
            version = ">=5.0"
        }
    }
    required_version = ">= 0.14.9"
}
/* Define the AWS provider configuration*/
provider "aws" {
    region = "us-east-1"
}
/* Reference an existing IAM role in AWS*/
data "aws_iam_role" "lab_role" {
    name = "LabRole"
}
/* Create an AWS Lambda function*/
resource "aws_lambda_function" "test_lambda2"{
    filename = "startEC2.zip"
    function_name = "DerekStartFunction"
    role = data.aws_iam_role.lab_role.arn
    runtime = "python3.9"
    handler = "startEC2.lambda_handler"
}