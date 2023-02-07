from rest_framework import generics
from rest_framework.response import Response

import face_recognition

from .serializers import ImageSerializer


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
            
            self.known_name_encodings.append(enconding)
            self.known_names.append(image.name.capitalize())

        return Response(self.known_name_encodings)

receive_images_view = ImagesUploadView.as_view()