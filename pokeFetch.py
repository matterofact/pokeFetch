
import requests
import cs50
import sys
import random
import PIL.ImageQt, PIL.Image
import urllib3

from kivy.app import App
from kivy.uix.widget import Widget
from io import BytesIO


def main():

    if __name__ == '__main__':
        pokeFetchApp().run()

class pokeFetchfunc(Widget):
    pass

class pokeFetchApp(App):
    def build(self):
        return pokeFetchfunc()

    #http = urllib3.PoolManager()
    #response = requests.get(bulba)
    #image = PIL.Image.open(BytesIO(response))
    #img = PIL.Image.Image(image)





main()