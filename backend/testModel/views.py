from rest_framework import generics
from rest_framework.response import Response

import cv2
import face_recognition
import numpy as np
import os
import tempfile
import pymongo

from .serializers import ImageSerializer
from train.models import FaceName

#connecting to mongodb
client = pymongo.MongoClient("mongodb+srv://Kennedy:Les5OoybneIII08V@cluster0.dtj0s4t.mongodb.net/?retryWrites=true&w=majority")

#Declare mongoDB Name
db = client['face_encoding_vectors']

#Declare mongoDB Collection
collection = db['face_encodings']


# fetching the known face encodings from mongoDB
def fetch_face_encodings():
    face_encodings_doc = list(collection.find({}))
    face_ids, face_encodings = [face_doc["face_id"] for face_doc in face_encodings_doc], [face_doc["face_encoding"] for face_doc in face_encodings_doc]

    RecognizeFaceView.known_face_encodings = np.array(face_encodings)
    RecognizeFaceView.known_face_ids = face_ids


# retrieving all details of the matched face from mysql db
def retrieve_face_name(face_id):
    face_name_obj = FaceName.objects.get(face_id=face_id)
    face_name = face_name_obj.face_name

    return face_name

#comparing the face encoding with the known encoding vectors
def compareFaceVectors(face_encodings, face_locations):
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        #matching...returns boolean list...default tolerance 0.6
        matches = face_recognition.compare_faces(RecognizeFaceView.known_face_encodings, face_encoding)
        face_id = ""
        #print(matches)

        # calculating similarity between unknown image and known images encodings
        #the smaller the face_distance the more similar the face...Euclidean distance
        face_distances = face_recognition.face_distance(RecognizeFaceView.known_face_encodings, face_encoding)
        # retrieving min value
        best_match = np.argmin(face_distances)
        #print(face_distances)

        if matches[best_match]:
            #getting the face id for the match
            face_id = RecognizeFaceView.known_face_ids[best_match]
            face_name = retrieve_face_name(face_id)

            # edit to handle multiple faces in one photo
            return face_name
        else:
            return "There was no match."
        
 
 # the view for recognizing unknown image
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
            
            #finding a match
            face_name = compareFaceVectors(face_encodings, face_locations)
 
            return Response(face_name)
        else:
            return Response({"detail": "Ensure the uploaded image has a face and its clear."}, status=400)

recognize_image_view = RecognizeFaceView.as_view()