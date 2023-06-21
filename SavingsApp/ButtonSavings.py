from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup

# RIPPLE para borrado
from kivy.uix.behaviors import TouchRippleBehavior

class ButtonSavings(TouchRippleBehavior, Button):
    """
    Clase ButtonSavings que hereda de TouchRippleBehavior y Button.
    
    Esta clase define el comportamiento y los elementos visuales de los botones de los nombres de los Savings. 
    Esto es debido a que el boton del menú de las notas, 
    tiene un comportamiento según la duración de la pulsación.

    Métodos:
        __init__(**kwargs): Constructor de la clase ButtonSavings.
        behavior_popup_closebtn(instance): Gestiona el comportamiento del botón "Cerrar" del Popup.
        behavior_popup_deletebtn(instance): Gestiona el comportamiento del botón "Borrar" del Popup.
        behavior_popup_editbtn(instance): Gestiona el coomportamiento del bot'on "Editar" del PopUp
        on_touch_down(touch): Define el comportamiento al pulsar el botón.
        on_touch_up(touch): Define el comportamiento al soltar el botón.
    """
    def __init__(self, **kwargs):
        """
        Constructor de la clase NoteButton.

        Args:
            **kwargs: Argumentos variables que se pasan al constructor de las clases padre.
        """
        super(ButtonSavings, self).__init__(**kwargs)
        self.current_popup = None
        self.touch_time = 0

    def behavior_popup_closebtn(self, instance):
        """
        Método que gestiona el comportamiento del botón "Cerrar" del Popup.
        Cierra el popup de manera segura.

        Args:
            instance: Botón "Cerrar" que ha sido pulsado.
        """
        self.current_popup.dismiss()
        self.current_popup = None

    def behavior_popup_editbtn(self, instance, label_new):
        """
        Método que gestiona el comportamiento del botón "Editar" del Popup.
        Guarda el nombre del boton nuevo, en la instancia.

        Args:
            instance: Botón "Borrar" que ha sido pulsado.
        """
        if (label_new.text):
            self.text = label_new.text
            self.current_popup.dismiss()
            self.current_popup = None
    
    def behavior_popup_deletebtn(self, instance):
        """
        Método que gestiona el comportamiento del popup de borrado, elimina la l'inea de la Obligacion

        Args:
            instance: Botón "Borrar" que ha sido pulsado.
        """
        # Comportamiento si borrado obtenemos el padre
        layout_parent = self.parent
        if (isinstance(layout_parent, BoxLayout)):
            self.current_popup.dismiss()
            self.current_popup = None            
            # Borrando elementos hijos del padre, menos a si mismo
            for child in layout_parent.children[:]:
                if (child is not self):
                    layout_parent.remove_widget(child)
            # Se borra el boton a si mismo a continuacion, ya que tiene que seguir ejecutando la logica
            # Esto es porque el abuelo contiene al padre y hay que borrarlo de manera segura.
            layout_parent.remove_widget(self)
            layout_grandparent = layout_parent.parent
            layout_grandparent.remove_widget(layout_parent)
                
    def on_touch_down(self, touch):
        """
        Método que define el comportamiento al pulsar el botón hacia abajo. Es el que pone el tiempo inicial de pulsación, 
        para que cuando el usuario deje de pulsar el botón se pueda llamar a on_touch_up. Llama al metodo heredado con Super. 
        ya que 

        Args:
            touch: Información sobre el evento de toque.
        """

        if self.collide_point(*touch.pos):
            self.touch_time = Clock.get_time()
    
        return super(ButtonSavings, self).on_touch_down(touch)
   
    # Popup de eliminar nota O abrir la nota si es un toque
    def on_touch_up(self, touch):
        """
        Método que define el comportamiento al soltar el botón. Depende de on_touch_down, de manera que podemos determinar la
        duración de la pulsación para que se introduzca el cambio de nommbre de la Obligacion o salte un PopUp para que se elimine la Obligacion.

        Args:
            touch: Información sobre el evento de toque.
        """
        if touch.grab_current is self:
            # Calculamos el tiempo del toque, si el tiempo de toque es encima de 0.5 creamos un PopUp de borrado de notas.
            ripple_duration = Clock.get_time() - self.touch_time
            # print(ripple_duration)
            if ripple_duration < 0.5:
                # Control de la cantidad de popups
                if self.current_popup is None:
                    # Head and middle
                    layout = BoxLayout(orientation='vertical')
                    
                    # Edicion del nombre de la obligacion
                    label_new = TextInput(multiline=False)
                    layout.add_widget(label_new)

                    # Bottom
                    bottomBoxLayout = BoxLayout(orientation='horizontal')
                    editbtn = Button(text='Edit', size_hint_y=None, height=40)
                    closebtn = Button(text='Exit', size_hint_y=None, height=40)
                    bottomBoxLayout.add_widget(editbtn)
                    bottomBoxLayout.add_widget(closebtn)
                    layout.add_widget(bottomBoxLayout)

                    # POPUP de introducion de texto
                    self.current_popup = Popup(
                        title='Edit obligation? '+ self.text,
                        content=layout,
                        size_hint=(0.3,0.3)
                        # size=(200,200)
                    )

                    closebtn.bind(on_release=self.behavior_popup_closebtn)
                    # Pasamos la referencia del nuevo label que le ponemos al boton
                    editbtn.bind(on_release=lambda x:self.behavior_popup_editbtn(editbtn, label_new=label_new))
                    self.current_popup.open()
            else:
                # Control de la cantidad de popups
                if self.current_popup is None:
                    # Head and middle
                    layout = BoxLayout(orientation='vertical')
                    
                    # Bottom
                    bottomBoxLayout = BoxLayout(orientation='horizontal')
                    deletebtn = Button(text='Delete', size_hint_y=None, height=40)
                    closebtn = Button(text='Exit', size_hint_y=None, height=40)
                    bottomBoxLayout.add_widget(deletebtn)
                    bottomBoxLayout.add_widget(closebtn)
                    layout.add_widget(bottomBoxLayout)

                    # POPUP de introducion de texto
                    self.current_popup = Popup(
                        title='Edit obligation? '+ self.text,
                        content=layout,
                        size_hint=(0.3,0.3)
                        # size=(200,200)
                    )

                    deletebtn.bind(on_release=self.behavior_popup_deletebtn)
                    # Pasamos la referencia del nuevo label que le ponemos al boton
                    closebtn.bind(on_release=self.behavior_popup_closebtn)
                    self.current_popup.open()
                    
        return super(ButtonSavings, self).on_touch_up(touch)
