import os

S3_BUCKET = os.getenv("S3_BUCKET", "your-s3-bucket-name")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
QUEUE_URL = os.getenv("QUEUE_URL", "your-sqs-queue-url")
API_KEY = os.getenv("API_KEY", "supersecretapikey123")
