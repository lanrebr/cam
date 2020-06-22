import requests
from base64 import b64encode
import face_recognition
import numpy as np
import pickle

#see https://github.com/ageitgey/face_recognition/issues/120
# https://pypi.org/project/face-recognition/
def get_image():
    url = "http://192.168.1.76/image.jpg"
    user = "admin"
    pwd = "pasoresa"
    auth = "Basic {}".format(b64encode(bytes(f"{user}:{pwd}", "utf-8")).decode("ascii"))
    headers = { 'Authorization' : auth }
    resp = requests.get(url, headers=headers )
    print("status code " + str(resp.status_code))
    if resp.status_code == 200:
        return resp.content,True
    else:
        print(resp.text)
        return {"error":resp.status_code},False

#def save_image(content):
#    with open('camera.jpg', 'wb') as handler:
#        handler.write(content)

all_face_encodings = {}
img1 = face_recognition.load_image_file("kennedy.jpg")
all_face_encodings["kennedy"] = face_recognition.face_encodings(img1)[0]

img1 = face_recognition.load_image_file("obama.jpg")
all_face_encodings["obama"] = face_recognition.face_encodings(img1)[0]

#img1 = face_recognition.load_image_file("michelle.jpg")
#all_face_encodings["michelle"] = face_recognition.face_encodings(img1)[0]

#img2 = face_recognition.load_image_file("sophia.jpg")
#all_face_encodings["sophia"] = face_recognition.face_encodings(img2)[0]

with open('dataset_faces.dat', 'wb') as f:
    pickle.dump(all_face_encodings, f)

# Load face encodings
with open('dataset_faces.dat', 'rb') as f:
	all_face_encodings = pickle.load(f)

# Grab the list of names and the list of encodings
face_names = list(all_face_encodings.keys())
face_encodings = np.array(list(all_face_encodings.values()))

unknown_image = face_recognition.load_image_file("obamas.jpg")
face_locations = face_recognition.face_locations(unknown_image)
#face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="cnn")
for face_location in face_locations:
    top, right, bottom, left = face_location
    print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

unknown_face = face_recognition.face_encodings(unknown_image)
result = face_recognition.compare_faces(face_encodings, unknown_face)

# Print the result as a list of names with True/False
names_with_result = list(zip(face_names, result))
print(names_with_result)

unknown_image = face_recognition.load_image_file("sophia.jpg")
face_locations = face_recognition.face_locations(unknown_image)
for face_location in face_locations:
    top, right, bottom, left = face_location
    print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

