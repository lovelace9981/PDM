import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.behaviors import TouchRippleBehavior

from ScreenNote import ScreenNote

kivy.require('1.11.1')

# Establecer color de fondo
Window.clearcolor = (0.96, 0.96, 0.96, 1) # Color de fondo Material Design

# Clase de comportamiento de crear un boton de Notas
class NoteButton(TouchRippleBehavior, Button):
    """
    Clase NoteButton que hereda de TouchRippleBehavior y Button.
    
    Esta clase define el comportamiento y los elementos visuales de los botones de notas. Esto es debido a que el boton del menú de las notas, 
    tiene un comportamiento según la duración de la pulsación.

    Métodos:
        __init__(**kwargs): Constructor de la clase NoteButton.
        behavior_popup_closebtn(instance): Gestiona el comportamiento del botón "Cerrar" del Popup.
        behavior_popup_deletebtn(instance): Gestiona el comportamiento del botón "Borrar" del Popup.
        on_touch_down(touch): Define el comportamiento al pulsar el botón.
        on_touch_up(touch): Define el comportamiento al soltar el botón.
    """
    def __init__(self, **kwargs):
        """
        Constructor de la clase NoteButton.

        Args:
            **kwargs: Argumentos variables que se pasan al constructor de las clases padre.
        """
        super(NoteButton, self).__init__(**kwargs)
        self.current_popup = None
        self.touch_time = 0

    def behavior_popup_closebtn(self, instance):
        """
        Método que gestiona el comportamiento del botón "Cerrar" del Popup.

        Args:
            instance: Botón "Cerrar" que ha sido pulsado.
        """
        self.current_popup.dismiss()
        self.current_popup = None

    def behavior_popup_deletebtn(self, instance):
        """
        Método que gestiona el comportamiento del botón "Borrar" del Popup.

        Args:
            instance: Botón "Borrar" que ha sido pulsado.
        """
        self.current_popup.dismiss()
        self.current_popup = None

        self.parent.remove_widget(self)
    
    def on_touch_down(self, touch):
        """
        Método que define el comportamiento al pulsar el botón. Es el que pone el tiempo inicial de pulsación, 
        para que cuando el usuario deje de pulsar el botoón se pueda llamar a on_touch_up.

        Args:
            touch: Información sobre el evento de toque.
        """
        if self.collide_point(*touch.pos):
            self.touch_time = Clock.get_time()
        return super(NoteButton, self).on_touch_down(touch)
   
    # Popup de eliminar nota O abrir la nota si es un toque
    def on_touch_up(self, touch):
        """
        Método que define el comportamiento al soltar el botón. Depende de on_touch_down, de manera que podemos determinar la
        duración de la pulsación para que se introduzca en el nuevo ScreeNote o salte un PopUp para que se elimine la nota.

        Args:
            touch: Información sobre el evento de toque.
        """
        if touch.grab_current is self:
            # Calculamos el tiempo del toque, si el tiempo de toque es encima de 0.5 creamos un PopUp de borrado de notas.
            ripple_duration = Clock.get_time() - self.touch_time
            # print(ripple_duration)
            if ripple_duration > 0.5:
                # Control de la cantidad de popups
                if self.current_popup is None:
                    # Head and middle
                    layout = BoxLayout(orientation='vertical')
                    
                    # Bottom
                    bottomBoxLayout = BoxLayout(orientation='horizontal')
                    deletebtn = Button(text='Delete Note', size_hint_y=None, height=40)
                    closebtn = Button(text='Exit', size_hint_y=None, height=40)
                    bottomBoxLayout.add_widget(deletebtn)
                    bottomBoxLayout.add_widget(closebtn)
                    layout.add_widget(bottomBoxLayout)

                    # POPUP de introducion de texto
                    self.current_popup = Popup(
                        title='Delete note? '+ self.text,
                        content=layout,
                        size_hint=(0.3,0.3)
                        # size=(200,200)
                    )

                    closebtn.bind(on_release=self.behavior_popup_closebtn)
                    deletebtn.bind(on_release=self.behavior_popup_deletebtn)
                    self.current_popup.open()
            else:
                # Obtenemos el screenmanager de la raiz
                sm = App.get_running_app().root

                # Comprobamos que exista esa pantalla
                screen_note = None
                # Buscamos si existe para creear una nueva pantalla o no
                for screen in sm.screens:
                    if screen.name == self.text:
                        screen_note = screen
                # No existe
                if screen_note is None:
                    # Aniadimos una nueva pantalla
                    new_screen = ScreenNote(name=self.text)
                    sm.add_widget(new_screen)
                    sm.current = self.text
                else:
                    # Existe, saltamos
                    sm.current = self.text

        return super(NoteButton, self).on_touch_up(touch)

# Clase main Menu
class MainMenu(Screen):
    """
    Clase MainMenu que hereda de Screen. Esto es debido a que es una pantalla que es el menú principal.
    Esta clase define el comportamiento y los elementos visuales de la pantalla del menú principal de la aplicación.

    Métodos:
        behavior_btn_create_note_popup(layout, popupfather, check_text, grid_notes): Gestiona el comportamiento del botón "Crear nota" del Popup.
        behavior_btn_close_note_popup(popupfather): Gestiona el comportamiento del botón "Cerrar" del Popup.
        create_note_buton_on_release(grid): Define el comportamiento al pulsar el botón "Nueva Nota".
        delete_note_buton_on_release(instance): Define el comportamiento al pulsar el botón "Borrar".
        __init__(**kwargs): Constructor de la clase MainMenu.
    """
    def behavior_btn_create_note_popup(self, layout, popupfather, check_text, grid_notes):
        """
        Método que define el comportamiento del botón "Crear nota" del Popup.

        Args:
            layout (BoxLayout): Layout que contiene los elementos del Popup.
            popupfather (Popup): Popup que contiene el botón "Crear nota".
            check_text (TextInput): Campo de texto donde se introduce el título de la nota.
            grid_notes (GridLayout): Layout donde se colocan las notas creadas.
        """
        if len(check_text.text) == 0 and self.error_label != 1: 
            self.error_label = 1
            # Mensaje emergente
            label = Label(text="[color=#C70039]No ha introducido ningun dato", markup=True)
            layout.add_widget(label)

        else:
            self.error_label = 0
            # Creamos el boton con la entrada de texto anterior finalizada
            btn = NoteButton(text=check_text.text, size_hint_y=None, height=40)
            # btn.bind(on_touch)
            grid_notes.add_widget(btn)
            popupfather.dismiss()
    
    def behavior_btn_close_note_popup(self, popupfather):
        """
        Método que define el comportamiento del botón "Cerrar" del Popup.

        Args:
            popupfather (Popup): Popup que contiene el botón "Cerrar".
        """
        popupfather.dismiss()


    def create_note_buton_on_release(self, grid):
        """
        Método que define el comportamiento al pulsar el botón "Nueva Nota".

        Args:
            grid (GridLayout): Layout donde se colocarán las nuevas notas creadas.
        """
        self.error_label = 0
        # Head and middle
        layout = BoxLayout(orientation='vertical')
        notetitle = TextInput(multiline=False)
        
        # Bottom
        bottomBoxLayout = BoxLayout(orientation='horizontal')
        createbtn = Button(text='Crear', size_hint_y=None, height=40)
        closebtn = Button(text='Salir', size_hint_y=None, height=40)
        bottomBoxLayout.add_widget(createbtn)
        bottomBoxLayout.add_widget(closebtn)

        layout.add_widget(notetitle)
        layout.add_widget(bottomBoxLayout)

        # POPUP de introducion de texto
        popup = Popup(
            title="Creando nueva nota",
            content=layout,
            size_hint=(0.3,0.3)
            # size=(200,200)
        )

        createbtn.bind(on_release=lambda x: self.behavior_btn_create_note_popup(layout, popup, notetitle, grid))
        closebtn.bind(on_release=lambda x: self.behavior_btn_close_note_popup(popup))
        popup.open()

    def __init__(self, **kwargs):
        """
        Constructor de la clase MainMenu.

        Args:
            **kwargs: Argumentos variables que se pasan al constructor de la clase padre.
        """
        super(MainMenu, self).__init__(**kwargs)
        self.baselayout = BoxLayout()
        self.baselayout.orientation = 'vertical'

        # CABECERA
        title_box = BoxLayout(size_hint_y=0.1) 
        title_label = Label(text='[color=000000]NoteApp[/color]', markup=True, font_size='20sp')
        title_box.add_widget(title_label)

        ## ANADIMOS AL Menu la caja del titulo
        self.baselayout.add_widget(title_box)

        # Crear un ScrollView, para hacer el scroll
        scroll_view = ScrollView()

        # Crear un GridLayout
        grid_notes = GridLayout(cols=1, spacing=0.1, size_hint_y=None)
        grid_notes.bind(minimum_height=grid_notes.setter('height'))

        # Añadir GridLayout a ScrollView
        scroll_view.add_widget(grid_notes)

        self.baselayout.add_widget(scroll_view)

        # BoxLayout para los botones Crear y Borrar
        box_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1)

        # Botones Crear y Borrar
        create_button = Button(text='Nueva Nota', size_hint_y=None, height=40)
        # delete_button = Button(text='Borrar', size_hint_y=None, height=40)

        # EMBEDD Actions
        create_button.bind(on_release=lambda x: self.create_note_buton_on_release(grid_notes))
        box_layout.add_widget(create_button)
        # self.box_layout.add_widget(delete_button)

        self.baselayout.add_widget(box_layout)

        # Lo aniadimos al screen
        self.add_widget(self.baselayout)


class NoteApp(App):
    """
    La clase NoteApp es la clase principal donde se lanza la app NoteApp
    Atributos:
        icon (string): Este atributo es utilizado para indicarle a la clase padre que es un icono
        title (string): Atributo de titulo
        sm (ScreenManager): Atributo que es un objeto de ScreenManager para gestionar la pantalla

    Métodos:
        build: Este metodo es utilizado para crear la aplicacion, tiene un funcionamiento similar a un constructor
    """
    def build(self):
        """
        Metodo utilizado para crear la aplicacion, se usa como constructor creando en la App padre un ScreenManager, que 
        es necesario para gestionar los cambios de pantalla entre las distintas aplicaciones.
        """
        # Atributo de clase de icono de app
        self.icon = 'icon/app.png'
        # Atributo de clase de titulo de app
        self.title = 'NoteApp'

        # Atributo de clase de Gestor de Pantallas
        self.sm = ScreenManager() 
        # Creacion de una pantalla
        screen = MainMenu(name="Menu")

        self.sm.add_widget(screen)
        self.sm.current = "Menu"
        return self.sm

if __name__ == '__main__':
    NoteApp().run()