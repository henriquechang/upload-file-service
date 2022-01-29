from botocore.exceptions import ClientError
from django.core.files.uploadedfile import InMemoryUploadedFile

from api.services.base_s3_service import BaseS3Service


class FakeS3Service(BaseS3Service):

    def __init__(self):
        pass

    def init_error(self):
        raise Exception

    def upload_file(self, file: InMemoryUploadedFile, bucket: str):
        return None

    def upload_file_raises(self, file, bucket):
        raise ClientError
