from rest_framework import generics

from testModel.models import FaceSearchLog
from .serializers import FaceSearchLogSerializer


# view for retrieving searchlogs
class FaceSearchLogView(generics.ListAPIView):
    queryset = FaceSearchLog.objects.all()
    serializer_class = FaceSearchLogSerializer

search_log_view = FaceSearchLogView.as_view()