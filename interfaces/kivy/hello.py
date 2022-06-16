# import kivy
# kivy.require('2.1.0')

from kivy.app import App
from kivy.uix.label import Label

class Hello(App):
    def build(self):
        return Label(text='Suck a fish.')

Hello().run()
