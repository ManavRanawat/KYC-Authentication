import imutils
from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os
import json
import cv2
from imutils.video import VideoStream
from .opencv_face import crop_image

def verify(pth,name): 
    knownEncodings = []
    knownNames = []
    vs = VideoStream(src=0).start()
    writer = None
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    while True:
        frame = vs.read()
        frame = cv2.flip(frame,1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #rgb = imutils.resize(frame, width=750)
        faces = face_cascade.detectMultiScale(rgb,1.1,4)
        if len(faces)>=1:
            #print("rxvx")
            boxes = face_recognition.face_locations(rgb,model="cnn")
            encodings = face_recognition.face_encodings(rgb, boxes)
            #print(encodings,boxes)
            for encoding in encodings:
                #print("baap")
                knownEncodings.append(encoding)
                knownNames.append(name)

        resized_img = cv2.resize(frame,(1000,700))
        cv2.imshow('Image',resized_img)
        if cv2.waitKey(1)==ord('q'):
            break
    
    cv2.destroyAllWindows()
    vs.stop()

    #print("[INFO] serializing encodings...")
    data = {"encodings": knownEncodings, "names": knownNames}
    #print(data)

    image = cv2.imread(pth)
    # print(image)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb,
        model="cnn" )
    encodings = face_recognition.face_encodings(rgb, boxes)

    names = []
    right = 0
    # print(encodings)
    for encoding in encodings:
        matches = face_recognition.compare_faces(data["encodings"],encoding)
        name = "Unknown"

        if True in matches:
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
            print("Captured:",len(data['names']),"Matched:",max(counts.values()))
            right = max(counts.values())
            name = max(counts, key=counts.get)
        #print(name)
    names.append(name)
    if right/len(data['names'])>0.6:
        return names[0]
    else:
        return "Unknown"

#print(verify(  opencv_face.crop_image('jash2.jpeg') ,'Person'))
