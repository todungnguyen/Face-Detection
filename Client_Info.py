from pymongo import MongoClient
from tkinter import *
import random
from PIL import Image, ImageTk 
import base64
import io
import time
from bson.objectid import ObjectId
import threading
from DataBase import * 

client = MongoClient('mongodb+srv://admin:admin@cluster0.o6hxp.mongodb.net/retryWrites=true&w=majority')
db = client.shop 
people = db.people

def get_list_client():
    list_person = people.find({"InShop" : 1})
    ps = []
    for p in list_person:
        ps.append(p)
    return ps

def person_to_text(p):
    s = ""
    list = ["Image"]
    for k, v in p.items():
        if k not in list:
            s = s + str(k) + ":" + str(v) + '\n'
    return s


def show_client(seconds):
    root = Tk()
    root.geometry("+20+20")
    ps = get_list_client()
    r = 0
    c = 0
    max_c = 5
    for i in range(len(ps)):
        image = ImageTk.PhotoImage(string_to_image(ps[i]['Image']).resize((200, 120), Image.ANTIALIAS))
        
        label_img = Label(root, image = image)
        label_img.photo = image   
        label_img.grid(row = r, column = c)

        label_text = Label(root, text = person_to_text(ps[i])).grid(row = r+1, column = c)
        if ps[i]['voleur'] != 0:
            label_text.config(bg = "red")
        if c == max_c - 1:
            c = 0
            r = r + 2
        else:
            c = c + 1
    root.after(seconds*1000, lambda: root.destroy())
    root.mainloop()


def repeat():
    start_time = time.time()
    seconds = 10
    
    show_client(seconds)
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        
        if elapsed_time > seconds:
            show_client(seconds)  
repeat()