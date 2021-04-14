from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import ColorProperty
from kivy.utils import get_random_color

# Window.clearcolor = get_random_color()
Window.clearcolor = [.59765625, .859375, .79296875, 1.]

FG_Color = ColorProperty(list(map(
    lambda x: min(x + 0.5, 1) if max(Window.clearcolor[:-1]) < 0.5 else max(x - 0.5, 0) if max(
        Window.clearcolor[:-1]) > 0.5 else x, Window.clearcolor[:-1])) + [1.0])
BG_Color = ColorProperty(Window.clearcolor)


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
            children[8].text = "Already have account? [color=0000ff]Ok[/color]"
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

            children[6].text = "No Account? [color=0000ff]Ok[/color]"

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
