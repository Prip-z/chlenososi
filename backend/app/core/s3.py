import aioboto3
from typing import Any
from botocore.exceptions import ClientError
from aiobotocore.config import AioConfig 
from app.core.config import configs as settings

class S3Storage:
    def __init__(self) -> None:
        self.session = aioboto3.Session()
        self.bucket_name = settings.S3_BUCKET_NAME

    def _get_client(self) -> Any:
        return self.session.client(
            's3',
            endpoint_url=settings.S3_ENDPOINT_URL,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            config=AioConfig(signature_version='s3v4')
        )

    async def init_bucket(self) -> None:
        async with self._get_client() as s3:
            try:
                await s3.head_bucket(Bucket=self.bucket_name)
            except ClientError as e:
                error_code = e.response.get('Error', {}).get('Code')
                if error_code in ['404', 'NoSuchBucket']:
                    await s3.create_bucket(Bucket=self.bucket_name)
                    
                    await s3.put_bucket_acl(Bucket=self.bucket_name, ACL='public-read')
                    
                    print(f"Bucket '{self.bucket_name}' successfully created with public-read ACL.")
                else:
                    raise e

    async def upload_file(self, file_bytes: bytes, object_name: str) -> str:
        async with self._get_client() as s3:
            await s3.put_object(
                Bucket=self.bucket_name,
                Key=object_name,
                Body=file_bytes
            )
            return f"{settings.S3_ENDPOINT_URL}/{self.bucket_name}/{object_name}"

s3_storage = S3Storage()