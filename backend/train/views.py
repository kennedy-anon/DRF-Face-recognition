from rest_framework import generics
from rest_framework.response import Response

import face_recognition

from .serializers import ImageSerializer
from .models import FaceName, FaceEncoding


class ImagesUploadView(generics.CreateAPIView):
    serializer_class = ImageSerializer
    known_names = []
    known_name_encodings = []

    def post(self, request, *args, **kwargs):

        #validating images
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        images = serializer.validated_data['images']
        
        for image in images:
            #calculating face enconding vectors
            loaded_image = face_recognition.load_image_file(image)
            enconding = face_recognition.face_encodings(loaded_image)[0]
            name = (image.name.split("."))[0]

            # saving the encoding to the database
            face_name, created = FaceName.objects.get_or_create(face_name=name)
            face_encoding = FaceEncoding.objects.create(face_id=face_name, face_encoding=enconding)
            
            self.known_name_encodings.append(enconding)
            self.known_names.append(name)

        return Response({"Message": "Training completed successfully."})

receive_images_view = ImagesUploadView.as_view()