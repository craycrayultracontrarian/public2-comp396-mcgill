import boto3
import os
from data.keys.credentials import aws_access_key_id, aws_secret_access_key

def upload_to_s3(file_path, bucket_name, s3_key, aws_access_key_id, aws_secret_access_key):
    # Initialize a session using Amazon S3
    s3 = boto3.client(
        's3', 
        aws_access_key_id=aws_access_key_id, 
        aws_secret_access_key=aws_secret_access_key
    )

    try:
        # Upload the file
        s3.upload_file(file_path, bucket_name, s3_key, ExtraArgs={'ContentType': 'image/png'})
        print(f"Successfully uploaded {file_path} to s3://{bucket_name}/{s3_key}")
    except Exception as e:
        print(f"Failed to upload {file_path} to s3://{bucket_name}/{s3_key}")
        print(e)

# Folder containing the images to upload
folder_path = 'data/screenshots'

# S3 bucket name
bucket_name = "socialcomputing"

