terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

provider "aws" {
  region     = var.aws_region
  access_key = "test"
  secret_key = "test"

  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    ec2 = "http://localhost.localstack.cloud:4566"
  }
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "environment" {
  type    = string
  default = "development"
}

variable "owner" {
  type    = string
  default = "finops-lab"
}

variable "ami_id" {
  type        = string
  description = "AMI ID for the selected AWS region"
}

resource "aws_instance" "cost_killing_test" {
  ami           = var.ami_id
  instance_type = "m5.2xlarge"

  tags = {
    Name        = "finops-cost-killing-test"
    Environment = var.environment
    Owner       = var.owner
    Project     = "finops-policy-engine"
    CostCenter  = "CC-1001"
    ManagedBy   = "terraform"
    FinOpsPolicy = "enforced"
  }
}