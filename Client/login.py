import re
import time

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import ColorProperty
from kivy.utils import get_random_color

Window.clearcolor = get_random_color()
from Client.client import Client

FG_Color = ColorProperty(list(map(
    lambda x: min(x + 0.5, 1) if max(Window.clearcolor[:-1]) < 0.5 else max(x - 0.5, 0) if max(
        Window.clearcolor[:-1]) > 0.5 else x, Window.clearcolor[:-1])) + [1.0])
BG_Color = ColorProperty(Window.clearcolor)

network = Client()


class MainScreen(Screen):
    fgcolor = FG_Color
    bgcolor = BG_Color

    def refresh(self, dt):
        try:
            if self.parent.current == "MainScreen":
                network.messages = network.get('messages', {"token": network.token})['data']['messages']
                children = self.children[0].children[::-1]
                text = ''
                for _, user, message in network.messages:
                    text += user+': '
                    text += f'\n{" "*(len(user)+6)}'.join(re.findall('.{1,25}', message, flags=re.S))
                    text += '\n'
                children[0].text = text
        except:
            pass

    def send(self):
        children = self.children[0].children[::-1]
        text = children[1].text
        network.post('new-message', {"token": network.token, "message": text})
        children[1].text = ""


class SignUpScreen(Screen):
    fgcolor = FG_Color
    bgcolor = BG_Color

    def sign_up(self):
        children = self.children[0].children[::-1]
        username_input = children[2].text
        password_input = children[4].text
        cpassword_input = children[6].text

        if not username_input or not password_input or not cpassword_input:
            children[8].text = "Already have account? [color=0000ff]You should fill all the details[/color]"
        elif password_input == cpassword_input:
            cred = {
                "username": username_input,
                "password": password_input
            }
            recv_data = network.post('signup', cred)
            if recv_data.status_code == 200:
                network.token = recv_data.json()["data"]["token"]
                self.parent.current = "MainScreen"
            elif recv_data.status_code == 401:
                children[8].text = f"Already have account? [color=0000ff]{recv_data.json()['message']}[/color]"
        else:
            children[8].text = "Already have account? [color=0000ff]Passwords dont match[/color]"


class LoginScreen(Screen):
    fgcolor = FG_Color
    bgcolor = BG_Color

    def login(self):
        children = self.children[0].children[::-1]
        username_input = children[2].text
        password_input = children[4].text

        if not username_input or not password_input:
            children[6].text = "No Account? [color=0000ff]You should fill all the details[/color]"
        else:
            cred = {
                "username": username_input,
                "password": password_input
            }
            recv_data = network.post('login', cred)
            if recv_data.status_code == 200:
                network.token = recv_data.json()["data"]["token"]
                self.parent.current = "MainScreen"
            elif recv_data.status_code == 401:
                children[6].text = f"No Account? [color=0000ff]{recv_data.json()['message']}[/color]"


screen = ""


class LoginApp(App):
    def build(self):
        global screen
        screen = ScreenManager()
        screen.add_widget(LoginScreen(name = "LoginScreen"))
        screen.add_widget(SignUpScreen(name = "SignUpScreen"))
        main = MainScreen(name = "MainScreen")
        screen.add_widget(main)
        Clock.schedule_interval(main.refresh, 0.10)
        return screen


if __name__ == "__main__":
    LoginApp().run()
