from abc import ABC, abstractmethod

from django.core.files.uploadedfile import InMemoryUploadedFile


class BaseS3Service(ABC):

    @abstractmethod
    def upload_file(self, file: InMemoryUploadedFile, bucket: str):
        pass