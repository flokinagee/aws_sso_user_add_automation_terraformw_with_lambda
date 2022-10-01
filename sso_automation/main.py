import os
from SsoUserCreation import SsoUserCreation as MainClass
import settings


def lambda_handler(event, context):
    admin_arn = os.environ['admin_arn']
    readonly_arn = os.environ['readonly_arn']
    region = os.environ['region']
    intance_arn = os.environ['intance_arn']
    IdentityStoreId = os.environ['IdentityStoreId']
    email = os.environ['email']

    sso_user = MainClass(region, intance_arn, admin_arn, readonly_arn, IdentityStoreId, email)
    return sso_user.main_hanlder(event)