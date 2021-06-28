####################################################################################
#  Ce fichier contient les 3 fonction principal de notre programe        ##########
##################################################################################

###########################################################################
#####    Importation des bibliotheque            #########################
#########################################################################
from keras.models import load_model
from time import sleep
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np
from Recognize import * 
import argparse
from DataBase import * 

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
############################################
###  Accées à la base de donnée   #########
##########################################
client = MongoClient('mongodb+srv://admin:admin@cluster0.o6hxp.mongodb.net/retryWrites=true&w=majority')
db = client.shop
people = db.people

#######################################################
###   Imporation du model de detection d'emotion #####
#####################################################
face_classifier=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
classifier = load_model('EmotionDetectionModel.h5')
class_labels=['Angry','Happy','Neutral','Sad','Surprise']


##################################################
####   La fonction qui s'execute à l'entrée #####
################################################
def Main_function_in ():
    cap=cv2.VideoCapture(0)
    known_face_encoding , known_face_names =  Image_recover (people)
    known_face_encodings = [] 
    for image in known_face_encoding : 
        try : 
            known_face_encodings.append(encode_face(np.array(image))[0][0])
        except : 
            continue 
    while True:
        ret,frame=cap.read()
        labels=[]
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces=face_classifier.detectMultiScale(gray,1.3,5)
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray=gray[y:y+h,x:x+w]
            roi_gray=cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)

            if np.sum([roi_gray])!=0:
                roi=roi_gray.astype('float')/255.0
                roi=img_to_array(roi)
                roi=np.expand_dims(roi,axis=0)

                preds=classifier.predict(roi)[0]
                #preds_ourModel = myModel.predict(roi)[0]
                label = class_labels[preds.argmax()]
                label_position=(x,y)
            
    
                cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3)
                easy_face_reco_In(frame, known_face_encodings, known_face_names,cap,label,people)
            
            #show_information (people)
            else:
                cv2.putText(frame,'No Face Found',(20,20),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3)
    
        cv2.imshow('Cliquez sur Q pour arreter le programme <3',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

##################################################
####   La fonction qui s'execute à la sortie ####
################################################

def Main_function_Out ():
    cap=cv2.VideoCapture(0)
    known_face_encoding , known_face_names =  Image_recover (people)
    known_face_encodings = [] 
    for image in known_face_encoding : 
        try : 
            known_face_encodings.append(encode_face(np.array(image))[0][0])
        except : 
            continue 

    while True:
        ret,frame=cap.read()
        labels=[]
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces=face_classifier.detectMultiScale(gray,1.3,5)
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray=gray[y:y+h,x:x+w]
            roi_gray=cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)

            if np.sum([roi_gray])!=0:
                roi=roi_gray.astype('float')/255.0
                roi=img_to_array(roi)
                roi=np.expand_dims(roi,axis=0)

                preds=classifier.predict(roi)[0]
                #preds_ourModel = myModel.predict(roi)[0]
                label = class_labels[preds.argmax()]
                label_position=(x,y)
            
    
                cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3)
                easy_face_reco_Out(frame, known_face_encodings, known_face_names,cap,label,people)
            
            #show_information (people)
            else:
                cv2.putText(frame,'No Face Found',(20,20),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3)
    
        cv2.imshow('Cliquez sur Q pour arreter le programme <3',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

##################################################
####   La fonction qui s'execute à la Caisse ####
################################################

def Main_function_Caisee ():
    cap=cv2.VideoCapture(0)
    known_face_encoding , known_face_names =  Image_recover (people)
    known_face_encodings = [] 
    for image in known_face_encoding : 
        try : 
            known_face_encodings.append(encode_face(np.array(image))[0][0])
        except : 
            continue 

    while True:
        ret,frame=cap.read()
        labels=[]
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces=face_classifier.detectMultiScale(gray,1.3,5)
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray=gray[y:y+h,x:x+w]
            roi_gray=cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)

            if np.sum([roi_gray])!=0:
                roi=roi_gray.astype('float')/255.0
                roi=img_to_array(roi)
                roi=np.expand_dims(roi,axis=0)
                preds=classifier.predict(roi)[0]
                label = class_labels[preds.argmax()]
                label_position=(x,y)
                cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3)
                easy_face_reco_caisse(frame, known_face_encodings, known_face_names,cap,label,people,100)
            else:
                cv2.putText(frame,'No Face Found',(20,20),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3)
        cv2.imshow('Cliquez sur Q pour arreter le programme <3',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

