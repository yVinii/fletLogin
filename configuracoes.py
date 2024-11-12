import flet as ft
import pyrebase  # Importa a biblioteca do Firebase

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

class ConfiguracoesPage(ft.UserControl):
    def __init__(self, page, on_logout, email):
        super().__init__()
        self.page = page
        self.on_logout = on_logout
        self.email = email

    def build(self):
        return ft.Column(
            controls=[
                ft.Text("Configurações", style="headlineMedium", text_align="center"),
                ft.Text(f"{self.email}", selectable=True, size=20),
                ft.ElevatedButton("Redefinir Senha", on_click=self.open_reset_password_dialog, width=250),
                ft.ElevatedButton("Logout", on_click=self.on_logout, width=250)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=50
        )

    def open_reset_password_dialog(self, e):
        try:
            # Tenta enviar o link de redefinição de senha
            auth.send_password_reset_email(self.email)
            self.show_message("Link de redefinição enviado para seu email!")
            self.page.update()  # Atualiza a página
        except Exception as ex:
            # Mostra mensagem de erro se o email não for válido
            self.show_message("Erro! Verifique o email e tente novamente.")

    def show_message(self, message):
        # Mostra uma mensagem para o usuário (como erro ou sucesso)
        snack_bar = ft.SnackBar(ft.Text(message))
        self.page.add(snack_bar)
        snack_bar.open = True  # Define open como True para mostrar o snack_bar
        self.page.update()  # Atualiza a página