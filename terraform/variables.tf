variable "aws_region" {
  description = "AWS region for the infrastructure."
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Deployment environment."
  type        = string
  default     = "development"

  validation {
    condition     = contains(["development", "staging", "production"], var.environment)
    error_message = "Environment must be development, staging, or production."
  }
}

variable "owner" {
  description = "Infrastructure owner."
  type        = string
  default     = "finops-team"
}

variable "ami_id" {
  description = "AMI ID used by the EC2 instance."
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type."
  type        = string
  default     = "m5.2xlarge"
}

variable "root_volume_size" {
  description = "Root EBS volume size in GiB."
  type        = number
  default     = 30

  validation {
    condition     = var.root_volume_size >= 8
    error_message = "Root volume size must be at least 8 GiB."
  }
}

variable "data_volume_size" {
  description = "Additional EBS data volume size in GiB."
  type        = number
  default     = 50

  validation {
    condition     = var.data_volume_size >= 10
    error_message = "Data volume size must be at least 10 GiB."
  }
}

variable "vpc_cidr" {
  description = "VPC CIDR block."
  type        = string
  default     = "10.20.0.0/16"
}

variable "subnet_cidr" {
  description = "Public subnet CIDR block."
  type        = string
  default     = "10.20.1.0/24"
}

variable "availability_zone" {
  description = "Availability zone for the subnet and EBS volume."
  type        = string
  default     = "us-east-1a"
}

variable "http_port" {
  description = "HTTP port exposed by the web server."
  type        = number
  default     = 80
}
