#!/usr/bin/env python3

from pynput import keyboard, mouse

import time

def on_move(x, y):
    print('move', x, y)

def on_click(x, y, button, pressed):
    print('click', x, y, button, pressed)

def on_scroll(x, y, dx, dy):
    print('scroll', x, y, dx, dy)

def on_press(key):
    print('press', key)

def on_release(key):
    print('release', key)

mouse_listener = mouse.Listener(
    on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll,
)
keyboard_listener =  keyboard.Listener(
    on_press=on_press,
    on_release=on_release,
)
mouse_listener.start()
keyboard_listener.start()

while True:
    time.sleep(1)
