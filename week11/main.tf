terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }
  required_version = ">= 0.14.9"
}
provider "aws" {
  profile = "default"
  region  = "us-east-1"
}
resource "aws_instance" "app_server" {
  ami           = "ami-0866a3c8686eaeeba"
  instance_type = "t2.micro"
  key_name = "vockey"
  vpc_security_group_ids = [aws_security_group.web-sg.id]
  tags = {
    Name = var.instance_name
  }
}
resource "aws_security_group" "web-sg" {
	name = "web-sg"
	ingress {
		from_port = 80
		to_port = 80
		protocol = "tcp"
		cidr_blocks = ["0.0.0.0/0"]
	}
	ingress {
		from_port = 22
		to_port = 22
		protocol = "tcp"
		cidr_blocks = ["0.0.0.0/0"]
	}
	egress {
		from_port = 0
		to_port = 0
		protocol = "-1"
		cidr_blocks = ["0.0.0.0/0"]
	}
}