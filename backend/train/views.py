from rest_framework import generics
from rest_framework.response import Response

import face_recognition
import pymongo

from .serializers import ImageSerializer
from .models import FaceName, NewUpdates #, FaceEncoding

#connecting to mongodb
client = pymongo.MongoClient("mongodb+srv://Kennedy:Les5OoybneIII08V@cluster0.dtj0s4t.mongodb.net/?retryWrites=true&w=majority")

#Define mongoDB Name
db = client['face_encoding_vectors']

#Define mongoDB Collection
collection = db['face_encodings']


#storing face encodings in mongoDB
def store_face_encodings(face_id, face_encoding):
    face_encoding_values = {
        "face_id": face_id,
        "face_encoding": face_encoding.tolist()
    }

    collection.insert_one(face_encoding_values)


# receives the training face images
class ImagesUploadView(generics.CreateAPIView):
    serializer_class = ImageSerializer

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

            # saving the face name to mysql database
            face_name, created = FaceName.objects.get_or_create(face_name=name)
            stored_face_id = face_name.face_id

            # saving the face encoding to the mongoDB database
            store_face_encodings(stored_face_id, enconding)

        #notifying testModel view of new changes
        update, created = NewUpdates.objects.get_or_create(updateCategory='unfetchedEncodings', newChanges = True)   
        update.newChanges = True
        update.save()

        return Response({"Message": "Training completed successfully."})

receive_images_view = ImagesUploadView.as_view()