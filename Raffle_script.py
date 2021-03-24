#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

# main.py

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase
from ln_database import LNDataBase
from kivy.uix.button import Button
import random
from kivy.animation import Animation
from kivy.clock import Clock


class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.namee.text)

                self.reset()

                sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""


class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            MainWindow.current = self.email.text
            self.reset()
            sm.current = "main"
        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""


class MainWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ""
    lucky_num = ObjectProperty(None)

    def submit_number(self):
        user_input = self.lucky_num.text
        if user_input != "":
            ln_db.add_number(user_input)

            self.reset()
            sm.current = "payment"
        else:
            invalidNumber()

    def reset(self):
        self.lucky_num.text = ""

    def logOut(self):
        sm.current = "login"

class NumberDisplayed(Screen):
    pass

class FirstPage(Screen):
    fp_label = ObjectProperty(None)
    fp_button = ObjectProperty(None)

    # The def on_enter() allows the app to call the clock and the random function without
    # requiring any action from the user (for instance a click).

    def on_enter(self, *args):
        Clock.schedule_interval(self.animate_button, 2)
        value = str(random.randint(1, 1000))
        self.ids.fp_button.text = value

    def animate_button(self, *args):
        widget = self.ids.fp_button
        anim = Animation(animated_color=(1,6,1,0.3), blink_size=250)
        anim.bind(on_complete=self.reset)
        anim.start(widget)


    def reset(self, *args):
        widget = args[1]
        widget.animated_color = (1,6,1,0.3)

# I had to change the widget.blink_size from 1 to 0.1 because the white circle was not going transparent.

        widget.blink_size = 0.1

    def press(self):
        value = str(random.randint(1,1000))
        self.ids.fp_button.text = value

    def submit_randomnumber(self):
        if self.ids.fp_button.text != "":
            ln_db.add_number(self.ids.fp_button.text)

            sm.current = "first"
        else:
            invalidNumber()

    def logOut(self):
        sm.current = "first"


class PaymentMethod(Screen):
    pass


class WindowManager(ScreenManager):
    pass

class ThankYou(Screen):
    pass

def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username or password.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()

def invalidNumber():
    pop = Popup(title='Invalid Number',
                  content=Label(text='Please fill in all inputs with a number from 1 to 1000.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()


kv = Builder.load_file("my.kv")

sm = WindowManager()
db = DataBase("users.txt")
ln_db = LNDataBase("lucky_number.txt")

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"), MainWindow(name="main"), NumberDisplayed(name="number"), FirstPage(name="first"), PaymentMethod(name="payment"), ThankYou(name="thankyou")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "create"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()