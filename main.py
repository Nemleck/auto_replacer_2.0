from keys import *
from time import sleep

keys = Keys()
def on_press(event):
    keys.add_key(event)
    
keyboard.on_press(on_press)

sleep(10000)