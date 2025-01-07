from rest_framework import serializers
from .models import UserUpload

class UserUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserUpload
        fields = ['id', 'file', 'script', 'uploaded_at', 'processed_audio', 'processed_video', 'processed_at']