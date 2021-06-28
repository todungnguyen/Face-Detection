from pymongo import MongoClient
import tkinter as tk
from PIL import Image, ImageTk 
import base64
import io
import numpy as np
from pymongo import MongoClient 
from bson.objectid import ObjectId
# the document is stored in a variable called peopleDocument.
import datetime
def insert_new_client (col, EmotionIn  ,image,EmotionOut= "nothing") : 
    string_image = image_to_string(image)
    date = datetime.datetime.now()
    #date = str(date)
    new_client = {"Image":string_image , "nb_visit" : 0 , "nb_achat" : 0 , "mean_shop" : 0 , "Emotion_in" : EmotionIn, "Emotion_out" : EmotionOut ,"first_visite" : date , "Last_visite" : date , "voleur" : 0 , "probaAchat" : 0.5, "InShop" : 1, "updateCaisse" : 0 }
    x = col.insert_one(new_client)
    return x.inserted_id

def select_client (idc,col) : 
    x = col.find_one({"_id" : ObjectId(idc)})
    return (x)

def update_caisse (idc,prix,people) :
    my_query = { "_id": ObjectId(idc)}
    X = select_client(idc,people)
    #print(X)
    new_nb_achat = X["nb_achat"] +1 
    if X["mean_shop"] == 0 : 
        newPrix =  (prix )
    else : 
        newPrix =  (X["mean_shop"] + prix ) / 2
    new_values = { "$set": {"mean_shop": newPrix ,  "nb_achat" :new_nb_achat , 
                             "updateCaisse" : 1} }
    x = people.update_one(my_query, new_values)


def update_out (idc,  people,EmotionOut) :
    my_query = { "_id": ObjectId(idc)}
    X = select_client(idc,people)
    date = datetime.datetime.now()
    #print(X)
    new_nb_visit = X["nb_visit"] +1 
    new_nb_achat = X["nb_achat"]
    new_proba = new_nb_achat  / (new_nb_visit)  
    new_values = { "$set": {"probaAchat" : new_proba , "Last_visite" : date ,"nb_visit"  :new_nb_visit ,"updateCaisse" : 0,"Emotion_out" : EmotionOut,"InShop": 0 } }
    people.update_one(my_query, new_values)

def update_In_shop (idc, people) : 
    #X = select_client (idc,col)
    #inShop = X ["InShop"]
    myquery = { "_id": ObjectId(idc) }
    newvalues = { "$set":{ "InShop": 1}}
    people.update_one(myquery, newvalues)



def image_to_string(image):
    print("typeImage" , type(image))
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format="PNG")
    imgByteArr = imgByteArr.getvalue()
    return base64.b64encode(imgByteArr).decode('utf-8')

def string_to_image(img_str):
    imgdata = base64.b64decode(str(img_str))
    return Image.open(io.BytesIO(imgdata))

def Image_recover (col): 
    list_person = col.find()
    listImage = []
    listID = []
    for p in list_person:
       # print("last print " ,np.array( string_to_image(p["Image"])).shape)
        listImage.append( (string_to_image(p["Image"])))
        listID.append(str(p["_id"]))
    
    return listImage , listID 

import numpy as np

def person_to_text(p):
    s = ""
    for k, v in p.items():
        if k != 'Image':
            s = s + str(k) + ":" + str(v) + '\n'
    return s

def show_information (people) : 
    list_person = people.find({"InShop" : 1})
    ps = []
    for p in list_person:
        ps.append(p)


    root = tk.Tk()

    r = 0
    c = 0
    # 2 images per lines
    max_c = 4
    for i in range(len(ps)):
        image = ImageTk.PhotoImage(string_to_image(ps[i]['Image']).resize((300, 200), Image.ANTIALIAS))
        label_img = tk.Label(image = image)
        label_img.photo = image   
        label_img.grid(row = r, column = c)

        label_text = tk.Label(text = person_to_text(ps[i])).grid(row = r+1, column = c)
    
        if c == max_c - 1:
            c = 0
            r = r + 2
        else:
            c = c + 1
    
    root.mainloop()