from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class ScreenNote(Screen):
    """
    Clase ScreenNote que hereda de Screen.
    
    Esta clase define el comportamiento y los elementos visuales de la pantalla de la nota-

    Métodos:
        __init__(name, **kwargs): Constructor de la clase ScreenNote.
        main_menu(instance): Gestiona el comportamiento del botón que lleva de regreso al menú principal.
        defLayout(): Define la disposición de los elementos en la pantalla.
    """
    def __init__(self, name, actual, **kwargs):
        """
        Constructor de la clase ScreenNote.

        Args:
            name (str): Nombre de la pantalla de notas. Recogido desde donde se haya creado.
        """
        super(ScreenNote, self).__init__(**kwargs)
        self.name = name
                
        self.actual = actual
        # Nombre de la nota prefijado
        self.defLayout()

    def main_menu(self, instance):
        """
        Método que gestiona el comportamiento del botón que lleva de regreso al menú principal.

        Args:
            instance: Botón "Volver al menú principal" que ha sido pulsado.
        """
        sm = App.get_running_app().root
        sm.current = "Menu"

    def next_note(self, instance):
        """
        Método que gestiona la logica de ir a la siguiente nota

        Args:
            instance: Botón de siguiente Nota pulsado
        """
        # Creamos una nota aniadiendola con un incremento
        next = self.actual + 1
        
        if (next > 0):            
            split_string = self.name.split("-")
            next_name_screen = split_string[0]+"-"+str(next)
        else:
            next_name_screen = self.name+"-"+str(next)
            print(f"Split: {next_name_screen}")
            
        sm = App.get_running_app().root

        # Comprobamos que exista esa pantalla
        screen_note = None
        # Buscamos si existe para creear una nueva pantalla o no
        for screen in sm.screens:
            if screen.name == next_name_screen:
                screen_note = screen
        # No existe
        if screen_note is None:
            # Aniadimos una nueva pantalla
            new_screen = ScreenNote(name=next_name_screen, actual=next)
            sm.add_widget(new_screen)
            sm.current = next_name_screen
        else:
            # Existe, saltamos
            sm.current = next_name_screen
       
    def previous_note(self, instance):
        # Creamos una nota aniadiendola con un incremento
        previous = self.actual - 1
        print(f"Previous {previous}")
        if (previous > 0):
            split_string = self.name.split("-")
            previous_name_screen = split_string[0]+"-"+str(previous)
            print(f"Previous name: {previous_name_screen}")
        else:
            split_string = self.name.split("-")
            previous_name_screen = split_string[0]
            print(f"Split: {previous_name_screen}")
        

        # Obtenemos el screenmanager de la raiz
        sm = App.get_running_app().root

        # Buscamos la pantalla anterior y saltamos a ella
        for screen in sm.screens:
            if screen.name == previous_name_screen:
                sm.current = previous_name_screen

    def defLayout(self):
        """
        Método que define la disposición de los elementos en la pantalla de la nota actual.
        """
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

        # Next page
        next_page = Button(text=f'NextPage')
        next_page.bind(on_release=self.next_note)

        # Previous page
        if (self.actual != 0):  
            button_previous= Button(text=f'PreviousNote')
            button_previous.bind(on_release=self.previous_note)
            bottom_layout.add_widget(button_previous)
        # Salir de la nota
        bottom_layout.add_widget(back_button)
        # Ir a la siguiente nota
        bottom_layout.add_widget(next_page)
        # Agregar los layouts al layout principal
        layout.add_widget(top_layout)
        layout.add_widget(middle_layout)
        layout.add_widget(bottom_layout)
        # Aniadirlo a la ventana
        self.add_widget(layout)
