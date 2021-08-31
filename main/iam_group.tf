resource "aws_iam_group" "developers" {
  name = "developers"
  path = "/"
}

resource "aws_iam_group_policy_attachment" "assume_developer_role" {
        for_each = aws_iam_policy.policy
        group      = aws_iam_group.developers.name
        policy_arn =  each.value.arn
        # count      = length(aws_iam_policy.policy)
        # group      = aws_iam_group.developers.name
        # policy_arn =  "aws_iam_policy.policy.arn
        # #policy_arn = element(aws_iam_policy.policy.*.arn, count.index)
        # # policy_arn = "${aws_iam_policy.policy.arn}"
}