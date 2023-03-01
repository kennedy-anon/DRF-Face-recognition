from django.contrib.auth.models import User
from rest_framework import serializers


# serializes the user details
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            'email', 
            'first_name', 
            'last_name'
        ]
