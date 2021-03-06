import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

# to access the images in the folder
path = 'participants'
images = []
classNames = []

# used the os dependency to grab the list of images in my directory
photos = os.listdir(path)
print(photos)
print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')


# load all our images from the directory
for photo in photos:

    currPhoto = cv2.imread(f'{path}/{photo}')

# append all the photos and only the file name with no extension to the lists created earlier
    images.append(currPhoto)
    classNames.append(os.path.splitext(photo)[0])
print(classNames)

# a function to encode the know photos
def findEcodings (imgList):
    encodeList = []
    for img in imgList:
        # convert the image to black and white
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # get the face encoding
        encodedImg = face_recognition.face_encodings(img)[0]
        encodeList.append(encodedImg)
    return encodeList

def markAtt(name):
    with open('Attendance.csv', 'r+') as f:
        # to ensure recoding attendance just once
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])

        # find arrival time if person is not on attendance list already
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')
        print(myDataList)









encodeknownList = findEcodings(images)
print('Encoding Complete')

# initialise the webcam
cap = cv2.VideoCapture(0)
# while loop to capture each frame one by one
while True:
    # read frame from a camera
    success, img = cap.read()
    # Resize the captured to a reasonable size
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    # locate all the faces in the current frame
    facesCurrFrame = face_recognition.face_locations(imgS)
    # encoding the faces in the current frame
    encodesCurrFrame = face_recognition.face_encodings(imgS, facesCurrFrame)

    for encodeFace, faceLoc in zip(encodesCurrFrame, facesCurrFrame):
        matches = face_recognition.compare_faces(encodeknownList, encodeFace)
        faceDis = face_recognition.face_distance(encodeknownList, encodeFace)
        # print(faceDis)
        # to get index of matching face
        matchIndex = np.argmin(faceDis)


        # draw rectangles on candidates faces
        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            # print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*5, x1*5
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            markAtt(name)



    cv2.imshow('Webcam', img)
    cv2.waitKey(1)
