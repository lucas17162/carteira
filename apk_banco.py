import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

class MeuLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.valor_input = TextInput(hint_text='Digite o valor', multiline=False)
        self.add_widget(self.valor_input)

        self.resultado = Label(text='Aguardando...')
        self.add_widget(self.resultado)

        self.btn_enviar = Button(text='Simular NFC')
        self.btn_enviar.bind(on_press=self.enviar_pagamento)
        self.add_widget(self.btn_enviar)

    def enviar_pagamento(self, instance):
        valor = self.valor_input.text
        try:
            resposta = requests.post("http://192.168.1.186:5001/nfc", json={"valor": valor})
            if resposta.status_code == 200:
                self.resultado.text = f"Resposta: {resposta.json()['mensagem']}"
            else:
                self.resultado.text = "Erro na requisição"
        except Exception as e:
            self.resultado.text = f"Erro: {e}"

class MeuApp(App):
    def build(self):
        return MeuLayout()

if __name__ == "__main__":
    MeuApp().run()
