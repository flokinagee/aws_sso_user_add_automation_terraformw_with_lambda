include "state" {
  path = find_in_parent_folders("state.hcl")
}


inputs = {
  sso = {
    name = "sso-user-add-automation"
    admin_arn = "arn:aws:sso:::permissionSet/ssoins-821083b25daa61f7/ps-dfcd094b8006531b"
    readonly_arn = "arn:aws:sso:::permissionSet/ssoins-821083b25daa61f7/ps-581218224c3582b9"
    region = "ap-southeast-1"
    intance_arn = "arn:aws:sso:::instance/ssoins-i8567Ddasa876"
    IdentityStoreId = "d-9878746dhj9"
    email = "<email>@email.com"
  }
}
