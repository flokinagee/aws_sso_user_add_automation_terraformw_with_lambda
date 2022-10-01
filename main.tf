terraform {
  backend "s3" {}
}

data "aws_caller_identity" "current" {}

locals  {
  tags = {
  Terraform = "True"
}
}