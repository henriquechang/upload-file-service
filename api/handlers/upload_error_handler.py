class UploadErrorHandler:

    def __init__(self):
        self.errors = []

    def add_upload_error(self, description: str, bucket: str):
        """Adds upload error to error array

          :param description: Error description message
          :param bucket: bucket name for reference
        """
        self.errors.append(f'{description}. Upload to bucket: ' + bucket + ' failed.')

