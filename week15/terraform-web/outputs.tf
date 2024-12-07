output "public_IP_Address" {
    description = "Public IP of web server"
	value = module.ec2_instance.public_ip
}

output "vpc_id" {
  value = module.vpc.vpc_id
}