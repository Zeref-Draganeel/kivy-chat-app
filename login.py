from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import ColorProperty
from kivy.utils import get_random_color

Window.clearcolor = get_random_color()


class LoginScreen(Widget):
    fgcolor = ColorProperty(list(map(lambda x: min(x+0.5,1) if max(Window.clearcolor[:-1])<0.5 else max(x-0.5,0) if max(Window.clearcolor[:-1])>0.5 else x, Window.clearcolor[:-1]))+[1.0])
    bgcolor = ColorProperty(Window.clearcolor)


class LoginApp(App):
    def build(self):
        return LoginScreen()


if __name__ == "__main__":
    LoginApp().run()
