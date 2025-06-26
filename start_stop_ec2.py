import boto3
import requests

prompt = int(input('Choose a option: '))
session = boto3.Session(profile_name='YOUR_PROFILE_NAME_HERE')
ec2_client = session.client('ec2')

def internet_connection():
    if requests.get('https://checkip.amazonaws.com/').status_code == 200:
        return True
    else:
        return False

def instance_descritpion():
    response = ec2_client.describe_instances()
    instance_id = response['Reservations'][0]['Instances'][0]['InstanceId']
    return instance_id

def stop():
    response = ec2_client.stop_instances(
        InstanceIds = [
            instance_descritpion()
        ],
        Force = True
    )
    print(response)

def start():
    response = ec2_client.start_instances(
        InstanceIds = [
            instance_descritpion()
        ],
        DryRun = True
    )
    print(response)

def screen():
    print('1. Stop Instances            2. Start Instances')
    if internet_connection():
        if prompt == 1:
            stop()
            print('Stopping')
        elif prompt == 2:
            start()
            print('Starting')
        else:
            print('Invalid option')

screen()