variable "region" {
    type = string
    default = "us-east-1"
    description = "Region for server."
}

variable "public_subnets" {
    type = list(string)
    default = ["10.0.1.0/24","10.0.2.0/24"]
    description = "List of public subnets."
}

variable "private_subnets" {
    type = list(string)
    default = ["10.0.101.0/24","10.0.102.0/24"]
    description = "List of private subnets."
}