from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .serializers import UserSerializer, ChangePasswordSerializer

User = get_user_model()


# retrieves user details given an access token
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

retrieve_user_view = UserDetailView.as_view()


# update user password
class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # check if old passwords match
            old_password = serializer.validated_data.get('old_password')
            if not user.check_password(old_password):
                return Response({'old_password': ['Wrong password.']}, status=400)
            
            # check if the new password meets the password policy
            new_password = serializer.validated_data.get('new_password')
            try:
                validate_password(new_password, user=user)
            except ValidationError as e:
                return Response({'new_password': e.messages}, status=400)
            
            # set new password
            user.set_password(new_password)
            user.save()
            return Response({'detail': 'Password updated successfully.'}, status=200)
        
        return Response(serializer.errors, status=400)
    
change_password_view = ChangePasswordView.as_view()