provider "aws" {
  version                 = ">= 2.0"
  region                  = var.aws_region
  profile                 = "default"
  shared_credentials_file = "<home-dir>.aws/credentials_hashitalks"

}
