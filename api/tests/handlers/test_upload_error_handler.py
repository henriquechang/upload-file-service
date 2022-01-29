from unittest import TestCase

from api.handlers.upload_error_handler import UploadErrorHandler
from faker import Faker

fake = Faker()


class TestUploadErrorHandler(TestCase):

    def setUp(self) -> None:
        self.upload_error_handler = UploadErrorHandler()

    def test_upload_error(self):
        description = fake.pystr()
        file_name = fake.pystr()
        errors_count = fake.pyint(min_value=1, max_value=10)
        for _ in range(0, errors_count):
            self.upload_error_handler.add_upload_error(description, file_name)
        self.assertListEqual(
            self.upload_error_handler.errors,
            [f"{description} for file: {file_name}" for _ in range(0, errors_count)]
        )