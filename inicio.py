import flet as ft

class PageInicio(ft.UserControl):
    def __init__(self, page, on_logout, show_register_employees_page, show_employees_page, show_settings_page):
        super().__init__()
        self.page = page
        self.on_logout = on_logout
        self.show_register_employees_page = show_register_employees_page
        self.show_employees_page = show_employees_page
        self.show_settings_page = show_settings_page

    def build(self):
        return ft.Column(
            controls=[
                # Texto de boas-vindas centralizado
                ft.Text("Bem Vindo!", style="headlineMedium", text_align="center", width=self.page.window.width),

                # Container 1 - Alinhado à esquerda
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Jogue no Tigrinho!", style="titleMedium"),
                            ft.Row(
                                controls=[
                                    ft.Image(src="images/tigrinho.png", width=35, height=35),
                                    ft.ElevatedButton("Jogue Agora!", on_click=self.on_jogar_click),
                                ],
                                spacing=30,
                            ),
                        ],
                        #alignment=ft.MainAxisAlignment.CENTER,
                        #horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=20,
                    bgcolor=ft.colors.AMBER_100,
                    #border_radius=10,
                    #alignment=ft.alignment.center_left,
                    width=self.page.window.width,  # Metade da largura da tela
                    margin=ft.Margin(0, 0, 0, 0),
                ),

                # Container 2 - Alinhado à direita (inteiro)
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Funcionários", style="titleMedium"),
                            ft.Text("Confira já os funcionários!", style="bodyMedium"),
                            ft.Column(
                                controls=[
                                    ft.ElevatedButton("Lista de Funcionários", width=self.page.window.width / 2, on_click=self.show_employees_page),
                                    ft.ElevatedButton("Cadastre um novo", width=self.page.window.width / 2, on_click=self.show_register_employees_page),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                        ],
                    ),
                    padding=20,
                    bgcolor=ft.colors.LIGHT_BLUE_100,
                    #border_radius=10,
                    alignment=ft.alignment.center_right,  # Alinha o Container inteiro à direita
                    width=self.page.window.width,  # Metade da largura da tela
                    margin=ft.Margin(0, 0, 0, 0),
                ),

                # Container 3 - Ocupa a largura inteira
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Configurações", style="titleMedium"),
                            ft.Text("Configure o seu perfil de usuário!", style="bodyMedium"),
                            ft.ElevatedButton("Configurações", on_click=self.show_settings_page),
                        ],
                        #alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    padding=20,
                    bgcolor=ft.colors.GREEN_100,
                    #border_radius=10,
                    #alignment=ft.alignment.center,
                    width=self.page.window.width,
                    margin=ft.Margin(0, 0, 0, 0),
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
            spacing=15
        )

    def on_jogar_click(self, e):
        pass  # Substitua por sua lógica

    def on_logout_click(self, e):
        pass  # Chama a função para voltar à página de login
