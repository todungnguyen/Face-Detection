################################################################################
####  ce fichier contient le programme qui permet la reconnaisance Faciale ####
##############################################################################



###########################################################################
#####    Importation des bibliotheque            #########################
#########################################################################
from tkinter import *
import cv2
import random as rd
import dlib
import PIL.Image 
import numpy as np
from imutils import face_utils
import argparse
from PIL import Image
from pathlib import Path
import os
import ntpath
from DataBase import * 
from bson.objectid import ObjectId

#######################################################
###   Imporation du model de detection d'emotion #####
#####################################################
pose_predictor_68_point = dlib.shape_predictor("pretrained_model/shape_predictor_68_face_landmarks.dat")
face_encoder = dlib.face_recognition_model_v1("pretrained_model/dlib_face_recognition_resnet_model_v1.dat")
face_detector = dlib.get_frontal_face_detector()



def transform(image, face_locations):
    ''' Cette fonction recupere les coordoonées d'un visage sur une image '''
    coord_faces = []
    for face in face_locations:
        rect = face.top(), face.right(), face.bottom(), face.left()
        coord_face = max(rect[0], 0), min(rect[1], image.shape[1]), min(rect[2], image.shape[0]), max(rect[3], 0)
        coord_faces.append(coord_face)

    return coord_faces


def encode_face(image):
    face_locations = face_detector(image, 1)
    
    face_encodings_list = []
    landmarks_list = []
    for face_location in face_locations:
        # DETECT FACES
        shape = pose_predictor_68_point(image, face_location)
        face_encodings_list.append(np.array(face_encoder.compute_face_descriptor(image, shape, num_jitters=1)))
        # GET LANDMARKS
        shape = face_utils.shape_to_np(shape)
        landmarks_list.append(shape)
    face_locations = transform(image, face_locations)
    return face_encodings_list, face_locations, landmarks_list


def easy_face_reco_In(frame, known_face_encodings, known_face_names,cap,EmotionIn,col):
    rgb_small_frame = frame[:, :, ::-1]
    # ENCODING FACE
    face_encodings_list, face_locations_list, landmarks_list = encode_face(rgb_small_frame)
    face_names = []

    for face_encoding,face_location in zip(face_encodings_list,face_locations_list) :
        if len(face_encoding) == 0 :
            return np.empty((0))
        if not len(known_face_encodings) == 0 : 
            vectors = np.linalg.norm(known_face_encodings - face_encoding, axis=1)
        else : 
            vectors =[]
        tolerance = 0.6
        result = []
        for vector in vectors:
            if vector <= tolerance:
                result.append(True)
            else:
                result.append(False)
        if True in result:
            first_match_index = result.index(True)
            name = known_face_names[first_match_index]
            update_In_shop (name, col)
        else:
            name = "Unknown"
            return_value, image = cap.read()
            s='known_faces/' +  "test.png"
            cv2.imwrite(s, image)
            image = PIL.Image.open(s)
            size =  image.size
            (top, right, bottom, left) = face_location 
            box = (max(0,left-40), max(0,top-40), min(right+40,size[0] ),bottom )
            area = image.crop(box)
            image = np.array(area)
            try : 
                new_client = insert_new_client ( col, EmotionIn  ,area , EmotionOut= "nothing")
                face_encoded = encode_face(image)[0][0]
                known_face_encodings.append(face_encoded)
                known_face_names.append(str(new_client))
            except : 
                continue 
            

        face_names.append(name)
    for (top, right, bottom, left), name in zip(face_locations_list, face_names):
     
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.rectangle(frame, (left, bottom - 30), (right, bottom), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, name, (left + 2, bottom - 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)

    for shape in landmarks_list:
        for (x, y) in shape:
            cv2.circle(frame, (x, y), 1, (255, 0, 255), -1)




def easy_face_reco_Out(frame, known_face_encodings, known_face_names,cap,EmotionOut,col):
    rgb_small_frame = frame[:, :, ::-1]
    # ENCODING FACE
    face_encodings_list, face_locations_list, landmarks_list = encode_face(rgb_small_frame)
    face_names = []

    for face_encoding,face_location in zip(face_encodings_list,face_locations_list) :
        if len(face_encoding) == 0 :
            return np.empty((0))
        # CHECK DISTANCE BETWEEN KNOWN FACES AND FACES DETECTED
        if not len(known_face_encodings) == 0 : 
            vectors = np.linalg.norm(known_face_encodings - face_encoding, axis=1)
        else : 
            vectors =[]
        tolerance = 0.6
        result = []
        for vector in vectors:
            if vector <= tolerance:
                result.append(True)
            else:
                result.append(False)
        if True in result:
            first_match_index = result.index(True)
            name = known_face_names[first_match_index]
            X =  select_client (name,col)
            test1 = X["updateCaisse"] 
            test2 = X ["InShop"]
            if (test2 == 1 )  : 
                update_out (name, col ,EmotionOut)
        face_names.append(name)
    for (top, right, bottom, left), name in zip(face_locations_list, face_names):
     
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.rectangle(frame, (left, bottom - 30), (right, bottom), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, name, (left + 2, bottom - 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)

    for shape in landmarks_list:
        for (x, y) in shape:
            cv2.circle(frame, (x, y), 1, (255, 0, 255), -1)

result = ""
def get_price(test, price):
    global result
    result = price.get()
    test.destroy()


def call_test():
    test = Tk()
    price = StringVar()
    Champ = Entry(test, textvariable= price)
    Champ.focus_set()
    Champ.place(x = 0, y = 0)
    Bouton = Button(test, text ='Valider', command = lambda: get_price(test, price))
    Bouton.place(x = 50, y = 50)
    test.mainloop()
    return result

import threading
def my_thread():
    try:
        t = threading.Thread(target=call_test)

        t.start()
    except:
        print("Error: unable to start thread")


def easy_face_reco_caisse(frame, known_face_encodings, known_face_names,cap,EmotionIn,col,prix):
    rgb_small_frame = frame[:, :, ::-1]
    # ENCODING FACE
    face_encodings_list, face_locations_list, landmarks_list = encode_face(rgb_small_frame)
    face_names = []

    for face_encoding,face_location in zip(face_encodings_list,face_locations_list) :
        if len(face_encoding) == 0 :
            return np.empty((0))
        # CHECK DISTANCE BETWEEN KNOWN FACES AND FACES DETECTED
        if not len(known_face_encodings) == 0 : 
            vectors = np.linalg.norm(known_face_encodings - face_encoding, axis=1)
        else : 
            vectors =[]
        tolerance = 0.6
        result = []
        for vector in vectors:
            if vector <= tolerance:
                result.append(True)
            else:
                result.append(False)
        if True in result:
            first_match_index = result.index(True)
            name = known_face_names[first_match_index]

            #date_now =  datetime.datetime.now()
            X =  select_client (name,col)
            test = X["updateCaisse"] 
            prixx = (rd.random() * 100)  +10 
            #########################################################
            #cap.release()
            #prixxx = (call_test())
            #frame.start()
            #############################################
            #update_caisse (name, prix , col )
            if (test==0 ) : 
                update_caisse (name, prixx, col )
                
        else:
            name = "Unknown"
            return_value, image = cap.read()
            s='known_faces/' +  "test.png"
            cv2.imwrite(s, image)
            image = PIL.Image.open(s)
            size =  image.size
            (top, right, bottom, left) = face_location 
            box = (max(0,left-40), max(0,top-40), min(right+40,size[0] ),bottom )
            area = image.crop(box)
            new_client = insert_new_client ( col, EmotionIn  ,area , EmotionOut= "nothing")
            date_now =  datetime.datetime.now()
            X =  select_client (new_client,col)
            diff_date = date_now -  X["Last_visite"]
            if (diff_date.seconds > 1500 ) : 
                update_caisse (new_client, prix , col )
            image = np.array(area)
            face_encoded = encode_face(image)[0][0]
            known_face_encodings.append(face_encoded)
            known_face_names.append(str(new_client))
            

        face_names.append(name)
    for (top, right, bottom, left), name in zip(face_locations_list, face_names):
     
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.rectangle(frame, (left, bottom - 30), (right, bottom), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, name, (left + 2, bottom - 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)

    for shape in landmarks_list:
        for (x, y) in shape:
            cv2.circle(frame, (x, y), 1, (255, 0, 255), -1)