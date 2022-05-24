from datetime import datetime

from app.main.s3 import S3Client
from app.main.config import Configuration


class MinioService:
    def put_backup(self, content, filename):
        config = Configuration()
        client = S3Client.get_client()
        key = str(datetime.timestamp(datetime.now())) + "/" + filename
        client.put_object(Body=content, Bucket=config.minio_bucket, Key=key)
