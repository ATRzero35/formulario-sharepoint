from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.network.urlrequest import UrlRequest
import json

class FormApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Campo de Nome
        self.nome = TextInput(hint_text="Seu Nome", size_hint=(1, 0.1))
        
        # Caixa de Seleção (OPCAO1 ou OPCAO2)
        self.spinner = Spinner(
            text="Selecione a Operação",
            values=("OPCAO1", "OPCAO2"),
            size_hint=(1, 0.1)
        )
        
        # Botão de Enviar
        btn_enviar = Button(text="Enviar", size_hint=(1, 0.1))
        btn_enviar.bind(on_press=self.enviar_dados)
        
        # Label para resultado
        self.resultado = Label(text="", size_hint=(1, 0.2))
        
        layout.add_widget(Label(text="Formulário SharePoint", font_size=20))
        layout.add_widget(self.nome)
        layout.add_widget(self.spinner)
        layout.add_widget(btn_enviar)
        layout.add_widget(self.resultado)
        
        return layout
    
    def enviar_dados(self, instance):
        dados = {
            "nome": self.nome.text,
            "operacao": self.spinner.text
        }
        
        UrlRequest(
            "https://formulario-api-hyc8.onrender.com",  # Substitua pela URL da API hospedada
            on_success=self.sucesso,
            on_failure=self.erro,
            req_body=json.dumps(dados),
            req_headers={"Content-Type": "application/json"}
        )
    
    def sucesso(self, req, result):
        self.resultado.text = f"ID Gerado: {result['id_unico']}"
    
    def erro(self, req, error):
        self.resultado.text = f"Erro: {error}"

if __name__ == "__main__":
    FormApp().run()