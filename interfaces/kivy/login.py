from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class LoginScreen(GridLayout):
    def __init__(self):
        GridLayout.__init__(self)
        self.cols = 2
        self.add_widget(Label(text='user name'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text='password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)
        self.add_widget(Button(text='submit', on_press=self.submit))

    def submit(self, instance):
        print(self.username.text, self.password.text)

class LoginApp(App):
    def build(self):
        return LoginScreen()

LoginApp().run()
