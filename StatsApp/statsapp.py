from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window

import statistics
import math 

class RoundedButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        # BACKGROUND
        self.background_color = rgb_to_kivy_color(255,87,51)
        # TEXT COLOR
        self.color = (0,0,0,1)

    def on_draw(self):
        with self.canvas.before:
            Color(rgb_to_kivy_color(165,214,167))  # establece el color a rojo
            RoundedRectangle(pos=self.pos, size=self.size, radius=[60,])

def rgb_to_kivy_color(r,g,b):
    return r / 255., g / 255., b / 255., 1

class StatApp(App):
    def build(self):
        self.icon = 'icon/app.png'
        self.title = 'StatCalc'
        # Estadisticos
        self.stat_data = [0]
        main_layout = BoxLayout(orientation="vertical", size_hint=(1,1))

        self.title_label = Label(text="StatCalc Unidimensional", size_hint=(1,0.1), color=(0,0,0,1))
        main_layout.add_widget(self.title_label)

        self.scroll_layout = BoxLayout(orientation="vertical", size_hint_y=None)
        self.scroll_layout.bind(minimum_height=self.scroll_layout.setter('height'))
        
        self.text_input = TextInput(text="0", multiline=False, size_hint_y=None, height=30, halign="center")
        self.scroll_layout.add_widget(self.text_input)

        scroll_view = ScrollView(size_hint=(1, 0.8))
        scroll_view.add_widget(self.scroll_layout)
        main_layout.add_widget(scroll_view)

        button_layout = BoxLayout(size_hint=(1,0.1), spacing=5)
        

        # self.new_stat_button = Button(text="Nuevo")
        self.new_stat_button = RoundedButton(text="Nuevo")
        self.new_stat_button.bind(on_release=self.add_stat_input)
        button_layout.add_widget(self.new_stat_button)

        # self.calc_button = Button(text="Calcular")
        self.calc_button = RoundedButton(text="Calcular")
        self.calc_button.bind(on_release=self.calculate)
        button_layout.add_widget(self.calc_button)

        # self.show_quantil = Button(text="Cuantiles")
        self.show_quantil = RoundedButton(text="Cuantiles")
        self.show_quantil.bind(on_release=self.quantil)
        button_layout.add_widget(self.show_quantil)

        # self.show_decil = Button(text="Deciles")
        self.show_decil = RoundedButton(text="Deciles")
        self.show_decil.bind(on_release=self.decil)
        button_layout.add_widget(self.show_decil)

        main_layout.add_widget(button_layout)

        Window.clearcolor = rgb_to_kivy_color(218,247,166)

        return main_layout

    def quantil(self, instance):
        self.stat_data = [float(text_input.text) for text_input in self.scroll_layout.children[::-1]]
        list_quantil = statistics.quantiles(self.stat_data, n=4, method='exclusive')
        popup_layout_base = BoxLayout(orientation='vertical')
        popup_layout = GridLayout(cols=3)
        n_q = 0
        for q in list_quantil:
            popup_layout.add_widget(Label(text=f"Cuantil {n_q+1}"))
            n_q+=1

        for q in list_quantil:
            popup_layout.add_widget(Label(text=f"{q}"))
        popup_layout_base.add_widget(popup_layout)
        popup_layout_base.add_widget(Button(text="OK", on_release=lambda x: popup.dismiss()))
        popup = Popup(title="Cuantiles", content=popup_layout_base, size_hint=(None, None), size=(400, 200))
        popup.title_align = 'center'

        popup.open()
    
    def decil(self, instance):
        self.stat_data = [float(text_input.text) for text_input in self.scroll_layout.children[::-1]]
        list_quantil = statistics.quantiles(self.stat_data, n=10, method='exclusive')
        popup_layout_base = BoxLayout(orientation='vertical')
        popup_layout = GridLayout(cols=9)
        
        n_q = 0
        for q in list_quantil:
            popup_layout.add_widget(Label(text=f"{n_q+1}"))
            n_q+=1

        for q in list_quantil:
            popup_layout.add_widget(Label(text=f"{q}"))
        popup_layout_base.add_widget(popup_layout)
        popup_layout_base.add_widget(Button(text="OK", on_release=lambda x: popup.dismiss()))
        popup = Popup(title="Deciles", content=popup_layout_base, size_hint=(0.9, 0.5))
        popup.title_align = 'center'
        popup.open()

    def add_stat_input(self, instance):
        new_text_input = TextInput(text="0", multiline=False, size_hint_y=None, height=30, halign="center")
        self.scroll_layout.add_widget(new_text_input)
        # Aniadimos los datos estadisticos
        self.stat_data.append(0)

    def calculate(self, instance):
        # Recorremos de nuevo los datos para obtenerlos de manera actualizada
        self.stat_data = [float(text_input.text) for text_input in self.scroll_layout.children[::-1]]
        # Calculo de la media
        mean = sum(self.stat_data) / len(self.stat_data)
        # calculo de la mediana
        median = statistics.median(self.stat_data)
        # obtencion de la moda
        mode = statistics.mode(self.stat_data)
        # Obtencion de la varianza
        varianza = statistics.variance(self.stat_data)
        # Obtencion de la desviacion tipica
        desv_tipica = math.sqrt(varianza)
        # devs_tipica_python = statistics.stdev(self.stat_data)
        # IQR
        list_quantil = statistics.quantiles(self.stat_data, n=4, method='exclusive')
        iqr = list_quantil[2] - list_quantil[0]

        popup_layout = BoxLayout(orientation="vertical")
        popup_layout.add_widget(Label(text=f"Media: {mean}"))
        popup_layout.add_widget(Label(text=f"Mediana: {median}"))
        popup_layout.add_widget(Label(text=f"Moda: {mode}"))
        popup_layout.add_widget(Label(text=f"Varianza: {varianza}"))
        popup_layout.add_widget(Label(text=f"Desviacion tipica: {desv_tipica}"))
        popup_layout.add_widget(Label(text=f"IQR: {iqr}"))
        # popup_layout.add_widget(Label(text=f"Desviacion tipica - 2: {devs_tipica_python}"))

        popup_layout.add_widget(Button(text="OK", on_release=lambda x: popup.dismiss()))
        popup = Popup(title="Resultados", content=popup_layout, size_hint=(None, None), size=(400, 400))
        popup.title_align = 'center'

        popup.open()


if __name__ == "__main__":
    StatApp().run()