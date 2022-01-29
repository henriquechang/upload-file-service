from rest_framework import status
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_422_UNPROCESSABLE_ENTITY
from rest_framework.response import Response
from rest_framework.views import APIView

from api.controllers.upload_controller import UploadController
from api.handlers.upload_error_handler import UploadErrorHandler
from api.serializers.upload_serializer import UploadSerializer
from api.services.s3_service import S3Service


class UploadView(APIView):

    s3_service = S3Service()
    upload_error_handler = UploadErrorHandler()
    upload_controller = UploadController(
        s3_service=s3_service,
        error_handler=upload_error_handler
    )

    def post(self, request, format=None):

        self.upload_error_handler.errors.clear()

        serializer = UploadSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serializer.errors
            )

        file = request.FILES['file']
        uploaded = self.upload_controller.send_to_buckets(file)
        if uploaded:
            return Response(status=HTTP_204_NO_CONTENT)
        errors = self.upload_error_handler.errors
        return Response(data={"errors": errors}, status=HTTP_422_UNPROCESSABLE_ENTITY)
