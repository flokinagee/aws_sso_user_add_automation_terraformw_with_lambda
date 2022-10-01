import main
import unittest
from io import BytesIO
from botocore.response import StreamingBody
from unittest import mock

class SSOUserAddtest(unittest.TestCase):
    event = {
        'Records' : [{
            's3' : {
                'bucket' : {
                    'name' : 'test-naga'
                },
                'object': {
                    'key': 'naga.csv'
                }
            }
        }]
    }

    def mock_get_object(self, *args, **kwargs):
        print("kwargs {}" .format(kwargs))
        with open('naga.csv') as f:
            data = f.read()
            data_mock  = data.encode("utf-8")
            raw_data = StreamingBody(BytesIO(data_mock), len(data_mock))      
        return { 'Body': raw_data }


    def mock_list_users(self, *args, **kwargs):
        print("kwargs {}" .format(kwargs))
        data   =   {
                    'Users': [
                    {
                        'UserName': 'nagarajan@email.com',
                        'UserId': 'stdagasdgagring',
                    },
                    {
                        'UserName': 'adsgadg@email.com',
                        'UserId': 'stdagasdgagring',
                    },
                   {
                        'UserName': 'adfagagsa@email.com',
                        'UserId': 'stdagasdgagring',
                    }
                ]
            }
        return data

    def mock_list_groups(self, *args, **kwargs):
        print("kwargs {}" .format(kwargs))
        data   = { "Groups" :[ {
                                'GroupId': '342452525',
                                'IdentityStoreId': 'i-dgkjsdgh',
                                'DisplayName': 'string'
        },{
                                'GroupId': 'xxxxxxx',
                                'IdentityStoreId': 'i-dgkjsdgh',
                                'DisplayName': 'gwb'
        }
        ]
                                                    }
        return data

    def mock_create_user(self, *args, **kwargs):
        print("kwargs {}" .format(kwargs))
        data   ={
                'UserId': 'string',
                'IdentityStoreId': 'string'
        }
        return data

    def mock_create_group(self, *args, **kwargs):
        print("kwargs {}" .format(kwargs))
        data   = {
                'GroupId': 'Sucess',
                'IdentityStoreId': 'string'
            }
                                                            
        return data



    def mock_send_email(self, *args, **kwargs):
        print("kwargs {}" .format(kwargs))
        data   = {
            'MessageId': 'string'
                }                                            
        return data

    def mock_create_account_assignment(self, *args, **kwargs):
        print("kwargs {}" .format(kwargs))
        data   = {
                'AccountAssignmentCreationStatus': {
                    'Status': 'SUCCEEDED',
                    'RequestId': 'string',
                    'FailureReason': 'string',
                    'TargetId': 'string',
                    'TargetType': 'AWS_ACCOUNT',
                    'PermissionSetArn': 'string',
                    'PrincipalType': 'GROUP',
                    'PrincipalId': 'string'
                }
        }
        return data

    @mock.patch('SsoUserCreation.boto3')
    def test_all(self, mock_boto3):
        mock_boto3.client('ses').send_email.side_effect = self.mock_send_email
        mock_boto3.client('s3').get_object.side_effect  = self.mock_get_object
        mock_boto3.client('identitystore').list_users.side_effect = self.mock_list_users
        mock_boto3.client('identitystore').list_groups.side_effect = self.mock_list_groups
        mock_boto3.client('identitystore').create_user.side_effect = self.mock_create_user
        mock_boto3.client('identitystore').create_group.side_effect = self.mock_create_group
        mock_boto3.client('sso-admin').create_account_assignmet.side_effect = self.mock_create_account_assignment
        main.lambda_handler(self.event, context=None)

if __name__ == '__main__':
    unittest.main(verbosity=9)
