import boto3
from botocore.exceptions import NoCredentialsError, ParamValidationError
import requests

session = boto3.Session(profile_name='Scarlassara', region_name='us-east-1')
client = session.client('s3')

def check_internet_connection():
    response = requests.get('https://checkip.amazonaws.com/')
    return response.status_code == 200

def create_bucket(bucket_name, bucket_region):
    try:
        client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': bucket_region,
            },
        )
    except client.exceptions.BucketAlreadyExists:
        print('This bucket already exists.')
    except client.exceptions.ClientError as error:
        print(f'ClientError: {error}')

def list_buckets():
    try:
        buckets = client.list_buckets()['Buckets']
        if buckets:
            for bucket in buckets:
                print(bucket['Name'])
            else:
                print('No buckets found.')
    except Exception as error:
        print(f'Exception: {error}')

def delete_bucket(bucket_name):
    try:
        client.delete_bucket(Bucket=bucket_name)
    except ParamValidationError as error:
        print(f'ParamValidationError: {error}')
    except client.exceptions.ClientError as error:
        print(f'ClientError: {error}')

def create_object(bucket_name, object_content, object_key):
    client.put_object(
        ACL='private',
        Bucket=bucket_name,
        Body=object_content,
        Key=object_key,
        ServerSideEncryption='AES256',
        StorageClass='STANDARD'
    )

def upload_object(bucket_name, file_path, object_name):
    try:
        client.upload_file(
            file_path,
            bucket_name,
            object_name
        )
        print('Upload completed successfully.')
    except PermissionError as error:
        print(f'PermissionError: {error}')
    except FileNotFoundError as error:
        print(f'FileNotFoundError: {error}')
    except client.exceptions.ClientError as error:
        print(f'ClientError: {error}')

def download_object(bucket_name, object_name, destination_file):
    try:
        client.download_file(
            bucket_name,
            object_name,
            destination_file
        )
        print('Download completed successfully.')
    except PermissionError as error:
        print(f'PermissionError: {error}')
    except FileNotFoundError as error:
        print(f'FileNotFoundError: {error}')
    except client.exceptions.ClientError as error:
        print(f'ClientError: {error}')


def main():
    if check_internet_connection():
        print(
            '1. List Buckets         2. Create Bucket        3. Delete Bucket\n'
            '4. Create Object        5. Upload Object        6. Download Object\n'
            '7. Delete Object')

        option = int(input("Select an option: "))

        if option == 1:
            list_buckets()
        elif option == 2:
            bucket_name = input('Bucket Name: ')
            bucket_region = input('Bucket Region: ')
            create_bucket(bucket_name, bucket_region)
        elif option == 3:
            bucket_name = input('Bucket Name: ')
            delete_bucket(bucket_name)
        elif option == 4:
            bucket_name = input('Bucket name: ')
            object_content = input('Object content: ')
            object_key = input('Object name: ')
            create_object(bucket_name, object_content, object_key)
        elif option == 5:
            bucket_name = input('Bucket Name: ')
            file_path = input('File path: ')
            object_name = input('Object Name: ')
            upload_object(bucket_name, file_path, object_name)
        elif option == 6:
            bucket_name = input('Bucket Name: ')
            object_name = input('Object Name: ')
            destination_file = input('Destination File: ')
            download_object(bucket_name, object_name, destination_file)
        elif option == 7:
            bucket_name = input('Bucket Name: ')
            file_path = input('File Path: ')
            object_name = input('Object Name: ')
            #delete_object(bucket_name, file_path, object_name)
        else:
            print("Invalid option.")
try:
    main()
except ValueError:
    print('Invalid input.')
