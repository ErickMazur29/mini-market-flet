import flet as ft
from database.data import get_connection
from views.home_view import Home

class Login:
    def __init__(self, page : ft.Page):
        self.page = page

        self.username = ft.TextField(label="Usuario", color=ft.Colors.BLACK)
        self.password = ft.TextField(label="Senha", password=True, can_reveal_password=True, color=ft.Colors.BLACK)

    def build(self):
        self.page.controls.clear()
        self.page.bgcolor = ft.Colors.WHITE
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        

        login_card = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.LOCK_PERSON_ROUNDED, size=50, color=ft.Colors.BLUE),
                    ft.Text("Bem-vindo", size=30, weight='bold', color=ft.Colors.BLACK_87),
                    ft.Text("Acesse sua conta para continuar", color=ft.Colors.BLACK_54),
                    
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT), # Espaçador
                    
                    self.username,
                    self.password,
                    
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    
                    ft.Button(
                        text="ENTRAR NO SISTEMA",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.BLUE,
                        ),
                        width=300,
                        height=50,
                        on_click=self.login_entrada
                    ),
                    
                    ft.TextButton(
                        content=ft.Text("Não possui cadastro? Cadastre-se agora!", size=12),
                        on_click=self.ir_para_cadastro
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            ),
            bgcolor=ft.Colors.WHITE,
            padding=40,
            width=400, 
            border_radius=20,
            shadow=ft.BoxShadow(
                blur_radius=15,
                color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
                offset=ft.Offset(0, 5),
            ),
        )

        self.page.add(login_card)
        self.page.update()

        #NOTIFCAÇÕES

    def mostrar_notificacao(self, mensagem, cor=ft.Colors.RED):
        snack = ft.SnackBar(
            content=ft.Text(mensagem, color=ft.Colors.WHITE),
            bgcolor=cor,
            duration=3000,
            show_close_icon=True
        )
        self.page.overlay.clear()
        self.page.overlay.append(snack)
        snack.open = True
        self.page.update()

        #ENTRADA
        
    def login_entrada(self, e):
        usuario = self.username.value.strip()
        senha = self.password.value.strip()

        if not usuario or not senha:
            # Chamada da notificação de erro
            self.mostrar_notificacao("Preencha todos os campos!")
            return
        
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT password FROM usuarios WHERE user_name = ?', (usuario,)
            )
            resultado = cursor.fetchone()

            if resultado is None:
                self.mostrar_notificacao("Usuario nao cadastrado!")
                self.password.value = ""
                self.page.update()
                return
            
            senha_existente = resultado[0]

            if senha == senha_existente:
                homeview = Home(self.page)
                homeview.build()
                self.mostrar_notificacao("Login realizado com sucesso!", ft.Colors.GREEN)

            else:
                self.mostrar_notificacao("Senha Incorreta!")
                self.password.value = ""
                self.page.update()


# CADASTRAR USUARIO

    def ir_para_cadastro(self, e):
        self.page.controls.clear()
        self.page.bgcolor = ft.Colors.WHITE
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.cad_user = ft.TextField(label="Usuario", color=ft.Colors.BLACK)
        self.cad_password = ft.TextField(label="Senha", password=True, can_reveal_password=True, color=ft.Colors.BLACK)

        cadastro_card = ft.Container(
            content= ft.Column(
                [
                    ft.Icon(ft.Icons.LOCK_PERSON_ROUNDED, size=50, color=ft.Colors.BLUE),
                    ft.Text("Cadastre-se por aqui!", size=30, weight='bold', color=ft.Colors.BLACK_87),
                    ft.Text("E faça parte do nosso grupo", color=ft.Colors.BLACK_54),
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT), # Espaçador

                    self.cad_user,
                    self.cad_password,
                    
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    
                    ft.Button(
                        text="CADASTRO",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.BLUE,
                        ),
                        width=300,
                        height=50,
                        on_click=self.cadastrar_usuario
                    ),
                    
                    ft.TextButton(
                        content=ft.Text("Ja possui cadastro? Entre por aqui!", size=12),
                        on_click=lambda e: self.build()

                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            ),
            bgcolor=ft.Colors.WHITE,
            padding=40,
            width=400, 
            border_radius=20,
            shadow=ft.BoxShadow(
                blur_radius=15,
                color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
                offset=ft.Offset(0, 5),
            ),
        )
        self.page.add(cadastro_card)
        self.page.update()

    def cadastrar_usuario(self, e):

        usuario = self.cad_user.value.strip()
        senha = self.cad_password.value.strip()

        if not usuario or not senha:
            # Chamada da notificação de erro
            self.mostrar_notificacao("Preencha todos os campos!")
            return
        
        try:
            # Conecta ao banco de dados
            with get_connection() as conn:
                cursor = conn.cursor()

                # Insere o novo usuário no banco
                cursor.execute(
                    'INSERT INTO usuarios (user_name, password) VALUES (?, ?)',
                    (usuario, senha)
                )
                conn.commit()

                self.cad_user.value = ""
                self.cad_password.value = ""
                self.build()
                self.mostrar_notificacao("Cadastro realizado com sucesso!", ft.Colors.GREEN)

        except Exception as ex:
            if "UNIQUE" in str(ex).upper():
                self.mostrar_notificacao("Este usuário já existe!")
            else:
                self.mostrar_notificacao(f"Erro ao cadastrar: {ex}")