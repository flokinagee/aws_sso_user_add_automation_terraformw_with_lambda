# Automate User group creation in AWS SSO for console access

## It will be suitable for who dont want to sync AD objects (onprem or external idp) into AWS SSO for console access

### what it will do
1) fill up the csv ("Firstname,Lastname,Email,BU,Entity,Account ID,Envioment") and drop it in S3 bucket 

2) S3 event driven configured to invoke lambda

3) Lambda process the CSV to create User Groun into AWS SSO

4) It will add group and permision set to respective account

5) Result will be sent in email (SES)

People can then access the the account via sso diretory link or ADFS if it is integrated

## Terraform / Terragrunt

### All resource are created via terraform that you can see in root directory
sso_automation.tf

#### terragrunt init
####  terragrung plan
####  terragrunt apply

### Lambda configuration can be found at sso_automation/

#### 1) make test (for test case)


NagarajansMBP2:sso_automation naga$ make test

python3 test_SsoUserCreation.py

test_all (__main__.SSOUserAddtest) ... {'Records': [{'s3': {'bucket': {'name': 'test-naga'}, 'object': {'key': 'naga.csv'}}}]}

kwargs {'Bucket': 'test-naga', 'Key': 'naga.csv'}

[['nagarjan', 'soong ', 'naga@emai.com', 'gwb', 'sg-company', '123456789101', 'sit']]

kwargs {'IdentityStoreId': 'd-874568437653'}

kwargs {'IdentityStoreId': 'd-874568437653'}

group not exist, creating it gwb

kwargs {'IdentityStoreId': 'd-874568437653', 'DisplayName': 'gwb-sg-company'}

found new user [['nagarjan', 'soong ', 'naga@emai.com', 'gwb', 'sg-company', '123456789101', 'sit']], Adding it

kwargs {'IdentityStoreId': 'd-874568437653', 'UserName': 'naga@emai.com', 'Name': {'GivenName': 'nagarjan', 'FamilyName': 'soong '}, 'DisplayName': 'nagarjan soong ', 'Emails': [{'Value': 'naga@emai.com'}]}

user naga@emai.com has been added. Adding to group

update_group_ownership string {'GroupId': 'Sucess', 'IdentityStoreId': 'string'}

group update has been completed

Group Sucess has been added to the account sg-company

Sending email

kwargs {'Source': 'nagamanokaran@email.com', 'Destination': {'ToAddresses': ['nagamanokaran@email.com']}, 'Message': {'Subject': {'Charset': 'UTF-8', 'Data': 'SSO UserAdd AWS Console Access'}, 'Body': {'Text': {'Charset': 'UTF-8', 'Data': "[{'UserName': 'nagarajan@email.com', 'UserId': 'stdagasdgagring'}, {'UserName': 'adsgadg@email.com', 'UserId': 'stdagasdgagring'}, {'UserName': 'adfagagsa@email.com', 'UserId': 'stdagasdgagring'}] <Check_user_group stage > [{'UserName': 'nagarajan@email.com', 'UserId': 'stdagasdgagring'}, {'UserName': 'adsgadg@email.com', 'UserId': 'stdagasdgagring'}, {'UserName': 'adfagagsa@email.com', 'UserId': 'stdagasdgagring'}] \ngroup not exist, creating it gwb \nfound new user [['nagarjan', 'soong ', 'naga@emai.com', 'gwb', 'sg-company', '123456789101', 'sit']], Adding it \nuser naga@emai.com has been added. Adding to group \nupdate_group_ownership string {'GroupId': 'Sucess', 'IdentityStoreId': 'string'} \ngroup update has been completed \nGroup Sucess has been added to the account 123456789101 \n"}}}}

ok

----------------------------------------------------------------------


Ran 1 test in 0.004s


OK


NagarajansMBP2:sso_automation naga$ 

#### 2) make clean

NagarajansMBP2:sso_automation naga$ make clean

find . -name __pycache__ -exec rm -r {} \;

find: ./__pycache__: No such file or directory


#### 3) make build (to generate build.zip )


NagarajansMBP2:sso_automation naga$ make build

>/dev/null zip -r build.zip * -x \*.pyc \*.md \*.log \*__pycache__\* \*.so lib/botocore\*

NagarajansMBP2:sso_automation naga$ ls -l build.zip

-rw-r--r--  1 naga  staff  4795  1 Oct 13:17 build.zip




Contribute
Please feel free to fork it and contribute

Author: Nagarajan Manokaran
email: floki.nagee@gmail.com
