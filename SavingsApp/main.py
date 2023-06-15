from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.core.window import Window


class MainLayout(BoxLayout):
    """
    Clase MainLayout que hereda de BoxLayout.
    
    Esta clase define el comportamiento y los elementos visuales del diseño principal de la aplicación SavingsApp.

    Métodos:
        __init__(**kwargs): Constructor de la clase MainLayout.
        check_mod_obligation(instance, maxobligation, content): Comprueba y modifica la obligación.
        mod_obligation(instance, nameobligation, maxobligation): Modifica la obligación.
        show_add_obligation_popup(instance): Muestra un popup para añadir una nueva obligación.
        add_obligation(instance, content): Añade una nueva obligación.
        reset_available(instance): Restablece los valores disponibles.
    """
    def __init__(self, **kwargs):
        """
        Constructor de la clase MainLayout. Definimos el espaciado dentro del layout, el scroll, los botones.
        """
        super(MainLayout, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 10
        self.spacing = 10

        # Title
        self.add_widget(Label(text="SavingsApp", size_hint=(1, 0.1), color=(0,1,0,1)))

        # Columns header
        header_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.1))
        header_layout.add_widget(Label(text="Obligación"))
        header_layout.add_widget(Label(text="Presupuesto"))
        header_layout.add_widget(Label(text="Disponible"))
        self.add_widget(header_layout)

        # ScrollView
        scroll_view = ScrollView(size_hint=(1, 0.6), size=(Window.width, Window.height))
        self.scroll_layout = BoxLayout(orientation="vertical", size_hint_y=None)
        self.scroll_layout.bind(minimum_height=self.scroll_layout.setter('height'))
        scroll_view.add_widget(self.scroll_layout)
        self.add_widget(scroll_view)

        # Buttons
        buttons_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.2))
        buttons_layout.add_widget(Button(text="Añadir Obligación", on_release=self.show_add_obligation_popup))
        buttons_layout.add_widget(Button(text="Reiniciar Disponible", on_release=self.reset_available))
        buttons_layout.add_widget(Button(text="Ver restante", on_release=self.diff_restante))

        self.add_widget(buttons_layout)
    
    def behavior_popup_closebtn(self, instance):
        """
        Método que gestiona el comportamiento del botón "Cerrar" del Popup.

        Args:
            instance: Botón "Cerrar" que ha sido pulsado.
        """
        self.popup.dismiss()
        self.popup = None

    def diff_restante(self, instance):
        """
        Método que restablece los valores de las obligaciones.

        Args:
            instance: Botón "Reiniciar Disponible" que ha sido pulsado.
        """
        # Logic to reset available values
        restante = 0
        for row_layout in self.scroll_layout.children[:]:  # Recorre todos los BoxLayout en el ScrollView
            if isinstance(row_layout, BoxLayout):  # Verifica si el widget es un BoxLayout
                elements = row_layout.children[::-1] # Recorre todos los botones en el BoxLayout en sentido inverso
                
                if isinstance(elements[2], Button):
                    value_button = elements[2].text  
                
                restante += int(value_button)

        # Popup De mostrar restante
        content = BoxLayout(orientation="vertical")
        content.add_widget(Label(text=f"Te quedan:{restante} $"))
        btn_exit = Button(text="Salir", on_release=self.behavior_popup_closebtn)
        content.add_widget(btn_exit)

        self.popup = Popup(title="Ahorro conseguido.", content=content, size_hint=(0.4, 0.4))
        self.popup.open()


    def check_mod_obligation(self, instance, maxobligation, content):
        """
        Método que comprueba y modifica la obligación.

        Args:
            instance: Obligación que está siendo modificada, es el botón.
            maxobligation: Máxima obligación permitida, usado para que al modificar, no sobrepase el valor introducido.
            content: Contenido del widget padre, para quie podamos modificar el PopUp y añadir un Label de error.
        """
        try:
            int_obligation_new = int(self.obligation_mod_input.text)
            int_max_obligation = int(maxobligation)
            if (int_obligation_new <= int_max_obligation and int_obligation_new >= 0):
                instance.text = self.obligation_mod_input.text
                self.popup.dismiss()
            else:
                label = Label(text=f"Debe estar entre 0 y {maxobligation}!", color=(1,0,0,1))
                # Comprobamos que exista
                if (label not in content.children):
                    content.add_widget(label)
                    # print("Incorrecto")
        except ValueError:
            # Comprobamos que exista
            if (label not in content.children):
                content.add_widget(label)

    def mod_obligation(self, instance, nameobligation, maxobligation):
        """
        Método que modifica la obligación. Cuando pulsamos Cambiar llamamos al método check_mod_obligation para comprobar que los valores sean correctos.

        Args:
            instance: Obligación que está siendo modificada.
            nameobligation: Nombre de la obligación.
            maxobligation: Máxima obligación permitida.
        """

        label_value = Label(text=f"No has puesto ningun dato", color=(1,0,0,1))

        self.obligation_mod_input = TextInput(multiline=False, text=instance.text)
        content = BoxLayout(orientation="vertical")
        content.add_widget(Label(text="Modificar:"))
        content.add_widget(self.obligation_mod_input)
        btn_obligation = Button(text="Guardar", on_release=lambda x: self.check_mod_obligation(instance, maxobligation, content))
        content.add_widget(btn_obligation)

        self.popup = Popup(title=f"Cambiar {nameobligation}", content=content, size_hint=(0.4, 0.4))
        self.popup.open()

    def show_add_obligation_popup(self, instance):
        """
        Método que añade una nueva obligación. Cuando se pulsa en Guardar, se llama a add_obligation, para hacer la comprobación de la lógica.

        Args:
            instance: Botón "Guardar" que ha sido pulsado.
            content: Contenido del widget padre.
        """
        self.obligation_name_input = TextInput(multiline=False)
        self.obligation_budget_input = TextInput(multiline=False)

        content = BoxLayout(orientation="vertical")
        content.add_widget(Label(text="Nombre:"))
        content.add_widget(self.obligation_name_input)
        content.add_widget(Label(text="Presupuesto:"))
        content.add_widget(self.obligation_budget_input)
        btn_obligation = Button(text="Guardar", on_release=lambda x: self.add_obligation(instance, content))
        content.add_widget(btn_obligation)

        self.popup = Popup(title="Añadir Obligación", content=content, size_hint=(0.4, 0.4))
        self.popup.open()

    def add_obligation(self, instance, content):
        """
        Método que restablece los valores disponibles d

        Args:
            instance: Botón "Reiniciar Disponible" que ha sido pulsado.
        """
        obligation_name = self.obligation_name_input.text
        obligation_budget = self.obligation_budget_input.text
        label_neg = Label(text=f"Has puesto un numero negativo", color=(1,0,0,1))
        label_value = Label(text=f"No has puesto ningun dato", color=(1,0,0,1))

        # Control de errores en blanco
        try:
            int_obligation_budget = int(obligation_budget)
            if (int_obligation_budget > 0):
                row_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=50)
                row_layout.add_widget(Label(text=obligation_name))
                row_layout.add_widget(Label(text=obligation_budget))
                btn_obligation = Button(text=obligation_budget)
                btn_obligation.bind(on_release=lambda x: self.mod_obligation(btn_obligation, obligation_name, obligation_budget))
                row_layout.add_widget(btn_obligation)
                self.scroll_layout.add_widget(row_layout)
                self.popup.dismiss()
            else:
                # Comprobamos que exista
                if (label not in content.children):
                    content.add_widget(label)
        except ValueError:
            # Comprobamos que exista
            if (label not in content.children):
                content.add_widget(label)


    def reset_available(self, instance):
        """
        Método que restablece los valores de las obligaciones.

        Args:
            instance: Botón "Reiniciar Disponible" que ha sido pulsado.
        """
        # Logic to reset available values
        for row_layout in self.scroll_layout.children[:]:  # Recorre todos los BoxLayout en el ScrollView
            if isinstance(row_layout, BoxLayout):  # Verifica si el widget es un BoxLayout
                elements = row_layout.children[::-1] # Recorre todos los botones en el BoxLayout en sentido inverso
                if isinstance(elements[1], Label):
                    value = elements[1].text
                
                if isinstance(elements[2], Button):
                    elements[2].text = value

class SavingsApp(App):
    """
    Clase SavingsApp que hereda de la clase App de Kivy.
    
    Esta es la clase principal de la aplicación SavingsApp. Define el layout principal 
    de la aplicación, el icono y el título de la ventana.

    Métodos:
        build(): Método heredado de la clase App de Kivy que construye la aplicación.
    """
    def build(self):
        """
        Método que constructor de la aplicación.
        
        Returns:
            MainLayout: Layout principal de la aplicación.
        """
        self.root = MainLayout()
        self.icon = 'icon/app.png'
        self.title = 'SavingsApp'
        return self.root


if __name__ == "__main__":
    SavingsApp().run()