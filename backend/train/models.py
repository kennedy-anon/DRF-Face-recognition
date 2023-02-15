from django.db import models

# for storing the names of the face vectors
class FaceName(models.Model):
    face_id = models.AutoField(primary_key=True, unique=True)
    face_name = models.TextField(max_length=255)


# for notifying of any new changes like new encondings
class NewUpdates(models.Model):
    updateCategory = models.CharField(max_length=40, unique=True)
    newChanges = models.BooleanField()

'''
# storing face encodings
class FaceEncoding(models.Model):
    face_id = models.ForeignKey(FaceName, on_delete=models.CASCADE)
    face_encoding = models.TextField()
'''