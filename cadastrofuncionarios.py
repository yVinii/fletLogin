import flet as ft
import firebase_admin
from firebase_admin import credentials, firestore

class CadastraFuncionariosPage(ft.UserControl):
    def __init__(self, page, on_logout, credential):
        super().__init__()
        self.page = page
        self.on_logout = on_logout  # Função para voltar para o login
        self.cred = credential
        self.db = firestore.client()

        # Campos de entrada
        self.nome_input = ft.TextField(label="Nome")
        self.salario_input = ft.TextField(label="Salário", keyboard_type=ft.KeyboardType.NUMBER)
        self.cargo_input = ft.Dropdown(
            label="Cargo",
            options=[
                ft.dropdown.Option("Chefe"),
                ft.dropdown.Option("Desenvolvedor"),
                ft.dropdown.Option("Analista"),
                # Adicione outras opções conforme necessário
            ],
        )
        
        # Botão de cadastro
        self.cadastrar_button = ft.ElevatedButton(
            "Cadastrar",
            on_click=self.cadastrar_funcionario,
            width=self.page.window.width / 2
        )

    def build(self):
        return ft.Column(
            controls=[
                ft.Row(
                    controls=[ft.Text("Cadastro Funcionários", style="headlineMedium", text_align="center")],  # Adiciona o botão em uma linha
                    alignment=ft.MainAxisAlignment.CENTER  # Centraliza o botão
                ),
                self.nome_input,
                self.salario_input,
                self.cargo_input,
                ft.Row(
                    controls=[self.cadastrar_button],  # Adiciona o botão em uma linha
                    alignment=ft.MainAxisAlignment.CENTER  # Centraliza o botão
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )

    def cadastrar_funcionario(self, e):
        nome = self.nome_input.value
        salario = self.salario_input.value
        cargo = self.cargo_input.value

        # Validações
        if not nome or len(nome) < 3:
            self.page.snack_bar = ft.SnackBar(ft.Text("O nome deve ter pelo menos 3 letras."))
            self.nome_input.value = " "
            self.nome_input.update()
            self.page.snack_bar.open = True
            self.page.update()
            return

        if not salario or not salario.isdigit() or not (1500 <= float(salario) <= 25000):
            self.page.snack_bar = ft.SnackBar(ft.Text("O salário deve ser um número entre 1500 e 25000."))
            self.salario_input.value = " "
            self.salario_input.update()
            self.page.snack_bar.open = True
            self.page.update()
            return

        if not cargo:
            self.page.snack_bar = ft.SnackBar(ft.Text("Você deve selecionar um cargo."))
            self.page.snack_bar.open = True
            self.page.update()
            return

        # Adiciona funcionário à coleção no Firestore
        self.db.collection("funcionarios").add({
            "nome": nome,
            "salario": float(salario),
            "cargo": cargo,
            "data_inclusao": firestore.SERVER_TIMESTAMP  # O timestamp será definido automaticamente
        })

        # Limpa os campos após o cadastro
        self.nome_input.value = ""
        self.salario_input.value = ""
        self.cargo_input.value = ""
        
        self.nome_input.update()
        self.salario_input.update()
        self.cargo_input.update()

        # Mensagem de sucesso
        self.page.snack_bar = ft.SnackBar(ft.Text("Funcionário cadastrado com sucesso!"))
        self.page.snack_bar.open = True
        self.page.update()  # Atualiza a página para refletir as mudanças