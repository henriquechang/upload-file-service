from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.upload_serializer import UploadSerializer


class UploadView(APIView):

    def post(self, request, format=None):

        serializer = UploadSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serializer.errors
            )

        file = request.FILES['file']
        return Response()
