variable "environment" {
  type = string
}

variable "owner" {
  type = string
}

variable "ami_id" {
  type = string
}

variable "instance_type" {
  type = string
}

variable "root_volume_size" {
  type = number
}

variable "data_volume_size" {
  type = number
}

variable "vpc_cidr" {
  type = string
}

variable "subnet_cidr" {
  type = string
}

variable "availability_zone" {
  type = string
}

variable "http_port" {
  type = number
}
