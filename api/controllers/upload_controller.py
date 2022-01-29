from api.handlers.upload_error_handler import UploadErrorHandler
from api.services.base_s3_service import BaseS3Service
from app import settings


class UploadController:

    def __init__(self, s3_service: BaseS3Service, error_handler: UploadErrorHandler):
        self.s3_service = s3_service
        self.error_handler = error_handler

    def send_to_buckets(self, file):
        """Send file to two different S3 buckets

          :param file: File to upload
          :returns: True if all files has been uploaded successfully or False if not
        """
        uploaded_1 = self.upload_to_bucket(file, settings.S3_BUCKET_1)
        file.seek(0)
        uploaded_2 = self.upload_to_bucket(file, settings.S3_BUCKET_2)
        if uploaded_1 and uploaded_2:
            return True
        return False

    def upload_to_bucket(self, file, bucket):
        """Calls S3 Service to Upload a file

          :param file: File to upload
          :param bucket: Bucket to upload to
          :returns: True if file has been uploaded successfully or False if not
        """
        try:
            self.s3_service.upload_file(file, bucket)
        except Exception as e:
            self.error_handler.add_upload_error(e.args[0], file.name)
            return False
        return True
