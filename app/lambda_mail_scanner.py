import boto3
import re
import json
import os

s3 = boto3.client('s3')
sns = boto3.client('sns')

RESULT_BUCKET = os.environ['RESULT_BUCKET']
RESULT_TOPIC_ARN = os.environ.get('RESULT_TOPIC_ARN')

def lambda_handler(event, context):
    results = {}
    buckets = s3.list_buckets()['Buckets']
    for bucket in buckets:
        bucket_name = bucket['Name']
        files = s3.list_objects_v2(Bucket=bucket_name).get('Contents', [])
        for file in files:
            file_key = file['Key']
            obj = s3.get_object(Bucket=bucket_name, Key=file_key)
            content = obj['Body'].read().decode('utf-8', errors='ignore')
            emails = extract_emails(content)
            if emails:
                results[file_key] = emails

    save_results_to_s3(results)
    publish_results(results)
    return {"status": "success", "results": results}

def extract_emails(content):
    email_regex = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    return re.findall(email_regex, content)

def save_results_to_s3(results):
    result_file = "/tmp/results.json"
    with open(result_file, 'w') as f:
        json.dump(results, f)
    s3.upload_file(result_file, RESULT_BUCKET, "results.json")

def publish_results(results):
    if RESULT_TOPIC_ARN:
        sns.publish(TopicArn=RESULT_TOPIC_ARN, Message=json.dumps(results))