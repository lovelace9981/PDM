from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.core.window import Window


class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 10
        self.spacing = 10

        # Title
        self.add_widget(Label(text="SavingsApp", size_hint=(1, 0.1), color=(0,1,0,1)))

        # Columns header
        header_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.1))
        header_layout.add_widget(Label(text="Nombre de Obligación"))
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
        self.add_widget(buttons_layout)

    def check_mod_obligation(self, instance, maxobligation, content):
        int_obligation_new = int(self.obligation_mod_input.text)
        int_max_obligation = int(maxobligation)
        if (int_obligation_new <= int_max_obligation and int_obligation_new >= 0):
            instance.text = self.obligation_mod_input.text
            self.popup.dismiss()
        else:
            label = Label(text=f"Incorrecto debe estar entre 0 y {maxobligation}!", color=(1,0,0,1))
            # Comprobamos que exista
            if (label not in content.children):
             content.add_widget(label)
            # print("Incorrecto")

    def mod_obligation(self, instance, nameobligation, maxobligation):
        self.obligation_mod_input = TextInput(multiline=False, text=instance.text)
        content = BoxLayout(orientation="vertical")
        content.add_widget(Label(text="Modificar:"))
        content.add_widget(self.obligation_mod_input)
        btn_obligation = Button(text="Guardar", on_release=lambda x: self.check_mod_obligation(instance, maxobligation, content))
        content.add_widget(btn_obligation)

        self.popup = Popup(title=f"Cambiar {nameobligation}", content=content, size_hint=(0.4, 0.4))
        self.popup.open()

    def show_add_obligation_popup(self, instance):
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
        obligation_name = self.obligation_name_input.text
        obligation_budget = self.obligation_budget_input.text
        label_neg = Label(text=f"Incorrecto!! has puesto un numero negativo", color=(1,0,0,1))
        label_value = Label(text=f"Incorrecto!! no has puesto ningun dato", color=(1,0,0,1))

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
        # Logic to reset available values
        for row_layout in self.scroll_layout.children[:]:  # Recorre todos los BoxLayout en el ScrollView
            if isinstance(row_layout, BoxLayout):  # Verifica si el widget es un BoxLayout
                elements = row_layout.children[::-1] # Recorre todos los botones en el BoxLayout en sentido inverso
                if isinstance(elements[1], Label):
                    value = elements[1].text
                
                if isinstance(elements[2], Button):
                    elements[2].text = value

class SavingsApp(App):
    def build(self):
        self.root = MainLayout()
        self.icon = 'icon/app.png'
        self.title = 'SavingsApp'
        # Window.clearcolor = (1, 1, 1, 1)  # White background
        return self.root


if __name__ == "__main__":
    SavingsApp().run()