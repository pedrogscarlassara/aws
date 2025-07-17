import boto3
from datetime import datetime, timezone
import botocore.exceptions
from dateutil.relativedelta import relativedelta

session = boto3.Session(profile_name='default')

def s3_part():
    client = session.client('s3')
    data = client.list_buckets()['Buckets']

    if not data:
        print("This account don't have buckets.")

    for bucket in data:
        versioning = client.get_bucket_versioning(Bucket=bucket['Name'])
        encryption = client.get_bucket_encryption(Bucket=bucket['Name'])
        acl = client.get_bucket_acl(Bucket=bucket['Name'])
        if 'Status' in versioning:
            ses_part('pedrogscarlassara@gmail.com', 'pedrogscarlassara@gmail.com',f'Bucket Name: {bucket['Name']}\nVersioning: {versioning['Status']}\nEncryption: {encryption['ServerSideEncryptionConfiguration']['Rules'][0]['BucketKeyEnabled']}')
        else:
            ses_part('pedrogscarlassara@gmail.com', 'pedrogscarlassara@gmail.com',f'S3\nBucket Name: {bucket['Name']}\nVersioning: Disabled\nEncryption: {encryption['ServerSideEncryptionConfiguration']['Rules'][0]['BucketKeyEnabled']}')

def ec2_part():
    client = session.client('ec2')
    data = client.describe_instances()
    date = data['Reservations'][0]['Instances'][0]['LaunchTime']
    uptime = (datetime.now(timezone.utc) - date)

    if not data['Reservations']:
        print("This account doesn't have any instances")
        return

    for reservation in data['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            try:
                if instance.get('NetworkInterfaces') and len(instance['NetworkInterfaces']) > 0:
                    network_interface = instance['NetworkInterfaces'][0]
                    if network_interface.get('Association') and 'PublicIp' in network_interface['Association']:
                        ses_part('pedrogscarlassara@gmail.com', 'pedrogscarlassara@gmail.com',f'EC2\nInstance ID: {instance_id}\nIP: {network_interface['Association']['PublicIp']}\nUptime: {uptime}')
                    else:
                        ses_part('pedrogscarlassara@gmail.com', 'pedrogscarlassara@gmail.com',f'EC2\nInstance ID: {instance_id}\nIP: Unknown (No public IP associated)')
                else:
                    ses_part('pedrogscarlassara@gmail.com', 'pedrogscarlassara@gmail.com',f'EC2\nInstance ID: {instance_id}\nIP: Unknown (No network interfaces)')
            except Exception as e:
                ses_part('pedrogscarlassara@gmail.com', 'pedrogscarlassara@gmail.com',f'EC2\nInstance ID: {instance_id}\nIP: Unknown (Error: {str(e)}')

def iam_part(username):
    client = session.client('iam')
    try:
        access_key = client.list_access_keys(UserName=username)['AccessKeyMetadata'][0]['CreateDate']
        access_key_id  = client.list_access_keys(UserName=username)['AccessKeyMetadata'][0]['AccessKeyId']
        admin_policy_check = client.get_policy(PolicyArn = 'arn:aws:iam::aws:policy/AdministratorAccess')

        if admin_policy_check['Policy']['AttachmentCount'] >= 1:
            ses_part('pedrogscarlassara@gmail.com', 'pedrogscarlassara@gmail.com', 'IAM\nThere is users with Administrator Policy attached.')
        if datetime.now(timezone.utc) >= access_key + relativedelta(months=3):
            print('IAM: Your Access Key is 3 months old, its recommended to deactivate the current key and create a new one.')
            delete_confirmation = input('Do you want to delete the key? (y/n)')
            if 'y' or 'yes' in delete_confirmation:
                print('Your Access Key was deleted.')
                ses_part('pedrogscarlassara@gmail.com', 'pedrogscarlassara@gmail.com', 'IAM\nYour IAM Access Key was deleted.')
                client.delete_access_key(UserName=username, AccessKeyId=access_key_id)
            else:
                print('Your Access Key still online.')

    except botocore.exceptions.ClientError as error:
            print(f'Error: {error}')

def ses_part(source, subject, body):
    client = session.client('ses')
    response = client.send_email(
        Source=source,
        Destination={
            'ToAddresses': [
                subject,
            ],
            'CcAddresses': [
                subject,
            ],
            'BccAddresses': [
                subject,
            ]
        },
        Message={
            'Subject': {
                'Data': subject,
                'Charset': 'UTF-8',
            },
            'Body': {
              'Text': {
                  'Data': body,
                  'Charset': 'UTF-8'
              },
            'Html': {
                'Data': body,
                'Charset': 'UTF-8'

            }
        }
    },
    Tags=[
        {
            'Name': 'string',
            'Value': 'string'
        }
    ]
)

iam_part('scarlassara-laptop')