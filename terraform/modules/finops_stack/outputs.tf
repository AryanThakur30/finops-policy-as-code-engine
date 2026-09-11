output "vpc_id" {
  value = aws_vpc.main.id
}

output "subnet_id" {
  value = aws_subnet.public.id
}

output "security_group_id" {
  value = aws_security_group.web.id
}

output "instance_id" {
  value = aws_instance.web.id
}

output "instance_private_ip" {
  value = aws_instance.web.private_ip
}

output "data_volume_id" {
  value = aws_ebs_volume.data.id
}
