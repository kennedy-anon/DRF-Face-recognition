from rest_framework import generics
from rest_framework.response import Response

import cv2
import face_recognition
import os
import tempfile
#from tempfile import NamedTemporaryFile

from .serializers import ImageSerializer

 
class RecognizeFaceView(generics.CreateAPIView):
    serializer_class = ImageSerializer
    
    def post(self, request, *args, **kwargs):
        # validating the image
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image = serializer.validated_data['image']

        # Writing the image to a temporary file
        temp_file_handle, temp_file_path = tempfile.mkstemp()
        with os.fdopen(temp_file_handle, 'wb') as f:
            f.write(image.read())
        
        # Reading the image from the temporary file
        loaded_image = cv2.imread(temp_file_path, cv2.IMREAD_COLOR)

        # Removing the temporary file
        os.remove(temp_file_path)

        #finding the face location in the image
        face_locations = face_recognition.face_locations(loaded_image)

        #confirming the image has a face
        if face_locations:
            print("there is a face")
        else:
            print(face_locations)
            print("there is no face")

        return Response(face_locations)

recognize_image_view = RecognizeFaceView.as_view()