
import requests
import urllib3
import pypokedex
import django
import pokepy
import kivy.graphics
import sys
import faulthandler

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
    def __init__(self, search):
        self.pokemon = pypokedex.get(name=search)
        self.dexId = str(self.pokemon.dex)
        self.img = self.pokemon.sprites.front['default']
        self.name = self.pokemon.name.title()
        if len(self.pokemon.types) > 1:
            self.types = str(self.pokemon.types[0]).title() + ', ' + str(self.pokemon.types[1]).title()
        else:
            self.types = str(self.pokemon.types[0]).title()

    def on_enter(self):
        return pokeFetch(self.ids.input.text)

class pokeFetchApp(App):
    def build(self):
        return pokeFetch('bulbasaur')



main()