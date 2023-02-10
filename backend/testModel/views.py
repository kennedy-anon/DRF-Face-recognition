from rest_framework import generics
from rest_framework.response import Response

import cv2
import face_recognition
import numpy as np
import os
import tempfile
import pymongo

from .serializers import ImageSerializer

#connecting to mongodb
client = pymongo.MongoClient("mongodb+srv://Kennedy:Les5OoybneIII08V@cluster0.dtj0s4t.mongodb.net/?retryWrites=true&w=majority")

#Declare mongoDB Name
db = client['face_encoding_vectors']

#Declare mongoDB Collection
collection = db['face_encodings']


# fetching the face encodings from mongoDB
def fetch_face_encodings():
    face_encodings_doc = list(collection.find({}))
    face_ids, face_encodings = [face_doc["face_id"] for face_doc in face_encodings_doc], [face_doc["face_encoding"] for face_doc in face_encodings_doc]

    RecognizeFaceView.known_face_encodings = np.array(face_encodings)
    RecognizeFaceView.known_face_ids = face_ids


#comparing the face encoding with the known encoding vectors
def compareFaceVectors(face_encodings, face_locations):
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces( face_encoding)

 
class RecognizeFaceView(generics.CreateAPIView):
    serializer_class = ImageSerializer
    known_face_encodings = []
    known_face_ids = []
    
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

            if len(self.known_face_encodings) == 0:
                # fetches known encodings if not available
                fetch_face_encodings()
 
            return Response({"message": "Testing Api"})
        else:
            return Response({"detail": "Ensure the uploaded image has a face and its clear."}, status=400)

recognize_image_view = RecognizeFaceView.as_view()