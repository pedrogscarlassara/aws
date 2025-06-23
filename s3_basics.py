import boto3
from botocore.exceptions import NoCredentialsError, ParamValidationError
import requests

session = boto3.Session(
    profile_name='YOUR_PROFILE_NAME',
    region_name='YOUR_AWS_REGION'
)

client = session.client('s3')


def check_internet_connection():
    response = requests.get('https://checkip.amazonaws.com/')
    return response.status_code == 200


def main():
    if check_internet_connection():
        print(
            '1. List Buckets         2. Create Bucket        3. Delete Bucket\n'
            '4. Create Object        5. Upload Object        6. Download Object\n'
            '7. Delete Object        8. TODO'
        )

        option = int(input("Select an option: "))

        if option == 1:
            print(client.list_buckets()['Buckets'])

        elif option == 2:
            try:
                bucket_name = input('Name your bucket: ')
                bucket_region = input('Which region do you want to create the bucket in? ')
                response = client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={
                        'LocationConstraint': bucket_region,
                    },
                )
                print(response)
            except client.exceptions.BucketAlreadyExists:
                print('This bucket already exists.')
            except client.exceptions.ClientError as error:
                print(f'ClientError: {error}')

        elif option == 3:
            bucket_name = input('Bucket Name: ')
            try:
                response = client.delete_bucket(Bucket=bucket_name)
                print(response)
            except ParamValidationError as error:
                print(f'ParamValidationError: {error}')
            except client.exceptions.ClientError as error:
                print(f'ClientError: {error}')

        elif option == 4:
            bucket_name = input('Bucket name: ')
            object_content = input('Object content: ')
            object_key = input('Object name: ')
            response = client.put_object(
                ACL='private',
                Bucket=bucket_name,
                Body=object_content,
                Key=object_key,
                ServerSideEncryption='AES256',
                StorageClass='STANDARD'
            )
            print(response)

        elif option == 5:
            try:
                bucket_name = input('Bucket Name: ')
                file_path = input('File Path to Upload: ')
                object_name = input('Object Name on S3: ')
                response = client.upload_file(
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

        elif option == 6:
            try:
                bucket_name = input('Bucket Name: ')
                object_name = input('Object Name on S3: ')
                destination_file = input('Destination File Name: ')
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

        elif option == 7:
            object_name = input('Object Name: ')
            bucket_name = input('Bucket Name: ')
            response = client.delete_object(
                Bucket=bucket_name,
                Key=object_name
            )
            print(response)

        elif option == 8:
            print('TODO: Implement this option.')

        else:
            print("Invalid option.")


try:
    main()
except ValueError:
    print('Invalid input.')
