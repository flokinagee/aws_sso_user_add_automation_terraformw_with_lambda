resource "aws_iam_policy" "policy" {
        for_each = var.aws_account_ids 

        name        = "assume_${each.key}_env_developer_role"
        path        = "/"
        description = "My test policy"

        # Terraform's "jsonencode" function converts a
        # Terraform expression result to valid JSON syntax.
        policy = jsonencode({
            Version = "2012-10-17"
            Statement = [
            {
                Action = [
                "sts:AssumeRole",
                ]
                Effect   = "Allow"
                Resource = "arn:aws:iam::${each.value}:role/developers"
            },
            ]
        })
}