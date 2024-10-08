import json
import os
import boto3
from botocore.exceptions import ClientError

bucket_name = "keh-tech-audit-tool"
object_name = "new_project_data.json"
autocomplete_object_name = "array_data.json"
region_name = os.getenv("AWS_DEFAULT_REGION")

s3 = boto3.client('s3', region_name=region_name)

def read_data():
    try:
        response = s3.get_object(Bucket=bucket_name, Key=object_name)
        data = json.loads(response['Body'].read().decode('utf-8'))
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            data = {'projects': []}
        else:
            abort(500, description=f"Error reading data: {e}")
    return data

def write_data(new_data):
    try:
        s3.put_object(
            Bucket=bucket_name,
            Key=object_name,
            Body=json.dumps(new_data, indent=4).encode('utf-8')
        )
    except ClientError as e:
        abort(500, description=f"Error writing data: {e}")



def read_array_data():
    try:
        response = s3.get_object(Bucket=bucket_name, Key=autocomplete_object_name)
        array_data = json.loads(response['Body'].read().decode('utf-8'))
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            array_data = {}
        else:
            abort(500, description=f"Error reading array data: {e}")
    return array_data

def write_array_data(new_array_data):
    try:
        s3.put_object(
            Bucket=bucket_name,
            Key=autocomplete_object_name,
            Body=json.dumps(new_array_data, indent=4).encode('utf-8')
        )
    except ClientError as e:
        abort(500, description=f"Error writing array data: {e}")
