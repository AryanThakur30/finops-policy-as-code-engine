terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.61.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  access_key = "test"
  secret_key = "test"

  endpoints {
    ec2                  = "http://localhost.localstack.cloud:4566"
    iam                  = "http://localhost.localstack.cloud:4566"
    sts                  = "http://localhost.localstack.cloud:4566"
    s3                   = "http://localhost.localstack.cloud:4566"
    cloudwatch           = "http://localhost.localstack.cloud:4566"
    elasticloadbalancing = "http://localhost.localstack.cloud:4566"
  }

  default_tags {
    tags = {
      Project     = "finops-policy-as-code-engine"
      Environment = var.environment
      Owner       = var.owner
      ManagedBy   = "terraform"
    }
  }
}
