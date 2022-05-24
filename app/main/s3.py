import boto3
from botocore.config import Config
from app.main.config import Configuration


class S3Client:
    _endpoint = None
    _access_key = None
    _secret_access_key = None

    @classmethod
    def get_client(cls):
        config = Configuration()
        return boto3.client(
            "s3",
            endpoint_url=config.minio_server,
            aws_access_key_id=config.minio_username,
            aws_secret_access_key=config.minio_password,
            config=Config(signature_version='s3v4'))
