from collections import defaultdict

import boto3
import time
import json

"""
A tool for retrieving basic information from the running EC2 instances.
"""
def lambda_handler(event, context):
# Connect to EC2
    ec2 = boto3.client('ec2')
    ssm = boto3.client('ssm')

    describeInstance = ec2.describe_instances(Filters=[
            {
                'Name': 'tag:Type',
                'Values': ['SQL']
        }
    ])

    InstanceId=[]
    # fetchin instance id of the running instances
    for i in describeInstance['Reservations']:
        for instance in i['Instances']:
            if instance["State"]["Name"] == "running":
                InstanceId.append(instance['InstanceId'])

     # looping through instance ids
    for instanceid in InstanceId:
        # command to be executed on instance
        response = ssm.send_command(
                InstanceIds=[instanceid],
                DocumentName="Copy-tagvalues",

                )

        # fetching command id for the output
        command_id = response['Command']['CommandId']

        # time.sleep(2)

        # fetching command output
        output = ssm.list_command_invocations(
              CommandId=command_id,
              InstanceId=instanceid
            )

    return {
        'statusCode': 200,
        'body': json.dumps(output),
        'command_id': command_id
    }

# def get_instance_name(fid):
#     """
#         When given an instance ID as str e.g. 'i-1234567', return the instance 'Name' from the name tag.
#         :param fid:
#         :return:
#     """
#     ec2 = boto3.resource('ec2')
#     ec2instance = ec2.Instance(fid)
#     instancename = ""
#     for tags in ec2instance.tags:
#         if tags["Key"] == "Environment":
#             instancename = tags["Value"]
#     return instancename
