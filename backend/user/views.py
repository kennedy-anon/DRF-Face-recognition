from rest_framework import generics
from django.contrib.auth import get_user_model

from .serializers import UserSerializer

User = get_user_model()


# retrieves user details given an access token
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

retrieve_user_view = UserDetailView.as_view()