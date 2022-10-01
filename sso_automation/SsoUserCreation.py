import boto3
from botocore.exceptions import ClientError
from csv import reader
import datetime

class SsoUserCreation():

    def __init__(self, region, intance_arn, admin_arn, readonly_arn, IdentityStoreId, email):
        self.intance_arn = intance_arn
        self.region = region
        self.admin_arn = admin_arn
        self.readonly_arn = readonly_arn
        self.IdentityStoreId = IdentityStoreId
        self.email = email
        self.client_s3 = boto3.client('s3', region_name = self.region)
        self.client_idstore = boto3.client('identitystore', region_name = self.region)
        self.client_sso = boto3.client('sso-admin', region_name = self.region)
        self.client_ses = boto3.client('ses', region_name= self.region)
        self.mail_content  = ''

    def list_groups(self):
        existing_group = []
        response = self.client_idstore.list_groups(IdentityStoreId=self.IdentityStoreId)
        existing_group.extend(response['Groups'])
        while response.get('Groups') and response['Groups'] and response.get('NextToken'):
            response = self.client_idstore.list_groups(IdentityStoreId=self.IdentityStoreId, NextToken=response['NextToken'])
            existing_group.extend(response['Groups'])
        return existing_group

    def list_users(self):
        existing_user = []
        response = self.client_idstore.list_users(IdentityStoreId=self.IdentityStoreId)
        existing_user.extend(response['Users'])
        while response.get('Users') and response['Users'] and response.get('NextToken'):
            response = self.client_idstore.list_users(IdentityStoreId=self.IdentityStoreId, NextToken=response['NextToken'])
            existing_user.extend(response['Users'])
        return existing_user

    def create_group(self, group):
        try:
            response = self.client_idstore.create_group(
                    IdentityStoreId=self.IdentityStoreId,
                    DisplayName=group['DisplayName']
                )
        except ClientError as e:
            print(e.response['Error'])
            self.mail_content += "create_group failed {}\n" .format(str(e.response['Error']))
            return False
        return response

    def update_group_ownership(self, userid, grp_response):
        print("update_group_ownership {} {}" .format(userid, grp_response))
        self.mail_content += "update_group_ownership {} {} \n" .format(str(userid), str(grp_response))
        try:
            response = self.client_idstore.create_group_membership(
                            IdentityStoreId=self.IdentityStoreId,
                            GroupId=grp_response['GroupId'],
                            MemberId={
                                'UserId': userid
                            }
                        )
        except ClientError as e:
            print(e.response['Error'])
            self.mail_content += "create_group_membership failed {} \n" .format(str(e.response['Error']))
            return False
        return True

    def create_account_assignmet(self, data, grp_response):
        role_arn = self.admin_arn if ( data[0][6].lower() == "sandbox" or data[0][6].lower() == "poc" ) else self.readonly_arn
        aws_account = data[0][5].strip('"')
        try:
            response = self.client_sso.create_account_assignment(
                                InstanceArn=self.intance_arn,
                                TargetId=aws_account,
                                TargetType='AWS_ACCOUNT',
                                PermissionSetArn=role_arn,
                                PrincipalType='GROUP',
                                PrincipalId=grp_response['GroupId']
                        )
        except ClientError as e:
            print(e.response['Error'])
            self.mail_content += "create_account_assignment failed {} \n" .format(str(e.response['Error']))
            return False
        print("Group {} has been added to the account {}" .format(grp_response['GroupId'], data[0][4]))
        self.mail_content += "Group {} has been added to the account {} \n" .format(grp_response['GroupId'], aws_account)
    def create_user(self, users, data, grp_response):
        for user in users:
            try:
                response = self.client_idstore.create_user(
                        IdentityStoreId=self.IdentityStoreId,
                        UserName=user[2],
                        Name = {
                            'GivenName' : user[0],
                            'FamilyName' : user[1]
                        },
                        DisplayName = user[0] + ' ' + user[1],
                        Emails = [{
                            'Value': user[2]
                        }
                        ]
                    )
            except ClientError as e:
                print(e.response['Error'])
                self.mail_content += "create_user failed {} \n" .format(str(e.response['Error']))
                return False
            print("user {} has been added. Adding to group" .format(user[2]))
            self.mail_content += "user {} has been added. Adding to group \n" .format(user[2])
            

            if self.update_group_ownership(response['UserId'], grp_response):
                print("group update has been completed")
                self.mail_content += "group update has been completed \n"

    def check_user_group(self, data):
        found_existing_group = False
        existing_user, existing_group = self.list_users(), self.list_groups()
        # print("existing user {}" .format(existing_user))
        # print("existing group {}" .format(existing_group))
        self.mail_content += "{} <Check_user_group stage > {} \n" .format(str(existing_user), str(existing_user))
        group_name = data[0][3] + '-' + data[0][4]
        for grp in existing_group:
            if group_name in grp.values():
                 found_existing_group = grp

        if not found_existing_group:
            print("group not exist, creating it {}" .format(data[0][3]))
            self.mail_content += "group not exist, creating it {} \n" .format(data[0][3])
            group_name = {'DisplayName' : group_name }
            grp_response = self.create_group(group_name)
        else:
            print("group exist {}" .format(found_existing_group))
            self.mail_content += "group exist {} \n" .format(str(found_existing_group))
            grp_response = found_existing_group

        new_user = list()
        for user in data:
            found_existing_user = False
            for ex_user in existing_user:
                if ex_user['UserName'] == user[2]:
                    found_existing_user = True
                    break
            if not found_existing_user:
                new_user.append(user)
        
        if new_user:
            print("found new user {}, Adding it" .format(str(new_user)))
            self.mail_content += "found new user {}, Adding it \n" .format(str(new_user))
            response = self.create_user(new_user, data, grp_response)
        else:
            print("All users are existing. No action needed")
            self.mail_content += "All users are existing. No action needed \n"
            response = "All users are existing. No action needed"
        return self.create_account_assignmet(data, grp_response)

    def parse_data(self, data):
        csv_reader = reader(data)
        line_count = 0
        data = list()
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue
            sanity = [x.lower() for x in row]
            data.append(sanity)
        data = [ x for x in data if any(x)]
        print(data)
        return self.check_user_group(data)

    def download_csv_from_s3(self, event):
        try:
            bucket = event['Records'][0]['s3']['bucket']['name']
            key = event['Records'][0]['s3']['object']['key']
            response_s3 = self.client_s3.get_object(Bucket=bucket, Key=key)
            response = response_s3['Body'].read().decode('utf-8').split('\n')
        except ClientError as e:
            print(e.response['Error'])
            self.mail_content += "{} <SSOUserADD Get_bject stage > {}\n" .format(datetime.datetime.today().strftime("%Y/%m/%d %I:%M:%S"), str(e.response['Error']))
            return False
        return self.parse_data(response)

    def send_email(self, content):
        self.client_ses.send_email(Source=self.email,Destination={'ToAddresses': [self.email]}, Message={'Subject': {'Charset': 'UTF-8','Data': 'SSO UserAdd AWS Console Access'},'Body': {'Text': {'Charset': 'UTF-8','Data': content}}})


    def main_hanlder(self, event):
        print(event)
        result =self.download_csv_from_s3(event)
        print("Sending email")
        self.send_email(self.mail_content)