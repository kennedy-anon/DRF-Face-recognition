from rest_framework import permissions, authentication ,generics

from testModel.models import FaceSearchLog
from .serializers import FaceSearchLogSerializer
from api.permissions import IsSeniorOfficerPermission


# view for retrieving searchlogs
class FaceSearchLogView(generics.ListAPIView):
    queryset = FaceSearchLog.objects.all()
    serializer_class = FaceSearchLogSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsSeniorOfficerPermission]

search_log_view = FaceSearchLogView.as_view()