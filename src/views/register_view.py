import flet as ft
from utils.notifications import build_snack
from services.user_service import crate_account

class Register:

    def __init__(self, page, router):
            self.page = page
            self.router = router

    def cadastrar_usuario(self, e):

        usuario = self.cad_user.value.strip()
        senha = self.cad_password.value.strip()

        if not usuario or not senha:
            # Chamada da notificação de erro
            build_snack(self.page, "Preencha todos os campos")
            return
        
        success, msg = crate_account(usuario, senha)

        if not success:
             build_snack(self.page, msg)
             return
        
        build_snack(self.page, msg, ft.Colors.GREEN)

        from views.login_view import Login
        self.router.go("login", Login)

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

