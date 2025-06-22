from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.recycleview import RecycleView
from kivy.properties import StringProperty, ListProperty, BooleanProperty
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from auth import register, login
from database import init_db, add_category, add_brand, add_product, get_categories, get_brands, get_products
import os

class SelectableLabel(Label):
    selected = BooleanProperty(False)

class LoginScreen(Screen):
    def handle_login(self, email, password):
        success, message = login(email, password)
        popup = Popup(
            title='Resultado',
            content=Label(text=message, font_name="Roboto", font_size='14sp', color=(1, 1, 1, 1)),
            size_hint=(0.5, 0.5),
            background_color=(0.18, 0.18, 0.18, 1)
        )
        popup.open()
        if success:
            self.manager.get_screen('main').current_user = email
            self.manager.current = 'main'

class RegisterScreen(Screen):
    def handle_register(self, username, email, password):
        success, message = register(username, email, password)
        popup = Popup(
            title='Resultado',
            content=Label(text=message, font_name="Roboto", font_size='14sp', color=(1, 1, 1, 1)),
            size_hint=(0.5, 0.5),
            background_color=(0.18, 0.18, 0.18, 1)
        )
        popup.open()
        if success:
            self.manager.current = 'login'

class MainScreen(Screen):
    current_user = StringProperty('')

class CategoryScreen(Screen):
    def add_category(self, name):
        if name:
            add_category(name)
            self.ids.category_name.text = ''
            self.update_category_list()
            popup = Popup(
                title='Éxito',
                content=Label(text='Categoría agregada', font_name="Roboto", font_size='14sp', color=(1, 1, 1, 1)),
                size_hint=(0.5, 0.5),
                background_color=(0.18, 0.18, 0.18, 1)
            )
            popup.open()

    def update_category_list(self):
        self.ids.category_list.data = [{'text': f"{cat_id}: {name}"} for cat_id, name in get_categories()]

class BrandScreen(Screen):
    def add_brand(self, name):
        if name:
            add_brand(name)
            self.ids.brand_name.text = ''
            self.update_brand_list()
            popup = Popup(
                title='Éxito',
                content=Label(text='Marca agregada', font_name="Roboto", font_size='14sp', color=(1, 1, 1, 1)),
                size_hint=(0.5, 0.5),
                background_color=(0.18, 0.18, 0.18, 1)
            )
            popup.open()

    def update_brand_list(self):
        self.ids.brand_list.data = [{'text': f"{brand_id}: {name}"} for brand_id, name in get_brands()]

class ProductScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.photo_path = ''
        self.selected_index = -1

    def get_category_names(self):
        return [f"{cat_id}: {name}" for cat_id, name in get_categories()]

    def get_brand_names(self):
        return [f"{brand_id}: {name}" for brand_id, name in get_brands()]

    def select_photo(self):
        popup = Popup(
            title='Seleccionar Foto',
            size_hint=(0.8, 0.8),
            background_color=(0.18, 0.18, 0.18, 1)
        )
        file_chooser = FileChooserListView(filters=['*.png', '*.jpg', '*.jpeg'])
        file_chooser.bind(on_submit=lambda instance, selection, touch: self.on_file_selected(selection, popup))
        popup.content = file_chooser
        popup.open()

    def on_file_selected(self, selection, popup):
        if selection:
            self.photo_path = selection[0]
            self.ids.photo_label.text = os.path.basename(self.photo_path)
        popup.dismiss()

    def add_product(self, name, category, brand):
        if name and category and brand and self.photo_path:
            category_id = category.split(":")[0]
            brand_id = brand.split(":")[0]
            add_product(name, category_id, brand_id, self.photo_path)
            self.ids.product_name.text = ''
            self.ids.category_choice.text = ''
            self.ids.brand_choice.text = ''
            self.photo_path = ''
            self.ids.photo_label.text = 'No seleccionada'
            self.update_product_list()
            popup = Popup(
                title='Éxito',
                content=Label(text='Producto agregado', font_name="Roboto", font_size='14sp', color=(1, 1, 1, 1)),
                size_hint=(0.5, 0.5),
                background_color=(0.18, 0.18, 0.18, 1)
            )
            popup.open()
        else:
            popup = Popup(
                title='Error',
                content=Label(text='Completa todos los campos', font_name="Roboto", font_size='14sp', color=(1, 1, 1, 1)),
                size_hint=(0.5, 0.5),
                background_color=(0.18, 0.18, 0.18, 1)
            )
            popup.open()

    def update_product_list(self):
        self.ids.product_list.data = [
            {'text': f"{prod_id}: {name} ({cat}, {brand})", 'selected': False}
            for prod_id, name, cat, brand, _ in get_products()
        ]

    def show_product_image(self, rv, index):
        if index >= 0:
            self.selected_index = index
            product = get_products()[index]
            photo_path = product[4]
            self.ids.product_image.source = photo_path if photo_path else ''
            for i, item in enumerate(self.ids.product_list.data):
                item['selected'] = (i == index)
            self.ids.product_list.refresh_from_data()

class TiendaApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(CategoryScreen(name='categories'))
        sm.add_widget(BrandScreen(name='brands'))
        sm.add_widget(ProductScreen(name='products'))
        return sm

if __name__ == '__main__':
    init_db()
    TiendaApp().run()