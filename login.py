from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import ColorProperty
from kivy.utils import get_random_color

Window.clearcolor = get_random_color()

FG_Color = ColorProperty(list(map(
    lambda x: min(x + 0.5, 1) if max(Window.clearcolor[:-1]) < 0.5 else max(x - 0.5, 0) if max(
        Window.clearcolor[:-1]) > 0.5 else x, Window.clearcolor[:-1])) + [1.0])
BG_Color = ColorProperty(Window.clearcolor)


class SignUpScreen(Screen):
    fgcolor = FG_Color
    bgcolor = BG_Color


class LoginScreen(Screen):
    fgcolor = FG_Color
    bgcolor = BG_Color


screen = ""


class LoginApp(App):
    def build(self):
        global screen
        screen = ScreenManager()
        screen.add_widget(LoginScreen(name = "LoginScreen"))
        screen.add_widget(SignUpScreen(name = "SignUpScreen"))
        return screen


if __name__ == "__main__":
    LoginApp().run()
