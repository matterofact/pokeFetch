
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

    # Clear the frame
    for widget in frm.winfo_children():
        widget.destroy()

    # List to store entry widgets
    entry_widgets = []

    # Create entry widgets for Pokémon party members
    for i in range(1, 7):
        party_member_label = tk.Label(frm, text="Pokemon " + str(i) + ":", font=('', 15))
        party_member_label.pack(pady=5)

        party_member_entry = ttk.Entry(frm, font=('', 15))
        party_member_entry.pack(pady=5)

        # Add the entry widget to the list
        entry_widgets.append(party_member_entry)

    # Submit button
    submit_party_button = ttk.Button(frm, text='Submit Party', command=lambda: submitParty(entry_widgets, user_id, root, frm))
    submit_party_button.pack(pady=10)

def submitParty(entry_widgets, user_id, root, frm):
    # Collect the values from the entry widgets
    party_data = [entry.get() for entry in entry_widgets]

    # Print collected data for debugging (you can replace this with actual database insertion code)
    print("Collected Party Data:")
    for i, pokemon in enumerate(party_data, start=1):
        print(f"Pokemon {i}: {pokemon}")
    
    # Insert the data into the database
    insert_party_into_db(user_id, party_data, root, frm)

def insert_party_into_db(user_id, party_data, root, frm):
    c.execute('''
        INSERT INTO parties (user_id, pokemon1, pokemon2, pokemon3, pokemon4, pokemon5, pokemon6)
        VALUES (?, ? ,?, ?, ?, ?, ?)
    ''', (user_id, *party_data))
    db.commit()

    partiesWindow(root, frm, user_id)

    
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
    loginButton.pack(pady=20)

    registerButton = ttk.Button(frm, text="Register", command=lambda: registerWindow(root, frm))
    registerButton.pack()
    root.mainloop()
  
def partiesWindow(root, frm, user_id):
    root.title("Parties")
    frm.destroy()
    frm = ttk.Frame(root, padding=10)
    frm.pack()

    parties = c.execute(
            "SELECT * FROM parties WHERE user_id = ?", [user_id]
        )
    parties = c.fetchall()

    # Remove the first two elements from each tuple
    for i in range(0,len(parties)):
        party_contents = [party[2:] for party in parties]
        party = ttk.Label(frm, text='Party ' + str(i+1))
        party.pack()
        # Button to view detailed summary of the first party for demonstration
        summary_button = ttk.Button(frm, text='View Party Summary', command=lambda i=i: partySummaryWindow(root, frm, user_id, parties[i][2:]))
        summary_button.pack(pady=10)

    new_party_button = ttk.Button(frm, text="New party", command=lambda: createParty(root, frm, user_id))
    new_party_button.pack()


# TODO Allow user to delete parties from the database
def partySummaryWindow(root, frm, user_id, party):
    # Clear the frame
    for widget in frm.winfo_children():
        widget.destroy()

    root.title("Party Summary")

    # Create a new frame for the party summary
    summary_frame = ttk.Frame(frm, padding=10)
    summary_frame.grid()

    # Fetch and display each Pokémon's sprite and name
    for i, pokemon_name in enumerate(party):
        if pokemon_name:
            pokemon = pypokedex.get(name=str(pokemon_name).lower())
            poke_name = pokemon.name.title()
            sprite_url = pokemon.sprites.front['default']
            response = requests.get(sprite_url)
            sprite_image = PIL.Image.open(BytesIO(response.content))
            sprite_photo = ImageTk.PhotoImage(sprite_image)

            name_label = ttk.Label(summary_frame, text=poke_name, font=('', 15))
            name_label.grid(column=0, row=i, padx=5, pady=5, sticky='w')

            # Display the sprite and name
            sprite_label = ttk.Label(summary_frame, image=sprite_photo)
            sprite_label.image = sprite_photo  # Keep a reference to avoid garbage collection
            sprite_label.grid(column=1, row=i, padx=5, pady=5)

    # Back button to go back to the parties window
    back_button = ttk.Button(summary_frame, text='Back', command=lambda: partiesWindow(root, frm, user_id))
    back_button.grid(column=0, row=len(party) + 1, columnspan=2, pady=10)
 

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
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    frm.grid_columnconfigure(0, weight=1)
    frm.grid_rowconfigure(0, weight=1)
    frm.focus()

    pokemon = pypokedex.get(name=search)
    dexId = str(pokemon.dex)
    pokeName = pokemon.name.title()
    url = pokemon.sprites.front['default']
    stats = pokemon.base_stats
    response = requests.get(url)
    temp = PIL.Image.open(BytesIO(response.content))
    sprite = ImageTk.PhotoImage(temp)

    types = ', '.join([t.title() for t in pokemon.types])
    abilities = ', '.join([a[0].title() for a in pokemon.abilities])

    # Creating widgets
    labels = [
        ("Pokedex ID: ", dexId),
        ("Name: ", pokeName),
        ("Type: ", types),
        ("Ability: ", abilities),
        ("Stats: ", ""),
        ("HP: ", stats[0]),
        ("Attack: ", stats[1]),
        ("Defense: ", stats[2]),
        ("Sp Atk: ", stats[3]),
        ("Sp Def: ", stats[4]),
        ("Speed: ", stats[5]),
    ]

    spriteImg = tk.Label(frm, image=sprite)
    spriteImg.grid(column=0, row=0, columnspan=2, pady=10)

    for i, (label_text, value_text) in enumerate(labels, start=1):
        tk.Label(frm, text=label_text, font=('', 15)).grid(column=0, row=i, sticky='w', padx=5)
        tk.Label(frm, text=value_text, font=('', 15)).grid(column=1, row=i, sticky='w', padx=5)

    # Adding a blank label to create a gap
    blankLabel = tk.Label(frm, text="")
    blankLabel.grid(column=0, row=len(labels) + 1, pady=10)

    search_label = ttk.Label(frm, text="Search for a Pokemon: ", font=('', 15))
    pokeSearch = tk.StringVar()
    searchBox = ttk.Entry(frm, textvariable=pokeSearch, font=('', 15))
    searchButton = ttk.Button(frm, text="Search", command=lambda: clear_window(root, frm, pokeSearch.get(), user_id))
    partiesButton = ttk.Button(frm, text="Parties", command=lambda: partiesWindow(root, frm, user_id))

    search_label.grid(column=0, row=len(labels) + 2, sticky='w', padx=5)
    searchBox.grid(column=1, row=len(labels) + 2, sticky='w', padx=5)
    searchButton.grid(column=2, row=len(labels) + 2, sticky='w', padx=5)
    partiesButton.grid(column=0, row=len(labels) + 3, sticky='w', pady=10)

    root.mainloop()

root = Tk()
root.geometry("525x750")
frm = ttk.Frame(root, padding=10)
loginWindow(frm)