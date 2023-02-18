from rest_framework import serializers

from .models import FaceSearchLog


# serializes the incoming face image
class ImageSerializer(serializers.Serializer):
    image = serializers.ImageField()


# for serializing the search log entries
class FaceSearchLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaceSearchLog
        fields = [
            'user_id',
            'face_id',
            'created_at'
        ]

        read_only_fields = [
            'created_at'
        ]