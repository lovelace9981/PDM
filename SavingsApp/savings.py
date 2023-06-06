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

    def show_add_obligation_popup(self, instance):
        self.obligation_name_input = TextInput(multiline=False)
        self.obligation_budget_input = TextInput(multiline=False)

        content = BoxLayout(orientation="vertical")
        content.add_widget(Label(text="Nombre de la Obligación:"))
        content.add_widget(self.obligation_name_input)
        content.add_widget(Label(text="Presupuesto de la Obligación:"))
        content.add_widget(self.obligation_budget_input)
        content.add_widget(Button(text="Guardar", on_release=self.add_obligation))

        self.popup = Popup(title="Añadir Obligación", content=content, size_hint=(0.4, 0.4))
        self.popup.open()

    def add_obligation(self, instance):
        obligation_name = self.obligation_name_input.text
        obligation_budget = self.obligation_budget_input.text

        row_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=50)
        row_layout.add_widget(Label(text=obligation_name))
        row_layout.add_widget(Label(text=obligation_budget))
        row_layout.add_widget(Button(text=obligation_budget))
        self.scroll_layout.add_widget(row_layout)

        self.popup.dismiss()

    def reset_available(self, instance):
        # Logic to reset available values
        pass


class SavingsApp(App):
    def build(self):
        self.root = MainLayout()
        # Window.clearcolor = (1, 1, 1, 1)  # White background
        return self.root


if __name__ == "__main__":
    SavingsApp().run()