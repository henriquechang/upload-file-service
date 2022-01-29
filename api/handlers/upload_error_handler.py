class UploadErrorHandler:

    def __init__(self):
        self.errors = []

    def add_upload_error(self, description: str, file_name: str):
        """Adds upload error to error array

          :param description: Error description message
          :param file_name: file name for reference
        """
        self.errors.append(f'{description} for file: ' + file_name)

