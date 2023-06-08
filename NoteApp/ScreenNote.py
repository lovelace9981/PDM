from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class BackButton(Button):
    def __init__(self, name, **kwargs):
        pass

    def back(self):
        pass


class ScreenNote(Screen):
    def __init__(self, name, **kwargs):
            super(ScreenNote, self).__init__(**kwargs)
            self.name = name
            # Nombre de la nota prefijado
            self.defLayout()

    def main_menu(self, instance):
        sm = App.get_running_app().root
        sm.current = "Menu"


    def defLayout(self):
        layout = BoxLayout(orientation='vertical')
        # Parte superior
        top_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        label = Label(text=self.name, color=(0,0,0,1), height=20)
        top_layout.add_widget(label)

        # Parte central
        middle_layout = GridLayout(cols=1, size_hint=(1, 0.5))
        textbox = TextInput()
        middle_layout.add_widget(textbox)

        # Parte inferior
        bottom_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        back_button = Button(text=f'Salir de {self.name}')
        # Preparamos el boton para volver al menu principal
        back_button.bind(on_release=self.main_menu)

        bottom_layout.add_widget(back_button)

        # Agregar los layouts al layout principal
        layout.add_widget(top_layout)
        layout.add_widget(middle_layout)
        layout.add_widget(bottom_layout)
        # Aniadirlo a la ventana
        self.add_widget(layout)
