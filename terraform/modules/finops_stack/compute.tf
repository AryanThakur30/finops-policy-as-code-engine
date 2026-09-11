resource "aws_instance" "web" {
  ami                         = var.ami_id
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.public.id
  vpc_security_group_ids      = [aws_security_group.web.id]
  associate_public_ip_address = true

  root_block_device {
    volume_type = "gp3"
    volume_size = var.root_volume_size
  }

  tags = {
    Name = "finops-${var.environment}-web"
    Tier = "application"
  }
}

resource "aws_ebs_volume" "data" {
  availability_zone = var.availability_zone
  size              = var.data_volume_size
  type              = "gp3"

  tags = {
    Name = "finops-${var.environment}-data"
    Tier = "storage"
  }
}

resource "aws_volume_attachment" "data" {
  device_name = "/dev/sdf"
  volume_id   = aws_ebs_volume.data.id
  instance_id = aws_instance.web.id
}
