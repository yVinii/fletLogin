import flet as ft
import pyrebase

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


class LoginPage(ft.UserControl):
    def __init__(self, page, on_login_success, on_forgot_password, on_register):
        super().__init__()
        self.page = page
        self.on_login_success = on_login_success  # Função para trocar a página após login
        self.on_forgot_password = on_forgot_password  # Função para abrir esqueceu senha
        self.on_register = on_register  # Função para ir para a página de registro
        self.email_field = ft.TextField(label="Email")  # Campo de email
        self.senha_field = ft.TextField(label="Senha", password=True, can_reveal_password=True)  # Campo de senha

    def build(self):
        # Função chamada ao clicar no botão de login
        def on_login_click(e):
            email = self.email_field.value  # Pega o email digitado
            senha = self.senha_field.value  # Pega a senha digitada

            # retirar dps
            #email = 'silveirafabrini@gmail.com'
            #senha = '123mudar'
            try:
                # Tenta fazer login com email e senha
                auth.sign_in_with_email_and_password(email, senha)
                self.on_login_success(email)  # Se funcionar, troca para a página inicial
            except:
                # Se der erro, mostra uma mensagem de erro
                self.senha_field.value = ""
                self.senha_field.update()
                self.show_message("Email ou senha inválidos!")

        return ft.Column(
            controls=[
                ft.Text("Tela de Login", style="headlineMedium", text_align="center"),  # Título
                self.email_field,  # Campo de email
                self.senha_field,  # Campo de senha
                ft.ElevatedButton("Entrar", on_click=on_login_click),  # Botão de login
                ft.TextButton("Esqueceu sua senha?", on_click=self.on_forgot_password),  # Botão de esqueceu senha
                ft.TextButton("Registre-se", on_click=self.on_register)  # Novo botão para registro
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Centraliza os campos na tela
            horizontal_alignment=ft.CrossAxisAlignment.CENTER  # Centraliza horizontalmente
        )

    def show_message(self, message):
        # Método para mostrar a mensagem de erro
        snack_bar = ft.SnackBar(ft.Text(message))  # Cria a snack_bar com a mensagem
        self.page.add(snack_bar)  # Adiciona a snack_bar à página
        snack_bar.open = True  # Define a snack_bar como aberta
        self.page.update()  # Atualiza a página