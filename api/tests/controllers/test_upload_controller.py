from unittest import TestCase
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile

from api.controllers.upload_controller import UploadController
from api.handlers.upload_error_handler import UploadErrorHandler
from faker import Faker

from api.services.fake_s3_service import FakeS3Service
from app import settings

fake = Faker()


class TestUploadController(TestCase):

    def setUp(self) -> None:
        settings.S3_BUCKET_1 = 'test_1'
        settings.S3_BUCKET_2 = 'test_2'

    def all_not_uploaded(self, file):
        return False

    def not_uploaded_first(self, file, bucket):
        if bucket == 'test_1':
            return False
        return True

    def not_uploaded_second(self, file, bucket):
        if bucket == 'test_2':
            return False
        return True

    def test_upload_success(self):
        fake_s3_service = FakeS3Service()
        upload_error_handler = UploadErrorHandler()
        upload_controller = UploadController(s3_service=fake_s3_service, error_handler=upload_error_handler)
        uploaded = upload_controller.send_to_buckets(
            SimpleUploadedFile(
                fake.pystr(),
                fake.binary(length=fake.pyint(min_value=1, max_value=10))
        ))
        self.assertTrue(uploaded)

    @patch.object(UploadController, 'send_to_buckets', all_not_uploaded)
    def test_upload_error_two_buckets(self):
        fake_s3_service = FakeS3Service()
        upload_error_handler = UploadErrorHandler()
        upload_controller = UploadController(s3_service=fake_s3_service, error_handler=upload_error_handler)
        uploaded = upload_controller.send_to_buckets(
            SimpleUploadedFile(
                fake.pystr(),
                fake.binary(length=fake.pyint(min_value=1, max_value=10))
            ))
        self.assertFalse(uploaded)

    @patch.object(UploadController, 'upload_to_bucket', not_uploaded_first)
    def test_upload_error_first_bucket(self):
        fake_s3_service = FakeS3Service()
        upload_error_handler = UploadErrorHandler()
        upload_controller = UploadController(s3_service=fake_s3_service, error_handler=upload_error_handler)
        uploaded = upload_controller.send_to_buckets(
            SimpleUploadedFile(
                fake.pystr(),
                fake.binary(length=fake.pyint(min_value=1, max_value=10))
            ))
        self.assertFalse(uploaded)

    @patch.object(UploadController, 'upload_to_bucket', not_uploaded_second)
    def test_upload_error_second_bucket(self):
        fake_s3_service = FakeS3Service()
        upload_error_handler = UploadErrorHandler()
        upload_controller = UploadController(s3_service=fake_s3_service, error_handler=upload_error_handler)
        uploaded = upload_controller.send_to_buckets(
            SimpleUploadedFile(
                fake.pystr(),
                fake.binary(length=fake.pyint(min_value=1, max_value=10))
            ))
        self.assertFalse(uploaded)
