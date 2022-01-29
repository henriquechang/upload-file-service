from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from api.controllers.upload_controller import UploadController
from api.services.fake_s3_service import FakeS3Service
from api.services.s3_service import S3Service

from app import settings

fake = Faker()


class TestAPIUpload(APITestCase):

    def setUp(self) -> None:
        settings.S3_BUCKET_1 = 'test_1'
        settings.S3_BUCKET_2 = 'test_2'

    def not_uploaded_first(self, file, bucket):
        if bucket == 'test_1':
            return False
        return True

    def not_uploaded_second(self, file, bucket):
        if bucket == 'test_2':
            return False
        return True

    @patch.object(S3Service, '__init__', FakeS3Service.__init__)
    @patch.object(S3Service, 'upload_file', FakeS3Service.upload_file)
    def test_upload_file_success(self):
        fake_file = SimpleUploadedFile(
            fake.pystr(),
            fake.binary(length=fake.pyint(min_value=1, max_value=10))
        )
        response = self.client.post('/upload', data={'file': fake_file})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.object(S3Service, '__init__', FakeS3Service.__init__)
    @patch.object(S3Service, 'upload_file', FakeS3Service.upload_file)
    def test_upload_file_error_large_file(self):
        fake_file = SimpleUploadedFile(
            fake.pystr(),
            fake.binary(length=fake.pyint(min_value=5000001, max_value=6000000))
        )
        response = self.client.post('/upload', data={'file': fake_file})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(S3Service, '__init__', FakeS3Service.init_error)
    @patch.object(S3Service, 'upload_file', FakeS3Service.upload_file_raises)
    def test_upload_file_init_error(self):
        fake_file = SimpleUploadedFile(
            fake.pystr(),
            fake.binary(length=fake.pyint(min_value=1, max_value=10))
        )
        response = self.client.post('/upload', data={'file': fake_file})
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    @patch.object(S3Service, '__init__', FakeS3Service.__init__)
    @patch.object(S3Service, 'upload_file', FakeS3Service.upload_file_raises)
    def test_upload_file_upload_error_two_buckets(self):
        fake_file = SimpleUploadedFile(
            fake.pystr(),
            fake.binary(length=fake.pyint(min_value=1, max_value=10))
        )
        response = self.client.post('/upload', data={'file': fake_file})
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    @patch.object(S3Service, '__init__', FakeS3Service.__init__)
    @patch.object(S3Service, 'upload_file', FakeS3Service.upload_file_raises)
    @patch.object(UploadController, 'upload_to_bucket', not_uploaded_first)
    def test_upload_file_upload_error_first_bucket(self):
        fake_file = SimpleUploadedFile(
            fake.pystr(),
            fake.binary(length=fake.pyint(min_value=1, max_value=10))
        )
        response = self.client.post('/upload', data={'file': fake_file})
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    @patch.object(S3Service, '__init__', FakeS3Service.__init__)
    @patch.object(S3Service, 'upload_file', FakeS3Service.upload_file_raises)
    @patch.object(UploadController, 'upload_to_bucket', not_uploaded_second)
    def test_upload_file_upload_error_second_bucket(self):
        fake_file = SimpleUploadedFile(
            fake.pystr(),
            fake.binary(length=fake.pyint(min_value=1, max_value=10))
        )
        response = self.client.post('/upload', data={'file': fake_file})
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
