import boto3
import csv
from datetime import datetime

main_bucket = input('Bucket to verify: ')
backup_bucket = input('Bucket to backup your data: ')


session = boto3.Session(profile_name='YOUR_PROFILE_NAME_HERE')
client = session.client('s3')

current_date = datetime.now()
year = current_date.year
month = current_date.month
day = current_date.day

def list_objects():
    response = client.list_objects_v2(
        Bucket=main_bucket
    )
    data = response['Contents'][0]['Key']
    return data

print(list_objects())

def copy_and_delete_files():
    try:
        response = client.list_objects_v2(Bucket=main_bucket)['Contents'][0]['Key']
        print(response)
        client.copy_object(
            ACL='private',
            Bucket=backup_bucket,
            CopySource= {
                'Bucket': main_bucket, 'Key': list_objects()
            },
            CopySourceIfModifiedSince=datetime(year,month, 30 - day),
            Key=f'{year}-{month}-{day}/{list_objects()}')
        client.delete_objects(
            Bucket=main_bucket,
            Delete = {
                'Objects': [
                    {
                        'Key': list_objects()
                    }
                ]
            }
        )
    except Exception as error:
        print(f'Error: {error}')

def data_report():
    data = [
        {'File Name': list_objects(), 'Main Bucket': main_bucket, 'File Path': f'{year}-{month}-{day}/{list_objects()}'}
    ]

    with open('bucket_report.csv', 'w', newline='') as csvfile:
        fieldnames = ['File Name', 'Main Bucket', 'File Path']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

copy_and_delete_files()
data_report()