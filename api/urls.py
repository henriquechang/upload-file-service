from django.urls import path

from api.views.upload_view import UploadView

urlpatterns = [
    path('upload', UploadView.as_view())
]
