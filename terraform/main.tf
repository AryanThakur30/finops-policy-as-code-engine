module "finops_stack" {
  source = "./modules/finops_stack"

  environment       = var.environment
  owner             = var.owner
  ami_id            = var.ami_id
  instance_type     = var.instance_type
  root_volume_size  = var.root_volume_size
  data_volume_size  = var.data_volume_size
  vpc_cidr          = var.vpc_cidr
  subnet_cidr       = var.subnet_cidr
  availability_zone = var.availability_zone
  http_port         = var.http_port
}
