from rest_framework import generics
from rest_framework.response import Response

import cv2
import face_recognition
import os
import tempfile

from .serializers import ImageSerializer

#comparing the face encoding with the known encoding vectors
def compareFaceVectors(face_encodings, face_locations):
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces( face_encoding)

 
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
            #calculating the face encoding vector
            face_encodings = face_recognition.face_encodings(loaded_image, face_locations)
            return Response(face_encodings)
        else:
            return Response({"detail": "Ensure the uploaded image has a face and its clear."}, status=400)

recognize_image_view = RecognizeFaceView.as_view()