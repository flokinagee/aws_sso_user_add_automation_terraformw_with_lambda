provider "aws" {
  version                 = ">= 2.0"
  region                  = var.aws_region
  profile                 = "default"
  shared_credentials_file = "/Users/mahaakutty/.aws/credentials_hashitalks"

}