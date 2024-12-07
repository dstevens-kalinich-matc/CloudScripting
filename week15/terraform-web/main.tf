# Specify the Terraform provider configuration
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">=5.0"
    }
  }
}

# Define the AWS provider with default profile and region
provider "aws" {
  profile = "default"
  region  = var.region
}

# Data source to grab the list of availability zones in the specified region
data "aws_availability_zones" "available" {
  state = "available"
  filter {
    name   = "zone-type"
    values = ["availability-zone"]
  }
}

# VPC module from Terraform Registry
module "vpc" {
    source = "terraform-aws-modules/vpc/aws"

    # Dynamically assign all availability zones
    azs = data.aws_availability_zones.available.names

    name = "derek-vpc"

    #Automatically assign public IPs to instances in public subnets
    map_public_ip_on_launch = "true"

    cidr = "10.0.0.0/16"

    # Pass subnets from variables
    public_subnets  = var.public_subnets
    private_subnets = var.private_subnets
}

# Security group module for allowing HTTP traffic
module "http_80_security_group" {
  source  = "terraform-aws-modules/security-group/aws//modules/http-80"
  version = "~> 5.0"
  name    = "web-sg"

  # Attach the security group to the VPC created
  vpc_id  = module.vpc.vpc_id

  # Define custom ingress rule
  ingress_with_cidr_blocks = [
    {
      from_port = 80
      to_port = 80
      protocol = "tcp"
      description = "Allow all HTTP traffic"
      cidr_blocks = "0.0.0.0/0"
    }
  ]
  # Let the VPC finish creating before running module
  depends_on = [module.vpc]
}

# Data source to get the latest Amazon Linux 2 AMI
data "aws_ami" "amazon_linux" {
    most_recent = true
    owners = ["amazon"]

    filter {
        name = "name"
        # Provided - Same listed in both instructions and documentation
        values = ["amzn2-ami-hvm-*-x86_64-gp2"]
    }
}

# Module from Terraform Registry
module "ec2_instance" {
    source  = "terraform-aws-modules/ec2-instance/aws"
    name = "derek-webserver"
    
    instance_type = "t2.micro"
    key_name = "vockey"
    monitoring = true

    # Attach the HTTP security group
    vpc_security_group_ids = [module.http_80_security_group.security_group_id]

    # Use the first instance in public subnet list
    subnet_id = module.vpc.public_subnets[0]

    # Use init-script for userdata
    user_data = templatefile("${path.module}/init-script.sh", {
        file_content = "Derek Stevens-Kalinich"
    })
}