# Caminho: infra/provider.tf

terraform {
  required_version = ">= 1.5.0"

  backend "s3" {
    bucket         = "titanic-api-terraform-state-414813662184"
    key            = "infra/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "titanic-api-terraform-lock"
    encrypt        = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}