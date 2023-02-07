from rest_framework import serializers


class ImageSerializer(serializers.Serializer):
    images = serializers.ListField(child=serializers.ImageField())