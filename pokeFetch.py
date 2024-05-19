
import requests
import urllib3
import pypokedex
import sys
import faulthandler
import tkinter as tk
import PIL.Image
import PIL
import io
import sqlite3
import bcrypt

from PIL import Image, ImageTk
from tkinter import *
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import Entry
from tkinter import messagebox
from io import BytesIO
from urllib.error import HTTPError


db = sqlite3.connect("pokeFetch.db")
c = db.cursor()


def clear_window(root, frm, search, user_id):
    frm.destroy()
    try: 
        pypokedex.get(name=search)  
    except PyPokedexHTTPError as err:
        if err.code == 404:
            clear_window(root, ttk.Frame(root, padding=10), 'bulbasaur', user_id)
        else:
            pass
    summaryWindow(search, root, frm, user_id)

def createParty(root, frm, user_id):
    # TODO Need to allow for looping submission of pokemon into a party, and then insert into the parties database
    for i in range(1,7):
        party_member_label  = tk.Label(frm, text="Pokemon " + str(i) + ":")
        party_member_label.pack()
        party_member_entry = ttk.Entry(frm, font=('',15))
        party_member_entry.pack()
    submit_party_button = ttk.Button(text='Submit Party')


def hash_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())

def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password, hashed_password)

def login(u, p, root, frm):
    user = c.execute(
        "SELECT username FROM users WHERE username = ?", [u]
    )

    username = c.fetchone()[0]

    user_id = c.execute(
        "SELECT id FROM users WHERE username = ?", [u]
    )

    user_id = c.fetchone()[0]

    passwordHash = c.execute(
        "SELECT password_hash FROM users WHERE username = ?", [u]
    )
    passwordHash = c.fetchone()[0]

    # Check if password is correct, if not, destroy the frm and try again
    if check_password(p, passwordHash):
        frm.destroy()
        summaryWindow('bulbasaur', root, frm, user_id)
    else:
        loginWindow(frm)

def loginWindow(frm):
    frm.destroy()
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

    loginButton = ttk.Button(frm, text="Login", command=lambda: login(username_entry.get(), password_entry.get(), root, frm))
    loginButton.pack()

    registerButton = ttk.Button(frm, text="Register", command=lambda: registerWindow(root, frm))
    registerButton.pack()
    root.mainloop()
  
def partiesWindow(root, frm, user_id):
    root.title("Parties")
    frm.destroy()
    frm = ttk.Frame(root, padding=10)
    frm.pack()
    c.execute(
            "SELECT * FROM parties WHERE user_id = ?", [user_id]
        )
    new_party_button = ttk.Button(frm, text="New party", command=lambda: createParty(root, frm, user_id))
    new_party_button.pack() 

    pass

def registerWindow(root, frm):

    root.title("Register")
    frm.destroy()
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

    password = password_entry.get()
    passwordConfirmation = password_confirmation_entry.get()
    
    registerButton = ttk.Button(frm, text="Register", command=lambda: register(root, frm, username_entry.get(), password_entry.get(), password_confirmation_entry.get()))
    registerButton.pack()

    loginButton = ttk.Button(frm, text="Login", command=lambda: loginWindow(frm))
    loginButton.pack()

def register(root, frm, username, password, passwordConfirmation):
    if password == passwordConfirmation:
        c.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hash_password(password))
        )
        db.commit()
        frm.destroy()
        frm = ttk.Frame(root, padding=10)
        frm.pack() 
        tk.Label(frm, text="Registered!").pack()
        tk.Button(frm, text="Login", command=lambda: loginWindow(frm)).pack()
 
## Check if username exists in database, if not, enter user into database
    
# Code to create a new user:
#db.execute (
 #           "INSERT INTO users (username, hash) VALUES(?, ?)", username, generate_password_hash(password)
  #      )


# TODO Need to check the api gives a valid response before creating the summary window. 
# If it returns a pyPokedexError or a HTTP error, it should just recreate the current frame

def summaryWindow(search, root, frm, user_id):
    http = urllib3.PoolManager()
    root.title("Summary: " + search.title())
    frm = ttk.Frame(padding=10)
    frm.grid()
    frm.grid_columnconfigure(16, minsize=100)
    frm.grid_rowconfigure(16, minsize=100)
    frm.focus()

    pokemon = pypokedex.get(name=search)       
    dexId = str(pokemon.dex)
    pokeName = pokemon.name.title()
    url = pokemon.sprites.front['default']
    stats = pokemon.base_stats
    response = requests.get(url)
    temp = PIL.Image.open(BytesIO(response.content))
    sprite = ImageTk.PhotoImage(temp)

    if len(pokemon.types) > 1:
        types = str(pokemon.types[0]).title() + ', ' + str(pokemon.types[1]).title()
    else:
        types = str(pokemon.types[0]).title()
    
    if len(pokemon.abilities) > 1:
        abilities = str(pokemon.abilities[0][0]).title() + ', ' + str(pokemon.abilities[1][0]).title()
    else:
        abilities = str(pokemon.abilities[0][0]).title()

    # TODO Abilities don't render text properly
    spriteImg = Label(frm, image=sprite).grid(column=0, row=0)
    idLabel = Label(frm, text="Pokedex ID: ", font=('',15)).grid(column=0, row=1, sticky='w')
    idValue = Label(frm, text=dexId, font=('',15)).grid(column=1, row=1, sticky='w') 
    nameLabel = Label(frm, text="Name: ", font=('',15)).grid(column=0, row=2, sticky='w')
    nameValue = Label(frm, text=pokeName, font=('',15)).grid(column=1, row=2, sticky='w')
    typeLabel = Label(frm, text="Type: ", font=('', 15)).grid(column=0, row=3, sticky='w')
    typeValue = Label(frm, text=types, font=('',15)).grid(column=1, row=3, sticky='w')
    abilitiesLabel = Label(frm, text="Ability: ", font=('', 15)).grid(column=0, row=4, sticky='w')
    abilitiesValue = Label(frm, text=abilities, font=('', 15)).grid(column=1, row=4)
    Label(frm, text='', font=('',15)).grid(column=1, row=4, sticky='w')
    statsLabel = Label(frm, text="Stats: ", font=('',15)).grid(column=0, row=5, sticky='w')
    Label(frm, text='', font=('',15)).grid(column=1, row=6, sticky='w')
    hpLabel = Label(frm, text="HP: ", font=('', 15)).grid(column=0, row=7, sticky='w')
    hpValue = Label(frm, text=stats[0], font=('',15)).grid(column=1, row=7, sticky='w')
    atkLabel = Label(frm, text="Attack: ", font=('', 15)).grid(column=0, row=8, sticky='w')
    atkValue = Label(frm, text=stats[1], font=('',15)).grid(column=1, row=8, sticky='w')
    defLabel = Label(frm, text="Defence: ", font=('', 15)).grid(column=0, row=9, sticky='w')
    defValue = Label(frm, text=stats[2], font=('',15)).grid(column=1, row=9, sticky='w')
    sp_atkLabel = Label(frm, text="Sp Atk: ", font=('', 15)).grid(column=0, row=10, sticky='w')
    sp_atkValue = Label(frm, text=stats[3], font=('',15)).grid(column=1, row=10, sticky='w')
    sp_defLabel = Label(frm, text="Sp Def: ", font=('', 15)).grid(column=0, row=11, sticky='w')
    sp_defValue = Label(frm, text=stats[4], font=('',15)).grid(column=1, row=11, sticky='w')
    speedLabel = Label(frm, text="Speed: ", font=('', 15)).grid(column=0, row=12, sticky='w')
    speedValue = Label(frm, text=stats[5], font=('',15)).grid(column=1, row=12, sticky='w')
    Label(frm, text='', font=('',15)).grid(column=1, row=13, sticky='w')

    # TODO Add ability to press enter to hit search and login buttons
    search_label = ttk.Label(frm, text="Search for a Pokemon: ", font=('',15)).grid(column=0, row=14, sticky='w')
    pokeSearch = tk.StringVar()
    searchBox = ttk.Entry(frm, textvariable=pokeSearch, font=('',15))
    searchBox.grid(column=0, row=15)
    searchButton = ttk.Button(frm, text="Search", command=lambda: clear_window(root, frm, pokeSearch.get(), user_id))
    searchButton.grid(column=2, row=15, sticky='w')
    partiesButton = ttk.Button(frm, text="Parties", command=lambda: partiesWindow(root, frm, user_id))
    partiesButton.grid(column=0, row=16, sticky='w')
    root.mainloop()

root = Tk()
root.geometry("500x750")
frm = ttk.Frame(root, padding=10)
loginWindow(frm)