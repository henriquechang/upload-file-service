from rest_framework.response import Response
from rest_framework.views import APIView


class UploadView(APIView):

    def post(self, request, format=None):
        return Response()
