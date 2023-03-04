from rest_framework import serializers

from testModel.models import FaceSearchLog


# serializing the fields to be read
class FaceSearchLogSerializer(serializers.ModelSerializer):
    crime_officer_id = serializers.IntegerField(source='user_id.id')
    # crime_officer_name = serializers.StringRelatedField(source='user_id.username')
    crime_officer_name = serializers.SerializerMethodField()
    # face_name = serializers.StringRelatedField(source='face_id.face_name')
    face_name = serializers.SerializerMethodField()
    search_date = serializers.DateTimeField(source='created_at')
    log_id = serializers.IntegerField(source='id')

    class Meta:
        model = FaceSearchLog
        fields = [
            'log_id',
            'crime_officer_id',
            'crime_officer_name',
            'face_id',
            'face_name',
            'search_date'
        ]

    # capitalizing face name
    def get_face_name(self, obj):
        return obj.face_id.face_name.capitalize()

    # combining first_name and last_name
    def get_crime_officer_name(self, obj):
        full_name = (obj.user_id.first_name.capitalize())+ " " + (obj.user_id.last_name.capitalize())

        return full_name