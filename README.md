# AWS

Automate the execution of SSM Document using AWS Lambda function and upon Success/Fail send a Email Notification Using AWS SNS.

automation.ps1 is a powershell script that transfer files in a specific location(ex: C://MYSQL/AUTOMATION) to AWS S3 bucket. To Automate this process we are using AWS Lambda funcation to trigger the SSM Document everyday at a specified time, for this we are using AWS EventBridge to schedule a trigger to lambda. 
