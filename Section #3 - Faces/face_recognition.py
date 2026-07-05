#pylint:disable=no-member

import os
import numpy as np
import cv2 as cv

BASE_DIR = os.path.dirname(__file__)

haar_cascade = cv.CascadeClassifier(os.path.join(BASE_DIR, 'haar_face.xml'))

people = ['Ben Afflek', 'Elton John', 'Jerry Seinfield', 'Madonna', 'Mindy Kaling', 'momoy2']
# features = np.load('features.npy', allow_pickle=True)
# labels = np.load('labels.npy')

face_recognizer = cv.face.LBPHFaceRecognizer_create()
face_recognizer.read(os.path.join(BASE_DIR, 'face_trained.yml'))

img_path = os.path.join(BASE_DIR, '..', 'Resources', 'Photos', 'momoy2.jpg')
img = cv.imread(img_path)
if img is None:
    raise FileNotFoundError(f"Could not read image: {img_path}")

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('Person', gray)

# Detect the face in the image
faces_rect = haar_cascade.detectMultiScale(gray, 1.1, 4)

for (x, y, w, h) in faces_rect:
    faces_roi = gray[y:y + h, x:x + w]

    label, confidence = face_recognizer.predict(faces_roi)
    print(f'Label = {people[label]} with a confidence of {confidence}')

    cv.putText(img, str(people[label]), (20, 20), cv.FONT_HERSHEY_COMPLEX, 1.0, (0, 255, 0), thickness=2)
    cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)

cv.imshow('Detected Face', img)

# Save the output image into Section 3 output folder
# Save the output image into Section 3 output folder with a name-based filename
out_name = 'momoy2 face recognition result.jpg'
out_path = os.path.join(BASE_DIR, '..', 'Section 3 output', out_name)
cv.imwrite(out_path, img)

cv.waitKey(0)
