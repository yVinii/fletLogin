import flet as ft
import threading
import pyrebase
import re  # Para validação de email

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

class RegistrarPage(ft.UserControl):
    def __init__(self, page, on_return_login):
        super().__init__()
        self.page = page
        self.on_return_login = on_return_login  # Função para voltar para o login
        self.email_field = ft.TextField(label="Email")  # Campo para inserir o email
        self.password_field = ft.TextField(label="Senha", password=True, can_reveal_password=True)  # Campo para inserir a senha

    def build(self):
        # Função chamada ao clicar no botão de registro
        def on_register(e):
            email = self.email_field.value  # Pega o email digitado
            password = self.password_field.value  # Pega a senha digitada
            
            # Validação de email e senha
            if not self.validate_email(email):
                self.show_message("Email inválido!")
                return
            
            if len(password) < 6:
                self.show_message("A senha deve ter pelo menos 6 caracteres!")
                self.password_field.value = ""
                self.password_field.update()
                return

            try:
                # Tenta criar um novo usuário
                auth.create_user_with_email_and_password(email, password)
                self.email_field.value = ""  # Limpa o campo de email
                self.password_field.value = ""  # Limpa o campo de senha
                self.show_message("Registro realizado com sucesso!")
                self.email_field.update()
                self.password_field.update()
                # Usa um Timer para voltar para a página de login após 2 segundos
                threading.Timer(2, self.on_return_login).start()
                self.page.update()  # Atualiza a página
            except Exception as ex:
                # Mostra mensagem de erro se o registro falhar
                self.show_message("Erro! Não foi possível registrar o usuário.")

        return ft.Column(
            controls=[
                ft.Text("Registrar", style="headlineMedium", text_align="center"),  # Título
                self.email_field,  # Campo para inserir o email
                self.password_field,  # Campo para inserir a senha
                ft.ElevatedButton("Registrar", on_click=on_register),  # Botão para registrar
                ft.TextButton("Voltar para o Login", on_click=self.on_return_login)  # Botão para voltar ao login
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Centraliza tudo na tela
            horizontal_alignment=ft.CrossAxisAlignment.CENTER  # Centraliza horizontalmente
        )

    def validate_email(self, email):
        # Valida se o email tem um formato correto
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None

    def show_message(self, message):
        # Mostra uma mensagem para o usuário (como erro ou sucesso)
        snack_bar = ft.SnackBar(ft.Text(message))
        self.page.add(snack_bar)
        snack_bar.open = True  # Define open como True para mostrar o snack_bar
        self.page.update()  # Atualiza a página
