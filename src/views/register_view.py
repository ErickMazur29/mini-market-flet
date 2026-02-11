import flet as ft
from database.data import get_connection

class Register:

    def __init__(self, page, router):
            self.page = page
            self.router = router

            self.username = ft.TextField(label="Usuario", color=ft.Colors.BLACK)
            self.password = ft.TextField(label="Senha", password=True, can_reveal_password=True, color=ft.Colors.BLACK)

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


    def mostrar_notificacao(self, mensagem, cor=ft.Colors.RED):
        snack = ft.SnackBar(
            content=ft.Text(mensagem, color=ft.Colors.WHITE),
            bgcolor=cor,
            duration=1000,
            show_close_icon=True
        )
        self.page.overlay.clear()
        self.page.overlay.append(snack)
        snack.open = True
        self.page.update()

    def build(self):
        self.page.bgcolor = ft.Colors.WHITE
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.window.maximized = True

        self.cad_user = ft.TextField(label="Usuario", color=ft.Colors.BLACK)
        self.cad_password = ft.TextField(label="Senha", password=True, can_reveal_password=True, color=ft.Colors.BLACK)

        from views.login_view import Login

        cadastro_card = ft.Container(
            content= ft.Column(
                [
                    ft.Icon(ft.Icons.LOCK_PERSON_ROUNDED, size=50, color=ft.Colors.BLUE),
                    ft.Text("Cadastre-se por aqui!", size=30, weight='bold', color=ft.Colors.BLACK_87),
                    ft.Text("E faça parte do nosso grupo", color=ft.Colors.BLACK_54),
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),

                    self.cad_user,
                    self.cad_password,
                    
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    
                    ft.Button(
                        "CADASTRO",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.BLUE,
                        ),
                        width=300,
                        height=50,
                        on_click= self.cadastrar_usuario
                    ),
                    
                    ft.TextButton(
                        content=ft.Text("Ja possui cadastro? Entre por aqui!", size=12),
                        on_click= lambda e: self.router.go("login", Login)

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
        self.page.controls.clear()
        self.page.add(cadastro_card)
        self.page.update()

