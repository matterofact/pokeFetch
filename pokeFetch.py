
import requests
import urllib3
import pypokedex
import sys
import faulthandler
import tkinter as tk
import PIL.Image
import io
import sqlite3

from PIL import Image, ImageTk
from tkinter import *
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import Entry
from tkinter import messagebox
from io import BytesIO
from werkzeug.security import check_password_hash, generate_password_hash

db = sqlite3.connect('pokeFetch.db')
c = db.cursor()


# Code to create parties table:
#db.execute(
 #           "CREATE TABLE IF NOT EXISTS 'portfolios' (portfolio_id INTEGER NOT NULL, symbol TEXT, shares INTEGER POSITVE, price FLOAT POSITIVE, total FLOAT POSITIVE, FOREIGN KEY (portfolio_id) REFERENCES users(id))"
  #      )






def login(username, password):
    #if username = valid and password = valid:
    #username = username_entry.get()
    #password = password_entry.get()
    user = db.execute(
        "SELECT * FROM users WHERE username = ?", [username]
    )
    print(user)
    if not user:
        loginWindow()
    passwordHash = c.fetchone()
    print(passwordHash)

    summaryWindow('bulbasaur')

def loginWindow():
    root = Tk()
    root.geometry("500x500")
    root.title("Login")
    frm = ttk.Frame(root, padding=10)
    frm.pack()


    username_label = tk.Label(frm, text="Username: ")
    username_label.pack()
    username_entry = ttk.Entry(frm, font=('',15))
    username_entry.pack()

    password_label = tk.Label(frm, text="Password: ")
    password_label.pack()
    password_entry = ttk.Entry(frm, font=('',15), show='*')
    password_entry.pack()

    loginButton = ttk.Button(frm, text="Login")
    loginButton.pack()
    username = username_entry.get()
    password = password_entry.get()
    loginButton.command = login(str(username), str(password))
    root.mainloop()


  
def partiesWindow():
    pass

def registerWindow():
    root = Tk()
    root.geometry("500x500")
    root.title("Login")
    frm = ttk.Frame(root, padding=10)
    frm.pack()


    username_label = tk.Label(frm, text="Username: ")
    username_label.pack()
    username_entry = ttk.Entry(frm, font=('',15))
    username_entry.pack()

    password_label = tk.Label(frm, text="Password: ")
    password_label.pack()
    password_entry = ttk.Entry(frm, font=('',15), show='*')
    password_entry.pack()

    password_confirmation_label = tk.Label(frm, text="Confirm Password: ")
    password_confirmation_label.pack()
    password_confirmation_entry = ttk.Entry(frm, font=('',15), show='*')
    password_confirmation_entry.pack()
 
## Check if username exists in database, if not, enter user into database
    
    # Code to create a new user:
#db.execute (
 #           "INSERT INTO users (username, hash) VALUES(?, ?)", username, generate_password_hash(password)
  #      )

def summaryWindow(search):

    http = urllib3.PoolManager()

    root = Tk()
    root.geometry("500x500")
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    frm.grid_columnconfigure(10, minsize=100)
    frm.grid_rowconfigure(10, minsize=100)

    pokemon = pypokedex.get(name=search)
    dexId = str(pokemon.dex)
    pokeName = pokemon.name.title()
    url = pokemon.sprites.front['default']
    response = requests.get(url)
    temp = PIL.Image.open(BytesIO(response.content))
    sprite = ImageTk.PhotoImage(temp)

    if len(pokemon.types) > 1:
        types = str(pokemon.types[0]).title() + ', ' + str(pokemon.types[1]).title()
    else:
        types = str(pokemon.types[0]).title()
    
    spriteImg = Label(frm, image=sprite).grid(column=0, row=0)
    idLabel = ttk.Label(frm, text="ID: ", font=('',15), ).grid(column=0, row=1, sticky='w')
    idValue = ttk.Label(frm, text=dexId, font=('',15), ).grid(column=1, row=1, sticky='w') 
    nameLabel = ttk.Label(frm, text="Name: ", font=('',15), ).grid(column=0, row=2, sticky='w')
    nameValue = ttk.Label(frm, text=pokeName, font=('',15), ).grid(column=1, row=2, sticky='w')
    typeLabel = ttk.Label(frm, text="Type: ", font=('', 15)).grid(column=0, row=3, sticky='w')
    typeValue = ttk.Label(frm, text=types, font=('',15)).grid(column=1, row=3, sticky='w')
    search_label = ttk.Label(frm, text="Search for a Pokemon: ", font=('',15)).grid(column=0, row=4, stick='w')
    pokeSearch = tk.StringVar()
    searchBox = ttk.Entry(frm, textvariable=pokeSearch, font=('',15))
    searchBox.grid(column=0, row=5)
    searchButton = ttk.Button(frm, text="Search")
    searchButton.grid(column=0, row=6, sticky='w')
    root.mainloop()
    searchButton.command=callback(pokeSearch.get())

loginWindow()