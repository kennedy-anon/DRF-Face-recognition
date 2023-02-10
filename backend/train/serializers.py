from rest_framework import serializers

#import ast

from .models import FaceName #FaceEncoding,


# serializes the training images
class ImageSerializer(serializers.Serializer):
    images = serializers.ListField(child=serializers.ImageField())


# serializes the names of the faces
class FaceNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaceName
        fields = [
            'face_id',
            'face_name'
        ]


'''
# serializes the face_encodings
class FaceEncodingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaceEncoding
        fields = [
            'face_id',
            'face_encoding'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['face_encoding'] = ast.literal_eval(representation['face_encoding'])
        return representation
        '''