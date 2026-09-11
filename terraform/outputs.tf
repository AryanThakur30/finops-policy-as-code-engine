output "vpc_id" {
  description = "ID of the FinOps VPC."
  value       = module.finops_stack.vpc_id
}

output "subnet_id" {
  description = "ID of the application subnet."
  value       = module.finops_stack.subnet_id
}

output "security_group_id" {
  description = "ID of the web security group."
  value       = module.finops_stack.security_group_id
}

output "instance_id" {
  description = "ID of the FinOps EC2 instance."
  value       = module.finops_stack.instance_id
}

output "instance_private_ip" {
  description = "Private IP address of the EC2 instance."
  value       = module.finops_stack.instance_private_ip
}

output "data_volume_id" {
  description = "ID of the additional EBS data volume."
  value       = module.finops_stack.data_volume_id
}
