
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.clock import mainthread
import json
import os

# Ürünler ve kodları
PRODUCTS_FILE = 'products.json'

def load_products():
    """ Ürünleri JSON dosyasından yükle """
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}

def save_products(products):
    """ Ürünleri JSON dosyasına kaydet """
    with open(PRODUCTS_FILE, 'w', encoding='utf-8') as file:
        json.dump(products, file, ensure_ascii=False, indent=4)

products = load_products()

class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=[20, 20, 40, 30], spacing=10)

        # Sonuç ekranı
        self.result_label = Label(text="Sonuç burada görünecek", size_hint_y=200, height=50)
        layout.add_widget(self.result_label)

        # Klavyeden giriş alanı
        self.input_text = TextInput(hint_text="Aramak için bir kelime girin", size_hint_y=100, height=40)
        layout.add_widget(self.input_text)

        # Klavyeden arama butonu
        keyboard_button = Button(text="Klavyeden Arama Yap", size_hint_y=80, height=40)
        keyboard_button.bind(on_press=self.keyboard_search)
        layout.add_widget(keyboard_button)

        # Yeni ürün ekleme için alanlar
        self.new_product_input = TextInput(hint_text="Yeni ürün adı", size_hint_y=100, height=40)
        layout.add_widget(self.new_product_input)

        self.new_code_input = TextInput(hint_text="Yeni ürün kodu", size_hint_y=100, height=40)
        layout.add_widget(self.new_code_input)

        add_product_button = Button(text="Ürün Ekle", size_hint_y=80, height=40)
        add_product_button.bind(on_press=self.add_new_product)
        layout.add_widget(add_product_button)

        # Alt tarafa boşluk eklemek için widget
        empty_space = Widget(size_hint_y=250, height=150)
        layout.add_widget(empty_space)

        return layout

    def keyboard_search(self, instance):
        # Klavyeden girilen metni al
        query = self.input_text.text.lower()
        print("Arama sonucu:", query)

        # Ürünü arama
        self.search_products(query)

    def search_products(self, query):
        # Sözlükteki ürünleri kontrol et ve eşleşenleri bul
        matches = [f"{product}: {code}" for product, code in products.items() if query in product]
        
        if matches:
            result_text = "\n".join(matches)
        else:
            result_text = "Ürün bulunamadı"

        self.update_result_label(f"Sonuç:\n{result_text}")

    @mainthread
    def update_result_label(self, result):
        # Sonucu ana iş parçacığında güncelle
        self.result_label.text = result

    def add_new_product(self, instance):
        # Yeni ürün ve kodu alın
        new_product = self.new_product_input.text.lower()
        new_code = self.new_code_input.text

        if new_product and new_code:
            # Ürünü products sözlüğüne ekle
            products[new_product] = new_code
            save_products(products)  # Yeni ürünü dosyaya kaydet
            print(f"Yeni ürün eklendi: {new_product} - {new_code}")
            self.update_result_label(f"Yeni ürün eklendi: {new_product} - {new_code}")
        else:
            self.update_result_label("Lütfen ürün adı ve kodunu girin")

if __name__ == "__main__":
    MyApp().run()
