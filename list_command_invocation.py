from collections import defaultdict

import boto3
import time
import json
ec2 = boto3.client('ec2')
ssm = boto3.client('ssm')
s3 = boto3.resource('s3')
sns = boto3.client('sns')
  
def check_response(response_json):
    try:
        if response_json['ResponseMetadata']['HTTPStatusCode'] == 200:
            return True
        else:
            return False
    except KeyError:
        return False

def lambda_handler(event, context):
    bucket =  '<S3_BUCKET_NAME>'
    key = '<FILENAME.JSON>'

    obj = s3.Object(bucket, key)
    data = obj.get()['Body'].read().decode('utf-8')
    json_data = json.loads(data)

    for command_id in json_data:
        response_iterator = ssm.list_command_invocations(
            CommandId = command_id,
            Details = True
        )
        
        if check_response(response_iterator):
            if response_iterator['CommandInvocations']:
                response_iterator_status = response_iterator['CommandInvocations'][0]['Status']
                if response_iterator_status != 'Pending':
                    if response_iterator_status == 'InProgress' or response_iterator_status == 'Success':
                        response = sns.publish(
                            TopicArn='<SNS TOPIC ARN>',
                            Message='Backup of EC2 SQL Servers to S3 SUCCESS ' +str(response_iterator['CommandInvocations'][0]['InstanceId']),
                            Subject='EC2 to S3'
                        )
                    else:
                        response = sns.publish(
                            TopicArn='<SNS TOPIC ARN',
                            Message='Backup of EC2 SQL Servers to S3 FAILED ' +str(response_iterator['CommandInvocations'][0]['InstanceId']),
                            Subject='EC2 to S3'
                        )
                        
    return {
        'json': json_data
    }
    
