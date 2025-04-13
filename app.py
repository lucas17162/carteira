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

        self.btn_extrato = Button(text='Ver Extrato')
        self.btn_extrato.bind(on_press=self.ver_extrato)
        self.add_widget(self.btn_extrato)

    def enviar_pagamento(self, instance):
        valor = self.valor_input.text
        try:
            resposta = requests.post("http://192.168.100.15:5001/nfc", json={"valor": valor})
            if resposta.status_code == 200:
                self.resultado.text = f"Resposta: {resposta.json()['mensagem']}"
            else:
                self.resultado.text = "Erro na requisição"
        except Exception as e:
            self.resultado.text = f"Erro: {e}"

    def ver_extrato(self, instance):
        try:
            resposta = requests.get("http://192.168.100.15:5001/extrato")
            if resposta.status_code == 200:
                extrato = resposta.json()['extrato']
                texto = "\n".join([f"R$ {linha}" for linha in extrato])
                self.resultado.text = f"Extrato:\n{texto}"
            else:
                self.resultado.text = "Erro ao buscar extrato"
        except Exception as e:
            self.resultado.text = f"Erro: {e}"


class CarteiraApp(App):
    def build(self):
        return MeuLayout()


if __name__ == "__main__":
    CarteiraApp().run()
