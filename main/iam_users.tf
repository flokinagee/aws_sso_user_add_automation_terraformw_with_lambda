resource "aws_iam_user" "naga" {
  name = "naga"
  path = "/users/"

}

resource "aws_iam_user_group_membership" "naga_developers" {
  user = aws_iam_user.naga.name

  groups = [
    aws_iam_group.developers.name
  ]
}

resource "aws_iam_user" "mano" {
  name = "mano"
  path = "/users/"

}

resource "aws_iam_user_group_membership" "mano_developers" {
  user = aws_iam_user.mano.name

  groups = [
    aws_iam_group.developers.name
  ]
}