import logging

import boto3
from botocore.exceptions import ClientError
from django.core.files.uploadedfile import InMemoryUploadedFile

from api.services.base_s3_service import BaseS3Service
from app import settings


class S3Service(BaseS3Service):

    __logger = logging.getLogger(__name__)

    def __init__(self):
        self.s3_client = self.__config()

    def __config(self):
        """Set up boto3 client config

        :returns: boto3 client
        """
        return boto3.client(
            service_name='s3',
            region_name='sa-east-1',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

    def upload_file(self, file: InMemoryUploadedFile, bucket: str):
        """Upload a file to an S3 bucket

        :param file: File to upload
        :param bucket: Bucket to upload to
        :raises ClientError: if bucket or config data is invalid
        """
        try:
            self.s3_client.put_object(Body=file, Bucket=bucket, Key=file.name)
        except ClientError as e:
            self.__logger.error(e)
            raise e
