from django.db import models
from django.conf import settings

from train.models import FaceName


# for storing face search logs
class FaceSearchLog(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT) # id of authenticated user
    face_id = models.ForeignKey(FaceName, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
