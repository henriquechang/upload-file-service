from unittest import TestCase

from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker

from api.serializers.upload_serializer import UploadSerializer

fake = Faker()


class TestUploadSerializer(TestCase):

    def test_valid_file(self):
        fake_file = SimpleUploadedFile(
            fake.pystr(),
            fake.binary(length=fake.pyint(min_value=1, max_value=5000000))
        )
        upload_serializer = UploadSerializer(data={'file': fake_file})
        self.assertTrue(upload_serializer.is_valid())

    def test_invalid_file(self):
        fake_file = SimpleUploadedFile(
            fake.pystr(),
            fake.binary(length=fake.pyint(min_value=5000001, max_value=6000000))
        )
        upload_serializer = UploadSerializer(data={'file': fake_file})
        self.assertFalse(upload_serializer.is_valid())
