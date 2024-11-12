import flet as ft
import pyrebase  # Importa a biblioteca do Firebase
import threading

firebaseConfig = {
  "apiKey": "AIzaSyCdhRjJHGFeOqe1qgkwBsh2oS-2d5IcLhM",
  "authDomain": "authentication-d1616.firebaseapp.com",
  "projectId": "authentication-d1616",
  "storageBucket": "authentication-d1616.firebasestorage.app",
  "databaseURL": "https://Authentication.firebaseio.com",
  "messagingSenderId": "242629951802",
  "appId": "1:242629951802:web:32d4ad5a9edd6b4d141003",
  "measurementId": "G-80C1773TT9"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

class EsqueceuSenhaPage(ft.UserControl):
    def __init__(self, page, on_return_login):
        super().__init__()
        self.page = page
        self.on_return_login = on_return_login  # Função para voltar para o login
        self.email_field = ft.TextField(label="Email")  # Campo para inserir o email

    def build(self):
        # Função chamada ao clicar no botão de reset
        def on_reset_password(e):
            email = self.email_field.value  # Pega o email digitado
            try:
                # Tenta enviar o link de redefinição de senha
                auth.send_password_reset_email(email)
                self.email_field.value = ""  # Limpa o campo de email
                self.show_message("Link de redefinição enviado para seu email!")
                self.email_field.update()
                 # Usa um Timer para voltar para a página de login após 2 segundos
                threading.Timer(10, self.on_return_login).start()
                self.page.update()  # Atualiza a página
            except Exception as ex:
                # Mostra mensagem de erro se o email não for válido
                self.show_message("Erro! Verifique o email e tente novamente.")

        return ft.Column(
            controls=[
                ft.Text("Redefinir Senha", style="headlineMedium", text_align="center"),  # Título
                self.email_field,  # Campo para inserir o email
                ft.ElevatedButton("Enviar Link de Redefinição", on_click=on_reset_password),  # Botão para enviar o link
                ft.TextButton("Voltar para o Login", on_click=self.on_return_login)  # Botão para voltar ao login
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Centraliza tudo na tela
            horizontal_alignment=ft.CrossAxisAlignment.CENTER  # Centraliza horizontalmente
        )

    def show_message(self, message):
        # Mostra uma mensagem para o usuário (como erro ou sucesso)
        snack_bar = ft.SnackBar(ft.Text(message))
        self.page.add(snack_bar)
        snack_bar.open = True  # Define open como True para mostrar o snack_bar
        self.page.update()  # Atualiza a página
