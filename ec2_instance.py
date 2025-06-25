import boto3

session = boto3.Session(
    profile_name='YOUR_PROFILE_NAME_HERE'
)

ec2_client = session.client('ec2')

key_name = 'YOUR_KEY_PAIR_NAME_HERE'
vpc_id = 'YOUR_VPC_ID_HERE'
subnet_id = 'YOUR_SUBNET_ID_HERE'
ami_id = 'YOUR_AMI_ID_HERE'
try:
    security_group_response = ec2_client.create_security_group(
        Description='This SG was created with Boto3',
        GroupName='Boto3SG',
        VpcId=vpc_id
    )

    sg_id = security_group_response['GroupId']
except Exception as error:
    print('Already Exists!')
    security_group_response = ec2_client.describe_security_groups(
        GroupNames=['Boto3SG']
    )
    sg_id = security_group_response['SecurityGroups'][0]['GroupId']

print(sg_id)

ec2_response = ec2_client.run_instances(
    BlockDeviceMappings=[
        {
            'DeviceName': '/dev/sda1',
            'Ebs': {
                'VolumeSize': 8,
                'DeleteOnTermination': True,
                'VolumeType': 'gp2',
                'Encrypted': False
            }
        }
    ],
    ImageId=ami_id,
    MaxCount=1,
    MinCount=1,
    InstanceType='t2.micro',
    KeyName=key_name,
    Monitoring={
        'Enabled': False
    },
    SecurityGroupIds=[sg_id],
    SubnetId=subnet_id,
    InstanceInitiatedShutdownBehavior='terminate',
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'My Server'
                },
                {
                    'Key': 'AWS',
                    'Value': 'This instance was created with Boto3'
                }
            ]
        }
    ]
)
print(ec2_response)