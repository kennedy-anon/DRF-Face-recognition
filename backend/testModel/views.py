from rest_framework import generics
from rest_framework.response import Response

import cv2
import face_recognition
from tempfile import NamedTemporaryFile

from .serializers import ImageSerializer

 
class RecognizeFaceView(generics.CreateAPIView):
    serializer_class = ImageSerializer
    
    def post(self, request, *args, **kwargs):
        # validating the image
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image = serializer.validated_data['image']

        #writting the image to a temporary file to read it
        with NamedTemporaryFile(delete=True) as temp_file:
            temp_file.write(image.read())
            temp_file.seek(0)
            loaded_image = cv2.imread(temp_file.name)

            # start here 
            if loaded_image is None:
                print("it is none")
            else:
                print("it is not none")

        #finding the face location in the image
        face_locations = face_recognition.face_locations(loaded_image)

        return Response(face_locations)

recognize_image_view = RecognizeFaceView.as_view()