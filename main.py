import flet as ft
from login import LoginPage
from esqueceusuasenha import EsqueceuSenhaPage
from inicio import PageInicio  # Importa a nova página inicial
from registrar import RegistrarPage
from menu_bar import MenuBar
from cadastrofuncionarios import CadastraFuncionariosPage
from configuracoes import ConfiguracoesPage
from listafuncionarios import FuncionariosPage
import firebase_admin
from firebase_admin import credentials, firestore
# C:/Users/vinicius.silveira/Documents/firebase/firebaseKey.json

# Inicialize o Firebase apenas uma vez
cred = credentials.Certificate("C:/Users/vinicius.silveira/Documents/firebase/firebaseKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()  # Cria o cliente Firestore uma única vez

class AppState:
    def __init__(self):
        self.email = ""  # Armazena o email do usuário logado

# Instância global de AppState
app_state = AppState()

def main(page: ft.Page):
    # Define as configurações do app para celular
    page.window.width = 390  # Largura típica de um celular
    page.window.height = page.window.height  # Usa altura total da tela
    emailConfig = ""

    # Função para exibir a tela de login
    def show_login_page(e=None):  # Aceita o argumento `e`
        page.controls.clear()
        page.add(LoginPage(page, show_inicio_page, show_forgot_password_page, show_register_page))
        page.update()

    # Função para exibir a tela de "Esqueceu sua senha"
    def show_forgot_password_page(e=None):  # Aceita o argumento `e`
        page.controls.clear()
        page.add(EsqueceuSenhaPage(page, show_login_page))
        page.update()

    def show_register_page(e):
        register_page = RegistrarPage(page, show_login_page)
        page.clean()  # Limpa a página atual
        page.add(register_page)  # Adiciona a nova página
        page.update()  # Atualiza a página

    # Função para exibir a tela inicial após o login
    def show_inicio_page(email, e=None):
        page.controls.clear()
        app_state.email = email
        #page.add(PageInicio(page, show_login_page))  # Adiciona a página inicial
        # Cria a coluna principal que vai conter todo o conteúdo
        main_content = ft.Column(
            controls=[
                PageInicio(page, show_login_page, show_register_employees_page, show_employees_page, show_settings_page),  # Adiciona a página inicial
                ft.Container(expand=True),  # Um contêiner expansível para ocupar o espaço restante
                MenuBar(page, show_inicio_page, show_register_employees_page, show_employees_page, show_settings_page)  # Adiciona a MenuBar
            ],
            alignment=ft.MainAxisAlignment.START,  # Alinha os controles ao topo
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centraliza horizontalmente
            expand=True  # Faz a coluna ocupar todo o espaço disponível
        )

        page.add(main_content)  # Adiciona a coluna principal na página

        page.update()  # Atualiza a página
        

    def show_employees_page(e):
        page.controls.clear()
        
        # Cria a coluna principal que vai conter o conteúdo rolável
        main_content = ft.Column(
            controls=[
                FuncionariosPage(page, db, show_employees_page),  # Adiciona a página inicial
                ft.Container(expand=True)  # Um contêiner expansível para ocupar o espaço restante
            ],
            alignment=ft.MainAxisAlignment.START,  # Alinha os controles ao topo
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centraliza horizontalmente
            expand=True,  # Faz a coluna ocupar todo o espaço disponível
            scroll="auto"  # Habilita o scroll automático para essa coluna
        )
        
        # Adiciona o main_content (conteúdo rolável) e a MenuBar (fixa) ao layout da página
        page.add(
            main_content,  # Adiciona o conteúdo rolável
            MenuBar(page, show_inicio_page, show_register_employees_page, show_employees_page, show_settings_page)  # Adiciona a MenuBar fixa
        )

        page.update()  # Atualiza a página

    def show_register_employees_page(e):
        page.controls.clear()
        # Cria a coluna principal que vai conter todo o conteúdo
        main_content = ft.Column(
            controls=[
                CadastraFuncionariosPage(page, show_login_page, cred),  # Adiciona a página inicial
                ft.Container(expand=True),  # Um contêiner expansível para ocupar o espaço restante
                MenuBar(page, show_inicio_page, show_register_employees_page, show_employees_page, show_settings_page)  # Adiciona a MenuBar
            ],
            alignment=ft.MainAxisAlignment.START,  # Alinha os controles ao topo
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centraliza horizontalmente
            expand=True  # Faz a coluna ocupar todo o espaço disponível
        )

        page.add(main_content)  # Adiciona a coluna principal na página

        page.update()  # Atualiza a página

    def show_settings_page(e):
        page.controls.clear()
        # Cria a coluna principal que vai conter todo o conteúdo
        main_content = ft.Column(
            controls=[
                ConfiguracoesPage(page, show_login_page, app_state.email),  # Adiciona a página inicial
                ft.Container(expand=True),  # Um contêiner expansível para ocupar o espaço restante
                MenuBar(page, show_inicio_page, show_register_employees_page, show_employees_page, show_settings_page)  # Adiciona a MenuBar
            ],
            alignment=ft.MainAxisAlignment.START,  # Alinha os controles ao topo
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centraliza horizontalmente
            expand=True  # Faz a coluna ocupar todo o espaço disponível
        )

        page.add(main_content)  # Adiciona a coluna principal na página

        page.update()  # Atualiza a página

    # Inicia o app com a página de login
    show_login_page()

# Inicia o app com o Flet
ft.app(target=main)
