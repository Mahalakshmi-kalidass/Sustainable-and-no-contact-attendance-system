import os
import numpy as np
import cv2
import pandas as pd
import time
import datetime

def facerecognizer(sub):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('/home/balaji/Downloads/Innovative_and_creative_project/Facerecognition_based_attendance_system/Trainer/Trainer.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades+cascadePath);
    df = pd.read_csv("/home/balaji/Downloads/Innovative_and_creative_project/Facerecognition_based_attendance_system/studentdetails/studentdetail.csv")


    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ["Enrol_id", "Enrol_Name"]
    attendance = pd.DataFrame(columns=col_names)

    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video widht
    cam.set(4, 480) # set video height

    # Define min window size to be recognized as a face
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)

    while True:
        ret, img =cam.read()
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
        )
        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,255,255), 2)
            Id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

        # Check if confidence is less them 100 ==> "0" is perfect match 
            if (confidence < 70):
                print(Id)
                e_name = df.loc[df["Enrol_id"] == Id]["Enrol_name"].values

                attendance.loc[len(attendance.index)] = [
                                Id,
                                e_name,
                            ]
            

            else:
                Id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))

            cv2.putText(img, str(Id), (x+5,y-5), font, 1, (0,0,0), 2)
            #cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,0,0), 1)
            attendance = attendance.drop_duplicates(
                       subset = ['Enrol_id'], keep="first"
                    )
            
            cv2.imshow('camera',img)
        k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break
        ts = time.time()
        #attendance[date] = 1
        date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
        Hour, Minute, Second = timeStamp.split(":")
        fileName = ("/home/balaji/Downloads/Innovative_and_creative_project/Facerecognition_based_attendance_system/Attendance/"+sub+"/"+
                    date
                    + "_"
                    + Hour
                    + "-"
                    + Minute
                    + ".csv"
                )
    attendance = attendance.drop_duplicates(["Enrol_id"], keep="first")
    print(attendance)

    cam.release()
    cv2.destroyAllWindows()

#facerecognizer()
    attendance.to_csv(fileName, index=False)
