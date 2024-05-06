
import requests
import urllib3
import pypokedex
import django
import pokepy
import kivy.graphics
import sys

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from io import BytesIO


def main():
    if __name__ == '__main__':
        pokeFetchApp().run()

    
class pokeFetch(Widget):
    search = 'bulbasaur'
    pokemon = pypokedex.get(name=str(search))
    dexId = str(pokemon.dex)
    img = pokemon.sprites.front['default']
    name = pokemon.name.title()
    if len(pokemon.types) > 1:
        types = str(pokemon.types[0]).title() + ', ' + str(pokemon.types[1]).title()
    else:
        types = str(pokemon.types[0]).title()

    def on_enter(self):
        search = self.ids.input.text
        return pokeFetch()


class pokeFetchApp(App):
    def build(self):
        return pokeFetch()



main()