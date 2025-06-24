import boto3

session = boto3.Session(
    profile_name='PROFILE_NAME_HERE'
)

ec2_client = session.client('ec2')

key_name = 'YOUR_KEY_HERE'
vpc_id = 'VPC_ID_HERE'
subnet = 'SUBNET_ID_HERE'
ami_id = 'AMI_ID_HERE'
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

resposta_ingress = ec2_client.authorize_security_group_ingress(
    GroupId=sg_id,
    IpPermissions=[
        {
            'FromPort': 22,
            'ToPort': 22,
            'IpProtocol': 'tcp',
            'IpRanges': [
                {
                    'CidrIp': '0.0.0.0/0',
                    'Description': 'SSH Access'
                }
            ]
        },
        {
            'FromPort': 80,
            'ToPort': 80,
            'IpProtocol': 'tcp',
            'IpRanges': [
                {
                    'CidrIp': '0.0.0.0/0',
                    'Description': 'HTTP Access'
                }
            ]
        }
    ]
)
