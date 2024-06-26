
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
from pypokedex import exceptions

# TODO Add comments to cite chatgpt usage


db = sqlite3.connect("pokeFetch.db")
c = db.cursor()

# I used ChatGPT to quickly generate a dictionary of all the pokemon types and their effectiveness ratings
type_effectiveness = {
    'normal': {
        'rock': 0.5, 'ghost': 0, 'steel': 0.5,
    },
    'fire': {
        'fire': 0.5, 'water': 0.5, 'grass': 2, 'ice': 2, 'bug': 2, 'rock': 0.5, 'dragon': 0.5, 'steel': 2,
    },
    'water': {
        'fire': 2, 'water': 0.5, 'grass': 0.5, 'ground': 2, 'rock': 2, 'dragon': 0.5,
    },
    'electric': {
        'water': 2, 'electric': 0.5, 'grass': 0.5, 'ground': 0, 'flying': 2, 'dragon': 0.5,
    },
    'grass': {
        'fire': 0.5, 'water': 2, 'grass': 0.5, 'poison': 0.5, 'ground': 2, 'flying': 0.5, 'bug': 0.5, 'rock': 2, 'dragon': 0.5, 'steel': 0.5,
    },
    'ice': {
        'fire': 0.5, 'water': 0.5, 'grass': 2, 'ice': 0.5, 'ground': 2, 'flying': 2, 'dragon': 2, 'steel': 0.5,
    },
    'fighting': {
        'normal': 2, 'ice': 2, 'poison': 0.5, 'flying': 0.5, 'psychic': 0.5, 'bug': 0.5, 'rock': 2, 'ghost': 0, 'dark': 2, 'steel': 2, 'fairy': 0.5,
    },
    'poison': {
        'grass': 2, 'poison': 0.5, 'ground': 0.5, 'rock': 0.5, 'ghost': 0.5, 'steel': 0, 'fairy': 2,
    },
    'ground': {
        'fire': 2, 'electric': 2, 'grass': 0.5, 'poison': 2, 'flying': 0, 'bug': 0.5, 'rock': 2, 'steel': 2,
    },
    'flying': {
        'electric': 0.5, 'grass': 2, 'fighting': 2, 'bug': 2, 'rock': 0.5, 'steel': 0.5,
    },
    'psychic': {
        'fighting': 2, 'poison': 2, 'psychic': 0.5, 'dark': 0, 'steel': 0.5,
    },
    'bug': {
        'fire': 0.5, 'grass': 2, 'fighting': 0.5, 'poison': 0.5, 'flying': 0.5, 'psychic': 2, 'ghost': 0.5, 'dark': 2, 'steel': 0.5, 'fairy': 0.5,
    },
    'rock': {
        'fire': 2, 'ice': 2, 'fighting': 0.5, 'ground': 0.5, 'flying': 2, 'bug': 2, 'steel': 0.5,
    },
    'ghost': {
        'normal': 0, 'psychic': 2, 'ghost': 2, 'dark': 0.5,
    },
    'dragon': {
        'dragon': 2, 'steel': 0.5, 'fairy': 0,
    },
    'dark': {
        'fighting': 0.5, 'psychic': 2, 'ghost': 2, 'dark': 0.5, 'fairy': 0.5,
    },
    'steel': {
        'fire': 0.5, 'water': 0.5, 'electric': 0.5, 'ice': 2, 'rock': 2, 'steel': 0.5, 'fairy': 2,
    },
    'fairy': {
        'fire': 0.5, 'fighting': 2, 'poison': 0.5, 'dragon': 2, 'dark': 2, 'steel': 0.5,
    },
}



def clear_window(root, frm, search, user_id):
    try: 
        pypokedex.get(name=search)  
    except pypokedex.exceptions.PyPokedexError as err:
        if err:
            return
        else:
            frm.destroy()
    summaryWindow(search, root, frm, user_id)

# Used chatgpt to quickly create a form with multiple inputs, and then loop through each of them to add each input to a list which can
# then be passed to the submit party function to be entered into the database

def createParty(root, frm, user_id, pokeName):
    # Looping submission of pokemon into a party, and then insert into the parties database

    # Clear the frame
    for widget in frm.winfo_children():
        widget.destroy()

    # List to store entry widgets
    entry_widgets = []

    # Create entry widget for party name
    party_name_label = tk.Label(frm, text="Party Name:", font=('', 15))
    party_name_label.pack(pady=5)

    party_name_entry = ttk.Entry(frm, font=('', 15))
    party_name_entry.pack(pady=5)

    entry_widgets.append(party_name_entry)

    # Create entry widgets for Pokémon party members
    for i in range(1, 7):
        party_member_label = tk.Label(frm, text="Pokemon " + str(i) + ":", font=('', 15))
        party_member_label.pack(pady=5)

        party_member_entry = ttk.Entry(frm, font=('', 15))
        party_member_entry.pack(pady=5)

        # Add the entry widget to the list
        entry_widgets.append(party_member_entry)

    # Submit button
    submit_party_button = ttk.Button(frm, text='Submit Party', command=lambda: submitParty(entry_widgets, user_id, root, frm, pokeName))
    submit_party_button.pack(pady=10)

    # Back button to go back to the parties window
    back_button = ttk.Button(frm, text='Back', command=lambda: partiesWindow(root, frm, user_id, pokeName))
    back_button.pack()


def submitParty(entry_widgets, user_id, root, frm, pokeName):
    # Collect the values from the entry widgets
    for entry in (entry_widgets):
        if entry.get() == '':
            continue
            try: 
                pypokedex.get(name=entry.get()) 
            except pypokedex.exceptions.PyPokedexError as err:
                if err:
                    messagebox.showerror("Failed to create party", "Invalid pokemon name in party.")
                    return
                
    party_data = [entry.get() for entry in entry_widgets]

 #   for pokemon in party_data:
 #       if pokemon:
 #           try:
 #           except pypokedex.PyPokedexHTTPError:
 ##               pypokedex.get(name=pokemon.lower())
 #               messagebox.showerror("Invalid Pokemon", f"{pokemon} is not a valid Pokemon name.")
 #               return
    # Print collected data for debugging (you can replace this with actual database insertion code)
    # This function was written by chatgpt to allow for keeping track of which names are being submitted into the parties database to make
    # it easier to debug database input before running the insert_party_into_db function and insert them into the database itself
    print("Collected Party Data:")
    print(f"Party name: {party_data[0]}")
    for i, pokemon in enumerate(party_data[1:], start=1):
        print(f"Pokemon {i}: {pokemon}")
    
    # Insert the data into the database
    insert_party_into_db(user_id, party_data, root, frm, pokeName)

def insert_party_into_db(user_id, party_data, root, frm, pokeName):
    c.execute('''
        INSERT INTO parties (user_id, party_name, pokemon1, pokemon2, pokemon3, pokemon4, pokemon5, pokemon6)
        VALUES (?, ?, ? ,?, ?, ?, ?, ?)
    ''', (user_id, *party_data))
    db.commit()

    partiesWindow(root, frm, user_id, pokeName)

# I used bcrypt to hash the passwords and then check entered passwords against the hash, so passwords are stored in the
# database securely and not in plain text
    
def hash_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())

def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password, hashed_password)

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

def login(u, p, root, frm):
    user = c.execute(
        "SELECT username FROM users WHERE username = ?", [u]
    )

    username = c.fetchone()

    if username is None:
        messagebox.showerror("Login Failed", "Invalid username or password.")
        loginWindow(frm)
        return

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
        messagebox.showerror("Login Failed", "Invalid username or password.")
        loginWindow(frm)

  
def partiesWindow(root, frm, user_id, pokeName):
    root.title("Parties")
    frm.destroy()
    frm = ttk.Frame(root, padding=10)
    frm.pack()

    parties = c.execute(
            "SELECT * FROM parties WHERE user_id = ?", [user_id]
        )
    parties = c.fetchall()


    # I had to change this section of the code because chatgpt was assigning party_id to the user_id column instead
    # I've changed the tuple index to 1 from 0, so it now assigns the correct party id to the party when it's deleted
    # This means the function now works correctly and removes the delete party from the database

    # Remove the first two elements from each tuple
    for i, party in enumerate(parties):
        party_id = party[1]
        party_contents = [party[2:] for party in parties]
        if party[8] == None:
            party = ttk.Label(frm, text='Party ' + str(i+1))
        else:
            party = ttk.Label(frm, text=party[8])
        party.pack(pady=10)
        # Button to view detailed summary of the first party for demonstration
        summary_button = ttk.Button(frm, text='View Party Summary', command=lambda i=i, party_id=party_id: partySummaryWindow(root, frm, user_id, party_id, parties[i][2:], pokeName))
        summary_button.pack(pady=10)

        delete_button = ttk.Button(frm, text='Delete Party', command=lambda party_id=party_id: delete_party(party_id, root, frm, user_id, pokeName))
        delete_button.pack(pady=10)

    # Blank label to buffer
    blankLabel = ttk.Label(frm, text='')
    blankLabel.pack()
    blankLabel2 = ttk.Label(frm, text='')
    blankLabel2.pack()
    # New party button to add a new party 
    new_party_button = ttk.Button(frm, text="New party", command=lambda: createParty(root, frm, user_id, pokeName))
    new_party_button.pack()

    # Back button to go back to the summary window
    back_button = ttk.Button(frm, text='Back', command=lambda: summaryWindow(pokeName, root, frm, user_id))
    back_button.pack()

def delete_party(party_id, root, frm, user_id, pokeName):
    try:
        c.execute("DELETE FROM parties WHERE party_id = ? AND user_id = ?", (party_id, user_id))
        db.commit()
        messagebox.showinfo("Success", "Party deleted successfully!")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        partiesWindow(root, frm, user_id, pokeName) 

# I used ChatGPT to quickly create the code for this funciton since it's quite similar to the pokemon summary window.
# There was a bug initially in that code that wouldn't delete parties correctly, so I went through and tweaked how the buttons had their 
# party ids assigned, and that fixed the problem with ChatGPT's code.

def partySummaryWindow(root, frm, user_id, party_id, party, pokeName):
    # Clear the frame
    for widget in frm.winfo_children():
        widget.destroy()

    root.title("Party Summary")

    type_coverage = get_type_coverage(party[:6])

    # Create a new frame for the party summary
    summary_frame = ttk.Frame(frm)
    summary_frame.grid(column=0, rowspan=10, padx=20)

    # Fetch and display each Pokémon's sprite and name
    for i, pokemon_name in enumerate(party[:6]):
        if pokemon_name:
            partyPos = i
            pokemon = pypokedex.get(name=str(pokemon_name).lower())
            poke_name = pokemon.name.title()
            sprite_url = pokemon.sprites.front['default']
            response = requests.get(sprite_url)
            sprite_image = PIL.Image.open(BytesIO(response.content))
            sprite_photo = ImageTk.PhotoImage(sprite_image)
            poke_types = ', '.join([t.title() for t in pokemon.types])

            name_label = ttk.Label(summary_frame, text=poke_name, font=('', 15))
            name_label.grid(column=0, row=i, padx=5, pady=5, sticky='w')

            # Display the sprite and name
            sprite_label = ttk.Label(summary_frame, image=sprite_photo)
            sprite_label.image = sprite_photo  # Keep a reference to avoid garbage collection
            sprite_label.grid(column=1, row=i, padx=5, pady=5)

            types_label = ttk.Label(summary_frame, text=poke_types, font=('', 15))
            types_label.grid(column=2, row=i, padx=5, pady=5)

            delete_button = ttk.Button(summary_frame, text="Delete from party", command=lambda partyPos=partyPos: remove_from_party(root, frm, user_id, party_id, party, pokeName, partyPos))
            delete_button.grid(column=3, row=i, padx=5, pady=5)
        else:
            partyPos = i
            add_pokemon_button = ttk.Button(summary_frame, text="Add pokemon", command=lambda partyPos=partyPos: add_to_party(root, frm, summary_frame, table_frame, user_id, party_id, party, pokeName, partyPos))
            add_pokemon_button.grid(column=3, row=i, padx=5, pady=5)
    strengths = []
    weaknesses = []
    immunities = []

    # Strengths list generation
    for t, count in type_coverage['strengths'].items():
        strengths.append((f"{t.title()}: {count}"))
 

    # Weaknesses list generation
    for t, count in type_coverage['weaknesses'].items():
        weaknesses.append((f"{t.title()}: {count}"))


    # Immunities list generation
    for t, count in type_coverage['immunities'].items():
        immunities.append((f"{t.title()}: {count}"))



    # Create a frame for the table
    table_frame = ttk.Frame(frm)
    table_frame.grid(column=1, row=1)

    # Create a label for type coverage
    type_coverage_label = ttk.Label(frm, text="Party Type Coverage:", font=('', 15))
    type_coverage_label.grid(column=1, row=0) 

    # Column headers
    headers = ["Strengths", "Weaknesses", "No effect"]
    for col, header in enumerate(headers):
        header_label = ttk.Label(table_frame, text=header, font=('', 12, 'bold'))
        header_label.grid(row=0, column=col, padx=5, pady=5)

    # Maximum number of rows for the table
    max_rows = max(len(strengths), len(weaknesses), len(immunities))

    # Fill in the table
    for row in range(max_rows):
        if row < len(strengths):
            strength_label = ttk.Label(table_frame, text=strengths[row])
            strength_label.grid(row=row + 1, column=0, padx=5, pady=5)
        else:
            strength_label = ttk.Label(table_frame, text="")
            strength_label.grid(row=row + 1, column=0, padx=5, pady=5)

        if row < len(weaknesses):
            weakness_label = ttk.Label(table_frame, text=weaknesses[row])
            weakness_label.grid(row=row + 1, column=1, padx=5, pady=5)
        else:
            weakness_label = ttk.Label(table_frame, text="")
            weakness_label.grid(row=row + 1, column=1, padx=5, pady=5)


        if row < len(immunities):
            immunity_label = ttk.Label(table_frame, text=immunities[row])
            immunity_label.grid(row=row + 1, column=2, padx=5, pady=5)
        else:
            immunity_label = ttk.Label(table_frame, text="")
            immunity_label.grid(row=row + 1, column=2, padx=5, pady=5)
 

    # Back button to go back to the parties window, moved to the top for the same reasons as stated in the partiesWindow comments
    back_button = ttk.Button(frm, text='Back', command=lambda: partiesWindow(root, frm, user_id, pokeName))
    back_button.grid(column=0, row=len(party) + 6, pady=10)
            
def get_type_coverage(party):
    type_coverage = {
        'strengths': {},
        'weaknesses': {},
        'immunities': {}
    }

    for pokemon_name in party:
        if pokemon_name:
            pokemon = pypokedex.get(name=pokemon_name.lower())
            counted_types = set()  # To track types already counted for this pokemon

            for types in pokemon.types:
                for target_type, effectiveness in type_effectiveness[types].items():
                    if target_type in counted_types:
                        continue  # Skip if this type has already been counted for this pokemon

                    if effectiveness == 2:
                        if target_type in type_coverage['strengths']:
                            type_coverage['strengths'][target_type] += 1
                        else:
                            type_coverage['strengths'][target_type] = 1
                    elif effectiveness == 0.5:
                        if target_type in type_coverage['weaknesses']:
                            type_coverage['weaknesses'][target_type] += 1
                        else:
                            type_coverage['weaknesses'][target_type] = 1
                    elif effectiveness == 0:
                        if target_type in type_coverage['immunities']:
                            type_coverage['immunities'][target_type] += 1
                        else:
                            type_coverage['immunities'][target_type] = 1
                    
                    counted_types.add(target_type)  # Mark this type as counted for this pokemon

    return type_coverage

def add_to_party(root, frm, summary_frame, table_frame, user_id, party_id, party, pokeName, partyPos):
    # Create entry widget for party name
    print(party_id)
    summary_frame.destroy()
    table_frame.destroy()
    frm.destroy()
    frm = tk.Frame()
    frm.pack()
    add_frame = ttk.Frame(frm)
    add_frame.pack()

    add_pokemon_label = tk.Label(frm, text="Pokemon Name:", font=('', 15))
    add_pokemon_label.pack()

    add_pokemon_entry = ttk.Entry(frm, font=('', 15))
    add_pokemon_entry.pack()

    submit_entry_button = ttk.Button(frm, text="Submit", command=lambda partyPos=partyPos: insert_into_party(root, frm, user_id, party_id, party, add_pokemon_entry.get(), partyPos))
    submit_entry_button.pack()

    back_button = ttk.Button(frm, text="Back", command=lambda: partySummaryWindow(root, frm, user_id, party_id, party, pokeName))
    back_button.pack()

def insert_into_party(root, frm, user_id, party_id, party, pokeName, partyPos):
    try:
        pypokedex.get(name=pokeName.lower())
    except pypokedex.exceptions.PyPokedexError:
        messagebox.showinfo("Error", "Failed to add Pokemon. Pokemon does not exist")
        return
    column_name = f"pokemon{partyPos+1}"
    print(column_name)
    try:
        query = f"UPDATE parties SET {column_name} = ? WHERE user_id = ? AND party_id = ?"
        c.execute(query, (pokeName, user_id, party_id))
        db.commit()
        messagebox.showinfo("Success", "Pokemon added to party successfully!")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        party = c.execute(
            "SELECT * FROM parties WHERE user_id = ? AND party_id = ?", [user_id, party_id]
        )
        party = c.fetchall()
        print(party)
        partySummaryWindow(root, frm, user_id, party_id, party[0][2:], pokeName) 
# There is a pause when the party summary is reloaded. And it doesn't load the deletion until after backing out to the parties screen and back
# into partySummaryWindow
def remove_from_party(root, frm, user_id, party_id, party, pokeName, index):
    column_name = f"pokemon{index+1}"
    try:
        query = f"UPDATE parties SET {column_name} = NULL WHERE user_id = ? AND party_id = ?"
        c.execute(query, (user_id, party_id))
        db.commit()
        messagebox.showinfo("Success", "Pokemon removed from party successfully!")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        party = c.execute(
            "SELECT * FROM parties WHERE user_id = ? AND party_id = ?", [user_id, party_id]
        )
        party = c.fetchall()
        partySummaryWindow(root, frm, user_id, party_id, party[0][2:], pokeName) 

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
    if not username or not password or not passwordConfirmation:
        messagebox.showerror("Registration Failed", "All fields are required.")
        return
    
    if password != passwordConfirmation:
        messagebox.showerror("Registration Failed", "Passwords do not match.")
        return

    if len(password) < 8:
        messagebox.showerror("Registration Failed", "Password must be at least 8 characters long.")
        return
    
    hashed_password = hash_password(password)

    try:
        c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_password))
        db.commit()
        frm.destroy()
        frm = ttk.Frame(root, padding=10)
        frm.pack()
        tk.Label(frm, text="Registered!").pack()
        tk.Button(frm, text="Login", command=lambda: loginWindow(frm)).pack()
    # Check if username exists in database, if not, enter user into database
    except sqlite3.IntegrityError:
        messagebox.showerror("Registration Failed", "Username already exists.")
        registerWindow(root, frm)


    

def summaryWindow(search, root, frm, user_id):
    http = urllib3.PoolManager()
    root.title("Summary: " + search.title())
    frm.destroy()
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    frm.grid_columnconfigure(0, weight=1)
    frm.grid_rowconfigure(0, weight=1)
    frm.focus()

    try:
        pokemon = pypokedex.get(name=search)
    except pypokedex.exceptions.PyPokedexError:
        messagebox.showerror("Error", f"{search} is not a valid Pokémon name.")
        return
    dexId = str(pokemon.dex)
    pokeName = pokemon.name.title()
    url = pokemon.sprites.front['default']
    stats = pokemon.base_stats
    response = requests.get(url)
    temp = PIL.Image.open(BytesIO(response.content))
    sprite = ImageTk.PhotoImage(temp)
    height = int(pokemon.height)
    weight = int(pokemon.weight)

    types = ', '.join([t.title() for t in pokemon.types])
    abilities = ', '.join([a[0].title() for a in pokemon.abilities])


    # Logic to make sure previous and next buttons wrap round to the last or first entry when reaching the start or end of the pokedex
    if pokemon.dex < 1025:
        next_pokemon = pypokedex.get(dex=pokemon.dex+1)
    else:
        next_pokemon = pypokedex.get(dex=1)
    
    if pokemon.dex > 1: 
        prev_pokemon = pypokedex.get(dex=pokemon.dex-1)
    else:
        prev_pokemon = pypokedex.get(dex=1025)

    # Creating widgets - I used ChatGPT for this so the layout is created using a loop, which is more concise than laying each element out 
    # individually
    labels = [
        ("Pokedex ID: ", dexId),
        ("Name: ", pokeName),
        ("Type: ", types),
        ("Ability: ", abilities),
        ("Height: ", str(height/10) + " m"),
        ("Weight: ", str(weight/10) + " kg"),
        ("", ""),
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
    blankLabel2 = tk.Label(frm, text="")
    blankLabel3 = tk.Label(frm, text="")
    blankLabel.grid(column=0, row=len(labels) + 1, pady=10)

    next_button = ttk.Button(frm, text="Next", command=lambda: summaryWindow(next_pokemon.name, root, frm, user_id))
    prev_button = ttk.Button(frm, text="Prev", command=lambda: summaryWindow(prev_pokemon.name, root, frm, user_id))
    search_label = ttk.Label(frm, text="Search for a Pokemon: ", font=('', 15))
    pokeSearch = tk.StringVar()
    searchBox = ttk.Entry(frm, textvariable=pokeSearch, font=('', 15))
    searchButton = ttk.Button(frm, text="Search", command=lambda: clear_window(root, frm, pokeSearch.get(), user_id))
    partiesButton = ttk.Button(frm, text="Parties", command=lambda: partiesWindow(root, frm, user_id, pokeName))

    prev_button.grid(column=0, row=len(labels) + 2, sticky='w', padx=5)
    next_button.grid(column=2, row=len(labels) + 2, sticky='w', padx=5)
    blankLabel2.grid(column=0, row=len(labels) + 3, sticky='w', padx=5, pady=5)
    search_label.grid(column=0, row=len(labels) + 4, sticky='w', padx=5)
    searchBox.grid(column=1, row=len(labels) + 4, sticky='w', padx=5)
    searchButton.grid(column=2, row=len(labels) + 4, sticky='w', padx=5)
    blankLabel3.grid(column=0, row=len(labels) + 5, sticky='w', padx=5, pady=5)
    partiesButton.grid(column=0, row=len(labels) + 6, sticky='w', pady=10)

    logoutButton = ttk.Button(frm, text='Log Out', command=lambda: loginWindow(frm))
    logoutButton.grid(column=0, row=len(labels) + 7, sticky='w', pady=10)

    root.mainloop()

root = Tk()
root.geometry("850x750")
frm = ttk.Frame(root, padding=10)
loginWindow(frm)