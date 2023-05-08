from rest_framework import authentication, generics, permissions
from rest_framework.response import Response

import cv2
import face_recognition
import numpy as np
import os
import tempfile
import pymongo
import base64

from .serializers import ImageSerializer, FaceSearchLogSerializer
from train.models import FaceName, NewUpdates
from api.permissions import IsCrimeOfficerPermission

#connecting to mongodb
client = pymongo.MongoClient("MongoDB URL")

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


# compose the return response
def composeResponse(face_details, face_image):
    # converting image to bas64
    image_str = cv2.imencode('.jpg', face_image)[1].tostring()
    b64_image = base64.b64encode(image_str).decode('utf-8')

    data = {
        'face_detail': face_details,
        'face_image': b64_image
    }

    return (data)
    '''
            cv2.imwrite("./output.jpg", face_image)

            with open('./output.jpg', "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

            response_data = {
                'image': encoded_string
            }'''
 

# drawing a rectangle to enclose the face
def drawFaceRectangle(top, right, bottom, left, face_image, face_index, face_name, green, blue):
    # green rectacgle for a match and red for unknown
    cv2.rectangle(face_image, (left, top), (right, bottom), (0, green, blue), 2)
    cv2.rectangle(face_image, (left, bottom - 15), (right, bottom), (0, green, blue), cv2.FILLED)
    font = cv2.FONT_HERSHEY_DUPLEX

    if face_name != "Unknown":
        # identified face ..green rectangle
        cv2.putText(face_image, str(face_index) + "." + face_name, (left + 6, bottom - 6 ), font, 1.0, (255, 255, 255), 1)
    else:
        # unknown face image ..red rectangle
        cv2.putText(face_image, str(face_index) + "." + face_name, (left + 6, bottom - 6 ), font, 1.0, (255, 255, 255), 1)
    
    return face_image


# check if there has been new encodings after previous fetch
def checkNewEncodings():
    update = NewUpdates.objects.get(updateCategory='unfetchedEncodings')
    unfetchedEncodings = update.newChanges

    if update.newChanges:
        update.newChanges = False
        update.save()

    return unfetchedEncodings


# creating a search face log
def logFaceSearch(face_id):
    serializer = FaceSearchLogSerializer(data={
        'user_id': RecognizeFaceView.authenticated_user_id,
        'face_id': face_id
    })

    if serializer.is_valid():
        serializer.save()

    '''...without using serializers
    user = User.objects.get(id=RecognizeFaceView.authenticated_user_id)
    face = FaceName.objects.get(face_id=face_id)
    FaceSearchLog(user_id=user, face_id=face).save()'''


# creating a face detail for every face in the image
def faceDetail(face_index, face_name, face_id):
    face_detail = {
                'face_no': face_index,
                'face_name': face_name,
                'face_id': face_id
            }
    
    return face_detail


#comparing the face encoding with the known encoding vectors
def compareFaceVectors(face_encodings, face_locations, face_image):
    face_details = [] # stores the details of the face
    # face_names = [] # for multiple faces in one image
    face_index = 1 # for labelling faces...face 1 matches to index 0 on face_names...

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        #matching...returns boolean list...default tolerance 0.6
        matches = face_recognition.compare_faces(RecognizeFaceView.known_face_encodings, face_encoding)
        face_id = ""
        #print(matches)

        # calculating similarity between unknown image and known images encodings
        #the smaller the face_distance the more similar the face...Euclidean distance
        face_distances = face_recognition.face_distance(RecognizeFaceView.known_face_encodings, face_encoding)
        # retrieving min value...returns an index
        best_match = np.argmin(face_distances)
        #print(face_distances)

        if matches[best_match]:
            #getting the face id for the match
            face_id = RecognizeFaceView.known_face_ids[best_match]
            face_name = (retrieve_face_name(face_id)).capitalize()

            # face_names.append(face_name)

            face_details.append(faceDetail(face_index, face_name, face_id)) # composing face details

            #drawing a green rectangle on the face image
            face_image = drawFaceRectangle(top, right, bottom, left, face_image, face_index, face_name, 255, 0)

            # logging a face search entry
            logFaceSearch(face_id)

        else:
            face_name = "No match found."
            # face_names.append(face_name)

            face_details.append(faceDetail(face_index, face_name, face_id)) # composing face details

            # red rectangle for no match
            face_image = drawFaceRectangle(top, right, bottom, left, face_image, face_index, "Unknown", 0, 255)

        face_index += 1

    # create response
    response_data = composeResponse(face_details, face_image)
    return response_data
        
 
# the view for recognizing unknown image
class RecognizeFaceView(generics.CreateAPIView):
    serializer_class = ImageSerializer
    #authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [IsCrimeOfficerPermission]

    known_face_encodings = []
    known_face_ids = []
    authenticated_user_id = ''

    def post(self, request, *args, **kwargs):
        # retrieve user id for search logging
        RecognizeFaceView.authenticated_user_id = request.user.id

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

            if checkNewEncodings() or len(self.known_face_encodings) == 0:
                # fetches known encodings if not available or if there have been an update
                fetch_face_encodings()
            
            #finding a match
            send_response = compareFaceVectors(face_encodings, face_locations, loaded_image)
 
            return Response(send_response, status=200)
        else:
            return Response({"detail": "Ensure the uploaded image has a face and its clear."}, status=400)

recognize_image_view = RecognizeFaceView.as_view()
