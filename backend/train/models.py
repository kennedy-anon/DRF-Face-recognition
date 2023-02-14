from django.db import models


# for storing the names of the face vectors
class FaceName(models.Model):
    face_id = models.AutoField(primary_key=True, unique=True)
    face_name = models.TextField(max_length=255)


# stores True or False to notify of new encodings
class NewEncoding(models.Model):
    unfetchedEncoding = models.BooleanField(default=True)


'''
# storing face encodings
class FaceEncoding(models.Model):
    face_id = models.ForeignKey(FaceName, on_delete=models.CASCADE)
    face_encoding = models.TextField()
'''