# -*- coding: utf-8 -*-
# +
from tkinter import *
from tkinter.messagebox import * # boîte de dialogue
from PIL import Image, ImageTk 

from pymongo import MongoClient
import base64
import io
import time
from bson.objectid import ObjectId
import threading
from App import * 


# -

def run_my_repeat(nouvel):
    nouvel.destroy()
    repeat()


def call_nouvel(fenetre):
    fenetre.destroy()
    nouvel= Tk()
    w = 750
    h = 650
    nouvel.geometry(str(w) + "x" + str(h))
    nouvel.title('Accueil')
        
    img = ImageTk.PhotoImage(Image.open("ue17.png").resize((w, h), Image.ANTIALIAS))
    panel = Label(nouvel, image = img)
    panel.place(x = 0, y = 0)
    
    w = w/3
    h = h/6
   #Création du bouton entree :
    L_entree = Button(nouvel, bg='cyan',fg='black',font=("Arial",20),text='Vidéo_Entrée', width=16,height=2,relief='raised', command =  Main_function_in )
    L_entree.place(x = w, y = h)
    #Création du bouton Info:
    L_info = Button(nouvel,text="Infomation_client",font=("Arial",20), bg='cyan',fg='black', width=16, height=2, relief='raised', command=lambda: run_my_repeat(nouvel))
    L_info.place(x = w, y = h + 100)
    #Création du bouton Info:
    L_caisse = Button(nouvel,text="Vidéo_Caisse",font=("Arial",20), bg='cyan',fg='black' , width=16, height=2, relief='raised',command =  Main_function_Caisee)
    L_caisse.place(x = w, y = h + 200)
    #Création du bouton Info:
    sortie = Button(nouvel, bg='cyan',fg='black',font=("Arial",20),text='Vidéo_Sortie', width=16,height=2,relief='raised',command =Main_function_Out)
    sortie.place(x = w, y = h + 300)

    button3 = Button(nouvel, text="Exit_Application", font=("Arial",20), bg='red',fg='black', command=exit, width=16, height=2, relief='raised')
    button3.place(x = w, y = h + 400)

    nouvel.mainloop()


def Verification():
    user = MongoClient('mongodb+srv://admin:admin@cluster0.o6hxp.mongodb.net/retryWrites=true&w=majority').shop.user
    query = user.find_one({"user": Iden.get(), "pass": Motdepasse.get()})
    
    if query != None:
        # le mot de passe est bon : on affiche une boîte de dialogue puis on ferme la fenêtre
        #showinfo('Résultat','Bienvenue')
        call_nouvel(Mafenetre)
        
    else:
        # le mot de passe est incorrect : on affiche une boîte de dialogue
        showwarning('Résultat','Identifiant ou Mot de passe incorrect.\nVeuillez recommencer !')
        Motdepasse.set('')
        Iden.set('')
################################
# Création de la fenêtre principale (main window)
# +
# Création de la fenêtre principale (main window)
Mafenetre = Tk()
Mafenetre.title('Identification requise')
w = 500
h = 300
Mafenetre.geometry(str(w) + "x" + str(h))
img = ImageTk.PhotoImage(Image.open("login.png").resize((w, h), Image.ANTIALIAS))
panel = Label(Mafenetre, image = img)
panel.place(x = 0, y = 0)

w = w/5
h = h/3
# Création d'un widget Label (texte 'Mot de passe')
Label1 = Label(Mafenetre, text = 'Mot de passe ')
Label1.place(x = w, y = h + 50)
# Création d'un widget Entry (champ de saisie)
Motdepasse= StringVar()
Champ1 = Entry(Mafenetre, textvariable= Motdepasse, show='*', bg ='bisque', fg='maroon')
Champ1.focus_set()
Champ1.place(x = w + 100, y = h + 50)

Label2 = Label(Mafenetre, text = 'Identifiant ')
Label2.place(x = w, y = h)
Iden = StringVar()
Champ2 = Entry(Mafenetre, textvariable= Iden, bg ='bisque', fg='maroon')
Champ2.focus_set()
Champ2.place(x = w + 100, y = h)

# Création d'un widget Button (bouton Valider)
Bouton = Button(Mafenetre, text ='Valider', command = Verification)
Bouton.place(x = w + 210, y = h + 100)




def connect(): 
    client = MongoClient('mongodb+srv://admin:admin@cluster0.o6hxp.mongodb.net/retryWrites=true&w=majority')
    db = client.shop 
    people = db.people
    return people


def image_to_string(image):
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format="png")
    imgByteArr = imgByteArr.getvalue()
    return base64.b64encode(imgByteArr).decode('utf-8')


def string_to_image(img_str):
    imgdata = base64.b64decode(str(img_str))
    return Image.open(io.BytesIO(imgdata))


def get_list_client():
    people = connect()
    list_person = people.find({"InShop" : 1})
    ps = []
    for p in list_person:
        ps.append(p)
    return ps


def person_to_text(p):
    s = ""
    list = ["Image", "InShop", "updateCaisse"]
    for k, v in p.items():
        if k not in list:
            s = s + str(k) + ":" + str(v) + '\n'
    return s

def show_client(seconds):
    root = Tk()
    root.geometry("+20+20")
    root.title("Information Client In Shop")
    ps = get_list_client()
    button = Button(root,text="Back",font=("Arial",15), bg="white",fg="black", width=8, height=2, command = lambda: call_nouvel(root))
    button.grid(row=0,column=0, sticky="w")
    r = 1
    c = 0
    max_c = 5
    for i in range(len(ps)):
        image = ImageTk.PhotoImage(string_to_image(ps[i]['Image']).resize((260, 230), Image.ANTIALIAS))
        label_img = Label(root, image = image)
        label_img.photo = image   
        label_img.grid(row = r, column = c)
        
        label_text = Label(root, text = person_to_text(ps[i]), borderwidth=2, relief="solid", highlightbackground="blue").grid(row = r+1, column = c, padx = 5, pady = 5)
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
    seconds = 30
    
    show_client(seconds)
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        
        if elapsed_time > seconds:
            show_client(seconds)  



Mafenetre.mainloop()




