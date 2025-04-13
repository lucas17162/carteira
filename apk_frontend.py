from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
import requests

class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=10, **kwargs)
        
        self.valor_input = TextInput(hint_text='Digite o valor', multiline=False)
        self.add_widget(self.valor_input)
        
        self.nfc_button = Button(text='Pagar com NFC')
        self.nfc_button.bind(on_press=self.enviar_pagamento)
        self.add_widget(self.nfc_button)
        
        self.extrato_button = Button(text='Ver Extrato')
        self.extrato_button.bind(on_press=self.ver_extrato)
        self.add_widget(self.extrato_button)
        
        self.status_label = Label(text='')
        self.add_widget(self.status_label)
    
    def enviar_pagamento(self, instance):
        valor = self.valor_input.text
        if valor:
            try:
                resposta = requests.post('http://SEU_SERVIDOR:5001/pagar', json={'valor': valor})
                if resposta.status_code == 200:
                    self.status_label.text = 'Pagamento enviado!'
                else:
                    self.status_label.text = 'Erro no pagamento.'
            except Exception as e:
                self.status_label.text = f'Erro: {e}'
    
    def ver_extrato(self, instance):
        try:
            resposta = requests.get('http://SEU_SERVIDOR:5001/extrato')
            if resposta.status_code == 200:
                self.status_label.text = resposta.text
            else:
                self.status_label.text = 'Erro ao buscar extrato.'
        except Exception as e:
            self.status_label.text = f'Erro: {e}'

class NFCApp(App):
    def build(self):
        return MainScreen()

if __name__ == '__main__':
    NFCApp().run()
