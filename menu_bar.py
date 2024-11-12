import flet as ft

class MenuBar(ft.UserControl):
    def __init__(self, page, show_home, show_register, show_employees, show_settings):
        super().__init__()
        self.page = page
        self.show_home = show_home  # Função para mostrar a página inicial
        self.show_register = show_register  # Função para mostrar a página de registro
        self.show_employees = show_employees  # Função para mostrar a página de funcionários
        self.show_settings = show_settings  # Função para mostrar a página de configurações

    def build(self):
        # Cria a linha da barra de navegação
        return ft.Row(
            controls=[
                ft.IconButton(ft.icons.HOME, on_click=self.show_home),  # Botão Início
                ft.IconButton(ft.icons.ADD, on_click=self.show_register),  # Botão Cadastro
                ft.IconButton(ft.icons.PERSON, on_click=self.show_employees),  # Botão Funcionários
                ft.IconButton(ft.icons.SETTINGS, on_click=self.show_settings),  # Botão Configurações
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,  # Espaça os botões igualmente
            width=self.page.window.width,  # Faz a linha ocupar toda a largura da tela
            height=60,  # Altura da barra de navegação
        )

    def add_to_bottom(self):
        # Adiciona uma linha de separação e a barra de navegação ao final da página
        self.page.add(ft.Column(
            controls=[
                ft.Divider(),  # Linha divisória acima da barra de navegação
                self.build()
            ],
            alignment=ft.MainAxisAlignment.END,  # Alinha a barra na parte inferior
            expand=True  # Faz a barra ocupar todo o espaço restante
        ))