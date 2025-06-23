import boto3
from botocore.exceptions import NoCredentialsError, ParamValidationError
import requests

session = boto3.Session(
    profile_name = 'Scarlassara',
    region_name = 'us-east-1'
)

client = session.client('s3')

def check_internet_connection():
    response = requests.get('https://checkip.amazonaws.com/')
    if response.status_code == 200:
        return True
    else:
        return False

def main():
    if check_internet_connection():
        print('1. List Bucket          2. Create Bucket            3. Delete Bucket \n'
              '4. Upload Object        5. Downlaod Object            6. Delete Object')

        option = int(input())

        if option == 1:
            print(client.list_buckets()['Buckets'])
        elif option == 2:
            try:
                bucket_name = input('Name your bucket: ')
                bucket_region = input('Which region do you want to create the bucket: ')
                response = client.create_bucket(
                    Bucket= f'{bucket_name}',
                    #Check the avaiable regions at: https://docs.aws.amazon.com/AmazonS3/latest/API/API_CreateBucketConfiguration.html
                    CreateBucketConfiguration={
                        'LocationConstraint': f'{bucket_region}',
                    },
                )
                print(response)
            except client.exceptions.BucketAlreadyExists:
                print('This bucket already exist.')
            except client.exceptions.ClientError as error:
                print(f'ClientError: {error}')
        elif option == 3:
            bucket_name = str(input('Bucket Name: '))
            try:
                response  = client.delete_bucket(Bucket=str(bucket_name))
                print(response)
            except ParamValidationError as error:
                print(f'ParamValidationError: {error}')
            except client.exceptions.ClientError as error:
                print(f'Client Error: {error}')
        elif option == 4:
            bucket_name = input('Bucket name: ')
            object_name = input('Object content: ')
            object_key = input('Object name: ')
            response = client.put_object(
                ACL='private',
                Bucket=bucket_name,
                Body=object_name,
                Key=object_key,
                ServerSideEncryption='AES256',
                StorageClass='STANDARD'
            )
            print(response)
        elif option == 5:
            try:
                bucket_name = input('Bucket Name: ')
                object_name = input('Object Name: ')
                file_name = input('File Name: ')
                response = client.download_file(
                    bucket_name,
                    object_name,
                    file_name

                )
                print(response)
            except PermissionError as error:
                print(f'PermissionError: {error}')




        elif option == 6:
            object_name = input('Insert the object name: ')
            bucket_name = input('Bucket nme: ')
            response = client.delete_object(
                Bucket=bucket_name,
                Key=object_name
            )
            print(response)
try:
    main()
except ValueError:
    print('Invalid option.')