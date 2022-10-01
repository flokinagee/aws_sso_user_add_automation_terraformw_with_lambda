resource "aws_cloudwatch_log_group" "lambda_sso" {
  name              = "/aws/lambda/lambda_${var.sso.name}"
  retention_in_days = 0
}

# See also the following AWS managed policy: AWSLambdaBasicExecutionRole
resource "aws_iam_policy" "lambda_sso_policy" {
  name        = "${var.sso.name}-policy"
  description = "${var.sso.name} policy"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "s3:GetObject",
        "identitystore:List*",
        "identitystore:Create*",
        "sso:CreateAccountAssignment",
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents",
        "ses:Send*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_sso_attach" {
  role       = aws_iam_role.lambda_sso_role.name
  policy_arn = aws_iam_policy.lambda_sso_policy.arn
}
resource "aws_iam_role" "lambda_sso_role" {
  name = "${var.sso.name}-lambda-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

######
resource "aws_lambda_function" "sso_user_add" {
  function_name = "lambda_${var.sso.name}"
  filename = "sso_automation/build.zip"
  source_code_hash = filebase64sha256("sso_automation/build.zip")
  role          = aws_iam_role.lambda_sso_role.arn
  handler       = "main.lambda_handler"
  runtime       = "python3.9"
  timeout       = 600

  # ... other configuration ...
  depends_on = [
    aws_iam_role_policy_attachment.lambda_sso_attach,
    aws_cloudwatch_log_group.lambda_sso
  ]
  environment {
    variables = {
      admin_arn = var.sso.admin_arn
      readonly_arn = var.sso.readonly_arn
      region = var.sso.region
      intance_arn = var.sso.intance_arn
      IdentityStoreId = var.sso.IdentityStoreId
      email = var.sso.email

    }
  }

}
#########
resource "aws_s3_bucket" "sso_user_add_bkt" {
  bucket = var.sso.name
  acl    = "private"
  tags = local.tags
}

resource "aws_lambda_permission" "allow_bucket" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.sso_user_add.arn
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.sso_user_add_bkt.arn
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.sso_user_add_bkt.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.sso_user_add.arn
    events              = ["s3:ObjectCreated:*"]
  }

  depends_on = [aws_lambda_permission.allow_bucket]
}
#########