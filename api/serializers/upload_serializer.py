from rest_framework import serializers


class UploadSerializer(serializers.Serializer):
    file = serializers.FileField(allow_empty_file=False)
    max_size = 5000000

    def validate_file(self, value):
        if value.size > self.max_size:
            raise serializers.ValidationError(f'File size exceeded maximum value of {self.max_size/1000000} Mb')
        return value
