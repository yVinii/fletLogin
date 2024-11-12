import flet as ft

class FuncionariosPage(ft.UserControl):
    def __init__(self, page, db, show_employees_page):
        super().__init__()
        self.page = page  # Guarda a página principal para exibir a lista
        self.db = db  # Banco de dados Firebase
        self.funcionarios_data = []  # Variável para armazenar a lista de funcionários
        self.show_employees_page = show_employees_page

    def carregar_funcionarios(self):
        # Consulta no Firestore para obter todos os funcionários
        funcionarios_ref = self.db.collection("funcionarios")
        docs = funcionarios_ref.stream()

        # Armazena os dados dos funcionários em uma lista
        self.funcionarios_data = []  # Limpa a lista antes de adicionar os dados
        for doc in docs:
            data = doc.to_dict()
            self.funcionarios_data.append({
                "id": doc.id,  # Armazenamos o ID do funcionário
                "nome": data.get("nome", "N/A"),
                "salario": data.get("salario", "N/A"),
                "cargo": data.get("cargo", "N/A"),
            })

    def build(self):
        # Carregar a lista de funcionários
        self.carregar_funcionarios()

        def on_click_editar_cargo(funcionario_cargo, funcionario_nome, funcionario_id):

            cargo_field = ft.Dropdown(value=str(funcionario_cargo), label="Cargo", 
                options=[
                    ft.dropdown.Option("Chefe"),
                    ft.dropdown.Option("Desenvolvedor"),
                    ft.dropdown.Option("Analista"),
                    # Adicione outras opções conforme necessário
                ])
            # Criar o Dialog (janela pop-up) com o título, sem conteúdo e com dois botões
            dialog = ft.AlertDialog(
                title=ft.Text(f"Edite o cargo de {funcionario_nome}", size=16),  # Título com o nome do funcionário
                content=cargo_field,
                actions=[
                    # O primeiro botão é para fechar o Dialog
                    ft.TextButton("Fechar", on_click=lambda e: fechar_dialog(dialog)),  # Fecha o diálogo quando clicado

                    # O segundo botão é para excluir o funcionário do banco de dados
                    ft.TextButton("Confirmar", on_click=lambda e: confirmar_edicao_cargo(funcionario_id, cargo_field.value, dialog, cargo_field))  # Chama a função para excluir e depois fecha o dialog
                ]
            )

            # Torna o dialog visível
            dialog.open = True

            # Exibe o diálogo na página
            self.page.dialog = dialog  # Atribui o dialog à página
            self.page.update()  # Atualiza a página para mostrar o dialog
        
        def confirmar_edicao_cargo(funcionario_id, novo_cargo, dialog, cargo_field):
            try:
                # Verifica se o salário está dentro do intervalo permitido
                if not novo_cargo:
                    self.page.snack_bar = ft.SnackBar(ft.Text("Erro: Você deve selecionar um cargo!"))
                    self.page.snack_bar.open = True
                    self.page.update()
                    return  # Interrompe a função para impedir a atualização

                # Atualiza o salário no banco de dados
                self.db.collection("funcionarios").document(funcionario_id).update({"cargo": novo_cargo})

                # Fecha o diálogo e mostra uma mensagem de sucesso
                dialog.open = False
                self.page.snack_bar = ft.SnackBar(ft.Text("Funcionário editado com sucesso!"))
                self.page.snack_bar.open = True

                # Recarrega a lista de funcionários atualizada
                self.show_employees_page(e=None)

            except ValueError:
                # Mensagem de erro caso o salário não seja um número válido
                self.page.snack_bar = ft.SnackBar(ft.Text("Erro: Cargo inválido!"))
                self.page.snack_bar.open = True
                self.page.update()


        def on_click_editar_salario(funcionario_salario, funcionario_nome, funcionario_id):

            salario_field = ft.TextField(value=str(funcionario_salario), label="Salário")
            # Criar o Dialog (janela pop-up) com o título, sem conteúdo e com dois botões
            dialog = ft.AlertDialog(
                title=ft.Text(f"Edite o salário de {funcionario_nome}", size=16),  # Título com o nome do funcionário
                content=salario_field,
                actions=[
                    # O primeiro botão é para fechar o Dialog
                    ft.TextButton("Fechar", on_click=lambda e: fechar_dialog(dialog)),  # Fecha o diálogo quando clicado

                    # O segundo botão é para excluir o funcionário do banco de dados
                    ft.TextButton("Confirmar", on_click=lambda e: confirmar_edicao_salario(funcionario_id, salario_field.value, dialog, salario_field))  # Chama a função para excluir e depois fecha o dialog
                ]
            )

            # Torna o dialog visível
            dialog.open = True

            # Exibe o diálogo na página
            self.page.dialog = dialog  # Atribui o dialog à página
            self.page.update()  # Atualiza a página para mostrar o dialog
        
        def confirmar_edicao_salario(funcionario_id, novo_salario, dialog, salario_field):
            try:
                novo_salario_float = float(novo_salario)
                
                # Verifica se o salário está dentro do intervalo permitido
                if novo_salario_float <= 1500 or novo_salario_float >= 25000:
                    self.page.snack_bar = ft.SnackBar(ft.Text("Erro: O salário deve estar entre 1500 e 25000!"))
                    self.page.snack_bar.open = True
                    self.page.update()
                    return  # Interrompe a função para impedir a atualização

                # Atualiza o salário no banco de dados
                self.db.collection("funcionarios").document(funcionario_id).update({"salario": novo_salario_float})

                # Fecha o diálogo e mostra uma mensagem de sucesso
                dialog.open = False
                self.page.snack_bar = ft.SnackBar(ft.Text("Funcionário editado com sucesso!"))
                self.page.snack_bar.open = True

                # Recarrega a lista de funcionários atualizada
                self.show_employees_page(e=None)

            except ValueError:
                # Mensagem de erro caso o salário não seja um número válido
                self.page.snack_bar = ft.SnackBar(ft.Text("Erro: Salário inválido! Insira um número."))
                self.page.snack_bar.open = True
                self.page.update()


        # Função para lidar com o clique e abrir o Dialog
        def on_click_deletar(funcionario_nome, funcionario_id):
            # Criar o Dialog (janela pop-up) com o título, sem conteúdo e com dois botões
            dialog = ft.AlertDialog(
                title=ft.Text(f"Deseja Excluir {funcionario_nome} ?", size=16),  # Título com o nome do funcionário
                actions=[
                    # O primeiro botão é para fechar o Dialog
                    ft.TextButton("Cancelar", on_click=lambda e: fechar_dialog(dialog)),  # Fecha o diálogo quando clicado

                    # O segundo botão é para excluir o funcionário do banco de dados
                    ft.TextButton("Excluir", on_click=lambda e: excluir_funcionario(funcionario_id, dialog))  # Chama a função para excluir e depois fecha o dialog
                ]
            )

            # Torna o dialog visível
            dialog.open = True

            # Exibe o diálogo na página
            self.page.dialog = dialog  # Atribui o dialog à página
            self.page.update()  # Atualiza a página para mostrar o dialog

        # Função para excluir o funcionário do banco de dados
        def excluir_funcionario(funcionario_id, dialog):
            # Exclui o funcionário do banco de dados usando o ID
            self.db.collection("funcionarios").document(funcionario_id).delete()

            # Remove o funcionário da lista
            self.funcionarios_data = [funcionario for funcionario in self.funcionarios_data if funcionario["id"] != funcionario_id]

            # Fecha o dialog após a exclusão
            dialog.open = False

            # Exibe o SnackBar de sucesso
            self.page.snack_bar = ft.SnackBar(ft.Text("Funcionário excluído com sucesso!"))
            self.page.snack_bar.open = True

            self.show_employees_page(e=None)

        # Função para fechar o dialog
        def fechar_dialog(dialog):
            dialog.open = False
            self.page.update()  # Atualiza a página para refletir o fechamento do dialog

        # Título da página
        titulo = ft.Text("Lista de Funcionários", style="headlineMedium", text_align="center")

        # Define a estrutura da tabela
        tabela = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Nome", weight="bold", width=50)),
                ft.DataColumn(label=ft.Text("Salário", weight="bold", width=70)),
                ft.DataColumn(label=ft.Text("Cargo", weight="bold", width=50)),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        # Envolvendo o nome com GestureDetector para capturar o clique
                        ft.DataCell(
                            ft.GestureDetector(
                                on_tap=lambda e, nome=funcionario["nome"], id=funcionario["id"]: on_click_deletar(nome, id),  # Passando o nome e o ID corretamente
                                content=ft.Text(funcionario["nome"], size=12)
                            )
                        ),
                        ft.DataCell(
                            ft.GestureDetector(
                                on_tap=lambda e, salario=funcionario["salario"], nome=funcionario["nome"], id=funcionario["id"]: on_click_editar_salario(salario, nome, id),  # Passando o nome e o ID corretamente
                                content=ft.Text(f"R$ {funcionario['salario']:.2f}".replace(".", ","), size=12)
                            )
                        ),
                        ft.DataCell(
                            ft.GestureDetector(
                                on_tap=lambda e, cargo=funcionario["cargo"], nome=funcionario["nome"], id=funcionario["id"]: on_click_editar_cargo(cargo, nome, id),  # Passando o nome e o ID corretamente
                                content=ft.Text(funcionario["cargo"], size=12)
                            )
                        ),
                    ]
                ) for funcionario in self.funcionarios_data  # Usando a lista atualizada de funcionários
            ]
        )

        # Retorna o layout final
        return ft.Column(
            controls=[titulo, tabela],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
