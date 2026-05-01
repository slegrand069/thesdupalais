from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen

from database import create_table
from ui.main_screen import MainScreen
from ui.detail_screen import DetailScreen
from ui.edit_screen import EditScreen


class WindowManager(ScreenManager):
    pass


class TeaApp(MDApp):
    def build(self):
        from kivy.uix.screenmanager import ScreenManager
        from ui.main_screen import MainScreen
        from ui.detail_screen import DetailScreen
        from ui.edit_screen import EditScreen
        from database import create_table

        create_table()

        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"  # ou "Dark"

        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(DetailScreen(name="detail"))
        sm.add_widget(EditScreen(name="edit"))

        return sm

if __name__ == "__main__":
    TeaApp().run()